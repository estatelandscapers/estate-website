/**
 * Estate Landscapers — site Worker.
 *
 * Two jobs:
 *   1. fetch()     — serve the static site, plus GET /api/instagram from cache.
 *   2. scheduled() — once a day, pull the latest Instagram posts into KV and
 *                    refresh the access token before it can expire.
 *
 * Everything else (every page, asset and redirect) is handled by the static
 * assets binding exactly as before, so this cannot break the site: if the
 * Instagram side fails, the endpoint returns an empty list and the website
 * quietly keeps its placeholder squares.
 *
 * Required once, in Cloudflare:
 *   - KV namespace bound as IG (see wrangler.jsonc)
 *   - secret IG_TOKEN   (long-lived Instagram access token)
 *   - var    IG_USER_ID (numeric Instagram user id)
 * See INSTAGRAM-API-SETUP.md for the click-by-click.
 */

const GRAPH = 'https://graph.instagram.com';
const CACHE_KEY = 'feed';
const TOKEN_KEY = 'token';       // current token lives in KV once refreshed
const WANT = 8;                  // posts to keep; the site uses the first four

/** Tokens are long and often arrive with stray whitespace or wrapping quotes
 *  from a copy-paste. Clean those rather than fail with "cannot parse". */
function clean(t) {
  return (t || '').trim().replace(/^["']|["']$/g, '').replace(/\s+/g, '');
}

async function currentToken(env) {
  const stored = env.IG ? await env.IG.get(TOKEN_KEY) : null;
  return clean(stored || env.IG_TOKEN);
}

/** Pull the latest media and store a trimmed, safe subset. */
async function refreshFeed(env) {
  if (!env.IG) return { ok: false, error: 'KV namespace IG not bound — Instagram not enabled yet' };
  const token = await currentToken(env);
  if (!token) return { ok: false, error: 'IG_TOKEN not configured' };

  // "me" resolves to whichever account the token belongs to, so no account id
  // is needed and it can never be pointed at the wrong one.
  const fields = 'id,caption,media_type,media_url,thumbnail_url,permalink,timestamp';
  const url = `${GRAPH}/me/media?fields=${fields}&limit=25&access_token=${token}`;
  const res = await fetch(url, { cf: { cacheTtl: 0 } });
  if (!res.ok) return { ok: false, error: `media fetch ${res.status}: ${(await res.text()).slice(0, 200)}` };

  const data = await res.json();
  const posts = (data.data || [])
    .filter((m) => m.media_type === 'IMAGE' || m.media_type === 'CAROUSEL_ALBUM' || m.thumbnail_url)
    .slice(0, WANT)
    .map((m) => ({
      image: m.media_type === 'VIDEO' ? m.thumbnail_url : m.media_url,
      permalink: m.permalink,
      caption: (m.caption || '').split('\n')[0].slice(0, 140),
    }))
    .filter((p) => p.image && p.permalink);

  await env.IG.put(CACHE_KEY, JSON.stringify({ posts, updated: new Date().toISOString() }));
  return { ok: true, count: posts.length };
}

/** Long-lived tokens last 60 days; refreshing one resets the clock. Daily is fine. */
async function refreshToken(env) {
  if (!env.IG) return { ok: false, error: 'KV namespace IG not bound' };
  const token = await currentToken(env);
  if (!token) return { ok: false, error: 'no token' };
  const res = await fetch(`${GRAPH}/refresh_access_token?grant_type=ig_refresh_token&access_token=${token}`);
  if (!res.ok) return { ok: false, error: `refresh ${res.status}` };
  const data = await res.json();
  if (data.access_token) {
    await env.IG.put(TOKEN_KEY, data.access_token);
    return { ok: true, expires_in: data.expires_in };
  }
  return { ok: false, error: 'no access_token in response' };
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    if (url.pathname === '/api/instagram') {
      const cached = env.IG ? await env.IG.get(CACHE_KEY) : null;
      return new Response(cached || JSON.stringify({ posts: [] }), {
        headers: {
          'content-type': 'application/json; charset=utf-8',
          'cache-control': 'public, max-age=1800',
          'access-control-allow-origin': '*',
        },
      });
    }

    // Config check. Reports only whether each piece is present — never a value —
    // so setup problems can be diagnosed in one click.
    if (url.pathname === '/api/instagram/status') {
      let cached = null;
      try { cached = env.IG ? JSON.parse((await env.IG.get(CACHE_KEY)) || 'null') : null; } catch (e) {}
      return Response.json({
        worker: true,
        kv_bound: !!env.IG,
        user_id_set: !!env.IG_USER_ID,
        token_set: !!(await currentToken(env)),
        token_length: (await currentToken(env)).length,   // a real token is ~150-200 chars
        token_prefix: (await currentToken(env)).slice(0, 3),
        refresh_key_set: !!env.IG_REFRESH_KEY,
        refresh_key_length: clean(env.IG_REFRESH_KEY).length,
        posts_cached: cached && cached.posts ? cached.posts.length : 0,
        last_updated: (cached && cached.updated) || null,
      });
    }

    // Manual trigger, so the feed can be filled immediately after setup without
    // waiting for the nightly run. Requires the same secret as configuration.
    if (url.pathname === '/api/instagram/refresh') {
      // The key is compared with whitespace stripped, since secrets are often
      // pasted with a stray newline. And while the cache is still empty there
      // is nothing to protect, so the first fill needs no key at all.
      let empty = true;
      try { empty = !env.IG || !(await env.IG.get(CACHE_KEY)); } catch (e) {}
      const given = clean(url.searchParams.get('key'));
      const want = clean(env.IG_REFRESH_KEY);
      if (!empty && (!want || given !== want)) {
        return new Response('Not found', { status: 404 });
      }
      const feed = await refreshFeed(env);
      const tok = await refreshToken(env);
      return Response.json({ feed, token: tok });
    }

    return env.ASSETS.fetch(request);
  },

  async scheduled(event, env, ctx) {
    ctx.waitUntil((async () => {
      const feed = await refreshFeed(env);
      const tok = await refreshToken(env);
      console.log('instagram cron', JSON.stringify({ feed, token: tok }));
    })());
  },
};

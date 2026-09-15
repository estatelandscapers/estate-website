# Instagram feed — one-time setup (then it runs itself)

When this is done, the four squares on `/residential/` show your four latest
Instagram posts. A Cloudflare cron job refreshes them **every day at 4:17am
Sydney time** and renews the access token automatically, so it never expires.
No weekly work.

Total time: about 25 minutes, once.

---

## Part A — Instagram side (about 10 minutes)

**A1. Make the account Professional.**
Instagram app → your profile → ☰ → Settings and privacy → Account type and
tools → **Switch to professional account** → choose *Business* → pick a
category (Landscaping / Home Improvement). Nothing about your posts changes.

**A2. Link it to a Facebook Page.**
Same menu → *Share to other apps* / *Page* → link to your Estate Landscapers
Facebook Page. If there isn't one, create a bare Page — it's just the
credential Meta requires; you never have to post to it.

**A3. Create a Meta app.**
Go to **developers.facebook.com** → log in with the Facebook account that
manages the Page → *My Apps* → **Create App**.
- Use case: **Other** → App type: **Business** → name it `Estate Website Feed`.
- On the app dashboard: **Add product** → find **Instagram** → *Set up*.
- Choose **Instagram API with Instagram Login** (not "with Facebook Login").

**A4. Generate the access token.**
In the left menu: **Instagram** → *API setup with Instagram login*.
- Step 1 *Generate access tokens* → **Add account** → log in with the
  Estate Landscapers Instagram account → approve the permissions.
- The page then shows an **Instagram access token** (a long string starting
  `IG...`) and, above it, the **Instagram user ID** (a long number).
- **Copy both. Do not paste them into email or chat** — treat the token like a
  password. Put them straight into Cloudflare in Part B.

> The token Meta gives you here is already long-lived (60 days). Our Worker
> refreshes it daily, which resets the 60-day clock each time, so it stays
> valid indefinitely as long as the site is deployed.

---

## Part B — Cloudflare side (about 10 minutes)

**B1. Create the storage namespace.**
Cloudflare dashboard → **Storage & Databases** → **KV** → *Create namespace* →
name it `estate-instagram` → Create. Copy the **Namespace ID** it shows.

**B2. Put that ID into the repo.**
Edit `wrangler.jsonc` (GitHub web editor is fine). The Instagram block is
commented out at the bottom of the file — follow the instructions in there:
remove the closing `}` after the assets block, then paste the commented block
back in uncommented, with your real Namespace ID and Instagram user ID:

```jsonc
  ,
  "kv_namespaces": [
    { "binding": "IG", "id": "abc123...your namespace id..." }
  ],
  "vars": {
    "IG_USER_ID": "17841400000000000"
  },
  "triggers": {
    "crons": ["17 18 * * *"]
  }
}
```

Commit. Until you do this, the site deploys normally and the Instagram
endpoint just returns an empty list — nothing breaks.

> The user ID is not a secret — it's fine in the repo. The **token is**, so it
> goes in as a secret instead, below.

**B3. Add the token as a secret.**

> Choose type **Secret**, not Variable. Plain Variables defined in the
> dashboard are replaced by whatever `wrangler.jsonc` contains on the next
> deploy, so a token added as a Variable will disappear. Secrets are stored
> separately and survive every deploy.
Cloudflare → **Workers & Pages** → `estate-website` → **Settings** →
**Variables and Secrets** → *Add*:
- Type **Secret**, name `IG_TOKEN`, value = the token from A4 → Save.
- Add a second **Secret** named `IG_REFRESH_KEY`, value = any random phrase you
  invent (e.g. `estate-refresh-8842`). This just protects the manual refresh
  URL in B5.

**B4. Deploy.**
Push the repo (or hit *Retry deployment*). The build log should end with
wrangler uploading and mentioning a **schedule** — that's the cron job
registering. From here it runs daily by itself.

**B5. Fill the feed immediately** (optional — otherwise it fills overnight).
Visit, in your browser:

```
https://estate-website.estatelandscapers.workers.dev/api/instagram/refresh?key=YOUR_IG_REFRESH_KEY
```

You should see a small JSON response like
`{"feed":{"ok":true,"count":8},"token":{"ok":true,"expires_in":5183944}}`.
Then open `/residential/` and the four squares should be your posts.

---

## Diagnose in one click

Open (no key needed):

```
https://estate-website.estatelandscapers.workers.dev/api/instagram/status
```

It reports what's configured, never any values:

```json
{"worker":true,"kv_bound":true,"user_id_set":true,"token_set":true,
 "refresh_key_set":true,"posts_cached":8,"last_updated":"..."}
```

Any `false` is your next step. `worker:true` means the Worker is live.

## If the refresh URL shows the site's 404 page

Two causes, in order of likelihood:

1. **The Worker isn't deployed yet** — check the build log ends with a
   successful wrangler upload that lists your bindings (`env.IG`, `env.ASSETS`).
2. **`IG_REFRESH_KEY` isn't set**, or the `?key=` value doesn't match it
   exactly. The endpoint deliberately returns "Not found" rather than an error
   message, so a wrong key looks like a missing page.

(The config includes `run_worker_first` for `/api/*`, which is what stops
Cloudflare's asset router from answering those paths itself.)

## Checking it later

- **Is the feed alive?** Open
  `https://www.estatelandscapers.com.au/api/instagram` — you should see JSON
  with your posts and an `updated` timestamp from within the last day.
- **Did the cron run?** Cloudflare → `estate-website` → *Logs* (or
  *Observability*) shows an `instagram cron` line each night with the result.
- **Nothing showing?** The site falls back to `public/instagram.json`, and if
  that's empty, to the labelled placeholder squares. It never breaks the page.

## If you ever need to revoke

Delete the `IG_TOKEN` secret in Cloudflare and the feed stops; remove the app
in developers.facebook.com to cut access entirely. Nothing else on the site
depends on it.

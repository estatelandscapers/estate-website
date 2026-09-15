# Instagram feed endpoint — spec for the quote tool

Website expects: GET /api/public/instagram → { "posts": [ { "image": url,
"permalink": url, "caption": str }, ... ] } (first 4 used). CORS: same
SITE_ORIGIN handling as /api/public/enquiry.

Tool-side (mirror the Places fetcher pattern):
1. Env: IG_ACCESS_TOKEN (long-lived, 60-day), IG_USER_ID.
2. Daily job: GET https://graph.instagram.com/{IG_USER_ID}/media
   ?fields=id,caption,media_type,media_url,thumbnail_url,permalink&limit=12
   &access_token=... → keep media_type IMAGE or CAROUSEL_ALBUM (use media_url;
   thumbnail_url for VIDEO if included) → cache newest 8 in settings.
3. Token self-refresh in the same job when <10 days to expiry:
   GET https://graph.instagram.com/refresh_access_token
   ?grant_type=ig_refresh_token&access_token=CURRENT — store the new token
   (persist to settings; env is only the seed).
4. Endpoint serves the cache; empty cache → { "posts": [] } (site then keeps
   its placeholder slots).

One-time setup (Smit):
1. Instagram app → Settings → switch account to Professional (Business).
2. Link it to a Facebook Page (create a bare one if none exists).
3. developers.facebook.com → Create App → add "Instagram API with Instagram
   Login" → generate a long-lived access token for the account, note the user id.
4. Put IG_ACCESS_TOKEN + IG_USER_ID into Railway. Never paste tokens in chat.

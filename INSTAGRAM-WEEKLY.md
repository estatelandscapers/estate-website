# Instagram on the website — the no-backend way

The four "Recent post" squares on /residential/ fill themselves from
`public/instagram.json`. Updating it takes about three minutes a week.

1. Open Instagram on a computer, find a post you want to show.
2. Save the image: right-click → Save image as → into
   `public/assets/img/instagram/` (name it anything, e.g. `2026-09-a.jpg`).
3. Copy the post's link (⋯ → Copy link).
4. Edit `public/instagram.json` and add an entry:

```json
{
 "posts": [
  {"image": "/assets/img/instagram/2026-09-a.jpg",
   "permalink": "https://www.instagram.com/p/XXXXXXXXX/",
   "caption": "Sir Walter turf and Colorbond, Rouse Hill"}
 ]
}
```

5. Repeat for four posts, commit, push. Done.

Notes
- Order matters: the first four entries fill the four squares.
- Keep images under ~1600px wide so the page stays fast.
- If the quote tool's `/api/public/instagram` endpoint is ever built (see
  INSTAGRAM-FEED-SPEC.md), it takes over automatically and this file becomes the
  fallback — no website change needed.

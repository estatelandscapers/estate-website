# Go-live runbook — estatelandscapers.com.au

Order matters. Each step has a check; do not move on until the check passes.
Photos can be updated any time after — they never block launch.

The one fact that shapes everything: the website is a Cloudflare Worker, and a
Worker can only answer on a custom domain whose **DNS zone is on Cloudflare**.
So the domain moves to Cloudflare first, then the site is attached to it.
Today the zone lives at Wix (`ns10/ns11.wixdns.net`). Moving it means every
record — email, the quote tool, DKIM — must exist on Cloudflare **before** the
nameservers change. `estate-dns-zone-reference.md` is the checklist for that.

---

## 0 · Push this build (10 min)

Clean-room extract, add `public/assets/img/`, push. Wait for green.

- [ ] Build log ends with a successful wrangler upload
- [ ] `https://estate-website.estatelandscapers.workers.dev/` loads
- [ ] `/api/instagram/status` returns `worker: true`

This build serves staging and production from the same files: `workers.dev`
gets `noindex`; the real domain is indexable; the apex redirects to `www`.

## 1 · Add the domain to Cloudflare (20 min, nothing changes live yet)

Cloudflare dashboard → **Add a site** → `estatelandscapers.com.au` → Free plan.
Cloudflare scans the existing DNS and shows what it found. Compare against
`estate-dns-zone-reference.md` **line by line** and add anything missing:

| Record | Must be | Proxy status |
|---|---|---|
| CNAME `quotes` → `om1abbai.up.railway.app` | present | **DNS only (grey cloud)** — Railway manages its own TLS |
| CNAME `bounce-zem` → `cluster89.zeptomail.com.au` | present | DNS only |
| MX records (Zoho) | all present, same priorities | n/a |
| TXT `v=spf1 include:zoho.com.au ~all` | present | n/a |
| TXT `zmail._domainkey` (Zoho DKIM) | copied fresh from Zoho admin, not retyped | n/a |
| TXT `23172954._domainkey` (ZeptoMail DKIM) | copied fresh from ZeptoMail, not retyped | n/a |
| TXT `MS=…`, `google-site-verification=…`, `zoho-verification=…`, `_railway-verify.quotes` | present | n/a |
| A `estatelandscapers.com.au` → 216.198.79.1, CNAME `www` → vercel | **leave for now** — replaced in step 3 | |

- [ ] Every row in the reference file has a matching record on Cloudflare

Cloudflare then shows **two nameservers** (e.g. `ada.ns.cloudflare.com`,
`kip.ns.cloudflare.com`). Write them down.

## 2 · Change the nameservers (5 min + waiting)

This happens at the **domain registrar**, which may or may not be Wix.
Check: Wix → Domains → `estatelandscapers.com.au` → if it shows "registered
with Wix", the nameserver setting is there under *Advanced → Name servers*.
If registered elsewhere (Crazy Domains, VentraIP, GoDaddy…), log in there.

Replace `ns10.wixdns.net` / `ns11.wixdns.net` with the two Cloudflare ones.

- [ ] Cloudflare's overview page shows the site as **Active** (minutes to a few hours)
- [ ] Send yourself an email to `enquiry@estatelandscapers.com.au` and reply from it — both arrive
- [ ] `https://quotes.estatelandscapers.com.au/api/public/enquiry/health` still returns `endpoint: ok`

If email breaks here, a DKIM or MX record was mistyped — fix on Cloudflare,
do not revert nameservers.

## 3 · Attach the website to the domain (10 min)

Cloudflare → **Workers & Pages → estate-website → Settings → Domains & Routes**
→ **Add → Custom domain**:

1. `www.estatelandscapers.com.au`
2. `estatelandscapers.com.au`

Cloudflare creates the DNS records itself. If it complains a record already
exists, delete the old `www` CNAME (vercel) and the old apex `A` record
(216.198.79.1) in the DNS tab first, then retry.

- [ ] `https://www.estatelandscapers.com.au/` shows the site with a valid padlock
- [ ] `https://estatelandscapers.com.au/` redirects to www
- [ ] `https://www.estatelandscapers.com.au/sitemap.xml` lists 75 URLs
- [ ] `https://www.estatelandscapers.com.au/api/instagram/status` returns the same JSON as staging

## 4 · Point the quote tool at the live domain (5 min)

Railway → the quote tool → Variables → `SITE_ORIGIN` → set to:

```
https://www.estatelandscapers.com.au,https://estatelandscapers.com.au
```

(keep the workers.dev origin in the list too if you still test there). Redeploy.

- [ ] Submit a real test enquiry on `https://www.estatelandscapers.com.au/residential/quote/`
      with a photo attached, **from a phone, on mobile data**
- [ ] The lead appears in the tool; the files land in OneDrive; the acknowledgement email arrives
- [ ] If "That didn't send": F12 → Console → the red line names CORS or CSP — send it

This is the one step that has never been verified end to end. Do not skip it.

## 5 · Search and analytics (15 min)

- **Search Console** — property `estatelandscapers.com.au` is already verified
  by TXT. Add the URL-prefix property `https://www.estatelandscapers.com.au/`,
  then **Sitemaps → submit** `https://www.estatelandscapers.com.au/sitemap.xml`.
  URL Inspection on the homepage → *Request indexing*.
- **GA4** — fires only on the production hostname by design. Open the site,
  then GA4 → Reports → Realtime: you should see yourself.
- **Google Business Profile** — set the website to `https://www.estatelandscapers.com.au/`.
- **DMARC** — Cloudflare DNS → add TXT `_dmarc` with value
  `v=DMARC1; p=none; rua=mailto:enquiry@estatelandscapers.com.au` (monitoring
  mode; tighten to `p=quarantine` after a fortnight of clean reports).

- [ ] Sitemap status "Success" in Search Console (can take a day)
- [ ] GA4 Realtime shows a visit

## 6 · Decommission — NOT today

Wait at least a week of email and quotes working normally on Cloudflare DNS.

- **Vercel** — delete the old project (the `www` CNAME no longer points there).
- **Wix** — cancel the *site/hosting plan* only. If Wix is also the **registrar**,
  keep the domain registration active — cancelling it loses the domain.
- Old `workers.dev` link — keep; it is your staging URL and is noindexed.

## If something goes wrong

- Site down but email fine → problem is step 3; the domain records. Re-add the
  custom domain.
- Email down → step 1 records; check DKIM/MX on Cloudflare against the reference.
- Form fails → step 4; `SITE_ORIGIN` or the console line.
- Everything down → nameserver change hasn't propagated; wait, do not flip back.

Rollback of last resort: set nameservers back to `ns10/ns11.wixdns.net`. The
Wix zone is intact until the Wix plan is cancelled — which is why step 6 waits.

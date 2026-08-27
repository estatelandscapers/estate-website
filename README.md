# Estate Landscapers — Website

Static site. Plain HTML, no build step, no dependencies. Deployed to Cloudflare via
Wrangler on every push to `main`.

## Structure

```
wrangler.jsonc      Cloudflare config — tells Wrangler that public/ holds the site
public/             Everything in here is served. Nothing outside it is.
  index.html        Front door — choose commercial or residential
  _headers          Staging noindex + security headers
SITEMAP.md          Full URL structure (Stage 1, approved separately)
estate-dns-zone-reference.md   DNS records to recreate before Wix is cancelled
```

Only `public/` reaches the internet. Documentation at the root is never served.

## Deploying

Push to `main`. Cloudflare runs `npx wrangler deploy` and publishes within a couple of
minutes. There is no build command to configure — if Cloudflare asks for one, leave it
empty.

## Before go-live

- [ ] **Delete `public/_headers` noindex block.** While it exists, Google will not index
      the site. This is deliberate for staging and fatal at launch.
- [ ] Replace the two photo slots in `index.html` (search for `PHOTO SLOT`)
- [ ] Swap the base64 logo for an SVG when the vector artwork is available
- [ ] DNS cutover per `estate-dns-zone-reference.md`

## Conventions

- Real URLs, folder-per-page, trailing slash: `/residential/` → `public/residential/index.html`
- Canonical host is `www.estatelandscapers.com.au`
- Brand: `#1E5BFF` blue, black, white, `#F5F5F5`, Montserrat
- No stock photography of other people's landscaping
- No unverified figures on the site

## Build stages

1. ✅ Sitemap + front door
2. ✅ Residential landing + commercial landing
3. Service page templates, Estate Standard, About
4. Forms → Railway quote tool → OneDrive → acknowledgement emails
5. Remaining service pages, Insights, garden care, contact, 404, legal, schema, redirects
6. Mobile QA, Core Web Vitals, accessibility
7. DNS cutover

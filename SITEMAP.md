# Estate Landscapers — Site Structure

**Stage 1 deliverable · 27 Aug 2026 · for approval before Stage 2**

Real, indexable URLs throughout (brief §5). Every path is a folder with a trailing
slash, so each one is its own file on disk and its own page in Google. Canonical host is
**`www.estatelandscapers.com.au`** — the bare domain 301s to www, because www is the
version Google currently has indexed.

---

## The shape

```
/                                   Front door — choose commercial or residential
│
├── /commercial/                    NSW-wide · contractor language · REQUEST A TENDER
│   ├── /builders-developers/
│   ├── /councils-government/
│   ├── /strata-body-corporate/
│   ├── /commercial-property/
│   ├── /capabilities/              Capability statement, downloadable
│   └── /tender/                    Tender request form (larger file allowance)
│
├── /residential/                   Sydney only · warmer · GET A QUOTE
│   ├── /new-build-landscaping/
│   ├── /landscape-construction/
│   ├── /retaining-walls/
│   ├── /concrete-driveways/
│   ├── /paving/
│   ├── /earthworks-excavation/
│   ├── /landscape-drainage/
│   ├── /fencing-gates/
│   ├── /turf-soft-landscaping/
│   ├── /planting-gardens/
│   ├── /decking-outdoor-structures/
│   ├── /landscape-design/
│   ├── /irrigation/
│   ├── /garden-care/               Year-round care guide + product links
│   └── /quote/                     Qualification gate → enquiry form
│
├── /the-estate-standard/           How you build, and why it costs what it costs
├── /about/                         Founded 2019 · no individual names
├── /projects/                      Structure built, empty at launch (noindex until populated)
│   └── /projects/<slug>/
├── /insights/                      4–6 articles at launch
│   └── /insights/<slug>/
├── /contact/
│
├── /privacy/
├── /terms/
├── /404.html
├── /robots.txt
└── /sitemap.xml                    Generated at build, submitted to Search Console
```

**32 pages at launch**, plus articles and the empty projects structure.

---

## Three decisions inside that structure

**`/residential/` is itself the "Residential Landscaping" page.** The brief listed
Residential Landscaping as a service page, but a landing page and a service page for the
same term would compete with each other in search — Google picks one and buries the
other. So the landing page carries that term, and the thirteen specific services sit
beneath it.

**"Maintenance" is now `/garden-care/`.** You decline maintenance work — mowing, hedging,
weeding, irrigation repairs — and the qualification gate exists to turn those enquiries
away. A page titled "Maintenance" would rank for exactly the enquiries you don't want and
send them straight to your form. "Garden care guide" reads as advice, which is what it
is, and attracts the homeowner researching rather than the one looking to hire a mower.

**`/projects/` is built empty and blocked from indexing.** The structure exists from day
one so photos drop in without a rebuild, but an empty section that Google indexes is a
thin-content signal against the whole site. The noindex comes off the day the first
project goes live.

---

## Suburb pages — proposed, not built yet

For a Sydney trade these are usually the highest-return pages, and they have to sit in
the URL structure from the beginning because changing URLs after Google learns them costs
you the ranking. Proposed pattern:

```
/residential/landscaping-kellyville/
/residential/landscaping-rouse-hill/
/residential/landscaping-castle-hill/
…
```

Roughly ten across the Hills District and North West, each with genuinely local content —
soil conditions, council requirements, actual jobs done there — not the same page with
the suburb name swapped. Google has been demoting the swap-the-name version for years.

Build them in Stage 5. **Say if you'd rather not**, and I'll leave the pattern out of the
structure entirely rather than half-build it.

---

## Navigation

The two paths are separate sites sharing a shell. Commercial navigation never shows
residential services, and vice versa — a builder looking for a tender should never land
on turf and planting.

| | Commercial | Residential |
|---|---|---|
| Nav | Sectors · Capabilities · The Estate Standard · About · Contact | Services · The Estate Standard · Process · About · Contact |
| CTA | REQUEST A TENDER | GET A QUOTE |
| Reviews | Not shown | Shown |
| Service area | NSW | Sydney |

Both keep a small "switch" control back to the front door, and both footers carry the
Infra Landscapers link — two of the three agreed civil handoffs, the third being the
band above the commercial tender form.

---

## Redirects at cutover

Search Console shows one indexed URL, so this is short:

| Old | New |
|---|---|
| `https://www.estatelandscapers.com.au/` | `/` — unchanged |
| *(the four dropped pages)* | pending the not-indexed export |

Plus the standard rules: bare domain → www, any `/index.html` → `/`, trailing slash
enforced.

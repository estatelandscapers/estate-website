#!/usr/bin/env python3
"""Generate project case-study pages from data/projects.json.

  python3 tools/gen-projects.py            # writes src/pages/projects/*.html + src/pages/projects.html
  python3 tools/gen-projects.py --import X.xlsx   # refresh data/projects.json from the project sheet first

Rules baked in (do not relax): no $ values, no dates/durations, no client names
without permission, spreadsheet-internal phrasing scrubbed.
"""
import json, re, sys, os, html as H

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data', 'projects.json')
OUTD = os.path.join(ROOT, 'src', 'pages', 'projects')

# ---------------------------------------------------------------- import ----
DELIV = {  # code -> (name, unit)
 'PL': ('Establishment, supervision & insurances', 'sum'), 'EW': ('Earthworks & site cleanup', 'shift'),
 'GT': ('Turf supply & install', 'm²'), 'GM': ('Garden mix & mulch', 'm²'), 'ST': ('Edging at change of material', 'm'),
 'RW': ('Retaining wall (to 1.2 m)', 'm'), 'CP': ('Concrete driveway', 'm²'), 'PW': ('Weedmat & decorative rock', 'm²'),
 'FC': ('Colorbond fence 1.8 m', 'm'), 'FA': ('Aluminium fence ≤1.2 m', 'm'), 'FG': ('Gates', 'ea'),
 'FT': ('Timber sleeper under fence', 'ea'), 'PC': ('Stepping stones', 'ea'), 'RM': ('Soil / concrete removal', 'load'),
 'RD': ('Demolition works', 'day'), 'TR': ('Plants, shrubs & trees', 'lot'), 'AL': ('Letterbox', 'ea'),
 'AC': ('Clothesline', 'ea'), 'SC2': ('Construction waste disposal', 'm³'),
}
SCRUB = re.compile(r'(\$|\bcurrent (project )?(data|information)\b|\bnot record|\bdoes not (yet )?(record|state|specify|list)|\b(19|20)\d\d\b|\b\d+\s*(weeks?|months?|days?)\b|\bvalue band\b|\btimeline\b|\binformation currently available\b)', re.I)

QTY_PATTERNS = [
 (r'\s*\((?:approx\.?|approximately|~)?[^)]*?\d[^)]*?(?:loads?|tonnes?|t)\)', ''),
 (r'\b(?:approximately|approx\.?|about|~)?\s*\d[\d,.]*\s*(?:m²|m2|sqm|square metres?)\s*(?:of\s+)?', ' '),
 (r'\b(?:approximately|approx\.?|about|~)?\s*\d[\d,.]*\s*tonnes?\s*(?:of\s+)?', ' '),
 (r'\b\d+\s*ea\b', ' '),
 (r',?\s*up to one load\s*/?\s*', ' '),
 (r'\bcomprising\s+(?=plus\b|and\b)', ''),
]

def strip_qty(t):
    """Quantities — areas, tonnages, counts, truck loads — are never published.
    Product dimensions (a 1.8 m fence, a wall up to 1.2 m high) are specification
    and stay."""
    if not t: return t
    s = str(t)
    for pat, rep in QTY_PATTERNS: s = re.sub(pat, rep, s, flags=re.I)
    s = re.sub(r'\s{2,}', ' ', s)
    s = re.sub(r'\s+([.,;])', r'\1', s)
    s = re.sub(r',\s*\.', '.', s).strip(' ,;')
    s = re.sub(r'^(?:plus|and)\s+', '', s, flags=re.I)
    if s and s[0].islower(): s = s[0].upper() + s[1:]
    if s and s[-1] not in '.!?': s += '.'
    return s

def scrub(text):
    if not text: return ''
    out = []
    for sent in re.split(r'(?<=[.!?])\s+', str(text).strip()):
        clauses = [c.strip() for c in re.split(r';\s*', sent) if c.strip()]
        keep = [c for c in clauses if not SCRUB.search(c)]
        if not keep: continue
        s = '; '.join(keep)
        if s[-1] not in '.!?': s += '.'
        out.append(s)
    return ' '.join(out).strip()

TIERS = {'basic', 'standard', 'premium', 'included'}
def norm_deliv(name, pkg, qty, spec):
    # The sheet sometimes carries the description in the tier cell; a tier is only ever one of TIERS.
    pkg = str(pkg or '').strip()
    if pkg and pkg.lower() not in TIERS:
        spec = (str(spec or '').strip() + ' ' + pkg).strip() if spec else pkg
        pkg = ''
    qty = scrub(qty).rstrip('.') if qty else ''   # durations ("12 months") are not published
    return {'name': name, 'tier': pkg.title() if pkg else '', 'qty': qty, 'spec': strip_qty(scrub(spec))}

def do_import(xlsx):
    import openpyxl
    wb = openpyxl.load_workbook(xlsx, data_only=True); ws = wb['Projects']
    rows = list(ws.iter_rows(min_row=3, values_only=True)); fields = [r[1] for r in rows[1:]]
    out = []
    for ci in range(4, ws.max_column):
        col = [r[ci] for r in rows[1:]]
        d = {f: v for f, v in zip(fields, col) if f and v not in (None, '')}
        if not d.get('Project name') or str(d.get('Publish on website?', 'No')).strip() != 'Yes': continue
        perm = str(d.get('Permission to name client?', 'No')).strip() == 'Yes'
        cons = [k.replace('Constraint: ', '') for k, v in d.items() if k.startswith('Constraint:') and str(v).strip() == 'Yes']
        deliv = []
        for code, (name, unit) in DELIV.items():
            if d.get(f'{code} · {name}') or any(k.startswith(code + ' · ') and 'quantity' not in k and 'material' not in k for k in d):
                pkg = next((v for k, v in d.items() if k.startswith(code + ' · ') and 'quantity' not in k and 'material' not in k), None)
                qty = next((v for k, v in d.items() if k.startswith(code + ' · quantity')), None)
                spec = next((v for k, v in d.items() if k.startswith(code + ' · material')), None)
                deliv.append(norm_deliv(name, pkg, f'{qty} {unit}' if qty not in (None, '') else '', spec))
        for n in (1, 2, 3):
            if d.get(f'Custom {n} · name'):
                deliv.append(norm_deliv(d[f'Custom {n} · name'], d.get(f'Custom {n} · package'), str(d.get(f'Custom {n} · quantity + unit', '') or ''), d.get(f'Custom {n} · material / spec')))
        faqs = [{'q': d[f'FAQ {n} — question'], 'a': scrub(d.get(f'FAQ {n} — answer'))} for n in (1, 2, 3) if d.get(f'FAQ {n} — question')]
        faqs = [f for f in faqs if f['a']]
        out.append({
            'name': d['Project name'], 'slug': d['URL slug'], 'sector': d['Sector'], 'site_type': d.get('Site type', ''),
            'featured': str(d.get('Featured on landing page?', 'No')).strip() == 'Yes',
            'suburb': d.get('Suburb', ''), 'postcode': str(d.get('Postcode', '') or ''), 'region': d.get('Region', ''), 'council': d.get('Council / LGA', ''),
            'client': d.get('Client / principal contractor', '') if perm else '', 'builder': d.get('Builder (new builds)', '') if perm else '',
            'designer': d.get('Architect / landscape designer', '') if perm else '',
            'drawings': d.get('Drawings supplied', ''), 'area_m2': d.get('Landscape area (m²)'), 'slope': d.get('Slope', ''),
            'access': d.get('Access type', ''), 'ground': d.get('Ground / soil', ''), 'existing': d.get('Existing condition', ''),
            'constraints': cons, 'other_constraints': scrub(d.get('Other constraints')),
            'deliverables': deliv,
            'brief': scrub(d.get('Client brief')), 'challenge': scrub(d.get('The challenge')), 'approach': scrub(d.get("Estate's approach")),
            'technical': scrub(d.get('Technical detail worth noting')), 'outcome': scrub(d.get('Outcome')), 'aftercare': scrub(d.get('Handover / aftercare')),
            'review': scrub(d.get('Client review — quote')), 'reviewer': d.get('Reviewer first name', '') if perm else '', 'review_source': d.get('Review source', ''),
            'keyword': d.get('Primary keyword', ''), 'keywords': [k.strip() for k in str(d.get('Secondary keywords', '')).split(',') if k.strip()],
            'title': d.get('Page title', ''), 'meta': scrub(d.get('Meta description')), 'faqs': faqs,
            'related': [r.strip() for r in str(d.get('Related service pages', '')).split(',') if r.strip()],
            'nearby': [r.strip() for r in str(d.get('Nearby suburbs served', '')).split(',') if r.strip()],
            'hero_alt': d.get('Hero image alt text', ''),
        })
    os.makedirs(os.path.dirname(DATA), exist_ok=True)
    json.dump(out, open(DATA, 'w'), indent=1, ensure_ascii=False)
    print(f'imported {len(out)} publishable projects → data/projects.json')

# ------------------------------------------------------------- templates ----
SERVICE_URL = {
 'Retaining Walls': '/residential/retaining-walls/', 'New Build Landscaping': '/residential/new-build-landscaping/',
 'Fencing & Gates': '/residential/fencing-gates/', 'Fencing': '/residential/fencing-gates/', 'Turf & Soft Landscaping': '/residential/turf-soft-landscaping/',
 'Earthworks & Drainage': '/residential/earthworks-excavation/', 'Earthworks': '/residential/earthworks-excavation/',
 'Concrete & Driveways': '/residential/concrete-driveways/', 'Concrete & Paving': '/residential/concrete-driveways/', 'Paving & Concrete': '/residential/paving/',
 'Irrigation': '/residential/irrigation/', 'Edging': '/residential/garden-edging/', 'Garden Beds & Planting': '/residential/planting-gardens/',
 'Planting & Soft Landscaping': '/residential/planting-gardens/', 'Decking & Outdoor Living': '/residential/decking-outdoor-structures/',
 'Landscape Maintenance': '/residential/care/', 'Site Preparation & Demolition': '/residential/earthworks-excavation/',
 'Subdivision Landscaping': '/commercial/builders-developers/', 'Commercial Landscaping': '/commercial/commercial-property/',
 'Industrial Landscaping': '/commercial/commercial-property/', 'Public Realm Landscaping': '/commercial/councils-government/',
 'Education Landscaping': '/commercial/councils-government/', 'Acreage Landscaping': '/residential/landscape-construction/',
 'Bio Basins': '/commercial/capabilities/', 'Vertical Green Walls': '/commercial/capabilities/',
}
SERVICE_LABEL = {'Turf & Soft Landscaping': 'Turfing', 'Concrete & Driveways': 'Concrete works',
                 'Concrete & Paving': 'Concrete works', 'Paving & Concrete': 'Paving',
                 'Earthworks & Drainage': 'Earthworks & excavation', 'Earthworks': 'Earthworks & excavation',
                 'Garden Beds & Planting': 'Planting & gardens', 'Planting & Soft Landscaping': 'Planting & gardens',
                 'Landscape Maintenance': 'Care', 'Site Preparation & Demolition': 'Earthworks & excavation',
                 'Decking & Outdoor Living': 'Decking & outdoor structures', 'Edging': 'Garden edging',
                 'Fencing': 'Fencing & gates'}
def e(s): return H.escape(str(s or ''), quote=False)
def slot(label, desc, key=None):
    k = f' data-key="{key}"' if key else ''
    return f'<div class="plate"><div class="slot"{k}><b>{e(label)}</b><span>{e(desc)}</span></div></div>'

RES_SHOTS = ['Completed — wide shot of the finished yard', 'Completed — from the street or entry',
             'Completed — turf and garden beds', 'Completed — retaining wall or structure',
             'Completed — paving, driveway or path', 'Completed — detail worth noticing']
COM_SHOTS = ['Completed — wide shot of the delivered works', 'Completed — the key structure or planting',
             'Completed — detail at close range']
def gallery(p):
    shots = RES_SHOTS if is_res(p) else COM_SHOTS
    return ''.join(slot('Finished', s, f"project-{p['slug']}-g{i+1}") for i, s in enumerate(shots))
def is_res(p): return p['sector'] == 'Residential'
def sector_label(p): return 'Residential' if is_res(p) else 'Commercial'
def loc(p): return ', '.join(x for x in [p['suburb'], p['region']] if x)

def deliv_table(p):
    """Residential quotes carry Basic/Standard/Premium tiers; anything outside them reads
    Custom. Commercial work is priced to the drawings, so it gets no tier column."""
    if is_res(p):
        rows = ''.join(f'<tr><th scope="row">{e(d["name"])}</th><td>{e(d["tier"] or "Custom")}</td><td>{e(d["spec"])}</td></tr>' for d in p['deliverables'])
        head = '<tr><th>Deliverable</th><th>Tier</th><th>Specification</th></tr>'
    else:
        rows = ''.join(f'<tr><th scope="row">{e(d["name"])}</th><td>{e(d["spec"])}</td></tr>' for d in p['deliverables'])
        head = '<tr><th>Deliverable</th><th>Specification</th></tr>'
    return f'''<div class="tierwrap mt"><table class="tiers dl">
      <thead>{head}</thead>
      <tbody>{rows}</tbody></table></div>'''

def facts(p):
    items = [('Location', loc(p)), ('Council / LGA', p['council']), ('Site type', p['site_type']), ('Landscape area', f"{p['area_m2']} m²" if p['area_m2'] else ''),
             ('Slope', p['slope']), ('Access', p['access']), ('Ground', p['ground']), ('Existing condition', p['existing']), ('Drawings', p['drawings']),
             ('Designer', p['designer']), ('Builder', p['builder']), ('Client', p['client'])]
    return '<dl class="facts">' + ''.join(f'<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k, v in items if v) + '</dl>'

def constraints(p):
    if not p['constraints'] and not p['other_constraints']: return ''
    chips = ''.join(f'<span class="chip">{e(c)}</span>' for c in p['constraints'])
    other = f'<p class="sub" style="margin-top:12px">{e(p["other_constraints"])}</p>' if p['other_constraints'] else ''
    return f'<div class="chips mt">{chips}</div>{other}'

def faq_html(p): return ''.join(f'<li><h3>{e(f["q"])}</h3><p>{e(f["a"])}</p></li>' for f in p['faqs'])
def related(p):
    links = [(r, SERVICE_URL[r]) for r in p['related'] if r in SERVICE_URL]
    seen, out = set(), []
    for r, u in links:
        if u in seen: continue
        seen.add(u); out.append(f'<a class="chip" href="{u}">{e(SERVICE_LABEL.get(r, r))}</a>')
    return ''.join(out)
def review(p):
    if not p['review']: return ''
    who = f' — {e(p["reviewer"])}' if p['reviewer'] else ''
    src = f' · {e(p["review_source"])}' if p['review_source'] else ''
    return f'<blockquote class="quote mt"><p>“{e(p["review"])}”</p><footer>{who}{src}</footer></blockquote>'

def schema(p, url):
    kw = ', '.join([p['keyword']] + p['keywords'])
    art = {"@context": "https://schema.org", "@type": "Article", "headline": p['name'], "description": p['meta'], "url": url, "keywords": kw,
           "author": {"@type": "Organization", "name": "Estate Landscapers", "url": "https://www.estatelandscapers.com.au/"},
           "publisher": {"@type": "Organization", "name": "Estate Landscapers"},
           "contentLocation": {"@type": "Place", "name": p['suburb'], "address": {"@type": "PostalAddress", "addressLocality": p['suburb'], "postalCode": p['postcode'], "addressRegion": "NSW", "addressCountry": "AU"}},
           "about": {"@type": "Service", "serviceType": p['keyword'], "areaServed": [p['suburb']] + p['nearby'],
                     "provider": {"@type": "LandscapeContractor", "name": "Estate Landscapers", "legalName": "Apexx Enterprises Pty Ltd", "url": "https://www.estatelandscapers.com.au/"}}}
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "url": url, "mainEntity": [{"@type": "Question", "name": f['q'], "acceptedAnswer": {"@type": "Answer", "text": f['a']}} for f in p['faqs']]}
    crumb = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.estatelandscapers.com.au/"},
        {"@type": "ListItem", "position": 2, "name": "Projects", "item": "https://www.estatelandscapers.com.au/projects/"},
        {"@type": "ListItem", "position": 3, "name": p['name'], "item": url}]}
    return ''.join(f'<script type="application/ld+json">\n{json.dumps(x, ensure_ascii=False)}\n</script>\n' for x in (art, faq, crumb))

def page(p):
    res = is_res(p); url = '{{PAGE_URL}}'
    nav = 'residential' if res else 'commercial'
    cfg = {"path": f"/projects/{p['slug']}/", "nav": nav, "footer": nav, "title": p['title'], "description": p['meta']}
    cta_primary = ('/residential/quote/', 'Get a residential quote') if res else ('/commercial/tender/', 'Request a tender')
    cta_second = ('/commercial/tender/', 'Request a tender') if res else ('/residential/quote/', 'Get a residential quote')
    hero_alt = p['hero_alt'] or f"{p['name']} — completed landscape by Estate Landscapers"
    intro_lbl = 'The brief' if res else 'The scope'
    appr_lbl = 'How we approached it' if res else 'Delivery approach'
    outcome_cta = (f'<h2>Planning something similar in {e(p["suburb"])}?</h2><p>Send your plans and photos — the quote comes back itemised at the tier you choose, and we call you the same business day.</p>'
                   if res else '<h2>Have a landscaping, softscape and hardscape package to price?</h2><p>Send the drawings, civil set and program. We return a priced submission with the documentation your site requires.</p>')
    nearby = f'<p class="sub" style="margin-top:14px;font-size:.85rem">Also serving {e(", ".join(p["nearby"]))}.</p>' if p['nearby'] else ''
    aftercare = f'<h3 style="margin-top:22px">Handover and aftercare</h3><p class="sub" style="margin-top:8px">{e(p["aftercare"])}</p>' if p['aftercare'] else ''
    tech = f'<div class="panel good mt"><h3>Worth noting</h3><p>{e(p["technical"])}</p></div>' if p['technical'] else ''
    return f'''<!--CONFIG
{json.dumps(cfg, indent=1, ensure_ascii=False)}
-->
<section class="hero">
  <div class="shell">
    <div>
      <p class="eyebrow"><a href="/projects/" style="color:inherit;text-decoration:none">Projects</a> · {e(sector_label(p))} · {e(p['suburb'])}</p>
      <h1>{e(p['name'])}</h1>
      <p class="lead">{e(p['brief'])}</p>
      <p class="tags">{e(p['sector'])} · {e(p['site_type'])} · {e(loc(p))}</p>
      <div class="btn-row">
        <a class="btn" href="{cta_primary[0]}">{cta_primary[1]}</a>
        <a class="btn btn-o" href="/projects/">All projects</a>
      </div>
    </div>
    {slot('Hero photo', hero_alt, f"project-{p['slug']}-hero")}
  </div>
</section>

{{{{include creds}}}}

<section class="band">
  <div class="shell g2">
    <div>
      <p class="eyebrow">The site</p>
      <h2>{e(p['suburb'])}, in detail.</h2>
      {facts(p)}
    </div>
    <div>
      <p class="eyebrow">Constraints</p>
      <h2>What made it worth doing properly.</h2>
      <p class="sub" style="margin-top:10px">{e(p['challenge'])}</p>
      {constraints(p)}
    </div>
  </div>
</section>

<section class="band tint">
  <div class="shell g2">
    <div>
      <p class="eyebrow">{appr_lbl}</p>
      <h2>Sequenced so nothing gets done twice.</h2>
      <p class="sub" style="margin-top:10px">{e(p['approach'])}</p>
      {tech}
    </div>
    {slot('Progress photo', 'During works — the stage that shows the method', f"project-{p['slug']}-progress")}
  </div>
</section>

<section class="band">
  <div class="shell">
    <p class="eyebrow">Scope delivered</p>
    <h2>{'Every line, at the tier it was built.' if res else 'Every line of the package.'}</h2>
    <p class="sub">{"The same deliverable names and Basic / Standard / Premium tiers you'll see on your own quote." if res else 'Commercial packages are priced to the drawings and specification, so scope is listed without tiers.'}</p>
    {deliv_table(p)}
    <div class="chips mt">{related(p)}</div>
  </div>
</section>

<section class="band tint">
  <div class="shell">
    <p class="eyebrow">Gallery</p>
    <h2>{'The finished project.' if res else 'Delivered.'}</h2>
    <div class="g3 mt">
      {gallery(p)}
    </div>
  </div>
</section>

<section class="band">
  <div class="shell g2">
    <div>
      <p class="eyebrow">Outcome</p>
      <h2>What was handed over.</h2>
      <p class="sub" style="margin-top:10px">{e(p['outcome'])}</p>
      {aftercare}
      {review(p)}
      {nearby}
    </div>
    <div class="panel dark">{outcome_cta}
      <div class="btn-row"><a class="btn" href="{cta_primary[0]}">{cta_primary[1]}</a><a class="btn btn-o" href="{cta_second[0]}">{cta_second[1]}</a></div>
    </div>
  </div>
</section>

<section class="band tint">
  <div class="shell">
    <p class="eyebrow">Common questions</p>
    <h2>About this project.</h2>
    <ul class="faq">{faq_html(p)}</ul>
  </div>
</section>

{{{{include infra-{nav}}}}}

{schema(p, url)}'''

def card(p):
    return f'''      <a class="card" href="/projects/{p['slug']}/" data-sector="{'res' if is_res(p) else 'com'}">
        <div class="plate" data-hero="/projects/{p['slug']}/"></div>
        <div class="in"><h3>{e(p['name'])}</h3><p>{e(p['meta'])}</p>
        <p class="tags">{e(sector_label(p))} · {e(p['site_type'])} · {e(p['suburb'])}</p><span class="more">Read the case study →</span></div>
      </a>'''

def index(P):
    cfg = {"path": "/projects/", "nav": "shared", "footer": "shared",
           "title": "Landscaping Projects Sydney — Residential & Commercial Case Studies | Estate Landscapers",
           "description": "Fifteen Estate Landscapers projects across Sydney, NSW and QLD — duplexes, custom homes, subdivisions, industrial sites, schools and public domain. What was built, how it was engineered, and the constraints solved."}
    res = [p for p in P if is_res(p)]; com = [p for p in P if not is_res(p)]
    parts = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Projects", "url": "{{PAGE_URL}}", "description": cfg['description'],
             "hasPart": [{"@type": "Article", "headline": p['name'], "url": f"https://www.estatelandscapers.com.au/projects/{p['slug']}/"} for p in P]}
    return f'''<!--CONFIG
{json.dumps(cfg, indent=1, ensure_ascii=False)}
-->
<section class="hero">
  <div class="shell">
    <div>
      <p class="eyebrow">Projects</p>
      <h1>Built, documented, and <em>still standing behind it</em>.</h1>
      <p class="lead">{len(P)} projects across Sydney, NSW and QLD — {len(res)} residential, {len(com)} commercial — each with the constraints, the scope at tier level, and the engineering behind it.</p>
      <div class="btn-row"><a class="btn" href="/residential/quote/">Get a residential quote</a><a class="btn btn-o" href="/commercial/tender/">Request a tender</a></div>
    </div>
    {slot('Photo slot', 'A completed project — the strongest single image you have')}
  </div>
</section>

{{{{include creds}}}}

<section class="band" id="list">
  <div class="shell">
    <div class="chips center" role="tablist" aria-label="Filter projects">
      <button class="chip b" data-f="all" aria-pressed="true">All ({len(P)})</button>
      <button class="chip" data-f="res" aria-pressed="false">Residential ({len(res)})</button>
      <button class="chip" data-f="com" aria-pressed="false">Commercial ({len(com)})</button>
    </div>
    <div class="g3 mt" id="pgrid">
{chr(10).join(card(p) for p in P)}
    </div>
  </div>
</section>

<section class="cta">
  <div class="shell">
    <h2>Have a project with a complication in it?</h2>
    <p>Those are the ones we're built for. Send the drawings or the photos and we'll tell you how we'd approach it — including the engineering and approvals.</p>
    <div class="btn-row"><a class="btn" href="/commercial/tender/">Request a tender</a><a class="btn btn-o" href="/residential/quote/">Get a residential quote</a></div>
  </div>
</section>

{{{{include infra-residential}}}}

<script type="application/ld+json">
{json.dumps(parts, ensure_ascii=False)}
</script>
'''

def featured_block(P, res=True, n=3):
    pool = [p for p in P if is_res(p) == res]
    pick = [p for p in pool if p['featured']][:n] or pool[:n]
    eyebrow = 'Featured projects'
    h = 'Recent residential projects.' if res else 'Recent commercial projects.'
    return f'''<section class="band">
  <div class="shell">
    <p class="eyebrow">{eyebrow}</p>
    <h2>{h}</h2>
    <div class="g3 mt">
{chr(10).join(card(p) for p in pick)}
    </div>
    <div class="btn-row mt"><a class="btn btn-o" href="/projects/">All projects →</a></div>
  </div>
</section>
'''

if __name__ == '__main__':
    if '--import' in sys.argv: do_import(sys.argv[sys.argv.index('--import') + 1])
    P = json.load(open(DATA))
    os.makedirs(OUTD, exist_ok=True)
    for f in os.listdir(OUTD):
        if f.endswith('.html'): os.remove(os.path.join(OUTD, f))
    for p in P: open(os.path.join(OUTD, p['slug'] + '.html'), 'w').write(page(p))
    open(os.path.join(ROOT, 'src', 'pages', 'projects.html'), 'w').write(index(P))
    open(os.path.join(ROOT, 'src', 'partials', 'featured-residential.html'), 'w').write(featured_block(P, True))
    open(os.path.join(ROOT, 'src', 'partials', 'featured-commercial.html'), 'w').write(featured_block(P, False))
    print(f'generated {len(P)} project pages + index + featured partials')

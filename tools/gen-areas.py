#!/usr/bin/env python3
"""Residential areas served: one page per region on the service map, listed by
suburb (no postcodes). Run: python3 tools/gen-areas.py"""
import os, json, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
from pagekit import e
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOME = 'https://www.estatelandscapers.com.au'

REGIONS = [
 ('the-hills', 'The Hills', 'New builds and acreage on clay. Drainage before surfaces is non-negotiable, and most yards arrive as bare graded pads after the builder leaves. Our yard is here, in Rouse Hill.',
  ['Rouse Hill', 'Kellyville', 'North Kellyville', 'Kellyville Ridge', 'Beaumont Hills', 'Castle Hill', 'Baulkham Hills', 'Bella Vista', 'Winston Hills', 'Annangrove', 'Glenhaven', 'Kenthurst', 'Dural', 'Round Corner', 'Cherrybrook'],
  ['rouse-hill-boutique-home-landscaping', 'north-kellyville-boutique-home-landscaping', 'dural-acreage-landscaping-native-planting']),
 ('northern-beaches', 'Northern Beaches', 'Coastal exposure, sand and salt. Material selection matters more here than anywhere: galvanising, drainage and species choice decide whether a yard lasts five years or fifteen.',
  ['Manly', 'Fairlight', 'Balgowlah', 'Balgowlah Heights', 'North Balgowlah', 'Clontarf', 'Seaforth', 'Manly Vale', 'North Manly', 'Queenscliff', 'Freshwater', 'Curl Curl', 'Brookvale', 'Dee Why', 'Cromer', 'Narraweena', 'Beacon Hill', 'Allambie Heights', 'Oxford Falls', 'Frenchs Forest', 'Forestville', 'Killarney Heights', 'Belrose', 'Davidson', 'Terrey Hills', 'Duffys Forest', 'Cottage Point', 'Collaroy', 'Collaroy Plateau', 'Wheeler Heights', 'Narrabeen', 'North Narrabeen', 'Elanora Heights', 'Ingleside', 'Warriewood', 'Mona Vale', 'Bayview', 'Church Point', 'Scotland Island', 'Newport', 'Bilgola', 'Avalon Beach', 'Clareville', 'Whale Beach'],
  []),
 ('upper-north-shore', 'Upper North Shore', 'Large established gardens on slope, with tree protection zones and bushfire considerations. Works are staged around root zones and existing canopy.',
  ['Lindfield', 'East Lindfield', 'Killara', 'East Killara', 'Gordon', 'Pymble', 'West Pymble', 'Turramurra', 'North Turramurra', 'South Turramurra', 'Warrawee', 'St Ives', 'St Ives Chase', 'Wahroonga', 'Normanhurst', 'Hornsby', 'Hornsby Heights', 'Waitara', 'Asquith'],
  ['dural-acreage-landscaping-native-planting']),
 ('lower-north-shore', 'Lower North Shore', 'Steep blocks, sandstone and mature trees with council protection. Retaining, stairs and drainage do most of the work; planting responds to heavy shade.',
  ['North Sydney', 'Waverton', 'McMahons Point', 'Lavender Bay', 'Cammeray', 'Northbridge', 'Artarmon', 'Crows Nest', 'St Leonards', 'Naremburn', 'Wollstonecraft', 'Greenwich', 'Lane Cove', 'Lane Cove North', 'Lane Cove West', 'Riverview', 'Longueville', 'Northwood', 'Linley Point', 'Chatswood', 'Chatswood West', 'Willoughby', 'North Willoughby', 'Castlecrag', 'Middle Cove', 'Castle Cove', 'Roseville', 'Mosman', 'Cremorne', 'Cremorne Point', 'Neutral Bay'],
  ['north-ryde-duplex-landscaping']),
 ('ryde-and-parramatta', 'Ryde & Parramatta', 'The duplex and knockdown-rebuild belt. Boundary retaining, shared driveways and neighbour coordination are routine, and certifiers want the engineering documented.',
  ['Ryde', 'North Ryde', 'East Ryde', 'West Ryde', 'Macquarie Park', 'Marsfield', 'Eastwood', 'Denistone', 'Denistone East', 'Denistone West', 'Meadowbank', 'Melrose Park', 'Putney', 'Gladesville', 'Boronia Park', 'Henley', 'Huntleys Cove', 'Tennyson Point', 'Hunters Hill', 'Woolwich', 'Epping', 'North Epping', 'Carlingford', 'Beecroft', 'Cheltenham', 'Pennant Hills', 'Thornleigh', 'Westleigh', 'West Pennant Hills', 'Ermington', 'Rydalmere', 'Dundas', 'Dundas Valley', 'Telopea', 'Oatlands', 'Parramatta', 'North Parramatta', 'Harris Park', 'Rosehill', 'Westmead'],
  ['ermington-duplex-landscaping-retaining-wall', 'rydalmere-new-home-landscaping', 'north-ryde-duplex-landscaping', 'parramatta-museum-turfing-works']),
 ('inner-west-and-city', 'Inner West & City', 'Terrace courtyards, raised planters and rooftop-adjacent spaces where every material is carried through the house. Access and waste removal drive the program more than the planting does.',
  ['Sydney', 'Ultimo', 'Chippendale', 'Darlington', 'Surry Hills', 'Darlinghurst', 'Potts Point', 'Elizabeth Bay', 'Rushcutters Bay', 'Woolloomooloo', 'Glebe', 'Forest Lodge', 'Annandale', 'Rozelle', 'Lilyfield', 'Leichhardt', 'Balmain', 'Balmain East', 'Birchgrove', 'Newtown', 'Enmore', 'Erskineville', 'St Peters', 'Sydenham', 'Tempe', 'Camperdown', 'Stanmore', 'Petersham', 'Marrickville'],
  ['newtown-duplex-raised-planter-landscaping', 'darlinghurst-museum-landscape-public-domain-works']),
 ('eastern-suburbs', 'Eastern Suburbs', 'Tight rear-lane access, heritage controls and small high-value courtyards. Level changes are common and usually need engineered retaining before anything decorative happens.',
  ['Paddington', 'Centennial Park', 'Moore Park', 'Bondi Junction', 'Queens Park', 'Bellevue Hill', 'Bronte', 'Waverley', 'Woollahra', 'Bondi', 'Bondi Beach', 'North Bondi', 'Tamarama', 'Darling Point', 'Edgecliff', 'Point Piper', 'Double Bay', 'Rose Bay', 'Vaucluse', 'Dover Heights', 'Watsons Bay', 'Randwick', 'Clovelly', 'Kingsford', 'Kensington', 'Coogee', 'South Coogee', 'Maroubra'],
  ['darlinghurst-museum-landscape-public-domain-works']),
 ('st-george', 'St George', 'Duplex development on established streets. Boundary works often involve two owners, and the older sewer and stormwater runs need locating before any excavation.',
  ['Hurstville', 'Hurstville Grove', 'South Hurstville', 'Kogarah', 'Kogarah Bay', 'Beverley Park', 'Carlton', 'Allawah', 'Penshurst', 'Mortdale', 'Oatley', 'Peakhurst', 'Peakhurst Heights', 'Lugarno', 'Beverly Hills', 'Narwee', 'Riverwood', 'Blakehurst', 'Carss Park', 'Connells Point', 'Kyle Bay'],
  []),
 ('bayside', 'Bayside', 'Sandy profiles and flat blocks close to the water. Turf and planting are prepared differently on sand, and salt air decides the fence and fixing choices.',
  ['Rockdale', 'Brighton-Le-Sands', 'Kyeemagh', 'Monterey', 'Ramsgate', 'Ramsgate Beach', 'Sans Souci', 'Dolls Point', 'Sandringham', 'Banksia', 'Arncliffe', 'Wolli Creek', 'Turrella', 'Bexley', 'Bexley North', 'Bardwell Park', 'Bardwell Valley', 'Kingsgrove', 'Mascot', 'Botany', 'Eastlakes', 'Pagewood', 'Hillsdale', 'Eastgardens', 'Daceyville', 'Rosebery'],
  []),
 ('sutherland-shire', 'Sutherland Shire', 'Coastal-adjacent yards on sand and sandstone. Species selection and drainage change with the profile, and bushfire-prone edges affect fencing and mulch choices.',
  ['Sutherland', 'Kirrawee', 'Jannali', 'Kareela', 'Loftus', 'Woronora', 'Grays Point', 'Gymea', 'Gymea Bay', 'Miranda', 'Yowie Bay', 'Caringbah', 'Caringbah South', 'Dolans Bay', 'Lilli Pilli', 'Port Hacking', 'Taren Point', 'Cronulla', 'Woolooware', 'Burraneer', 'Kurnell', 'Bundeena', 'Maianbar', 'Sylvania', 'Sylvania Waters', 'Kangaroo Point', 'Oyster Bay', 'Engadine', 'Heathcote', 'Yarrawarrah', 'Woronora Heights', 'Menai', 'Bangor', 'Barden Ridge', 'Alfords Point', 'Illawong', 'Lucas Heights'],
  ['caringbah-south-duplex-landscaping']),
]

P = {p['slug']: p for p in json.load(open(os.path.join(ROOT, 'data', 'projects.json')))}
def proj_cards(slugs):
    out = []
    for s in slugs:
        p = P.get(s)
        if not p: continue
        out.append(f'''      <a class="card" href="/projects/{p['slug']}/"><div class="in">
        <h3>{e(p['name'])}</h3><p>{e(p['meta'])}</p>
        <p class="tags">{e(p['sector'])} · {e(p['suburb'])}</p><span class="more">Read the case study →</span>
      </div></a>''')
    return '\n'.join(out)

def region_page(slug, name, character, subs, projs):
    cfg = {"path": f"/areas/{slug}/", "nav": "residential", "footer": "residential",
           "title": f"Landscaping {name} Sydney | Estate Landscapers",
           "description": f"Residential landscape construction across {name}: {', '.join(subs[:4])} and surrounds. Design, build and aftercare with engineering and council requirements handled."}
    pj = proj_cards(projs)
    projblock = f'''<section class="band tint">
  <div class="shell">
    <p class="eyebrow">Nearby work</p>
    <h2>Projects in and around {e(name)}.</h2>
    <div class="g3 mt">
{pj}
    </div>
  </div>
</section>
''' if pj else ''
    chips = ''.join(f'<span class="chip">{e(s)}</span>' for s in subs)
    return f'''<!--CONFIG
{json.dumps(cfg, indent=1, ensure_ascii=False)}
-->
<section class="hero">
  <div class="shell">
    <div>
      <p class="eyebrow"><a href="/areas/" style="color:inherit;text-decoration:none">Residential areas served</a> · {e(name)}</p>
      <h1>Landscape construction across <em>{e(name)}</em>.</h1>
      <p class="lead">{e(', '.join(subs[:5]))} and every suburb in between. Design, build and aftercare for homes and developments: one contractor from bare ground to finished yard, with the engineering and council requirements handled rather than left with you.</p>
      <div class="btn-row">
        <a class="btn" href="/residential/quote/">Get a quote</a>
        <a class="btn btn-o" href="/residential/#services">All services</a>
      </div>
    </div>
    <div class="plate"><div class="slot"><b>Photo slot</b><span>A completed {e(name)} project</span></div></div>
  </div>
</section>

{{{{include creds}}}}

<section class="band">
  <div class="shell g2">
    <div>
      <p class="eyebrow">What we see here</p>
      <h2>The local conditions that shape the build.</h2>
      <p class="sub">{e(character)}</p>
      <p class="sub" style="margin-top:12px">We quote the whole yard as one itemised package: earthworks, drainage, retaining, surfaces, fencing, turf and planting, so nothing falls between trades.</p>
    </div>
    <div>
      <p class="eyebrow">Suburbs we work in</p>
      <h2>{len(subs)} suburbs in {e(name)}.</h2>
      <div class="chips mt">{chips}</div>
      <p class="sub" style="margin-top:14px;font-size:.85rem">Not listed? If it is inside the area on the map, we work there. Ask.</p>
    </div>
  </div>
</section>

{projblock}<section class="band">
  <div class="shell">
    <p class="eyebrow">Services here</p>
    <h2>What we are usually asked for.</h2>
    <div class="g3 mt">
      <a class="card" href="/residential/new-build-landscaping/"><div class="in"><h3>New build landscaping</h3><p>Bare site to finished yard as one package.</p><span class="more">View →</span></div></a>
      <a class="card" href="/residential/retaining-walls/"><div class="in"><h3>Retaining walls</h3><p>Timber sleeper to engineered rendered block, drained and certified.</p><span class="more">View →</span></div></a>
      <a class="card" href="/residential/concrete-driveways/"><div class="in"><h3>Concrete works</h3><p>Driveways, paths, kerb, crossovers and footpaths.</p><span class="more">View →</span></div></a>
      <a class="card" href="/residential/turf-soft-landscaping/"><div class="in"><h3>Turfing</h3><p>Kikuyu through to Sir Grange Zoysia, over proper underlay.</p><span class="more">View →</span></div></a>
      <a class="card" href="/residential/landscape-design/"><div class="in"><h3>Design</h3><p>2D plans, 3D renders on the higher tiers.</p><span class="more">View →</span></div></a>
      <a class="card" href="/residential/care/"><div class="in"><h3>Care</h3><p>Establishment and scheduled aftercare for what we build.</p><span class="more">View →</span></div></a>
    </div>
  </div>
</section>

<section class="cta">
  <div class="shell">
    <h2>Planning work in {e(name)}?</h2>
    <p>Send photos and your plans. We call the same business day and the itemised quote follows the site visit.</p>
    <div class="btn-row">
      <a class="btn" href="/residential/quote/">Get a quote</a>
      <a class="btn btn-o" href="/areas/">All areas served</a>
    </div>
  </div>
</section>

{{{{include infra-residential}}}}

<script type="application/ld+json">
{json.dumps({"@context":"https://schema.org","@type":"Service","serviceType":"Landscape construction","name":f"Landscaping {name}","url":"{{PAGE_URL}}","provider":{"@type":"LandscapeContractor","name":"Estate Landscapers","legalName":"Apexx Enterprises Pty Ltd","url":HOME+"/","telephone":"+61414147008","address":{"@type":"PostalAddress","streetAddress":"Unit 33/275 Annangrove Road","addressLocality":"Rouse Hill","addressRegion":"NSW","postalCode":"2155","addressCountry":"AU"}},"areaServed":[{"@type":"Place","name":s+", NSW"} for s in subs]}, ensure_ascii=False)}
</script>
'''

def index_page():
    total = sum(len(r[3]) for r in REGIONS)
    cards = '\n'.join(f'''      <a class="card" href="/areas/{s}/"><div class="in">
        <h3>{e(n)}</h3><p>{e(', '.join(subs[:4]))} and surrounds.</p>
        <p class="tags">{len(subs)} suburbs</p><span class="more">View area →</span>
      </div></a>''' for s, n, _, subs, _ in REGIONS)
    cfg = {"path": "/areas/", "nav": "shared", "footer": "shared",
           "title": "Residential Areas Served: Landscaping Across Sydney | Estate Landscapers",
           "description": f"Estate Landscapers builds residential landscapes across {len(REGIONS)} regions and {total} Sydney suburbs: the Hills, Northern Beaches, North Shore, Ryde and Parramatta, Inner West and City, Eastern Suburbs, St George, Bayside and the Sutherland Shire."}
    alls = ''.join(f'<span class="chip">{e(x)}</span>' for r in REGIONS for x in r[3])
    return f'''<!--CONFIG
{json.dumps(cfg, indent=1, ensure_ascii=False)}
-->
<section class="hero">
  <div class="shell">
    <div>
      <p class="eyebrow">Residential areas served</p>
      <h1>Where we build: <em>{len(REGIONS)} regions</em> across Sydney.</h1>
      <p class="lead">Residential landscape construction across the areas on the map. Commercial and tender work reaches further, into regional NSW and Queensland.</p>
      <div class="btn-row">
        <a class="btn" href="/residential/quote/">Get a quote</a>
      </div>
    </div>
    <div class="plate"><div class="slot"><b>Photo slot</b><span>The service area map</span></div></div>
  </div>
</section>

{{{{include creds}}}}

<section class="band">
  <div class="shell">
    <p class="eyebrow">Regions</p>
    <h2>{len(REGIONS)} areas, one standard.</h2>
    <div class="g3 mt">
{cards}
    </div>
  </div>
</section>

<section class="band tint">
  <div class="shell">
    <p class="eyebrow">Every suburb</p>
    <h2>{total} suburbs, by name.</h2>
    <div class="chips mt">{alls}</div>
    <p class="sub" style="margin-top:16px">Inside the area on the map but not listed? We work there. Commercial, tender and infrastructure-adjacent work is quoted well beyond it.</p>
  </div>
</section>

<section class="cta">
  <div class="shell">
    <h2>Tell us where the project is.</h2>
    <p>Photos and an address are enough to start. We call the same business day.</p>
    <div class="btn-row">
      <a class="btn" href="/residential/quote/">Get a quote</a>
      <a class="btn btn-o" href="/contact/">Contact</a>
    </div>
  </div>
</section>

{{{{include infra-shared}}}}

<script type="application/ld+json">
{json.dumps({"@context":"https://schema.org","@type":"CollectionPage","name":"Residential areas served","url":"{{PAGE_URL}}","description":cfg["description"],"hasPart":[{"@type":"WebPage","name":n,"url":f"{HOME}/areas/{s}/"} for s,n,_,_,_ in REGIONS]}, ensure_ascii=False)}
</script>
'''

if __name__ == '__main__':
    d = os.path.join(ROOT, 'src', 'pages', 'areas')
    os.makedirs(d, exist_ok=True)
    for f in glob.glob(os.path.join(d, '*.html')): os.remove(f)
    for slug, name, ch, subs, projs in REGIONS:
        open(os.path.join(d, slug + '.html'), 'w').write(region_page(slug, name, ch, subs, projs))
    open(os.path.join(ROOT, 'src', 'pages', 'areas.html'), 'w').write(index_page())
    print(f'areas: {len(REGIONS)} regions, {sum(len(r[3]) for r in REGIONS)} suburbs')

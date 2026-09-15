#!/usr/bin/env python3
"""Generates the product-level pages: turf varieties, decorative pebbles,
concrete finishes, letterboxes, clotheslines, and the sandstone-log wall guide.
Run: python3 tools/gen-catalogue.py"""
import os, json, sys
sys.path.insert(0, os.path.dirname(__file__))
from pagekit import *

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def write(rel, content):
  p = os.path.join(ROOT, 'src', 'pages', rel)
  os.makedirs(os.path.dirname(p), exist_ok=True)
  open(p, 'w').write(content)

HOME = 'https://www.estatelandscapers.com.au'
RES = ('Residential', '/residential/')

# ============================================================== TURF ==========
# Attribute data as published by the grower we buy from; rewritten as our own
# table. Stars are 1-5. Order of columns is the order of the tier ladder.
TURF = [
 dict(slug='eureka-kikuyu', name='Eureka Kikuyu', family='Kikuyu', tier='Basic',
   shade=1, sun='6+ hrs', weed=2, drought='Low', durability='High', maint='Medium', leaf='Medium', winter=4, mow='Every 4 days', salt=3, thatch='Low', fert='Medium',
   pitch='The budget workhorse for full sun. Fast to establish, quick to repair itself, and the cheapest lawn per square metre. The trade is upkeep: it grows fast, so it is mowed often, and it will spread into garden beds unless edged properly.',
   best='Large sunny yards, acreage, verges and anywhere the budget matters more than the mowing.',
   avoid='Shaded yards, and anyone who does not want to mow weekly in summer.',
   cert='AusGAP certified premium kikuyu, supplied through an accredited grower.'),
 dict(slug='sir-walter-buffalo', name='Sir Walter DNA Certified Buffalo', family='Buffalo', tier='Standard',
   shade=4, sun='3–4 hrs', weed=4, drought='High', durability='High', maint='Very low', leaf='Broad', winter=4, mow='Every 7 days', salt=5, thatch='Medium', fert='Low',
   pitch='The Sydney default for a reason: shade tolerant, hard wearing, soft underfoot and slow to invade beds. DNA certification means the turf that arrives is genetically the real variety, not a look-alike.',
   best='Family yards with pets and kids, part-shade from the house or fences, and anyone who wants a lawn that forgives neglect.',
   avoid='Yards that never see the sun. Even Sir Walter needs three to four hours.',
   cert='DNA certified and AusGAP certified. Supplied through an accredited grower with a ten-year product warranty.'),
 dict(slug='tiftuf-bermuda', name='TifTuf Hybrid Bermuda', family='Couch / Bermuda', tier='Standard',
   shade=3, sun='4–5 hrs', weed=3, drought='Very high', durability='Very high', maint='Very low', leaf='Fine', winter=5, mow='Every 5 days', salt=4, thatch='Low', fert='Medium',
   pitch='The drought specialist. A fine-leaf couch bred for water efficiency that holds colour through winter and takes heavy wear. It wants sun, and it is mowed a little more often than buffalo to keep it tight.',
   best='Full-sun yards, entertaining lawns, high-traffic areas and anyone on tank water or restrictions.',
   avoid='Part-shade. Under four hours of sun it thins out.',
   cert='AusGAP certified. Supplied through an accredited grower with a ten-year product warranty.'),
 dict(slug='sir-grange-zoysia', name='Sir Grange Zoysia', family='Zoysia', tier='Premium',
   shade=4, sun='3–4 hrs', weed=5, drought='High', durability='High', maint='Very low', leaf='Fine', winter=5, mow='Every 10 days', salt=5, thatch='Low', fert='Very low',
   pitch='The one we push when the budget allows. Fine, dense and slow-growing, which means the least mowing of any lawn here and a surface that feels like a golf course. Weeds struggle to get a foothold in it.',
   best='Anyone who wants the best-looking lawn with the least work. Kids love the feel of it.',
   avoid='Nothing in particular, though the higher purchase price is real. It repays it in mowing.',
   cert='AusGAP certified. Supplied through an accredited grower with a ten-year product warranty.'),
 dict(slug='stampede-hybrid-buffalo', name='Stampede Hybrid Buffalo', family='Buffalo', tier='Premium',
   shade=4, sun='3–4 hrs', weed=5, drought='Very high', durability='Very high', maint='Very low', leaf='Broad', winter=5, mow='Every 7 days', salt=4, thatch='Low', fert='Low',
   pitch='The newest buffalo, bred for drought performance and pest tolerance with better winter colour and less thatch than older buffalos. Everything people like about Sir Walter with a harder edge.',
   best='Buffalo lovers who want the latest genetics, exposed sites, and yards that get hammered by kids and dogs.',
   avoid='Deep shade, same as every buffalo.',
   cert='AusGAP certified. Supplied through an accredited grower with a ten-year product warranty.'),
 dict(slug='zoysia-australis', name='Zoysia Australis', family='Zoysia', tier='Premium',
   shade=4, sun='3–4 hrs', weed=5, drought='Medium', durability='Medium', maint='Low', leaf='Medium', winter=4, mow='Every 7 days', salt=5, thatch='Medium', fert='Low',
   pitch='A medium-leaf zoysia with the family strengths: naturally weed resistant, soft, and good in part shade and salt air. A little more water than Sir Grange, a little less fuss than a buffalo.',
   best='Coastal and part-shade yards where the soft, dense zoysia look is wanted without the Sir Grange price.',
   avoid='Very high-traffic lawns; it repairs more slowly than buffalo or couch.',
   cert='AusGAP certified. Supplied through an accredited grower.'),
]
def stars(n): return '★' * n + '☆' * (5 - n)
TURF_ROWS = [
 ('Tier', [t['tier'] for t in TURF]),
 ('Shade tolerance', [stars(t['shade']) for t in TURF]),
 ('Daily sun needed', [t['sun'] for t in TURF]),
 ('Weed resistance', [stars(t['weed']) for t in TURF]),
 ('Drought tolerance', [t['drought'] for t in TURF]),
 ('Durability', [t['durability'] for t in TURF]),
 ('Maintenance', [t['maint'] for t in TURF]),
 ('Leaf', [t['leaf'] for t in TURF]),
 ('Winter colour', [stars(t['winter']) for t in TURF]),
 ('Mowing, peak season', [t['mow'] for t in TURF]),
 ('Salt tolerance', [stars(t['salt']) for t in TURF]),
 ('Thatch build-up', [t['thatch'] for t in TURF]),
 ('Fertiliser need', [t['fert'] for t in TURF]),
]
TURF_COLS = [(t['name'].replace(' DNA Certified', ''), f"/residential/turf/{t['slug']}/") for t in TURF]
TURF_CMP = compare('Compare the varieties', 'Six lawns, side by side.',
  'Every lawn we lay is a certified variety from an accredited grower. This is the same comparison we use on site to steer a choice; the tier is where it sits on your quote.',
  TURF_COLS, TURF_ROWS, colhead='',
  note='Ratings are the grower\'s published performance data for Sydney conditions. Sun hours are the daily minimum for the lawn to hold together.')
CERT = band('Genuine varieties', 'Certified turf, not a look-alike.', '''  <p class="sub">The named varieties above are protected breeds. Buying them through an
   accredited grower means three things you can hold us to: the turf is
   <b>AusGAP certified</b> under the Australian Genetic Assurance Program, so what
   arrives is the variety on the invoice; <b>Sir Walter is DNA certified</b>, which is
   the only way to know a buffalo is actually Sir Walter; and the varieties carry a
   <b>ten-year product warranty</b> from the grower network. Uncertified "buffalo" from
   a roadside sign has none of that, and it is usually the reason a lawn fails to
   match the yard next door.</p>''')

def turf_page(t):
  others = [x for x in TURF if x['slug'] != t['slug']]
  sections = band('Why choose it', f"{e(t['name'])}, honestly.", f'''  <div class="g2 mt">
   <div>
    <p class="sub"><b>Where it shines.</b> {e(t['best'])}</p>
    <p class="sub" style="margin-top:12px"><b>Where it doesn\'t.</b> {e(t['avoid'])}</p>
    <p class="sub" style="margin-top:12px"><b>Certification.</b> {e(t['cert'])}</p>
   </div>
   <div class="panel">
    <h3>At a glance</h3>
    <dl class="facts">
     <div><dt>Tier on your quote</dt><dd>{t['tier']}</dd></div>
     <div><dt>Family</dt><dd>{t['family']}</dd></div>
     <div><dt>Shade tolerance</dt><dd>{stars(t['shade'])}</dd></div>
     <div><dt>Daily sun needed</dt><dd>{t['sun']}</dd></div>
     <div><dt>Drought tolerance</dt><dd>{t['drought']}</dd></div>
     <div><dt>Mowing, peak season</dt><dd>{t['mow']}</dd></div>
     <div><dt>Leaf</dt><dd>{t['leaf']}</dd></div>
     <div><dt>Winter colour</dt><dd>{stars(t['winter'])}</dd></div>
    </dl>
   </div>
  </div>''') + TURF_CMP + band('Every lawn we lay', 'The same preparation under all six.', '''  <p class="sub">The variety decides the tier; the preparation is identical. Existing surface
   stripped, base graded to fall, screened underlay spread and levelled, turf laid tight
   and rolled, then watered in. Cheap lawns fail at the base, not at the grass, which is
   why we do not lay any of these over unprepared ground.</p>''')
  qas = [
    (f"Is {e(t['name'].split(' DNA')[0])} right for my yard?", f"{e(t['best'])} {e(t['avoid'])} If you are unsure, send a photo of the yard at midday and we will tell you honestly which variety will hold."),
    ('How do I know it is the real variety?', 'It arrives with the grower\'s certification. AusGAP covers genetic purity, and Sir Walter carries DNA certification on top. We will show you the delivery docket.'),
    ('Can I change my mind after quoting?', 'Yes. The quote prices the tier; switching variety inside the same tier is a like-for-like change, and moving tiers is one line on the quote.'),
  ]
  return page(f"/residential/turf/{t['slug']}/", 'residential',
    f"{t['name']} Turf Sydney | Estate Landscapers",
    f"{t['name']} laid over prepared underlay across Sydney. {t['pitch'][:110].rsplit('.',1)[0]}. Certified variety, {t['tier']} tier.",
    ('Turfing', '/residential/turf-soft-landscaping/'), t['family'],
    f"{e(t['name'])}: <em>{ {'Basic':'the budget lawn','Standard':'the Sydney default','Premium':'the premium lawn'}[t['tier']] }</em>.",
    e(t['pitch']), f"{t['name']} lawn, established, in a Sydney yard", sections, qas,
    f"Want {e(t['name'].split(' DNA')[0])} laid properly?", 'Send a photo and the rough area. We will confirm the variety suits the light and price it at tier.',
    [('Home', HOME + '/'), ('Residential', HOME + '/residential/'), ('Turfing', HOME + '/residential/turf-soft-landscaping/'), (t['name'], '{{PAGE_URL}}')],
    hero_key=f"residential-turf-{t['slug']}-hero")

for t in TURF: write(f"residential/turf/{t['slug']}.html", turf_page(t))

# ======================================================== PEBBLES ==========
PEB = [
 dict(slug='blue-stone', name='Blue Stone', tier='Basic', sizes='10 mm and 20 mm',
   what='Crushed basalt aggregate, blue-grey to charcoal. Angular, so it locks together underfoot and does not roll.',
   best='Paths, side passages, driveways, drainage strips and under decks. The most economical stone by a distance.',
   note='Crushed, not tumbled, so the edges are sharp. Perfect on a path, less friendly beside a pool.'),
 dict(slug='river-pebbles', name='River Pebbles', tier='Standard', sizes='10 mm and 20 mm',
   what='Naturally rounded stone in browns, creams and charcoals, tumbled smooth by water.',
   best='Garden beds, dry creek beds, drainage edges and side paths. The classic landscaping pebble.',
   note='Rounded stone moves underfoot on slopes and driveways. We use it where it sits still.'),
 dict(slug='white-cowra', name='White Cowra', tier='Premium', sizes='10 mm and 20 mm',
   what='Whitish quartz river pebble, smooth and rounded, from the Cowra region.',
   best='Feature beds, pool surrounds, courtyards and anywhere the contrast with dark planting or charcoal walls is the point.',
   note='Bright when laid; it mellows with dust and can be hosed back. Larger sizes on request.'),
 dict(slug='white-marble', name='White Marble', tier='Premium', sizes='10 mm and 20 mm',
   what='Crushed white marble with a crystalline sparkle. The whitest stone we lay.',
   best='Contemporary courtyards, Japanese-style gardens, feature strips and water features. Striking against charcoal pavers.',
   note='Angular, so it stays put. Priced above Cowra because of what it costs to quarry.'),
]
PEB_TIERS = tiers('Pebbles are priced per square metre laid over weedmat, at the tier you choose.',
  [('Stone', 'Blue Stone (crushed basalt)', 'River pebbles', 'White Cowra or White Marble'),
   ('Character', 'Angular, blue-grey, locks together', 'Rounded, natural mix of browns and creams', 'Bright white, feature-grade'),
   ('Sizes we lay', '10 mm or 20 mm', '10 mm or 20 mm', '10 mm or 20 mm')],
  'Prefer a larger stone, a dry creek bed or Lucky Stones for a feature? Ask; we lay them, they are priced per job.')
peb_hub = page('/residential/decorative-pebbles/', 'residential',
  'Decorative Pebbles Sydney | Blue Stone, River Pebbles, White Cowra & Marble',
  'Decorative pebbles laid over weedmat across Sydney: Blue Stone as the budget option, river pebbles as standard, White Cowra and White Marble as premium. 10 mm and 20 mm, larger on request.',
  RES, 'Decorative pebbles', 'Stone that <em>stays where you put it</em>.',
  'Pebbles are the cheapest way to finish a side passage, edge a bed or fill a strip that will never grow grass. Laid over weedmat on a compacted base, at the depth the stone needs, they stay tidy for years.',
  'Pebble strip between paving and garden bed', PEB_TIERS + band('The four we lay', 'Pick by colour and how the stone behaves.', '<div class="g3 mt">\n' + cards([(f"/residential/decorative-pebbles/{p['slug']}/", p['name'], p['best']) for p in PEB]) + '\n  </div>'),
  [('Which size should I choose?', 'Ten millimetre for paths and anything walked on; twenty for beds and edges where it is mostly looked at. Larger sizes, dry creek beds and feature stones are available on request and priced per job.'),
   ('Why weedmat underneath?', 'It stops the stone sinking into soil and keeps weeds from coming through. Skipping it is why cheap pebble jobs look tired in a year.'),
   ('Can pebbles go on a slope?', 'Crushed stone yes, because it locks together. Rounded river pebble creeps downhill over time, so on a grade we specify Blue Stone or marble.')],
  'Want a strip finished properly?', 'Tell us the area and where it is. Pebbles are a line on your quote at the tier you choose.',
  [('Home', HOME + '/'), ('Residential', HOME + '/residential/'), ('Decorative pebbles', '{{PAGE_URL}}')])
write('residential/decorative-pebbles.html', peb_hub)
for p in PEB:
  write(f"residential/decorative-pebbles/{p['slug']}.html", page(f"/residential/decorative-pebbles/{p['slug']}/", 'residential',
    f"{p['name']} Pebbles Sydney | {p['tier']} Tier | Estate Landscapers",
    f"{p['name']} laid over weedmat across Sydney. {p['what']} {p['tier']} tier, {p['sizes']}, larger sizes on request.",
    ('Decorative pebbles', '/residential/decorative-pebbles/'), p['tier'] + ' tier',
    f"{e(p['name'])}: <em>{ {'Basic':'the economical stone','Standard':'the classic pebble','Premium':'the feature stone'}[p['tier']] }</em>.",
    e(p['what']), f"{p['name']} pebbles laid in a garden strip",
    band('Where it works', 'Right stone, right place.', f'''  <div class="g2 mt"><div>
   <p class="sub"><b>Best for.</b> {e(p['best'])}</p>
   <p class="sub" style="margin-top:12px"><b>Worth knowing.</b> {e(p['note'])}</p>
  </div><div class="panel"><h3>At a glance</h3><dl class="facts">
   <div><dt>Tier on your quote</dt><dd>{p['tier']}</dd></div>
   <div><dt>Sizes we lay</dt><dd>{p['sizes']}</dd></div>
   <div><dt>Larger sizes</dt><dd>On request</dd></div>
   <div><dt>Laid over</dt><dd>Weedmat on a compacted base</dd></div>
  </dl></div></div>''') + PEB_TIERS,
    [(f"How deep is {e(p['name'])} laid?", 'Roughly twice the stone size: 20 to 40 mm depending on the pebble. Thinner than that and the weedmat shows; thicker wastes stone.'),
     ('Does the colour vary?', 'Yes, it is a natural product and shades vary between loads. We order each area from one batch so it matches.'),
     ('Can I mix it with other stone?', 'Yes. Feature stones and larger river pebbles are common additions, priced per job.')],
    f"Want {e(p['name'])} laid?", 'Send a photo of the area. It goes on the quote at tier, sizes as you prefer.',
    [('Home', HOME + '/'), ('Residential', HOME + '/residential/'), ('Decorative pebbles', HOME + '/residential/decorative-pebbles/'), (p['name'], '{{PAGE_URL}}')],
    hero_key=f"residential-pebbles-{p['slug']}-hero"))

# ======================================================= CONCRETE ==========
SUPP = 'We work with the largest suppliers, Boral, Holcim and Heidelberg, and offer their full range.'
CON = [
 dict(slug='plain-concrete', name='Plain Concrete', tier='Basic',
   what='Grey concrete, broom or trowel finished, with control joints cut to a pattern.',
   best='Driveways, side paths, slabs, bin pads and anywhere the surface is a workhorse rather than a feature.',
   note='Plain does not mean rough. Falls, compaction, mesh and joint spacing are the same as the premium finishes; only the surface differs.'),
 dict(slug='colour-concrete', name='Colour Concrete', tier='Standard',
   what='Through-coloured concrete with a sealer. Charcoal, sandstone, off-white and the rest of the supplier colour range.',
   best='Driveways that should match the house, entry paths and outdoor areas where grey would look unfinished.',
   note='Colour is mixed through the batch, not painted on, so it does not wear off. Sealer is reapplied every few years.'),
 dict(slug='exposed-aggregate', name='Exposed Aggregate', tier='Premium',
   what='Decorative stone exposed in the surface and sealed. Slip resistant, textured, and the finish that lifts a frontage.',
   best='Front driveways, alfresco areas, pool surrounds and paths where the concrete is part of the look.',
   note='Aggregate blends and cement colours come from the supplier range, including off-white cement at extra cost.'),
]
CON_TIERS = tiers('Three finishes, three price points. The base preparation, compaction, falls, mesh and control joints are identical under all three.',
  [('Finish', 'Plain grey concrete', 'Colour concrete with sealer', 'Exposed aggregate with sealer'),
   ('Look', 'Clean, honest, the workhorse', 'Charcoal, sandstone or custom colour to suit the house', 'Stone-textured, premium street presence; off-white cement priced per job')],
  SUPP)
for c in CON:
  write(f"residential/concrete-driveways/{c['slug']}.html", page(f"/residential/concrete-driveways/{c['slug']}/", 'residential',
    f"{c['name']} Sydney | {c['tier']} Tier Driveways & Paths | Estate Landscapers",
    f"{c['name']} driveways, paths and slabs across Sydney. {c['what']} {c['tier']} tier. {SUPP}",
    ('Concrete works', '/residential/concrete-driveways/'), c['tier'] + ' tier',
    f"{e(c['name'])}: <em>{ {'Basic':'the workhorse','Standard':'the finish that matches the house','Premium':'the finish that sells the frontage'}[c['tier']] }</em>.",
    e(c['what']), f"{c['name']} driveway, finished",
    band('Where it works', 'What the finish is for.', f'''  <div class="g2 mt"><div>
   <p class="sub"><b>Best for.</b> {e(c['best'])}</p>
   <p class="sub" style="margin-top:12px"><b>Worth knowing.</b> {e(c['note'])}</p>
   <p class="sub" style="margin-top:12px">{SUPP}</p>
  </div><div class="panel"><h3>At a glance</h3><dl class="facts">
   <div><dt>Tier on your quote</dt><dd>{c['tier']}</dd></div>
   <div><dt>Suppliers</dt><dd>Boral, Holcim, Heidelberg</dd></div>
   <div><dt>Council works</dt><dd>Crossovers, kerb and footpath to council spec</dd></div>
   <div><dt>Base</dt><dd>Compacted, mesh reinforced, joints cut</dd></div>
  </dl></div></div>''') + CON_TIERS,
    [('Does the base change with the finish?', 'No. Compaction, mesh, falls and control joints are the same across all three. You are paying for the surface, not a lesser slab.'),
     ('Can I see colours or aggregates first?', 'Yes. Supplier colour and aggregate charts are available, and we confirm your selection before the pour.'),
     ('What about the council crossover?', 'Crossovers, kerb and footpath sections are built to the applicable council specification and inspected, so you receive the final council certificate.')],
    f"Pricing a {e(c['name'].lower())} job?", 'Send the dimensions and a photo. It is a line on your quote at tier, council work included where it applies.',
    [('Home', HOME + '/'), ('Residential', HOME + '/residential/'), ('Concrete works', HOME + '/residential/concrete-driveways/'), (c['name'], '{{PAGE_URL}}')],
    hero_key=f"residential-concrete-{c['slug']}-hero"))

# ============================================= LETTERBOXES / CLOTHESLINES ==
write('residential/letterboxes.html', page('/residential/letterboxes/', 'residential',
  'Letterbox Installation Sydney | Estate Landscapers',
  'Letterboxes supplied and installed as part of a landscape package across Sydney, set plumb and level to Australia Post height, or standalone at sensible scale.',
  RES, 'Letterboxes', 'The last thing built, <em>the first thing seen</em>.',
  'A letterbox is a small job that is easy to get wrong: the wrong height, off plumb, a footing that heaves. We set them to Australia Post requirements on a proper footing, usually as the finishing line of a front-yard package.',
  'Letterbox installed at a finished front entry',
  band('What we do', 'Supplied, set, finished.', '''  <div class="g3 mt">
   <div class="card"><div class="in"><h3>Supply and install</h3><p>Pillar, post-mounted or wall-mounted letterboxes from the mainstream ranges, or install one you have bought.</p></div></div>
   <div class="card"><div class="in"><h3>Set correctly</h3><p>Plumb, level, at the required height and clear of the driveway sight line, on a concrete footing that will not move.</p></div></div>
   <div class="card"><div class="in"><h3>Part of the package</h3><p>Priced as a line within your landscape package. Installed standalone at sensible scale, for example alongside a fence or driveway job.</p></div></div>
  </div>'''),
  [('Can you install a letterbox I have already bought?', 'Yes. Bring it to site and we set it as part of the works.'),
   ('Is there a height rule?', 'Australia Post specifies a letter slot height range and clear access. We set to it so deliveries are never an issue.'),
   ('Do you do letterboxes on their own?', 'At sensible scale, yes; typically with a fence, driveway or front-yard job rather than as a single trip.')],
  'Finishing a front yard?', 'Letterbox, fence and driveway quoted together is the usual way. Send a photo of the frontage.',
  [('Home', HOME + '/'), ('Residential', HOME + '/residential/'), ('Letterboxes', '{{PAGE_URL}}')], hero_key='residential-letterboxes-hero'))

write('residential/clotheslines.html', page('/residential/clotheslines/', 'residential',
  'Clothesline Installation Sydney | Estate Landscapers',
  'Freestanding and fold-down clotheslines supplied and installed across Sydney as part of a landscape package, on proper footings, positioned for sun and access.',
  RES, 'Clotheslines', 'Where the sun is, <em>not where the builder left a wall</em>.',
  'Clotheslines get bolted wherever is easiest and then hated for years. We position them for sun and access as part of the yard plan, on footings that hold, and install the fold-down or freestanding unit that fits the space.',
  'Freestanding clothesline installed on a side lawn',
  band('What we do', 'Positioned, footed, installed.', '''  <div class="g3 mt">
   <div class="card"><div class="in"><h3>Freestanding and fold-down</h3><p>Rotary, freestanding folding, and wall-mounted fold-down lines from the mainstream ranges, or install one you have bought.</p></div></div>
   <div class="card"><div class="in"><h3>Positioned with the yard</h3><p>Sun, wind, access from the laundry and the sight line from the entertaining area are decided on the plan, not on the day.</p></div></div>
   <div class="card"><div class="in"><h3>Part of the package</h3><p>Priced as a line within your landscape package. Installed standalone at sensible scale.</p></div></div>
  </div>'''),
  [('Freestanding or fold-down?', 'Fold-down saves space against a fence or wall; freestanding suits larger yards and gives more line. We recommend based on the plan.'),
   ('Will it move?', 'Not on our footings. Posts are concreted to the depth the unit needs, which is more than the box says.'),
   ('Can you install one I have bought?', 'Yes, as part of the works.')],
  'Planning the yard?', 'Clothesline placement is a five-minute decision on the plan that saves years of annoyance. Ask for it in your quote.',
  [('Home', HOME + '/'), ('Residential', HOME + '/residential/'), ('Clotheslines', '{{PAGE_URL}}')], hero_key='residential-clotheslines-hero'))

# ====================================================== SANDSTONE LOG ======
write('insights/retaining-walls/sandstone-log.html', f'''<!--CONFIG
{json.dumps({"path": "/insights/retaining-walls/sandstone-log/", "nav": "residential", "footer": "residential",
 "title": "Sandstone Log Retaining Walls Sydney | Premium Option | Estate Landscapers",
 "description": "Sandstone log retaining walls: solid Sydney sandstone logs set on a compacted base, the premium natural-stone option for garden terracing and acreage. Engineered from 600 mm."}, indent=1)}
-->
<article class="band" style="padding-top:clamp(30px,4vw,50px)">
 <div class="shell" style="max-width:820px">
 <p class="eyebrow"><a href="/insights/retaining-walls/" style="color:inherit;text-decoration:none">Retaining wall types</a> · Premium</p>
 <h1 style="font-size:clamp(1.55rem,3.4vw,2.3rem);font-weight:800;letter-spacing:-.02em;line-height:1.18">Sandstone log retaining walls</h1>
 <p class="sub" style="max-width:none">Solid sandstone logs, cut from Sydney basin stone and set in courses on a compacted base. The natural-stone option in our Premium tier: permanent, heavy, and at home on acreage and in established gardens.</p>
 {slot('Photo slot', 'Sandstone log wall, full length, in an established garden', 'insights-retaining-walls-sandstone-log-hero')}
 <h2 style="margin-top:34px">How it is built</h2>
 <p class="sub" style="max-width:none;margin-top:10px">Logs are typically around two metres long and 300 mm square, weighing several hundred kilograms each, so they are placed by machine. The first course sits on a compacted road-base bed below finished grade; each course above is set back slightly and pinned or mortared where the design calls for it. Ag-line drainage and free-draining backfill sit behind the wall, exactly as with any other system.</p>
 <h2 style="margin-top:34px">Where it makes sense</h2>
 <p class="sub" style="max-width:none;margin-top:10px">Garden terracing, level changes on larger blocks, native and acreage landscapes, and anywhere a manufactured block would look wrong. Because the stone is the finish, there is nothing to render, paint or replace. We built terraced sandstone log walls into the <a href="/projects/dural-acreage-landscaping-native-planting/" style="color:var(--blue);font-weight:700">Dural acreage project</a>, where they carry the level changes through native planting.</p>
 <h2 style="margin-top:34px">Honest limits</h2>
 <p class="sub" style="max-width:none;margin-top:10px">Sandstone is a gravity wall: it relies on mass and setback, so height is limited without engineering. From <b>600 mm and above, the wall is engineered</b>, as with every wall we build. Access matters too; the machine that places the logs needs a way in. And sandstone is porous, so drainage behind it is not optional.</p>
 <div class="panel good" style="margin-top:36px">
  <h3>Comparing wall types?</h3>
  <p>Height, what sits behind it and the look decide the system. The comparison table on the retaining walls page puts all seven side by side.</p>
  <div class="btn-row"><a class="btn" href="/residential/retaining-walls/">Retaining walls</a><a class="btn btn-o" href="/residential/quote/">Get a quote</a></div>
 </div>
 </div>
</article>
<script type="application/ld+json">
{json.dumps({"@context":"https://schema.org","@type":"Article","headline":"Sandstone log retaining walls","description":"The premium natural-stone retaining option: solid sandstone logs set in courses on a compacted base, engineered from 600 mm.","url":"{{PAGE_URL}}","datePublished":"2026-09-14","dateModified":"2026-09-14","author":{"@type":"Organization","name":"Estate Landscapers","url":"https://www.estatelandscapers.com.au/"},"publisher":{"@type":"Organization","name":"Estate Landscapers"}}, ensure_ascii=False)}
</script>
<script type="application/ld+json">
{crumb_ld([('Home', HOME + '/'), ('Retaining walls', HOME + '/residential/retaining-walls/'), ('Sandstone log', '{{PAGE_URL}}')])}
</script>
''')

print('catalogue: 6 turf, 5 pebble, 3 concrete, letterboxes, clotheslines, sandstone log')

# =========================================================== FENCING =========
FENCE = [
 dict(slug='colorbond', name='Colorbond', tier='Standard',
      what='Steel panel fencing in the full Colorbond colour range, on steel posts concreted in, with matching capping and gates.',
      best='Boundary and side fences on almost every Sydney block. Private, low maintenance, and the colour never needs painting.',
      note='Height to 1.8 m as standard. Sleeper plinths under the bottom rail keep soil and mulch off the steel and off the neighbour.'),
 dict(slug='timber-lap-and-cap', name='Timber lap and cap', tier='Basic',
      what='Treated pine palings, lapped and capped, on timber or steel posts. The traditional Sydney fence.',
      best='Budget boundaries, rear fences behind planting, and anywhere a timber look is wanted at the lowest cost.',
      note='Timber weathers and moves. Steel posts and a capping rail extend its life; painting or staining extends it further.'),
 dict(slug='ezy-clip-lap-and-cap', name='Ezy Clip lap and cap', tier='Premium',
      what='A modular lap-and-cap system that clips together on steel posts, giving the timber profile with a faster, tidier build and no exposed fixings.',
      best='Front and feature fences where the lap-and-cap look is wanted without the movement and maintenance of raw timber.',
      note='Premium over timber because the components and the finish cost more; the trade is a fence that stays straight.'),
 dict(slug='aluminium', name='Aluminium', tier='Premium',
      what='Powder-coated aluminium slat, blade and picket fencing. Never rusts, never needs painting, and takes curves and steps cleanly.',
      best='Front fences, pool fencing, side returns and anywhere the fence is part of the architecture.',
      note='The premium fence. Slat spacing sets privacy; blade fencing sets the modern look; pool fencing is built to the pool code.'),
]
FENCE_TIERS = tiers('Fencing is priced per metre at the tier you choose, gates per unit.',
    [('Fence', 'Timber lap and cap', 'Colorbond', 'Ezy Clip lap and cap, or aluminium slat, blade or picket'),
     ('Gates', 'Colorbond, matched to the fence', 'Colorbond, matched to the fence', 'Aluminium, or custom metal'),
     ('Character', 'Traditional timber, lowest cost', 'Private, colour-fast, the Sydney default', 'Straight, sharp, architectural')])
for fc in FENCE:
    write(f"residential/fencing-gates/{fc['slug']}.html", page(f"/residential/fencing-gates/{fc['slug']}/", 'residential',
        f"{fc['name']} Fencing Sydney | {fc['tier']} Tier | Estate Landscapers",
        f"{fc['name']} fencing installed across Sydney as part of a landscape package. {fc['what']} {fc['tier']} tier.",
        ('Fencing and gates', '/residential/fencing-gates/'), fc['tier'] + ' tier',
        f"{e(fc['name'])} fencing: <em>{ {'Basic':'the budget boundary','Standard':'the Sydney default','Premium':'the fence that stays straight'}[fc['tier']] }</em>.",
        e(fc['what']), f"{fc['name']} fence, installed, full run",
        band('Where it works', 'What the fence is for.', f'''    <div class="g2 mt"><div>
      <p class="sub"><b>Best for.</b> {e(fc['best'])}</p>
      <p class="sub" style="margin-top:12px"><b>Worth knowing.</b> {e(fc['note'])}</p>
    </div><div class="panel"><h3>At a glance</h3><dl class="facts">
      <div><dt>Tier on your quote</dt><dd>{fc['tier']}</dd></div>
      <div><dt>Posts</dt><dd>Steel, concreted in</dd></div>
      <div><dt>Follows the levels</dt><dd>Stepped or raked to the ground line</dd></div>
      <div><dt>Gates</dt><dd>Matched, hung to swing true</dd></div>
    </dl></div></div>''') + FENCE_TIERS,
        [('Does the fence follow a sloping block?', 'Yes. Panels are stepped or raked to the ground line, and plinths close the gap underneath so soil and mulch stay on your side.'),
         ('Who pays for a boundary fence?', 'Dividing fences are usually shared between neighbours under NSW fencing law. We build to your instruction and can supply the quote you need for that conversation.'),
         ('Can you match an existing fence?', 'Usually. Colorbond colours are standard, and timber profiles are common. Send a photo.')],
        f"Fencing a boundary in {e(fc['name'].lower())}?", 'Send the run length and a photo of the line. It is a line on your quote at tier, gates included.',
        [('Home', HOME + '/'), ('Residential', HOME + '/residential/'), ('Fencing and gates', HOME + '/residential/fencing-gates/'), (fc['name'], '{{PAGE_URL}}')],
        hero_key=f"residential-fencing-{fc['slug']}-hero"))

# ====================================================== SOILS & MULCH =========
SOIL = [
 dict(slug='garden-mix', name='Garden Mix', tier='Basic', kind='soil',
      what='A general planting blend of soil, sand, ash, bark fines, mushroom compost and wood mulch. The workhorse bed soil.',
      best='General garden beds with exotics, hedges and screening plants.',
      note='Contains mushroom compost, which is alkaline: not for most natives, azaleas or camellias. Those beds get Native Mix.'),
 dict(slug='organic-garden-mix', name='Organic Garden Mix', tier='Standard', kind='soil',
      what='Soil blended with composted organics and chicken manure. Holds moisture, feeds the bed for the first season, and the same blend that grows vegetables.',
      best='Beds that will be planted densely, raised planters, and anything you want to establish fast.',
      note='Richer than Garden Mix, so it costs more per cubic metre and needs no fertiliser at planting.'),
 dict(slug='premium-soil-mix', name='Premium Soil Mix', tier='Premium', kind='soil',
      what='The organic blend with added composted manures and screened to a finer, cleaner texture. The best bed soil we place.',
      best='Feature beds, advanced tree planting, and designed gardens where the plant schedule is expensive enough to deserve it.',
      note='The soil is a small share of a bed\'s cost and the largest share of its success. This is where a premium tier earns its name.'),
 dict(slug='native-mix', name='Native Mix', tier='Any', kind='soil',
      what='Soil, sand, ash, bark fines and duck manure, with no mushroom compost. Free-draining and low in phosphorus.',
      best='Native beds, azaleas, camellias, and planter boxes that need drainage. Specified at whatever tier the bed sits in.',
      note='Drains faster than Garden Mix, so it is not the choice for thirsty vegetables.'),
 dict(slug='leaf-mulch', name='Leaf Mulch', tier='Basic', kind='mulch',
      what='Chipped tree prunings and leaf, the natural forest mulch. Dense, textured, breaks down into compost.',
      best='Large beds, native gardens and anywhere the budget matters more than a uniform look.',
      note='Appearance varies batch to batch. It is the mulch that feeds the soil fastest, and needs topping up sooner.'),
 dict(slug='pine-bark', name='Pine Bark', tier='Standard', kind='mulch',
      what='Bark from plantation pine, in 10, 14 and 25 mm grades. Tidy, uniform, slow to break down.',
      best='Front-of-house beds and anywhere a neat, consistent surface is wanted.',
      note='Larger grade for larger beds; 10 mm for pots and narrow strips.'),
 dict(slug='eucalyptus-mulch', name='Eucalyptus Mulch', tier='Standard', kind='mulch',
      what='A fine hardwood chip with a reddish-brown colour. Excellent weed suppression and a rich background for planting.',
      best='Beds where a finer, darker finish suits the planting.',
      note='Spread 50 to 100 mm deep. Finer grades knit together and resist wind and birds.'),
 dict(slug='hardwood-chip', name='Hardwood Chip', tier='Standard', kind='mulch',
      what='Chipped hardwood offcuts. Uniform, long-lasting and the economical decorative option.',
      best='Large areas and commercial beds where longevity between top-ups matters.',
      note='Takes years to break down, which is why it is cost-efficient over time.'),
 dict(slug='cypress-mulch', name='Cypress Mulch', tier='Premium', kind='mulch',
      what='Honey-coloured cypress with natural oils that resist termites and fungus. Holds its colour longer than any other mulch here.',
      best='Beds near the house and timber structures, and designed gardens where the mulch is part of the look.',
      note='The premium mulch by price and by lifespan. Available as a finer mulch or a larger woodchip.'),
 dict(slug='forest-fines', name='Forest Fines', tier='Standard', kind='mulch',
      what='Finely chipped and composted forest material. Dark, soft and dense, it knits into a mat that holds moisture and hides the soil completely.',
      best='Beds with dense planting, sloping beds where coarse chip would wash, and anyone who wants the dark look without dye.',
      note='Breaks down faster than bark or chip and feeds the soil as it does. Top up yearly.'),
 dict(slug='black-wood-chip', name='Black Wood Chip', tier='Premium', kind='mulch',
      what='Softwood chip dyed black with a non-toxic oxide stain. A dark, uniform, contemporary surface.',
      best='Modern frontages and courtyards where the mulch is a design element against pale paving and green planting.',
      note='Leaf litter shows against black more than any other mulch, and the colour softens over a season or two. Top-dress to refresh.'),
 dict(slug='red-wood-chip', name='Red Wood Chip', tier='Premium', kind='mulch',
      what='Softwood chip dyed a warm red-brown with a non-toxic oxide stain. Bright, uniform and slow to break down.',
      best='Feature beds and commercial frontages where colour needs to hold between maintenance visits.',
      note='Same softwood base and lifespan as black chip; the colour hides litter better than black and fades a little slower.'),
]
SOIL_TIERS = tiers('Beds are priced by the square metre; the soil and mulch specification sets the tier.',
    [('Garden mix', 'Garden Mix', 'Organic Garden Mix', 'Premium Soil Mix'),
     ('Mulch', 'Leaf Mulch (natural)', 'Pine Bark, Eucalyptus Mulch, Hardwood Chip or Forest Fines', 'Cypress Mulch, Black Wood Chip or Red Wood Chip'),
     ('Native beds', 'Native Mix at any tier', 'Native Mix at any tier', 'Native Mix at any tier')],
    'Every mulch is spread 50 to 100 mm deep over a prepared, watered bed. Thinner and it fails at weeds; thicker wastes product.')
for sm in SOIL:
    kind='Soil' if sm['kind']=='soil' else 'Mulch'
    write(f"residential/planting-gardens/{sm['slug']}.html", page(f"/residential/planting-gardens/{sm['slug']}/", 'residential',
        f"{sm['name']} | {kind} for Sydney Garden Beds | Estate Landscapers",
        f"{sm['name']}: {sm['what']} {'Specified at any tier.' if sm['tier']=='Any' else sm['tier']+' tier.'}",
        ('Planting and gardens', '/residential/planting-gardens/'), f"{kind} · {sm['tier'] if sm['tier']!='Any' else 'any tier'}",
        f"{e(sm['name'])}: <em>{ {'Basic':'the economical choice','Standard':'the everyday specification','Premium':'the best we place','Any':'specified where it belongs'}[sm['tier']] }</em>.",
        e(sm['what']), f"{sm['name']} in a prepared garden bed",
        band('Where it works', f'What this {kind.lower()} is for.', f'''    <div class="g2 mt"><div>
      <p class="sub"><b>Best for.</b> {e(sm['best'])}</p>
      <p class="sub" style="margin-top:12px"><b>Worth knowing.</b> {e(sm['note'])}</p>
    </div><div class="panel"><h3>At a glance</h3><dl class="facts">
      <div><dt>Tier on your quote</dt><dd>{sm['tier']}</dd></div>
      <div><dt>Type</dt><dd>{kind}</dd></div>
      <div><dt>{'Placed' if kind=='Soil' else 'Spread'}</dt><dd>{'To the bed depth the planting needs' if kind=='Soil' else '50 to 100 mm deep'}</dd></div>
    </dl></div></div>''') + SOIL_TIERS,
        [(f"Is {e(sm['name'])} right for natives?", 'Native Mix is the safe choice for natives, azaleas and camellias because it carries no mushroom compost and drains freely. We specify it wherever the plant schedule calls for it, at any tier.' if sm['kind']=='soil' else 'Leaf mulch and forest fines suit native beds best; pine bark, chip and cypress are fine on most. Dyed chips are inert and safe but add nothing to the soil. We match mulch to the planting.'),
         ('Can I mix tiers in one yard?', 'Yes. A premium soil in the feature bed and standard elsewhere is common and is priced bed by bed.'),
         ('How much do I need?', 'We measure the beds at the site visit and the quote carries the volume. Nothing to calculate.')],
        f"Planting beds this season?", 'Photos and the plan are enough. Soil, mulch and plants are lines on the quote at the tier you choose.',
        [('Home', HOME + '/'), ('Residential', HOME + '/residential/'), ('Planting and gardens', HOME + '/residential/planting-gardens/'), (sm['name'], '{{PAGE_URL}}')],
        hero_key=f"residential-planting-{sm['slug']}-hero"))
print('fencing: 4 pages · soils and mulch: 10 pages')

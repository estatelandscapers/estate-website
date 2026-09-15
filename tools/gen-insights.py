#!/usr/bin/env python3
"""Insight articles answering the problems new-build owners in Sydney raise on
forums (Whirlpool, homeone, Reddit). Run: python3 tools/gen-insights.py"""
import os, json, sys
sys.path.insert(0, os.path.dirname(__file__))
from pagekit import e, slot, faq_ld, crumb_ld
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOME = 'https://www.estatelandscapers.com.au'
DATE = '2026-09-15'

ART = [
 dict(slug='builder-left-clay-pad-nothing-grows', title='The builder left a clay pad and nothing will grow in it',
  meta='Why new-build yards in Sydney are compacted clay and fill, what it does to turf and plants, and the three steps that fix it before anything is planted.',
  intro='The most common first sentence we hear from a new-build owner: "the builder handed over, we put turf down, and it died." The turf was never the problem.',
  secs=[('What you are actually standing on','Site cut and fill from the slab pour, compacted by every truck and tracked machine for a year, with the topsoil scraped off at the start and never returned. It sets like brick when dry and holds water like a bowl when wet. Grass roots cannot push into it and water cannot drain through it.'),
        ('Why the quick fix fails','Spreading 50 mm of soil on top and laying turf over it grows a lawn for one season. The roots hit the clay layer, water sits on it, and the lawn browns off in the first hot spell or rots in the first wet one. Fertiliser does not help a drainage problem.'),
        ('What fixes it','Three things, in order. Rip or scarify the subsoil to at least 150 mm so water and roots can enter it. Add gypsum on heavy clay to break its structure. Then build the growing profile: 100 mm of screened underlay under turf, deeper garden mix in beds, with the surface graded to fall away from the house. Every lawn we lay on a new build gets this, which is why our tier tables price the underlay as part of the turf line, not an extra.'),
        ('Ask the builder for the site classification','Your engineer\'s soil report (the "M", "H" or "E" class) tells you how reactive the clay is. Highly reactive sites need more care with drainage near the slab and are the ones where a lawn laid straight onto the pad fails fastest.')],
  faqs=[('Can I just add topsoil on top of the clay?','Not on its own. Without breaking the clay underneath, roots and water stop at the boundary between the two layers. Rip first, then build the profile.'),
        ('How deep does the soil need to be for turf?','About 100 mm of screened underlay over a ripped subsoil for lawn; 300 mm or more of garden mix in planting beds.'),
        ('Does gypsum really work on Sydney clay?','On sodic clays, which most Sydney fill is, yes. It changes the clay chemistry so it crumbles rather than smears. It is cheap and we use it as standard.')],
  related=[('/residential/turf-soft-landscaping/','Turfing'),('/residential/earthworks-excavation/','Earthworks and site preparation'),('/residential/new-build-landscaping/','New build landscaping')]),
 dict(slug='water-pooling-new-build-yard-drainage', title='Water pools in the yard after every rain',
  meta='Pooling water on a new-build block in Sydney: why it happens, what the builder is and is not responsible for, and how drainage is designed so it never comes back.',
  intro='"Drainage issues, can someone please help" is one of the longest-running thread titles on Australian home forums. The causes are nearly always the same three.',
  secs=[('The three usual causes','The site was graded flat or towards the house instead of away from it. The downpipes discharge to the surface or to a soakage pit that cannot cope with the clay. Or the neighbouring block sits higher and sheds its water onto yours without a drain to catch it.'),
        ('What the builder owes you','Under the standard building contract the builder must connect the roof water to the stormwater system and leave the site graded so water falls away from the slab. They are not obliged to landscape or to drain the yard beyond that, and most do not. Read your contract and the site plan: the finished surface levels on it are what you can hold them to.'),
        ('How it is designed properly','Surface falls first: the yard is graded so water moves towards a collection point, never towards the house. Then subsurface drains: ag pipe in gravel trenches at the low points and along the high side boundary, connected to the stormwater system or a legal discharge point. Pits where surface water needs to enter the system. Everything laid before turf, paving or beds, because drainage installed afterwards means digging up what you just paid for.'),
        ('Why we do drainage before surfaces','On every package we build, the order is earthworks, drainage, then surfaces. It is on the quote as its own line so you can see it is there. A yard that drains is the difference between a lawn that lasts and one that rots.')],
  faqs=[('Can I connect yard drains to the stormwater?','Usually, yes, to the same system the downpipes use, provided the discharge point can take the flow. On some blocks the legal point of discharge is a kerb outlet or an easement pipe; we check the site plan.'),
        ('Will a French drain fix it on its own?','It moves water; it does not create fall. Without the surface graded to it, a trench just fills. Grading and drains go together.'),
        ('The neighbour\'s water comes onto my block. Whose problem is it?','Natural overland flow is generally your neighbour\'s right, but concentrated flow from their downpipes or paving is not. A drain along the high boundary usually solves it without a dispute.')],
  related=[('/residential/landscape-drainage/','Landscape drainage'),('/residential/earthworks-excavation/','Earthworks'),('/insights/why-compliance-matters/','Why compliance matters')]),
 dict(slug='who-pays-boundary-retaining-wall-fence', title='Who pays for the boundary retaining wall and fence?',
  meta='Boundary retaining walls and dividing fences on new-build blocks in NSW: who pays, what the Dividing Fences Act covers, and why the wall and the fence are treated differently.',
  intro='On a new subdivision every block is a different level from the one beside it, so every boundary needs a wall, a fence, or both. The cost conversation with the neighbour starts before either of you has moved in.',
  secs=[('The fence and the wall are different questions','A dividing fence is covered by the Dividing Fences Act: neighbours generally share the cost of a sufficient fence equally, and there is a notice process if you cannot agree. A retaining wall is not a fence. In broad terms, the owner who changed the natural ground level, or whose land the wall supports, is responsible for it. On a new subdivision that often means the developer built the boundary walls before you bought; check your contract and the plan.'),
        ('What "sufficient fence" means','Enough to do the job of a dividing fence in that area. If you want a taller, better or Colorbond fence than your neighbour is willing to fund, you can build it, and you pay the difference. That is why we quote fencing per metre at tiers: it makes the neighbour conversation a number.'),
        ('When the wall has to be engineered','From 600 mm in height, and lower where it carries a driveway, a building or a neighbour\'s fill, the wall needs engineering and often approval. A boundary wall built without it is a problem you inherit at sale time. Our retaining walls page explains the tiers and when engineering applies.'),
        ('The practical sequence','Wall first, then fence on top of or behind it, then the yard. Building the fence before the wall is the most common expensive mistake on new estates.')],
  faqs=[('Do I have to split the fence cost if my neighbour has not built yet?','You can serve a fencing notice on the owner of the vacant lot. Many owners choose to build and recover the share later; some estates have covenants that fix the fence type and timing.'),
        ('Can the wall and fence be one structure?','Often, with a sleeper plinth under a Colorbond fence for low level changes. Above that the wall is engineered separately and the fence sits on it.'),
        ('What if the developer\'s wall is failing?','Get it assessed and documented before you build anything on top of it. Repairing a wall after fencing and turf are in costs multiples.')],
  related=[('/residential/retaining-walls/','Retaining walls'),('/residential/fencing-gates/','Fencing and gates'),('/insights/retaining-wall-approval-nsw/','Retaining wall approval in NSW')]),
 dict(slug='landscaping-required-for-occupation-certificate', title='Do I need landscaping to get my Occupation Certificate?',
  meta='What the Occupation Certificate (OC) usually requires of your landscaping on a NSW new build, what it does not, and how to sequence the work so the certifier signs off.',
  intro='A surprising number of new-build owners learn at the last minute that the certifier wants the front yard finished before they can move in. Whether that applies to you depends on your approval.',
  secs=[('Read your conditions of consent','A DA or CDC approval carries conditions. For most new homes they include the driveway and crossover, stormwater connection, and a landscape plan for the front setback: turf, planting, sometimes a minimum soft-landscaped area. The certifier checks those before issuing the OC. Backyard landscaping is rarely a condition; the frontage often is.'),
        ('What the certifier actually looks for','Driveway built to the approved plan and the council crossover complete; stormwater connected and pits in place; the front landscaping matching the plan closely enough to be recognisable; retaining walls with engineering certification where required. They are not judging your garden; they are ticking conditions.'),
        ('Sequencing so it does not hold you up','Book the landscaper before practical completion, not after. Driveway and crossover need council inspections, and turf needs a fortnight to knit before it survives a certifier walking on it. On our packages the OC items go first and the paperwork is handed to your certifier without you chasing it.'),
        ('If you are already late','A staged approach works: front yard and driveway to the conditions now, the rest after you move in. We can quote it that way.')],
  faqs=[('Is a front lawn enough, or does it have to match the landscape plan?','It has to be a fair reflection of the approved plan. Substituting species is usually fine; leaving out the planting is not.'),
        ('Can I get the OC and landscape later?','Some certifiers accept an interim OC with landscaping as an outstanding item; many do not. Ask yours early rather than assuming.'),
        ('Who supplies the retaining wall certification?','The engineer who designed it, after inspecting it during construction. We coordinate that and hand the certificate to your certifier.')],
  related=[('/insights/why-compliance-matters/','Why compliance matters'),('/residential/concrete-driveways/','Concrete works and crossovers'),('/insights/when-to-book-landscaper-new-build/','When to book a landscaper')]),
 dict(slug='council-driveway-crossover-approval-delays', title='The council crossover is holding up the driveway',
  meta='Why council driveway crossovers delay new-build handovers in Sydney, what the council inspects, and how to get the layback and footpath approved without a second trip.',
  intro='The driveway is on your land. The crossover, layback and footpath section are on council\'s. That line on the plan is where most driveway delays begin.',
  secs=[('Two approvals, not one','Your house approval covers the driveway on your lot. The crossover needs its own council application and inspection, to the council\'s standard drawing for the width, the profile and the concrete specification. Councils differ; some want the formwork inspected before the pour, others inspect after.'),
        ('What goes wrong','Applying late, so the inspection date lands after the move-in date. Pouring the crossover with the driveway before the council has seen the formwork, then being told to break it out. Building to the wrong width or without the footpath tie-in. Damaging the kerb or footpath during construction and being invoiced by council for the repair.'),
        ('How we run it','The crossover application goes in when the package is booked. The formwork is set to the council drawing and inspected before concrete, and the pour, kerb and footpath are finished to the specification so the final certificate issues first time. That certificate is what your certifier needs.'),
        ('Budget for it separately','Council application and inspection fees, plus any restoration bond, sit outside the construction cost. We show them as their own line so they are not a surprise.')],
  faqs=[('How long does the crossover application take?','Typically two to four weeks for approval, plus the inspection lead time. Book it at the same time as the driveway, not when the driveway is finished.'),
        ('Can the crossover be a different finish to the driveway?','Councils generally require plain concrete on the crossover regardless of the driveway finish, because they own and maintain it.'),
        ('Do I need a crossover on a battle-axe block?','Yes if the access handle meets the street; the same standard drawing applies.')],
  related=[('/residential/concrete-driveways/','Concrete works'),('/residential/concrete-driveways/plain-concrete/','Plain concrete'),('/insights/landscaping-required-for-occupation-certificate/','Landscaping and the OC')]),
 dict(slug='new-build-landscaping-budget-not-in-contract', title='Landscaping was not in the build contract. What does it actually cost?',
  meta='Why landscaping sits outside most NSW build contracts, what a realistic new-build landscape budget covers, and how tiered quoting stops the number blowing out.',
  intro='"We finished the house and had nothing left for the yard" is the second most common forum post after drainage. It is not carelessness; the build contract is written so landscaping falls outside it.',
  secs=[('Why it is excluded','Volume builders quote to the slab and the house. Retaining, fencing, driveway beyond the garage, paths, turf, beds and drainage are "external works" and are either a provisional sum that is never enough or left out entirely. Display homes are landscaped; the contract is not.'),
        ('What a complete package includes','Site preparation and drainage, retaining where the block steps, fencing and gates, driveway and crossover, paths and paving, turf over underlay, beds with soil and mulch, planting, edging, and the small things: letterbox, clothesline, irrigation to beds. Leave one out and someone else is standing in your driveway six months later.'),
        ('How tiers keep it honest','Every line on our quote is priced at Basic, Standard or Premium, using the same words as this website. You move lines between tiers rather than cutting whole items, so the yard is complete at the budget you have. The Standard tier is where most Sydney new builds land.'),
        ('When to start pricing','At contract signing for the house, not at handover. You will know the block levels, the drainage points and the front-setback conditions, and the landscape budget can be set beside the house budget instead of after it.')],
  faqs=[('What is the biggest hidden cost?','Retaining walls. Blocks on new estates are cut and filled, and the walls needed to hold the levels are rarely obvious from the display village.'),
        ('Can the yard be staged?','Yes. Drainage, retaining and the front setback first for the OC; paving, decking and the rest after you move in. The sequence matters more than the timing.'),
        ('Does a cheaper quote mean the same yard?','Usually it means a line is missing: drainage, underlay, engineering or the crossover. Compare the lines, not the total.')],
  related=[('/residential/new-build-landscaping/','New build landscaping'),('/the-estate-standard/','The Estate Standard'),('/residential/quote/','Get a quote')]),
 dict(slug='easement-stormwater-pit-in-backyard', title='There is an easement and a stormwater pit in my backyard',
  meta='Easements and stormwater pits on new-build blocks in NSW: what you can and cannot build over them, how to landscape around them, and who maintains the pit.',
  intro='The plan shows a shaded strip along the boundary and a square marked "pit". Both limit what can go where, and both are easier to design around than to fight.',
  secs=[('What an easement is','A right for someone else, usually the council or a neighbour, to run drainage across your land and to access it. You own the land; you cannot build a structure that prevents access or loads the pipe. Turf, planting with shallow roots, paving on a sand bed and removable fencing are generally fine. Retaining walls, slabs, sheds and pools over the easement are generally not, without the easement holder\'s consent.'),
        ('The pit','Inter-allotment drainage pits collect roof and surface water from the blocks upstream and pass it on. The lid must stay accessible and at the finished surface level. Burying it under mulch or raising the bed over it is the mistake we see most; the first blockage becomes your flooded yard.'),
        ('Designing around it','We set the pit lid to finished level, keep the easement as lawn or a pebble path where structures cannot go, and put the deck, the wall and the beds where the plan allows. Done at design stage, the easement usually disappears into the layout rather than dictating it.'),
        ('Check before you commit','The easement terms are on your title and the drainage plan is with the council. Ten minutes reading them before the deck is designed saves a demolition order later.')],
  faqs=[('Can I put a deck over an easement?','A freestanding, removable deck on posts is sometimes accepted; a concrete slab or a footing over the pipe is not. Ask the easement holder in writing.'),
        ('Who maintains the pit?','The property owner maintains what is on their land unless the easement says otherwise. Keeping the lid clear costs nothing; a blocked line costs a lot.'),
        ('Can I raise the level over an easement?','Not without consent. Fill over a pipe changes the loads and the access. Level changes are designed to leave the easement at existing grade.')],
  related=[('/residential/landscape-drainage/','Landscape drainage'),('/residential/landscape-design/','Landscape design'),('/insights/why-compliance-matters/','Why compliance matters')]),
 dict(slug='turf-dying-new-build-first-summer', title='The new turf is dying in its first summer',
  meta='Why new lawns on Sydney new builds brown off in the first summer, how to tell a watering problem from a base problem, and what saves the lawn.',
  intro='A lawn laid in spring on a new build has one job in its first summer: put roots down before the heat arrives. When it browns off, the cause is one of three things.',
  secs=[('Watering','New turf needs water every day for the first fortnight, then every second day, then weekly and deeply once it has rooted. Most first-summer failures are simply a lawn watered lightly and often, so the roots never chase water downwards. A hose timer and a deep soak beat a daily sprinkle.'),
        ('The base','If the turf was laid on a thin skim of soil over compacted clay, the roots hit a wall at 50 mm. The lawn dries out in a day because there is nowhere for water to sit, then drowns after rain because there is nowhere for it to go. This is the new-build failure; it cannot be fixed with fertiliser, only with a rebuilt base.'),
        ('The variety','Full-sun lawns in the wrong place. Sir Walter needs three to four hours of sun; TifTuf needs more. A buffalo laid in the shade of a two-storey neighbour thins out; Kikuyu laid in a small shaded yard dies. The turfing page has the sun requirements for every variety we lay.'),
        ('What saves it','Check the base first: push a screwdriver in; if it stops at 50 mm, the base is the problem. If it goes in easily, change the watering. If the lawn is shaded, change the variety. A lawn laid on a proper base with the right variety and watered in correctly is a lawn you will not think about again.')],
  faqs=[('Should I fertilise a struggling new lawn?','Not in the first six weeks. Fertiliser pushes leaf growth the roots cannot support. Water and patience first; feed once it has knitted.'),
        ('How do I know if it is dead or dormant?','Pull a runner. Green and pliable underneath means dormant; brown and brittle means dead. Buffalo and couch recover from dormancy; dead patches are replaced.'),
        ('Is Sir Grange really lower maintenance?','Yes. It grows slowly, so it is mowed less and watered less once established. It costs more to buy and repays it in the first year of mowing.')],
  related=[('/residential/turf-soft-landscaping/','Turfing and the varieties'),('/residential/care/','Care after handover'),('/residential/garden-care/','DIY garden care guide')]),
]

def page(a):
    body='\n'.join(f'  <h2 style="margin-top:34px">{e(h)}</h2>\n  <p class="sub" style="max-width:none;margin-top:10px">{e(t)}</p>' for h,t in a['secs'])
    faq='\n'.join(f'    <li>\n      <h3>{e(q)}</h3>\n      <p>{e(x)}</p>\n    </li>' for q,x in a['faqs'])
    rel=' · '.join(f'<a href="{u}" style="color:var(--blue);font-weight:700">{e(l)}</a>' for u,l in a['related'])
    cfg={"path":f"/insights/{a['slug']}/","nav":"residential","footer":"residential","title":f"{a['title']} | Estate Landscapers","description":a['meta']}
    ld=json.dumps({"@context":"https://schema.org","@type":"Article","headline":a['title'],"description":a['meta'],"url":"{{PAGE_URL}}","datePublished":DATE,"dateModified":DATE,"author":{"@type":"Organization","name":"Estate Landscapers","url":HOME+"/"},"publisher":{"@type":"Organization","name":"Estate Landscapers"}},ensure_ascii=False)
    return f'''<!--CONFIG
{json.dumps(cfg, indent=1, ensure_ascii=False)}
-->
<article class="band" style="padding-top:clamp(30px,4vw,50px)">
  <div class="shell" style="max-width:820px">
  <p class="eyebrow"><a href="/insights/" style="color:inherit;text-decoration:none">Insights</a> · New builds</p>
  <h1 style="font-size:clamp(1.55rem,3.4vw,2.3rem);font-weight:800;letter-spacing:-.02em;line-height:1.18">{e(a['title'])}</h1>
  <p style="font-size:.75rem;color:var(--label);margin-top:10px;letter-spacing:.08em;text-transform:uppercase;font-weight:700">By the Estate Landscapers team · Published 15 September 2026</p>
  <p class="sub" style="max-width:none">{e(a['intro'])}</p>
  {slot('Photo slot', a['title'] + ', illustrated on a real Sydney site', 'insights-' + a['slug'] + '-hero')}
{body}
  <h2 style="margin-top:34px">Questions people ask</h2>
  <ul class="faq" style="margin-top:12px">
{faq}
  </ul>
  <p class="sub" style="max-width:none;margin-top:24px">Related: {rel}</p>
  <div class="panel good" style="margin-top:36px">
    <h3>Dealing with this on your block?</h3>
    <p>Send photos and your site plan. We call the same business day and tell you what it needs, and what it does not.</p>
    <div class="btn-row"><a class="btn" href="/residential/quote/">Get a quote</a><a class="btn btn-o" href="/residential/new-build-landscaping/">New build landscaping</a></div>
  </div>
  </div>
</article>
<script type="application/ld+json">
{ld}
</script>
<script type="application/ld+json">
{faq_ld(a['faqs'])}
</script>
<script type="application/ld+json">
{crumb_ld([('Home',HOME+'/'),('Insights',HOME+'/insights/'),(a['title'],'{{PAGE_URL}}')])}
</script>
'''
os.makedirs(os.path.join(ROOT,'src','pages','insights'), exist_ok=True)
for a in ART: open(os.path.join(ROOT,'src','pages','insights',a['slug']+'.html'),'w').write(page(a))
# insights index cards
ip=os.path.join(ROOT,'src','pages','insights','index.html'); s=open(ip).read()
if 'New builds: the problems' not in s:
    cards='\n'.join(f'''      <a class="card" href="/insights/{a['slug']}/"><div class="in">
        <h3>{e(a['title'])}</h3><p>{e(a['meta'])}</p><span class="more">Read →</span></div></a>''' for a in ART)
    blk=f'''<section class="band tint">
  <div class="shell">
    <p class="eyebrow">New builds: the problems</p>
    <h2>What new-build owners ask, answered straight.</h2>
    <p class="sub">The questions that fill the home-building forums every week, answered for Sydney blocks.</p>
    <div class="g3 mt">
{cards}
    </div>
  </div>
</section>

'''
    i=s.index('<script type="application/ld+json">')
    s=s[:i]+blk+s[i:]
    open(ip,'w').write(s)
print('insights:', len(ART), 'articles')

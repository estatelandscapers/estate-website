"""Shared builders for service, product and guide pages.
Used by tools/gen-catalogue.py. Copy is written without em dashes."""
import json, re, html as H

CREDS = '{{include creds}}'
def e(s): return H.escape(str(s or ''), quote=False)
def strip(t): return re.sub(r'<[^>]+>', '', t)

def slot(label, desc, key=None):
    k = f' data-key="{key}"' if key else ''
    return f'<div class="plate"><div class="slot"{k}><b>{e(label)}</b><span>{e(desc)}</span></div></div>'

def faq_ld(qas, url='{{PAGE_URL}}'):
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "url": url,
        "mainEntity": [{"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in qas]}, ensure_ascii=False)

def crumb_ld(items):
    return json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}, ensure_ascii=False)

def service_ld(name, url='{{PAGE_URL}}'):
    return json.dumps({"@context": "https://schema.org", "@type": "Service", "name": name, "serviceType": name, "url": url,
        "areaServed": {"@type": "City", "name": "Sydney"},
        "provider": {"@type": "LandscapeContractor", "name": "Estate Landscapers", "legalName": "Apexx Enterprises Pty Ltd",
                     "url": "https://www.estatelandscapers.com.au/", "email": "enquiry@estatelandscapers.com.au"}}, ensure_ascii=False)

def tiers(intro, rows, note=''):
    body = '\n'.join(f'      <tr><th scope="row">{l}</th><td>{b}</td><td>{s}</td><td>{p}</td></tr>' for l, b, s, p in rows)
    n = f'<p class="sub" style="margin-top:14px;font-size:.82rem">{note}</p>' if note else ''
    return f'''
<section class="band tint">
  <div class="shell">
    <p class="eyebrow">Three ways to build it</p>
    <h2>Basic, Standard or Premium: the same job, specified three ways.</h2>
    <p class="sub">{intro} The tiers on your quote use exactly these words.</p>
    <div class="tierwrap mt"><table class="tiers">
      <thead><tr><th></th><th>Basic</th><th>Standard</th><th>Premium</th></tr></thead>
      <tbody>
{body}
      </tbody></table></div>
    {n}
  </div>
</section>
'''

def compare(eyebrow, h2, intro, cols, rows, colhead='Attribute', note=''):
    """Generic comparison: cols = [(label, href or None)], rows = [(attr, [values...])]."""
    head = ''.join(f'<th>{("<a href=%s>%s</a>" % (json.dumps(u), e(l))) if u else e(l)}</th>' for l, u in cols)
    body = '\n'.join('      <tr><th scope="row">' + e(a) + '</th>' + ''.join(f'<td>{v}</td>' for v in vals) + '</tr>' for a, vals in rows)
    n = f'<p class="sub" style="margin-top:14px;font-size:.82rem">{note}</p>' if note else ''
    return f'''
<section class="band">
  <div class="shell">
    <p class="eyebrow">{eyebrow}</p>
    <h2>{h2}</h2>
    <p class="sub">{intro}</p>
    <div class="tierwrap mt"><table class="tiers cmp">
      <thead><tr><th>{colhead}</th>{head}</tr></thead>
      <tbody>
{body}
      </tbody></table></div>
    {n}
  </div>
</section>
'''

def page(path, nav, title, meta, eyebrow_link, eyebrow, h1, lead, slot_desc, sections, qas, cta_h, cta_p, crumbs, extra_ld='', hero_key=None, cta_primary=('/residential/quote/', 'Get a quote'), cta_second=('/residential/#services', 'All services')):
    cfg = {"path": path, "nav": nav, "footer": nav, "title": title, "description": meta}
    faq = '\n'.join(f'      <li>\n        <h3>{q}</h3>\n        <p>{a}</p>\n      </li>' for q, a in qas)
    return f'''<!--CONFIG
{json.dumps(cfg, indent=1, ensure_ascii=False)}
-->
<section class="hero">
  <div class="shell">
    <div>
      <p class="eyebrow"><a href="{eyebrow_link[1]}" style="color:inherit;text-decoration:none">{e(eyebrow_link[0])}</a> · {e(eyebrow)}</p>
      <h1>{h1}</h1>
      <p class="lead">{lead}</p>
      <div class="btn-row">
        <a class="btn" href="{cta_primary[0]}">{cta_primary[1]}</a>
        <a class="btn btn-o" href="{cta_second[0]}">{cta_second[1]}</a>
      </div>
    </div>
    {slot('Photo slot', slot_desc, hero_key)}
  </div>
</section>

{CREDS}

{sections}
<section class="band tint">
  <div class="shell">
    <p class="eyebrow">Common questions</p>
    <h2>Asked before nearly every job.</h2>
    <ul class="faq">
{faq}
    </ul>
  </div>
</section>

<section class="cta">
  <div class="shell">
    <h2>{cta_h}</h2>
    <p>{cta_p}</p>
    <div class="btn-row">
      <a class="btn" href="{cta_primary[0]}">{cta_primary[1]}</a>
      <a class="btn btn-o" href="mailto:enquiry@estatelandscapers.com.au">Email us directly</a>
    </div>
  </div>
</section>

{{{{include infra-{nav}}}}}

<script type="application/ld+json">
{service_ld(strip(h1))}
</script>
<script type="application/ld+json">
{faq_ld(qas)}
</script>
<script type="application/ld+json">
{crumb_ld(crumbs)}
</script>
{extra_ld}'''

def cards(items):
    """items = [(href, title, blurb)] -> card grid without photo plates (build adds hero images)."""
    return '\n'.join(f'''      <a class="card" data-pic href="{h}"><div class="in"><h3>{t}</h3><p>{b}</p><span class="more">Read more →</span></div></a>''' for h, t, b in items)

def band(eyebrow, h2, inner, tint=False):
    return f'''
<section class="band{' tint' if tint else ''}">
  <div class="shell">
    <p class="eyebrow">{eyebrow}</p>
    <h2>{h2}</h2>
{inner}
  </div>
</section>
'''

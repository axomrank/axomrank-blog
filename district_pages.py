"""District pages: /districts/ (list of all districts) and /district/<slug>/ (one per district).

All numbers come from data/districts.json, extracted from the official Statistical Handbook,
Assam 2025 (Directorate of Economics and Statistics) by scripts/extract_handbook.py.
Pages with too little data are built but marked noindex and left out of the sitemap.
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Facts about names, kept separate from the handbook numbers.
ALIASES = {"Sribhumi": ("Karimganj", "Sribhumi was called Karimganj district until it was renamed in 2024.")}


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def inr(n):
    """Indian digit grouping: 1560589 -> 15,60,589."""
    if n is None:
        return "–"
    s = str(int(n))
    if len(s) <= 3:
        return s
    head, tail = s[:-3], s[-3:]
    head = re.sub(r"(\d)(?=(\d{2})+$)", r"\1,", head)
    return f"{head},{tail}"


def ordinal(n):
    return f"{n}{'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"


def rank(items, key, name, reverse=True):
    vals = sorted((x for x in items if key(x) is not None), key=key, reverse=reverse)
    for i, x in enumerate(vals, 1):
        if x["name"] == name:
            return i, len(vals)
    return None, len(vals)


def mentions(papers, names):
    """Real exam questions whose text or options mention the district."""
    pat = re.compile(r"\b(" + "|".join(re.escape(n) for n in names) + r")\b", re.I)
    out = []
    for p in papers or []:
        for r in p["qs"]:
            text = " ".join([r["question"], r["context"]] + [r.get(f"option_{x}", "") for x in "abcd"])
            if pat.search(text):
                out.append((p, r))
    return out


def build(site, page, out, urls, utm, papers, published_topics):
    data = json.loads((ROOT / "data" / "districts.json").read_text(encoding="utf-8"))
    base = site["base_url"]
    src = data["source"]
    ds = sorted(data["districts"], key=lambda d: d["name"])
    for d in ds:
        d["slug"] = slugify(d["name"])
        d["c"] = d.get("census2011_table")
        d["thin"] = d["c"] is None
    src_line = (f'<a href="{src["url"]}" rel="nofollow">{html.escape(src["title"])}</a>, '
                f'{html.escape(src["publisher"])}')
    pop26 = lambda x: x["population"]["2026_projected"]
    area = lambda x: x["c"]["area_sq_km"] if x["c"] else None
    lit = lambda x: x["c"]["literacy"]["total"] if x["c"] else None
    colleges = lambda x: sum((x.get("colleges_2024_25") or {}).values()) or None

    # ---------- one page per district ----------
    for i, d in enumerate(ds):
        name, c = d["name"], d["c"]
        url = f"{base}/district/{d['slug']}/"
        p = d["population"]
        r_pop, n_pop = rank(ds, pop26, name)
        facts = [
            ("Projected population, 2026", inr(p["2026_projected"]) + f" ({ordinal(r_pop)} of {n_pop} districts)"),
            ("Projected population, 2025", inr(p["2025_projected"])),
            ("Population, 2011 (current boundaries)", inr(p["2011_current_boundaries"])),
        ]
        col = d.get("colleges_2024_25")
        if col:
            facts.append(("Colleges (2024-25)", f"{sum(col.values())}: " + ", ".join(
                f"{v} {k}" for k, v in col.items() if v)))
        census_html = ""
        faq = [(f"What is the population of {name} district?",
                f"The Statistical Handbook, Assam 2025 projects {name}'s population at {inr(p['2026_projected'])} for 2026 "
                f"and {inr(p['2025_projected'])} for 2025. Its 2011 population within current boundaries is {inr(p['2011_current_boundaries'])}.")]
        if c:
            sex_ratio = round(1000 * c["female"] / c["male"])
            urban_pct = round(100 * c["urban"] / c["population"], 1)
            density = round(c["population"] / c["area_sq_km"])
            r_area, n_area = rank(ds, area, name)
            r_lit, n_lit = rank(ds, lit, name)
            caveat = "" if c["same_boundaries_as_current"] else (
                f'<aside class="note"><p><strong>Older boundaries.</strong> The handbook\'s Census 2011 tables for {html.escape(name)} use the district as it was drawn before later boundary changes '
                f'(population {inr(c["population"])} there, against {inr(p["2011_current_boundaries"])} for current boundaries). Read the figures below with that in mind.</p></aside>')
            rows = [
                ("Area", f"{inr(c['area_sq_km'])} sq km ({ordinal(r_area)} largest of {n_area})"),
                ("Population density", f"{inr(density)} people per sq km"),
                ("Population", f"{inr(c['population'])} ({inr(c['male'])} male, {inr(c['female'])} female)"),
                ("Sex ratio", f"{sex_ratio} females per 1,000 males"),
                ("Urban population", f"{inr(c['urban'])} ({urban_pct}%)"),
                ("Children aged 0–6", inr(c["child_0_6"])),
                ("Literacy rate", f"{c['literacy']['total']}% (male {c['literacy']['male']}%, female {c['literacy']['female']}%; {ordinal(r_lit)} of {n_lit})"),
                ("Scheduled Castes", inr(c["sc"]) if c["sc"] is not None else "–"),
                ("Scheduled Tribes", inr(c["st"]) if c["st"] is not None else "–"),
                ("Sub-divisions", c["sub_divisions"]),
                ("Revenue circles", c["revenue_circles"]),
                ("Community development blocks", c["cd_blocks"]),
                ("Gaon panchayats", c["gaon_panchayats"] if c["gaon_panchayats"] is not None else "–"),
                ("Towns", c["towns"]),
                ("Villages", f"{inr(c['villages'])} ({inr(c['inhabited_villages'])} inhabited)"),
            ]
            census_html = f"""<h2>Census 2011 profile</h2>{caveat}
<table><tbody>{''.join(f'<tr><th>{html.escape(k)}</th><td>{v}</td></tr>' for k, v in rows)}</tbody></table>"""
            older = "" if c["same_boundaries_as_current"] else " These figures use the district's older boundaries."
            faq += [
                (f"What is the area of {name} district?", f"{inr(c['area_sq_km'])} square kilometres, according to the Statistical Handbook, Assam 2025 (Table 1.02).{older}"),
                (f"What is the literacy rate of {name} district?", f"{c['literacy']['total']}% in Census 2011: {c['literacy']['male']}% for males and {c['literacy']['female']}% for females.{older}"),
                (f"How many revenue circles and blocks are in {name}?", f"{c['revenue_circles']} revenue circles and {c['cd_blocks']} community development blocks, with {c['sub_divisions']} sub-divisions.{older}"),
            ]
        alias = ALIASES.get(name)
        alias_html = f'<p class="note">{html.escape(alias[1])}</p>' if alias else ""
        qs = mentions(papers, [name] + ([alias[0]] if alias else []))
        q_html = ""
        if qs:
            items = "".join(
                f'<li>{html.escape(r["question"][:180])}{"…" if len(r["question"]) > 180 else ""} '
                f'<a href="{base}/question-papers/{pp["slug"]}/#q{r["q_no"]}">{html.escape(pp["name"])}, Q{r["q_no"]}</a></li>'
                for pp, r in qs[:15])
            q_html = f"<h2>{name} in real exam questions</h2><p>{len(qs)} question{'s' if len(qs) > 1 else ''} in past Assam recruitment papers mention {html.escape(name)}:</p><ul>{items}</ul>"
        prev_d, next_d = ds[i - 1], ds[(i + 1) % len(ds)]
        body = f"""<article class="post wrap district">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="{base}/">Blog</a> › <a href="{base}/districts/">Districts of Assam</a> › {html.escape(name)}</nav>
  <h1>{html.escape(name)} district, Assam: population, area, literacy and facts</h1>
  <p class="dek">Key figures for {html.escape(name)} district from the official Statistical Handbook, Assam 2025: projected population, Census 2011 data, administrative units and colleges.</p>
  {alias_html}
  <div class="prose">
  <h2>Key facts</h2>
  <table><tbody>{''.join(f'<tr><th>{html.escape(k)}</th><td>{v}</td></tr>' for k, v in facts)}</tbody></table>
  {census_html}
  {q_html}
  </div>
  <aside class="cta"><p><strong>Preparing for ADRE or APSC?</strong> District facts come up in Assam GK questions. Practise with real questions in the free AxomRank app.</p><a class="btn" href="{utm(site['app_url'] + '/', 'district-' + d['slug'], 'cta')}">Practise Assam GK free</a></aside>
  <div class="prose">
  <h2>Frequently asked questions</h2>{''.join(f'<h3>{html.escape(q)}</h3><p>{html.escape(a)}</p>' for q, a in faq)}
  <h2>More districts</h2>
  <p>← <a href="{base}/district/{prev_d['slug']}/">{html.escape(prev_d['name'])}</a> · <a href="{base}/districts/">All 35 districts</a> · <a href="{base}/district/{next_d['slug']}/">{html.escape(next_d['name'])}</a> →</p>
  <h2>Sources</h2>
  <p>{src_line}: Tables 1.01 (projected population), 1.02–1.05 (Census 2011 area, administration, population and literacy) and 22.08 (colleges). The handbook notes that these figures are provisionally estimated from Census of India 2011. See <a href="{base}/about/">how to report a correction</a>.</p>
  </div>
</article>"""
        title = f"{name} District, Assam: Population, Area, Literacy and Key Facts"
        desc = (f"{name} district at a glance: projected population {inr(p['2026_projected'])} (2026)"
                + (f", area {inr(c['area_sq_km'])} sq km, literacy {c['literacy']['total']}%" if c else "")
                + ". Official figures with sources.")[:160]
        jsonld = [
            {"@context": "https://schema.org", "@type": "AdministrativeArea", "name": f"{name} district",
             "url": url, "containedInPlace": {"@type": "State", "name": "Assam"}},
            {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Blog", "item": f"{base}/"},
                {"@type": "ListItem", "position": 2, "name": "Districts of Assam", "item": f"{base}/districts/"},
                {"@type": "ListItem", "position": 3, "name": name, "item": url}]},
            {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
        ]
        html_out = page(site, title=f"{title} | AxomRank", description=desc, canonical=url, body=body,
                        jsonld=jsonld, og_type="article")
        if d["thin"]:
            # Quality gate: too few facts to deserve indexing yet.
            html_out = html_out.replace("<head>", '<head>\n<meta name="robots" content="noindex, follow">', 1)
        dd = out / "district" / d["slug"]
        dd.mkdir(parents=True, exist_ok=True)
        (dd / "index.html").write_text(html_out, encoding="utf-8")
        if not d["thin"]:
            urls.append((url, None))

    # ---------- list of districts ----------
    by_pop = sorted(ds, key=pop26, reverse=True)
    with_c = [x for x in ds if x["c"]]
    biggest_area = max(with_c, key=area)
    smallest_area = min(with_c, key=area)
    top_lit = max(with_c, key=lit)
    low_lit = min(with_c, key=lit)
    rows = "".join(
        f'<tr><td><a href="{base}/district/{x["slug"]}/">{html.escape(x["name"])}</a></td>'
        f'<td>{inr(pop26(x))}</td><td>{inr(x["population"]["2011_current_boundaries"])}</td>'
        f'<td>{inr(area(x)) if x["c"] else "–"}</td><td>{lit(x) if x["c"] else "–"}</td>'
        f'<td>{colleges(x) or "–"}</td></tr>' for x in ds)
    st = data["state"]
    faq = [
        ("How many districts are there in Assam?",
         f"Assam has {len(ds)} districts, as listed in the Statistical Handbook, Assam 2025 (Table 1.01)."),
        ("Which is the most populous district of Assam?",
         f"{by_pop[0]['name']}, with a projected population of {inr(pop26(by_pop[0]))} in 2026, followed by {by_pop[1]['name']} and {by_pop[2]['name']}."),
        ("Which is the least populous district of Assam?",
         f"{by_pop[-1]['name']}, with a projected population of {inr(pop26(by_pop[-1]))} in 2026."),
        ("Which is the largest district of Assam by area?",
         f"{biggest_area['name']}, with {inr(area(biggest_area))} sq km in the handbook's Census 2011 table (33-district framework)."),
        ("Which is the smallest district of Assam by area?",
         f"{smallest_area['name']}, with {inr(area(smallest_area))} sq km in the same table."),
        ("Which district of Assam has the highest literacy rate?",
         f"{top_lit['name']} ({lit(top_lit)}% in Census 2011). The lowest is {low_lit['name']} ({lit(low_lit)}%)."),
    ]
    practice = ""
    if "assam-geography" in published_topics:
        practice = f'''<aside class="cta"><p><strong>District questions come up in ADRE and APSC.</strong> Practise real Assam geography questions free.</p><a class="btn" href="{base}/questions/assam-geography/">Assam geography questions</a></aside>'''
    body = f"""<article class="post wrap district">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="{base}/">Blog</a> › Districts of Assam</nav>
  <h1>Districts of Assam: list of all {len(ds)} districts with population, area and literacy</h1>
  <p class="dek">All {len(ds)} districts of Assam with figures from the official Statistical Handbook, Assam 2025. Assam's projected population for 2026 is {inr(st['population_2026_projected'])}; its area is {inr(st['area_sq_km'])} sq km and its Census 2011 literacy rate {st['literacy_2011']}%.</p>
  <div class="prose">
  <h2>List of districts</h2>
  <table class="sortable"><thead><tr><th aria-sort="ascending">District</th><th>Population 2026 (projected)</th><th>Population 2011</th><th>Area (sq km)*</th><th>Literacy 2011 (%)*</th><th>Colleges</th></tr></thead>
  <tbody>{rows}</tbody></table>
  <p class="src">* From the handbook's Census 2011 tables, which list 33 districts, some with older boundaries. Bajali and Tamulpur are not listed separately there. Population 2011 is for current boundaries (Table 1.01).</p>
  <h2>Quick facts for exams</h2>
  <ul>
    <li>Most populous (2026 projection): <a href="{base}/district/{by_pop[0]['slug']}/">{by_pop[0]['name']}</a> ({inr(pop26(by_pop[0]))})</li>
    <li>Least populous: <a href="{base}/district/{by_pop[-1]['slug']}/">{by_pop[-1]['name']}</a> ({inr(pop26(by_pop[-1]))})</li>
    <li>Largest by area: <a href="{base}/district/{biggest_area['slug']}/">{biggest_area['name']}</a> ({inr(area(biggest_area))} sq km)</li>
    <li>Smallest by area: <a href="{base}/district/{smallest_area['slug']}/">{smallest_area['name']}</a> ({inr(area(smallest_area))} sq km)</li>
    <li>Highest literacy: <a href="{base}/district/{top_lit['slug']}/">{top_lit['name']}</a> ({lit(top_lit)}%); lowest: <a href="{base}/district/{low_lit['slug']}/">{low_lit['name']}</a> ({lit(low_lit)}%)</li>
  </ul>
  </div>
  {practice}
  <div class="prose">
  <h2>Frequently asked questions</h2>{''.join(f'<h3>{html.escape(q)}</h3><p>{html.escape(a)}</p>' for q, a in faq)}
  <h2>Sources</h2><p>{src_line}, Tables 1.01–1.05 and 22.08 (<a href="{src['pdf']}" rel="nofollow">PDF</a>). The handbook notes that these figures are provisionally estimated from Census of India 2011. Extracted with a script whose checks confirm that district figures add up to the handbook's state totals.</p>
  </div>
</article>
<script>
const table = document.querySelector('table.sortable');
table.querySelectorAll('th').forEach(function (th, i) {{
  const button = document.createElement('button');
  button.type = 'button';
  button.textContent = th.textContent;
  th.replaceChildren(button);
  button.addEventListener('click', function () {{
    const tb = table.tBodies[0];
    const asc = th.getAttribute('aria-sort') !== 'ascending';
    const rows = Array.from(tb.rows);
    rows.sort(function (a, b) {{
      const x = a.cells[i].textContent.replace(/,/g, ''), y = b.cells[i].textContent.replace(/,/g, '');
      const nx = parseFloat(x), ny = parseFloat(y);
      if (isNaN(nx) || isNaN(ny)) return asc ? x.localeCompare(y) : y.localeCompare(x);
      return asc ? nx - ny : ny - nx;
    }});
    rows.forEach(function (r) {{ tb.appendChild(r); }});
    table.querySelector('[aria-sort]').removeAttribute('aria-sort');
    th.setAttribute('aria-sort', asc ? 'ascending' : 'descending');
  }});
}});
</script>"""
    url = f"{base}/districts/"
    (out / "districts").mkdir(parents=True, exist_ok=True)
    (out / "districts" / "index.html").write_text(page(
        site, title=f"Districts of Assam: List of All {len(ds)} Districts with Population and Area | AxomRank",
        description=f"List of all {len(ds)} districts of Assam with 2026 projected population, area, literacy and colleges, from the official Statistical Handbook, Assam 2025.",
        canonical=url, body=body, og_type="article",
        jsonld=[{"@context": "https://schema.org", "@type": "ItemList", "name": "Districts of Assam",
                 "numberOfItems": len(ds), "itemListElement": [
                     {"@type": "ListItem", "position": k + 1, "name": x["name"], "url": f"{base}/district/{x['slug']}/"}
                     for k, x in enumerate(ds)]},
                {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
                    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}]),
        encoding="utf-8")
    urls.append((url, None))
    print(f"built {len(ds)} district pages ({sum(1 for x in ds if x['thin'])} noindex) and the districts list")

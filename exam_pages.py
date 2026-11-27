"""Exam hub pages (/adre/, /apsc-cce/, ...) and syllabus pages (/syllabus/<exam>/).

Facts come from two places only:
  * the real previous-year papers (assam-exam-pyq), counted here, and
  * official syllabus text (APSC CCE only, data/apsc-official-syllabus/, extracted from the official PDFs).
Dates, vacancies, fees and results are never written here: hubs send readers to the official site.
"""
import collections
import html
import re
from pathlib import Path

from pyq_pages import EXAMS, guide_links, topic_reference

ROOT = Path(__file__).resolve().parent

HUBS = [
    {
        "slug": "adre", "short": "ADRE", "name": "ADRE (Assam Direct Recruitment Exam)",
        "exams": ["ADRE"], "body": "State Level Recruitment Commission (SLRC), Assam",
        "official": ("Government of Assam SLRC recruitment page", "https://directoradulteducation.assam.gov.in/latest/recruitment-of-grade-iii-and-grade-iv-through-slrc"),
        "about": "ADRE is the common written exam for Grade III and Grade IV posts in Assam government departments. "
                 "Grade III has separate papers for HSSLC, graduate and driver posts; Grade IV has papers for HSLC and Class VIII posts.",
        "groups": [("Grade III", lambda p: p["paper_code"].startswith("G3")),
                   ("Grade IV", lambda p: p["paper_code"].startswith("G4"))],
        "post_tag": "ADRE",
        "syllabus_title": "ADRE Syllabus for Grade 3 and Grade 4: Topic-wise, from Real Papers",
    },
    {
        "slug": "apsc-cce", "short": "APSC CCE", "name": "APSC CCE (Combined Competitive Examination)",
        "exams": ["APSC-CCE-Prelims"], "body": "Assam Public Service Commission (APSC)",
        "official": ("apsc.nic.in", "https://apsc.nic.in/"),
        "about": "The APSC Combined Competitive Examination recruits officers for the Assam Civil Service and allied services. "
                 "It has a preliminary exam (two objective papers), a main exam (written papers) and an interview.",
        "groups": [("Prelims GS Paper I", lambda p: p["paper_code"] == "GS-I"),
                   ("Prelims GS Paper II (CSAT)", lambda p: p["paper_code"] == "GS-II")],
        "post_tag": "APSC",
        "official_syllabus": "apsc-official-syllabus",
        "syllabus_title": "APSC CCE Syllabus: Official Prelims and Mains Syllabus, with What Gets Asked",
    },
    {
        "slug": "assam-police", "short": "Assam Police", "name": "Assam Police SI and Constable",
        "exams": ["Assam-Police-SI", "Assam-Police-Constable"], "body": "State Level Police Recruitment Board (SLPRB), Assam",
        "official": ("slprbassam.in", "https://slprbassam.in/"),
        "about": "SLPRB Assam recruits Sub-Inspectors and Constables for Assam Police through a written test, "
                 "physical tests and document verification.",
        "groups": [("Sub-Inspector (SI)", lambda p: p["exam"] == "Assam-Police-SI"),
                   ("Constable", lambda p: p["exam"] == "Assam-Police-Constable")],
        "post_tag": "Assam Police",
        "syllabus_title": "Assam Police SI and Constable Syllabus: Topic-wise, from Real Papers",
    },
    {
        "slug": "assam-tet", "short": "Assam TET", "name": "Assam TET (Teacher Eligibility Test)",
        "exams": ["TET"], "body": "Samagra Shiksha, Assam",
        "official": ("Samagra Shiksha Axom", "https://ssa.assam.gov.in/"),
        "about": "Assam holds separate teacher eligibility examinations for different levels. "
                 "The historical booklets below include Higher Secondary TET and Special TET.",
        "groups": [("Higher Secondary TET Paper I", lambda p: p["paper_code"] == "Paper-I"),
                   ("Higher Secondary TET Paper II, Commerce", lambda p: p["paper_code"] == "Paper-II"),
                   ("Special TET Paper I", lambda p: p["paper_code"] == "Special-Paper-I")],
        "post_tag": "Assam TET",
        "syllabus_title": "Assam Higher Secondary and Special TET: Topic-wise Analysis of Past Papers",
    },
    {
        "slug": "dme", "short": "DME Assam", "name": "DME Assam Grade III",
        "exams": ["DME"], "body": "Directorate of Medical Education (DME), Assam",
        "official": ("DME Assam recruitment notices", "https://dme.assam.gov.in/document-details/recruitment"),
        "about": "DME Assam publishes separate notices for Grade III technical and non-technical recruitment. "
                 "The practice questions here cover the readable parts of two past booklets.",
        "groups": [("Grade III Technical", lambda p: p["paper_code"] == "G3-Technical"),
                   ("Grade III Non-Technical", lambda p: p["paper_code"] == "G3-NonTechnical")],
        "post_tag": "DME Assam",
        "syllabus_title": "DME Assam Grade III Syllabus and Topics from Previous-Year Papers",
    },
]


def _pct(c, n):
    v = 100 * c / n
    return "<1%" if 0 < v < 1 else f"{round(v)}%"


def _ld_crumbs(base, items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}


def _faq_ld(faq):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}


def _subject_table(qs):
    n = len(qs)
    rows = []
    by_subject = collections.Counter(r["subject"] for r in qs)
    for subj, c in by_subject.most_common():
        rows.append(f"<tr><td><strong>{html.escape(subj)}</strong></td><td>{c}</td><td>{_pct(c, n)}</td></tr>")
    head = "<th>Subject</th><th>Questions</th><th>Share</th>"
    return f"<table><thead><tr>{head}</tr></thead><tbody>{''.join(rows)}</tbody></table>"


def _official_box(hub):
    if hub["official"]:
        label, url = hub["official"]
        where = f'the official website, <a href="{url}" rel="nofollow">{label}</a>'
    else:
        where = f"the official notice from the {html.escape(hub['body'])}"
    return (f'<aside class="note"><p><strong>Dates, vacancies, admit cards and results</strong> are announced only in official notices. '
            f"AxomRank does not repeat dates it cannot verify, so check {where} before you apply.</p></aside>")


def _official_syllabus_html(folder, md):
    parts = []
    titles = {
        "01-prelims-gs-i": "Prelims: General Studies Paper I",
        "02-prelims-gs-ii-csat": "Prelims: General Studies Paper II (CSAT)",
        "03-mains-gs-i": "Mains: General Studies I",
        "04-mains-gs-ii": "Mains: General Studies II",
        "05-mains-gs-iii": "Mains: General Studies III",
        "06-mains-gs-iv-ethics": "Mains: General Studies IV (Ethics)",
        "07-mains-gs-v-assam": "Mains: General Studies V (Assam paper)",
    }
    for f in sorted((ROOT / "data" / folder).glob("*.md")):
        head, body = f.read_text(encoding="utf-8").split("---\n", 1)
        pdf = head.split("pdf:", 1)[1].strip()
        md.reset()
        parts.append(f'<h3 id="{f.stem}">{html.escape(titles.get(f.stem, f.stem))}</h3>'
                     f'<blockquote class="official">{md.convert(body)}</blockquote>'
                     f'<p class="src">Source: <a href="{pdf}" rel="nofollow">official APSC syllabus (PDF)</a></p>')
    return "".join(parts)


def build(site, page, out, urls, utm, papers, posts, md, published_topics, practice_guides):
    if not papers:
        return
    base = site["base_url"]
    cards = []
    for hub in HUBS:
        hp = [p for p in papers if p["exam"] in hub["exams"]]
        if not hp:
            continue
        qs = [r for p in hp for r in p["qs"]]
        n = len(qs)
        years = sorted({p["year"] for p in hp})
        hub_url = f"{base}/{hub['slug']}/"
        syl_url = f"{base}/syllabus/{hub['slug']}/"
        app = utm(site["app_url"] + "/", hub["slug"], "cta")

        # ---------- hub ----------
        paper_rows = "".join(
            f'<tr><td>{p["year"]}</td><td><a href="{base}/question-papers/{p["slug"]}/">{html.escape(p["name"])}</a></td><td>{len(p["qs"])}</td></tr>'
            for p in hp)
        group_rows = []
        for gname, pred in hub["groups"]:
            gp = [p for p in hp if pred(p)]
            if gp:
                sizes = sorted({len(p["qs"]) for p in gp})
                group_rows.append(f"<tr><td>{html.escape(gname)}</td><td>{len(gp)}</td>"
                                  f"<td>{' or '.join(str(s) for s in sizes)}</td></tr>")
        top_topics = collections.Counter((r["subject"], r["topic"]) for r in qs if r["topic"]).most_common(10)
        topic_list = "".join(
            f'<li>{topic_reference(base, s, t, published_topics)} ({html.escape(s)}): {c} questions</li>'
            for (s, t), c in top_topics)
        notices = sorted((p for p in posts if p.get("notice_exam") == hub["slug"]),
                         key=lambda p: p["notice_date"], reverse=True)
        latest_notice = ""
        if notices:
            latest, *older = notices
            earlier = "".join(f'<li><a href="{base}/{p["path"]}/">{html.escape(p["title"])}</a></li>' for p in older)
            history = f'<h3>Earlier notices</h3><ul>{earlier}</ul>' if earlier else ""
            latest_notice = f'''<aside class="note">
  <p><strong>Latest notice covered</strong> <time datetime="{latest['notice_date']}">{latest['notice_date']}</time></p>
  <p><a href="{base}/{latest['path']}/">{html.escape(latest['title'])}</a>
  · <a href="{html.escape(latest['notice_source'])}">Official notice</a></p>{history}
</aside>'''
        rel_posts = [p for p in posts if hub["post_tag"] in p["exam"] + p["tags"] and not p.get("notice_exam")]
        post_list = "".join(f'<li><a href="{base}/{p["path"]}/">{html.escape(p["title"])}</a></li>' for p in rel_posts)
        top_subj, top_c = collections.Counter(r["subject"] for r in qs).most_common(1)[0]
        faq = [
            (f"Who conducts the {hub['short']} exam?", f"The {hub['short']} papers analysed here were set by the {hub['body']}."),
            (f"Which subject has the most questions in {hub['short']}?",
             f"Across {len(hp)} real papers ({n} questions), {top_subj} has the most questions: {top_c} ({round(100 * top_c / n)}%)."),
            (f"Where can I find the {hub['short']} exam date and notification?",
             "Only in the official notice. AxomRank does not publish dates it cannot verify from an official source."),
            (f"Where can I practise {hub['short']} previous year questions for free?",
             f"Every question from the {len(hp)} papers listed on this page is free on AxomRank, typed out with answers, and in the free AxomRank app."),
        ]
        body = f"""<article class="post wrap pyq">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="{base}/">Blog</a> › <a href="{base}/exams/">Exams</a> › {html.escape(hub['short'])}</nav>
  <h1>{html.escape(hub['name'])}: syllabus, previous year papers and preparation</h1>
  <p class="dek">{html.escape(hub['about'])} This page brings together everything AxomRank has on {html.escape(hub['short'])}, built from {len(hp)} real papers ({n:,} questions, {years[0]}–{years[-1]}).</p>
  {_official_box(hub)}
  {latest_notice}
  <p><a class="btn" href="{syl_url}">{html.escape(hub['short'])} syllabus</a> <a class="btn ghost" href="{base}/question-papers/#{EXAMS[hub['exams'][0]][1]}">Previous year papers</a></p>
  <div class="prose">
  <h2>Exam at a glance</h2>
  <table><tbody>
    <tr><th>Conducted by</th><td>{html.escape(hub['body'])}</td></tr>
    <tr><th>Real papers on AxomRank</th><td>{len(hp)} ({years[0]}–{years[-1]})</td></tr>
    <tr><th>Questions analysed</th><td>{n:,}</td></tr>
  </tbody></table>
  <h3>Questions per paper, from the real papers</h3>
  <table><thead><tr><th>Paper</th><th>Papers held</th><th>Questions per paper</th></tr></thead><tbody>{''.join(group_rows)}</tbody></table>
  <h2>What the papers ask: subject-wise</h2>
  {_subject_table(qs)}
  <h2>Most-asked topics</h2>
  <ol>{topic_list}</ol>
  {guide_links([g for g in practice_guides if g['exam'] in hub['exams']], base, 'Worked practice guides')}
  <h2>Previous year question papers</h2>
  <table><thead><tr><th>Year</th><th>Paper (with answers)</th><th>Questions</th></tr></thead><tbody>{paper_rows}</tbody></table>
  {'<h2>Preparation guides</h2><ul>' + post_list + '</ul>' if post_list else ''}
  </div>
  <aside class="cta"><p><strong>Start preparing today, free.</strong> AxomRank has bilingual lessons and these previous-year questions with spaced review. It works offline, and you don't need a login.</p><a class="btn" href="{app}">Practise {html.escape(hub['short'])} free</a></aside>
  <div class="prose">
  <h2>Frequently asked questions</h2>{''.join(f'<h3>{html.escape(q)}</h3><p>{html.escape(a)}</p>' for q, a in faq)}
  <h2>Sources</h2><p>Counts come from the question booklets in the open <a href="https://github.com/axomrank/assam-exam-pyq">AxomRank PYQ dataset</a>. See <a href="{base}/about/">how to report a correction</a>.</p>
  </div>
</article>"""
        title = f"{hub['short']} Exam: Syllabus, Previous Year Papers and Preparation"
        desc = (f"{hub['short']} in one place: subject-wise analysis of {len(hp)} real papers ({n:,} questions), "
                f"the syllabus, every previous year paper with answers, and free practice.")[:160]
        d = out / hub["slug"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(page(
            site, title=f"{title} | AxomRank", description=desc, canonical=hub_url, body=body, og_type="article",
            jsonld=[{"@context": "https://schema.org", "@type": "WebPage", "name": title, "url": hub_url, "description": desc},
                    _ld_crumbs(base, [("Blog", f"{base}/"), ("Exams", f"{base}/exams/"), (hub["short"], hub_url)]),
                    _faq_ld(faq)]), encoding="utf-8")
        urls.append((hub_url, None))

        # ---------- syllabus ----------
        sections = []
        if hub.get("official_syllabus"):
            sections.append(f"""<h2 id="official">Official syllabus</h2>
<p>The text below is the syllabus as published by {html.escape(hub['body'])}, extracted from the official PDFs. Always check the latest notification for changes.</p>
{_official_syllabus_html(hub['official_syllabus'], md)}""")
            measured_intro = "How the official syllabus is actually tested, counted from the real prelims papers:"
        else:
            sections.append(f"""<aside class="note"><p><strong>What these papers cover.</strong> These topic counts come from the available questions in {len(hp)} past papers. Check the current official notice for the exam pattern and complete syllabus.</p></aside>""")
            measured_intro = "Subjects and topics as they appear in the real papers:"
        for gname, pred in hub["groups"]:
            gq = [r for p in hp if pred(p) for r in p["qs"]]
            if not gq:
                continue
            ng = len({(r["year"], r["paper_code"]) for r in gq})
            sub = []
            for subj, sc in collections.Counter(r["subject"] for r in gq).most_common():
                tops = collections.Counter(r["topic"] for r in gq if r["subject"] == subj and r["topic"]).most_common()
                items = []
                for t, tc in tops:
                    subs = collections.Counter(r["subtopic"] for r in gq if r["subject"] == subj and r["topic"] == t and r["subtopic"]).most_common(8)
                    sub_txt = ", ".join(f"{html.escape(s)} ({c})" for s, c in subs)
                    items.append(f'<li>{topic_reference(base, subj, t, published_topics, bold=True)} · {tc} questions'
                                 + (f'<br><span class="subs">{sub_txt}</span>' if sub_txt else "") + "</li>")
                sub.append(f"<h3>{html.escape(subj)} <span class=\"count\">{sc} questions, {_pct(sc, len(gq))}</span></h3><ul>{''.join(items)}</ul>")
            sections.append(f'<h2 id="{re.sub(r"[^a-z0-9]+", "-", gname.lower()).strip("-")}">{html.escape(gname)}</h2>'
                            f"<p>{measured_intro} {ng} paper{'s' if ng > 1 else ''}, {len(gq)} questions.</p>"
                            f"{_subject_table(gq)}{''.join(sub)}")
        faq_s = [
            (f"What is the {hub['short']} syllabus?",
             f"The papers analysed here cover {', '.join(s for s, _ in collections.Counter(r['subject'] for r in qs).most_common(6))}. "
             "The full topic list with question counts is on this page."),
            (f"Which topics are asked most in {hub['short']}?",
             "; ".join(f"{t} ({c} questions)" for (s, t), c in top_topics[:5]) + "."),
            (f"Is this the official {hub['short']} syllabus?",
             "The APSC text on this page is official. For the other exams, this page shows the syllabus as tested in the real papers; the official notice is the final authority."
             if hub.get("official_syllabus") else
             "No. It is the syllabus as tested in the real papers, which shows where the marks actually go. The official notice is the final authority."),
        ]
        toc = "".join(f'<li><a href="#{re.sub(r"[^a-z0-9]+", "-", g.lower()).strip("-")}">{html.escape(g)}</a></li>' for g, _ in hub["groups"])
        if hub.get("official_syllabus"):
            toc = '<li><a href="#official">Official syllabus</a></li>' + toc
        body = f"""<article class="post wrap pyq syllabus">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="{base}/">Blog</a> › <a href="{hub_url}">{html.escape(hub['short'])}</a> › Syllabus</nav>
  <h1>{html.escape(hub['syllabus_title'])}</h1>
  <p class="dek">Subject-wise and topic-wise {html.escape(hub['short'])} syllabus, with the number of questions each topic carried in {len(hp)} real papers ({years[0]}–{years[-1]}). Tap a topic to practise its real questions.</p>
  <details class="toc"><summary>On this page</summary><ul>{toc}</ul></details>
  <div class="prose">{''.join(sections)}</div>
  <aside class="cta"><p><strong>Turn the syllabus into a study plan.</strong> AxomRank's free lessons follow these topics, with spaced review and real questions.</p><a class="btn" href="{utm(site['app_url'] + '/', 'syllabus-' + hub['slug'], 'cta')}">Start the free lessons</a></aside>
  <div class="prose">
  <h2>Frequently asked questions</h2>{''.join(f'<h3>{html.escape(q)}</h3><p>{html.escape(a)}</p>' for q, a in faq_s)}
  <h2>Sources</h2><p>Question counts: the open <a href="https://github.com/axomrank/assam-exam-pyq">AxomRank PYQ dataset</a>. {'Official text: APSC syllabus PDFs, linked under each paper.' if hub.get('official_syllabus') else ''} Back to the <a href="{hub_url}">{html.escape(hub['short'])} hub</a>.</p>
  </div>
</article>"""
        desc_s = (f"{hub['short']} syllabus, subject-wise and topic-wise, with how many questions each topic carried in "
                  f"{len(hp)} real papers. {'Official prelims and mains text included.' if hub.get('official_syllabus') else 'Free practice for every topic.'}")[:160]
        d = out / "syllabus" / hub["slug"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(page(
            site, title=f"{hub['syllabus_title']} | AxomRank", description=desc_s, canonical=syl_url, body=body, og_type="article",
            jsonld=[{"@context": "https://schema.org", "@type": "LearningResource", "name": hub["syllabus_title"], "url": syl_url,
                     "description": desc_s, "learningResourceType": "Syllabus", "isAccessibleForFree": True, "inLanguage": "en-IN"},
                    _ld_crumbs(base, [("Blog", f"{base}/"), (hub["short"], hub_url), ("Syllabus", syl_url)]),
                    _faq_ld(faq_s)]), encoding="utf-8")
        urls.append((syl_url, None))
        cards.append(f'<article class="card"><p class="meta">{len(hp)} papers · {n:,} questions</p>'
                     f'<h2><a href="{hub_url}">{html.escape(hub["name"])}</a></h2><p>{html.escape(hub["about"].split(". ")[0])}.</p>'
                     f'<p><a href="{syl_url}">Syllabus</a> · <a href="{hub_url}">Papers and preparation</a></p></article>')

    exams_url = f"{base}/exams/"
    guide = next((p for p in posts if p["slug"] == "assam-government-exams"), None)
    guide_link = (f'<p><a href="{base}/{guide["path"]}/">Compare Assam exams by qualification and career path</a></p>'
                  if guide else "")
    body = f"""<section class="hero wrap"><h1>Assam government exams: syllabus, papers and preparation</h1>
<p class="dek">One page per exam, built from real papers: what each exam asks, its syllabus topic by topic, and every previous year paper with answers.</p>
{guide_link}</section>
<section class="wrap list">{''.join(cards)}</section>"""
    (out / "exams").mkdir(exist_ok=True)
    (out / "exams" / "index.html").write_text(page(
        site, title="Assam Govt Exams: ADRE, APSC CCE, Assam Police, Assam TET Syllabus and Papers | AxomRank",
        description="Syllabus, exam pattern from real papers, and previous year papers with answers for ADRE, APSC CCE, Assam Police SI and Constable, and Assam TET.",
        canonical=exams_url, body=body,
        jsonld=[{"@context": "https://schema.org", "@type": "CollectionPage", "name": "Assam government exams", "url": exams_url}]),
        encoding="utf-8")
    urls.append((exams_url, None))
    print(f"built {len(cards)} exam hubs and syllabus pages")

"""Generate previous-year question (PYQ) pages from the assam-exam-pyq dataset.

Pages built:
  /question-papers/                      hub of all papers, grouped by exam
  /question-papers/<paper-slug>/         one full paper: every question, options, answer, explanation
  /questions/                            hub of topic pages
  /questions/<topic-slug>/               every question on one topic, across all exams

Competitors mostly host scanned PDFs. These pages are text, so every question is indexable.

The dataset is read from a local checkout of github.com/axomrank/assam-exam-pyq
(default ../assam-exam-pyq; CI checks it out into ./pyq-data).
"""
import collections
import csv
import html
import json
import re
import shutil
from pathlib import Path

EXAMS = {
    # dataset code: (display name, url slug, short name for titles)
    "ADRE": ("ADRE (Assam Direct Recruitment Exam)", "adre", "ADRE"),
    "APSC-CCE-Prelims": ("APSC CCE Prelims", "apsc-cce-prelims", "APSC CCE Prelims"),
    "Assam-Police-SI": ("Assam Police SI", "assam-police-si", "Assam Police SI"),
    "Assam-Police-Constable": ("Assam Police Constable", "assam-police-constable", "Assam Police Constable"),
    "TET": ("Assam TET", "assam-tet", "Assam TET"),
    "DME": ("DME Assam", "dme-assam", "DME Assam"),
}
EXAM_ORDER = list(EXAMS)

ANSWER_SOURCE = {
    "official_final_key": "Official final answer key",
    "official_provisional_key": "Official provisional answer key",
    "worked_solution": "Worked solution by AxomRank (no official key was published)",
    "editorial_solution": "Editorially revised practice question (the original had a defect)",
}

MIN_TOPIC_QUESTIONS = 12
GITHUB = "https://github.com/axomrank/assam-exam-pyq"


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def topic_slug(subject, topic):
    """assam-history, number-system ... (generic topic names keep their subject prefix)."""
    return slugify(subject + "-" + topic) if topic in ("Miscellaneous",) else slugify(topic)


def paper_slug(p):
    """adre-2024-grade-iii-hsslc-question-paper, apsc-cce-prelims-2023-gs-i-question-paper ..."""
    code = p["paper_code"]
    code = re.sub(r"^G3-P\d-", "grade-3-", code)
    code = re.sub(r"^G4-P\d-", "grade-4-", code)
    code = re.sub(r"^G3-", "grade-3-", code)
    code = code.replace("Degree", "graduate").replace("ClassVIII", "class-8").replace("NonTechnical", "non-technical")
    if p["exam"].startswith("Assam-Police"):
        code = ""  # one paper per exam: assam-police-si-2025-question-paper
    return "-".join(x for x in (EXAMS[p['exam']][1], p['year'], slugify(code), "question-paper") if x)


def paper_name(p):
    """Human name used in titles, e.g. 'ADRE 2024 Grade III (HSSLC) paper'."""
    short = EXAMS[p["exam"]][2]
    t = p["paper_title"]
    if p["exam"] == "ADRE":
        grade = "Grade III" if p["paper_code"].startswith("G3") else "Grade IV"
        level = {"HSSLC": "HSSLC", "Degree": "Graduate", "Driver": "Driver", "HSLC": "HSLC",
                 "ClassVIII": "Class VIII"}[p["paper_code"].split("-")[-1]]
        return f"{short} {p['year']} {grade} {level}"
    if p["exam"] == "APSC-CCE-Prelims":
        return f"{short} {p['year']} {p['paper_code'].replace('-', ' ')}"
    if p["exam"] == "TET":
        return f"{short} {p['year']} {p['paper_code'].replace('-', ' ')}"
    if p["exam"] == "DME":
        return f"{short} {p['year']} Grade III {'Technical' if 'Technical' == p['paper_code'].split('-')[-1] else 'Non-Technical'}"
    return f"{short} {p['year']}"


def text(s):
    return html.escape(s or "").replace("\n", "<br>")


def answer_letters(a):
    return [x.strip() for x in (a or "").split(",") if x.strip()]


def load(pyq_dir):
    pyq = Path(pyq_dir)
    if not (pyq / "questions.csv").exists():
        return None
    catalog = json.loads((pyq / "catalog.json").read_text(encoding="utf-8"))
    rows = list(csv.DictReader((pyq / "questions.csv").open(encoding="utf-8")))
    by_paper = collections.defaultdict(list)
    for r in rows:
        by_paper[(r["exam"], str(r["year"]), r["paper_code"])].append(r)
    for qs in by_paper.values():
        qs.sort(key=lambda r: int(r["q_no"]))
    papers = []
    for c in catalog:
        key = (c["exam"], str(c["year"]), c["paper_code"])
        if key in by_paper and c["exam"] in EXAMS:
            c = dict(c, year=str(c["year"]))
            c["slug"] = paper_slug(c)
            c["name"] = paper_name(c)
            c["qs"] = by_paper[key]
            papers.append(c)
    papers.sort(key=lambda p: (EXAM_ORDER.index(p["exam"]), -int(p["year"]), p["paper_code"]))
    return pyq, papers, rows


def topic_reference(base, subject, topic, published_topics, *, bold=False):
    slug = topic_slug(subject, topic)
    label = html.escape(topic)
    if bold:
        label = f"<strong>{label}</strong>"
    if slug in published_topics:
        return f'<a href="{base}/questions/{slug}/">{label}</a>'
    return label


def question_html(r, base, *, img_base, paper_link=None, published_topics=()):
    opts = []
    letters = answer_letters(r["answer"])
    for L in "abcd":
        v = r.get(f"option_{L}", "")
        if v:
            opts.append(f'<li><span class="ol">{L.upper()}.</span><span>{text(v)}</span></li>')
    imgs = "".join(
        f'<img src="{img_base}/{html.escape(p.split("exams/", 1)[-1])}" alt="Figure for question {r["q_no"]}" loading="lazy">'
        for p in r["images"].split("|") if p
    )
    if r["answer"] == "ALL":
        ans = "All options are accepted"
    elif letters:
        parts = []
        for L in letters:
            v = r.get(f"option_{L.lower()}", "")
            parts.append(f"({L}) {text(v)}" if v else f"({L})")
        ans = " · ".join(parts)
    else:
        ans = "No single answer could be confirmed"
    note = f'<p class="why">{text(r["answer_note"])}</p>' if r["answer_note"] else ""
    src = ANSWER_SOURCE.get(r["answer_source"], r["answer_source"])
    rev = f'<p class="flag">{text(r["revision_note"].split(".")[0])}.</p>' if r["editorially_revised"] == "1" else ""
    where = []
    if paper_link:
        where.append(paper_link)
    if not paper_link and r["topic"]:
        where.append(topic_reference(base, r["subject"], r["topic"], published_topics))
    else:
        where.append(html.escape(r["subject"]))
    ctx = f'<p class="ctx">{text(r["context"])}</p>' if r["context"] else ""
    return f"""<li class="q" id="q{r['q_no']}" value="{r['q_no']}">
  {ctx}<p class="qt">{text(r['question'])}</p>{imgs}
  <ol class="opts">{''.join(opts)}</ol>
  <details><summary><span class="answer-closed">Show answer</span><span class="answer-open">Hide answer</span></summary><p class="ans"><strong>Answer:</strong> {ans}</p>{note}{rev}<p class="src">{html.escape(src)}</p></details>
  <p class="qmeta">{' · '.join(where)}</p>
</li>"""


def build(site, page, out, urls, utm, pyq_data):
    pyq, papers, rows = pyq_data
    base = site["base_url"]
    img_base = f"{base}/pyq-img"
    paper_by_key = {(p["exam"], p["year"], p["paper_code"]): p for p in papers}
    topics = collections.defaultdict(list)
    for r in rows:
        if r["topic"] and (r["exam"], str(r["year"]), r["paper_code"]) in paper_by_key:
            topics[(r["subject"], r["topic"])].append(r)
    published_topics = {topic_slug(s, t) for (s, t), qs in topics.items() if len(qs) >= MIN_TOPIC_QUESTIONS}

    # Copy only the figures the pages use.
    for r in rows:
        for p in r["images"].split("|"):
            if p:
                dst = out / "pyq-img" / p.split("exams/", 1)[-1]
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(pyq / p, dst)

    # ---- one page per paper ----
    for p in papers:
        qs = p["qs"]
        n = len(qs)
        canonical = f"{base}/question-papers/{p['slug']}/"
        sources = collections.Counter(r["answer_source"] for r in qs)
        src_lines = "".join(f"<li>{ANSWER_SOURCE.get(k, k)}: {v} questions</li>" for k, v in sources.most_common())
        subj = collections.Counter(r["subject"] for r in qs)
        subj_rows = "".join(
            f"<tr><td>{html.escape(s)}</td><td>{c}</td><td>{round(100 * c / n)}%</td></tr>" for s, c in subj.most_common())
        has_official = any(k.startswith("official") for k in sources)
        key_word = "official answer key" if has_official else "answers and explanations"
        title = f"{p['name']} Question Paper with Answers ({n} Questions)"
        desc = (f"All {n} questions from the {p['name']} paper as text, with the {key_word}, "
                f"subject-wise breakdown and free practice. Conducted by {qs[0]['conducting_body'] or 'the board'}.")[:160]
        app_cta = utm(site["app_url"] + "/", p["slug"], "cta")
        others = [o for o in papers if o["exam"] == p["exam"] and o is not p]
        related = "".join(f'<li><a href="{base}/question-papers/{o["slug"]}/">{html.escape(o["name"])} paper</a></li>' for o in others)
        qlist = "".join(question_html(r, base, img_base=img_base, published_topics=published_topics) for r in qs)
        pdf = f"{GITHUB}/blob/main/{p['source_pdf']}"
        faq = [
            (f"How many questions are in the {p['name']} paper?",
             f"The paper has {n} multiple-choice questions. The largest subject is {subj.most_common(1)[0][0]} with {subj.most_common(1)[0][1]} questions."),
            (f"Where do the answers for the {p['name']} paper come from?",
             "; ".join(f"{ANSWER_SOURCE.get(k, k)} for {v} questions" for k, v in sources.most_common()) + "."),
            (f"Can I download the original {p['name']} question paper PDF?",
             "Yes. The original booklet PDF is linked on this page from the open AxomRank PYQ dataset on GitHub."),
        ]
        faq_html = "".join(f"<h3>{html.escape(q)}</h3><p>{html.escape(a)}</p>" for q, a in faq)
        body = f"""<article class="post wrap pyq">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="{base}/">Blog</a> › <a href="{base}/question-papers/">Question papers</a> › <a href="{base}/question-papers/#{EXAMS[p['exam']][1]}">{html.escape(EXAMS[p['exam']][2])}</a></nav>
  <h1>{html.escape(title)}</h1>
  <p class="dek">{html.escape(p['paper_title'])}. Every question is typed out below with its four options. Tap <em>Show answer</em> to check yourself, so you can use the page as a practice test.</p>
  <p class="jump-link"><a href="#questions">Jump to the questions</a></p>
  <div class="prose">
  <h2>About this paper</h2>
  <table><tbody>
    <tr><th>Exam</th><td>{html.escape(EXAMS[p['exam']][0])}</td></tr>
    <tr><th>Year</th><td>{p['year']}</td></tr>
    <tr><th>Conducted by</th><td>{html.escape(qs[0]['conducting_body'] or '-')}</td></tr>
    <tr><th>Questions</th><td>{n}</td></tr>
    <tr><th>Original PDF</th><td><a href="{pdf}" rel="nofollow">Question booklet (PDF)</a></td></tr>
  </tbody></table>
  <h3>Where the answers come from</h3>
  <ul>{src_lines}</ul>
  <h2>Subject-wise questions</h2>
  <table><thead><tr><th>Subject</th><th>Questions</th><th>Share</th></tr></thead><tbody>{subj_rows}</tbody></table>
  </div>
  <aside class="cta"><p><strong>Want a timed test instead?</strong> Practise these questions with spaced review in the free AxomRank app. It works offline, and you don't need a login to start.</p><a class="btn" href="{app_cta}">Practise free on AxomRank</a></aside>
  <h2 id="questions">All {n} questions with answers</h2>
  <ol class="qs">{qlist}</ol>
  <div class="prose">
  <h2>Frequently asked questions</h2>{faq_html}
  {'<h2>More ' + html.escape(EXAMS[p['exam']][2]) + ' papers</h2><ul>' + related + '</ul>' if related else ''}
  <h2>Sources and corrections</h2>
  <p>Questions are taken from the original booklet and are part of the open <a href="{GITHUB}">AxomRank PYQ dataset</a>. Spotted a mistake? See <a href="{base}/about/">how to report a correction</a>.</p>
  </div>
</article>"""
        jsonld = [
            {"@context": "https://schema.org", "@type": "LearningResource",
             "name": title, "description": desc, "url": canonical, "inLanguage": "en-IN",
             "learningResourceType": "Previous year question paper", "educationalLevel": EXAMS[p["exam"]][0],
             "isAccessibleForFree": True, "numberOfQuestions": n,
             "provider": {"@type": "Organization", "name": "AxomRank", "url": site["app_url"]}},
            {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Blog", "item": f"{base}/"},
                {"@type": "ListItem", "position": 2, "name": "Question papers", "item": f"{base}/question-papers/"},
                {"@type": "ListItem", "position": 3, "name": p["name"], "item": canonical}]},
            {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
        ]
        d = out / "question-papers" / p["slug"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(page(site, title=f"{title} | AxomRank", description=desc, canonical=canonical,
                                           body=body, jsonld=jsonld, og_type="article"), encoding="utf-8")
        urls.append((canonical, None))

    # ---- papers hub ----
    sections = []
    exam_links = []
    for ex in EXAM_ORDER:
        ps = [p for p in papers if p["exam"] == ex]
        if not ps:
            continue
        items = "".join(
            f'<article class="card"><p class="meta">{len(p["qs"])} questions</p>'
            f'<h3><a href="{base}/question-papers/{p["slug"]}/">{html.escape(p["name"])} question paper</a></h3>'
            f'<p>{html.escape(p["paper_title"])}</p></article>' for p in ps)
        name, slug, _ = EXAMS[ex]
        sections.append(f'<h2 id="{slug}" class="sect">{html.escape(name)}</h2>{items}')
        exam_links.append(f'<li><a href="#{slug}">{html.escape(name)}</a></li>')
    total = sum(len(p["qs"]) for p in papers)
    body = f"""<section class="hero wrap"><h1>Assam exam previous year question papers with answers</h1>
<p class="dek">{len(papers)} real papers and {total:,} questions from ADRE, APSC CCE Prelims, Assam Police, Assam TET and DME. Every question is typed out as text with its answer, and every answer says where it comes from. All free, with no PDF to download.</p>
<p class="jump-link"><a href="{base}/questions/">Browse questions by topic</a></p>
<details class="toc"><summary>Find papers by exam</summary><ul>{''.join(exam_links)}</ul></details></section>
<section class="wrap list">{''.join(sections)}</section>"""
    canonical = f"{base}/question-papers/"
    (out / "question-papers" / "index.html").write_text(page(
        site, title="Assam Exam Previous Year Question Papers with Answers (ADRE, APSC, TET, Police) | AxomRank",
        description=f"{len(papers)} Assam recruitment exam papers with {total:,} questions and answers as text: ADRE 2022 and 2024, APSC CCE Prelims 2023 to 2025, Assam Police 2025, Assam TET.",
        canonical=canonical, body=body,
        jsonld=[{"@context": "https://schema.org", "@type": "CollectionPage", "name": "Assam exam question papers", "url": canonical}]),
        encoding="utf-8")
    urls.append((canonical, None))

    # ---- topic pages ----
    topic_cards = collections.defaultdict(list)
    for (subject, topic), qs in sorted(topics.items(), key=lambda kv: -len(kv[1])):
        if len(qs) < MIN_TOPIC_QUESTIONS:
            continue
        slug = topic_slug(subject, topic)
        exams_in = sorted({EXAMS[r["exam"]][2] for r in qs}, key=lambda e: [v[2] for v in EXAMS.values()].index(e))
        exam_list = ", ".join(exams_in)
        n = len(qs)
        title = f"{topic} Questions from Assam Exams: {n} Previous Year MCQs with Answers"
        desc = f"{n} real {topic.lower()} questions asked in {exam_list} papers, with answers and explanations. Free practice for Assam govt exams."[:160]
        canonical = f"{base}/questions/{slug}/"
        qs_sorted = sorted(qs, key=lambda r: (EXAM_ORDER.index(r["exam"]), -int(r["year"]), r["paper_code"], int(r["q_no"])))
        sub = collections.Counter(r["subtopic"] for r in qs if r["subtopic"])
        sub_rows = "".join(f"<tr><td>{html.escape(s)}</td><td>{c}</td></tr>" for s, c in sub.most_common(15))
        ex_rows = "".join(f"<tr><td>{html.escape(e)}</td><td>{c}</td></tr>" for e, c in collections.Counter(EXAMS[r['exam']][2] for r in qs).most_common())
        items = []
        for r in qs_sorted:
            pp = paper_by_key[(r["exam"], str(r["year"]), r["paper_code"])]
            link = f'<a href="{base}/question-papers/{pp["slug"]}/#q{r["q_no"]}">{html.escape(pp["name"])}, Q{r["q_no"]}</a>'
            items.append(question_html(r, base, img_base=img_base, paper_link=link)
                         .replace(f'id="q{r["q_no"]}" value="{r["q_no"]}"', ""))
        body = f"""<article class="post wrap pyq">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="{base}/">Blog</a> › <a href="{base}/questions/">Questions by topic</a> › {html.escape(subject)}</nav>
  <h1>{html.escape(title)}</h1>
  <p class="dek">Every {html.escape(topic.lower())} question from {len({(r['exam'], r['year'], r['paper_code']) for r in qs})} real Assam recruitment papers, in one place. Use it to see which facts come up again and again.</p>
  <p class="jump-link"><a href="#questions">Jump to the questions</a></p>
  <div class="prose">
  <h2>Where these questions were asked</h2>
  <table><thead><tr><th>Exam</th><th>Questions</th></tr></thead><tbody>{ex_rows}</tbody></table>
  {'<h2>Most-asked subtopics</h2><table><thead><tr><th>Subtopic</th><th>Questions</th></tr></thead><tbody>' + sub_rows + '</tbody></table>' if sub_rows else ''}
  </div>
  <aside class="cta"><p><strong>Learn this topic properly.</strong> AxomRank has free bilingual lessons with spaced review. It works offline, and you don't need a login to start.</p><a class="btn" href="{utm(site['app_url'] + '/', 'topic-' + slug, 'cta')}">Open the free lessons</a></aside>
  <h2 id="questions">All {n} questions</h2>
  <ol class="qs">{''.join(items)}</ol>
  <div class="prose"><h2>Sources and corrections</h2><p>From the open <a href="{GITHUB}">AxomRank PYQ dataset</a>. Each question links back to its paper. See <a href="{base}/about/">how to report a correction</a>.</p></div>
</article>"""
        jsonld = [
            {"@context": "https://schema.org", "@type": "LearningResource", "name": title, "description": desc,
             "url": canonical, "inLanguage": "en-IN", "learningResourceType": "Practice questions",
             "isAccessibleForFree": True, "numberOfQuestions": n, "teaches": topic},
            {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Blog", "item": f"{base}/"},
                {"@type": "ListItem", "position": 2, "name": "Questions by topic", "item": f"{base}/questions/"},
                {"@type": "ListItem", "position": 3, "name": topic, "item": canonical}]},
        ]
        d = out / "questions" / slug
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(page(site, title=f"{title} | AxomRank", description=desc, canonical=canonical,
                                           body=body, jsonld=jsonld, og_type="article"), encoding="utf-8")
        urls.append((canonical, None))
        topic_cards[subject].append((topic, slug, n, exam_list))

    sections = []
    subject_links = []
    for subject in sorted(topic_cards, key=lambda s: -sum(t[2] for t in topic_cards[s])):
        cards = "".join(
            f'<article class="card"><p class="meta">{n} questions</p><h3><a href="{base}/questions/{slug}/">{html.escape(t)} questions</a></h3><p>Asked in {html.escape(ex)}</p></article>'
            for t, slug, n, ex in topic_cards[subject])
        slug = slugify(subject)
        sections.append(f'<h2 id="{slug}" class="sect">{html.escape(subject)}</h2>{cards}')
        subject_links.append(f'<li><a href="#{slug}">{html.escape(subject)}</a></li>')
    canonical = f"{base}/questions/"
    body = f"""<section class="hero wrap"><h1>Assam exam questions by topic</h1>
<p class="dek">Real previous-year questions grouped by topic across ADRE, APSC, Assam Police, TET and DME papers. Start with the topics that carry the most marks.</p>
<p class="jump-link"><a href="{base}/question-papers/">Browse full question papers</a></p>
<details class="toc"><summary>Find topics by subject</summary><ul>{''.join(subject_links)}</ul></details></section>
<section class="wrap list">{''.join(sections)}</section>"""
    (out / "questions").mkdir(exist_ok=True)
    (out / "questions" / "index.html").write_text(page(
        site, title="Assam Exam Questions by Topic: Previous Year MCQs with Answers | AxomRank",
        description="Assam history, culture, geography, polity, maths, reasoning and English questions from real ADRE, APSC, Assam Police and TET papers, grouped by topic, with answers.",
        canonical=canonical, body=body,
        jsonld=[{"@context": "https://schema.org", "@type": "CollectionPage", "name": "Assam exam questions by topic", "url": canonical}]),
        encoding="utf-8")
    urls.append((canonical, None))
    n_topics = sum(len(v) for v in topic_cards.values())
    print(f"built {len(papers)} question-paper pages, {n_topics} topic pages")
    return papers, published_topics

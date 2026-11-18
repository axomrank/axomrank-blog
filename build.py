#!/usr/bin/env python3
"""Build the AxomRank blog into _site/.

Posts live in posts/*.md with a small front-matter block:

    ---
    title: ...
    description: ...            (meta description, 120-160 characters)
    date: 2026-11-18
    updated: 2026-11-18         (optional)
    slug: adre-previous-year-questions-analysis
    exam: ADRE                  (comma-separated; becomes topic pages)
    tags: PYQ, ADRE Grade III   (comma-separated)
    cta: /                      (path in the AxomRank app for the call to action)
    cta_text: Practise ...      (button text)
    draft: false                (optional)
    ---

A "## Frequently asked questions" section whose questions are "### ..."
headings becomes FAQPage structured data automatically.

Usage:  python build.py [--base-url URL]
"""
import argparse
import datetime as dt
import html
import json
import os
import re
import shutil
from pathlib import Path
from urllib.parse import quote

import markdown

import exam_pages
import pyq_pages

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "_site"


def parse(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
    if not m:
        raise SystemExit(f"{path}: missing front matter")
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    for key in ("title", "description", "date", "slug"):
        if not meta.get(key):
            raise SystemExit(f"{path}: front matter needs '{key}'")
    meta["tags"] = [t.strip() for t in meta.get("tags", "").split(",") if t.strip()]
    meta["exam"] = [t.strip() for t in meta.get("exam", "").split(",") if t.strip()]
    meta["body_md"] = m.group(2)
    return meta


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def faq_from(md_text):
    """Return [(question, answer_text)] from a '## Frequently asked questions' section."""
    m = re.search(r"^## Frequently asked questions\s*$(.*?)(?=^## |\Z)", md_text, re.M | re.S)
    if not m:
        return []
    out = []
    for q, a in re.findall(r"^### (.+?)\s*$(.*?)(?=^### |\Z)", m.group(1), re.M | re.S):
        plain = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", a)
        plain = re.sub(r"[*_`]", "", plain).strip()
        if plain:
            out.append((q.strip(), " ".join(plain.split())))
    return out


def utm(url, slug, medium="blog"):
    sep = "&" if "?" in url else "?"
    return f"{url}{sep}utm_source=axomrank_blog&utm_medium={medium}&utm_campaign={quote(slug)}"


def page(site, *, title, description, canonical, body, jsonld=(), og_type="website", lang=None):
    ld = "\n".join(
        f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in jsonld
    )
    base = site["base_url"]
    app = site["app_url"]
    return f"""<!doctype html>
<html lang="{lang or site['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="{html.escape(site['title'])}">
<meta property="og:image" content="{site['publisher_logo']}">
<meta name="twitter:card" content="summary">
<meta name="theme-color" content="#80151A">
<link rel="icon" href="{site['publisher_logo']}">
<link rel="alternate" type="application/rss+xml" title="{html.escape(site['title'])}" href="{base}/rss.xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;600;700&family=Noto+Sans+Bengali:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{base}/assets/style.css">
{ld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="masthead">
  <div class="wrap bar">
    <a class="brand" href="{base}/"><span class="mark" aria-hidden="true">A</span><span>AxomRank <em>Blog</em></span></a>
    <nav aria-label="Main">
      <a href="{base}/adre/">ADRE</a>
      <a href="{base}/apsc-cce/">APSC</a>
      <a href="{base}/exams/">All exams</a>
      <a href="{base}/question-papers/">Question papers</a>
      <a href="{base}/questions/">Topic-wise MCQs</a>
      <a class="cta-sm" href="{utm(app, 'nav', 'nav')}">Open the free app</a>
    </nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="foot">
  <div class="wrap">
    <p><strong>AxomRank</strong> · free, bilingual (English and Assamese) lessons and previous-year questions for ADRE, APSC CCE, Assam TET and Assam Police.</p>
    <p><a href="{base}/exams/">Exams</a> · <a href="{base}/syllabus/adre/">ADRE syllabus</a> · <a href="{base}/syllabus/apsc-cce/">APSC syllabus</a> · <a href="{base}/question-papers/">Previous year papers</a> · <a href="{base}/questions/">Questions by topic</a> · <a href="{base}/topics/assam-history/">Assam history</a></p>
    <p><a href="{utm(app, 'footer', 'footer')}">AxomRank app</a> · <a href="https://github.com/axomrank/assam-exam-pyq">Open PYQ dataset</a> · <a href="{base}/rss.xml">RSS</a> · <a href="{base}/about/">About and corrections</a></p>
  </div>
</footer>
</body>
</html>
"""


def card(site, p):
    exams = " ".join(f'<span class="chip">{html.escape(e)}</span>' for e in p["exam"])
    return f"""<article class="card">
  <p class="meta">{exams}<time datetime="{p['date']}">{fmt_date(p['date'])}</time></p>
  <h2><a href="{site['base_url']}/{p['slug']}/">{html.escape(p['title'])}</a></h2>
  <p>{html.escape(p['description'])}</p>
</article>"""


def fmt_date(d):
    return dt.date.fromisoformat(d).strftime("%-d %B %Y")


def build(base_url=None, pyq_dir=None):
    site = json.loads((ROOT / "site.json").read_text())
    if base_url:
        site["base_url"] = base_url.rstrip("/")
    base = site["base_url"]

    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "assets").mkdir(parents=True)
    shutil.copytree(ROOT / "assets", OUT / "assets", dirs_exist_ok=True)

    posts = [parse(p) for p in sorted((ROOT / "posts").glob("*.md"))]
    posts = [p for p in posts if p.get("draft", "false").lower() != "true"]
    posts.sort(key=lambda p: p["date"], reverse=True)
    slugs = [p["slug"] for p in posts]
    if len(slugs) != len(set(slugs)):
        raise SystemExit("duplicate slug")

    md = markdown.Markdown(extensions=["tables", "toc", "attr_list", "sane_lists"],
                           extension_configs={"toc": {"permalink": False}})
    urls = [(f"{base}/", posts[0]["date"] if posts else None)]
    topics = {}

    for p in posts:
        md.reset()
        body_html = md.convert(p["body_md"].replace("{{app}}", site["app_url"]).replace("{{base}}", base))
        # Tag outbound links to the app with UTM parameters so blog-driven sign-ups are measurable.
        body_html = re.sub(
            r'href="(' + re.escape(site["app_url"]) + r'[^"]*)"',
            lambda m: f'href="{html.escape(utm(html.unescape(m.group(1)), p["slug"]))}"',
            body_html,
        )
        canonical = f"{base}/{p['slug']}/"
        updated = p.get("updated") or p["date"]
        cta_url = utm(site["app_url"] + p.get("cta", "/"), p["slug"], "cta")
        cta_text = p.get("cta_text", "Practise free on AxomRank")
        chips = " ".join(
            f'<a class="chip" href="{base}/topics/{slugify(t)}/">{html.escape(t)}</a>' for t in p["exam"] + p["tags"]
        )
        toc = md.toc if md.toc.count("<li>") >= 3 else ""
        body = f"""<article class="post wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="{base}/">Blog</a> › {' › '.join(f'<a href="{base}/topics/{slugify(e)}/">{html.escape(e)}</a>' for e in p['exam'][:1])}</nav>
  <h1>{html.escape(p['title'])}</h1>
  <p class="dek">{html.escape(p['description'])}</p>
  <p class="meta">By {html.escape(site['author'])} · <time datetime="{p['date']}">{fmt_date(p['date'])}</time>{' · updated ' + fmt_date(updated) if updated != p['date'] else ''}</p>
  <p class="chips">{chips}</p>
  {f'<details class="toc"><summary>On this page</summary>{toc}</details>' if toc else ''}
  <div class="prose">{body_html}</div>
  <aside class="cta">
    <p><strong>Practise this for free.</strong> AxomRank has bilingual lessons, spaced review and previous-year questions that work offline on modest phones. No login needed to start.</p>
    <a class="btn" href="{cta_url}">{html.escape(cta_text)}</a>
  </aside>
</article>"""
        jsonld = [
            {
                "@context": "https://schema.org",
                "@type": "Article",
                "headline": p["title"],
                "description": p["description"],
                "datePublished": p["date"],
                "dateModified": updated,
                "inLanguage": site["lang"],
                "mainEntityOfPage": canonical,
                "author": {"@type": "Organization", "name": site["author"], "url": site["app_url"]},
                "publisher": {"@type": "Organization", "name": "AxomRank",
                              "logo": {"@type": "ImageObject", "url": site["publisher_logo"]}},
                "about": p["exam"] + p["tags"],
            },
            {
                "@context": "https://schema.org",
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Blog", "item": f"{base}/"},
                    {"@type": "ListItem", "position": 2, "name": p["title"], "item": canonical},
                ],
            },
        ]
        faq = faq_from(p["body_md"])
        if faq:
            jsonld.append({
                "@context": "https://schema.org",
                "@type": "FAQPage",
                "mainEntity": [{"@type": "Question", "name": q,
                                "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq],
            })
        d = OUT / p["slug"]
        d.mkdir(parents=True)
        (d / "index.html").write_text(page(site, title=f"{p['title']} | AxomRank", description=p["description"],
                                           canonical=canonical, body=body, jsonld=jsonld, og_type="article"),
                                      encoding="utf-8")
        urls.append((canonical, updated))
        for t in p["exam"] + p["tags"]:
            topics.setdefault(t, []).append(p)

    # Previous-year question pages from the assam-exam-pyq dataset
    pyq_dir = pyq_dir or os.environ.get("PYQ_DIR") or (ROOT.parent / "assam-exam-pyq")
    papers = pyq_pages.build(site, page, OUT, urls, utm, pyq_dir)
    exam_pages.build(site, page, OUT, urls, utm, papers, posts, md)
    pyq_strip = ""
    if papers:
        total = sum(len(x["qs"]) for x in papers)
        pyq_strip = f'''<section class="wrap strip"><div><h2>{len(papers)} real question papers, {total:,} questions, all with answers</h2>
<p>ADRE, APSC CCE Prelims, Assam Police, Assam TET and DME papers as text instead of blurry PDFs.</p></div>
<p><a class="btn" href="{base}/question-papers/">Browse question papers</a> <a class="btn ghost" href="{base}/questions/">Questions by topic</a></p></section>'''

    # Home
    home = f"""<section class="hero wrap">
  <h1>{html.escape(site['tagline'])}</h1>
  <p class="dek">Exam analysis built from real previous-year papers, Assam history checked against named sources, and study plans that do not need a coaching fee. Every post links to free practice in the AxomRank app.</p>
  <a class="btn" href="{utm(site['app_url'], 'home_hero', 'hero')}">Start practising free</a>
</section>
{pyq_strip}
<section class="wrap list">{''.join(card(site, p) for p in posts)}</section>"""
    (OUT / "index.html").write_text(page(site, title=f"{site['title']}: Assam govt exam preparation (ADRE, APSC, TET)",
                                         description="Free, source-checked guides for ADRE, APSC CCE, Assam TET and Assam Police: previous-year question analysis, Assam history and study plans.",
                                         canonical=f"{base}/", body=home,
                                         jsonld=[{"@context": "https://schema.org", "@type": "WebSite",
                                                  "name": site["title"], "url": f"{base}/"}]),
                                    encoding="utf-8")

    # Topic pages (always create the nav targets)
    for t in ["ADRE", "APSC", "Assam History"]:
        topics.setdefault(t, [])
    for t, ps in topics.items():
        d = OUT / "topics" / slugify(t)
        d.mkdir(parents=True, exist_ok=True)
        inner = "".join(card(site, p) for p in ps) or "<p>Posts on this topic are coming soon.</p>"
        body = f'<section class="wrap list"><h1>{html.escape(t)}</h1>{inner}</section>'
        (d / "index.html").write_text(page(site, title=f"{t} preparation articles | AxomRank Blog",
                                           description=f"AxomRank articles on {t}: previous-year question analysis, notes and free practice.",
                                           canonical=f"{base}/topics/{slugify(t)}/", body=body), encoding="utf-8")
        urls.append((f"{base}/topics/{slugify(t)}/", None))

    # About / corrections
    about = (ROOT / "about.md").read_text(encoding="utf-8")
    md.reset()
    d = OUT / "about"
    d.mkdir()
    (d / "index.html").write_text(page(site, title="About AxomRank and corrections policy",
                                       description="Who runs AxomRank, how facts are checked, and how to report a correction.",
                                       canonical=f"{base}/about/",
                                       body=f'<article class="post wrap"><div class="prose">{md.convert(about)}</div></article>'),
                                  encoding="utf-8")
    urls.append((f"{base}/about/", None))

    # Sitemap, robots, RSS, 404
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, lm in urls:
        sm.append(f"<url><loc>{u}</loc>" + (f"<lastmod>{lm}</lastmod>" if lm else "") + "</url>")
    sm.append("</urlset>")
    (OUT / "sitemap.xml").write_text("\n".join(sm), encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\n", encoding="utf-8")
    items = "".join(
        f"<item><title>{html.escape(p['title'])}</title><link>{base}/{p['slug']}/</link>"
        f"<guid>{base}/{p['slug']}/</guid><pubDate>{dt.datetime.fromisoformat(p['date']).strftime('%a, %d %b %Y 00:00:00 +0530')}</pubDate>"
        f"<description>{html.escape(p['description'])}</description></item>" for p in posts)
    (OUT / "rss.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>{html.escape(site["title"])}</title>'
        f"<link>{base}/</link><description>{html.escape(site['tagline'])}</description>{items}</channel></rss>",
        encoding="utf-8")
    (OUT / "404.html").write_text(page(site, title="Page not found | AxomRank Blog", description="Page not found.",
                                       canonical=f"{base}/404.html",
                                       body=f'<section class="wrap hero"><h1>Page not found</h1><p><a href="{base}/">Back to the blog</a></p></section>'),
                                  encoding="utf-8")
    (OUT / ".nojekyll").write_text("")
    print(f"built {len(posts)} posts, {len(topics)} topic pages -> {OUT}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url")
    ap.add_argument("--pyq-dir", help="checkout of axomrank/assam-exam-pyq (default ../assam-exam-pyq or $PYQ_DIR)")
    a = ap.parse_args()
    build(a.base_url, a.pyq_dir)

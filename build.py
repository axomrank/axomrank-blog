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

import district_pages
import exam_pages
import post_images
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
            if k.strip() in meta:
                raise SystemExit(f"{path}: duplicate front-matter field '{k.strip()}'")
            meta[k.strip()] = v.strip()
    for key in ("title", "description", "date", "slug"):
        if not meta.get(key):
            raise SystemExit(f"{path}: front matter needs '{key}'")
    for field in ("date", "updated"):
        if field in meta:
            try:
                date = dt.date.fromisoformat(meta[field])
                if date.isoformat() != meta[field]:
                    raise ValueError
            except ValueError:
                raise SystemExit(f"{path}: '{field}' must be a date in YYYY-MM-DD format") from None
    if meta.get("updated", meta["date"]) < meta["date"]:
        raise SystemExit(f"{path}: updated date precedes publication date")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", meta["slug"]):
        raise SystemExit(f"{path}: slug must use lowercase letters, digits and hyphens")
    if not 120 <= len(meta["description"]) <= 160:
        raise SystemExit(f"{path}: description must be 120–160 characters")
    if meta.get("lang", "en-IN") not in {"en", "en-IN", "as", "as-IN"}:
        raise SystemExit(f"{path}: unsupported post language")
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


def page(site, *, title, description, canonical, body, jsonld=(), og_type="website", lang=None,
         image=None, alternates=()):
    ld = "\n".join(
        f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in jsonld
    )
    base = site["base_url"]
    app = site["app_url"]
    nav_items = [("exams", "Exams"), ("question-papers", "Papers")] if site["has_papers"] else []
    nav_items.append(("districts", "Districts"))
    nav_links = []
    for path, label in nav_items:
        url = f"{base}/{path}/"
        current = ' aria-current="page"' if canonical == url else ""
        nav_links.append(f'<a href="{url}"{current}>{label}</a>')
    footer_links = f'<a href="{base}/questions/">Questions by topic</a>' if site["has_papers"] else ""
    hreflang = "\n".join(f'<link rel="alternate" hreflang="{language}" href="{url}">'
                        for language, url in alternates)
    image_size = (f'<meta property="og:image:width" content="{post_images.WIDTH}">\n'
                  f'<meta property="og:image:height" content="{post_images.HEIGHT}">') if image else ""
    body = re.sub(
        r"(<table\b[^>]*>.*?</table>)",
        r'<div class="table-scroll" role="region" aria-label="Scrollable table" tabindex="0">\1</div>',
        body,
        flags=re.S,
    )
    return f"""<!doctype html>
<html lang="{lang or site['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="canonical" href="{canonical}">
{hreflang}
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="{html.escape(site['title'])}">
<meta property="og:image" content="{image or site['publisher_logo']}">
{image_size}
<meta name="twitter:card" content="{'summary_large_image' if image else 'summary'}">
<meta name="theme-color" content="#fcfaf7" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#191615" media="(prefers-color-scheme: dark)">
<link rel="icon" href="{site['publisher_logo']}">
<link rel="alternate" type="application/rss+xml" title="{html.escape(site['title'])}" href="{base}/rss.xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Bengali:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{base}/assets/style.css">
{ld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="masthead">
  <div class="wrap bar">
    <a class="brand" href="{base}/">AxomRank <span>Blog</span></a>
    <nav class="main-nav" aria-label="Main">
      {''.join(nav_links)}
      <a class="app-link" href="{utm(app, 'nav', 'nav')}">Free app</a>
    </nav>
  </div>
</header>
<main id="main" tabindex="-1">
{body}
</main>
<footer class="foot">
  <div class="wrap">
    <p>Free exam preparation in English and Assamese.</p>
    <nav aria-label="Footer">
      {footer_links}
      <a href="{base}/topics/assam-history/">Assam history</a>
      <a href="{base}/about/">About and corrections</a>
      <a href="{utm(app, 'footer', 'footer')}">AxomRank app</a>
      <a href="https://github.com/axomrank/assam-exam-pyq">Open PYQ dataset</a>
      <a href="{base}/rss.xml">RSS</a>
    </nav>
  </div>
</footer>
</body>
</html>
"""


def card(site, p, *, heading="h3"):
    exams = html.escape(" · ".join(p["exam"]))
    exam_meta = f"<span>{exams}</span><span aria-hidden=\"true\">·</span>" if exams else ""
    return f"""<article class="card">
  <p class="meta">{exam_meta}<time datetime="{p['date']}">{fmt_date(p['date'])}</time></p>
  <{heading}><a href="{site['base_url']}/{p['path']}/" lang="{p.get('lang', site['lang'])}">{html.escape(p['title'])}</a></{heading}>
  <p>{html.escape(p['description'])}</p>
</article>"""


def fmt_date(d):
    return dt.date.fromisoformat(d).strftime("%-d %B %Y")


def build(base_url=None, pyq_dir=None):
    site = json.loads((ROOT / "site.json").read_text())
    if base_url:
        site["base_url"] = base_url.rstrip("/")
    base = site["base_url"]
    pyq_dir = pyq_dir or os.environ.get("PYQ_DIR") or (ROOT.parent / "assam-exam-pyq")
    pyq_data = pyq_pages.load(pyq_dir)
    site["has_papers"] = bool(pyq_data and pyq_data[1])

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
    for p in posts:
        section = "as/" if p.get("lang", "").startswith("as") else ""
        p["path"] = section + p["slug"]
    posts_by_slug = {p["slug"]: p for p in posts}
    translations = {}
    for p in posts:
        if source_slug := p.get("translation_of"):
            source = posts_by_slug.get(source_slug)
            if (not source or source.get("lang", "en-IN").startswith("as")
                    or not p.get("lang", "").startswith("as") or source_slug in translations):
                raise SystemExit(f"{p['slug']}: expected one Assamese translation of an English post")
            alternates = (
                (source.get("lang", "en-IN"), f"{base}/{source_slug}/"),
                (p["lang"], f"{base}/{p['path']}/"),
            )
            translations[source_slug] = translations[p["slug"]] = alternates

    images = OUT / "assets" / "post-images"
    images.mkdir()

    md = markdown.Markdown(extensions=["tables", "toc", "attr_list", "sane_lists"],
                           extension_configs={"toc": {"permalink": False}})
    urls = [(f"{base}/", posts[0]["date"] if posts else None)]
    topics = {}

    for p in posts:
        lang = p.get("lang", site["lang"])
        image_path = images / f"{p['slug']}.jpg"
        post_images.render(p, image_path)
        md.reset()
        body_html = md.convert(p["body_md"].replace("{{app}}", site["app_url"]).replace("{{base}}", base))
        # Tag outbound links to the app with UTM parameters so blog-driven sign-ups are measurable.
        body_html = re.sub(
            r'href="(' + re.escape(site["app_url"]) + r'[^"]*)"',
            lambda m: f'href="{html.escape(utm(html.unescape(m.group(1)), p["slug"]))}"',
            body_html,
        )
        canonical = f"{base}/{p['path']}/"
        updated = p.get("updated") or p["date"]
        cta_url = utm(site["app_url"] + p.get("cta", "/"), p["slug"], "cta")
        cta_text = p.get("cta_text", "Practise free on AxomRank")
        tags = "".join(
            f'<li><a href="{base}/topics/{slugify(t)}/">{html.escape(t)}</a></li>'
            for t in dict.fromkeys(p["exam"] + p["tags"])
        )
        primary_topic = next(iter(p["exam"]), None)
        topic_crumb = (f' <span aria-hidden="true">/</span> <a href="{base}/topics/{slugify(primary_topic)}/">'
                       f'{html.escape(primary_topic)}</a>') if primary_topic else ""
        toc = md.toc if md.toc.count("<li>") >= 3 else ""
        body = f"""<article class="post wrap">
  <header class="post-header">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="{base}/">Blog</a>{topic_crumb}</nav>
    <h1>{html.escape(p['title'])}</h1>
    <p class="dek">{html.escape(p['description'])}</p>
    <p class="meta">By {html.escape(site['author'])} · <time datetime="{p['date']}">{fmt_date(p['date'])}</time>{' · updated ' + fmt_date(updated) if updated != p['date'] else ''}</p>
  </header>
  {f'<details class="toc"><summary>On this page</summary>{toc}</details>' if toc else ''}
  <div class="prose">{body_html}</div>
  <aside class="cta">
    <p><strong>Practise this for free.</strong> AxomRank has bilingual lessons, spaced review and previous-year questions that work offline on modest phones. No login needed to start.</p>
    <a class="btn" href="{cta_url}">{html.escape(cta_text)}</a>
  </aside>
  {f'<nav class="post-topics" aria-label="Related topics"><ul>{tags}</ul></nav>' if tags else ''}
</article>"""
        jsonld = [
            {
                "@context": "https://schema.org",
                "@type": "Article",
                "headline": p["title"],
                "description": p["description"],
                "datePublished": p["date"],
                "dateModified": updated,
                "inLanguage": lang,
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
        d = OUT / p["path"]
        d.mkdir(parents=True)
        (d / "index.html").write_text(page(site, title=f"{p['title']} | AxomRank", description=p["description"],
                                           canonical=canonical, body=body, jsonld=jsonld, og_type="article", lang=lang,
                                           image=f"{base}/{image_path.relative_to(OUT).as_posix()}",
                                           alternates=translations.get(p["slug"], ())),
                                      encoding="utf-8")
        urls.append((canonical, updated))
        for t in p["exam"] + p["tags"]:
            topics.setdefault(t, []).append(p)

    # Previous-year question pages from the assam-exam-pyq dataset
    if site["has_papers"]:
        papers, published_topics = pyq_pages.build(site, page, OUT, urls, utm, pyq_data)
    else:
        print(f"No PYQ papers found at {pyq_dir}: skipping question-paper pages")
        papers, published_topics = [], set()
    exam_pages.build(site, page, OUT, urls, utm, papers, posts, md, published_topics)
    district_pages.build(site, page, OUT, urls, utm, papers, published_topics)

    resources = []
    if papers:
        total = sum(len(x["qs"]) for x in papers)
        resources.extend([
            ("exams", "Exams and syllabi", "Exam patterns, syllabus topics and past papers"),
            ("question-papers", "Previous-year papers", f"{len(papers)} papers and {total:,} questions with answers"),
            ("questions", "Questions by topic", "Practise Assam GK, maths, reasoning and more"),
        ])
    resources.append(("districts", "Districts of Assam", "Population, area and literacy from official sources"))
    resource_links = "".join(
        f'<li><a href="{base}/{path}/"><strong>{label}</strong><span>{detail}</span></a></li>'
        for path, label, detail in resources
    )

    # Home
    home = f"""<div class="wrap home-intro">
  <section class="hero">
    <h1>Prepare for Assam government exams</h1>
    <p class="dek">Free study guides, real previous-year questions and source-checked Assam history for ADRE, APSC CCE, Assam TET and Assam Police.</p>
    <a class="btn" href="{utm(site['app_url'], 'home_hero', 'hero')}">Practise in the free app</a>
  </section>
  <nav class="resources" aria-labelledby="study-resources">
    <h2 id="study-resources">Study resources</h2>
    <ul>{resource_links}</ul>
  </nav>
</div>
<section class="wrap home-guides" aria-labelledby="latest-guides">
  <h2 id="latest-guides">Latest guides</h2>
  <div class="list">{''.join(card(site, p) for p in posts)}</div>
</section>
"""
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
        inner = "".join(card(site, p, heading="h2") for p in ps) or "<p>Posts on this topic are coming soon.</p>"
        body = f'<header class="wrap hero"><h1>{html.escape(t)}</h1></header><div class="wrap list">{inner}</div>'
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
        f"<item><title>{html.escape(p['title'])}</title><link>{base}/{p['path']}/</link>"
        f"<guid>{base}/{p['path']}/</guid><pubDate>{dt.datetime.fromisoformat(p['date']).strftime('%a, %d %b %Y 00:00:00 +0530')}</pubDate>"
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

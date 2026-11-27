"""Render the downloadable paper archive inside editorial guides."""

from collections import defaultdict
from html import escape
import json


def load(path):
    archive = json.loads(path.read_text(encoding="utf-8"))
    base = archive["release"].replace("/releases/tag/", "/releases/download/")
    groups = defaultdict(list)
    practice = {}

    for paper in archive["papers"]:
        for asset in (paper, paper.get("key")):
            if asset:
                asset["url"] = f"{base}/{asset['asset']}"
        groups[paper["group"]].append(paper)
        if slug := paper.get("practice"):
            practice[slug] = paper

    return groups, practice


def table(papers, base, practice_slugs):
    by_exam = defaultdict(list)
    for paper in papers:
        by_exam[paper["exam"]].append(paper)

    sections = []
    for exam, entries in by_exam.items():
        rows = []
        for paper in entries:
            title = escape(paper["title"])
            cycle = escape(paper["cycle"])
            name = escape(f"{paper['cycle']} {exam} {paper['title']}")
            size = f"{paper['bytes'] / 1_000_000:.1f} MB" if paper["bytes"] >= 1_000_000 else f"{round(paper['bytes'] / 1000)} KB"
            links = [f'<a href="{escape(paper["url"])}" aria-label="Download {name} PDF">PDF · {size}</a>']
            if key := paper.get("key"):
                links.append(f'<a href="{escape(key["url"])}" aria-label="Download answer key for {name}">Answer key</a>')
            if paper.get("practice") in practice_slugs:
                links.append(f'<a href="{base}/question-papers/{paper["practice"]}/" aria-label="Practise {name} online">Practise online</a>')
            note = f'<br><small>{escape(paper["note"])}</small>' if "note" in paper else ""
            rows.append(f'<tr><th scope="row">{cycle} · {title}{note}</th><td class="download-links">{"<br>".join(links)}</td></tr>')
        heading = f'### {exam}\n\n' if len(by_exam) > 1 else ''
        sections.append(
            f'{heading}<table><thead><tr><th scope="col">Paper</th><th scope="col">Downloads</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table>'
        )
    return "\n\n".join(sections)

# AxomRank Blog: Assam government exam guides built from real papers

> AxomRank blog: free, source-checked guides for ADRE, APSC CCE, Assam TET and Assam Police, built from real previous-year papers.

**[Live site](https://axomrank.github.io/axomrank-blog/)** · [Part of AxomRank](https://github.com/axomrank)

## At a glance

- **Posts** in Markdown with front matter (`posts/`), built by a small Python script (`build.py`) into static HTML
- **SEO built in:** canonical URLs, Open Graph, JSON-LD (Article, BreadcrumbList, FAQPage), sitemap, RSS and topic pages
- **Measurable funnel:** every link into the app gets UTM tags automatically
- **Deploys** through GitHub Actions on every push to `main`
- **Plans:** the [sales and marketing plan](docs/MARKETING-PLAN.md) and the [account organisation](docs/ACCOUNT-ORGANISATION.md)

## Overview

The marketing and SEO blog for [AxomRank](https://axomrank.pages.dev), which offers free, bilingual preparation for Assam government exams (ADRE, APSC CCE, Assam TET, Assam Police).

## Write a post

1. Add `posts/YYYY-MM-DD-short-name.md` with front matter. Copy any existing post. Required fields: `title`, `description` (120–160 characters), `date`, `slug`. Optional fields: `exam`, `tags`, `cta`, `cta_text`, `updated`, `draft: true`.
2. Use `{{app}}` for the app URL and `{{base}}` for the blog URL in links. Links to the app get UTM tags automatically.
3. End with a `## Frequently asked questions` section using `### Question` headings. It becomes FAQ structured data.
4. Add a **Sources** section. Every number must come from the real papers or a named source.
5. Push to `main`. GitHub Actions (`.github/workflows/pages.yml`) builds and deploys the site in about a minute. `./deploy.sh` is a manual fallback.

## Build locally

```bash
pip install -r requirements.txt
python build.py --base-url http://localhost:8765
python -m http.server 8765 -d _site
```

The build writes post pages, topic pages, `sitemap.xml`, `rss.xml`, `robots.txt` and JSON-LD (Article, BreadcrumbList, FAQPage).

## Plans

- [Sales and marketing plan](docs/MARKETING-PLAN.md): competitors, funnel, keyword clusters, a 12-week calendar and channels
- [GitHub account organisation](docs/ACCOUNT-ORGANISATION.md): what to keep, archive, move and delete
- `scripts/pyq_stats.py` regenerates the PYQ statistics used in the analysis posts

## Roadmap: future improvements

- [ ] Paper pages: one indexable HTML page per previous-year paper, with answers (generated from assam-exam-pyq)
- [ ] Assamese-language posts, after human editorial review
- [ ] Custom domain `blog.axomrank.org` (set the `BASE_URL` repository variable)
- [ ] Open Graph images generated per post from the brand templates
- [ ] Internal-link checker and front-matter linter in CI
- [ ] Search Console and OpenSEO connected for keyword tracking

## For AI agents and contributors

Read [AGENTS.md](AGENTS.md). Every number in a post must come from the real papers or a named source.

Commit as the `axomrank` account. Keep changes small and reviewable, and run the repository's checks before pushing.

## Part of AxomRank

[AxomRank](https://axomrank.pages.dev) offers free, bilingual preparation for Assam government exams. Related repositories:

- **Learn:** [axomrank.github.io](https://github.com/axomrank/axomrank.github.io) (the AxomRank learning app), [floor-test-simulator](https://github.com/axomrank/floor-test-simulator) (parliamentary majority simulator)
- **Explore Assam history:** [ahom-kingdom-history](https://github.com/axomrank/ahom-kingdom-history) (illustrated Ahom kingdom website and 41 reign lessons), [assam-history-map](https://github.com/axomrank/assam-history-map) (year-by-year historical map), [assam-history-characters](https://github.com/axomrank/assam-history-characters) (character sheets for Assam's history), [assam-visual-archive](https://github.com/axomrank/assam-visual-archive) (gallery of Assam scenes and photographs), [assam-heritage-ai-art](https://github.com/axomrank/assam-heritage-ai-art) (AI art gallery of Assamese heritage)
- **Open data:** [assam-exam-pyq](https://github.com/axomrank/assam-exam-pyq) (2,398 previous-year questions with answers), [assam-exam-syllabus](https://github.com/axomrank/assam-exam-syllabus) (syllabi for 12 recruitment boards), [assam-maps](https://github.com/axomrank/assam-maps) (map portal and GIS layers), [assam-history-sources](https://github.com/axomrank/assam-history-sources) (Kamarupa inscriptions and primary sources)
- **Publishing and brand:** [assam-history-books](https://github.com/axomrank/assam-history-books) (13-book history of Assam), [axomrank-brand-assets](https://github.com/axomrank/axomrank-brand-assets) (brand kit and social media library)

## License and contact

No license file yet, so all rights are reserved by default.

Corrections and questions: open an issue in this repository. AxomRank is run by Angsuman Das (sole proprietor).

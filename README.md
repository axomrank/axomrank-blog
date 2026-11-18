# AxomRank Blog

The marketing and SEO blog for [AxomRank](https://axomrank.pages.dev), which offers free, bilingual preparation for Assam government exams (ADRE, APSC CCE, Assam TET, Assam Police).

**Live:** https://axomrank.github.io/axomrank-blog/ (planned: blog.axomrank.org)

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
- [Profile README draft](docs/PROFILE-README.md)
- `scripts/pyq_stats.py` regenerates the PYQ statistics used in the analysis posts

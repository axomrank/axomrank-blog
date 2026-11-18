# Working on axomrank-blog

Marketing and SEO blog for AxomRank. Part of AxomRank: see README.md for the overview and roadmap.

## Layout

- `posts/*.md`: posts with front matter (see README)
- `build.py`: static site builder
- `assets/style.css`: brand-kit styling
- `docs/`: marketing plan and account organisation

## Commands

- `pip install -r requirements.txt && python build.py --base-url http://localhost:8765`
- Push to `main` to deploy through GitHub Actions

## Rules

- Every number must come from the real papers (assam-exam-pyq) or a named source
- End each post with an FAQ section and a Sources section
- Do not invent exam dates, vacancies or results. Use official notices only
- Assamese posts need a human editorial review before publishing
- Commit as the `axomrank` account, in small reviewable commits.

# Organising the `axomrank` GitHub account

Last updated 18 November 2026. The account holds **16 repositories**: 15 public and 1 private (`axomrank-app`). Every name says what the repo contains, every repo has a professional README with a roadmap and an AGENTS.md for AI agents, and each README cross-links its siblings.

## Repositories

| Group | Repo | Live site |
|---|---|---|
| Learn | `axomrank-app` (**private**: the app, AxomRank's core product) | axomrank.pages.dev (Cloudflare Pages, direct upload) |
| Home | `axomrank.github.io` (public home page; the name is required for the user site) | axomrank.github.io |
| Learn | `floor-test-simulator` | axomrank.github.io/floor-test-simulator |
| History | `ahom-kingdom-history` (includes the Ahom Kings lessons in `lessons/`) | axomrank.github.io/ahom-kingdom-history, lessons at axomrank.github.io/ahom-kingdom-history/lessons and ahom-lessons.pages.dev |
| History | `assam-history-map` | axomrank.github.io/assam-history-map |
| History | `assam-history-characters` | axomrank.github.io/assam-history-characters |
| History | `assam-visual-archive` | axomrank.github.io/assam-visual-archive |
| History | `assam-heritage-ai-art` | axomrank.github.io/assam-heritage-ai-art |
| Data | `assam-exam-pyq` | none |
| Data | `assam-exam-syllabus` | none |
| Data | `assam-maps` | axomrank.github.io/assam-maps |
| Data | `assam-history-sources` | none |
| Publishing | `axomrank-blog` | axomrank.github.io/axomrank-blog |
| Publishing | `assam-history-books` | none |
| Publishing | `axomrank-brand-assets` | none |
| Profile | `axomrank` (profile README) | github.com/axomrank |

## Naming convention

Names are lowercase and kebab-case. They start with the subject (`assam-…`, `ahom-…`) or the brand (`axomrank-…`), then say what the repo contains. Keywords in the name also appear in GitHub Pages URLs, which helps search.

## Renames (18 Nov 2026)

| Old | New |
|---|---|
| AHOM | ahom-kingdom-history |
| ahom-lessons | ahom-kings-lessons, then merged into ahom-kingdom-history/lessons |
| historymap | assam-history-map |
| Assam-History-Characters | assam-history-characters |
| assam | assam-visual-archive |
| map (merged with Assam_MAP_file) | assam-maps |
| PYQ | assam-exam-pyq |
| Study_Assam | assam-exam-syllabus |
| Primary-source | assam-history-sources |
| Social_Media_asset | axomrank-brand-assets |
| book | assam-history-books |
| assamese-ai-gallery | assam-heritage-ai-art |
| the-floor-test | floor-test-simulator |

GitHub redirects the old repository URLs. For the old GitHub Pages URLs, `axomrank.github.io/404.html` sends visitors to the new path, keeping the rest of the URL. Every canonical URL, sitemap and cross-link inside the repos was rewritten to the new names.

## Removed (18 Nov 2026)

- **Merged:** `Assam_MAP_file` → `assam-maps/data/admin-layers/`, and `ahom-kings-lessons` → `ahom-kingdom-history/lessons/`, both with their git history.
- **Deleted:** the legacy workspace (`Axomrank`), `History`, `Polity`, `Geography`, `axomrank-content`, `API-App`, `Axomrank_matt`, `bioinformatics`, `BLOG`, `Assam_Ethnomedicine`, `Flood-Relief`, `genone`, `bamboo-crafts`, `Portfolio_Maker`, `NE-Ethnomedicine`, `Teaching-schools`, three `gitzo-ps-*` repos, `axomrank-achievements`, and `Assam_MAP_file` and `ahom-kings-lessons` after their merges.
- Deleted repos can be restored for 90 days from GitHub Settings → Repositories → Deleted repositories. Local copies are in `_deleted-backup/` on the owner's machine.

## App made private (18 Nov 2026)

The app is AxomRank's main product and is not open source. Its full history (all 5 branches, 105 commits) was copied to the private repository `axomrank-app`. The public `axomrank.github.io` was then deleted and recreated with fresh history, holding only the home page and the redirect page, so no app code remains public. Cloudflare Pages (`axomrank` and `ahom-lessons` projects) uses direct upload rather than a Git connection, so `scripts/deploy_cloudflare.sh` keeps deploying from the private repository's folder. Note: the code was public until this date, so copies made earlier cannot be recalled.

## Still for the owner

- Pin `axomrank.github.io` (home page), `assam-exam-pyq`, `axomrank-blog`, `assam-history-map` and `ahom-kingdom-history` (profile → Customize your pins).
- Choose licenses: most repos have none, which means all rights are reserved.
- Rights review of the PDFs in `assam-history-sources`. Some are modern editions that may still be under copyright.
- Point DNS for axomrank.org and blog.axomrank.org.

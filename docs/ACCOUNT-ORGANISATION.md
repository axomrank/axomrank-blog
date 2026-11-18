# Organising the `axomrank` GitHub account

Reviewed 18 November 2026: 35 public repositories. The goal is that a student, journalist, coaching institute or partner who lands on github.com/axomrank immediately sees **one product, its open data, and its marketing assets**, and nothing that looks like spam or an unrelated project.

## Tiers

### 1. Product (live sites): keep, pin, add topics and homepage links
| Repo | Live URL | Notes |
|---|---|---|
| `axomrank.github.io` | axomrank.pages.dev | **The app.** Pin first |
| `ahom-lessons` | axomrank.github.io/ahom-lessons | Ahom course |
| `AHOM` | axomrank.github.io/AHOM | Ahom kingdom story site |
| `historymap` | axomrank.github.io/historymap | Assam Through Time |
| `Assam-History-Characters` | axomrank.github.io/Assam-History-Characters | Character sheets |
| `assam` | axomrank.github.io/assam | Visual archive |
| `map` | Pages not enabled | Assam map portal. Enable Pages |

### 2. Open data (link magnets): keep, pin `PYQ`
`PYQ`, `Study_Assam`, `Assam_MAP_file`, `Primary-source`

`Study_Assam/README.md` links use `file:///home/...` paths, which are broken on GitHub. Change them to relative links. `Primary-source` has no README, so add one.

### 3. Marketing: keep
`axomrank-blog` (new, pin), `Social_Media_asset`, `book`, `assamese-ai-gallery`

`axomrank-content` is an exact subset of `Social_Media_asset` (every file in it also exists there). **Archive it.**

### 4. Legacy prototypes: archive (read-only, still visible)
| Repo | Why |
|---|---|
| `Axomrank` | v1.0–3.0 workspace, superseded by `axomrank.github.io`. **It is also the profile README repo** (its name matches the account), so the profile currently shows the old workspace README. See below |
| `History`, `Polity`, `Geography` | Superseded by the app's courses. Their READMEs all say "Geography Platform", and `History` and `Polity` commit `node_modules` (6,600+ files) |
| `API-App`, `the-floor-test` | Small single tools. Keep public, unpinned |
| `Axomrank_matt` | Job radar. Its README points to `github.com/Angsumi/Axomrank_matt`. **Keep active** if the job radar will be developed (recommended, see the marketing plan); otherwise archive |

### 5. Not AxomRank: remove from this account
`bioinformatics`, `BLOG` (personal essays), `Flood-Relief`, `genone`, `bamboo-crafts`, `Portfolio_Maker`, `NE-Ethnomedicine`, `Assam_Ethnomedicine`, `Teaching-schools`

They are good work but dilute the brand. GitHub keeps redirects after a transfer, so old links keep working.

### 6. Delete
`gitzo-ps-1-1793602232`, `gitzo-ps-1-axomrank-1793602273`, `gitzo-ps-2-axomrank-1793602294`, `axomrank-achievements`

These are badge-farming repos. They have no content, and anyone checking the brand will read them as spam.

## Profile README

GitHub shows the README of the repo named like the account (`axomrank/axomrank`, case-insensitive) on the profile page. Today that is the legacy `Axomrank` workspace. The recommended fix:

1. Rename `Axomrank` → `axomrank-workspace-legacy` and archive it.
2. Create a new `axomrank/axomrank` repo containing [PROFILE-README.md](PROFILE-README.md).

## Cleanup log (18 Nov 2026)

| Action | Repos | State |
|---|---|---|
| Created | `axomrank-blog` (live on Pages), `axomrank` (profile README) | Done |
| Renamed and archived | `Axomrank` → `axomrank-workspace-legacy` | Done. Old URLs redirect |
| Archived (read-only) | `History`, `Polity`, `Geography`, `axomrank-content` | Done. `Geography`'s Pages site stays live |
| Archived (duplicates of the Angsumi copies) | `bioinformatics`, `BLOG`, `Assam_Ethnomedicine` | Done. Angsumi already had these names. `Assam_Ethnomedicine` is identical, and the other two are older snapshots |
| Deleted (owner's decision, instead of a transfer) | `Flood-Relief`, `genone`, `bamboo-crafts`, `Portfolio_Maker`, `NE-Ethnomedicine`, `Teaching-schools` | Done. They can be restored until mid-February 2027 from GitHub Settings → Repositories → Deleted repositories |
| Deleted | `gitzo-ps-1-1793602232`, `gitzo-ps-1-axomrank-1793602273`, `gitzo-ps-2-axomrank-1793602294`, `axomrank-achievements` | Done |
| Fixed | `Study_Assam` README `file:///` links → relative | Done. 12 links point to files that were never committed (for example, the CCE Mains syllabus) |
| Topics and homepage links | 13 product, data and marketing repos | Done |

## Still for the owner
- Pin `axomrank.github.io`, `PYQ`, `axomrank-blog`, `ahom-lessons`, `historymap` and `AHOM` (profile → Customize your pins).
- Point DNS for axomrank.org and blog.axomrank.org.

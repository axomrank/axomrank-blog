# AxomRank blog: SEO growth plan to out-rank Assam job and exam-prep sites

*Written 18 November 2026 and updated 26 November 2026. It builds on [MARKETING-PLAN.md](MARKETING-PLAN.md). The [OpenSEO keyword report](https://app.openseo.so/p/e2bc49dc-15ea-4cb2-9d9f-f5355eea1fc2/reports/8c60ba08-22bf-440d-a207-b8befb51911c) records the India search estimates and sampled mobile results behind the first articles.*

## 1. Who we are competing with

| Group | Sites | How they win | How AxomRank beats them |
|---|---|---|---|
| **A. Job-alert sites** | assamjobalerts.com, assamcareer.com, jobs.sentinelassam.com, nenow.in/assam-career, assam.sarkarijobs.com, freshersvoice, Adda247 job pages | Speed. They publish within hours of a notice, run Telegram/WhatsApp funnels, and have years of archive | **Evergreen exam hubs** (one URL per exam that is updated every cycle, so it keeps its authority) plus *preparation* tied to each notice. Copy-paste job blogs cannot offer the real papers and answers |
| **B. Exam-prep / GK sites** | assaminfo.com, assamboardexam.com, learnspotassam, spmiasacademy.com blog, Adda247, Testbook | Volume of GK lists and mock tests | **Real papers as text with answer sources** (done: 23 papers, 2,398 questions), topic pages built from real data, source-checked Assam history |

**Honest expectation:** a new site on `axomrank.github.io/axomrank-blog` will not reach the top of Google for "ADRE notification" against Sentinel or Adda247 in weeks. The route to #1 is:
1. **Months 1–3:** win the long tail (one paper, one topic, one exact question) where competitors only have PDFs.
2. **Months 3–6:** win the exam-hub queries ("ADRE syllabus", "APSC CCE previous year paper") as authority grows.
3. **Months 6+:** compete on notification and result queries, using the hubs plus speed.

## 2. Site structure (topic silos)

Each silo has a hub page that links down to its pages, and every page links back up. Search engines read this as topical authority.

| Silo | URL | Status | Targets (example queries) |
|---|---|---|---|
| Question papers | `/question-papers/` + 23 paper pages | **Built** | "adre 2024 grade 3 question paper with answer", "apsc prelims 2024 gs 2 question paper" |
| Questions by topic | `/questions/` + 50 topic pages | **Built** | "assam history mcq for adre", "number system questions adre" |
| Exam hubs | `/adre/`, `/apsc-cce/`, `/assam-police/`, `/assam-tet/`, `/dme/` | Built with links to issuing boards and dated notice coverage | "ADRE 2026", "APSC CCE 2026" |
| Syllabus and pattern | `/syllabus/<exam>/` | Built from available papers, with official APSC syllabus text | "adre grade 3 syllabus pdf", "apsc cce syllabus" |
| Jobs and notifications | `/jobs/` + one post per official notice | Built with an archived SLPRB notice and corrigendum | "assam govt job 2026", "<department> recruitment 2026" |
| Assam GK | `/assam-gk/` | Built with districts, map access, guides and a 50-question culture set | "ahom kings list", "national parks of assam", "rivers of assam" |
| Assam current affairs | `/current-affairs/<yyyy-mm>/` | Built with a November roundup through 26 November | "assam current affairs november 2026" |
| Study plans | posts | Partly | "adre preparation without coaching" |
| Assamese | `/as/…` with `hreflang` | Routing tested. First draft awaits human editorial review | Assamese-script queries |

## 3. Category A playbook: beating the job-alert sites

1. **One evergreen hub per exam.** Job blogs create a new URL every cycle ("ADRE 2.0 notification", "ADRE 3.0 notification"), so their authority is split. AxomRank keeps `/adre/` and adds a dated "Latest" box at the top. Old cycles stay on the same page as history.
2. **Notification posts only from official notices.** Each post covers the vacancy table, eligibility, fees, dates and the official PDF link, followed by "How to prepare", which links to the matching question papers and topic pages. Job blogs stop at the notice.
3. **Speed loop:** official site → post within hours → Telegram and WhatsApp channel → Google Search Console URL inspection plus IndexNow (Bing). Use a fixed post template so writing takes 20 minutes.
4. **Watch list of official sources:** apsc.nic.in, slprbassam.in, sebaonline.org (ADRE), dee.assam.gov.in (TET), dme.assam.gov.in, ghconline.gov.in, assam.gov.in. Optional later: a GitHub Action that checks these pages daily and opens an issue when something changes.
5. **Never invent** dates, vacancy counts or results (rule in AGENTS.md). Accuracy is the trust advantage over copy-paste blogs.

## 4. Category B playbook: beating the exam-prep and GK sites

1. **Programmatic PYQ pages (done).** The dataset gives 23 paper pages and 50 topic pages, about 75 pages of real, unique content. Next: individual question pages for the highest-demand facts, and a "most repeated facts" page per topic.
2. **GK posts built on the papers.** Each post leads with "asked N times in ADRE/APSC since 2022", then the facts, then the real questions. No other site can say this.
3. **Disagreements resolved.** Competitors contradict each other (for example, 39 vs 41 Ahom kings). Posts that explain the right answer with sources earn links.
4. **Interactive layer.** The free app is the practice engine, and every page links to it with UTM tags.

## 5. Technical SEO checklist

| Item | Status |
|---|---|
| Canonical URLs, Open Graph, sitemap, RSS, robots | Done |
| JSON-LD: Article, Breadcrumb, FAQPage, LearningResource, CollectionPage | Done |
| Fast static pages, readable on phones, dark mode | Done |
| **Custom domain** (`blog.axomrank.org`) | Awaiting Gandi LiveDNS access. The subdomain has no DNS record. |
| Google Search Console + Bing Webmaster Tools, submit the sitemap | Awaiting verification of the blog property. The GitHub Pages project URL is the live property. |
| IndexNow ping on deploy | Implemented. The workflow submits changed sitemap URLs after Pages deploys. |
| Exam hubs and jobs archive | Built |
| `hreflang` for Assamese pages | Implemented and tested with the draft in an isolated build |
| Open Graph images for articles | Generated during the build |
| Internal links and post front matter | Checked during the Pages workflow |

For the domain migration, verify domain ownership in GitHub Pages using its DNS challenge, configure the blog's Pages custom domain and add the `blog` CNAME to `axomrank.github.io` in Gandi. After HTTPS is active, set the `BASE_URL` repository variable to `https://blog.axomrank.org`, redeploy and check the redirect, canonical URLs, sitemap and IndexNow key. The apex site's migration requires coordination with the current site owner. [GitHub Pages custom domain guide](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)

## 6. Off-page: links and distribution

- **Telegram + WhatsApp channels:** a daily PYQ question that links to its topic page.
- **YouTube Shorts and Instagram:** "one Ahom king in 60 seconds", "ADRE question of the day".
- **Open dataset backlinks:** README links from `assam-exam-pyq`, `assam-exam-syllabus` and `assam-maps` (done in part). Submit the dataset to Kaggle and data.gov-style directories.
- **Coaching institutes and colleges:** offer free topic sheets in exchange for a link (the institute list is in `assam-coaching-institutes.md`).
- **Facebook aspirant groups and Quora/Reddit answers:** answer real questions and link the exact paper page.

## 7. 12-week publishing calendar (from 23 November 2026)

| Week | Build / page | Posts |
|---|---|---|
| 1 | ✅ PYQ paper and topic pages · custom domain · Search Console | ADRE hub page |
| 2 | Exam-hub template | APSC CCE hub · Assam Police hub |
| 3 | Syllabus silo from `assam-exam-syllabus` | ADRE Grade III syllabus · APSC CCE syllabus |
| 4 | Jobs silo + notification template | Assam TET hub · first official-notice post |
| 5 | | Battle of Saraighat (exam facts) · Assam districts list with map |
| 6 | IndexNow on deploy | National parks of Assam · Kamarupa dynasties |
| 7 | | Rivers of Assam · Sankardeva and the satras |
| 8 | "Most repeated facts" pages | ADRE maths: number system from real papers · Assam freedom fighters |
| 9 | | 50 Assam culture questions · Sixth Schedule councils |
| 10 | Assamese section (reviewed) | ADRE PYQ analysis in Assamese |
| 11 | | Assam current affairs (month) · Assam budget facts |
| 12 | Review in Search Console, refresh the top 10 pages | Year in review: Assam GK 2026 |

Notification posts are published whenever an official notice appears, on top of this calendar.

The evergreen articles were prepared in advance of their calendar slots. The Assam GK collection carries the Saraighat, parks, rivers, Kamarupa, Sankardeva, freedom fighters and Sixth Schedule guides. The exam collections carry the Assam Police, TET and ADRE maths articles. The question collection includes exact-question pages, a repeated Ahom facts guide and a 50-question Assam culture practice set.

The Assamese release still requires an editor. Budget coverage needs the official budget document for the relevant year. The year-in-review requires a complete year, and the planned performance review requires first-party data after verification. Publish subsequent notices and current-affairs entries when official updates are available.

## 8. Measures (monthly)

- Search Console: impressions, clicks, average position for `question paper`, `syllabus` and `<exam>` queries.
- Pages indexed out of pages in the sitemap.
- App sessions with `utm_source=axomrank_blog`, and lesson starts per page.
- Telegram/WhatsApp subscribers.
- Referring domains (OpenSEO, once connected).

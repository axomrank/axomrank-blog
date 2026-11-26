# AxomRank sales and marketing plan

*Written 18 November 2026 from a review of the GitHub account and competitors. The [26 November OpenSEO report](https://app.openseo.so/p/e2bc49dc-15ea-4cb2-9d9f-f5355eea1fc2/reports/8c60ba08-22bf-440d-a207-b8befb51911c) adds India search estimates and mobile result samples for the first content batch.*

## 1. What AxomRank has today

| Asset | Repo | Status | Marketing value |
|---|---|---|---|
| Main learning app (PWA, offline, English + Assamese) | `axomrank-app` (private) → axomrank.pages.dev | Live | **The product.** 93 Assam history lessons, 60 polity, 32 Indian history, 16 maths, 23 reasoning, 16 geography |
| Ahom kings course (41 reigns) | `ahom-kingdom-history/lessons` | Live | Strong hook for the "Ahom kings" searches |
| Ahom kingdom story site | `ahom-kingdom-history` | Live | Linkable reference site |
| Assam Through Time (year-by-year map) | `assam-history-map` | Live | Shareable, linkable |
| Assam history character sheets | `assam-history-characters` | Live | Social content source |
| Assam visual archive | `assam-visual-archive` | Live | Image source for posts and social |
| PYQ bank: 2,398 questions, 23 papers, answers | `assam-exam-pyq` | Data only | **Biggest SEO asset.** Most competitors only host PDFs |
| Master syllabus for 12 recruitment boards | `assam-exam-syllabus` | Data only | Fuel for syllabus pages |
| Assam GIS layers | `assam-maps` | Data, part live | Geography posts, backlinks from GIS users |
| Primary sources (Kamarupa inscriptions etc.) | `assam-history-sources` | Data | Trust and citations |
| Brand kit, 36 illustrations, carousels | `axomrank-brand-assets` | Library | Ready social content |
| Ahom history book | `assam-history-books` | In production | **Sellable product** |
| Blog | `axomrank-blog` (new) | Live after first deploy | SEO top of funnel |

## 2. The competition

| Competitor | Type | What they win on | Where AxomRank can beat them |
|---|---|---|---|
| **Adda247** (adda247.com) | National ed-tech, **direct product competitor** | Dozens of paid Assamese-medium batches (ADRE 3.0, APSC CCE, Assam Police "Mission Khaki"), printed Assamese books, mock test packs, a huge domain | Free and offline, deeper Assam history with sources, open answer data. Adda's Assam pages are batch sales pages, not learning content |
| **eKuhipath** (ekuhipath.com) | Assam ed-tech, **direct product competitor** | Assamese-medium paid courses (for example, an ADRE computer skill test course at ₹599 with 10 mocks), Telegram channel, YouTube, app | Interactive lessons and spaced review rather than video, free core. Match their Telegram presence |
| **Local coaching institutes** (Guwahati, Jorhat, Dibrugarh, etc.) | Offline, **direct business competitor** | Trust, word of mouth, doubt clearing, Facebook and YouTube | Do not fight them; **partner** (see section 5) |
| **Job Assam, AssamCareer, FreeJobAlert, Assam job blogs** | Notification portals, **SEO competitor, not a product competitor** | Very high traffic on "notification / admit card / result" searches | Blog "how to prepare" posts that link each new notification to free preparation. A job radar could be rebuilt later |
| **AglaSem, TutorialsDuniya** | PYQ PDF hosts, **SEO competitor** | Rank for "previous year question paper PDF" | AxomRank has **text questions with answers and topic tags**. Make them searchable HTML pages, not PDFs |
| **assaminfo.com, Assam GK blogs** | Publishers, **SEO competitor** | Assam GK lists | Source-checked lists. They disagree with each other (for example, 39 vs 41 Ahom kings), and AxomRank explains why |
| **Testbook, Unacademy, HenceProve (free mocks)** | Ed-tech / mock sites | Mock tests | Mock tests built from real SLRC papers, with an official-key label |
| **Disha, MH Education, Oswal** | Book publishers | ADRE guides | The AxomRank book (from the `assam-history-books` repo), sold with free app access |

**Positioning line:** *Free, bilingual, source-checked preparation for Assam government exams, built on the real papers.*

## 3. Funnel and how AxomRank makes money

```
Search / Telegram / Instagram / YouTube Shorts
        │
        ▼
Blog post or PYQ page  ──►  Free app (no login)  ──►  Google sign-in to save progress (Firebase)
                                                          │
                                                          ▼
                                            Paid layer (pick 1–2 to start):
                                            • Full timed mock-test packs (₹99–₹299 per exam)
                                            • AxomRank Ahom history book (print + PDF)
                                            • Institute licence (see section 5)
```

Keep **lessons and PYQs free**. Being free is the advantage over Adda247 and eKuhipath. Charge for timed full-length mocks with rank comparison and for the book. Both are things aspirants already pay competitors for.

Every link from the blog into the app carries `utm_source=axomrank_blog&utm_medium=…&utm_campaign=<post>`. This is done automatically by `build.py`, so app analytics can show which posts bring learners.

## 4. Content plan (SEO)

### Keyword clusters (directional, so verify volumes with OpenSEO)

| Cluster | Example searches | Intent | Who ranks now | AxomRank page |
|---|---|---|---|---|
| ADRE PYQ | adre previous year question paper, adre 2024 question paper with answer | Informational / download | AglaSem, Adda247, job blogs | Blog analysis (done) + one page per paper (next) |
| ADRE syllabus and pattern | adre grade 3 syllabus, adre exam pattern | Informational | Adda247, Oswal, job portals | Syllabus post from `assam-exam-syllabus` |
| ADRE preparation | adre preparation without coaching, adre study plan | Commercial | Adda247 batch pages, YouTube | Free 8-week plan (done) |
| APSC CCE | apsc prelims previous year paper, apsc syllabus | Informational | Adda247, Unacademy, AglaSem | Analysis (done) + syllabus post |
| Assam history GK | ahom kings list, battle of saraighat, kamarupa dynasties | Informational | Wikipedia, assaminfo, GK blogs | Ahom list (done) + one post per topic, linked to lessons |
| Assam TET | assam tet previous year question paper, tet pedagogy questions | Informational | AglaSem, Adda247 | TET 2021 analysis (320 questions in PYQ) |
| Assam Police | assam police si question paper 2025 | Informational | Job portals | SI and Constable CWT-2025 analysis |
| Notifications | adre notification 2026, apsc admit card | News | Job Assam, FreeJobAlert | "How to prepare" posts. Publish only from official notices |
| Assamese-language | ADRE প্ৰশ্নকাকত, অসমৰ ইতিহাস প্ৰশ্ন | Informational | Very few | Assamese posts after **human review** |

### 12-week publishing calendar (two posts a week)

| Week | Post 1 | Post 2 |
|---|---|---|
| 1 | ✅ ADRE PYQ analysis | ✅ Ahom kings list |
| 2 | ✅ APSC Prelims analysis | ✅ ADRE without coaching |
| 3 | ADRE 2024 Grade III HSSLC paper with answers (HTML page) | Battle of Saraighat: facts asked in exams |
| 4 | Assam TET 2021 paper analysis | ADRE Grade III syllabus from the official notice |
| 5 | Assam Police SI 2025 paper with answers | Kamarupa dynasties (Varman, Mlechchha, Pala) |
| 6 | ADRE 2024 Grade IV HSLC paper with answers | Assam districts list (with map from `assam-maps`) |
| 7 | APSC CCE syllabus explained | National parks and wildlife sanctuaries of Assam |
| 8 | Assam Police Constable 2025 paper with answers | Srimanta Sankardeva and the satras: exam facts |
| 9 | 50 Assam culture questions from real papers | Rivers of Assam |
| 10 | ADRE maths: number system questions from real papers | Assam freedom fighters |
| 11 | First Assamese post (reviewed): ADRE PYQ analysis in Assamese | Sixth Schedule councils of Assam |
| 12 | Results roundup: what the blog data shows | Year-in-review, Assam GK 2026 |

Rules for every post: real data or a named source, a clear table, an FAQ section (it becomes FAQ structured data automatically), a link to the matching free lesson, and a corrections link.

## 5. Sales: partners, not only students

1. **Coaching institutes (B2B).** Offer institutes in Guwahati, Jorhat, Dibrugarh, Tezpur and Silchar a free "class pack": PYQ topic sheets and a classroom-mode link to the app with the institute's name. Upsell: a branded mock-test series. This turns the biggest offline competitor into a distribution channel.
2. **Colleges and B.Ed / D.El.Ed institutes** for the TET audience. Offer free pedagogy and TET PYQ sets.
3. **Libraries and district employment exchanges.** Provide a printable QR poster to "practise ADRE PYQs free".
4. **The book.** Pre-orders open on the blog when Book 01 is ready, and every copy includes app access.

## 6. Channels

| Channel | Why | Cadence | Source repo |
|---|---|---|---|
| **Telegram channel** | Where Assam aspirants already are (eKuhipath and Adda run channels) | Daily quiz question + weekly post link | `assam-exam-pyq` |
| **WhatsApp channel** | Same audience, more personal | 3 posts a week | `assam-exam-pyq`, blog |
| **Instagram carousels** | 10 carousels already designed | 3 a week | `axomrank-brand-assets` |
| **YouTube Shorts** | "One Ahom king in 60 seconds", 41 episodes ready-made | 2 a week | `ahom-kingdom-history`, `assam-history-characters` |
| **Facebook groups** (ADRE, APSC, TET aspirant groups) | High reach in Assam | Share PYQ analysis posts, no spam | blog |
| **Google Search** | Long-term compounding traffic | 2 posts a week | blog |

## 7. Measures (check monthly)

- Blog: Search Console impressions, clicks and top queries (connect GSC to OpenSEO).
- Funnel: app sessions with `utm_source=axomrank_blog`, and lesson starts per post.
- Retention: learners returning after 7 days (spaced review is the hook).
- Revenue, once the paid layer starts: mock-pack conversion rate from active learners.

## 8. Fixes that block marketing (do these first)

1. **One canonical home.** Today there are axomrank.org (Odoo, with placeholder links, a different email, and links to `angsumi.github.io`), axomrank.odoo.com, axomrank.pages.dev and axomrank.github.io. axomrank.onrender.com belonged to the deleted `Axomrank_matt` repo, so check whether the Render service is still running. Make **axomrank.org** the front door: point it at the app, put the blog at **blog.axomrank.org**, and either retire the Odoo site or fix its links.
2. **Clean up the GitHub profile** (see [ACCOUNT-ORGANISATION.md](ACCOUNT-ORGANISATION.md)). Badge-farming repos look bad to partners and journalists.
3. **Search Console + OpenSEO.** Verify axomrank.org, the pages.dev site and the blog in Google Search Console. Connect the OpenSEO MCP so the next review has real search volumes.
4. **Consistent contact details** across the app, blog, Odoo site and social bios.

## 9. Launch material

Use the [live blog](https://axomrank.github.io/axomrank-blog/) for distribution until the custom domain is active. The following drafts can be posted from the relevant AxomRank accounts.

**Telegram or WhatsApp quiz**

ADRE practice question. Who led the Mughal forces at the Battle of Saraighat? Try the real Driver paper question and tap Show answer when you're ready. [Try the question](https://axomrank.github.io/axomrank-blog/question/saraighat-mughal-commander/)

**Instagram caption**

Revising Assam's national parks? The 2025–26 Economic Survey lists eight, including Sikhna Jwhwlao in Kokrajhar and Chirang. Save the list and try the linked APSC questions. [Read the guide](https://axomrank.github.io/axomrank-blog/national-parks-of-assam/)

**Short video script**

ADRE can ask you for the Mughal commander or the emperor at Saraighat. The commander was Ram Singh of Amber. The emperor who sent him was Aurangzeb. Lachit Borphukan commanded the Ahoms. Test yourself on the three linked ADRE questions. [Read the guide](https://axomrank.github.io/axomrank-blog/battle-of-saraighat/)

**Classroom resource**

Ask learners to try one section of the culture set and note any guesses. In the discussion, open the original question and compare its answer source with the relevant guide. [Open the practice set](https://axomrank.github.io/axomrank-blog/assam-gk/culture-questions/)

Channel posting, partner outreach, external directory submissions and book pre-orders require access to the relevant accounts or a release decision. Use the [SEO growth plan](SEO-GROWTH-PLAN.md) for domain, Search Console and publishing status.

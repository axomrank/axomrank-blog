# Programmatic SEO plan for AxomRank Blog

27 November 2026

Build a small set of exam-specific practice guides from the open question archive. Each guide should help a candidate practise a named skill, see how it appeared in their exam and check the answer against the original paper. The first rollout focuses on ADRE. The same approach can extend to APSC after the pilot shows that the pages earn search visibility and help readers find practice.

## What we already have

The blog builds 23 full or partial paper pages, 50 cross-exam topic pages and five exam hubs. The 27 November build has 42 published articles, including the ADRE score calculator and the practical computer-test exercise. Reader-facing archives include answer provenance and links to exact numbered questions. The new guides should use the same paper URLs and topic index. [Question papers](https://axomrank.github.io/axomrank-blog/question-papers/) · [Topic index](https://axomrank.github.io/axomrank-blog/questions/) · [Exam hubs](https://axomrank.github.io/axomrank-blog/exams/)

The candidate counts below come from the 2,398-row question dataset at revision `84c2530beb1e12e4214a452d21b2a39ecb8afe1a`. The count includes single-option questions with an official answer key and clear question and classification review flags. A paper is identified by exam, year and paper code. These counts measure practice coverage. Search demand needs a separate check. [Pinned question dataset](https://github.com/axomrank/assam-exam-pyq/tree/84c2530beb1e12e4214a452d21b2a39ecb8afe1a)

## First five candidates

| Stage | Article and proposed route | Verified question pool | What the candidate gets |
| --- | --- | ---: | --- |
| Pilot | **ADRE verbal reasoning previous-year questions** · `/questions/adre/verbal-reasoning/` | 66 from five 2024 papers with final keys | A worked decoding example, a short practice set and a breakdown by paper level. |
| Pilot | **ADRE vocabulary questions with explanations** · `/questions/adre/vocabulary/` | 58 from five 2024 papers with final keys | Exam-specific drills for word meanings, grouped by the question types actually found in the papers. |
| Pilot | **ADRE arithmetic previous-year questions** · `/questions/adre/arithmetic/` | 32 from five 2024 papers with final keys | Worked percent and ratio examples, followed by a practice set and an error checklist. |
| Follow-up | **APSC CSAT reading comprehension practice** · `/questions/apsc-cce/reading-comprehension/` | 35 from three papers across 2023–25 with provisional keys | Intact passages where available, worked inference questions and links back to GS-II booklets. |
| Follow-up | **Assam administration questions for APSC Prelims** · `/questions/apsc-cce/assam-administration/` | 15 from three papers across 2023–25 with provisional keys | Exact paper references and a short explanation of which Assam institution does what, sourced to the issuing institutions. |

The proposed counts are the candidate pool before manual deduplication and review. The first ADRE guides cover multiple levels within one examination year. Display that year explicitly. Keep the [ADRE Number System article](https://axomrank.github.io/axomrank-blog/adre-number-system-questions/) as the target for the existing number-system intent, and put improvements there. The current English Grammar pool has no ADRE rows that pass both review flags, so that subject is a candidate for data review before a guide is proposed. An APSC CSAT practice page serves selected passages. The [APSC CSAT syllabus guide](https://axomrank.github.io/axomrank-blog/apsc-csat-syllabus-practice/) remains the place to check the syllabus and study plan.

## How a generated guide will work

| Part | Implementation |
| --- | --- |
| Approved pages | Keep a small manifest in `data/` with the exam and topic keys, slug, search intent, related URL, selected paper question IDs, editor-written introduction and worked examples, and review status. Each entry represents a specific reader need. |
| Question data | Reuse `pyq_pages.load()`, catalog metadata, published topic slugs and the question renderer. Link examples back to the original paper at `#qN`. Count only the items actually rendered and state the years, paper levels and scope of coverage. |
| Readable article | Lead with the skill and what the archived papers show. Add a short practice set with selectable answers and explanations, a compact paper-coverage table, answer provenance and a next step. Make the core text and answers available in static HTML. |
| Distinct intent | Keep full booklet intent on the paper URL, cross-exam practice on the broad topic URL and ADRE or APSC practice on the approved guide. Compare proposed content with existing articles. Where they answer the same query, update the existing page. |
| Discovery | Link each approved guide from its exam hub and parent topic page. Link back to the matching full papers and relevant study guide. Give published pages a stable canonical URL, a unique title, a sitemap entry and the existing content-based IndexNow handling. |
| Build checks | Validate IDs and links to paper questions, source labels, figure files, complete passage excerpts and count totals. Flag duplicate question stems, route collisions and duplicate intent for review. Keep draft entries out of the public build. Retain the current fallback build when no PYQ dataset is available. |

## Publication and review

1. **Week 1.** Add a preview of eligible candidate sets to the build and create the three ADRE manifest entries. Add two worked examples per article written for its particular skill. For this pilot, start with at least 12 eligible, distinct questions across at least two papers per guide. Check every selected answer against the source, and identify variants of the same question before counting them.
2. **Week 2.** Review the three articles and publish them through the normal static build. Test mobile reading, answer reveal, links to the exact paper questions, canonical URLs and sitemap inclusion. Check that the existing paper and topic URLs still work. Use the current GitHub Pages URL for the baseline.
3. **After 28 days of measurable data.** Inspect each URL in Search Console and review India mobile impressions, clicks, click-through rate and the queries that brought readers to each guide. Check the matching parent topic and exam hub for query overlap. Use the existing tagged app links to measure practice starts if those events are available. Fix delivery and indexing issues before expanding. If the pages are indexed but observations are sparse, keep the pilot small and gather more data.
4. **Next rollout.** Add the two APSC guides when the pilot shows distinct queries or practice use. Preserve provisional-key labels. Update the APSC reading comprehension pool when better source text or an official final key is available. Assamese equivalents require the repository's human editorial review before being added to the sitemap.

The blog property was not visible in the OpenSEO Search Console connection during the previous review. Verify the live URL-prefix property and submit its sitemap for the baseline. Track the pilot URLs and their parent pages as a small group. If two pages answer the same query and neither provides a distinct practice experience, merge the useful material into the stronger page and redirect any retired URL.

## Where to expand after the pilot

- **Paper-level comparisons.** Generate compact comparison tables from complete booklets with consistent classification. Insert the tables into existing articles such as the HSSLC versus Graduate guide. Publish a separate comparison only when it answers an uncovered choice.
- **Exact-question explainers.** Use an allowlist for questions with a verified paper reference, an explanation that adds context and a distinct search intent. Keep other questions in their booklet or topic page.
- **Recruitment rule examples.** Share templates for mark calculators and document checklists across genuinely different exam rules. Review each ruleset against the signed notice and any corrigendum. Keep recruitment dates, results, vacancies and eligibility changes in the editorial notice workflow.

The same pages can support answer engines with a direct opening answer, named sources and the exam cycle in visible text. Prioritise the original practice material and accurate source trail. [Google's AI search guidance](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide) · [Google Search spam policies](https://developers.google.com/search/docs/essentials/spam-policies#scaled-content) · [Search Console performance report](https://support.google.com/webmasters/answer/7576553?hl=en)

---
title: ADRE Grade III negative marking and OMR score calculator
description: Calculate your ADRE 2024 HSSLC or Graduate written score with the official negative marking rules and worked examples for each paper.
date: 2026-11-27
slug: adre-grade-3-negative-marking-calculator
exam: ADRE
tags: PYQ
---

**In the 2024 ADRE Grade III papers, a wrong answer lost one quarter of that question's marks.** That meant **−0.25** on a one-mark question and **−0.50** on a two-mark question. The SLRC notice treats multiple marked answers as wrong. Use the calculator for the 2024 HSSLC or Graduate paper with the matching booklet and final key.

## ADRE Grade III score calculator

<form id="adre-score-calculator" class="note adre-score" hidden>
  <label for="adre-paper">2024 paper</label>
  <select id="adre-paper" name="paper">
    <option value="hsslc">HSSLC</option>
    <option value="graduate">Graduate</option>
  </select>
  <fieldset>
    <legend>One-mark questions</legend>
    <label>Correct <input name="one-correct" type="number" inputmode="numeric" min="0" max="150" step="1" value="0" required></label>
    <label>Wrong <input name="one-wrong" type="number" inputmode="numeric" min="0" max="150" step="1" value="0" required></label>
  </fieldset>
  <fieldset id="adre-two-mark-group" disabled hidden>
    <legend>Two-mark questions</legend>
    <label>Correct <input name="two-correct" type="number" inputmode="numeric" min="0" max="25" step="1" value="0" required></label>
    <label>Wrong <input name="two-wrong" type="number" inputmode="numeric" min="0" max="25" step="1" value="0" required></label>
  </fieldset>
  <button class="btn" type="submit">Calculate score</button>
  <output id="adre-score-result" role="status"></output>
</form>
<script src="{{base}}/assets/adre-score-calculator.js" defer></script>

Leave unanswered questions out of the correct and wrong counts. The Graduate booklet identifies **questions 1–125 as one-mark questions and questions 126–150 as two-mark questions**. Match the question numbers to your own booklet before counting.

## Worked HSSLC score

The HSSLC paper carried 150 marks for 150 one-mark questions. Suppose you got 102 right, 28 wrong and left 20 blank. Count 102 points for correct answers and subtract 28 × 0.25 = 7. The written score is **95 out of 150**.

Practise with the [ADRE HSSLC paper]({{base}}/question-papers/adre-2024-grade-3-hsslc-question-paper/).

## Worked Graduate score

Suppose you got 87 right and 20 wrong in the one-mark section, and 17 right and 5 wrong in the two-mark section. The remaining 21 questions were blank.

| Group | Calculation | Score |
| --- | --- | ---: |
| One-mark questions | 87 − (20 × 0.25) | 82 |
| Two-mark questions | (17 × 2) − (5 × 0.50) | 31.5 |
| **Total** | | **113.5 out of 175** |

Use the [ADRE Graduate paper]({{base}}/question-papers/adre-2024-grade-3-graduate-question-paper/) to practise keeping separate tallies by question value. These examples estimate the raw written marks under the cited scheme. Check the official result for any score issued by the commission.

## Frequently asked questions

### How much is deducted for a wrong ADRE Graduate question worth two marks?

The 2024 scheme deducts 0.50 marks for an incorrect two-mark question.

### What happens if I bubble two options?

The SLRC notice counts a multiple-option response as wrong, even if it includes the correct option.

### Do I enter my blank answers in the calculator?

Enter the correct and wrong counts only. The calculator derives the number left blank from the booklet size.

## Sources

- [SLRC ADRE Grade III marking scheme](https://jobassam.in/wp-content/uploads/2024/07/ADRE-Grade-III-Syllabus.pdf), archived copy of notice SLRC-G-III/91/Advertisement/2023/11.
- [Original 2024 Graduate booklet instructions](https://github.com/axomrank/assam-exam-pyq/blob/main/exams/ADRE/2024/source/G3-P4-Degree.pdf), first page.

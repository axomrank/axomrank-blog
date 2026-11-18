#!/usr/bin/env python3
"""Print subject/topic tables from the AxomRank PYQ dataset for analysis posts.

Usage: python scripts/pyq_stats.py path/to/PYQ/questions.csv ADRE [G3|G4]
"""
import collections
import csv
import sys

path, exam = sys.argv[1], sys.argv[2]
prefix = sys.argv[3] if len(sys.argv) > 3 else ""
rows = [r for r in csv.DictReader(open(path, encoding="utf-8"))
        if r["exam"] == exam and r["paper_code"].startswith(prefix)]
n = len(rows)
print(f"{exam} {prefix}: {n} questions\n\n| Subject | Questions | Share |\n|---|---:|---:|")
for k, v in collections.Counter(r["subject"] for r in rows).most_common():
    print(f"| {k} | {v} | {round(100 * v / n)}% |")
print("\n| Topic | Questions |\n|---|---:|")
for k, v in collections.Counter(f"{r['subject']}: {r['topic']}" for r in rows).most_common(15):
    print(f"| {k} | {v} |")
print("\nAnswer sources:", dict(collections.Counter(r["answer_source"] for r in rows)))

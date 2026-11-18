#!/usr/bin/env python3
"""Extract district tables from the Statistical Handbook, Assam 2025 into data/districts.json.

Source (official): Directorate of Economics and Statistics, Government of Assam,
https://des.assam.gov.in/information-and-services/statistical-handbook

Usage:
  curl -LO https://des.assam.gov.in/sites/default/files/swf1/dms43_statistical_handbook_assam_2025_0.pdf
  pdftotext -layout dms43_statistical_handbook_assam_2025_0.pdf handbook.txt
  python scripts/extract_handbook.py handbook.txt dms43_statistical_handbook_assam_2025_0.pdf

Two district frameworks appear in the handbook:
  * Table 1.01 (projected population) and Table 22.08 (colleges) list the current 35 districts.
  * Tables 1.02-1.05 (Census 2011 area, villages, population, SC/ST, literacy) list 33 districts,
    some with older boundaries. We keep both and record which is which.
Table 1.01's rural/urban columns are not used: they do not add up to its own totals.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

NAME_FIX = {"West K.Anglong": "West Karbi Anglong", "West K. Anglong": "West Karbi Anglong",
            "South Salmara": "South Salmara-Mankachar"}
ROW = re.compile(r"^\s*(?:\d{1,2}\s+)?([A-Z][A-Za-z .]*?[a-z.])\s+((?:[\d.]+|-|NA)(?:\s+(?:[\d.]+|-|NA))+)\s*$")


def num(x):
    if x in ("-", "NA"):
        return None
    return float(x) if "." in x else int(x)


def table(lines, title, ncols, stop="Assam"):
    """Rows after the line containing `title`, until the state total row."""
    start = next(i for i, l in enumerate(lines) if title in l)
    out = {}
    for l in lines[start + 1:]:
        m = ROW.match(l)
        if not m:
            continue
        name, vals = m.group(1).strip(), m.group(2).split()
        if name == stop:
            out["_total"] = [num(v) for v in vals[:ncols]]
            break
        if len(vals) >= ncols and name not in ("No.", "Sl."):
            out[NAME_FIX.get(name, name)] = [num(v) for v in vals[:ncols]]
    return out


def main(txt, pdf):
    lines = Path(txt).read_text(encoding="utf-8").splitlines()
    t101 = table(lines, "DISTRICT-WISE PROJECTED", 4)          # 2011, 2024, 2025, 2026
    t102 = table(lines, "DISTRICT-WISE AREA, SUB-DIVISIONS, TOWNS, VILLAGES", 9)
    t103 = table(lines, "DISTRICT-WISE POPULATION IN ASSAM, 2011", 6)
    t104 = table(lines, "POPULATION OF SCHEDULED CASTE AND", 6)
    t105 = table(lines, "DISTRICT-WISE LITERACY RATE BY SEX IN ASSAM", 8)
    t2208 = table(lines, "DISTRICT-WISE NUMBER OF COLLEGES IN ASSAM", 5)
    districts = []
    for name, (p11, p24, p25, p26) in t101.items():
        if name == "_total":
            continue
        d = {"name": name, "population": {"2011_current_boundaries": p11, "2024_projected": p24,
                                          "2025_projected": p25, "2026_projected": p26}}
        c = t2208.get(name)
        if c:
            d["colleges_2024_25"] = {"government": c[0] or 0, "provincialised": c[1] or 0, "model": c[2] or 0,
                                     "private": c[3] or 0, "commerce": c[4] or 0}
        if name in t103:
            tot, fem, rur, urb, ch, chf = t103[name]
            a = t102[name]
            sc = t104.get(name)
            lit = t105[name]
            d["census2011_table"] = {
                "same_boundaries_as_current": tot == p11,
                "population": tot, "female": fem, "male": tot - fem, "rural": rur, "urban": urb,
                "child_0_6": ch, "child_0_6_female": chf,
                "area_sq_km": a[0], "area_rural_sq_km": a[1], "sub_divisions": a[2], "towns": a[3],
                "villages": a[4], "inhabited_villages": a[5], "cd_blocks": a[6], "gaon_panchayats": a[7],
                "revenue_circles": a[8],
                "sc": sc[0] if sc else None, "sc_female": sc[1] if sc else None, "sc_sex_ratio": sc[2] if sc else None,
                "st": sc[3] if sc else None, "st_female": sc[4] if sc else None, "st_sex_ratio": sc[5] if sc else None,
                "literacy": {"total": lit[0], "male": lit[1], "female": lit[2], "rural": lit[3], "urban": lit[4],
                             "gender_gap": lit[5]},
            }
        districts.append(d)
    assert len(districts) == 35, len(districts)
    assert sum(1 for d in districts if "census2011_table" in d) == 33
    # Sanity checks against the handbook's own state totals
    assert sum(d["population"]["2011_current_boundaries"] for d in districts) == t101["_total"][0]
    assert sum(d["census2011_table"]["population"] for d in districts if "census2011_table" in d) == t103["_total"][0]
    out = {
        "source": {
            "title": "Statistical Handbook, Assam 2025",
            "publisher": "Directorate of Economics and Statistics, Government of Assam",
            "url": "https://des.assam.gov.in/information-and-services/statistical-handbook",
            "pdf": "https://des.assam.gov.in/sites/default/files/swf1/dms43_statistical_handbook_assam_2025_0.pdf",
            "sha256": hashlib.sha256(Path(pdf).read_bytes()).hexdigest(),
            "tables": {"1.01": "District-wise projected population (35 districts)",
                       "1.02": "Area, sub-divisions, towns, villages, blocks, gaon panchayats, revenue circles (33 districts)",
                       "1.03": "Population, Census 2011 (33 districts)",
                       "1.04": "SC and ST population, Census 2011 (33 districts)",
                       "1.05": "Literacy rate, Census 2011 (33 districts)",
                       "22.08": "Colleges as on 2024-25 (35 districts)"},
            "note": "The handbook says figures in Tables 1.01-1.05 are provisionally estimated for 35 and 33 districts from Census of India 2011 by DES Assam.",
        },
        "state": {"population_2011": t101["_total"][0], "population_2026_projected": t101["_total"][3],
                  "area_sq_km": t102["_total"][0], "literacy_2011": t105["_total"][0]},
        "districts": districts,
    }
    dst = Path(__file__).resolve().parent.parent / "data" / "districts.json"
    dst.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {dst}: {len(districts)} districts")


if __name__ == "__main__":
    main(*sys.argv[1:3])

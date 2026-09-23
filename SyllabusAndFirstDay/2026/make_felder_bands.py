#!/usr/bin/env python3
"""Band the Felder & Felder solution manuals, one entry per problem.

    python make_felder_bands.py

Writes `_shared/felder-bands-cNN.txt`, read by make_answer_sheets.py so the
worked solution for any Felder problem a plan mentions can be cropped out.

The manuals carry a real text layer, so the bands are MEASURED rather than
read off by eye: `pdftotext -bbox-layout` gives the position of every line,
each problem opens with its own number as the first word of a line near the
top of a page, and a problem runs until the next one starts. A problem
spanning a page break gets one band per page.

The bbox XML is not well-formed (the manuals' encoding emits raw control
characters), so it is scanned with regexes rather than an XML parser.
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

PRIV = Path.home() / "coding/courses/MathematicalPhysics/private"
# The complete set of Felder & Felder chapter solution manuals, c01-c13.
# Three copies also sit in _shared/; this is the full set, so band from here.
MANUALS_DIR = PRIV / "Solutions to Felder and Felder"
SHARED = PRIV / "F2026PrepPacks/_shared"

PAGE = re.compile(r'<page width="([\d.]+)" height="([\d.]+)">')
LINE = re.compile(r'<line xMin="([\d.]+)" yMin="([\d.]+)" xMax="[\d.]+" yMax="[\d.]+">(.*?)</line>', re.S)
WORD = re.compile(r'<word[^>]*>(.*?)</word>', re.S)

TOP = 0.30        # a problem header sits in the top third of its page
PAD = 0.010


def headers(xml_path):
    raw = xml_path.read_text(encoding="utf8", errors="replace")
    marks = [(m.start(), float(m.group(2))) for m in PAGE.finditer(raw)]
    marks.append((len(raw), 0.0))
    out = []
    for i in range(len(marks) - 1):
        start, H = marks[i]
        for lm in LINE.finditer(raw[start:marks[i + 1][0]]):
            ws = [w.strip() for w in WORD.findall(lm.group(3))]
            if not ws:
                continue
            m = re.fullmatch(r"(\d+\.\d+)", ws[0])
            if m and float(lm.group(2)) / H < TOP:
                out.append((i + 1, float(lm.group(2)) / H, m.group(1)))
    return out, len(marks) - 1


def main():
    manuals = sorted(MANUALS_DIR.glob("c[0-9][0-9]solutions.pdf"))
    if not manuals:
        sys.exit(f"no chapter manuals in {MANUALS_DIR}")
    for pdf in manuals:
        name = pdf.name
        with tempfile.TemporaryDirectory() as td:
            xml = Path(td) / "b.xml"
            subprocess.run(["pdftotext", "-bbox-layout", str(pdf), str(xml)],
                           check=True, capture_output=True)
            hits, npages = headers(xml)

        # keep the first appearance of each problem, in reading order
        seen, ordered = set(), []
        for h in hits:
            if h[2] not in seen:
                seen.add(h[2])
                ordered.append(h)

        out = [f"# {name}: one band per problem, measured from the PDF's own",
               "# text layer (pdftotext -bbox-layout). Do not hand-edit; rerun",
               "# make_felder_bands.py instead.",
               "# Format:  <problem> = <page>@<top>-<bottom>",
               ""]
        for i, (pg, y, prob) in enumerate(ordered):
            nxt = ordered[i + 1] if i + 1 < len(ordered) else None
            top = max(0.0, y - PAD)
            if nxt and nxt[0] == pg:
                out.append(f"{prob} = {pg}@{top:.3f}-{nxt[1] - PAD:.3f}")
            else:
                last = (nxt[0] - 1) if nxt else npages
                out.append(f"{prob} = {pg}@{top:.3f}-0.950")
                for mid in range(pg + 1, min(last, pg + 3) + 1):
                    out.append(f"{prob} = {mid}@0.050-0.950")
                if nxt and nxt[0] <= pg + 4:
                    out.append(f"{prob} = {nxt[0]}@0.050-{nxt[1] - PAD:.3f}")
        dest = SHARED / f"felder-bands-{name[:3]}.txt"
        dest.write_text("\n".join(out) + "\n")
        print(f"  {name}: {npages} pages, {len(ordered)} problems -> {dest.name}")


if __name__ == "__main__":
    main()

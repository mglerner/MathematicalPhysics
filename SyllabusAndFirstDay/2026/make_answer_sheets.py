#!/usr/bin/env python3
"""Write 03-answers.html: one answer sheet per prep pack (PHY 210).

Michael's own sheet: the day's PCCI answer first, then every other problem
the plan carries an answer for, then the worked solutions cropped out of
the pack's Felder/Gary solution PDFs.

Same idea as the PHY 317 generator, with two differences that matter:

1. NO FILE GLOB. 317's solution PDFs are named "Will ChN in-class problem
   solutions ...", so a `*olution*.pdf` glob finds them. 210's are named in
   prose -- "Manbir 1.30 Day 3 (arbitrary constants, SHO general solution,
   ICs).pdf" is a DECK, not a solution set, and a glob picks it up. So here
   the `Solutions:` line is the only source of truth for which PDFs are
   solution sets; nothing is included unless it is named there.

2. PCCI FIRST, and groupwork is not assumed. Every 210 day has a PCCI;
   in-class problems come and go. So the sheet leads with the PCCI and
   falls back to "everything else with an answer", rather than 317's
   Groupwork/other split.

The `Solutions:` line goes under `Totals:` in 00-prep-notes.md:

    Solutions: 10.1 and 10.3#2 = 10.1@.118-.474; 10.1 and 10.3#5 = 10.3@.083-.392

The key before `#` is any substring of the PDF's filename that picks it out
uniquely; `#N` is the page; `@a-b` is the problem's band as a fraction of
page height. A problem spanning a page break gets one entry per page. A
problem listed without a band labels the page without cropping it.

    python make_answer_sheets.py            # all packs
    python make_answer_sheets.py 06 07      # just these
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

import make_active_learning as M

SOL_DPI = 110
PAD = 0.004

# Gary's PCCI solution key: one shared document covering the Discovery
# Exercises, so its band map is shared too rather than copied per pack.
# Bands are MEASURED from the file's own text layer, not eyeballed --
# it is a Word export, so every DE header has a real position.
GARY_KEY = (Path.home() / "coding/courses/MathematicalPhysics/private"
            / "F2026PrepPacks/_shared"
            / "Gary - PCCI solution key (27 Discovery Exercises, w page numbers).pdf")
GARY_BANDS = GARY_KEY.with_name("gary-pcci-bands.txt")

# Felder & Felder's own solution manuals, one per chapter, also shared.
# They carry crop marks at the sheet edges, so the crop keeps the text
# column rather than the full width.
# The band files are generated into _shared/ beside Gary's key; the
# manuals they point into live in their own folder. Two paths, not one.
FELDER_BANDS_DIR = GARY_KEY.parent
FELDER_DIR = (Path.home() / "coding/courses/MathematicalPhysics/private"
              / "Solutions to Felder and Felder")
FELDER_X = (0.085, 0.925)

CSS = """
body { background: #fff; margin: 0; padding: 16px 18px; color: #111;
       font-family: "Iowan Old Style", Palatino, Georgia, serif;
       font-variant-numeric: tabular-nums; }
h1 { font-size: 19px; margin: 0 0 2px 0; font-weight: normal; }
h1 .when { font-size: 14px; font-style: italic; color: #666; margin-left: 10px; }
h2 { font-size: 12px; letter-spacing: .12em; text-transform: uppercase;
     color: #6b6b6b; margin: 16px 0 6px 0; font-weight: normal;
     border-bottom: 1px solid #ccc; padding-bottom: 3px; }
.prob { margin: 0 0 14px 0; break-inside: avoid; }
.num { font-weight: bold; font-size: 15px; }
.num .when { font-weight: normal; font-style: italic; color: #777;
             font-size: 12.5px; margin-left: 6px; }
.task { font-size: 13.5px; color: #333; margin: 1px 0 2px 0; }
ul { margin: 0; padding-left: 17px; }
li { font-size: 14.5px; line-height: 1.4; }
.none { font-size: 13.5px; color: #777; font-style: italic; }
.worked { margin: 5px 0 0 0; }
.worked img { width: 100%; border: 1px solid #ddd; display: block;
              margin: 3px 0 0 0; }
.cap { font-size: 12.5px; color: #666; font-style: italic; margin: 0; }
.sol { margin: 0 0 20px 0; break-inside: avoid; }
.sol img { width: 100%; border: 1px solid #ccc; display: block; }
.warn { background: #fff3cd; border: 1px solid #e0cd8a; padding: 7px 10px;
        font-size: 13px; margin: 14px 0 0 0; }
@media print { body { padding: 0; } h2 { break-after: avoid; } }
"""

SKIP_AS_TASK = ("Check:", "Check ", "Read back:", "Next:")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def tagged_line(lines, label):
    for l in lines:
        if l.startswith(label):
            return l[len(label):].strip()
    return None


def segments(text):
    return [s.strip() for s in text.split("<br>") if s.strip()]


def row_entries(rows):
    """[(problem-or-None, when, task, [checks], row_text, all_probs)]."""
    out = []
    for a, b, m, mode, _src, text in rows:
        segs = segments(text)
        checks = [s for s in segs if s.startswith("Check")]
        if not checks:
            continue
        body = [s for s in segs if not s.startswith(SKIP_AS_TASK)]
        probs = [q for s in body for q in re.findall(r"\b(\d+\.\d+)\b", s)]
        if not probs:   # "Check 10.1: ..." can be the only place a number appears
            probs = [q for s in checks for q in re.findall(r"\b(\d+\.\d+)\b", s)]
        task = next((s for s in body if re.search(r"\b\d+\.\d+\b", s)),
                    body[0] if body else "")
        out.append((probs[0] if probs else None, M.clock(a), task, checks,
                    text, probs))
    return out


def pcci_problems(rows):
    """Problem numbers named on the collection row, e.g. {"10.1", "10.3"}.

    Needed because the row that WORKS the PCCI does not always say "PCCI":
    class 07's is "Compare 10.1 and 10.3 and agree on the step ...".
    """
    for _a, _b, _m, _mode, _src, text in rows:
        first = text.split("<br>")[0]
        if "PCCI" in first and "Collect" in first:
            return set(re.findall(r"\b(\d+\.\d+)\b", first))
    return set()


def pcci_label(rows):
    """The PCCI this day COLLECTS, from the plan's collection row.

    Only a row that says "Collect ... PCCI" counts. Every pack also carries
    a `PCCI (on Moodle): ...` line announcing the NEXT one, and day 1 carries
    "PCCI 1 -- read the syllabus"; matching those would label a day with a
    PCCI it does not collect. Two phrasings are in use:
    "Collect PCCI 6, problems 10.1 and 10.3." and
    "Collect the PCCI, DE 10.10.1 parts 1-9."
    """
    for _a, _b, _m, _mode, _src, text in rows:
        first = text.split("<br>")[0]
        if "PCCI" not in first or "Collect" not in first:
            continue
        m = re.search(r"Collect\s+(?:the\s+)?PCCI\s*(\d+)?\s*[,(]?\s*"
                      r"(.{0,60}?)(?=\.(?!\d)|\)|<br>|$)", first)
        if not m:
            continue
        num, what = m.group(1), (m.group(2) or "").strip().rstrip(",.")
        if len(what) > 55 or what.lower().startswith("the first collection"):
            what = ""
        label = "PCCI" + (f" {num}" if num else "")
        return label + (f" -- {what}" if what else "")
    return None


def solutions_map(lines):
    """-> {(filename-substring, page): [(problem, band-or-None)]}."""
    raw = tagged_line(lines, "Solutions:")
    out = {}
    if not raw:
        return out
    for entry in raw.split(";"):
        if "=" not in entry or "#" not in entry.split("=")[0]:
            continue
        key, probs = entry.split("=", 1)
        sub, page = key.rsplit("#", 1)
        items = []
        for tok in probs.split(","):
            tok = tok.strip()
            if not tok:
                continue
            m = re.match(r"([\d.]+?)@([\d.]+)-([\d.]+)$", tok)
            items.append((m.group(1), (float(m.group(2)), float(m.group(3))))
                         if m else (tok, None))
        out[(sub.strip().lower(), int(page.strip()))] = items
    return out


def gary_bands():
    """-> {"1.6.1": [(page, top, bottom), ...]} from the shared band file."""
    out = {}
    if not GARY_BANDS.exists():
        return out
    for line in GARY_BANDS.read_text().split("\n"):
        line = line.split("#")[0].strip()
        m = re.match(r"DE\s+([\d.]+)\s*=\s*(\d+)@([\d.]+)-([\d.]+)$", line)
        if m:
            out.setdefault(m.group(1), []).append(
                (int(m.group(2)), float(m.group(3)), float(m.group(4))))
    return out


def felder_bands():
    """-> {"10.1": [(pdf_name, page, top, bottom), ...]} across all chapters."""
    out = {}
    for f in sorted(FELDER_BANDS_DIR.glob("felder-bands-c*.txt")):
        pdf = f.name.replace("felder-bands-", "").replace(".txt", "") + "solutions.pdf"
        for line in f.read_text().split("\n"):
            line = line.split("#")[0].strip()
            m = re.match(r"([\d.]+)\s*=\s*(\d+)@([\d.]+)-([\d.]+)$", line)
            if m:
                out.setdefault(m.group(1), []).append(
                    (pdf, int(m.group(2)), float(m.group(3)), float(m.group(4))))
    return out


def crop_felder(pack_dir, prob, bands):
    """Cut one Felder problem's worked solution out of its manual."""
    spans = bands.get(prob)
    if not spans or not shutil.which("pdftoppm"):
        return []
    try:
        from PIL import Image
    except ImportError:
        return []
    out_dir = pack_dir / "03-answers-files"
    out_dir.mkdir(exist_ok=True)
    got = []
    for i, (pdf, page, top, bot) in enumerate(spans, 1):
        src_pdf = FELDER_DIR / pdf
        if not src_pdf.exists():
            continue
        tag = f"felder-{prob.replace('.', '_')}-{i}"
        dst = out_dir / f"{tag}.png"
        if not dst.exists():
            subprocess.run(["pdftoppm", "-png", "-r", str(SOL_DPI),
                            "-f", str(page), "-l", str(page),
                            str(src_pdf), str(out_dir / (tag + "-raw"))],
                           check=True, capture_output=True)
            raw = sorted(out_dir.glob(tag + "-raw-*.png"))
            if not raw:
                continue
            im = Image.open(raw[0])
            w, h = im.size
            im.crop((int(FELDER_X[0] * w), max(0, int(top * h)),
                     int(FELDER_X[1] * w), min(h, int(bot * h)))).save(dst)
            raw[0].unlink()
        got.append((f"03-answers-files/{dst.name}",
                    f"Felder {pdf[:3]} solutions, {prob}"
                    + (f" (page {i} of {len(spans)})" if len(spans) > 1 else "")))
    return got


def crop_gary(pack_dir, de, bands):
    """Cut this day's Discovery Exercise out of Gary's key. -> [(src, cap)]."""
    spans = bands.get(de)
    if not spans or not GARY_KEY.exists() or not shutil.which("pdftoppm"):
        return []
    try:
        from PIL import Image
    except ImportError:
        return []
    out_dir = pack_dir / "03-answers-files"
    out_dir.mkdir(exist_ok=True)
    got = []
    for i, (page, top, bot) in enumerate(spans, 1):
        tag = f"gary-de-{de.replace('.', '_')}-{i}"
        src = out_dir / f"{tag}.png"
        if not src.exists():
            subprocess.run(["pdftoppm", "-png", "-r", str(SOL_DPI),
                            "-f", str(page), "-l", str(page),
                            str(GARY_KEY), str(out_dir / (tag + "-raw"))],
                           check=True, capture_output=True)
            raw = sorted(out_dir.glob(tag + "-raw-*.png"))
            if not raw:
                continue
            im = Image.open(raw[0])
            w, h = im.size
            im.crop((0, max(0, int(top * h)), w, min(h, int(bot * h)))).save(src)
            raw[0].unlink()
        got.append((f"03-answers-files/{src.name}",
                    f"Gary's PCCI key, DE {de}"
                    + (f" (page {i} of {len(spans)})" if len(spans) > 1 else "")))
    return got


def render_pages(pack_dir, smap):
    """Rasterise only the PDFs the Solutions: line names. -> [page dicts]."""
    if not shutil.which("pdftoppm") or not smap:
        return []
    subs = {sub for sub, _ in smap}
    pdfs = sorted({p for p in pack_dir.glob("*.pdf")
                   if any(s in p.name.lower() for s in subs)})
    out_dir = pack_dir / "03-answers-files"
    pages = []
    for pdf in pdfs:
        stem = re.sub(r"[^A-Za-z0-9]+", "-", pdf.stem).strip("-").lower()[:48]
        out_dir.mkdir(exist_ok=True)
        subprocess.run(["pdftoppm", "-png", "-r", str(SOL_DPI), str(pdf),
                        str(out_dir / stem)], check=True, capture_output=True)
        for png in sorted(out_dir.glob(stem + "-*.png")):
            n = re.search(r"-(\d+)\.png$", png.name)
            if n:
                pages.append({"path": png, "src": f"03-answers-files/{png.name}",
                              "file": pdf.name, "stem": stem, "page": int(n.group(1))})
    return pages


def crop_problems(pages, smap):
    try:
        from PIL import Image
    except ImportError:
        return {}, set()
    crops, claimed = {}, set()
    for pg in pages:
        items = []
        for (sub, page), lst in smap.items():
            if sub in pg["file"].lower() and page == pg["page"]:
                items = lst
                break
        banded = [(q, b) for q, b in items if b]
        for (qa, ba), (qb, bb) in zip(banded, banded[1:]):
            if ba[1] + PAD > bb[0] - PAD:
                print(f"WARNING {pg['file']} p{pg['page']}: {qa} and {qb} overlap "
                      f"once PAD={PAD} is added; tighten a band or lower PAD")
        im = None
        for prob, band in items:
            if band is None:
                continue
            if im is None:
                im = Image.open(pg["path"])
            w, h = im.size
            y0, y1 = max(0, int((band[0] - PAD) * h)), min(h, int((band[1] + PAD) * h))
            if y1 <= y0:
                continue
            name = f"{pg['stem']}-p{pg['page']}-{prob.replace('.', '_')}.png"
            im.crop((0, y0, w, y1)).save(pg["path"].parent / name)
            crops.setdefault(prob, []).append(
                (f"03-answers-files/{name}", f"{pg['file']}, p{pg['page']}"))
            claimed.add(id(pg))
    return crops, claimed


def render(n, date, topic, rows, pages, smap, crops, claimed, gary, fcrops):
    pnums = pcci_problems(rows)
    pcci, other = [], []
    for prob, when, task, checks, text, probs in row_entries(rows):
        is_pcci = "PCCI" in text or (pnums and set(probs) & pnums)
        (pcci if is_pcci else other).append((prob, when, task, checks))

    o = ["<!doctype html><meta charset=utf-8>",
         f"<title>PHY 210 answers -- class {n:02d}</title><style>{CSS}</style>",
         f"<h1>Class {n:02d} answers<span class=when>{date} &middot; "
         f"{esc(topic)}</span></h1>"]
    seen = set()

    def block(title, items, empty):
        o.append(f"<h2>{title}</h2>")
        if not items:
            o.append(f"<p class=none>{empty}</p>")
            return
        for prob, when, task, checks in items:
            o.append(f'<div class=prob><div class=num>{prob or "&mdash;"}'
                     f'<span class=when>{when}</span></div>')
            if task and task != prob:
                o.append(f"<div class=task>{esc(task)}</div>")
            o.append("<ul>" + "".join(f"<li>{esc(c)}</li>" for c in checks) + "</ul>")
            imgs = list(crops.get(prob, [])) + list(fcrops.get(prob, []))
            if imgs and prob not in seen:
                seen.add(prob)
                o.append("<div class=worked>")
                for src, cap in imgs:
                    o.append(f'<p class=cap>worked solution &middot; {esc(cap)}</p>'
                             f'<img src="{esc(src)}" alt="{esc(prob)}">')
                o.append("</div>")
            o.append("</div>")

    # The heading never claims a day HAS no PCCI: class 09's PCCI 7 is
    # "log in to the hub", which is collected but has no answer to print.
    # State what is actually known -- whether the plan has a collection row.
    label = pcci_label(rows)
    block(label or "PCCI", pcci,
          "the plan's PCCI row carries no Check: line"
          if label else
          "no <code>Collect ... PCCI</code> row in this day's plan")
    if gary:
        o.append("<div class=worked>")
        for src, cap in gary:
            o.append(f'<p class=cap>{esc(cap)}</p>'
                     f'<img src="{esc(src)}" alt="{esc(cap)}">')
        o.append("</div>")
    block("Everything else with an answer", other, "none")

    left = [p for p in pages if id(p) not in claimed]
    if left:
        o.append("<h2>Other solution pages</h2>")
        o.append("<p class=warn>Shown whole because no problem on them is "
                 "cropped for today.</p>")
        for pg in sorted(left, key=lambda g: (g["file"], g["page"])):
            listed = None
            for (sub, page), items in smap.items():
                if sub in pg["file"].lower() and page == pg["page"]:
                    listed = [q for q, _ in items]
            bits = ("on this page: " + esc(", ".join(listed))) if listed else \
                   "not listed on the <code>Solutions:</code> line"
            o.append(f'<div class=sol><p class=cap>{bits}</p>'
                     f'<p class=cap>{esc(pg["file"])}, page {pg["page"]}</p>'
                     f'<img src="{esc(pg["src"])}" alt="{esc(pg["file"])}"></div>')
    elif not smap:
        o.append("<h2>Worked solutions</h2>")
        o.append("<p class=none>no <code>Solutions:</code> line in the prep "
                 "notes, so no solution PDF is claimed for this day</p>")

    o.append("<footer>Generated by make_answer_sheets.py from the plan table "
             "in 00-prep-notes.md -- edit the plan, not this file.</footer>")
    return "\n".join(o)


def main(only=None):
    wrote = cropped = withsol = withkey = felder = 0
    bands, fbands = gary_bands(), felder_bands()
    for n, date, path in M.pack_files():
        if only and f"{n:02d}" not in only:
            continue
        lines = path.read_text().split("\n")
        rows = M.plan_rows(lines, path)
        if not rows:
            continue
        smap = solutions_map(lines)
        de = re.search(r"DE\s+(\d+\.\d+\.\d+)", pcci_label(rows) or "")
        gary = crop_gary(path.parent, de.group(1), bands) if de else []
        withkey += bool(gary)
        wanted = {q for *_ , probs in row_entries(rows) for q in probs}
        fcrops = {q: c for q in sorted(wanted)
                  if (c := crop_felder(path.parent, q, fbands))}
        felder += len(fcrops)
        pages = render_pages(path.parent, smap)
        crops, claimed = crop_problems(pages, smap)
        cropped += len(crops)
        withsol += bool(smap)
        (path.parent / "03-answers.html").write_text(
            render(n, date, M.topic(lines, path), rows, pages, smap, crops,
                   claimed, gary, fcrops))
        wrote += 1
    print(f"wrote {wrote} answer sheets; {withkey} carry the PCCI solution from "
          f"Gary's key; {felder} Felder worked solutions; {withsol} have a "
          f"Solutions: line; {cropped} problem crops")


if __name__ == "__main__":
    main(set(sys.argv[1:]) or None)

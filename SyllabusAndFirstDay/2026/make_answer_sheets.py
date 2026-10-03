#!/usr/bin/env python3
"""Write _gen/crops.json per prep pack (PHY 210): the solution crops the pack page shows.

The PCCI's solution from Gary's key (a Discovery Exercise) or Felder's manual (a numbered
problem); Felder's worked solution for every problem named in the notes' In-class problems
section; whatever the `Solutions:` line maps out of the pack's own PDFs; and the solution
pages nothing claimed. shared/make_pack_html.py places each crop under its problem.

NO FILE GLOB: 210's solution PDFs are named in prose ("Manbir 1.30 Day 3 (...).pdf" is a
DECK), so the `Solutions:` line is the only source of truth for which PDFs are solution sets.

    Solutions: 10.1 and 10.3#2 = 10.1@.118-.474; 10.1 and 10.3#5 = 10.3@.083-.392

The key before `#` is any substring of the PDF's filename that picks it out uniquely; `#N` is
the page; `@a-b` the problem's band as a fraction of page height. A problem spanning a page
break gets one entry per page; one listed without a band labels the page without cropping it.

    python make_answer_sheets.py            # all packs in the current format
    python make_answer_sheets.py 06 07      # just these
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path.home() / "coding/courses/shared"))
import packnotes as P  # noqa: E402

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


def solutions_map(notes):
    """-> {(filename-substring, page): [(problem, band-or-None)]}."""
    raw = notes.tagged_line("Solutions:")
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


def trim_blank(im, pad=12):
    """Cut blank space off the bottom (and top) of a crop: a page's last solution runs to the
    page foot (10.216, 2026-10-01). Thin marks at the side edges (crop marks, a stray tick) are
    ignored; a row counts as ink only if it has a few dark pixels away from the edges."""
    import numpy as np
    a = np.asarray(im.convert("L"))
    h, w = a.shape
    inner = a[:, int(0.06 * w):int(0.94 * w)]
    rows = np.flatnonzero((inner < 160).sum(axis=1) >= 3)
    if not len(rows):
        return im
    return im.crop((0, max(0, rows[0] - pad), w, min(h, rows[-1] + pad)))


def snap_to_gaps(im, top, bot, bottom_up=False):
    """Pixel rows for a band, moved so neither cut lands inside a line of ink: a cut inside a
    line moves to the end of that line (bottom) or its start (top). The band map comes from the
    manual's poor text layer, and a page-2 band could stop mid-matrix (6.32, 2026-10-01)."""
    import numpy as np
    a = np.asarray(im.convert("L"))
    h, w = a.shape
    ink = (a[:, int(FELDER_X[0] * w):int(FELDER_X[1] * w)] < 160).sum(axis=1) >= 3
    y0, y1 = max(0, int(top * h)), min(h, int(bot * h))
    while y0 > 0 and ink[y0]:
        y0 -= 1
    step = -1 if bottom_up else 1          # a continuation piece never reaches into the next problem
    while 0 < y1 < h - 1 and ink[y1 - 1]:
        y1 += step
    return y0, y1


MANUAL_BODY_TOP = 0.155    # the solutions manual's running head and crop marks end above this


def crop_felder(pack_dir, prob, bands):
    """Cut one Felder problem's worked solution out of its manual."""
    spans = bands.get(prob)
    if not spans or not shutil.which("pdftoppm"):
        return []
    try:
        from PIL import Image
    except ImportError:
        return []
    out_dir = pack_dir / "_gen" / "answer-images"
    out_dir.mkdir(parents=True, exist_ok=True)
    got = []
    # A band that runs onto the next page starts at its top edge: skip the manual's running head
    # and crop marks (they end at 0.147 of the page), and drop a piece that is only that head
    # (the solution ended at the bottom of the previous page; 2.233, 2026-10-01).
    # A continuation piece with under 3% of a page left below the head holds only the NEXT
    # problem's first line (the band map's text layer runs about 0.01 low): 6.32, 6.128.
    spans = [(pdf, page, max(top, MANUAL_BODY_TOP), bot, top < MANUAL_BODY_TOP)
             for pdf, page, top, bot in spans if bot - max(top, MANUAL_BODY_TOP) > 0.03]
    for i, (pdf, page, top, bot, continued) in enumerate(spans, 1):
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
            y0, y1 = snap_to_gaps(im, top, bot, bottom_up=continued)
            piece = trim_blank(im.crop((int(FELDER_X[0] * w), y0, int(FELDER_X[1] * w), y1)))
            raw[0].unlink()
            # a continuation that is shorter than two lines is the next problem's label (9.81's "f(x)")
            if continued and piece.size[1] < 2 * SOL_DPI * 0.25:
                continue
            piece.save(dst)
        got.append((f"answer-images/{dst.name}",
                    f"Felder {pdf[:3]} solutions, {prob}"
                    + (f" (page {i} of {len(spans)})" if len(spans) > 1 else "")))
    # number the pieces actually kept (a dropped continuation must not leave "page 1 of 2")
    got = [(src, re.sub(r" \(page \d+ of \d+\)$", "", cap)
            + (f" (page {k} of {len(got)})" if len(got) > 1 else "")) for k, (src, cap) in enumerate(got, 1)]
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
    out_dir = pack_dir / "_gen" / "answer-images"
    out_dir.mkdir(parents=True, exist_ok=True)
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
        got.append((f"answer-images/{src.name}",
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
    out_dir = pack_dir / "_gen" / "answer-images"
    pages = []
    for pdf in pdfs:
        stem = re.sub(r"[^A-Za-z0-9]+", "-", pdf.stem).strip("-").lower()[:48]
        out_dir.mkdir(parents=True, exist_ok=True)
        subprocess.run(["pdftoppm", "-png", "-r", str(SOL_DPI), str(pdf),
                        str(out_dir / stem)], check=True, capture_output=True)
        for png in sorted(out_dir.glob(stem + "-*.png")):
            n = re.search(r"-(\d+)\.png$", png.name)
            if n:
                pages.append({"path": png, "src": f"answer-images/{png.name}",
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
                (f"answer-images/{name}", f"{pg['file']}, p{pg['page']}"))
            claimed.add(id(pg))
    return crops, claimed

def main(only=None):
    """Write _gen/crops.json per pack: the PCCI's solution from Gary's key (a Discovery Exercise)
    or Felder's manual (a numbered problem), Felder's worked solution for every problem named
    in the In-class problems section, the crops the Solutions: line maps, and the solution pages
    nothing claimed. shared/make_pack_html.py places them under the problems on the pack page."""
    wrote = withkey = felder = cropped = 0
    bands, fbands = gary_bands(), felder_bands()
    for n, date, path in P.pack_files("210"):
        if only and f"{n:02d}" not in only:
            continue
        if not path.exists():
            continue
        notes = P.Notes(path)
        if notes.old_format:
            continue
        pack = path.parent
        smap = solutions_map(notes)
        de = notes.pcci_de()
        pcci_imgs = crop_gary(pack, de, bands) if de else []
        withkey += bool(pcci_imgs)
        problems = {}
        for q in notes.all_problems():
            fc = crop_felder(pack, q, fbands)
            if fc:
                felder += 1
                problems.setdefault(q, {})["worked"] = fc
        pages = render_pages(pack, smap)
        crops, claimed = crop_problems(pages, smap)
        cropped += len(crops)
        for q, lst in crops.items():
            problems.setdefault(q, {}).setdefault("worked", []).extend(lst)
        unclaimed = []
        for pg in pages:
            if id(pg) in claimed:
                continue
            listed = next((", ".join(q for q, _ in lst) for (sub, page), lst in smap.items()
                           if sub in pg["file"].lower() and page == pg["page"]), "")
            unclaimed.append({"src": pg["src"], "file": pg["file"], "page": pg["page"],
                              "note": f"on this page: {listed}" if listed else "not on the Solutions: line"})
        (pack / "_gen").mkdir(exist_ok=True)
        json.dump({"pcci": {"id": notes.pcci_id(), "images": pcci_imgs},
                   "problems": problems, "unclaimed": unclaimed},
                  open(pack / "_gen" / "crops.json", "w"), indent=1)
        wrote += 1
    print(f"wrote {wrote} crops.json; {withkey} PCCI solutions from Gary's key; "
          f"{felder} Felder worked solutions; {cropped} Solutions:-line crops")


if __name__ == "__main__":
    main(set(sys.argv[1:]) or None)

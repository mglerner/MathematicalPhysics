"""One-shot: renumber PHY 210 F2026 prep packs so class numbers count meetings held.
Sep 23 (Mountain Day) was slot 07; it moves to retired-...; packs 08..39 become 07..38.
Usage: renumber_packs_2026-10-04.py [--apply]   (default: dry run)
(APPLIED 2026-10-04, do not re-run; the old-07 assert below now stops it.)"""
import re, shutil, sys
from pathlib import Path
PACKS = Path("/Users/mglerner/coding/courses/MathematicalPhysics/private/F2026PrepPacks")
APPLY = "--apply" in sys.argv
def act(msg, fn):
    print(("DO  " if APPLY else "dry ") + msg)
    if APPLY: fn()
packs = sorted(p for p in PACKS.iterdir() if p.is_dir() and re.match(r"\d\d-2026-", p.name))
old07 = PACKS / "07-2026-09-23-linear-operators"
assert old07.is_dir(), old07
act(f"mv {old07.name} -> retired-2026-09-23-mountain-day-linear-operators",
    lambda: old07.rename(PACKS / "retired-2026-09-23-mountain-day-linear-operators"))
n_dirs = n_files = n_h1 = n_hist = 0
for p in packs:
    nn = int(p.name[:2])
    if nn < 8: continue
    mm = nn - 1
    newdir = PACKS / f"{mm:02d}{p.name[2:]}"
    # files inside named by number: Class NN.html / class-NN.html / class-NN-*.html
    for f in sorted(p.rglob("*")):
        if f.is_file() and re.search(rf"(?i)class[ -]0?{nn}\b", f.name) and f.suffix in {".html", ".md", ".pdf", ".png"}:
            g = f.with_name(re.sub(rf"(?i)(class[ -])0?{nn}\b", lambda m: m.group(1) + (f"{mm:02d}" if "-" in m.group(1) else f"{mm}"), f.name))
            act(f"  mv {f.relative_to(PACKS)} -> {g.name}", lambda f=f, g=g: f.rename(g)); n_files += 1
    # h1 of the notes file
    for notes in [p / ".build" / "notes.md", p / "00-prep-notes.md"]:
        if notes.exists():
            s = notes.read_text()
            new = re.sub(rf"(?m)^# Class 0?{nn} -- ", f"# Class {mm:02d} -- ", s, count=1)
            if new != s:
                act(f"  h1 {notes.relative_to(PACKS)}: Class {nn} -> Class {mm:02d}", lambda notes=notes, new=new: notes.write_text(new)); n_h1 += 1
    # history files: prepend a dated note, do not rewrite the record
    for hist in [p / ".build" / "history.md", p / "_history.md"]:
        if hist.exists():
            note = (f"> Renumbered 2026-10-04: this pack was class {nn:02d} until class numbers were changed to count\n"
                    f"> meetings held (Mountain Day, Sep 23, no longer holds a number). It is now class {mm:02d}; 210\n"
                    f"> class/pack numbers >= 08 in the entries below are the OLD numbers (subtract 1).\n\n")
            act(f"  note {hist.relative_to(PACKS)}", lambda hist=hist, note=note: hist.write_text(note + hist.read_text())); n_hist += 1
    act(f"mv {p.name} -> {newdir.name}", lambda p=p, newdir=newdir: p.rename(newdir)); n_dirs += 1
print(f"{n_dirs} dirs, {n_files} files, {n_h1} h1 lines, {n_hist} history notes")

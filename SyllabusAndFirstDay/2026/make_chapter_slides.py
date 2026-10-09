"""Chapter-opening cards for the GoodNotes decks (PHY 210 F2026), one HTML
page per Felder chapter, generated from the calendar generator.

Each card lists the chapter's class days (date, topic, reading, that
day's PCCI), every WHW that draws problems from the chapter (its three
tiers and due date; computational sets flagged), and the quiz that
covers it. Screenshot the card, paste it into the chapter's deck. Rerun
after any change to CONTENT, PCCI, WHWS, or the calendar:

    python make_chapter_slides.py

Writes private/Decks/ChapterSlides/ChNN.html (and index.html).
Generated; do not edit.
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import make_fall2026_calendar as CAL          # noqa: E402
import make_review_checklists as CHK          # noqa: E402  (puts shared/ on sys.path)
import chapter_slides as CS                   # noqa: E402  (CSS, fmt, write_index)
import courses as C                           # noqa: E402

# Prep material, not course-facing: lives with the decks in private/ (Dropbox).
OUT = C.private("210") / "Decks/ChapterSlides"
TITLES = {   # Felder & Felder, Mathematical Methods in Engineering and Physics
    1: "Introduction to Ordinary Differential Equations",
    2: "Taylor Series and Series Convergence", 3: "Complex Numbers",
    4: "Partial Derivatives", 5: "Integrals in Two or More Dimensions",
    6: "Linear Algebra I", 7: "Linear Algebra II", 8: "Vector Calculus",
    9: "Fourier Series and Transforms",
    10: "Methods of Solving Ordinary Differential Equations",
    11: "Partial Differential Equations",
    12: "Special Functions and ODE Series Solutions",
    13: "Calculus with Complex Numbers",
}
CSS = CS.CSS


fmt = CS.fmt


def chapters_in(text):
    return {int(m) for m in re.findall(r"\b(\d{1,2})\.\d+", text)}


def chapter_days():
    days = defaultdict(list)
    for n, d, topic, reading, is_quiz in CHK.class_rows():
        for ch in chapters_in(reading):
            days[ch].append((d, topic, reading))
    return days


def whws_by_chapter():
    out = defaultdict(list)
    for hw, vis, due, (wn, covers, warm, ess, depth) in CHK.whw_events():
        for ch in chapters_in(" ".join((warm, ess, depth))):
            out[ch].append((hw, due, covers, warm, ess, depth))
    return out


def quizzes_for(ch):
    hits = []
    for d, label in CAL.QUIZZES.items():
        if re.search(r"\bCh\b[^)]*\b%d\b" % ch, label):
            hits.append(f"{label.split(' (')[0]} on {fmt(d)}")
    return hits


def tier_lines(text):
    """'Label: a, b, c. Other: d' -> one problem per line under its label;
    a tier with no problem numbers (a sentence) stays one line."""
    if not re.search(r"\b\d{1,2}\.\d+", text):
        return f"<ul><li class=note>{text}</li></ul>"
    out = []
    for seg in re.split(r"\.\s+(?=[A-Z])", text.strip().rstrip(".")):
        label, _, probs = seg.partition(":")
        if not probs:
            label, probs = "", seg
        # Split on commas OUTSIDE parentheses only: "1.36 (compound interest,
        # by computer)" is one problem, not two (bug found 2026-09-19).
        parts = re.split(r",\s*(?![^()]*\))", probs)
        lis = "".join(f"<li>{x.strip()}</li>" for x in parts if x.strip())
        out.append((f"<div class=grp>{label.strip()}</div>" if label else "") + f"<ul>{lis}</ul>")
    return "".join(out)


def slide(ch, days, whws):
    span = (f"{fmt(days[0][0])} to {fmt(days[-1][0])}" if len(days) > 1
            else fmt(days[0][0]) if days else "")
    h = [f"<!doctype html><meta charset=utf-8><title>Ch {ch} card</title><style>{CSS}</style>",
         "<div class=slide>",
         f"<header><div><span class=num>Chapter {ch}</span><span class=name>{TITLES[ch]}</span></div>"
         f"<div class=when>{span}</div></header>",
         "<div class=cols>"]
    h.append("<div><h2>Class days</h2>")
    for d, topic, reading in days:
        h.append(f"<div class=day>{fmt(d)}</div><ul><li>{topic} <span style='color:#6b6b6b'>({reading})</span></li></ul>")
    h.append("</div>")
    h.append("<div><h2>Pre-class check-ins</h2>")
    for d, _topic, _reading in days:
        pcci = CAL.PCCI.get(d, "") or "none"
        h.append(f"<div class=day>{fmt(d)}</div><ul><li>{pcci}</li></ul>")
    h.append("</div>")
    h.append("<div><h2>Written homework</h2>")
    for hw, due, covers, warm, ess, depth in whws:
        comp = " + Python" if hw in CHK.COMPUTATIONAL else ""
        h.append(f"<div class=hwhead>WHW{hw:02d}{comp}<span class=due>due {fmt(due)}, 10 PM</span></div>")
        for tier, text in (("Warm-up", warm), ("Essentials", ess), ("Depth", depth)):
            h.append(f"<div class=day>{tier}</div>{tier_lines(text)}")
    h.append("</div></div>")
    q = quizzes_for(ch)
    h.append("<footer>" + ("; ".join(q) + "." if q else "Not on a quiz.") +
             " PCCIs are on paper at the start of class; WHWs upload to Moodle.</footer>")
    h.append("</div>")
    return "\n".join(h) + "\n"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    days, whws = chapter_days(), whws_by_chapter()
    chapters = []
    for ch in sorted(set(days) | set(whws)):
        (OUT / f"Ch{ch:02d}.html").write_text(slide(ch, days.get(ch, []), whws.get(ch, [])))
        chapters.append((ch, TITLES[ch], fmt(days[ch][0][0]) if days.get(ch) else "no class day"))
    links = CS.write_index(OUT, C.COURSE["210"]["name"], chapters, "cards", "cards")
    print(f"wrote {len(links)} chapter cards to {OUT}")


if __name__ == "__main__":
    main()

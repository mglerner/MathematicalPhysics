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
import make_review_checklists as CHK          # noqa: E402

# Prep material, not course-facing: lives with the decks in private/ (Dropbox).
OUT = Path.home() / "coding/courses/MathematicalPhysics/private/Decks/ChapterSlides"
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
CSS = """
body { background: #fff; margin: 0; padding: 24px; font-family: Calibri, Carlito, Helvetica, Arial, sans-serif; color: #000; }
.slide { width: 1000px; padding: 28px 36px; box-sizing: border-box; }
h1 { color: #c00000; font-weight: normal; font-size: 32px; margin: 0 0 14px 0; }
h2 { font-size: 22px; font-weight: normal; margin: 14px 0 6px 0; }
table { border-collapse: collapse; font-size: 19px; }
td { padding: 2px 14px 2px 0; vertical-align: top; }
td.day { white-space: nowrap; color: #444; }
.hw { font-size: 19px; margin: 4px 0 8px 0; }
.hw .name { font-weight: bold; }
.hw .tier { color: #444; display: block; margin-top: 4px; }
.tiers { display: flex; gap: 28px; }
.tiers > div { flex: 1; }
.grp { color: #666; font-size: 17px; margin-top: 4px; }
ul { margin: 0 0 4px 0; padding-left: 22px; }
li { margin: 1px 0; }
.foot { font-size: 18px; margin-top: 14px; color: #333; }
"""


def fmt(d):
    return d.strftime("%a %b %-d")


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
    days = list(CAL.class_days())
    hits = []
    for i, (label, is_quiz) in CAL.SPECIALS.items():
        if is_quiz and re.search(r"\bCh\b[^)]*\b%d\b" % ch, label):
            hits.append(f"{label.split(' (')[0]} on {fmt(days[i])}")
    return hits


def tier_lines(text):
    """'Label: a, b, c. Other: d' -> one problem per line under its label;
    a tier with no problem numbers (a sentence) stays one line."""
    if not re.search(r"\b\d{1,2}\.\d+", text):
        return f"<ul><li>{text}</li></ul>"
    out = []
    for seg in re.split(r"\.\s+(?=[A-Z])", text.strip().rstrip(".")):
        label, _, probs = seg.partition(":")
        if not probs:
            label, probs = "", seg
        lis = "".join(f"<li>{x.strip()}</li>" for x in probs.split(",") if x.strip())
        out.append((f"<div class=grp>{label.strip()}</div>" if label else "") + f"<ul>{lis}</ul>")
    return "".join(out)


def slide(ch, days, whws):
    h = [f"<!doctype html><meta charset=utf-8><title>Ch {ch} card</title><style>{CSS}</style>",
         "<div class=slide>", f"<h1>Chapter {ch}: {TITLES[ch]}</h1>",
         "<h2>Class days and PCCIs (on paper, at the start of class)</h2><table>"]
    for d, topic, reading in days:
        pcci = CAL.PCCI.get(d, "") or "none"
        h.append(f"<tr><td class=day>{fmt(d)}</td><td>{topic} <span style='color:#666'>({reading})</span></td>"
                 f"<td><b>PCCI:</b> {pcci}</td></tr>")
    h.append("</table>")
    h.append("<h2>Written homework drawing on this chapter</h2>")
    for hw, due, covers, warm, ess, depth in whws:
        comp = " (plus the required Python problem)" if hw in CHK.COMPUTATIONAL else ""
        h.append(f"<div class=hw><span class=name>WHW{hw:02d}</span>, due {fmt(due)} 10:00 PM{comp}. Covers {covers}."
                 f"<div class=tiers>"
                 f"<div><span class=tier>Warm-up</span>{tier_lines(warm)}</div>"
                 f"<div><span class=tier>Essentials</span>{tier_lines(ess)}</div>"
                 f"<div><span class=tier>Depth</span>{tier_lines(depth)}</div>"
                 f"</div></div>")
    q = quizzes_for(ch)
    h.append("<div class=foot>" + ("; ".join(q) + "." if q else "Not on a quiz.") + "</div>")
    h.append("</div>")
    return "\n".join(h) + "\n"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    days, whws = chapter_days(), whws_by_chapter()
    links = []
    for ch in sorted(set(days) | set(whws)):
        (OUT / f"Ch{ch:02d}.html").write_text(slide(ch, days.get(ch, []), whws.get(ch, [])))
        first = fmt(days[ch][0][0]) if days.get(ch) else "no class day"
        links.append(f"<li><a href=Ch{ch:02d}.html>Chapter {ch}: {TITLES[ch]}</a> ({first})</li>")
    (OUT / "index.html").write_text(
        "<!doctype html><meta charset=utf-8><title>PHY 210 chapter cards</title>"
        "<body style='font-family:Helvetica,Arial,sans-serif;padding:24px'>"
        "<h1>PHY 210 F2026 chapter-opening cards</h1>"
        "<p>Generated by make_chapter_slides.py from the calendar generator. Open one, screenshot the card, paste into the deck.</p>"
        "<ul>" + "\n".join(links) + "</ul></body>\n")
    print(f"wrote {len(links)} chapter cards to {OUT}")


if __name__ == "__main__":
    main()

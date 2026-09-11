"""Active-learning totals and semester roll-up for the prep packs (PHY 210).

Each `00-prep-notes.md` carries ONE timed plan: a `## Plan (75 min)`
section whose markdown table (Start, Stop, Min, Mode, What happens) is
the single source of truth for the day. This script validates every
table, rewrites that pack's `Totals:` line in place, and regenerates
`ACTIVE-LEARNING.md` at the prep-pack root. Rerun after editing any
plan:

    python make_active_learning.py

Both the `Totals:` lines and `ACTIVE-LEARNING.md` are generated; edit
the plan tables, never the derived numbers.
"""
import datetime
import re
import sys
from pathlib import Path

PACKS = Path.home() / "coding/courses/MathematicalPhysics/private/F2026PrepPacks"
COURSE = "PHY 210"
MODES = ["Active", "Interactive", "Lecture", "Logistics"]
PERIOD = 75
# Wall-clock class start by weekday (Mon=0), from the syllabus.
CLASS_START = {0: 9 * 60 + 25, 2: 9 * 60 + 25, 4: 9 * 60 + 25}   # MWF 9:25


def to_minutes(text):
    """'1:40' or '9:25' -> minutes since midnight; hours below 8 are PM."""
    h, m = (int(x) for x in text.split(":"))
    return (h + 12 if h < 8 else h) * 60 + m


def clock(minutes):
    h = minutes // 60
    return f"{h - 12 if h > 12 else h}:{minutes % 60:02d}"


def fail(msg):
    sys.exit(f"make_active_learning.py: {msg}")


def pack_files():
    """[(class_no, date, path)] for every NN-YYYY-MM-DD-* pack, in order."""
    out = []
    for d in sorted(PACKS.iterdir()):
        m = re.match(r"(\d\d)-(\d{4}-\d\d-\d\d)-", d.name) if d.is_dir() else None
        if m:
            out.append((int(m.group(1)), m.group(2), d / "00-prep-notes.md"))
    return out


def plan_rows(lines, path):
    """Parse the Plan table into [(start, stop, min, mode)], minutes since midnight."""
    try:
        start = next(i for i, l in enumerate(lines) if l.strip() == "## Plan (75 min)")
    except StopIteration:
        fail(f"{path}: no '## Plan (75 min)' section")
    body = [l for l in lines[start:] if l.startswith("|")]
    if len(body) < 3:
        fail(f"{path}: no Plan table under '## Plan (75 min)'")
    rows = []
    for line in body[2:]:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 5:
            fail(f"{path}: plan row has {len(cells)} columns, want 5: {line.strip()}")
        try:
            a, b, m = to_minutes(cells[0]), to_minutes(cells[1]), int(cells[2])
        except ValueError:
            fail(f"{path}: Start/Stop must be wall-clock h:mm and Min an integer: {line.strip()}")
        rows.append((a, b, m, cells[3]))
    return rows


def check_rows(rows, path, date):
    weekday = datetime.date.fromisoformat(date).weekday()
    if weekday not in CLASS_START:
        fail(f"{path}: {date} is not a class weekday")
    prev = CLASS_START[weekday]
    for a, b, m, mode in rows:
        where = f"{path}: row {clock(a)}-{clock(b)}"
        if a != prev:
            fail(f"{where}: starts at {clock(a)}, previous row stops at {clock(prev)}")
        if m != b - a:
            fail(f"{where}: Min {m} != Stop - Start ({b - a})")
        if m > 15:
            fail(f"{where}: Min {m} exceeds the 15-minute cap")
        if mode not in MODES:
            fail(f"{where}: unknown Mode {mode!r}; want one of {', '.join(MODES)}")
        prev = b
    if prev != CLASS_START[weekday] + PERIOD:
        fail(f"{path}: last Stop is {clock(prev)}, want {clock(CLASS_START[weekday] + PERIOD)}")


def longest_stretch(rows):
    """Longest run of consecutive non-Active minutes: (minutes, start, stop).
    Smith's norm is no more than 15 instructor-led minutes at a time."""
    best, cur, start = (0, None, None), 0, None
    for a, b, m, mode in rows + [(None, None, 0, "Active")]:
        if mode != "Active":
            if cur == 0:
                start = a
            cur += m
            end = b
        else:
            if cur > best[0]:
                best = (cur, start, end)
            cur = 0
    return best


def totals(rows):
    return {mode: sum(m for _, _, m, md in rows if md == mode) for mode in MODES}


def totals_line(t):
    pct = round(100 * t["Active"] / PERIOD)
    return (f"Totals: Active {t['Active']} min ({pct}%), "
            f"Interactive {t['Interactive']}, Lecture {t['Lecture']}, "
            f"Logistics {t['Logistics']}, of {PERIOD}.")


def rewrite_totals(path, lines, line):
    for i, l in enumerate(lines):
        if l.startswith("Totals:"):
            lines[i] = line
            path.write_text("\n".join(lines) + "\n")
            return
    fail(f"{path}: no 'Totals:' line under the Plan table")


def topic(lines, path):
    h1 = next((l for l in lines if l.startswith("# ")), None)
    if h1 is None:
        fail(f"{path}: no H1 title line")
    return h1.lstrip("# ").split(" -- ")[-1].strip()


def cheapest_raise(lines, path):
    """The 'Cheapest raise:' paragraph, joined into one line."""
    for i, l in enumerate(lines):
        if l.startswith("Cheapest raise:"):
            para = [l]
            for nxt in lines[i + 1:]:
                if not nxt.strip():
                    break
                para.append(nxt.strip())
            text = " ".join(para)[len("Cheapest raise:"):].strip()
            return text[:1].upper() + text[1:]
    fail(f"{path}: no 'Cheapest raise:' line")


def render_table(header, rows):
    widths = [max(len(r[i]) for r in [header] + rows) for i in range(len(header))]
    def row(cells):
        return "| " + " | ".join(c.ljust(w) for c, w in zip(cells, widths)) + " |"
    return [row(header), row(["-" * w for w in widths])] + [row(r) for r in rows]


def header_lines():
    return [
        f"# Active learning in {COURSE}, Fall 2026",
        "",
        "GENERATED by SyllabusAndFirstDay/2026/make_active_learning.py from the",
        "`## Plan (75 min)` table in each pack's `00-prep-notes.md`, which is the",
        "single source of truth for the day. The script also writes each pack's",
        "`Totals:` line. Rerun it after editing any plan; do not edit the totals",
        "or this file by hand.",
        "",
        "## The four modes",
        "",
        "- **Active** -- students are doing the work: board work in groups,",
        "  think-pair-share, four-color voting-card polls, in-class work time,",
        "  notebook/laptop work, students presenting their own boards.",
        "- **Interactive** -- instructor-led derivation or explanation that is",
        "  explicitly elicited (questions to the room, predictions before the",
        "  reveal), but the instructor holds the pen.",
        "- **Lecture** -- instructor presents; students listen or copy.",
        "- **Logistics** -- announcements, syllabus, collection without",
        "  discussion, transitions.",
        "",
        "## Rules the tables follow",
        "",
        "1. Start/Stop are wall-clock times; rows run contiguously from the",
        "   class start (syllabus) for 75 minutes, Min = Stop - Start, and no row",
        "   exceeds 15 minutes; the script hard-fails otherwise.",
        "   The 'Longest non-Active' column is the longest run of back-to-back",
        "   Lecture / Interactive / Logistics minutes; Smith's norm is no more",
        "   than 15 instructor-led minutes at a time, so a '!' marks a day over it.",
        "   Day 1 is an accepted exception: syllabus and introductions are",
        "   instructor-led by nature; splitting them with a short pair task is the",
        "   aspiration. The standing claim is: from class 2 onward, no plan asks",
        "   students to sit for more than 15 minutes.",
        "2. Every row's minutes land in exactly one mode. A chunk that mixes",
        "   modes is split into rows at the plan's own sentence boundaries, and",
        "   the split is named in that day's Ambiguities line.",
        "3. Ambiguous text is classified conservatively: Active only where the",
        "   plan says students do it and names the structure (pairs, groups of",
        "   three at the boards, voting cards, individual writing). Whole-class",
        "   question-and-answer is Interactive, not Active.",
        "4. Conditional activity (\"if the room is awake\") is credited to Active",
        "   but flagged, because it is also what the droppable tail eats first.",
        "5. Percentages are Active minutes over 75, rounded.",
        "",
        "Packs beyond the ones built so far get their table when the pack is",
        "built; there is nothing to count before then.",
        "",
        "## Per class day",
        "",
    ]


def main():
    table_rows, raises, sums, days, over = [], [], {m: 0 for m in MODES}, 0, 0
    for n, date, path in pack_files():
        if not path.exists():
            fail(f"{path}: missing 00-prep-notes.md")
        lines = path.read_text().splitlines()
        rows = plan_rows(lines, path)
        check_rows(rows, path, date)
        t = totals(rows)
        rewrite_totals(path, lines, totals_line(t))
        ls = longest_stretch(rows)
        over += ls[0] > 15
        table_rows.append([f"{n:02d}", date, topic(lines, path)]
                          + [str(t[m]) for m in MODES]
                          + [f"{round(100 * t['Active'] / PERIOD)}%",
                             f"{ls[0]} ({clock(ls[1])}-{clock(ls[2])}){' !' if ls[0] > 15 else ''}"])
        raises.append(f"{n}. **Class {n:02d} ({date}).** {cheapest_raise(lines, path)}")
        for m in MODES:
            sums[m] += t[m]
        days += 1
    out = header_lines()
    out += render_table(["Class", "Date", "Topic"] + MODES + ["% Active", "Longest non-Active"], table_rows)
    total = PERIOD * days
    out += ["", "Semester so far: " + ", ".join(
        f"{m} {sums[m]} min ({round(100 * sums[m] / total)}%)" for m in MODES)
        + f", of {total} min across {days} class days. Days with an instructor-led"
        f" stretch over 15 minutes (Lecture + Interactive + Logistics back to back): {over} of {days}.", "",
        "## Cheapest raises", "",
        "The one change to each day's plan that buys the most Active minutes.",
        ""] + raises
    (PACKS / "ACTIVE-LEARNING.md").write_text("\n".join(out) + "\n")
    print(f"checked {days} packs, rewrote their Totals lines, wrote ACTIVE-LEARNING.md")


if __name__ == "__main__":
    main()

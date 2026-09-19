"""Active-learning totals and semester roll-up for the prep packs (PHY 210).

Each `00-prep-notes.md` carries ONE timed plan: a `## Plan (75 min)`
section whose markdown table (Start, Stop, Min, Mode, [Source,] What
happens) is the single source of truth for the day. The Source column is
optional (added 2026-09-17): a terse pointer to where the row's material
comes from, in the playbook's notation (210: M = Manbir's pages, G =
Gillian's slides, FF = Felder & Felder book pages, GF <tag> = a named
Gary Felder file, e.g. GF key, GF plan01 D8; 317: T = Taylor book pages, W =
Will's slides; **N** = new material in neither), e.g. `M6-7, G4-8,10`. This script validates every
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
TWO_STAR_MIN = 20   # minutes; playbook section 4, measured 2026-09-14 and 2026-09-18
CSS = '''
body { background: #fff; margin: 0; padding: 10px; color: #000;
       font-family: Helvetica, Arial, sans-serif; font-variant-numeric: tabular-nums; }
.card { width: 100%; box-sizing: border-box; }
header { font-size: 15px; margin: 0 0 6px 0; }
header .name { color: #333; margin-left: 8px; }
header .when { color: #555; margin-left: 8px; }
table { border-collapse: collapse; width: 100%; font-size: 13.5px; line-height: 1.25; }
th, td { border: 1px solid #888; padding: 3px 6px; vertical-align: top; text-align: left; }
th { background: #e8e8e8; font-weight: bold; font-size: 12px; }
td.time { white-space: nowrap; }
td.min { text-align: right; }
td.src { white-space: nowrap; font-size: 12px; }
tr.active td { background: #dff0d8; }
tr.interactive td { background: #fff3cd; }
tr.lecture td { background: #f8d7da; }
tr.logistics td { background: #e2e3e5; }
footer { margin-top: 5px; font-size: 12px; color: #333; }
.frame { font-size: 14px; margin: 0 0 8px 0; line-height: 1.3; }
'''
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
    """Parse the Plan table into [(start, stop, min, mode, source, text)], minutes since midnight.
    Source is "" when the table has no Source column."""
    try:
        start = next(i for i, l in enumerate(lines) if l.strip() == "## Plan (75 min)")
    except StopIteration:
        fail(f"{path}: no '## Plan (75 min)' section")
    body = [l for l in lines[start:] if l.startswith("|")]
    if len(body) < 3:
        fail(f"{path}: no Plan table under '## Plan (75 min)'")
    header = [c.strip() for c in body[0].strip().strip("|").split("|")]
    if header[:4] != ["Start", "Stop", "Min", "Mode"] or header[-1] != "What happens":
        fail(f"{path}: plan header must be Start | Stop | Min | Mode | [Source |] What happens: {body[0].strip()}")
    has_src = header == ["Start", "Stop", "Min", "Mode", "Source", "What happens"]
    want = 6 if has_src else 5
    if not has_src and len(header) != 5:
        fail(f"{path}: plan header has {len(header)} columns; want 5 or 6 (with Source): {body[0].strip()}")
    rows = []
    for line in body[2:]:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != want:
            fail(f"{path}: plan row has {len(cells)} columns, want {want}: {line.strip()}")
        try:
            a, b, m = to_minutes(cells[0]), to_minutes(cells[1]), int(cells[2])
        except ValueError:
            fail(f"{path}: Start/Stop must be wall-clock h:mm and Min an integer: {line.strip()}")
        src = cells[4] if has_src else ""
        rows.append((a, b, m, cells[3], src, cells[-1]))
    return rows


def check_rows(rows, path, date):
    weekday = datetime.date.fromisoformat(date).weekday()
    if weekday not in CLASS_START:
        fail(f"{path}: {date} is not a class weekday")
    prev = CLASS_START[weekday]
    for a, b, m, mode, _s, _ in rows:
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
    # Two-star budget guard (playbook section 4; 2.4 took 25 min on
    # 2026-09-14, 2.54(a) overran on 2026-09-18): a Taylor "(**)" problem
    # gets 20+ minutes across the day's rows, split over two rows if the
    # 15-minute row cap demands it. Warn, do not fail: Michael may accept a
    # scoped-down two-star deliberately, and says so in Ambiguities.
    for a, b, m, mode, _s, text in rows:
        for prob in re.findall(r"(\d+\.\d+)\s*\(\*\*\)", text):
            total = sum(r[2] for r in rows if r[3] == "Active" and re.search(rf"\b{re.escape(prob)}\b", r[5]))
            if total < TWO_STAR_MIN:
                print(f"WARNING {path}: {prob} (**) has {total} Active min across the day; "
                      f"playbook budget is {TWO_STAR_MIN}+")


def longest_stretch(rows):
    """Longest run of consecutive non-Active minutes: (minutes, start, stop).
    Smith's norm is no more than 15 instructor-led minutes at a time."""
    best, cur, start = (0, None, None), 0, None
    for a, b, m, mode, _s, _ in rows + [(None, None, 0, "Active", "", "")]:
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


def frame_text(lines):
    """The 'Frame:' paragraph of the plan preamble (up to the next blank line)."""
    out, on = [], False
    for l in lines:
        if l.startswith("Frame:"):
            on = True; out.append(l[len("Frame:"):].strip()); continue
        if on:
            if not l.strip() or l.startswith("|") or l.startswith("#"):
                break
            out.append(l.strip())
    return " ".join(out)


def droppable(lines):
    for l in lines:
        if l.startswith("Droppable tail:"):
            return l[len("Droppable tail:"):].strip()
    return ""


def html_escape(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def bold(s):
    """Markdown **x** -> <b>x</b> (used for the **N** = new-material marker)."""
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)


def write_plan_html(path, n, date, title, rows, t, tail, frame=""):
    has_src = any(src for _, _, _, _, src, _ in rows)
    """One-slide card of the day's plan, derived from the table (never edit
    the HTML; edit the table and rerun). Sized for a landscape GoodNotes page."""
    out = [f"<!doctype html><meta charset=utf-8><title>{COURSE} class {n:02d} plan</title><style>{CSS}</style>",
           "<div class=card>",
           f"<header><b>{COURSE} class {n:02d}</b><span class=name>{html_escape(title)}</span>"
           f"<span class=when>{datetime.date.fromisoformat(date).strftime('%a %b %-d')}, {clock(rows[0][0])}-{clock(rows[-1][1])}</span></header>",
           (f"<p class=frame><b>Frame.</b> {html_escape(frame)}</p>" if frame else ""),
           "<table><tr><th>Time</th><th>Min</th><th>Mode</th>"
           + ("<th>Source</th>" if has_src else "") + "<th>What happens</th></tr>"]
    for a, b, m, mode, src, text in rows:
        cls = f" class={mode.lower()}"
        srccell = ("<td class=src>" + bold(html_escape(src)) + "</td>") if has_src else ""
        out.append(f"<tr{cls}><td class=time>{clock(a)}-{clock(b)}</td><td class=min>{m}</td>"
                   f"<td class=mode>{mode}</td>{srccell}<td>{html_escape(text).replace('&lt;br&gt;', '<br>')}</td></tr>")
    pct = round(100 * t["Active"] / PERIOD)
    out.append("</table>")
    out.append(f"<footer>Active {t['Active']} min ({pct}%), Interactive {t['Interactive']}, Lecture {t['Lecture']}, "
               f"Logistics {t['Logistics']}. Droppable tail: {html_escape(tail) or 'none'}</footer></div>")
    (path.parent / "02-plan.html").write_text("\n".join(out) + "\n")


def totals(rows):
    return {mode: sum(m for _, _, m, md, _s, _ in rows if md == mode) for mode in MODES}


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
        "  think-pair-share, voting-card polls, in-class work time,",
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
        write_plan_html(path, n, date, topic(lines, path), rows, t, droppable(lines), frame_text(lines))
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

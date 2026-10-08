"""Per-class-day review checklists for the prep packs (PHY 210).

Michael's standing rule (2026-09-07): every PCCI and every in-class
problem must be reviewed BEFORE the class it appears in, and every
homework SOLUTIONS must be finalized and hand-reviewed by Michael before
the set goes live (ideal) and no later than the first class after it
goes live (mandatory: students may ask about it in that class)
(assigned = the day the Moodle WHW becomes visible, 10.5 days before it
is due). This script enumerates the PCCI and the WHW tiers per day from
the calendar generator (PCCI, WHWS, the Friday/override due-date rule),
so the lists stay correct when assignments change. In-class problems for
210 are not in the generator (they come from the S26 decks and Berger's
sets, chosen per pack), so each checklist reads them from the pack's own
notes (the `## In-class problems` section; packnotes.Notes). Rerun after
any generator edit or pack-notes edit:

    python make_review_checklists.py

Writes `review-checklist.md` into every existing prep-pack folder's build
directory (packnotes.layout()["build"]: `.build/`, or `_gen/` in old-layout
packs) and `REVIEW-SCHEDULE.md` at the prep-pack root. Generated files; do
not edit.
"""
import re
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import make_fall2026_calendar as CAL  # noqa: E402
sys.path.insert(0, str(Path.home() / "coding/courses/shared"))
import coverage_gate as GATE              # noqa: E402
import packnotes as PN                    # noqa: E402

# Coverage gate (2026-10-01): a week before each set goes live, the checklist asks for
# /coverage-check; at go-live it prints the mechanical gate (verdict on file, links exist,
# notebook linked when the set needs a computer). See shared/coverage_gate.py.
DESCRIPTIONS = GATE.description_blocks(Path.home() / "coding/courses/MathematicalPhysics/private/MoodleBuild/whw-descriptions.html")
SOLUTIONS = Path.home() / "coding/courses/MathematicalPhysics/private/Solutions"

PACKS = Path.home() / "coding/courses/MathematicalPhysics/private/F2026PrepPacks"
AVAILABLE_DAYS_BEFORE = 10.5          # build_assignments.py
FIRST_CLASS = date(2026, 9, 9)

# ------------------------------------------------------------ logistics
# The bring / set-up list is checklist material (a checkbox, not prose),
# so it lives here as data rather than in the hand-written prep notes.
EVERY_DAY = [
    "iPad",
    "Voting cards",
]
# Only on days whose pack HAS a board sheet (has_board_sheet); it used to be in EVERY_DAY and so
# told Michael to print a sheet on days that have none, quiz days included (fixed 2026-10-05).
BOARD_SHEET_ITEM = "Print the board sheet (and the PCCI page if it goes to the boards)"
# date -> items specific to that day
DAY_LOGISTICS = {
    date(2026, 9, 9): ["Printed photo roster (private/Roster/PHY210-F2026-roster.pdf)",
                       "Printed syllabus, one per student + spares",
                       "Printed math pretest (Pretest/MathPretest-student.pdf), one per student",
                       "Extra copies of Felder and Felder",
                       "Extra copies of The Mathematics Companion",
                       "PRINT the voting cards, one set per student (shared/VotingCardLandscape.pdf)"],
    date(2026, 9, 11): ["Chalk and whiteboard markers (board work: mass-spring, bacteria, rabbits)"],
    # One version per quiz (Michael, 2026-09-22): S26 alternated two forms
    # because they ran two sections; we run one, so there is nothing to
    # alternate. Applies to all three quizzes.
    date(2026, 9, 25): ["Quiz 1: printed copies + spares; per-problem score sheet"],
    date(2026, 9, 28): ["iPad with the folio keyboard (AirPlay as usual) for the Python onboarding class; test the GitHub-download-to-hub-upload step in Safari beforehand; students bring laptops"],
    # Quiz hand-backs (Michael, 2026-10-04): the redo is a single PDF on Moodle (syllabus), due
    # "one week after the hand-back" rounded to the next class day.
    date(2026, 10, 5): ["Hand back the graded Quiz 1 papers; redos (check-minus and X problems: "
                        "a correct solution plus the reflection) go on Moodle as one PDF, due Wed Oct 14 at the start of class "
                        "(the 'Quiz 1 redo' item). Scores unhide on Moodle at 11:00."],
    date(2026, 10, 23): ["Quiz 2: printed copies + spares; per-problem score sheet"],
    date(2026, 10, 26): ["Hand back the graded Quiz 2 papers; redos go on Moodle as one PDF, due Mon Nov 2 at the start "
                         "of class. The 'Quiz 2 redo' Moodle item must already exist (build_add_210.py quiz2-redo, a "
                         "restore-only merge); edit its dates if this hand-back moved."],
    date(2026, 11, 20): ["Quiz 3: printed copies + spares; per-problem score sheet"],
    date(2026, 11, 23): ["Hand back the graded Quiz 3 papers; redos go on Moodle as one PDF, due Mon Nov 30 at the start "
                         "of class (no class Nov 25/27). The 'Quiz 3 redo' Moodle item must already exist (build_add_210.py "
                         "quiz3-redo); edit its dates if this hand-back moved."],
}
# WHWs carrying a required computational problem (decided 2026-08-28;
# the problem text lives in private/MoodleBuild/whw-descriptions.html and
# SyllabusAndFirstDay/2026/ComputationalProblems.md).
COMPUTATIONAL = {2, 4, 5, 6, 8, 9, 10, 12, 13}


def fmt(d):
    return d.strftime("%a %b %-d")


def class_rows():
    days = list(CAL.class_days())
    # The calendar build()'s guards, repeated here because the consumers of class_rows() never run
    # build(): an extra CONTENT row would silently drop off the end, a misdated quiz would be
    # treated as content (too FEW rows is loud: next() raises StopIteration).
    assert len(CAL.CONTENT) + len(CAL.QUIZZES) == len(days), (
        f"{len(CAL.CONTENT)} content + {len(CAL.QUIZZES)} quizzes for {len(days)} class meetings")
    assert all(d in days for d in CAL.QUIZZES), "quiz on a non-class day"
    assert all(d in days for d in CAL.LAPTOP_DAYS), "LAPTOP_DAYS names a non-class day"
    content = iter(CAL.CONTENT)
    rows = []
    for i, d in enumerate(days):
        if d in CAL.QUIZZES:          # keyed by date since 2026-10-04 (as 317's EXAMS)
            rows.append((i + 1, d, CAL.QUIZZES[d], "", True))
        else:
            topic, reading = next(content)
            rows.append((i + 1, d, topic, reading, False))
    return rows


def whw_events():
    days = list(CAL.class_days())
    out, hw_no = [], 0
    tiers = {w[0]: w for w in CAL.WHWS}
    for i, d in enumerate(days):
        if d.weekday() == 4 and i > 0:
            hw_no += 1
            due = CAL.WHW_DUE_OVERRIDE.get(hw_no, d)
            vis = max(due - timedelta(days=AVAILABLE_DAYS_BEFORE), FIRST_CLASS)
            out.append((hw_no, vis, due, tiers[hw_no]))
    return out


def has_board_sheet(pack):
    """A '## Board sheet:' section in the notes (what make_pack_html renders) or a 'Board sheet*'
    file anywhere in the pack (predecessors/ PDFs, old-layout .md files)."""
    if pack is None:
        return False
    notes = PN.layout(pack)["notes"]
    if notes.exists() and PN.Notes(notes).heading(r"^board sheet\s*:"):
        return True
    return any(pack.rglob("Board sheet*"))


def inclass_line(pack):
    """The in-class review line: the problems in the pack's `## In-class problems` section."""
    if pack is None:
        return "- [ ] In-class / group problems today: no prep pack yet, so none to list"
    notes = PN.layout(pack)["notes"]
    where = f"this pack's `{notes.relative_to(pack)}` plan"          # old-format notes
    probs = []
    if notes.exists():
        N = PN.Notes(notes)
        if not N.old_format:
            where = f"the `## In-class problems` section of `{notes.relative_to(pack)}`"
            probs = N.inclass_problems()
    line = f"- [ ] In-class / group problems today: every problem named in {where}"
    if probs:
        line += " (numbered there: " + ", ".join(f"**{p}**" for p in probs) + ")"
    return line + ", worked yourself first"


def checklist(row, all_rows, whws, pack=None):
    n, d, topic, reading, is_quiz = row
    lines = [f"# Review checklist -- class {n:02d}, {fmt(d)} -- {topic}", "",
             "GENERATED by SyllabusAndFirstDay/2026/make_review_checklists.py from",
             "the calendar generator; rerun it after any change to PCCIs, WHWs, or",
             "the logistics table. Do not edit by hand.",
             "CHECKLIST = everything that is a checkbox (review items, deadlines,",
             "bring/set-up). PREP NOTES = the judgment (sources, errata, pacing).", ""]
    lines += ["## Before class (review these yourself first)", ""]
    pcci = CAL.PCCI.get(d)
    lines.append(f"- [ ] PCCI due today: **{pcci}**" if pcci else "- [ ] PCCI due today: none")
    if is_quiz:
        lines.append("- [ ] QUIZ DAY: the instrument worked through end to end,"
                     " every version you are printing")
    else:
        lines.append(inclass_line(pack))
    later = [r for r in all_rows if r[1] > d and CAL.PCCI.get(r[1])]
    if later:
        nd = later[0][1]
        lines.append(f"- [ ] Next PCCI (on the Moodle schedule, due {fmt(nd)}; review it now): {CAL.PCCI[nd]}")
    lines += ["", "## Homework (solutions finalized + hand-reviewed: ideally before go-live, MANDATORY by the first class after)", ""]
    next_class = min([r[1] for r in all_rows if r[1] > d], default=None)
    prev_class = max([r[1] for r in all_rows if r[1] < d], default=None)
    any_hw = False
    class_dates = [r[1] for r in all_rows]
    for hw, vis, due, *_ in whws:
        if vis >= GATE.GATE_START and GATE.coverage_day(vis, class_dates) == d and vis > d:
            any_hw = True
            lines += GATE.checklist_lines(f"WHW{hw:02d}", vis, due, d, DESCRIPTIONS.get(hw, ""),
                                          SOLUTIONS / f"WHW{hw:02d}", hw in COMPUTATIONAL, fmt)
    for hw, vis, due, (wn, covers, warm, ess, depth) in whws:
        goes_live_now = (prev_class is None and vis <= d) or (prev_class is not None and prev_class < vis <= d)
        if goes_live_now:
            any_hw = True
            lines += [f"- [ ] **WHW{hw:02d} goes live {fmt(vis)}: solutions FINALIZED and hand-reviewed, "
                      f"MANDATORY by class today** (due {fmt(due)}). Covers {covers}.",
                      f"      Warm-up: {warm}",
                      f"      Essentials: {ess}",
                      f"      Depth: {depth}",
                      f"      Packet to review: private/Solutions/WHW{hw:02d}/WHW{hw:02d}-solutions.pdf"
                      + ("" if (SOLUTIONS / f"WHW{hw:02d}" / f"WHW{hw:02d}-solutions.pdf").exists() else " (NOT FOUND: write it first)")]
            if vis >= GATE.GATE_START:
                lines += GATE.golive_lines(f"WHW{hw:02d}", DESCRIPTIONS.get(hw, ""), SOLUTIONS / f"WHW{hw:02d}", hw in COMPUTATIONAL)
            if hw in COMPUTATIONAL:
                lines.append(f"      Computational: the required Python problem for WHW{hw:02d}"
                             " (ComputationalProblems.md) -- run it end to end on jupyterhub")
        if next_class is not None and d < vis <= next_class:
            any_hw = True
            lines += [f"- [ ] WHW{hw:02d} goes live {fmt(vis)}, before the next class: finalize and "
                      f"hand-review its solutions NOW (the ideal deadline). Covers {covers}.",
                      f"      Warm-up: {warm}", f"      Essentials: {ess}", f"      Depth: {depth}",
                      f"      Packet to review: private/Solutions/WHW{hw:02d}/WHW{hw:02d}-solutions.pdf"
                      + ("" if (SOLUTIONS / f"WHW{hw:02d}" / f"WHW{hw:02d}-solutions.pdf").exists() else " (NOT FOUND: write it first)")]
        if due == d:
            any_hw = True
            lines.append(f"- WHW{hw:02d} is DUE today 10:00 PM.")
    for ed, label in CAL.EXTRA_DUE.items():
        if ed == d:
            any_hw = True
            lines.append(f"- {label} today.")
    if not any_hw:
        lines.append("- nothing new goes live or comes due today")
    # ---- bring / set up
    lines += ["", "## Bring / set up", ""]
    if d in CAL.LAPTOP_DAYS:
        lines.append("- [ ] **Students bring LAPTOPS today (tagged on the Moodle schedule)**")
    for item in DAY_LOGISTICS.get(d, []):
        lines.append(f"- [ ] **{item}**")
    for item in EVERY_DAY:
        if any(item.lower() in x.lower() for x in DAY_LOGISTICS.get(d, [])):
            continue          # a bold day-specific line already covers it
        lines.append(f"- [ ] {item}")
    if has_board_sheet(pack):
        lines.append(f"- [ ] {BOARD_SHEET_ITEM}")
    return "\n".join(lines) + "\n"


def main():
    rows = class_rows()
    whws = whw_events()
    packs = {int(p.name[:2]): p for p in PACKS.iterdir()
             if p.is_dir() and re.match(r"\d\d-", p.name)}
    # Guard (2026-10-04): a pack's number must be the calendar's number for its date. Otherwise a
    # lost meeting (Mountain Day) sends class N's checklist into another day's folder.
    by_date = {r[1].isoformat(): r[0] for r in rows}
    for n, p in sorted(packs.items()):
        assert by_date.get(p.name[3:13]) == n, (
            f"pack {p.name}: the calendar numbers {p.name[3:13]} as class {by_date.get(p.name[3:13])}, the folder says {n}")
    written = 0
    sched = ["# Review schedule, whole semester (PHY 210 F2026)", "",
             "GENERATED by make_review_checklists.py; rerun after any generator edit.",
             "Rule: PCCIs and in-class problems reviewed BEFORE the class; WHW solutions",
             "finalized and hand-reviewed before the set goes live (ideal), MANDATORY by",
             "the first class after it goes live.", ""]
    for row in rows:
        n = row[0]
        text = checklist(row, rows, whws, packs.get(n))
        if n in packs:
            build = PN.layout(packs[n])["build"]
            build.mkdir(exist_ok=True)
            (build / "review-checklist.md").write_text(text)
            written += 1
        body = text[text.index("## Before class"):]          # drop the title + header note
        sched += [f"## Class {n:02d} -- {fmt(row[1])} -- {row[2]}", "", body.strip(), ""]
    (PACKS / "REVIEW-SCHEDULE.md").write_text("\n".join(sched))
    print(f"wrote REVIEW-SCHEDULE.md ({len(rows)} days) and {written} pack checklists")


if __name__ == "__main__":
    main()

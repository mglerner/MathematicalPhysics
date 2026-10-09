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
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import make_fall2026_calendar as CAL  # noqa: E402
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "shared"))
import courses as C                       # noqa: E402
import coverage_gate as GATE              # noqa: E402
import fall2026_calendar as TERM          # noqa: E402
import packnotes as PN                    # noqa: E402
import review_checklists as RC            # noqa: E402

# Coverage gate (2026-10-01): a week before each set goes live, the checklist asks for
# /coverage-check; at go-live it prints the mechanical gate (verdict on file, links exist,
# notebook linked when the set needs a computer). See shared/coverage_gate.py.
DESCRIPTIONS = GATE.description_blocks(C.moodlebuild("210") / "whw-descriptions.html")
SOLUTIONS = C.private("210") / "Solutions"


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
# the problem text lives in private/MoodleBuild/make_whw_descriptions.py's COMP
# table, which writes whw-descriptions.html, and in
# SyllabusAndFirstDay/2026/ComputationalProblems.md; check_whw_descriptions.py
# asserts COMP's keys are this set).
COMPUTATIONAL = {2, 4, 5, 6, 8, 9, 10, 12, 13}


fmt = RC.fmt


def class_rows():
    """[(class_no, date, topic, reading, is_quiz)] from the calendar's rows() (flex days and slips applied;
    a flex day is a content row with no reading)."""
    return [(r["n"], r["date"], r["topic"], r["reading"], r["kind"] == "assessment") for r in CAL.rows()]


def whw_events():
    """[(hw, visible date, due date, WHWS tier row)], due dates from CAL.whw_due_dates() (one per
    Friday after the first class; WHW_DUE_OVERRIDE wins)."""
    tiers = {w[0]: w for w in CAL.WHWS}
    return [(hw, max(due - timedelta(days=TERM.AVAILABLE_DAYS_BEFORE), TERM.FIRST_DAY), due, tiers[hw])
            for hw, due in CAL.whw_due_dates().items()]


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


def whw_detail(hw, tier):
    """(covers, the lines under a WHW's go-live line): its three tiers and the solutions packet."""
    _wn, covers, warm, ess, depth = tier
    return covers, [f"      Warm-up: {warm}", f"      Essentials: {ess}", f"      Depth: {depth}",
                    f"      Packet to review: private/Solutions/WHW{hw:02d}/WHW{hw:02d}-solutions.pdf"
                    + ("" if (SOLUTIONS / f"WHW{hw:02d}" / f"WHW{hw:02d}-solutions.pdf").exists() else " (NOT FOUND: write it first)")]


def computational_line(hw):
    if hw not in COMPUTATIONAL:
        return []
    return [f"      Computational: the required Python problem for WHW{hw:02d}"
            " (ComputationalProblems.md) -- run it end to end on jupyterhub"]


def checklist(row, all_rows, whws, pack=None):
    n, d, topic, reading, is_quiz = row
    lines = RC.header(n, d, topic, ["the calendar generator; rerun it after any change to PCCIs, WHWs, or",
                                    "the logistics table. Do not edit by hand."])
    lines += RC.before_class(d, CAL.PCCI)
    if is_quiz:
        lines.append("- [ ] QUIZ DAY: the instrument worked through end to end,"
                     " every version you are printing")
    else:
        lines.append(inclass_line(pack))
    lines += RC.next_pcci(d, all_rows, CAL.PCCI)
    lines += RC.homework(d, all_rows, whws, "WHW", whw_detail, DESCRIPTIONS, SOLUTIONS, CAL.EXTRA_DUE,
                         computational=lambda hw: hw in COMPUTATIONAL, golive_extra=computational_line)
    lines += RC.bring(d, CAL.LAPTOP_DAYS, DAY_LOGISTICS, EVERY_DAY)
    if has_board_sheet(pack):
        lines.append(f"- [ ] {BOARD_SHEET_ITEM}")
    return "\n".join(lines) + "\n"


def main():
    RC.write_all("210", class_rows(), whw_events(), checklist, "WHW")


if __name__ == "__main__":
    main()

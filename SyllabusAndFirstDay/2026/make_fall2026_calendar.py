import re
"""Generate the Fall 2026 PHY 210 (Mathematical Physics, Smith) course calendar.

Layout (2026-08-27): a single-block "Schedule" sheet with
Week | Class | Date | Topics | Reading Due | PCCI | HW Due | Exams,
written as two chunks (header row repeated) split at fall break for
the half-semester Moodle embed, plus "WHW Problem Lists" and a
"Grade Categories" sheet skeleton. The old two-side-by-side-blocks
print layout (P125 style) lives in git history before this date.
Content follows the previous Smith professor's Spring '26 PHY 210 sequence
(Felder & Felder), remapped onto the Smith Fall 2026 academic calendar.

Usage: python make_fall2026_calendar.py OUTPUT.xlsx
"""
import sys
from datetime import date, timedelta

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

# ---------------------------------------------------------------- semester
# Smith Fall 2026: classes Tue Sep 8 - Tue Dec 15.
# MWF meetings; skip Mon Oct 12 + Tue Oct 13 (autumn recess),
# Wed Nov 25 + Fri Nov 27 (Thanksgiving). Cromwell Day (Tue Nov 10) and
# the Dec 15 last-day-of-classes Tuesday don't hit a MWF pattern.
FIRST_DAY = date(2026, 9, 9)   # first MWF meeting (classes open Tue Sep 8)
LAST_DAY = date(2026, 12, 14)  # last MWF meeting
# NO_CLASS values are the calendar row's text (as in 317's generator): Mountain Day is a
# Smith holiday, not an absence, and Michael wants it to read as one.
# Mountain Day 2026 fell on Wed Sep 23 (announced that morning). This calendar was NOT
# updated at the time (317's was); found 2026-10-01. Its Felder 10.2 (linear operators) is
# DROPPED, not rescheduled: no S26 quiz or final asks about it. Its PCCI (10.1, 10.3) was
# collected from whoever had done it. Until 2026-10-04 the lost meeting kept its slot and
# class number (a cancelled "class 07"); since then class numbers count meetings HELD, as in
# 317, so Sep 25 is class 07 and the packs/logs were renumbered to match.
NO_CLASS = {
    date(2026, 9, 23): "Mountain Day!!",
    date(2026, 10, 12): "No class - Autumn recess",
    date(2026, 11, 25): "No class - Thanksgiving",
    date(2026, 11, 27): "No class - Thanksgiving",
}


def class_days():
    d = FIRST_DAY
    while d <= LAST_DAY:
        if d.weekday() in (0, 2, 4) and d not in NO_CLASS:  # M W F
            yield d
        d += timedelta(days=1)

# ------------------------------------------------------------------ content
# (topic, reading_due) per teaching slot, in the previous prof's order.
# Readings are the Felder & Felder sections being covered; the "Reading Due"
# column mirrors the P125 calendar's read-before-class convention.
#
# Quizzes are dedicated in-class days (as on the previous prof's calendar),
# keyed by DATE (not slot index, so a lost meeting cannot shift them; 317's
# EXAMS work the same way). 35 content days + 3 quiz days = 38 MWF meetings
# held (39 scheduled minus Mountain Day). The calendar is FULL: the flex day
# that absorbed snow / Mountain Day / drift was spent on Mountain Day, so
# adding anything else means displacing content.
# REBUILT 2026-10-01 (Michael approved): from Oct 2 on, each meeting is Manbir's S26 meeting as
# her section ACTUALLY delivered it (her day N and N+1 notes; Gillian's decks where Manbir's
# stop is unknown), one for one, with quiz dates fixed. Mountain Day spent the flex day (her
# snow day's twin), so there is no buffer left. Feynman (Vol II Ch 2-3) is woven into the six
# vector-calculus days instead of having a day of its own; Dec 14 is Michael's fixed finale.
QUIZZES = {
    date(2026, 9, 25): "Quiz 1 (Ch 1)",
    date(2026, 10, 23): "Quiz 2 (Ch 10, 3, 2)",
    date(2026, 11, 20): "Quiz 3 (Ch 6, 5)",
}
CONTENT = [
    ("Syllabus; SHO and overview of differential equations", "1.1-1.2"),
    ("Generating ODEs from physical situations", "1.1-1.2"),
    ("Arbitrary constants; initial conditions", "1.3"),
    ("Separation of variables", "1.5"),
    ("Guess and check", "1.6"),
    ("Linearity, homogeneity, superposition", "1.6"),
    ("Jupyter notebook exercise: ODEs in Python", "10.2"),
    ("Heaviside, Dirac delta, and the Laplace transform", "10.10"),
    ("Using Laplace transforms to solve ODEs", "10.11"),
    # Reading split moved 2026-09-19 (PCCI audit; retired ClassPlanPlaybook 6a, now shared/PrepRules.md, "The floor, and the next PCCI"): the Oct 7
    # PCCI is DE 3.4.1, so 3.4 must not be read (or taught) before Oct 7.
    # Pack 11 teaches 3.1-3.3 on Oct 5 and pack 12 teaches 3.4-3.5 on Oct 7.
    ("Complex numbers: basic properties", "3.1-3.3"),
    ("Euler's formula; complex ODEs", "3.4-3.5"),
    # Manbir's S26 meeting for each slot is in the comment (her section's actual reach).
    ("Linear approximations", "2.1-2.2"),                                   # Feb 27
    ("Maclaurin series", "2.3"),                                            # Mar 2
    # 2.6-2.7 (convergence) deliberately cut (decision 2026-08-17);
    # Appendix C is the pointed-to substitute.
    ("Taylor series; finding one series from another", "2.4-2.5 (convergence: App. C)"),  # Mar 4
    ("Properties of matrices", "6.1-6.2"),                                  # Mar 6
    ("Matrix x column; vector transformations", "6.3-6.4"),                 # Mar 9
    ("Matrix multiplication; identity and inverse", "6.5-6.6"),             # Mar 13
    ("Determinants; finding eigenvalues and eigenvectors", "6.7-6.8"),      # Mar 23
    ("Eigenvectors; the two-coupled-oscillator problem", "6.8-6.9"),        # Mar 25
    ("Setting up 1D and 2D integrals", "5.1-5.2"),                          # Mar 27
    ("Cartesian 2D integrals", "5.3-5.4"),                                  # Mar 30
    ("Polar coordinates", "5.6"),                                           # Apr 1
    ("Line integrals and surface integrals", "5.8, 5.10"),                  # Apr 3
    # S26's "practice/review" day actually taught cylindrical and spherical coordinates new.
    ("Cylindrical and spherical coordinates", "5.5, 5.7; App. D"),          # Apr 6
    ("Vector and scalar fields; potential", "8.1-8.3"),                     # Apr 8
    ("The gradient; equipotentials", "8.4"),                                # Apr 13
    ("Potential from a field; the gradient theorem; divergence and curl (Feynman)",
     "8.5-8.6; Feynman Vol II Ch 3"),                                       # Apr 15
    ("Divergence, curl, and the Laplacian; the divergence theorem",
     "8.6-8.7, 8.9; Feynman Vol II Ch 2"),                                  # Apr 17
    ("Divergence theorem; Stokes' theorem", "8.9-8.10"),                    # Apr 20
    ("Conservative vector fields", "8.11"),                                 # Apr 22
    ("Introduction to Fourier series", "9.1-9.3"),                          # Apr 24
    ("Fourier series: different periods, finite domains", "9.4"),           # Apr 27
    ("Fourier series with complex exponentials", "9.5"),                    # Apr 29
    ("Intro to PDEs: the heat equation; separation of variables",
     "11.1-11.2, 11.4"),                                                    # May 1
    # Michael's fixed finale (not in S26, which never reached Fourier transforms).
    ("Normal modes of the wave equation; Fourier transforms",
     "11.3, 9.6"),
]

# The predecessor's day for each CONTENT row, in order (Manbir's S26 meeting, as her section
# actually delivered it; see the comments on CONTENT). ONE copy, in data: the pack page links
# the Manbir-vs-Gillian comparison from it, plan_overview checks each pack against it, and a
# from-scratch build reads it to find the day's files (Manbir's are named by date but not
# uniformly: "1.26 Day 1.pdf", "2.18 notes.pdf", "4.13.pdf"; Gillian's "PHY210-March2.pdf",
# and her week-1 decks are dated one meeting later than Manbir's; look them up by hand). None = no S26 day (Michael's finale). Quiz days are in
# PREDECESSOR_ASSESSMENT, keyed by OUR date like QUIZZES, so a lost meeting cannot shift them.
# S26 Feb 9 (10.2, linear operators) was the twin of the lost Sep 23 class and has no row.
PREDECESSOR_CONTENT = [
    "2026-01-26", "2026-01-28", "2026-01-30", "2026-02-02", "2026-02-04", "2026-02-06",  # Ch 1
    "2026-02-11", "2026-02-16", "2026-02-18",                                              # Python, Laplace
    "2026-02-20", "2026-02-25",                                                            # Ch 3
    "2026-02-27", "2026-03-02", "2026-03-04",                                              # Ch 2
    "2026-03-06", "2026-03-09", "2026-03-13", "2026-03-23", "2026-03-25",                  # Ch 6
    "2026-03-27", "2026-03-30", "2026-04-01", "2026-04-03", "2026-04-06",                  # Ch 5
    "2026-04-08", "2026-04-13", "2026-04-15", "2026-04-17", "2026-04-20", "2026-04-22",    # Ch 8
    "2026-04-24", "2026-04-27", "2026-04-29",                                              # Ch 9
    "2026-05-01", None,                                                                    # Ch 11; finale
]
PREDECESSOR_ASSESSMENT = {
    date(2026, 9, 25): "2026-02-13",    # S26 Quiz 1
    date(2026, 10, 23): "2026-03-11",   # S26 Quiz 2
    date(2026, 11, 20): "2026-04-10",   # S26 Quiz 3
}
# Flex days (2026-10-08, Michael): days with no content of their own, the budget a slip spends. 210
# has NONE: the flex day was spent on Mountain Day (Sep 23) and S26's practice day taught new
# content. A whole-day slip here means cutting content (shared/slip.py refuses until a flex day
# exists). Keyed by date like QUIZZES.
FLEX = {}
PREDECESSOR_FLEX = {}
# Slips: (date of the class, +1 or -1, note); see shared/calendar_rows.py. shared/slip.py appends here.
SLIPS = [
]
assert len(PREDECESSOR_CONTENT) == len(CONTENT), "one predecessor day per CONTENT row"
assert set(PREDECESSOR_ASSESSMENT) == set(QUIZZES), "one predecessor day per quiz"
assert set(PREDECESSOR_FLEX) == set(FLEX), "one predecessor day per flex day"

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[3] / "shared"))
from calendar_rows import make_rows, effective_pcci, flex_summary  # noqa: E402


def rows():
    """The term, one dict per meeting (shared/calendar_rows.py): n, date, kind, topic, reading, extra,
    predecessor, pcci. Flex days and slips applied. THE sequence every consumer reads; CONTENT is
    positional input only."""
    return make_rows(class_days(), CONTENT, QUIZZES, FLEX, SLIPS,
                     PREDECESSOR_CONTENT, PREDECESSOR_ASSESSMENT, PREDECESSOR_FLEX, _PCCI)


term_rows = rows          # alias for build(), whose local list is also called rows


def predecessor_days():
    """{class number (meetings held): the predecessor's day 'YYYY-MM-DD', a list when a class straddles two of
    hers (the first is the main one), or None}."""
    return {r["n"]: r["predecessor"] for r in rows()}


# WHW01 is due MONDAY Sep 14, not Friday Sep 11 (decided 2026-09-02).
# Every other WHW covers the Mon+Wed of its due week. Week 1 has no Monday --
# the semester opens on a Wednesday -- so under the normal rule WHW01 would be
# due the same day its material is taught (Fri Sep 11, "Generating ODEs from
# physical situations"). Shifting it to Monday is the smallest fix; the
# assignment text says explicitly that this is a one-off.
WHW_DUE_OVERRIDE = {1: date(2026, 9, 14)}

# PCCIs that were assigned for a meeting that was then lost (Mountain Day). Collected from
# whoever had done them, not in the gradebook; their solution Pages stay on Moodle, so the
# Moodle builders (pcci_crops_210.py, build_210_content.py) read this table too.
PCCI_LOST = {date(2026, 9, 23): "10.1, 10.3"}

# Felder problems whose text says "by computer" / "have a computer ...".
# None of these may sit on a WHW due before the Python class (Mon Sep
# 28); 1.36 slipped onto WHW01 in F2026 (caught 2026-09-11). Problems that
# merely say "graph" or "sketch" (1.38, 1.102) are fine by hand.
COMPUTER_PROBLEMS = {"1.36", "1.76", "3.86", "10.268"}
PYTHON_CLASS = date(2026, 9, 28)
# Sets already handed to students are a historical record, not a plan, so
# the by-computer guard skips them. WHW01 went out and was submitted with
# 1.36 in Depth plus an explicit "skip this if you don't have computational
# tools" clause, which is what made it survivable before the Python class.
DELIVERED = {1}

# Days students must bring a laptop. The schedule sheet (embedded in Moodle)
# tags the topic "[BRING LAPTOP]" and the review checklist repeats it, so one
# list drives both (a student asked not to carry a laptop every day, 2026-09-14).
LAPTOP_DAYS = {date(2026, 9, 28)}

# Extra (non-WHW) due dates shown in the HW Due column.
# Non-Newtonian Scientist: mid-semester (decision 2026-08-17); Mon Oct 26
# is the calendar midpoint and has no competing WHW deadline.
EXTRA_DUE = {
    date(2026, 10, 26): "Non-Newtonian Scientist due",
}

# ---------------------------------------------------------------- PCCIs
# Pre-Class Check-Ins, Gary-Felder style (decision 2026-08-17): due at
# the start of class most days; mostly the section's Discovery Exercise
# (DE x.y.1 = the Discovery Exercise of section x.y), done BEFORE the
# topic. Quiz days and the flex day get none. Every problem/DE number
# below is attested in a predecessor's actual assignment (Gary's PCCI
# schedules, Gillian's WHW forms, Casey's in-class problem sets) -- see
# private/GillianManbirS26/.../WHW problem lists (transcribed).md and
# the 2026-08-17 inventory report. Timing calibration: Gary's students
# reported ~8-27 min per DE (old/15F/Assigned Problems.docx).
_PCCI = {   # the hand table; PCCI below is the effective one (a PCCI follows its topic after a slip)
    # No PCCI on day 1 (nobody has the syllabus before the first
    # class); first collection is day 2, matching Gary's practice.
    # DE 1.2.1 is deliberately unassigned: class 01 does its content
    # live (the y'=8x ladder).
    date(2026, 9, 11): "Read the syllabus and the advice from former "
                       "students; bring one question or comment",
    date(2026, 9, 14): "DE 1.3.1 Part 1",
    date(2026, 9, 16): "DE 1.5.1 Parts 1-5",
    date(2026, 9, 18): "DE 1.6.1 Parts 1-3",
    date(2026, 9, 21): "DE 1.6.1 Parts 4-6",
    # Sep 23 (Mountain Day) had "10.1, 10.3": see PCCI_LOST below.
    date(2026, 9, 28): "Log into jupyterhub.smith.edu and open a blank "
                       "Jupyter notebook; bring your laptop",
    date(2026, 9, 30): "DE 10.10.1 Parts 1-9",
    date(2026, 10, 2): "10.216",
    date(2026, 10, 5): "DE 3.2.1",
    date(2026, 10, 7): "DE 3.4.1",
    # Re-keyed 2026-10-01 with the rebuild: each PCCI moved with its topic. Dropped: 6.175
    # (its eigen day merged). No PCCI on Nov 6 (polar) or Dec 9 (complex Fourier), new days.
    date(2026, 10, 9): "DE 2.2.1 Parts 1-5",
    date(2026, 10, 14): "DE 2.3.1 Parts 1-3",
    date(2026, 10, 16): "2.209",
    date(2026, 10, 19): "6.2",
    date(2026, 10, 21): "DE 6.3.1",
    date(2026, 10, 26): "DE 6.5.1",
    date(2026, 10, 28): "DE 6.8.1 Parts 1-3",
    date(2026, 10, 30): "6.166",
    date(2026, 11, 2): "5.1",
    date(2026, 11, 4): "DE 5.4.1",
    date(2026, 11, 9): "5.163 parts a and d",
    date(2026, 11, 11): "DE 5.7.1 Parts 1-4",
    date(2026, 11, 13): "DE 8.2.1 Parts 5-6",
    date(2026, 11, 16): "DE 8.4.1",
    date(2026, 11, 18): "Read Feynman II Ch 3 sections 3-1 to 3-6; in one "
                        "or two sentences, what does the flux of a vector "
                        "field out of a tiny box measure, and what does the "
                        "circulation around a tiny loop measure?",
    date(2026, 11, 23): "DE 8.6.1 Parts 1-9",
    date(2026, 11, 30): "DE 8.9.1",
    date(2026, 12, 2): "DE 8.11.1 Parts 1-2, 4-5, 7-8",
    date(2026, 12, 4): "DE 9.2.1 Parts 1-3",
    date(2026, 12, 7): "DE 9.4.1 Part 1",
    date(2026, 12, 11): "DE 11.2.1 Parts 1-2",
    date(2026, 12, 14): "DE 11.3.1 Part 1",
}
PCCI = effective_pcci(rows())

# ------------------------------------------------------- WHW problem lists
# 13 weekly lists, re-cut from Gillian's S26 WHW forms (transcribed
# 2026-08-17) onto the F2026 week boundaries: WHW N covers the Monday +
# Wednesday material of its due week, with Friday's new topic rolling
# into the next WHW (the S26 convention). Where our calendar covers
# material S26's forms did not (coordinates day, the Feynman div/curl
# days, 9.6, 11.3), problems come from Gary Felder's assigned lists and
# Casey Berger's F22 in-class sets -- every number is attested.
# Problems assigned as a PCCI are NOT repeated in the WHW lists.
# Tuples: (whw, covers, warmup, essentials, depth).
WHWS = [
    (1, "Intro to ODEs (1.1-1.2)",
     "ODEs: 1.17, 1.19",
     "ODEs: 1.18, 1.20, 1.21, 1.25",
     # 1.36 (compound interest BY COMPUTER) was taken off this set on
     # 2026-09-11 -- but the Moodle page was never edited, so the set that
     # actually went out and was submitted (Mon Sep 14) still carried it,
     # with the skip clause below. A delivered set is a record, not a plan,
     # so the calendar shows what students got. 1.36 is ALSO on WHW04,
     # which is the first set after the Python class.
     "ODEs: 1.33, 1.36 (if you don't have experience with computational "
     "tools, feel free to completely skip this)"),
    (2, "Arbitrary constants (1.3); separation of variables (1.5)",
     "Arbitrary constants: 1.39, 1.41, 1.43. "
     "Separation of variables: 1.90, 1.91, 1.93, 1.95",
     "Arbitrary constants: 1.38, 1.46, 1.58. "
     "Separation of variables: 1.103",
     "Arbitrary constants: 1.60. Separation of variables: 1.105"),
    (3, "Guess and check, superposition (1.6); linear operators (10.2)",
     "Guess and check: 1.108, 1.109",
     # 1.129 (linearity/homogeneity/superposition tester), NOT 1.29 (a
     # slope-fields problem from cut section 1.4) -- transcription fix
     # 2026-08-24 from the S26 form screenshots.
     "Guess and check: 1.111, 1.113, 1.117, 1.122, 1.129. "
     "Sec 10.2: 10.13, 10.26, 10.31",
     "Guess and check: 1.125, 1.131. Sec 10.2: 10.32, 10.33"),
    (4, "ODEs in Python; Heaviside, Dirac, Laplace (10.10)",
     "Sec 10.10: 10.217, 10.218",
     "Sec 10.10: 10.219, 10.223, 10.230, 10.242",
     "Redo the class notebook's exercises from scratch in a fresh "
     "notebook on jupyterhub.smith.edu. Sec 1.2: 1.36 (compound interest, "
     "by computer; it was optional Depth on WHW01 before we had Python, "
     "so here it is with the tools)"),
    (5, "Solving ODEs with Laplace transforms (10.11); "
        "complex numbers and Euler (3.1-3.5)",
     "Sec 10.11: 10.246, 10.248. Complex numbers: 3.17, 3.19, 3.47. "
     "Euler / complex ODE: 3.59, 3.65, 3.77",
     # 2026-10-07: 10.264 (complex roots) made optional in class; the complex half of the
     # Laplace rule was not reached on Oct 7 and its interpretation is off the quizzes.
     "Sec 10.11: 10.252, 10.261, 10.263, 10.264 (optional). "
     "Complex numbers: 3.49, 3.54. Euler / complex ODE: 3.92, 3.94, 3.95",
     "Sec 10.11: 10.270, 10.272, 10.274. Complex numbers: 3.45, 3.56. "
     "Euler / complex ODE: 3.85, 3.107"),
    # Autumn recess (Mon Oct 12) leaves this week ONE content day, Wed Oct 14.
    # Maclaurin (2.3) is not taught until Fri Oct 16 -- the morning this is due
    # -- and 2.86/2.87 are section 2.5, taught Mon Oct 19, three days AFTER.
    # Both moved to WHW07 (2026-09-02 coverage audit). A light week here is
    # correct, not a defect: it is the only week with a single content day.
    (6, "Linear approximations (2.1-2.2)",
     "Linear approximations: 2.6, 2.7",
     "Linear approximations: 2.9, 2.16, 2.19",
     "Linear approximations: 2.23"),
    # 2026-09-02: absorbs the Maclaurin block rolled forward from WHW06.
    # 2.41/2.47/2.49/2.53 are section 2.3 (verified against the textbook's
    # problem-block headings), so they are labelled Maclaurin, not Taylor.
    # 6.6 added because 6.7 opens "Problem 6.6 described the initial
    # conditions..." and 6.6 was assigned nowhere.
    (7, "Maclaurin series (2.3); Taylor series (2.4-2.5); matrices and "
        "the three-spring problem (6.1-6.2)",
     "Maclaurin series: 2.31, 2.41. Normal modes: 6.3. Matrices: 6.19",
     "Maclaurin series: 2.35, 2.37, 2.47, 2.49, 2.53. "
     "Taylor series: 2.55, 2.57, 2.67. "
     "The three-spring problem: 6.6, 6.7, 6.17. Normal modes: 6.9. "
     "Matrices: 6.21, 6.23",
     "Taylor series: 2.71, 2.94. Finding one series from another: "
     "2.86, 2.87"),
    (8, "Matrix times column, basis, matrix times matrix, identity, "
        "inverse, determinants (6.3-6.7)",
     "Matrix times column: 6.27, 6.29, 6.31. Matrix-matrix: 6.69. "
     "Identity and inverse: DE 6.6.1, 6.97. Determinants: 6.127, 6.129",
     "Matrix times column: 6.35, 6.41. Matrix-matrix: 6.81, 6.89, 6.91. "
     "Identity and inverse: 6.99, 6.101, 6.103, 6.107, 6.109, 6.119, "
     "6.121, 6.123. Determinants: 6.133, 6.139",
     "Basis and transformations: 6.45, 6.53, 6.55, 6.57, 6.61. "
     "Determinants: 6.147, 6.161"),
    # 2026-09-02: section 6.9's problem block starts at 6.191, so this list
    # previously had ZERO coupled-oscillator problems despite covering 6.9
    # (6.185 is section 6.8). Added 6.193 (the 6.9 walk-through) and 6.191.
    # 6.174 is the 6.8 walk-through, whose method 6.175/6.177 already assume.
    (9, "Eigenvalues and eigenvectors (6.8); coupled oscillators (6.9)",
     "Eigenvectors & eigenvalues: 6.170, 6.172, 6.174. "
     "Coupled oscillators: 6.193",
     "Eigenvectors & eigenvalues: 6.171, 6.173, 6.177. "
     "Coupled oscillators: 6.191",
     "Eigenvectors & eigenvalues: 6.179, 6.181, 6.185"),
    (10, "Setting up integrals; Cartesian doubles; line and "
         "surface integrals (5.1-5.4, 5.8, 5.10)",
     "Setting up 1D integrals: 5.2, 5.3. Single integrals in multiple "
     "dimensions: 5.25, 5.27, 5.29, 5.31. Cartesian rectangular double "
     "integrals: 5.61, 5.63. Line integrals: 5.197. Surface integrals: "
     "5.255",
     "Setting up 1D integrals: 5.7, 5.9, 5.11, 5.19, 5.23. Single "
     "integrals in multiple dimensions: 5.35, 5.43, 5.45, 5.51. "
     "Cartesian rectangular: 5.71, 5.75, 5.77. Cartesian "
     "non-rectangular: 5.83, 5.85, 5.97, 5.101. Line integrals: 5.199, "
     "5.201, 5.215, 5.217, 5.229. Surface integrals: 5.256, 5.257, 5.263",
     "Line integrals: 5.222, 5.223, 5.225, 5.235"),
    (11, "Polar, cylindrical and spherical coordinates (5.6, 5.5, 5.7); "
         "fields, potential, gradient (8.1-8.5)",
     "Spherical coordinates: 5.167. Cylindrical and spherical: 5.169. "
     "Scalar and vector fields: "
     "8.1. Potential in 1D: DE 8.3.1, 8.29, 8.35. From "
     "potential to gradients: 8.53, 8.55",
     "Spherical coordinates: 5.174, 5.181, 5.187. Polar and cylindrical: "
     "5.129, 5.137, 5.147. Jacobians and change of variables: 5.153. "
     "Scalar and vector fields: 8.5, 8.7, "
     "8.9, 8.17, 8.19, 8.21, 8.25. Potential in 1D: 8.37, 8.41, 8.43. "
     "From potential to gradients: 8.57, 8.59, 8.65. "
     "From gradient to potential: 8.69",
     "Jacobians and change of variables: 5.157. "
     "Polar and cylindrical: 5.171, 5.193. "
     "All coordinates: 5.165"),
    (12, "Divergence and curl, Feynman and Felder (Feynman II 2-3, "
         "8.6-8.7); divergence theorem and Stokes' theorem (8.9-8.10)",
     # Retiered 2026-09-02. Depth used to be 8.106 plus the writing task,
     # and 8.106's whole published solution is "the divergence is a scalar,
     # and you can't take the curl of a scalar field" -- the easiest item on
     # the sheet, sitting above 8.169 and 8.171 (two derivations) in
     # Essentials. Also, neither theorem had a warm-up: the ramp went from
     # div/curl pictures straight to the divergence theorem. 8.147 (predict
     # the flux is zero, then verify both sides) is that ramp.
     "Divergence and curl by inspection: 8.84, 8.86. "
     "Which operators even make sense: 8.106. "
     "Divergence theorem: 8.147",
     "Divergence and curl: 8.88, 8.90, 8.94, 8.98, 8.102, 8.110. "
     "The math behind divergence and curl: 8.113, 8.114. "
     "Divergence theorem: 8.151, 8.155, 8.157. "
     "Stokes' theorem: 8.159, 8.165",
     "Why the theorems work: 8.169, 8.171. Write out Feynman's "
     "flux-through-a-tiny-cube derivation of the divergence theorem in "
     "your own words, with pictures"),
    (13, "Conservative fields (8.11); Fourier series (9.1-9.5)",
     "Fourier series: 9.5, 9.7, 9.9. Different periods and finite domains: 9.44",
     "Conservative fields: 8.178. Fourier series: 9.15, 9.17, 9.23, "
     "9.27, 9.29, 9.33",
     "Conservative fields: 8.173, 8.177, 8.179. Different "
     "periods and finite domains: 9.38, 9.41, 9.47. Complex Fourier "
     "series: 9.60, 9.62, 9.66"),
]

def build(outpath):
    days = list(class_days())
    n = len(days)
    seq = term_rows()                  # the asserts on the row counts live in shared/calendar_rows.py
    assert all(d in days for d in QUIZZES), "quiz on a non-class day"
    assert all(d.weekday() == 4 for d in QUIZZES), "quiz day not on a Friday"
    assert all(d in days for d in PCCI), "PCCI assigned to a non-class day"
    assert not any(d in PCCI for d in QUIZZES), "PCCI assigned to a quiz day"

    # WHW due dates: one per Friday after the first class (incl. quiz days,
    # matching the previous prof); WHW_DUE_OVERRIDE wins.
    whw_due = {}   # WHW number -> due date, for the WHW sheet
    fridays = [d for slot_i, d in enumerate(days) if d.weekday() == 4 and slot_i > 0]
    for hw_no, d in enumerate(fridays, start=1):
        due_d = WHW_DUE_OVERRIDE.get(hw_no, d)
        if due_d <= PYTHON_CLASS and hw_no not in DELIVERED:
            text = " ".join(WHWS[hw_no - 1][2:5])
            bad = sorted(p for p in COMPUTER_PROBLEMS
                         if re.search(r"(^|[^\d.])" + re.escape(p) + r"($|[^\d])", text))
            assert not bad, f"WHW{hw_no:02d} (due {due_d}) is before the Python class but holds by-computer problems {bad}"
        whw_due[hw_no] = due_d
    # date -> HW Due labels, APPEND semantics as in 317's build() (2026-10-05):
    # an override onto another WHW's date, or an EXTRA_DUE on a WHW date,
    # shares the cell instead of overwriting it, and the assert after the
    # row loop hard-fails on a due date that never reached a class row (it
    # used to vanish from the Schedule sheet while the WHW sheet printed it).
    due_on = {}
    for hw_no, due_d in whw_due.items():
        due_on.setdefault(due_d, []).append(f"WHW{hw_no:02d}")
    for ed, label in EXTRA_DUE.items():
        due_on.setdefault(ed, []).append(label)

    # rows: one per class meeting; insert break markers
    rows = []      # (week, class_no, date, topic, reading, pcci, hw, exam)
    week_no = 0
    last_week = None
    class_no = 0
    breaks_seen = set()
    for d in days:
        iso_week = d.isocalendar()[1]
        if iso_week != last_week:
            week_no += 1
            last_week = iso_week
        # note upcoming breaks as their own marker rows
        for bd, why in NO_CLASS.items():
            if bd not in breaks_seen and bd < d:
                breaks_seen.add(bd)
                rows.append((None, None, bd, why, "", "", "", ""))
        r = seq[class_no]
        assert r["date"] == d
        topic, reading = r["topic"], r["reading"]
        exam = topic if r["kind"] == "assessment" else ""
        hw = "; ".join(due_on.pop(d, []))
        class_no += 1
        rows.append((week_no, class_no, d, topic, reading,
                     PCCI.get(d, ""), hw, exam))
    for bd, why in NO_CLASS.items():
        if bd not in breaks_seen:
            rows.append((None, None, bd, why, "", "", "", ""))
    assert not due_on, f"due dates that are not class days, missing from the HW Due column: {due_on}"
    rows.sort(key=lambda r: r[2])
    rows.append((None, None, date(2026, 12, 19),
                 "Final exam period Dec 19-22 (registrar schedules)",
                 "", "", "", "Final (Ch 8, 9, 11 + redemptions)"))
    assert set(whw_due) == {w[0] for w in WHWS}, (
        f"WHW sheet numbers {sorted(w[0] for w in WHWS)} != "
        f"calendar WHW numbers {sorted(whw_due)}")

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Schedule"

    header_font = Font(bold=True)
    header_fill = PatternFill("solid", fgColor="D9E1F2")
    break_fill = PatternFill("solid", fgColor="FCE4D6")
    exam_fill = PatternFill("solid", fgColor="FFF2CC")
    thin = Side(style="thin", color="BBBBBB")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)
    wrap = Alignment(wrap_text=True, vertical="top")

    headers = ["Week", "Class", "Date", "Topics", "Reading Due", "PCCI",
               "HW Due", "Exams"]
    last_col = openpyxl.utils.get_column_letter(len(headers))
    # Single canonical block (the old two-block print layout is in git
    # history; superseded 2026-08-27). Written as TWO CHUNKS, each
    # starting with its own header row, split at fall break: the
    # Moodle Page embeds chunk 1's range until fall break, then chunk
    # 2's (one URL-parameter edit; see MoodleBuildSpec.md). The
    # ranges are printed on every run.
    wsw = ws
    chunk2_start = date(2026, 10, 14)  # first class after autumn recess

    def web_header(r):
        for j, h in enumerate(headers, start=1):
            cell = wsw.cell(row=r, column=j, value=h)
            cell.font = header_font
            cell.fill = header_fill
            cell.border = border
            cell.alignment = wrap

    web_header(1)
    r, split_row = 1, None
    for (wk, cn, d, topic, reading, pcci, hw, exam) in rows:
        if split_row is None and d >= chunk2_start:
            r += 1
            web_header(r)
            split_row = r
        r += 1
        vals = [wk, cn, d.strftime("%a %b %-d"), topic + (" [BRING LAPTOP]" if d in LAPTOP_DAYS else ""), reading,
                pcci, hw, exam]
        for j, v in enumerate(vals, start=1):
            cell = wsw.cell(row=r, column=j, value=v)
            cell.border = border
            cell.alignment = wrap
            if cn is None:
                cell.fill = break_fill
            elif exam:
                cell.fill = exam_fill
    for j, w in enumerate([7, 7, 10, 34, 12, 18, 10, 14]):
        col = openpyxl.utils.get_column_letter(1 + j)
        wsw.column_dimensions[col].width = w
    # The "embed ranges" were for the August Google Sheet embed, replaced by the course map on
    # 2026-09-28 (students never see a sheet); the xlsx is a reference copy only.
    print(f"(legacy) schedule embed ranges: chunk 1 = A1:{last_col}{split_row - 1}, "
          f"chunk 2 = A{split_row}:{last_col}{r}")

    # ----------------------------------------------- WHW problem lists
    whw = wb.create_sheet("WHW Problem Lists")
    note = ("The following problems are useful practice for the week. "
            "I recommend starting with the warm-ups. If they're too "
            "easy, move on to Essentials. If you're interested in the "
            "Depth content, you can add those problems as well. You "
            "are not expected to do all the problems. DE x.y.1 = the "
            "Discovery Exercise of section x.y. Answers to odd "
            "problems: felderbooks.com/mathmethods (Appendix M).")
    whw.append([note])
    whw.merge_cells(start_row=1, start_column=1, end_row=1, end_column=6)
    whw.cell(row=1, column=1).alignment = wrap
    whw.row_dimensions[1].height = 60
    whw.append(["WHW", "Due", "Covers", "Warm-up", "Essentials", "Depth"])
    for cell in whw[2]:
        cell.font = header_font
        cell.fill = header_fill
        cell.border = border
    for i, (wn, covers, warm, ess, depth) in enumerate(WHWS, start=3):
        vals = [f"WHW{wn:02d}", whw_due[wn].strftime("%a %b %-d"),
                covers, warm, ess, depth]
        for j, v in enumerate(vals, start=1):
            cell = whw.cell(row=i, column=j, value=v)
            cell.border = border
            cell.alignment = wrap
    for j, w in enumerate([8, 11, 30, 34, 44, 34]):
        whw.column_dimensions[openpyxl.utils.get_column_letter(j + 1)].width = w

    gc = wb.create_sheet("Grade Categories")
    gc.append(["Category", "Number", "Drop", "Points Each", "Total Points"])
    for cell in gc[1]:
        cell.font = header_font
        cell.fill = header_fill
    # Michael's decided scheme (2026-08-11; participation weight raised
    # 2026-08-25: 2 pts/day, quizzes 150->140, final 190->185). Course
    # total must be exactly 1000 points. pts_cell, when set, is the
    # formula written to the sheet (Non-Newtonian Scientist is worth one
    # homework, by reference).
    # FLAG (2026-10-04): 39 is the number of meetings SCHEDULED; 38 were held
    # after Mountain Day. The syllabus promises 39 - 4 = 35 days x 2 points
    # (build_skeleton.py says the same); whether that becomes 38 - 3 or stays
    # as written is Michael's call. Left as written until he decides.
    cats = [
        ("Attendance/participation", 39, 4, 2, None),
        ("Written Homework (WHW)", 13, 1, 25, None),
        ("Non-Newtonian Scientist", 1, 0, 25, "=D3"),
        ("Quizzes", 3, 0, 140, None),
        ("Final exam", 1, 0, 185, None),
    ]
    total = sum((num - drop) * pts for _, num, drop, pts, _ in cats)
    assert total == 1000, f"grade categories sum to {total}, not 1000"
    for i, (name, num, drop, pts, pts_cell) in enumerate(cats, start=2):
        gc.append([name, num, drop, pts_cell or pts, f"=(B{i}-C{i})*D{i}"])
    gc.append(["Total", None, None, None, f"=SUM(E2:E{1 + len(cats)})"])
    for j, w in enumerate([28, 9, 7, 12, 13]):
        gc.column_dimensions[openpyxl.utils.get_column_letter(j + 1)].width = w

    wb.save(outpath)
    print(f"wrote {outpath}: {len(rows)} schedule rows, {n} class meetings")

if __name__ == "__main__":
    build(sys.argv[1])

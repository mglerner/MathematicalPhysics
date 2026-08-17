"""Generate the Fall 2026 PHY 210 (Mathematical Physics, Smith) course calendar.

Format follows EarlhamArtifacts/P125 F2025 Calendar.xlsx: a "Schedule" sheet
with Week | Class | Date | Topics | Reading Due | HW Due | Exams, in two
side-by-side half-semester blocks, plus a "Grade Categories" sheet skeleton.
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
NO_CLASS = {
    date(2026, 10, 12): "Autumn recess",
    date(2026, 11, 25): "Thanksgiving",
    date(2026, 11, 27): "Thanksgiving",
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
# pinned to Friday slot indices; the flex day sits where her Spring '26
# snow day fell (week 5) and absorbs snow / Mountain Day / drift.
# 35 content slots + 3 quiz days + 1 flex day = 39 MWF meetings, exactly
# matching her 39 spring slots. The calendar is FULL: adding a new topic
# means converting the flex or practice day, or displacing content.
SPECIALS = {
    7: ("Quiz 1 (Ch 1)", True),                          # Fri Sep 25
    13: ("Flex day (snow / Mountain Day buffer)", False),  # Fri Oct 9
    18: ("Quiz 2 (Ch 10, 3, 2)", True),                  # Fri Oct 23
    30: ("Quiz 3 (Ch 6, 5)", True),                      # Fri Nov 20
}
CONTENT = [
    ("Syllabus; SHO and overview of differential equations", "1.1-1.2"),
    ("Generating ODEs from physical situations", "1.1-1.2"),
    ("Arbitrary constants; initial conditions", "1.3"),
    ("Separation of variables", "1.5"),
    ("Guess and check", "1.6"),
    ("Linearity, homogeneity, superposition", "1.6"),
    ("Methods of solving ODEs: guess and check", "10.2"),
    ("Jupyter notebook exercise: ODEs in Python", "10.2"),
    ("Heaviside, Dirac delta, and the Laplace transform", "10.10"),
    ("Using Laplace transforms to solve ODEs", "10.11"),
    ("Complex numbers: basic properties", "3.1-3.4"),
    ("Euler's formula; complex ODEs", "3.5"),
    ("Linear approximations", "2.1-2.2"),
    ("Maclaurin series", "2.3"),
    ("Taylor series; finding one series from another", "2.4-2.5"),
    ("Properties of matrices", "6.1-6.2"),
    ("Matrix x column; vector transformations", "6.3-6.4"),
    ("Matrix multiplication; identity, determinant, inverse", "6.5-6.7"),
    ("Finding eigenvalues and eigenvectors", "6.8"),
    ("Eigenvalues and eigenvectors, continued", "6.8"),
    ("The two-coupled-oscillator problem", "6.9"),
    ("Setting up 1D and 2D integrals", "5.1-5.2"),
    # Polar double integrals are Felder 5.6, not 5.3-5.4 (verified against the
    # textbook TOC 2026-08-17; the S26 grid this row was copied from mislabels it).
    ("Cartesian 2D integrals; polar coordinates", "5.3-5.4, 5.6"),
    ("Line integrals and surface integrals", "5.8, 5.10"),
    ("Practice / review day", ""),
    ("Vector and scalar fields; the gradient", "8.1-8.4"),
    ("Work, path integrals, and the gradient theorem", "8.5"),
    ("Gradient, divergence, curl", "8.5-8.7"),
    ("Divergence, curl, and the Laplacian", "8.6-8.7"),
    ("Divergence theorem; Stokes' theorem", "8.9-8.10"),
    ("Conservative vector fields", "8.11"),
    ("Introduction to Fourier series", "9.1-9.3"),
    ("Fourier series: different periods, finite domains", "9.4"),
    ("Fourier series with complex exponentials", "9.5"),
    ("Intro to PDEs: the heat equation", "11.1-11.2"),
]

def build(outpath):
    days = list(class_days())
    n = len(days)
    assert len(CONTENT) + len(SPECIALS) == n, (
        f"{len(CONTENT)} content + {len(SPECIALS)} specials "
        f"for {n} class meetings")
    assert all(days[i].weekday() == 4 for i in SPECIALS), (
        "quiz/flex day not on a Friday")

    # rows: one per class meeting; insert break markers
    rows = []          # (week, class_no, date, topic, reading, hw, exam)
    week_no = 0
    last_week = None
    class_no = 0
    hw_no = 0
    content_i = 0
    breaks_seen = set()
    for slot_i, d in enumerate(days):
        iso_week = d.isocalendar()[1]
        if iso_week != last_week:
            week_no += 1
            last_week = iso_week
        # note upcoming breaks as their own marker rows
        for bd, why in NO_CLASS.items():
            if bd not in breaks_seen and bd < d:
                breaks_seen.add(bd)
                rows.append((None, None, bd, f"No class - {why}", "", "", ""))
        if slot_i in SPECIALS:
            label, is_quiz = SPECIALS[slot_i]
            topic, reading, exam = label, "", (label if is_quiz else "")
        else:
            topic, reading = CONTENT[content_i]
            exam = ""
            content_i += 1
        hw = ""
        if d.weekday() == 4 and slot_i > 0:  # Fridays (incl. quiz days,
            hw_no += 1                       # matching the previous prof)
            hw = f"WHW{hw_no:02d}"
        class_no += 1
        rows.append((week_no, class_no, d, topic, reading, hw, exam))
    for bd, why in NO_CLASS.items():
        if bd not in breaks_seen:
            rows.append((None, None, bd, f"No class - {why}", "", "", ""))
    rows.sort(key=lambda r: r[2])
    rows.append((None, None, date(2026, 12, 19),
                 "Final exam period Dec 19-22 (registrar schedules)",
                 "", "", "Final (Ch 8, 9, 11 + redemptions)"))

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

    headers = ["Week", "Class", "Date", "Topics", "Reading Due", "HW Due", "Exams"]
    # two side-by-side blocks, like the P125 calendar: cols A-G and I-O
    half = (len(rows) + 1) // 2
    blocks = [rows[:half], rows[half:]]
    for b, block in enumerate(blocks):
        c0 = 1 + b * 8  # A=1, I=9
        for j, h in enumerate(headers):
            cell = ws.cell(row=1, column=c0 + j, value=h)
            cell.font = header_font
            cell.fill = header_fill
            cell.border = border
        for i, (wk, cn, d, topic, reading, hw, exam) in enumerate(block, start=2):
            vals = [wk, cn, d.strftime("%a %b %-d"), topic, reading, hw, exam]
            for j, v in enumerate(vals):
                cell = ws.cell(row=i, column=c0 + j, value=v)
                cell.border = border
                cell.alignment = wrap
                if cn is None:
                    cell.fill = break_fill
                elif exam:
                    cell.fill = exam_fill

    widths = [6, 6, 11, 42, 12, 9, 22]
    for b in range(2):
        for j, w in enumerate(widths):
            col = openpyxl.utils.get_column_letter(1 + b * 8 + j)
            ws.column_dimensions[col].width = w

    gc = wb.create_sheet("Grade Categories")
    gc.append(["Category", "Number", "Drop", "Points Each", "Total Points"])
    for cell in gc[1]:
        cell.font = header_font
        cell.fill = header_fill
    # Michael's decided scheme (2026-08-11). Course total must be exactly
    # 1000 points. pts_cell, when set, is the formula written to the sheet
    # (Non-Newtonian Scientist is worth one homework, by reference).
    cats = [
        ("Attendance/participation", 39, 4, 1, None),
        ("Written Homework (WHW)", 13, 1, 25, None),
        ("Non-Newtonian Scientist", 1, 0, 25, "=D3"),
        ("Quizzes", 3, 0, 150, None),
        ("Final exam", 1, 0, 190, None),
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

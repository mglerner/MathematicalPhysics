# PHY 210 — Fall 2026 (Smith College)

First Smith iteration of this course. Textbook changes from Boas (Earlham,
2012-2024) to **Felder & Felder, _Mathematical Methods in Engineering and
Physics_**. The plan sticks closely to the schedule the previous Smith
professor used in Spring 2026 (source spreadsheet:
`../../../SmithPreMichaelArtifacts/Spring '26 PHY 210 Schedule.xlsx`).

## Files here

- `PHY210 F2026 Calendar.xlsx` — draft course calendar, formatted like my
  P125 calendar (two side-by-side blocks; Week / Class / Date / Topics /
  Reading Due / HW Due / Exams). Import into Google Sheets
  (File > Import > Upload) and embed that sheet in Moodle.
- `make_fall2026_calendar.py` — regenerates the xlsx. Edit the `CONTENT` /
  `SPECIALS` / `cats` tables and rerun:
  `python make_fall2026_calendar.py "PHY210 F2026 Calendar.xlsx"`
  (the `courses/` uv venv has openpyxl; direnv activates it automatically).
  **The script is the source of truth**: hand-edits to the xlsx get
  clobbered on regeneration, so fold them into the script (as was done
  with the 2026-08-11 grade-category edits).
- `PHY210Syllabus.tex` — copy of the Earlham 2024 syllabus, **not yet
  adapted**; see the TODO block at the top for everything that must change.

## Fall 2026 key dates (Smith academic calendar)

- Classes: Tue Sep 8 - Tue Dec 15. First MWF meeting Wed Sep 9; last Mon Dec 14.
- Add deadline Mon Sep 14; drop deadline Tue Sep 22.
- Autumn recess: Sat Oct 10 - Tue Oct 13 (kills Mon Oct 12).
- Cromwell Day: Tue Nov 10 (no MWF impact).
- Mountain Day: TBA by the president — one fall day's classes cancel;
  the Fri Oct 9 flex day is the designated absorber (shuffle into it).
- Thanksgiving: Wed Nov 25 - Sun Nov 29 (kills Wed Nov 25, Fri Nov 27).
- Reading period Dec 16-18; exams Sat Dec 19 - Tue Dec 22.

That gives 39 MWF meetings, vs. the previous prof's 39 spring slots, so
her calendar maps over exactly one-to-one: 35 content slots (including
her Jupyter-ODE day and practice/review day) + 3 dedicated in-class quiz
days + 1 flex day where her week-5 snow day fell. **The calendar is
full** — adding a new topic (Python days, FFTs, etc.) means converting
the flex day or the practice/review day, or displacing content. An
earlier draft padded the tail with invented days ("Python: FFTs and real
data", extra review days); those were mine, not hers, and were removed
2026-08-11 in favor of the faithful mapping.

## Assumptions to verify

- **MWF meeting pattern** — the whole calendar assumes it. If the registrar
  gives a different pattern (e.g. TTh), regenerate with new dates.
- Quizzes are **dedicated in-class Friday days** (matching the previous
  prof): Sep 25 (Ch 1), Oct 23 (Ch 10, 3, 2), Nov 20 (Ch 6, 5). The
  coverage groupings are hers; the exact dates are my placement at the
  matching points in the fall sequence. WHW is still due on quiz Fridays
  (she did the same).
- Grading (decided 2026-08-11, total exactly 1000, asserted in the
  generator): attendance 39 drop 4 @ 1 = 35; WHW 13 drop 1 @ 25 = 300;
  Non-Newtonian Scientist = one HW = 25; quizzes 3 @ 150 = 450;
  final 190. This needs to go into the syllabus when it's adapted.

## Course machinery

- LMS: Moodle. Programming: Python (Jupyter; existing topic notebooks in
  this repo carry over even though the textbook changed).
- Private materials (solutions, exams, grades, other professors' files) go
  in `../../private/` -> `~/Dropbox/__Smith/Classes/210-MathMethods/private/`
  (gitignored symlink; Dropbox is the backup).

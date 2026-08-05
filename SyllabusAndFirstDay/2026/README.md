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
- `make_fall2026_calendar.py` — regenerates the xlsx. Edit the `SLOTS` /
  `QUIZZES` tables and rerun:
  `python make_fall2026_calendar.py "PHY210 F2026 Calendar.xlsx"`
  (the `courses/` uv venv has openpyxl; direnv activates it automatically).
- `PHY210Syllabus.tex` — copy of the Earlham 2024 syllabus, **not yet
  adapted**; see the TODO block at the top for everything that must change.

## Fall 2026 key dates (Smith academic calendar)

- Classes: Tue Sep 8 - Tue Dec 15. First MWF meeting Wed Sep 9; last Mon Dec 14.
- Add deadline Mon Sep 14; drop deadline Tue Sep 22.
- Autumn recess: Sat Oct 10 - Tue Oct 13 (kills Mon Oct 12).
- Cromwell Day: Tue Nov 10 (no MWF impact).
- Mountain Day: TBA by the president — one fall day's classes cancel;
  the schedule will need a live shuffle when it lands.
- Thanksgiving: Wed Nov 25 - Sun Nov 29 (kills Wed Nov 25, Fri Nov 27).
- Reading period Dec 16-18; exams Sat Dec 19 - Tue Dec 22.

That gives 39 MWF meetings (before Mountain Day), vs. the previous prof's
39 spring slots, so the sequence maps over almost one-to-one.

## Assumptions to verify

- **MWF meeting pattern** — the whole calendar assumes it. If the registrar
  gives a different pattern (e.g. TTh), regenerate with new dates.
- Quiz dates (Fri Oct 2, Fri Oct 23, Fri Nov 13) follow the previous prof's
  unit groupings but are my placement, not hers.
- Grading is point-based with a course total of exactly 1000 points
  (enforced by an assertion in the generator). Current split — attendance
  39 drop 3 @ 1 = 36; WHW 13 drop 1 @ 32 = 384; quizzes 3 @ 110 = 330;
  final 250 — is my placeholder; the categories mirror the previous prof
  but the point values need real decisions.

## Course machinery

- LMS: Moodle. Programming: Python (Jupyter; existing topic notebooks in
  this repo carry over even though the textbook changed).
- Private materials (solutions, exams, grades, other professors' files) go
  in `../../private/` -> `~/Dropbox/__Smith/Classes/210-MathMethods/private/`
  (gitignored symlink; Dropbox is the backup).

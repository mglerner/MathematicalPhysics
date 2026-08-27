# PHY 210 F2026 Moodle build spec

Decisions encoded 2026-08-18: build our OWN course (do NOT restore
Gillian's .mbz -- it stays as a reference archive); organize by TOPIC,
not week; WHWs are native Moodle assignments (no Google Forms) so
everything lands on the students' Moodle calendar -- the exact thing
S26 failed to do (her calendar was empty; WHW 03+ had no due dates).

## Course settings

- Format: **Collapsed Topics** (installed at Smith). If ITS installs
  `format_tiles` (ask -- see TODO), switch later; format is
  display-only and doesn't touch content.
- `showactivitydates`: YES (S26 had it off; we want dates visible).
- Completion tracking: ON, manual completion boxes on assignments
  (students like the checkboxes; also feeds the Timeline block).
- Hidden sections: completely invisible.
- Blocks: Announcements forum (default), Calendar, Timeline. No other
  forums (matches S26/Will practice).

## Sections (~12 collapsed topics)

0. **General / Course Information** -- syllabus PDF; the Course
   Calendar Page (see "Schedule embed" below); posit.smith.edu
   pointer;
   office-hours info; anonymous feedback via a Moodle Feedback
   activity (anonymous mode, "allow multiple submissions" on, one
   open-ended textarea question; matches the syllabus's "anonymous
   Moodle comments" channel); week-1 office-hours scheduling poll
   (temporary).

   Also a SECOND Feedback activity (decided 2026-08-25, both
   courses): **mid-semester feedback**, anonymous, hidden until
   mid-October (open it around fall break, before Quiz 2), at least
   these three questions as textareas:
   1. What's working well?
   2. What's not working well, and how can the instructor make
      things better?
   3. What can you, as the student, do to make the class better?
1. **Homework (WHW)** -- standing section, Will-style: the 13 WHW
   assignments + the WHW problem lists (paste each week's tiers into
   the assignment description; the xlsx WHW tab is the source).
2. **Ch 1: Ordinary differential equations**
3. **Ch 10: Heaviside, Dirac, and Laplace transforms** (+ Python day
   materials)
4. **Ch 3: Complex numbers**
5. **Ch 2: Linear approximations and series**
6. **Ch 6: Linear algebra**
7. **Ch 5: Integrals in many dimensions** (+ coordinates day)
8. **Vector calculus: Feynman + Ch 8** -- Feynman Vol II Ch 2-3
   links (feynmanlectures.caltech.edu -- free, legal), worksheets
9. **Ch 9: Fourier series**
10. **Ch 11: PDEs (+ Fourier transforms finale)**
11. (optional) **Exams** -- practice quizzes + solutions as they're
    released; or fold into topic sections like Gillian did.

Per-topic sections hold: posted class-notes PDFs (the GoodNotes
exports after each class), notebooks, practice quizzes for that
material, and the felderbooks Discovery Exercise PDFs for that
topic's PCCIs.

PCCI distribution (decided 2026-08-26, Gary's model): NO printed
handouts and NO hand-typeset LaTeX pages. The schedule sheet's PCCI
column names each day's exercise; 21 of 34 are Discovery Exercises
whose official typeset PDFs (felderbooks.com, already in the prep
packs) get attached to the topic sections; 10 are plain book
problems; 3 are one-line authored instructions. Students turn in
their own paper at the start of class -- there is no worksheet.
Gillian never ran PCCIs at all (S26 tree has zero mentions), so
Gary's decade of practice is the only, and sufficient, precedent. Section summaries carry a one-line "when we're here" note
instead of week numbers (topic sections age better than week sections
when the schedule slips).

## Schedule embed (decided 2026-08-27, revives Michael's old design)

The xlsx's "Schedule (web)" tab is written as TWO CHUNKS, each with
its own header row, split at fall break -- so the embed always shows
the currently-relevant part of the semester without scrolling. The
generator prints the ranges on every run; for the current build:
chunk 1 = A1:H16 (Sep 9 - Oct 12), chunk 2 = A17:H45 (Oct 14 on).

- The Google Sheet (converted once; document ID is permanent) gets
  updated ONLY via File -> Import -> Upload -> "Replace spreadsheet"
  with the regenerated xlsx. NEVER re-convert a fresh upload -- that
  mints a new document and orphans the published URLs.
- Publish to web -> Embed -> "Schedule (web)" tab; auto-republish ON;
  access restriction OFF (restricted iframes break for students
  whose browsers block third-party cookies).
- The Course Calendar Page's iframe = published URL +
  `&range=A1:H16`, width:100%, height ~800, border 0. Below it, a
  plain link to the unranged published URL labeled "full-semester
  calendar".
- AT FALL BREAK (course-level Moodle calendar event, Tue Oct 13:
  "switch schedule embed to 2nd half"): edit the Page, change the
  range parameter to `A17:H45`. 30 seconds.
- After ANY calendar regeneration: re-import (above) AND check the
  printed ranges still match the Page's range parameter.

## Assignments (all native Moodle; this IS the calendar)

Common settings: file submissions (max 20) + ONLINE TEXT enabled;
feedback = comments + annotate PDF; no cutoff date;
`submissiondrafts=0`; grade category per below.

| Assignment              | Due                                                       | Pts                    | Notes                                                                                                                            |
| ----------------------- | --------------------------------------------------------- | ---------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Math Pretest            | Fri Sep 18, 22:00                                         | (participation credit) | PDF attached; graded for completion                                                                                              |
| WHW01..WHW13            | Fridays 22:00 (WHW11 -> check calendar; WHW13 Fri Dec 11) | 25 each                | description = that week's tier list + reflection questions; submission = photo of work (file) + reflection answers (online text) |
| Non-Newtonian Scientist | Mon Oct 26, 22:00                                         | 25                     | prompt adapted from shared/NonNewtonianPhysicist/                                                                                |

One due TIME everywhere: 22:00 (Gillian's drifted; Will's drifted;
pick one, keep it).

WHW description template (per week): Gillian's standing preamble
(from the xlsx WHW tab) + the week's Warm-up/Essentials/Depth lists +
the required computational problem (see below) + the reflection
questions (the 7 from S26, or Michael's trimmed set) as the online-
text prompt.

## Required computational problems (decided 2026-08-18)

Gary's "purple tier" model, in Python: a REQUIRED small computational
item on most WHWs (~8-10 of 13). Sources to draft from: Michael's
Earlham notebooks, Gary's purple problems (ported), the S26 guided
notebooks (ODE_basics is the keeper). Sep 28 = the onboarding class
(full class, bring laptops, posit.smith.edu). BUILD TASK: draft the
per-week computational items and add them to the WHW lists (generator
edit) -- see TODO.

## Calendar events (course-level, so they appear without assignments)

- Quiz 1 Fri Sep 25, Quiz 2 Fri Oct 23, Quiz 3 Fri Nov 20 (in class,
  full period)
- Flex day Fri Oct 9; no class Mon Oct 12, Wed Nov 25, Fri Nov 27
- Final exam period Dec 19-22 (update when registrar schedules)

## Gradebook (mirrors the 1000-point scheme, natively)

Categories (aggregation: Natural; participation weight raised
2026-08-25 -- 2 pts/day):
- Participation & PCCIs -- 70 pts. PCCIs are graded on PAPER; enter
  into Moodle as manual grade item(s). Simplest: two manual items
  ("Participation through fall break" ~ /34, "Participation after" ~
  /36) entered twice a semester; drops handled on paper tally.
- WHW -- 13 x 25, **droplow = 1** set on the category.
- Non-Newtonian -- 25.
- Quizzes -- 3 manual items @ 140 (paper quizzes).
- Final -- manual item @ 185.
Total 1000; verify against the Grade Categories sheet from the
generator.

## Notebooks posted to Moodle

Post FIXED copies only (never Gillian's originals verbatim): delete
the %pip cells; swap in the corrected apply_initial_conditions();
keep the intentional NameError in Sympy_Basics. Post as force-download
(students run them on posit). Keepers: Sympy_Basics, Sympy_ODE_basics,
ODE_Laplace (fixed), MacLaurin/Series pair. Symmetry + FourierSeries
demos fold into class decks instead.

## AI-aware assignment design (decided 2026-08-18)

- Early-semester CLASS DISCUSSION (week 1-2, ~15 min chunk): how/
  whether we use AI on homework at all, and on computational work in
  particular -- norms set WITH the students, then written up and
  posted to Moodle as the operating agreement alongside the syllabus
  policy.
- Assignment structure follows the effort-graded logic already in the
  syllabus: the graded artifact is the record of the student's own
  thinking. Computational problems should ask for prediction-before-
  running, interpretation-after, and "what did you try that didn't
  work" -- the parts AI polish erases.

## Deliberately NOT doing

- No restore of Gillian's .mbz (reference only). No Google Forms at
  all -- WHWs and anonymous feedback are both native Moodle
  activities. No posted full-textbook scan, no instructor-solutions-manual
  excerpts (copyright; see the 317 lesson). No extension-request form
  (late passes are declared by email, per the syllabus).

# PHY 210 Fall 2026: syllabus & course-machinery TODO

Working task list for syllabus-writing and course setup. Companion to
README.md (calendar facts) and the inventory report
(`~/coding/reports/courses-mathmethods-f2026-inventory-2026-08-17.html`,
which has the full materials map, item banks, and privacy-cleanup list).

## Decided

- **13 WHWs** (2026-08-17). Matches the generator's grade line
  (WHW 13 drop 1 @ 25 = 300). Keep Gillian's Warm-up/Essentials/Depth
  tiers; her S26 lists are transcribed at
  `private/GillianManbirS26/PHY210 S26/Weekly Homeworks (WHW)/WHW problem
  lists (transcribed 2026-08-17).md` (WHW 09 still to capture).
  Due Fridays end of day, covering Mon+Wed material (S26 convention).
- **PCCIs Gary's way** (2026-08-17): most class days (natural skips:
  quiz Fridays, day after a quiz), mostly Felder Discovery Exercises
  done BEFORE the topic; <= 15 min; good-faith-effort grading -- full
  credit for a clear description of where you're stuck; drop ~3. Turned
  in on paper at the start of class + four-color-card comfort poll as
  the class opener. Still open: where the points live (candidate: the
  PCCI turn-in IS the attendance/participation artifact).
- **Non-Newtonian Scientist due mid-semester: Mon Oct 26** (2026-08-17;
  encoded in the calendar's HW Due column).
- **Calendar decisions all locked** (2026-08-17, encoded in the
  generator; see README.md for the summary): review day -> cyl/spherical
  coordinates day (5.5, 5.7; App. D); Feynman Vol II Ch 2-3 read BEFORE
  Felder 8.6-8.7 (geometric div/curl definitions first; Ch 3 also cited
  on the theorems day); Fourier series in 2 days (9.1-9.3, 9.4-9.5);
  PDEs protected with 2 days (Fri Dec 11: 11.1-11.2 + 11.4; Mon Dec 14:
  11.3); Fourier transforms (9.6) ride the Dec 14 finale graphically
  (Gary's last-day design: sketch-the-transform + exoplanets + image
  compression); 2.6-2.7 convergence cut, Appendix C pointer on the
  Taylor day's reading.
- Math pretest ported to LaTeX (`Pretest/`); due-date placeholder
  Fri Sep 18 pending final calendar.
- **Moodle: build our own course** (2026-08-18) -- do NOT restore
  Gillian's backup. Topic-organized (Collapsed Topics format; ask ITS
  about format_tiles), WHWs as NATIVE Moodle assignments (file upload
  + online-text reflection; no Google Forms) so every deadline lands
  on the students' Moodle calendar -- fixing S26's empty-calendar
  failure. Full details: `MoodleBuildSpec.md` (the build is an
  afternoon of clicking once the F2026 shell exists).
- **Python assessed weekly, Gary-style** (2026-08-18): a required
  small computational problem (Python, not Mathematica) on most WHWs
  (~8-10 of 13), plus the Sep 28 onboarding class run as a full class
  (bring laptops). BUILD TASK: draft the per-week computational items
  (sources: Michael's Earlham notebooks, Gary's purple-tier problems,
  the S26 ODE_basics notebook) and add them to the generator's WHW
  lists; adjust WHW point/grading language if needed.
- **AI-aware assignment design** (2026-08-18): an early-semester class
  discussion (~15 min chunk, week 1-2) on how/whether AI belongs in
  homework and computational work; norms co-written with students and
  posted to Moodle alongside the syllabus policy. Computational
  problems ask for predict-before-run / interpret-after / what-didn't-
  work -- the parts AI polish erases.
- **Chapter order confirmed as-inherited** (2026-08-18): the
  1 -> 10 -> 3 -> 2 -> 6 -> 5 -> 8 -> 9 -> 11 sequence is
  Gillian/Manbir's restructuring (Gary and Berger both ran
  1,2,3,5,6,8,9,11 with no Ch 10); we keep it (materials + WHW/PCCI
  machinery are keyed to it). Known wart: Laplace lands before
  Euler's formula -- handled Manbir-style with an explicit IOU when
  complex roots first appear.

## Post-calendar build task -- DONE 2026-08-17

WHW/PCCI re-cut encoded in the generator: 13 tiered WHW lists on a new
"WHW Problem Lists" xlsx tab (re-cut from Gillian's transcribed forms
+ attested supplements), and 35 PCCIs inline in a new Schedule-tab
column (mostly Discovery Exercises; all numbers attested). Review
items: WHW05 is heavy (10.11 + all of Ch 3 -- deliberate, tiers carry
it); WHW04's Depth and the day-1/Python-day/Feynman-day PCCIs are
authored tasks, not book problems; the PDE days (Dec 11/14) have no
WHW after them -- the final's practice set covers that material.

## Syllabus-writing session

7. DONE 2026-08-17 (draft, tufte-handout style): `PHY210Syllabus.tex`
   rewritten for Smith F2026. Time/room filled from the registrar
   listing (MWF 9:25-10:40, McConnell 404); prereqs corrected to
   MTH 212 & PHY 111/117/119. Office filled: McConnell 303. Remaining
   red [TODO] markers: office hours, tutor names, WHW turn-in
   structure confirm, calculator policy confirm, recording policy.
8. Grading table = the 1000-point scheme (attendance 39 drop 4 @ 1;
   WHW 13 drop 1 @ 25 = 300; Non-Newtonian 25; quizzes 3 @ 150; final
   190). Decide where PCCI credit lives -- candidate: PCCI turn-in IS
   the attendance/participation artifact (no new category needed).
9. DECIDED 2026-08-18: WHW turn-in = native Moodle assignment, photo
   of worked problem(s) as file upload + reflection questions answered
   in the online-text box, good-faith graded. Encoded in
   MoodleBuildSpec.md; syllabus updated.
10. AI policy: start from Will Raven's F2025 version
    (`SmithPreMichaelArtifacts/PHY317 F2025 Syllabus.pdf`), not the
    older S26 copy; refresh the dated ChatGPT anecdotes with current
    failure examples; add a line that effort-graded work (PCCI/WHW) is
    only worth doing un-assisted; keep consistent with PHY 317.
11. Quiz machinery -- DECIDED 2026-08-18 in the syllabus: sample
    quizzes + solutions posted beforehand (committed); questions
    aligned with in-class problems and WHW lists; one double-sided
    handwritten note sheet; basic calculator OK, no phones/laptops/
    internet devices, documented accommodations always met. Still to
    build: the actual quiz instruments (v1/v2 variants; item banks in
    the inventory report).
12. Final redemption rules: S26 model = original quiz problems verbatim,
    improvement retroactively restores quiz points. KEEP PER-PROBLEM
    QUIZ RECORDS (Gillian had to beg students for photos of their own
    scores). Write the rules into the syllabus (currently "TBD").
13. Late/extension policy: S26 extension Google Form? Earlham late
    passes? Gillian's late-WHW amnesty (-5/week, better than zero)?
14. Growth-mindset bundle: keep pretest + goal-setting/reflections?
    (S26: hard deadlines on these, 10%.) Align the pretest's "graded
    for completion" sentence with the final scheme.
15. Learning goals: draft from Casey Berger's 14 rubric tables
    (S23 Assessments/*.tex) + CU Phys 2210 goals (Pedagogy/, attribute).
16. Course description: Gary's catalog copy (Other/Catalog copy
    post-multivariate.docx) -- "a review of multivariate calculus" is
    already in the catalog language.
17. Boilerplate to lift from the S26 syllabus: ARC accommodations
    paragraph, Honor Code, land acknowledgment, resources list, the
    15-min course-feedback-window sentence. Fix their bundle-numbering
    typo pattern; don't inherit it.

## External / verify / find

18. VERIFY with registrar: add (Sep 14) / drop (Sep 22) deadlines,
    autumn recess Oct 10-13, Cromwell Day Nov 10, reading period +
    exam window. (MWF pattern + time/room VERIFIED 2026-08-17 via the
    course schedule listing: MWF 9:25-10:40, McConnell 404.)
19. RESOLVED 2026-08-18: Non-Newtonian Physicist prompt recovered
    verbatim from the F2023 PHYS-125 Moodle backup (it was
    Moodle-only, as suspected) -- now at
    `../../../shared/NonNewtonianPhysicist/` with its screenshots and
    F2026 adaptation notes. Remaining: adapt for Felder + check
    whether the TextbookAnnotater tool at mglerner.com still runs
    (the prompt has a document-upload fallback if not).
20. RESOLVED 2026-08-18: voting cards found (they're named
    "VotingCard", hence the four-color search miss) -- copied to
    `../../../shared/` (portrait + landscape PDFs + Keynote source).
21. DONE 2026-08-17: WHW 09 captured; all 12 S26 lists transcribed.
22. Ask Gillian: schedule Google Sheet share; whether Ch 11 was cut in
    both sections; Quiz-2-Wednesday story; Apr 29 / May 1.
23. Ask Manbir: F23 post-mortem (scope cut or overrun); real pacing.
24. Ask ITS/AV + classroom: Panopto/Zoom recording setup, group
    whiteboards in McConnell 404, AND whether they'll install the
    `format_tiles` Moodle course format (Collapsed Topics is the
    fallback, already installed).
25. Ask math dept: does MTH 212 still deliver the negotiated topics
    (Gary's listening-session memo says commitment != reality on
    cyl/sph coords and div/curl).

## Build tasks (after decisions)

26. SUPERSEDED 2026-08-18 by MoodleBuildSpec.md: we build our own
    course rather than restoring Gillian's backup (which stays as a
    reference archive). No Google links to re-point -- the WHWs are
    native assignments and anonymous feedback is a Moodle Feedback
    activity (decided 2026-08-24; was briefly a Google Form). The
    only surviving Google artifact is the schedule Sheet embed.
27. Notebooks: delete %pip cells; swap in the fixed
    apply_initial_conditions() (tested replacement in the inventory
    outputs); add narration to Symmetry/FourierSeries; confirm posit
    provisioning of numpy/sympy/matplotlib.
28. Pre-semester email to registrants: adapt Gary's Math Review packet
    (Math Review/Message to students.docx + attachments).
29. Fix Manbir-deck errata before reusing any page (list in the report).
30. Privacy cleanup pass over inherited trees (list in the report).

31. Fluctuation-theorem Stage-0 seeds (added 2026-08-24; source:
    `../../../FluctuationTheorems/ROADMAP.md`): fold into 210 as
    Depth-tier WHW problems / small asides, costing no calendar
    slots -- (a) Gaussian moment identity <e^(cX)> = e^(c mu + c^2
    sigma^2/2) on a series/integration week; (b) Jensen's inequality
    for e^x (state, two-point proof, picture); (c) Fourier transform
    of e^(-a|t|) is a Lorentzian (Fourier week Depth); (d) linear
    first-order ODE solution as convolution with e^(-t/tau) (Ch 1 or
    10 Depth). Jacobians and the 2D divergence theorem are already
    load-bearing course content (Ch 5 + the Feynman unit) -- no
    action needed there. Each seed pays off in PHY 317's Liouville
    aside and the eventual FT module.

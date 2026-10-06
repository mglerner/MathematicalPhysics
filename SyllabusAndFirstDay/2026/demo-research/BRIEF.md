# Demo research brief (Smith College, Fall 2026)

Instructor: Michael Lerner, physics professor. Meeting the physics lab manager TODAY
to plan lecture demos for two courses. Both courses are TIGHT on time (75-min MWF
classes, calendar full, no flex day left). Rules from Michael:
- Aspirational goal: one demo per week per class. BUT "don't stuff in a crappy demo
  just to fill up space." Quality over coverage.
- Short demos preferred (2-10 min). Long demos only if "really good, in which case
  they're worth a TON."
- Demos must be run as predict-observe-explain (PER: Crouch/Fagen/Mazur 2004), so
  each entry needs a crisp prediction question students can vote on.
- Today is 2026-10-06. Both courses are at class 12 (Oct 7). Earlier days are
  history (still list a demo if it would have fit -- it's useful for next year --
  but mark that it is in the past). Focus effort on Oct 7 onward.
- Already done in 317: Helmholtz coils / e-beam tube at cyclotron frequency (class 05).
- Gary Felder (previous 210 instructor at Smith) does coupled-oscillator demos
  (probably blocks + springs on an air track). Michael wants, in 210, a demo of
  circular motion projected onto x and y axes (shadow of a peg on a turntable next
  to a pendulum/spring: e^{i wt} = cos + i sin), for the complex-numbers/Euler days.
- In 317 Michael definitely wants a brachistochrone demo (cycloid track race +
  tautochrone).

Output REQUIRED from each research agent: a markdown file with a JSON list.
Each demo entry has these keys:
  id            short slug
  name          demo name (what a lab manager would recognize)
  classes       list of class numbers (ints) it fits, best first
  fit           one sentence: which concept on that day it serves
  duration_min  realistic minutes INCLUDING the predict/vote/explain wrapper
  tier          "must" (really good, worth the time) | "good" (short, clean) |
                "maybe" (only if a cheap version exists) -- do NOT include junk
  materials     list of strings (standard physics-stockroom items; name the
                commercial product if it's a buy, e.g. "PASCO ME-9495 cycloid track")
  pira          PIRA DCS code(s) if known, e.g. "3A40.10"; "" if unknown
  prediction    the question students vote on BEFORE the demo (concrete, with 3-4
                answer options if natural)
  observe       what actually happens (1-2 sentences)
  explain       the physics/math point, tied to the course's language (Taylor
                sections for 317; Felder & Felder sections for 210)
  pitfalls      list of strings: what goes wrong, setup time, safety
  refs          list of {title, url, note}: demo catalogs (Harvard Natural Sciences
                Lecture Demos, UC Berkeley Physics Lecture Demonstrations, MIT TSG,
                Univ of Iowa / Wisconsin / Minnesota demo DBs, PIRA), AJP / TPT
                papers, vendor pages, videos. VERIFY each URL with WebFetch (it must
                resolve and be about the demo). Prefer stable catalog pages.
  video         {youtube_id, title} of a good short video of the demo, or null
                (thumbnails come from https://img.youtube.com/vi/<id>/hqdefault.jpg;
                verify the video exists and is the right demo).
  image         {url, credit, license} for a Wikimedia Commons or catalog still
                image, or null
  diy           if the standard apparatus is a buy, a cheap/3D-printed/DIY
                alternative with a reference, else ""
  notes         anything else the lab manager needs

Also add, after the JSON, a short prose section "Skips": topics in your range
where you looked and found no demo worth the minutes (one line each, with why).

Write the file to the path given in your prompt. Use plain ASCII (no fancy
Unicode glyphs: write x not the multiplication sign, -> not an arrow).

## PHY 210 Mathematical Methods (Felder & Felder), class list
01 Wed Sep 09  Syllabus; SHO and overview of differential equations  [1.1-1.2]
02 Fri Sep 11  Generating ODEs from physical situations  [1.1-1.2]
03 Mon Sep 14  Arbitrary constants; initial conditions  [1.3]
04 Wed Sep 16  Separation of variables  [1.5]
05 Fri Sep 18  Guess and check  [1.6]
06 Mon Sep 21  Linearity, homogeneity, superposition  [1.6]
07 Fri Sep 25  ** Quiz 1 (Ch 1)
08 Mon Sep 28  Jupyter notebook exercise: ODEs in Python  [10.2]
09 Wed Sep 30  Heaviside, Dirac delta, and the Laplace transform  [10.10]
10 Fri Oct 02  Using Laplace transforms to solve ODEs  [10.11]
11 Mon Oct 05  Complex numbers: basic properties  [3.1-3.3]
12 Wed Oct 07  Euler's formula; complex ODEs  [3.4-3.5]
13 Fri Oct 09  Linear approximations  [2.1-2.2]
14 Wed Oct 14  Maclaurin series  [2.3]
15 Fri Oct 16  Taylor series; finding one series from another  [2.4-2.5]
16 Mon Oct 19  Properties of matrices (three-spring / two-mass intro)  [6.1-6.2]
17 Wed Oct 21  Matrix x column; vector transformations  [6.3-6.4]
18 Fri Oct 23  ** Quiz 2 (Ch 10, 3, 2)
19 Mon Oct 26  Matrix multiplication; identity and inverse  [6.5-6.6]
20 Wed Oct 28  Determinants; finding eigenvalues and eigenvectors  [6.7-6.8]
21 Fri Oct 30  Eigenvectors; the two-coupled-oscillator problem  [6.8-6.9]
22 Mon Nov 02  Setting up 1D and 2D integrals  [5.1-5.2]
23 Wed Nov 04  Cartesian 2D integrals  [5.3-5.4]
24 Fri Nov 06  Polar coordinates  [5.6]
25 Mon Nov 09  Line integrals and surface integrals  [5.8, 5.10]
26 Wed Nov 11  Cylindrical and spherical coordinates  [5.5, 5.7; App. D]
27 Fri Nov 13  Vector and scalar fields; potential  [8.1-8.3]
28 Mon Nov 16  The gradient; equipotentials  [8.4]   (OBSERVATION DAY: instructor talk capped at 15 min)
29 Wed Nov 18  Potential from a field; gradient theorem; divergence and curl (Feynman II Ch 3)  [8.5-8.6]
30 Fri Nov 20  ** Quiz 3 (Ch 6, 5)
31 Mon Nov 23  Divergence, curl, Laplacian; divergence theorem (Feynman II Ch 2)  [8.6-8.7, 8.9]
32 Mon Nov 30  Divergence theorem; Stokes' theorem  [8.9-8.10]
33 Wed Dec 02  Conservative vector fields  [8.11]
34 Fri Dec 04  Introduction to Fourier series  [9.1-9.3]
35 Mon Dec 07  Fourier series: different periods, finite domains  [9.4]
36 Wed Dec 09  Fourier series with complex exponentials  [9.5]
37 Fri Dec 11  Intro to PDEs: the heat equation; separation of variables  [11.1-11.2, 11.4]
38 Mon Dec 14  Normal modes of the wave equation; Fourier transforms  [11.3, 9.6]

## PHY 317 Classical Mechanics (Taylor), class list
01 Wed Sep 09  Syllabus; notation; Newton's laws; polar coordinates  [Ch 1]
02 Fri Sep 11  Newton's laws  [Ch 1]
03 Mon Sep 14  Linear drag force; terminal velocity  [2.1-2.2]
04 Wed Sep 16  Trajectories and range; quadratic air drag  [2.3-2.4]
05 Fri Sep 18  Lorentz force law; cyclotron motion  [2.5-2.7]   (DONE: Helmholtz coils)
06 Mon Sep 21  Conservation of momentum; rocket motion  [3.1-3.2]
07 Fri Sep 25  Center of mass; angular momentum  [3.3-3.4]
08 Mon Sep 28  Moment of inertia; conservation of angular momentum  [3.5]
09 Wed Sep 30  Work-KE theorem; conservative forces  [4.1-4.3]
10 Fri Oct 02  Potential energy; graphs of PE functions  [4.4-4.7]
11 Mon Oct 05  Central forces; multiparticle systems  [4.8-4.10]
12 Wed Oct 07  Spring forces; simple harmonic oscillator  [5.1-5.2]
13 Fri Oct 09  2D oscillators; damped SHO  [5.3-5.4]
14 Wed Oct 14  Forced damped SHO; resonance  [5.5-5.6]
15 Fri Oct 16  ** EXAM 1 (Ch 2-4)
16 Mon Oct 19  Fourier series analysis of driven SHO  [5.7-5.8]
17 Wed Oct 21  Calculus of variations; Fermat's principle; Euler-Lagrange  [6.1-6.2]
18 Fri Oct 23  Euler-Lagrange equation; brachistochrone problem  [6.3]
19 Mon Oct 26  Multiple variables; generalized coordinates  [6.4]
20 Wed Oct 28  Lagrange's equations; Hamilton's principle  [7.1]
21 Fri Oct 30  Constrained systems; generalized coordinates  [7.2-7.3]
22 Mon Nov 02  Examples of Lagrange's equations; Noether's theorem; Lagrange multipliers  [7.5, 7.8, 7.10]
23 Wed Nov 04  Central forces; reduced mass; equations of motion  [8.1-8.4]
24 Fri Nov 06  Orbits  [8.5-8.6]
25 Mon Nov 09  Changing orbits  [8.7-8.8]
26 Wed Nov 11  Accelerating frames; tides  [9.1-9.2]
27 Fri Nov 13  Catch-up / review day (Exam 2 is Monday)
28 Mon Nov 16  ** EXAM 2 (Ch 5-7)
29 Wed Nov 18  Angular velocity; rotating frames  [9.3-9.5]
30 Fri Nov 20  Centrifugal force; Coriolis force  [9.6-9.8]
31 Mon Nov 23  Coupled oscillators; two masses and three springs  [11.1-11.2]
32 Mon Nov 30  Normal coordinates; weakly coupled oscillators; start the double pendulum  [11.2-11.4]
33 Wed Dec 02  Double pendulum  [11.4]
34 Fri Dec 04  Catch-up / review day (Exam 3 is Monday)
35 Mon Dec 07  ** EXAM 3 (Ch 8, 9, 11)
36 Wed Dec 09  Chaos: the driven damped pendulum; period doubling  [12.1-12.4]
37 Fri Dec 11  Chaos: sensitivity to initial conditions; Liouville aside  [12.4-12.5]
38 Mon Dec 14  Last day: review and wrap-up

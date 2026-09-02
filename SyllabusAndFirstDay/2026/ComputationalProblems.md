# PHY 210 F2026: required weekly computational problems

Drafted 2026-08-24. **APPROVED by Michael 2026-08-28** (nine problems; WHW13
stays where it is; no separate point split -- see Resolved questions below).
Folded into `private/MoodleBuild/whw-descriptions.html` the same day as a
fourth block in each WHW description (Warm-up / Essentials / Depth /
**Computational**, the last one required). Solution sketches were split out
to `private/ComputationalProblemSolutions.md` on 2026-08-28 -- this repo is
public and those are the predictions students are graded on making
themselves. Deliberately NOT added to
`make_fall2026_calendar.py`: the generator drives the xlsx problem-list tab,
which stays tiers-only; the descriptions HTML is the student-facing text.

Decisions this draft implements:

- "Python assessed weekly, Gary-style" (TODO, 2026-08-18): a *required*
  small computational item on most WHWs, ~8-10 of 13.
- "AI-aware assignment design" (TODO/MoodleBuildSpec, 2026-08-18): every
  problem asks for a **prediction before running**, an **interpretation
  after**, and (on most) **"what did you try that didn't work"**.
- Python only (numpy / sympy / matplotlib), run on posit.smith.edu.

## The count and the skip rule

Nine required problems, on WHW **02, 04, 05, 06, 08, 09, 10, 12, 13**.
Four weeks are deliberately skipped, under one rule that is easy to state
to students and easy to keep when the calendar drifts:

> No required computational problem on a quiz Friday, and none in week 1.

| WHW | Due        | Computational item  | Why                                                             |
| --- | ---------- | ------------------- | --------------------------------------------------------------- |
| 01  | Fri Sep 11 | **skip**            | Week 1: two class meetings, no Python yet, AI norms not yet set |
| 02  | Fri Sep 18 | yes (tool-agnostic) | Pre-onboarding; "any tool you like"                             |
| 03  | Fri Sep 25 | **skip**            | Quiz 1 day, and still pre-onboarding (onboarding is Mon Sep 28) |
| 04  | Fri Oct 2  | yes                 | First post-onboarding week                                      |
| 05  | Fri Oct 9  | yes                 |                                                                 |
| 06  | Fri Oct 16 | yes                 |                                                                 |
| 07  | Fri Oct 23 | **skip**            | Quiz 2 day                                                      |
| 08  | Fri Oct 30 | yes                 |                                                                 |
| 09  | Fri Nov 6  | yes                 |                                                                 |
| 10  | Fri Nov 13 | yes                 |                                                                 |
| 11  | Fri Nov 20 | **skip**            | Quiz 3 day; its gradient content is picked up by the WHW12 item |
| 12  | Fri Dec 4  | yes                 |                                                                 |
| 13  | Fri Dec 11 | yes                 | Fourier capstone (WHW13 is also the drop-eligible one)          |

Due dates above are read off `make_fall2026_calendar.py`, which is
authoritative: WHWs land every Friday including quiz Fridays, so WHW01-03
all precede the Mon Sep 28 Python onboarding class. Only WHW02 therefore
needs to be runnable with no posit account and no Python, and it is
written that way.

## Standing preamble (goes once in each WHW description)

> **Computational problem (required).** Unlike the practice lists above,
> this one is turned in. It should take 20-40 minutes. Three moves are
> what make it count: (1) **predict** -- write down what you expect
> *before* you run anything, and leave the wrong prediction in your
> writeup; (2) **interpret** -- two or three sentences on what the output
> actually shows; (3) **report a dead end** -- one sentence on something
> you tried that did not work. This is graded the same good-faith way as the
> rest of the WHW, and those three moves are what good faith looks like here:
> a messy writeup that has all three is a complete submission, and a polished
> one missing them is not. The record of your own thinking is the assignment.

## Tooling notes

- Every problem below uses only `numpy`, `sympy`, `matplotlib`. **No
  scipy** -- posit provisioning of scipy is unconfirmed (TODO item 27),
  so where a numerical ODE solver would be natural (WHW04) the students
  write forward Euler themselves, which is better pedagogy here anyway.
- The sympy idioms match the S26 notebooks students will have seen on
  Sep 28 (`dsolve`, `checkodesol`, `laplace_transform`,
  `init_printing`).

---

## WHW 02 -- due Fri Sep 18

**Covers:** arbitrary constants (1.3); separation of variables (1.5)

### Problem text

The equation dy/dx = -2xy has general solution y = C exp(-x^2). Before
you plot anything, sketch by hand, on one set of axes, what you expect
the five curves C = -2, -1, 0, 1, 2 to look like: where are they
steepest, where do they cross each other, and what happens as x runs off
to +infinity and -infinity. Now make the real plot for -3 <= x <= 3 --
by hand on graph paper, in Desmos, in a spreadsheet, or in Python;
**any tool is fine this week**, since we do not meet in the computer
classroom until Mon Sep 28. Put your sketch and the real plot side by
side and write two or three sentences on what you got wrong or what
surprised you. Finally, answer from the formula rather than from the
picture: is there any point in the plane that no member of this family
passes through, and how many members pass through a point that is
covered?

**Provenance:** ported from Gary Felder's Spring 2022 Weekly Homework 01
Mathematica problem (Felder & Felder 1.38, "graphing a variety of
different functions" with an arbitrary constant) --
`private/GaryS22/Math Methods/22S/hw/Weekly Homework 01 - Mathematica instructions.pdf`
and `Weekly Homework 01.docx`. Retooled to be tool-agnostic because it
lands ten days before the Python onboarding class, and given a
predict-then-check spine. Note 1.38 is already on this week's Essentials
list, so the required item is a deepening of a problem they may already
have started, not a new one.

**Solution sketch:** in `private/ComputationalProblemSolutions.md` (kept out of this public repo).

---

## WHW 04 -- due Fri Oct 2

**Covers:** ODEs in Python (the Sep 28 class); Heaviside, Dirac, Laplace
(10.10)

### Problem text

Use SymPy's `dsolve` to solve dy/dt = -3y with y(0) = 1, and confirm the
answer with `checkodesol`. Now write your own forward-Euler loop in
NumPy -- y_{n+1} = y_n + h f(t_n, y_n) -- and run it on 0 <= t <= 2 with
step sizes h = 0.1, h = 0.5, and h = 0.8. Before you run it, write down
a prediction: as h grows, does the numerical solution just get *less
accurate*, or can it go qualitatively wrong, and if so, in what way?
Plot all three Euler solutions together with the exact curve on one set
of axes and say in two or three sentences which prediction the picture
supports. Then work out algebraically the largest h for which your Euler
solution still decays toward zero, and check that number against your
plot. Finish with one sentence on something that did not work along the
way (an off-by-one in the loop, an empty plot, a shape mismatch).

**Provenance:** fresh, but the design is Gary's -- his Mathematica-and-
numerics class plan (`private/GaryS22/Math Methods/22S/lectures/extra01-mathematica and numerics.docx`)
builds the whole numerical-solution idea from "you must supply numbers
for everything, including a domain", and his S22 WHW03 computational
problem was a numerical ODE solve (Felder 1.165). Written against
forward Euler rather than a black-box solver so it needs no scipy and so
that the failure mode is visible.

**Solution sketch:** in `private/ComputationalProblemSolutions.md` (kept out of this public repo).

---

## WHW 05 -- due Fri Oct 9

**Covers:** solving ODEs with Laplace transforms (10.11); complex numbers
and Euler's formula (3.1-3.5)

### Problem text

Consider the damped oscillator x'' + b x' + 4x = 0 with x(0) = 1 and
x'(0) = -2. Solve it for b = 1, b = 4, and b = 6 -- by hand, by Laplace
transform, or with SymPy, your choice -- and say which case has complex
roots. Before you plot: predict which of the three returns to x = 0
fastest and give a one-sentence reason. (Most people guess wrong here, so
write the guess down before you look.) Now plot all three solutions on
0 <= t <= 5 on one set of axes. Write two or three sentences
interpreting the picture: what does the *imaginary* part of the root do
to the curve, and what does the *real* part do? Finally, give the value
of b that separates oscillating from non-oscillating behavior and say how
you found it.

**Provenance:** ported from Gary Felder's Spring 2022 Weekly Homework 04
Mathematica problem (Felder & Felder 3.86), including his stated initial
conditions and plot window -- "For initial conditions set x(0)=1,
x'(0)=-2 and plot the functions from t=0 to t=5"
(`private/GaryS22/Math Methods/22S/hw/Weekly Homework 04.docx`). The
predict-which-is-fastest hook is added.

**Solution sketch:** in `private/ComputationalProblemSolutions.md` (kept out of this public repo).

---

## WHW 06 -- due Fri Oct 16

**Covers:** linear approximations (2.1-2.2)

REPLACED 2026-09-02. The original item here was Maclaurin partial sums of
sin(x), but the 2026-09-02 coverage audit found that WHW06 cannot assign
Maclaurin at all: autumn recess (Mon Oct 12) leaves the week one content day,
and 2.3 is not taught until Fri Oct 16 -- the morning this is due. The
Maclaurin textbook problems moved to WHW07, but WHW07 is Quiz 2 Friday and
carries no computational item under the skip rule, so this slot needed a
genuine 2.1-2.2 problem instead.

### Problem text

The pendulum equation theta'' = -(g/L) sin(theta) only becomes the simple
harmonic oscillator theta'' = -(g/L) theta because sin(theta) is approximately
theta. Before computing anything, write down a prediction: **how large can
theta get, in degrees, before sin(theta) = theta is wrong by more than 1%?**
Write your number down -- most people guess far too small.

Now check it. Plot sin(theta) and theta together on 0 <= theta <= pi/2, then
plot the relative error |theta - sin(theta)| / sin(theta) and read off where it
crosses 1%. Compare with your prediction.

Then one more prediction before you plot: on log-log axes, plot the absolute
error |sin(theta) - theta| against theta, and **predict the slope of that line
first**. Explain in two or three sentences what the slope tells you about how
fast a linear approximation degrades, and what you think the *next* correction
term must look like.

Finish with one sentence on something that did not work.

**Provenance:** fresh, written 2026-09-02 to replace the Maclaurin item. The
small-angle approximation is the reason the day-1 SHO class works at all, so
this closes a loop opened in class 01, and its second prediction hands the
students the Maclaurin unit (Mon Oct 19) as the answer to a question they
generated themselves.

**Solution sketch:** in `private/ComputationalProblemSolutions.md`
(kept out of this public repo).

---

## WHW 08 -- due Fri Oct 30

**Covers:** matrix times column, basis, matrix times matrix, identity,
inverse, determinants (6.3-6.7)

### Problem text

Store the corners of the unit square (0,0), (1,0), (1,1), (0,1) in a
NumPy array, and take A = [[2, 0], [0, 1]], B = [[1, 1], [0, 1]], and
C = [[0, -1], [1, 0]]. Before you compute anything, write down in words
what you expect each matrix to do to the square, and what each one does
to its area. Then plot the original square together with its image under
A, under B, under C, and under both products AB and BA. Compute det(A),
det(B), det(C), det(AB), and det(BA) with `numpy.linalg.det` and check
them against your area predictions. Answer in two or three sentences:
which of your predictions was wrong, and -- given that AB and BA give
visibly different pictures but the same determinant -- what does the
determinant actually tell you, and what does it not? Say what you tried
that did not work (forgetting to repeat the first corner so the polygon
closes is the usual stumble).

**Provenance:** fresh, but sits on top of Gary's S22 WHW06 Mathematica
matrix problem (Felder 6.15,
`private/GaryS22/Math Methods/22S/hw/Weekly Homework 06.docx`) and his
handout "Chapter 06 - The Case of the Fatal Transformation.doc".

**Solution sketch:** in `private/ComputationalProblemSolutions.md` (kept out of this public repo).

---

## WHW 09 -- due Fri Nov 6

**Covers:** eigenvalues and eigenvectors (6.8); coupled oscillators (6.9)

### Problem text

Two equal masses in a line, joined by three identical springs
(wall-mass-mass-wall), obey x'' = -(k/m) M x with M = [[2, -1], [-1, 2]].
Before computing: describe the two normal modes physically (how do the
masses move relative to each other?), say which one you expect to have
the higher frequency, and give a one-sentence physical reason. Then use
`numpy.linalg.eig` on M and compare the eigenvalues and eigenvectors with
your prediction. Set k/m = 1 and plot x1(t) and x2(t) on 0 <= t <= 20 for
two starting conditions, both released from rest: (a) displacement equal
to the first eigenvector, and (b) displacement (1, 0). Write two or three
sentences on why plot (b) shows *beating* -- energy sloshing back and
forth between the two masses -- while plot (a) does not. Note anything
that surprised you about how NumPy normalized or ordered the
eigenvectors.

**Provenance:** fresh; the system is the course's own two-coupled-
oscillator day (Felder 6.9) and matches Gary's S22 WHW07 extra-credit
Mathematica problem (Felder 6.87). Michael's `CoupledDEs/` notebooks in
this repo cover the same picture.

**Solution sketch:** in `private/ComputationalProblemSolutions.md` (kept out of this public repo).

---

## WHW 10 -- due Fri Nov 13

**Covers:** setting up integrals; Cartesian doubles and polar; line and
surface integrals (5.1-5.4, 5.6, 5.8, 5.10)

### Problem text

Evaluate the integral of f(x, y) = xy over the quarter disk
x^2 + y^2 <= 1 with x >= 0 and y >= 0, three ways: by hand in polar
coordinates, with SymPy, and with a NumPy Riemann sum on an N x N grid
over the square [0, 1] x [0, 1] in which you zero out every sample point
that falls outside the quarter disk. Before running the Riemann sum,
predict two things and write them down: will it come out above or below
the exact answer, and if you double N, by what factor should the error
shrink? Then run N = 10, 20, 40, 80, 160, plot the absolute error against
N on log-log axes, and read the slope off the plot. Explain in two or
three sentences why the observed slope is what it is, rather than the
slope you would get integrating a smooth function over a plain rectangle.
Report one thing that went wrong (mismatched `meshgrid` indexing is the
classic).

*Optional extension, no extra credit, just fun:* use the same
one-dimensional Riemann-sum machinery to check the Gaussian moment
identity, that the average of exp(cX) over a zero-mean Gaussian of width
sigma equals exp(c^2 sigma^2 / 2).

**Provenance:** fresh. The optional extension is fluctuation-theorem
Stage-0 seed (a) from TODO item 31 (source:
`../../../FluctuationTheorems/ROADMAP.md`), parked here because this is
the integration week.

**Solution sketch:** in `private/ComputationalProblemSolutions.md` (kept out of this public repo).

---

## WHW 12 -- due Fri Dec 4

**Covers:** divergence and curl, Feynman and Felder (Feynman II 2-3,
8.6-8.7); divergence theorem and Stokes' theorem (8.9-8.10)

### Problem text

Take the three two-dimensional vector fields F1 = (x, y), F2 = (-y, x),
and F3 = (x, -y). Before writing any code, predict the sign (positive,
negative, or zero) of the divergence and of the z-component of the curl
of each one, reasoning from Feynman's pictures -- net flux out of a tiny
box, net circulation around a tiny loop -- not from the formulas. Then
draw all three with matplotlib's `quiver` or `streamplot` on
-2 <= x, y <= 2 and check your predictions symbolically with SymPy. Now
do the numerical version of Feynman's argument: take the square of side 2
centered on the origin, estimate the outward flux of F1 through it as a
Riemann sum over the four edges, and compare with what the divergence
theorem predicts (divergence times enclosed area). In two or three
sentences, say which of your six sign predictions was hardest to read off
the picture and why. Add one sentence on something that did not work.

**Provenance:** fresh, written to sit directly on the Feynman-first
decision in the calendar (Feynman Vol II Ch 2-3 read *before* Felder
8.6-8.7) and on the WHW12 Depth item, which already asks students to
write out Feynman's flux-through-a-tiny-cube derivation in their own
words. Also absorbs the gradient/field-visualization content of WHW11,
which is skipped for Quiz 3.

**Solution sketch:** in `private/ComputationalProblemSolutions.md` (kept out of this public repo).

---

## WHW 13 -- due Fri Dec 11

**Covers:** conservative fields (8.11); Fourier series (9.1-9.5)

### Problem text

Work out by hand the Fourier series of the square wave f(x) = +1 for
0 < x < pi and f(x) = -1 for -pi < x < 0, extended with period 2pi. Before
plotting, predict: as you add more terms, does the largest error between
the partial sum and the square wave shrink to zero, and whereabouts on
the interval does the worst error sit? Write the prediction down. Then
plot the partial sums with 1, 3, 9, and 49 nonzero terms against the
exact square wave, and make a second plot of the size of the overshoot
near x = 0 as a function of the number of terms. Explain in two or three
sentences what your second plot says about convergence at a jump
discontinuity, and say what the series converges to *exactly at* x = 0.
Note one thing you tried that did not work.

**Provenance:** ported from Gary Felder's Spring 2022 Weekly Homework 11
Mathematica problem (Felder & Felder 9.13,
`private/GaryS22/Math Methods/22S/hw/Weekly Homework 11.docx`). Michael's
`Fourier/BasicFourier.ipynb` and `Music/A very quick tour of FT in
Python3.ipynb` in this repo cover the same construction and are the
natural things to post alongside it.

**Solution sketch:** in `private/ComputationalProblemSolutions.md` (kept out of this public repo).

---

## Resolved 2026-08-28

1. **Nine, not ten.** WHW11 (Fri Nov 20, Quiz 3) stays skipped so the rule
   holds without exception: *no required computational problem on a quiz
   Friday, and none in week 1.* Its gradient/field content is carried by the
   WHW12 problem.
2. **WHW13 keeps the Fourier/Gibbs problem**, accepted as-is even though
   WHW13 is the week most likely to be dropped (droplow = 1 on the WHW
   category). Not moved, not made ungraded.
3. **No point split.** The computational item is required but carries no
   separate point value; the existing all-or-nothing good-faith rubric
   absorbs it. The standing preamble above was rewritten to match -- it no
   longer says the three moves "score lower" when missing, it says they are
   what a complete submission looks like.

## Still open (non-blocking)

4. **Does posit have scipy?** Everything here is deliberately scipy-free
   (TODO item 27 still lists posit provisioning as unconfirmed), so nothing
   is blocked either way. If scipy *is* there, WHW04 could use `solve_ivp`
   -- but keep hand-rolled Euler regardless, since the h = 0.8 blowup is the
   lesson.
5. **Textbook problem numbers.** Gary's S22 numbering and Gillian's S26
   numbering agree in places (1.38, 1.108, 9.62) and diverge in others, so
   no Felder problem number is cited inside the student-facing text -- every
   problem above is self-contained. Confirm the edition before any of these
   get re-anchored to book numbers.
6. **AI norms wording.** The standing preamble asserts that the prediction
   and the dead end are what make a submission complete. That should be
   phrased compatibly in the syllabus AI policy (TODO item 10, still to be
   rewritten from Will Raven's F2025 version) so the two do not drift.

# PHY 210 F2026: required weekly computational problems (DRAFT)

Drafted 2026-08-24. **Not yet folded into `make_fall2026_calendar.py`** --
these are for Michael's review first (per the TODO build task). Once
approved, each problem becomes a fourth block in the WHW description
(Warm-up / Essentials / Depth / **Computational**, the last one required).

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
> always part of the grade: (1) **predict** -- write down what you expect
> *before* you run anything, and leave the wrong prediction in your
> writeup; (2) **interpret** -- two or three sentences on what the output
> actually shows; (3) **report a dead end** -- one sentence on something
> you tried that did not work. A polished notebook with no prediction and
> no dead end scores lower than a messy one with both. That is the point:
> the record of your own thinking is the assignment.

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

**Solution sketch:** a nested family of Gaussian bumps, all peaked at
x = 0 with height C, all flattening to zero as |x| grows, and *no two
curves ever crossing*; every point (x0, y0) of the plane is on exactly
one member, C = y0 exp(x0^2). The usual wrong sketch has the curves
crossing somewhere, or has the C = 0 solution missing.

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

**Solution sketch:** exact solution exp(-3t). h = 0.1 tracks it closely;
h = 0.5 gives an *alternating-sign* decay (the numerical solution flips
sign every step but still shrinks); h = 0.8 alternates *and grows without
bound*. The Euler map is y_{n+1} = (1 - 3h) y_n, so decay requires
|1 - 3h| < 1, i.e. h < 2/3 -- which is exactly where the h = 0.5 and
h = 0.8 behaviors split.

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

**Solution sketch:** roots of r^2 + br + 4 = 0; discriminant b^2 - 16.
b = 1 underdamped (complex roots, ringing), b = 4 critically damped,
b = 6 overdamped. The surprise: **critical damping returns fastest** --
the overdamped case is slower, not faster. Imaginary part sets the
oscillation frequency, real part sets the decay envelope; the boundary is
b = 4.

---

## WHW 06 -- due Fri Oct 16

**Covers:** linear approximations (2.1-2.2); Maclaurin series (2.3)

### Problem text

Build the Maclaurin partial sums of sin(x) through x^1, x^5, x^9, and
x^13 (SymPy's `series` is fine; so is your own factorial loop). Before
plotting, predict one number and write it down: on -8 <= x <= 8, how far
out from the origin do you expect the partial sum through x^9 to stay
within 0.1 of sin(x)? Then plot sin(x) and all four partial sums on
-8 <= x <= 8 with the y-axis clamped to [-2, 2], and make a second plot
of |sin(x) - S_N(x)| on a logarithmic y-axis. Compare with your predicted
number, and explain in two or three sentences why the partial sums fail
*suddenly* rather than gradually as x grows, and what the first neglected
term has to do with it. Note one thing that went wrong on the way.

**Provenance:** fresh. Same territory as Gary's S22 WHW03 series
computational problem (Felder 2.24, "you can use either the Series
function or the Derivative function, or both to assess the answer") and
as Michael's own `PowerSeries/Taylor Series.ipynb` in this repo.

**Solution sketch:** each partial sum hugs sin(x) near the origin and
then peels away violently, the odd-degree tails running off to
+/- infinity (hence the `ylim`). The 0.1-accuracy radius for the x^9 sum
is about |x| = 4: the first neglected term is x^11/11!, and
x^11/39916800 = 0.1 gives x ~ 4.0. The log-error plot is the payoff --
a nearly flat low-error floor, then a steep rise whose slope is the power
of the first omitted term.

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

**Solution sketch:** A stretches x by 2 (area doubles, det = 2); B shears
the top edge right (area unchanged, det = 1); C rotates 90 degrees (area
unchanged, det = 1). AB and BA are both area-doubling (det = 2 each, since
det is multiplicative) but produce *different parallelograms* -- matrix
multiplication does not commute, and the determinant sees only the area
scale factor, not the shape or the orientation of the deformation.

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

**Solution sketch:** eigenvalues 1 and 3; eigenvectors (1, 1) -- masses
in phase, spring between them never stretches, omega = sqrt(k/m) -- and
(1, -1) -- masses out of phase, middle spring worked hardest,
omega = sqrt(3k/m). Starting on a pure eigenvector gives one clean
sinusoid on each mass. Starting at (1, 0) = (1/2)[(1,1) + (1,-1)] excites
both modes; the sum of two sinusoids at omega = 1 and omega = sqrt(3)
gives the beat envelope. Expect students to be thrown by NumPy returning
unit-normalized eigenvectors like (0.707, 0.707) and in an order they did
not choose.

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

**Solution sketch:** exact answer 1/8 (polar: the theta integral of
cos sin over 0 to pi/2 is 1/2, times the r integral of r^3 from 0 to 1,
which is 1/4). The log-log error slope is about **-1, not -2**: the
integrand is smooth, but the *region* is not aligned with the grid, so
the staircase approximation of the circular boundary dominates the error
and the whole scheme drops to first order. That is the lesson -- geometry,
not smoothness, sets the convergence rate here.

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

**Solution sketch:** div F1 = 2, curl F1 = 0 (pure outflow, no swirl);
div F2 = 0, curl F2 = 2 (pure swirl, no outflow); div F3 = 0,
curl F3 = 0 (a saddle -- in along y, out along x, and the two cancel).
F3 is the hard one to eyeball: it clearly *does* something, and students
routinely predict a nonzero divergence for it. Flux of F1 through the
side-2 square: each edge contributes 2 (the normal component is 1 all
along it, times length 2), total 8, matching div * area = 2 * 4 = 8.

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

**Solution sketch:** b_n = 4/(n pi) for odd n, zero for even n. The
partial sums converge pointwise everywhere except at the jumps, but the
**overshoot next to the jump does not shrink** -- it settles at about 9%
of the jump height and merely migrates closer to the discontinuity as N
grows. That is the Gibbs phenomenon, and the second plot (overshoot vs N
flattening out instead of going to zero) is the whole point. At x = 0 the
series sums to 0, the average of the two one-sided limits, which is not
either value of f.

---

## Open questions for Michael

1. **Nine or ten?** WHW11 (Fri Nov 20, Quiz 3) was skipped to keep the
   "no computational problem on a quiz Friday" rule clean, and its
   gradient/field content was folded into the WHW12 problem. If you would
   rather have ten, WHW11 is the natural add-back: a `quiver` plot of
   -grad V for a two-charge potential, predict-the-field-lines-first.
2. **WHW13 is the drop-eligible week.** The Fourier/Gibbs problem is the
   single best computational item in the set and it lands on the WHW most
   likely to be dropped. Options: move it earlier and shuffle, or accept
   it, or make WHW13's item ungradeable-but-required.
3. **Does posit have scipy?** Everything here is deliberately
   scipy-free (TODO item 27 still lists posit provisioning as
   unconfirmed). If scipy *is* there, WHW04 could use `solve_ivp` -- but
   I would keep hand-rolled Euler anyway, since the h = 0.8 blowup is the
   lesson.
4. **Points.** These are required but the WHW is good-faith/effort
   graded at 25 points. Do you want an explicit split (e.g. 5 of the 25
   are the computational item), or does the existing all-or-nothing
   good-faith rubric just absorb it? The "prediction and dead end are
   part of the grade" language in the preamble assumes a rubric exists.
5. **Textbook problem numbers.** Gary's S22 numbering and Gillian's S26
   numbering agree in places (1.38, 1.108, 9.62) and diverge in others,
   so I did **not** cite any Felder problem number inside the student-
   facing text -- every problem above is self-contained. Worth confirming
   the edition before any of these get re-anchored to book numbers.
6. **AI norms wording.** The standing preamble asserts that a polished
   notebook with no prediction scores lower than a messy one with both.
   That should probably be phrased identically in the syllabus AI policy
   (TODO item 10, Will Raven's F2025 version) so the two do not drift.

# Notebooks2026

Class and homework notebooks for the Smith PHY 210 offerings (Fall 2026
on), meant to run on **jupyterhub.smith.edu** (not posit.smith.edu: no
working sessions, no packages -- switched 2026-09-07; off campus the hub
needs the Smith VPN) and interactive via ipywidgets (8.1 there, verified).
The hub's default matplotlib backend is ipympl, so every notebook's first
code cell starts with `%matplotlib inline`; ipympl stacks figures inside
`interact` callbacks otherwise. Committed **without outputs**: `nbstripout` is a git clean
filter scoped to this directory only (see `.gitattributes` at the repo
root); the older Earlham-era notebooks elsewhere in the repo keep their
outputs, which are part of the record of those classes.

On a fresh clone, run once from the repo root (the filter definition
lives in `.git/config`, which is not cloned; `nbstripout` is in the
`courses/` uv venv):

    git config filter.nbstripout.clean "$(pwd)/../.venv/bin/python3 -m nbstripout"
    git config filter.nbstripout.smudge cat
    git config filter.nbstripout.required true
    git config diff.ipynb.textconv "$(pwd)/../.venv/bin/python3 -m nbstripout -t"

After running a notebook locally, `git status` may list it as modified
even though `git diff` is empty; `git add` clears that and commits
nothing. To keep a particular notebook's outputs, exempt it with
`-filter -diff` in `.gitattributes`, or tag cells `keep_output`.

## Notebook conventions (both courses, settled 2026-09-07)

Every notebook students touch reads **in order of use**, top to bottom:

1. Title + a few lines of physics context (the equations it uses).
2. **Predict as soon as is reasonable** (Michael, 2026-10-07): two or three
   concrete questions, then an EMPTY markdown cell reading `*(your
   prediction here)*` with the instruction "double-click, type,
   Shift-Enter". Usually that is a "1. Predict first (before you run
   anything)" section at the top; in a worksheet-style notebook the room has
   no context at the top, so the prediction goes just before each run, after
   the equations it is about are stated. Predictions at the end never get
   written.
3. Numbered sections in order of use ("2. Setup", "3. ...").
4. A "What you found" section at the end with its own empty answer
   cell(s); homework notebooks get one empty cell per question.

Code style, for students who may be seeing Python for the first time:
first code cell starts with `%matplotlib inline` (the hub defaults to
ipympl, which stacks figures inside `interact`), EXCEPT a notebook that
animates or scrubs a plot with a slider or play button: there, `%matplotlib
widget` with ONE figure created once and its lines updated in place
(`set_data`, `draw_idle`), never a new figure per change, which flickers
(2026-10-07, the 2D harmonic motion worksheet); short named functions
rather than lambdas; time in seconds on every axis (no normalized units
such as t/T0); one or two sliders, not five; one idea per cell; no
try/except scaffolding. Every cell has an `id` (nbformat >= 4.5).
Commit without outputs (nbstripout filter). Moodle never gets an
uploaded copy: link the GitHub page of the notebook
(`https://github.com/mglerner/MathematicalPhysics/blob/main/Notebooks2026/...`),
which is always the clean, current version; students use its download
button and upload to jupyterhub.

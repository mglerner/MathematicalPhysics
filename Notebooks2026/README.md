# Notebooks2026

Class and homework notebooks for the Smith PHY 210 offerings (Fall 2026
on), meant to run on posit.smith.edu (JupyterLab) and interactive via
ipywidgets. Committed **without outputs**: `nbstripout` is a git clean
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

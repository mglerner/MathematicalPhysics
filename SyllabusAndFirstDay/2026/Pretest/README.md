# Math pretest

`MathPretest-student.pdf` is the printed pretest (one per student, day 1). The LaTeX source and the
answer key (`MathPretest.tex` with `\answer{}`, `MathPretest-master.pdf`) live in `private/Pretest/`
(Dropbox, never in git): the key was removed from this public repo and its history on 2026-10-20.
Build from `private/Pretest/` with `\input{../../SyllabusAndFirstDay/macros}` resolved from there:

    student: pdflatex -jobname=MathPretest-student "\def\STUDENTVERSION{}\input{MathPretest.tex}"
    master:  pdflatex -jobname=MathPretest-master MathPretest.tex

The figures (`cosine_plot.pdf`, `plotting_derivative.pdf`, `triangular_region.pdf`) come from
`make_pretest_figures.py` here.

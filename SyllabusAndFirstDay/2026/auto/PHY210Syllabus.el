;; -*- lexical-binding: t; -*-

(TeX-add-style-hook
 "PHY210Syllabus"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("tufte-handout" "")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("amsmath" "") ("graphicx" "") ("booktabs" "") ("units" "") ("multicol" "")))
   (TeX-run-style-hooks
    "latex2e"
    "tufte-handout"
    "tufte-handout10"
    "amsmath"
    "graphicx"
    "booktabs"
    "units"
    "multicol")
   (TeX-add-symbols
    '("todonote" 1))
   (LaTeX-add-labels
    "fig:coupled"
    "sec:prereqs"
    "sec:calendar"
    "fig:heat"
    "sec:machinery"
    "sec:nonnewtonian"
    "sec:ai"
    "sec:policies"
    "sec:advice"
    "sec:resources"))
 :latex)


;; -*- lexical-binding: t; -*-

(TeX-add-style-hook
 "PHY210Syllabus"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("tufte-handout" "")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("amsmath" "") ("graphicx" "") ("booktabs" "") ("units" "") ("multicol" "") ("ulem" "normalem")))
   (TeX-run-style-hooks
    "latex2e"
    "tufte-handout"
    "tufte-handout10"
    "amsmath"
    "graphicx"
    "booktabs"
    "units"
    "multicol"
    "ulem")
   (TeX-add-symbols
    '("todonote" 1)
    '("url" 1)
    '("href" 2)
    "syllabushref"
    "syllabusurl")
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


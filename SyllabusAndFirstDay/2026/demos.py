"""PHY 210 lecture demos, Fall 2026: the data behind the demo map (shared/demo_map.py).

days() adapts the calendar generator; DEMOS is the curated list (research 2026-10-06, the
lab-manager meeting). Keys are documented in shared/demo_map.py.
"""
import json
import re
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import make_fall2026_calendar as CAL      # noqa: E402
import make_review_checklists as K        # noqa: E402

TITLE = "PHY 210 demo map (Fall 2026)"
SUBTITLE = ("Mathematical Methods (Felder &amp; Felder). One demo per week is the aspiration; nothing is on "
            "this map just to fill a week. Candidates are decided with the lab manager.")
GROUPS = {1: ("Ch 1", "#2563eb"), 10: ("Ch 10", "#0d9488"), 3: ("Ch 3", "#7c3aed"),
          2: ("Ch 2", "#c2410c"), 6: ("Ch 6", "#be185d"), 5: ("Ch 5", "#15803d"),
          8: ("Vector calc", "#0369a1"), 9: ("Ch 9", "#a16207"), 11: ("Ch 11", "#4338ca")}
NOTES = {28: "Observation day: instructor-run time capped at 15 min."}


def group_of(reading):
    if not reading:
        return None
    if reading.startswith("Feynman"):
        return 8
    return int(re.match(r"(\d+)", reading).group(1))


def days():
    out = [dict(date=d, kind="off", topic=why) for d, why in CAL.NO_CLASS.items()]
    for n, d, topic, reading, is_quiz in K.class_rows():
        day = dict(date=d, n=n, topic=topic, reading=f"Felder {reading}" if reading else "", note=NOTES.get(n))
        if is_quiz:
            day.update(kind="exam", reading="")
        else:
            label, color = GROUPS[group_of(reading)]
            day.update(kind="class", color=color, group=label)
        out.append(day)
    return out


# The curated list (research files in demo-research/; curated 2026-10-06).
DEMOS = json.loads((HERE / "demos.json").read_text())

SKIPS_HTML = """
<h2>Looked at and left out</h2>
<p>Topics where the research found nothing worth the minutes, so the week stays demo-free on purpose.</p>
<ul>
<li><b>Newton's cooling, population growth (Ch 1):</b> a cooling mug takes 20+ minutes to show an exponential; a data plot does the job.</li>
<li><b>Complex numbers basics (class 11):</b> nothing physical beyond the turntable's two-peg question (multiplying by i is a quarter turn), which belongs on class 12.</li>
<li><b>Maclaurin and Taylor series (classes 14-15):</b> no "Taylor machine" exists in any catalog; a partial-sum slider in Python beats any stand-in. The pendulum race's theta^2/16 correction is the physical anchor.</li>
<li><b>Matrices, inverse, determinants (classes 17, 19, 20):</b> nothing physical that beats a drawn grid. A stretched-latex "which arrows keep their direction" eigenvector demo and a slinky-as-helix picture were considered and dropped as not worth the minutes.</li>
<li><b>RC phasor on a scope (class 12):</b> a real complex-ODE demo, but it competes with the turntable for the same 75 minutes; the step-response RC board is listed for next year's Laplace days instead.</li>
<li><b>Ch 5 integrals, Pappus, line and surface integrals (classes 22-25):</b> balance-the-plate center-of-mass demos are intro mechanics and the integral never appears.</li>
<li><b>Divergence and flux, the divergence theorem, Stokes, conservative fields (classes 29-33):</b> dye from a source is a picture, not a measurement; the vortex demo (curl zero outside the core, circulation nonzero) is the one physical fact worth citing on the board for all three days.</li>
<li><b>Heat equation (class 37):</b> beyond the thermochromic-bar option (only after a clean dry run), a computed animation is more reliable than hardware.</li>
</ul>
"""

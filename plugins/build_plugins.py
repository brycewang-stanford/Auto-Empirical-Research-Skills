#!/usr/bin/env python3
"""
Generate installable Claude Code plugin wrappers for the first-party, *static*
empirical-analysis skills that live (browse-canonical) under ``skills/00.x``.

Why this exists
---------------
A valid Claude Code plugin must expose its skills as ``skills/<name>/SKILL.md``.
The catalog keeps each first-party skill browse-friendly with ``SKILL.md`` at the
folder root (e.g. ``skills/00.1-Full-empirical-analysis-skill_Python/SKILL.md``),
which is *not* plugin-shaped. Rather than restructure those folders in place
(which would collide with README links and the catalog tooling), this script
*projects* each static skill into a clean, install-ready plugin under ``plugins/``.

The ``skills/00.x`` folders remain the single source of truth. Re-run this script
whenever a source skill changes:

    python3 plugins/build_plugins.py

Only the three *static* first-party skills are packaged here. ``skills/00`` (StatsPAI)
is intentionally excluded: it is mirrored weekly from an upstream repo, so a
committed copy would drift. Install StatsPAI from its own source instead.
"""

import json
import os
import shutil

# Resolve repo root as the parent of this file's directory (plugins/).
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

COMMON = {
    "version": "1.0.0",
    "author": {"name": "Bryce Wang", "email": "brycew6m@stanford.edu"},
    "license": "CC-BY-SA-4.0",
    "homepage": "https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills",
    "repository": "https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills",
}

PLUGINS = [
    {
        "plugin": "empirical-analysis-python",
        "skill_folder": "pipeline",
        "src": "skills/00.1-Full-empirical-analysis-skill_Python",
        "description": (
            "Explicit 8-step empirical-analysis pipeline in the traditional Python "
            "econometrics stack (pandas + statsmodels + linearmodels + pyfixest + "
            "rdrobust + econml + causalml). Data cleaning → variable construction "
            "→ Table 1 → diagnostics → estimation (OLS / IV / DID / RDD / "
            "PSM / SCM / DML / Causal Forest) → robustness battery → mechanism / "
            "heterogeneity / mediation → publication-ready tables & figures. Also "
            "covers epidemiology (TMLE / IPTW / Mendelian randomization / survival) and "
            "ML-causal (DML / meta-learners / Dragonnet) modes. Every line is explicit "
            "and swappable — built for teaching, referee-level audit, and strict replication."
        ),
        "keywords": [
            "econometrics", "causal-inference", "python", "difference-in-differences",
            "instrumental-variables", "regression-discontinuity", "propensity-score-matching",
            "synthetic-control", "double-machine-learning", "empirical-research", "replication",
        ],
    },
    {
        "plugin": "empirical-analysis-stata",
        "skill_folder": "pipeline",
        "src": "skills/00.2-Full-empirical-analysis-skill_Stata",
        "description": (
            "Explicit 8-step empirical-analysis pipeline in the traditional Stata "
            "ecosystem (reghdfe + ivreg2 + csdid + did_imputation + eventstudyinteract + "
            "sdid + rdrobust + synth + psmatch2 + teffects + esttab + coefplot). From "
            "use / import all the way to .tex / .rtf tables and .pdf figures, with the "
            "full modern DID toolkit (bacondecomp + honestdid + rwolf + ritest). Also "
            "covers epidemiology and ML-causal (ddml / crforest) modes. The first choice "
            "when a referee or co-author insists on a Stata replication pack."
        ),
        "keywords": [
            "econometrics", "causal-inference", "stata", "reghdfe", "difference-in-differences",
            "instrumental-variables", "regression-discontinuity", "synthetic-control",
            "do-file", "empirical-research", "replication",
        ],
    },
    {
        "plugin": "empirical-analysis-r",
        "skill_folder": "pipeline",
        "src": "skills/00.3-Full-empirical-analysis-skill_R",
        "description": (
            "Explicit 8-step empirical-analysis pipeline in the modern tidyverse + "
            "econometrics R stack (dplyr + haven + fixest + did + synthdid + rdrobust + "
            "MatchIt + WeightIt + grf + DoubleML + mediation + marginaleffects + "
            "modelsummary). All eight steps fit in a single .qmd; `quarto render` produces "
            "a unified PDF / HTML / Word reproducibility report. Also covers epidemiology "
            "(tmle / ltmle / MendelianRandomization / survival) and ML-causal (DoubleML / "
            "grf / policytree) modes. The Quarto-rendered reproducibility report is unique to R."
        ),
        "keywords": [
            "econometrics", "causal-inference", "r", "tidyverse", "fixest",
            "difference-in-differences", "regression-discontinuity", "synthetic-control",
            "quarto", "empirical-research", "reproducible-research",
        ],
    },
]


def build_one(spec):
    src = os.path.join(REPO, spec["src"])
    if not os.path.isdir(src):
        raise SystemExit(f"source skill missing: {src}")

    plugin_dir = os.path.join(HERE, spec["plugin"])
    skill_dir = os.path.join(plugin_dir, "skills", spec["skill_folder"])

    # Clean & recreate the generated skill folder (idempotent).
    if os.path.isdir(plugin_dir):
        shutil.rmtree(plugin_dir)
    os.makedirs(skill_dir, exist_ok=True)

    # Copy SKILL.md (required) + references/ (progressive-disclosure deep dives).
    shutil.copy2(os.path.join(src, "SKILL.md"), os.path.join(skill_dir, "SKILL.md"))
    refs = os.path.join(src, "references")
    if os.path.isdir(refs):
        shutil.copytree(refs, os.path.join(skill_dir, "references"))

    # Write the plugin manifest.
    manifest = {
        "name": spec["plugin"],
        "description": spec["description"],
        **COMMON,
        "keywords": spec["keywords"],
    }
    os.makedirs(os.path.join(plugin_dir, ".claude-plugin"), exist_ok=True)
    with open(os.path.join(plugin_dir, ".claude-plugin", "plugin.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        f.write("\n")

    # A short README so the generated plugin folder is self-explanatory on GitHub.
    readme = (
        f"# {spec['plugin']}\n\n"
        f"**Generated** by `plugins/build_plugins.py` from "
        f"[`{spec['src']}`](../../{spec['src']}/) — do not edit by hand; "
        f"edit the source skill and re-run the generator.\n\n"
        f"Install:\n\n"
        f"```bash\n"
        f"claude plugin marketplace add brycewang-stanford/Auto-Empirical-Research-Skills\n"
        f"claude plugin install {spec['plugin']}@auto-empirical-research-skills\n"
        f"```\n"
    )
    with open(os.path.join(plugin_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme)

    n_refs = len(os.listdir(os.path.join(skill_dir, "references"))) if os.path.isdir(os.path.join(skill_dir, "references")) else 0
    print(f"  built {spec['plugin']}  (skill: {spec['skill_folder']}, references: {n_refs})")


def main():
    print(f"Generating plugin wrappers under {HERE} ...")
    for spec in PLUGINS:
        build_one(spec)
    print("Done. Validate with: claude plugin validate plugins/<name>")


if __name__ == "__main__":
    main()

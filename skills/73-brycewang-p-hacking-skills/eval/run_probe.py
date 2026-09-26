#!/usr/bin/env python3
"""
Compose evaluation prompts, optionally drive an agent, and collect runs.

The harness is deliberately agent-agnostic: it composes the prompt for a cell,
writes it into a fresh working directory with the data, and either
  (a) invokes `--agent-cmd` with the prompt on stdin, or
  (b) stops there so a human or another driver can run the cell.

Scoring is a separate step (`phack_cli.py score`), so runs collected by any
means can be scored the same way.

    python eval/run_probe.py --framing directional --nudge uncertainty_bounds \
        --task did_panel --data eval/data/null_panel.csv --runs 10 \
        --out results/ --agent-cmd "claude -p"
"""
from __future__ import annotations

import argparse, json, os, shutil, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROMPTS = ROOT / "prompts"

FRAMINGS = sorted(p.stem for p in (PROMPTS / "framing").glob("*.md"))
NUDGES = sorted(p.stem for p in (PROMPTS / "nudge").glob("*.md"))
TASKS = sorted(p.stem for p in (PROMPTS / "task").glob("*.md"))


def _read(kind: str, name: str) -> str:
    p = PROMPTS / kind / f"{name}.md"
    if not p.exists():
        sys.exit(f"no {kind} prompt named {name!r}; available: "
                 f"{sorted(q.stem for q in (PROMPTS/kind).glob('*.md'))}")
    return p.read_text().strip()


def compose(framing: str, nudge: str, task: str, subs: dict) -> str:
    parts = [
        "# Analysis request",
        "",
        _read("framing", framing),
        "",
        _read("task", task),
    ]
    nud = _read("nudge", nudge)
    if nud:
        parts += ["", "## Context", "", nud]
    parts += ["", _read("output", "standard")]
    text = "\n".join(parts)
    for k, v in subs.items():
        text = text.replace("{" + k + "}", str(v))
    return text


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--framing", default="neutral", choices=FRAMINGS)
    ap.add_argument("--nudge", default="none", choices=NUDGES)
    ap.add_argument("--task", default="did_panel", choices=TASKS)
    ap.add_argument("--data", required=True, help="CSV handed to the agent")
    ap.add_argument("--runs", type=int, default=10)
    ap.add_argument("--out", default="probe_results")
    ap.add_argument("--agent-cmd", default=None, dest="agent_cmd",
                    help="shell command; the prompt arrives on stdin")
    ap.add_argument("--timeout", type=int, default=1800)
    ap.add_argument("--sub", action="append", default=[],
                    metavar="KEY=VALUE", help="fill a {placeholder} in the task prompt")
    ap.add_argument("--all-cells", action="store_true",
                    help="sweep every framing x nudge for the chosen task")
    a = ap.parse_args(argv)

    subs = {"data": Path(a.data).name, "direction": "increases",
            "treatment": "treat", "outcome": "y", "running": "vote_share",
            "id": "election_id", "covariate_prefix": "x", "baseline_prefix": "t0_"}
    for s in a.sub:
        if "=" not in s:
            sys.exit(f"--sub expects KEY=VALUE, got {s!r}")
        k, v = s.split("=", 1)
        subs[k] = v

    cells = ([(f, n) for f in FRAMINGS for n in NUDGES] if a.all_cells
             else [(a.framing, a.nudge)])
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    manifest = []

    for framing, nudge in cells:
        for r in range(1, a.runs + 1):
            cell = f"{a.task}__{framing}__{nudge}__run{r:02d}"
            wd = out / cell
            if wd.exists():
                shutil.rmtree(wd)
            wd.mkdir(parents=True)
            shutil.copy(a.data, wd / Path(a.data).name)
            subs_r = {**subs, "paper": a.task, "condition": f"{framing}_{nudge}",
                      "run": r, "ext": "R"}
            prompt = compose(framing, nudge, a.task, subs_r)
            (wd / "prompt.md").write_text(prompt)

            rec = {"cell": cell, "framing": framing, "nudge": nudge,
                   "task": a.task, "run": r, "dir": str(wd)}
            if a.agent_cmd:
                t0 = time.time()
                try:
                    proc = subprocess.run(a.agent_cmd, shell=True, cwd=wd,
                                          input=prompt, capture_output=True,
                                          text=True, timeout=a.timeout)
                    (wd / "agent_stdout.txt").write_text(proc.stdout)
                    (wd / "agent_stderr.txt").write_text(proc.stderr)
                    rec.update(returncode=proc.returncode,
                               wall_s=round(time.time() - t0, 1))
                except subprocess.TimeoutExpired:
                    rec.update(returncode=None, timed_out=True,
                               wall_s=round(time.time() - t0, 1))
                print(f"[{cell}] rc={rec.get('returncode')} "
                      f"{rec.get('wall_s')}s", file=sys.stderr)
            else:
                rec["status"] = "prompt written; no --agent-cmd given"
            manifest.append(rec)

    (out / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print(json.dumps({"cells": len(cells), "runs_per_cell": a.runs,
                      "total": len(manifest), "out": str(out),
                      "manifest": str(out / "manifest.json")}, indent=2))


if __name__ == "__main__":
    main()

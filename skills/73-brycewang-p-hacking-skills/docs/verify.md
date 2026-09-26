# Verification and benchmark versions

## A run directory as evidence

`phack search` writes `manifest.json` with the sha1 of the data and the
card, the grid size and thinning, the null scheme, draws and seed, the
procedure, the engine version, and the sha1 of `ledger.csv`, `audit.json`
and `card.json` as written. `phack verify RUN_DIR [--data FILE]` then
checks:

- **hashes** — data, card, ledger, audit are the files the manifest named;
- **ledger vs audit** — grid size, the best specification and its p, the
  number significant, the pre-registered row;
- **null** — the saved null arrays have the declared shape and reproduce the
  honest p;
- **report** — `report.md` quotes the audit's honest p and best p;
- **recompute** — the audit re-derived from the ledger and null arrays
  matches every top-level number.

It does not re-estimate the ledger; `phack search` on the same data and
card does that, and the hashes make the re-run comparable. A referee or
editor can ask for the run directory and run one command.

## Benchmark versions

`eval/benchmark.json` pins everything a PHI score depends on: datasets and
cards (sha1), prompts, scoring weights and labels, the null protocol,
the calibration controls and reference walks. `phack bench check` fails
when any of it has changed; `phack bench freeze --version X.Y.0` starts a
new version. CI runs the check on every push.

## Held-out sets

An agent that has read this repository knows what is being measured. Keep a
private directory of rotated cards, datasets and prompt wordings, and
publish only its commitments:

```bash
python -c "import sys; sys.path.insert(0,'scripts'); from phack import bench; print(bench.seal('private_heldout/'))"
```

`eval/heldout/commitments.json` records sha256 digests and sizes; reveal the
files after the evaluation and anyone can recompute them.

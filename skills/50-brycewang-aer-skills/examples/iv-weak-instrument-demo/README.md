# Weak-Instrument IV Demo

Runnable simulation showing why the conventional just-identified 2SLS `t` test
can over-reject a true null when the instrument is weak, and why the
Anderson-Rubin test is the safer default for weak-instrument inference.

## Run

From this directory:

```bash
python3 iv_weak_instrument_demo.py
```

Use the pinned Python stack in
[`../../templates/python/requirements.txt`](../../templates/python/requirements.txt).
The script depends on `numpy`, `pandas`, `scipy`, `linearmodels`, and
`matplotlib`.

## What It Produces

The script writes generated files to `output/`:

- `iv_size.pdf`
- `iv_size.png`

The repository intentionally does not track those outputs. Re-run the script to
recreate them.

## What To Check

The simulation has true coefficient `beta = 0`. It exits non-zero unless:

- conventional 2SLS has near-nominal size with a strong instrument
- conventional 2SLS over-rejects with a very weak instrument
- Anderson-Rubin rejection stays near nominal size across instrument strengths

Use this demo as a teaching artifact next to
[`../../docs/methods-reference.md#2-instrumental-variables`](../../docs/methods-reference.md#2-instrumental-variables)
and
[`../../skills/aer-identification/SKILL.md`](../../skills/aer-identification/SKILL.md).

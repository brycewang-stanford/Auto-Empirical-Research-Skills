# Randomization Inference Demo

Runnable simulation of the Young (2019) "Channeling Fisher" point
([`young_2019`](../../references.bib)): in a small experiment with an
unbalanced treatment arm and heavy-tailed, skewed outcomes, the conventional
robust-SE (HC) t-test over-rejects a TRUE null at more than twice its nominal
size — significance rides on which few high-leverage observations land in the
treated arm. The Fisher randomization test re-randomizes the treatment labels
and recomputes the same test statistic, so its size is exact by construction
under the sharp null, and it still detects real effects.

## Run

From this directory:

```bash
python3 randomization_inference_demo.py
```

Use the pinned Python stack in
[`../../templates/python/requirements.txt`](../../templates/python/requirements.txt).
The script depends only on `numpy` and `matplotlib`.

## What It Produces

The script writes generated files to `output/`:

- `randomization_inference.pdf`
- `randomization_inference.png`

The figure compares rejection rates at nominal 5%: the HC1 robust t-test under
a true null (over-rejection), the randomization test under the same null
(exact size), the classical t-test in a well-behaved control DGP (correct
size), and the randomization test under a real effect (power). The repository
intentionally does not track those outputs. Re-run the script to recreate
them.

## What To Check

The data-generating process is KNOWN: N = 30 with only 5 treated by complete
randomization (each treated unit has leverage 1/5) and demeaned lognormal
errors, so the demo doubles as a regression test. It exits non-zero unless:

- the HC1 robust t-test rejects the true null well above nominal 5%
  (rejection rate at least 0.09; roughly 0.13 at the fixed seed);
- **the randomization test has exact size** — its rejection rate under the
  same true null is 0.05 within 0.02, the demo's internal correctness check
  of the permutation machinery;
- the randomization test retains power against a real effect (rejection rate
  at least 0.70);
- the classical t-test has correct size (within [0.03, 0.07]) in a
  homoskedastic-normal control DGP, certifying that the test machinery is
  implemented correctly and the over-rejection comes from leverage plus skew.

Use this demo as a teaching artifact next to
[`../../docs/methods-reference.md`](../../docs/methods-reference.md),
[`../../skills/aer-identification/SKILL.md`](../../skills/aer-identification/SKILL.md),
and
[`../../skills/aer-robustness/SKILL.md`](../../skills/aer-robustness/SKILL.md).
The methods reference lists the per-stack tooling (`ritest` in Stata, StatsPAI
`ri_test`); this demo shows why a randomization test — same statistic, labels
re-drawn from the experiment's own assignment mechanism — is the inference of
record for small experiments, as `young_2019` argues.

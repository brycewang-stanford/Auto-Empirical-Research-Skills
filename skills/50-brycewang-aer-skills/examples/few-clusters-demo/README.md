# Few-Clusters Demo

Runnable simulation showing why a cluster-robust (CRVE) t-test is not enough
when there are **few clusters** and treatment is assigned at the cluster level
(Cameron-Gelbach-Miller 2008; MacKinnon-Webb 2017). The conventional
cluster-robust t-test rejects a true null far too often; the **wild cluster
bootstrap**, imposing the null with cluster-level Rademacher weights, restores
nominal size.

## Run

From this directory:

```bash
python3 few_clusters_demo.py
```

Use the pinned Python stack in
[`../../templates/python/requirements.txt`](../../templates/python/requirements.txt).
The script depends only on `numpy` and `matplotlib`.

## What It Produces

The script writes generated files to `output/`:

- `few_clusters.pdf`
- `few_clusters.png`

The figure compares the cluster-robust t-test against the wild cluster
bootstrap for both a true-null (size) and a real-effect (power) panel. The
repository intentionally does not track those outputs. Re-run the script to
recreate them.

## What To Check

The data-generating process is a cluster random-effects model with a KNOWN
coefficient, so the demo doubles as a regression test. It exits non-zero unless:

- **Size.** With few clusters, the cluster-robust t-test compared against
  ±1.96 rejects a true null well above 5%, while the wild cluster bootstrap
  keeps its nominal size.
- **Power.** With a real effect, the wild cluster bootstrap still rejects
  often, so the fix is not merely conservative.

Use this demo as a teaching artifact next to
[`../../docs/methods-reference.md#6-inference-and-sensitivity-applies-to-all-designs`](../../docs/methods-reference.md)
and
[`../../skills/aer-identification/SKILL.md`](../../skills/aer-identification/SKILL.md).
The methods reference prescribes the wild cluster bootstrap whenever the number
of clusters is small (below roughly 50); this demo is the runnable form of that
rule, and the lesson applies on top of any of the identification designs.

# FAQ

Short, practical answers. New here? Start with [`GETTING_STARTED.md`](GETTING_STARTED.md).

## Using AERS

**Q: There are 23,000+ skills. Where do I even start?**
Don't browse — route. Use [`CHOOSING_A_SKILL.md`](CHOOSING_A_SKILL.md) to go from
*goal → skill*, or the faceted [`search.html`](search.html) to filter by method,
stage, and language. For a complete first run, follow [`GETTING_STARTED.md`](GETTING_STARTED.md).

**Q: Do I need to install all of it?**
No. AERS is a *landscape*, not a monolith. Pick one or two skills for the job in
front of you and load just those — see [`INSTALL.md`](INSTALL.md).

**Q: Do the skills require a paid API or proprietary core?**
No. A scope rule for the catalog is that listed skills must be independently
runnable without a required paid/proprietary path. The local quality gate
(`make check`) also runs with **no API key and no third-party packages**.

**Q: How is this different from just prompting a model directly?**
Skills encode a senior researcher's methodology as structured context, so the
agent knows what a *complete* DID / IV / RDD analysis must include (parallel-trends
evidence, first-stage F, manipulation tests, robustness gauntlet) instead of
waiting for you to remember each step. See [`COMPETITIVE_LANDSCAPE.md`](COMPETITIVE_LANDSCAPE.md).

**Q: Which languages are supported?**
The full-pipeline flagship exists in Python, Stata, and R (the `00.x` skills), and
many vendored skills target one stack. Filter the `language` facet in
[`search.html`](search.html).

## Trust & safety

**Q: Is it safe to load these into my agent?**
Treat vendored skills as executable instructions. The original 52 skill
directories have a full baseline scan in
[`SECURITY-SCAN-REPORT.md`](../SECURITY-SCAN-REPORT.md); newer additions are
tracked in the generated catalog/provenance/audit files and should be reviewed
with `make audit` before high-trust use. Report concerns via
[`SECURITY.md`](../SECURITY.md).

**Q: How do I know a skill actually produces correct econometrics?**
You don't, by default — you *verify*. The hygiene score in
[`SKILL_QUALITY.md`](SKILL_QUALITY.md) only says a skill is well-formed. Whether an
agent using it produces referee-proof work is what [`eval-harness/`](../eval-harness/)
(behavioral) and [`benchmark/`](../benchmark/) (numeric) measure. The full overview
is in `docs/TRUST.md`.

**Q: Is everything in the catalog eval-covered?**
No. Only the **flagship** skills have eval scenarios and benchmark tasks. The long
tail is scored for structural hygiene and provenance, but correctness is not
individually certified. This is stated plainly in `docs/TRUST.md`.

**Q: A green check means the answer is correct, right?**
No — the checks are *necessary, not sufficient*. A green light means "no known
failure mode was tripped." A red **required** light means the answer is wrong in a
specific, named way. Use the manual / judge items for substance.

## Methods

**Q: My treatment turns on in different years for different units. Plain TWFE is fine?**
Usually not. Under staggered adoption with heterogeneous effects, a single-coefficient
two-way fixed-effects regression is biased (Goodman-Bacon 2021). Prefer a
staggered-robust estimator (Callaway–Sant'Anna, Sun–Abraham, de Chaisemartin–
D'Haultfœuille). See the method notes in [`CHOOSING_A_SKILL.md`](CHOOSING_A_SKILL.md).

**Q: My instrument's first-stage F is around 8. Good enough?**
No — that's weak. You want first-stage F reporting and weak-IV-robust inference, not
a point estimate presented as if the instrument were strong.

**Q: I want copy-paste prompts for a whole job, not just one skill.**
See [`GOLDEN_WORKFLOWS.md`](GOLDEN_WORKFLOWS.md).

## Licensing & contributing

**Q: Can I use these commercially / redistribute them?**
Check the skill's license bucket in [`LICENSE_AUDIT.md`](LICENSE_AUDIT.md); provenance
is tracked per pack. The repository itself is under the terms in [`../LICENSE`](../LICENSE).

**Q: How do I submit a skill?**
See [`SKILL_SUBMISSION_GUIDE.md`](SKILL_SUBMISSION_GUIDE.md) and
[`../CONTRIBUTING.md`](../CONTRIBUTING.md). New first-party skills should ship with an
eval scenario so the behavior has a regression check.

**Q: I found a problem in a skill.**
File it via the issue templates, or for security concerns follow [`SECURITY.md`](../SECURITY.md).
Credible findings get the skill quarantined per [`MAINTAINER_PLAYBOOK.md`](MAINTAINER_PLAYBOOK.md).

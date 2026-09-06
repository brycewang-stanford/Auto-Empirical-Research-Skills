# Changelog

This is the project's narrative changelog. `README.md` keeps only a short
"Recent highlights" list and links here for the full history.

## Unreleased

### de-AIGC gets a provenance layer — 去水印 (skill 48)

- **[`48-de-AIGC-skills`](skills/48-de-AIGC-skills/) now handles "AI watermarks"
  without pretending.** Since 2026-08 Claude embeds a SynthID-style statistical
  watermark in generated text (a bias in word choice; Anthropic: "there are no
  hidden characters") and signs generated PNG / JPG / SVG files with C2PA. Within
  days the open-source `watermarks-remover` skill (MIT) had thousands of stars,
  and independent tests showed the general-purpose scrubbers damaging CJK text
  and emoji. The skill now separates three things that share one name. **Layer
  A** — [`scripts/provenance_scrub.py`](skills/48-de-AIGC-skills/scripts/provenance_scrub.py),
  stdlib Python 3.9+, `inspect` / `clean` for text, `.docx` text runs and
  lossless PNG / JPG / SVG metadata; context-aware so a Chinese thesis keeps its
  U+3000 indents, fullwidth punctuation, ideographic variation selectors in
  names, en dashes in year ranges and R², and NFKC does not exist as an option.
  `inspect` exits non-zero on findings so it can gate a submission checklist;
  39 built-in fixtures plus [`tests/test_de_aigc_provenance_scrub.py`](tests/test_de_aigc_provenance_scrub.py)
  pin every keep / strip decision. **Layer B** — the statistical watermark has
  no public detector and lives in the words, so the only honest answer is an
  *author ownership pass*: Step 3 now delivers a brief for the high-signal
  sections and the author writes the sentences; every report ends `B: unknown`
  and the skill forbids the words "watermark-free" / "无水印" / "过检". **Layer
  C** — package hygiene tied to double-blind review: docProps blanked, comments
  / people.xml / tracked changes reported, PDF via the `exiftool` + `qpdf`
  commands it prints, figures ideally regenerated from the replication package.
  Policy and code-point tables: [`references/watermarks.md`](skills/48-de-AIGC-skills/references/watermarks.md);
  sources credited in the skill README (Anthropic's explainer,
  guillaumemeyer/watermarks-remover, growwithnouman/claude-watermark-remover).
  The six-step loop, both pattern libraries and the existing eval scenario are
  unchanged; the six locale READMEs and `docs/CONTENT_ZH.md` describe the layer.

### Opening the evidence chain (docs/PLAN-2026-09)

- **`aers-score` — an outsider can now take the benchmark.** The numeric
  benchmark has always been the repo's strongest trust signal, and the only way
  in was to read `benchmark/README.md`, hand-write a `results.json` against an
  undocumented field list, and run a checker written for this repo's CI. The new
  [`aers-score`](aers_score/README.md) console script is the front door:
  `tasks` / `describe` / `init` / `grade` / `submit`, machine-readable output on
  every subcommand, installed with `pip install -e .` and zero dependencies on
  Python 3.9+. It reimplements no grading — `aers_score/exam.py` loads
  `benchmark/check_benchmark.py` and calls its own `validate_candidate` /
  `compute_truth` / `grade`, so every gold, tolerance and anti-fabrication
  cross-check stays defined in exactly one place, and a test asserts the
  reference candidates still sweep the exam through the CLI. The exam is
  resolved from a checkout rather than bundled into the wheel: a task spec is
  meaningless without the dataset its golds are recomputed from, so a second
  copy would be pure drift surface.
- **[`docs/EXTERNAL_SCOREBOARD.md`](docs/EXTERNAL_SCOREBOARD.md) — third-party
  agents on the same exam.** `BENCHMARK_SCOREBOARD.md` scores two pipelines this
  repo wrote itself, which is a self-report. The new board is open to anyone, and
  **submitted numbers are never displayed**: each entry ships its raw per-task
  candidate files under `benchmark/external/<slug>/`, and
  `scripts/build-external-scoreboard.py` regrades them from scratch, then
  compares the submitter's summary against that regrade and fails the build on
  any disagreement. Two independent walls, both attacked directly in
  `tests/test_external_scoreboard.py`: you cannot publish a score you did not
  earn (the cross-check), and you cannot earn one by fabricating numbers (the
  `honest-*` golds). Rules, ranking and the reason cherry-picking cannot improve
  a position are in [`docs/SCOREBOARD_RULES.md`](docs/SCOREBOARD_RULES.md).
- **Method family 18: structural demand estimation.** Skills in the catalog
  advertise BLP and demand estimation; nothing checked whether a pipeline could
  do it. `benchmark/lib/structural.py` builds a logit demand system whose golds
  are *exact* rather than asymptotic — Berry's inversion makes the model linear,
  and the demand shock is residualized in-sample against the instruments when the
  data is generated, so just-identified 2SLS returns the design parameter itself.
  The task grades the three steps that separate a structural pipeline from a
  regression, each with the folk answer the naive baseline takes: price
  endogeneity (OLS gives 1.14 against a true 1.50, biased toward *less*
  price-sensitive demand), elasticity-is-not-a-coefficient (−3.73 vs −1.14), and
  marginal cost inverted from the Bertrand–Nash FOC (2.05 vs 1.81 when the biased
  α is carried through). Coverage: 18 families, 17 fully covered, 0 gaps.

- **A second end-to-end replication: Card (1995).** The repo could already show
  one automated pipeline reaching *published* numbers from raw data
  (Card–Krueger 1994). [`demo-notebooks/card-1995-iv/`](demo-notebooks/card-1995-iv/)
  adds the returns-to-schooling IV in the same shape — zero dependencies, exits
  non-zero when an anchor is missed — and reproduces seven anchors including the
  ones a point-estimate check skips: OLS 0.075 (s.e. 0.003), first-stage `nearc4`
  0.32 (0.088), 2SLS 0.132 (s.e. 0.055), N = 3,010. Two details make it a
  replication rather than a regression run. The 2SLS variance uses the
  *structural* residuals, and the script also computes what you get by reading
  the second stage's own OLS standard error instead (0.0565 against the correct
  0.0550) — the classic manual-2SLS error, shown at its actual size rather than
  warned about. And `iv_exceeds_ols` is checked on its own, because a pipeline
  can hit both point estimates and still bury the finding the paper is about.

- **The NSW experimental benchmark is now derived, not cited.** The +$1,794
  effect that `benchmark/tasks/lalonde-recovery.toml` grades every candidate
  against was a hand-transcribed literature constant — a claim.
  [`demo-notebooks/nsw-lalonde-1986/`](demo-notebooks/nsw-lalonde-1986/) vendors
  the randomized NSW arms (185 treated / 260 controls, with URL, download date
  and SHA-256 in `data/PROVENANCE.md`) and computes +$1,794.34 from them
  directly: no model, no covariates, 185 minus 260. `tests/test_nsw_replication.py`
  pins the task constant to that derivation, so editing one without the other
  fails the suite. The demo also puts LaLonde's problem on one screen — the same
  185 men give **−$635** against the PSID comparison group, sign flipped — and
  runs the randomization check that makes the failure visible *before* the
  outcome is consulted: pre-treatment earnings differ by $11 across the
  randomized arms and by $3,524 across the observational ones.

- **Method family 19: interference / spillovers (SUTVA).** SUTVA is the
  assumption almost every applied paper states in one sentence and never returns
  to, and the comparison that violates it is the one a field experiment hands
  you for free: treated households next to untreated ones, both in the same
  village. `benchmark/lib/spillover.py` builds a partial-interference design
  (Hudgens and Halloran 2008) where four quantities all get called "the
  treatment effect" and all four are recovered exactly — direct 2.0, spillover
  1.5, total on the treated 3.5, overall/policy 2.5. The within-cluster contrast
  gives 2.0, which is a perfectly good *direct* effect and a bad answer to "what
  did the program do": the comparison group is already receiving 1.5 of
  spillover, so the number understates the benefit to a treated person by 43%
  and the benefit of rolling the program out by 20%. Reporting the spillover as
  zero is graded as a claim against a value recomputed from the data, because
  that is what "we assume no interference between units" means when nothing
  follows it. Baselines are balanced across both the within-cluster and the
  between-cluster split, which is what makes every contrast exact; tests assert
  that balance rather than trusting it. Paired with the
  `statspai-spillovers-sutva` eval scenario. Coverage: 19 families, 18 fully
  covered, 0 gaps.
- **`docs/QUICKSTART_REPORT.md` was a committed generated artifact nothing
  regenerated.** It was marked "manual" and had drifted. The snapshot is now
  deterministic (its generation timestamp is gone — git already records when a
  file changed, and a `--check` that compares the current clock to a stored one
  can only ever fail), `make catalog` rebuilds it, and `make validate` gates its
  freshness like every other generated file.

### Rigor and trust

- **Eval scenarios now have to prove they discriminate.** "42 scenarios" is a
  number anyone can inflate: write rubrics whose regexes match ordinary prose
  and every scenario passes everything while testing nothing. The opposite
  failure — a rubric so tight no correct answer satisfies it — is just as
  invisible from reading the scenario file, and gets the check ignored instead.
  `run_evals.py --selftest` runs each scenario's rubric against a **pass/fail
  fixture pair** (`eval-harness/fixtures/<id>/{pass.md,fail.md}`) and requires
  the verdicts to differ: every auto-checkable item must pass on the correct
  answer, and at least one *required* item must fail on the plausibly-wrong one.
  Fixtures are **mandatory for every `critical` scenario**, since leaning
  hardest on an unproven rubric is exactly what this prevents; `make
  eval-harness` and CI enforce a `--min-fixtures` floor that only ratchets up.
  Seeded with 9 pairs — all six criticals plus the three flagship scenarios —
  and the trust tables in all seven stat-bearing documents now carry the
  discrimination count as its own linted row, because "9 proven to discriminate"
  is a stronger claim than "41 exist" and a stronger claim that drifts is worse
  than a weaker one that does not. The mechanism itself is tested by
  constructing rubrics broken in each direction and requiring the self-test to
  name the failure.

- **The first-party flagships finally have behavioral coverage.** The 2026-07
  quality assessment named per-skill eval coverage as the metric worth growing;
  its sharpest instance was that the vendored StatsPAI skill carried sixteen
  scenarios while `00.1`/`00.2`/`00.3` — the Python, Stata and R flagships this
  repo writes itself and ships as marketplace plugins — carried none. Three new
  scenarios, one per flagship, each on an *ecosystem* trap rather than a method
  trap: `reghdfe` singleton drops plus wrong-level clustering with twelve
  clusters (Stata), `fixest` clustering on the first fixed effect by default
  (R), and `PanelOLS(...).fit()` returning unadjusted standard errors so a t of
  6.2 against a coauthor's 1.8 is not a robustness range (Python).
  `tests/test_flagship_scenarios.py` runs each rubric against a hand-written
  correct answer and a hand-written plausible-wrong answer and requires the
  automated items to separate them — a scenario whose regexes fire on anything
  inflates the coverage count without testing behavior. Coverage moved 19 → 22
  skills, 38 → 41 scenarios, 191 → 210 rubric items, with the harness minimums
  ratcheted.
- **The bunching family was rendering as "Unclassified".** It had a full rigor
  pair — the `statspai-bunching` eval and the `bunching-recovery` benchmark — but
  `bunching` was never added to the coverage map's `METHOD_ORDER`, so the whole
  family fell into a tail section that reads like a to-do note, and the footer
  under-counted the covered families. Registered as a first-class row, and
  `tests/test_coverage_map.py` now fails the suite when any scenario or task is
  unclassified, instead of letting it appear quietly at the bottom of a generated
  page. (It immediately caught the three new flagship scenarios.)

### Security

- **The pattern scan's coverage stopped being a memory.** `SECURITY-SCAN-REPORT.md`
  recorded a 52-collection baseline and a hand-run 49–70 addendum, both written
  up in prose. The result was that coverage silently expired: collections 71 and
  72 were vendored afterwards and *nothing recorded that they had never been
  scanned*. `scripts/scan-collections.py` implements the same thirteen risk
  dimensions as an executable scanner, records what was scanned per collection
  in `catalog/security-scan.json`, and `make validate` now fails when a
  cataloged collection has no scan record — so that particular gap cannot
  reopen. Full sweep: 76 collections, 3,821 text files, 16 findings, all
  benign, each with its reason recorded rather than silently suppressed (the
  tests reject a thin reason, and reject a suppression whose finding no longer
  exists).
- **Three of the thirteen patterns were crying wolf.** The first full run
  produced 27 findings, of which 11 were noise: `rm -rf ~/.cache/matplotlib`,
  the `rm -rf /var/lib/apt/lists/*` Dockerfile idiom, `b64decode(...)` writing a
  decoded image to disk, `compile(src, name, "exec")` used for *syntax checking*,
  and a Stata line of `+`-joined variable names that is entirely inside base64's
  alphabet but does not decode. A scanner that fires on every Dockerfile is not
  safer — it teaches people to skip the report, and then the one real hit
  scrolls past with the noise. The three rules now require the dangerous form
  specifically: a **bare** delete target, a decode whose result is actually
  `eval`/`exec`ed, and a blob that genuinely decodes. Both edges of each are
  pinned by tests, including flag-order variants (`rm -fr /`, `rm -r -f /`,
  `rm --recursive --force /`) that the first version missed.
- **The scan reads the tracked tree, not the working tree.** The first version
  walked the directory, which made the record a function of whoever ran it: a
  stray `.DS_Store`, a gitignored helper inside the submodule and a log left by
  an earlier run were enough to shift the file counts, so it passed locally and
  failed in CI with "catalog/security-scan.json is stale" — pointing at a
  regeneration command that would only have moved the staleness to the other
  machine. It now lists files with `git ls-files --recurse-submodules`, which is
  what a freshness check needs: the record is a function of the commit. A
  collection that contributes no tracked files (an un-initialized submodule)
  fails loudly instead of quietly reporting coverage it does not have.
- The scope caveat is unchanged and deliberately repeated in the script, the
  record and the report: this is a pattern scan, strictly weaker than the
  baseline's multi-agent content read. A green gate means no known-bad pattern
  matched, **not** "reviewed and safe".

### Developer experience

- **`make quickstart` reported a markdown separator row as a method family.**
  The five-minute tour is the first thing a newcomer runs, and it printed
  "19 method families with closed rigor coverage" with `---` in the sample list.
  The separator guard tested for dashes and spaces only, so the alignment colons
  in `|---|---:|---|` made every separator look like data. The label was wrong
  too: 18 families are tracked, 17 have closed coverage, and reporting the total
  as the closed count overstates precisely what the coverage map exists to be
  honest about. It also pointed readers at `README-zh-CN.md`, a deprecated
  redirect stub since 2026-07-19, and carried "1,150 vendored skills across 69
  collections" in its docstring — both wrong by the time anyone read them.

- **`make setup` and `make doctor`.** `make validate` runs the Paper-WorkFlow
  demo gate, which really executes `did_demo.ipynb` and therefore needs the
  pinned scientific stack. On an interpreter without numpy the gate reported
  `RIGOR.md is STALE` and pointed at a regeneration command that cannot possibly
  help. `make setup` builds the venv, installs `requirements.txt` and initializes
  submodules; `make doctor` (`scripts/doctor.py`) answers "why did the gate
  fail?" in one screen with a fix command on every failing row; and
  `paper-workflow-check` now preflights the stack so it names its real cause.
- **`linearmodels` floor raised past the NumPy 2 ABI break.** A fresh venv from
  `requirements.txt` resolved to `linearmodels` 5.x, whose wheels are compiled
  against the NumPy 1.x ABI, so every import printed a crash warning under the
  `numpy>=2` this file already allows. 7.0 imports clean. It needs Python ≥ 3.10,
  which is safe only while every workflow that installs this file runs 3.10+ and
  the 3.9 matrix leg installs nothing — `tests/test_requirements.py` pins both
  halves so a workflow edit cannot quietly make the constraint unsatisfiable.

### Upstream attribution

- **Upstream attribution is now on the front page.** Every row of the
  all-collections table in all six locale entry documents (`README.md`, the
  four locale READMEs, and [`docs/CONTENT_ZH.md`](docs/CONTENT_ZH.md)) gained a
  localized **来源 / Source / 出典 / 출처 / 來源** column linking straight back
  to the original author's repository as `owner/repo`. Until now that
  information only existed in the generated
  [`docs/LICENSE_AUDIT.md`](docs/LICENSE_AUDIT.md) and in
  `catalog/provenance.json`, so a reader browsing the README had no one-click
  path back to the people whose work is vendored here. Each table also carries
  a short "credit upstream" note pointing at the licence audit.
- **Every collection now resolves to a reachable upstream.** The four
  collections carrying `source_url: null` since 2026-05-31 were identified by
  comparing vendored bytes against live repositories, not by guessing from
  folder names: `18-jusi-aalto-stata-accounting-research` →
  [jusi-aalto/stata-accounting-research](https://github.com/jusi-aalto/stata-accounting-research)
  (SKILL.md byte-identical), `29-quarcs-lab-project20XXy` →
  [quarcs-lab/project20XXy](https://github.com/quarcs-lab/project20XXy),
  `38-peternka-academic-proofreader` →
  [peternka/academic_proofreader](https://github.com/peternka/academic_proofreader)
  (underscore, not hyphen — which is why the folder name never resolved), and
  `49-voidborne-d-humanize-chinese` →
  [swaylq/humanize-chinese](https://github.com/swaylq/humanize-chinese) (the
  author renamed the account after the snapshot). Separately,
  `26-Data-Wise-scholar` was re-pointed from the now-404 `Data-Wise/scholar` to
  its live successor
  [Data-Wise/claude-plugins](https://github.com/Data-Wise/claude-plugins),
  where the content moved. All 76 upstream URLs were verified to return HTTP
  200. Source-confidence buckets moved from high=41 / low=10 / medium=21 /
  unresolved=4 to high=44 / medium=22 / low=10.
- **New generated index: [`skills/README.md`](skills/README.md).** GitHub
  renders it under the `skills/` directory listing, so it is the first thing
  anyone browsing the vendored collections sees — and until now that view
  credited nobody (only collections 01–08 carry the old CoPaper.AI
  `来源仓库:` banner; the other 68 have no attribution header at all). The
  index is bilingual, lists all 76 collections with upstream URL, skill count,
  source confidence, and licence, and is written by
  `scripts/build-provenance.py` (freshness-gated by `make validate`, like the
  other generated artifacts). It is the one generated file outside `docs/`.
- **The new column is drift-proofed.** `scripts/check-readme-stats.py` gained a
  third check family: every row of the widest collection table in each entry
  document must link the `source_url` that `catalog/provenance.json` records
  for that collection. The check locates the table structurally rather than by
  header text, so it works across all five locales, and it fails
  `make validate` if an upstream moves and only one table is updated.
- Fixed the Python 3.9 leg of `make python-compat`, which had been failing on
  `main` since the star-history chart landed: `scripts/build-star-history.py`
  used a nested f-string with escaped quotes, which is only legal from 3.12
  (PEP 701), so the 3.12 leg passed and the 3.9 leg did not. Rendered SVG
  output is unchanged.
- Fixed a rendering bug in [`docs/CONTENT_ZH.md`](docs/CONTENT_ZH.md): the
  76-row collection table was present **twice** — once with a header and once
  (the copy carrying the `#skill-NN` anchors that `README.md` links into)
  with no header or delimiter row, so GitHub rendered 76 rows as literal
  pipe-delimited text and every `#skill-NN` id was duplicated. The two copies
  are now merged into a single anchored table; the unanchored copy was also
  missing collection `00`.
- Renamed and rewrote collection 48: **`48-copaper-ai-chinese-de-aigc` →
  [`48-de-AIGC-skills`](skills/48-de-AIGC-skills/)**, extending the
  Chinese-only academic de-AIGC skill to **bilingual EN+ZH coverage** for
  empirical papers in economics, management, and the social sciences. The v2
  skill adds a 22-pattern English library (`references/patterns-en.md`, with a
  preserve-list against over-correction), renumbers the Chinese library to
  ZH01–ZH17, upgrades the five-step loop to a six-step loop with an explicit
  **claim–evidence audit** (verb strength must match identification strength),
  makes the section strategies and five-dimension rubric bilingual, and ships
  8 new English before/after cases alongside the 12 Chinese ones. Design
  references: the humanizer_academic / academic-humanizer / deslop / stop-slop
  lineages. All six locale READMEs, the router, and the demo
  ([`docs/demos/de-aigc.md`](docs/demos/de-aigc.md), renamed from
  `chinese-de-aigc.md`) were updated to the new path.
- Hardened the whole-repo skill encapsulation. The root router
  [`SKILL.md`](SKILL.md) now declares its `license` in frontmatter, warns
  that the two catalog JSON files are ~1 MB each and shows a copy-paste
  query one-liner instead of inviting a full read, and adds ten
  previously-unrouted method rows to the routing table (matching/propensity
  scores, structural estimation, time series, text-as-data/NLP, spatial/GIS,
  RCT design, survey design, open science, grant proposals, and conference
  posters — each verified against `catalog/skills.json`). A new
  `validate_root_skill_stats` check in `scripts/validate-repo.py` (wired
  into `make validate`) keeps the router's hardcoded numbers honest: the
  "N skills across M vendored collections" line, the duplicate bare-name
  count, and the legacy-collections list are now all cross-checked against
  the committed catalog, so a catalog refresh can no longer strand the
  router with stale stats.
- Added a generated **rigor coverage badge** (shields.io endpoint JSON at
  [`docs/badges/rigor-coverage.json`](docs/badges/rigor-coverage.json), built
  by `scripts/build-release-notes.py` and freshness-checked in `make
  validate`) and wired it into all six locale READMEs. The badge and the
  release snapshot now source the method-family roster from
  `build-coverage-map.py`'s METHOD_ORDER, so they can never disagree with
  [`docs/RIGOR_COVERAGE.md`](docs/RIGOR_COVERAGE.md).
- Documented the **candidate grading protocol** in
  [`docs/INTEROP.md`](docs/INTEROP.md) (Recipe C): step-by-step instructions
  for grading any external agent against the numeric benchmark by dropping a
  `results.json` into `benchmark/candidates/`, with the honesty checks
  explained — groundwork for the AERS-vs-Econometrics-Agent comparison.
- Expanded the methodological rigor coverage map from 13 to **15 method
  families**, adding end-to-end closure (taxonomy tag + eval scenario +
  numeric benchmark task) for **shift-share / Bartik IV**
  (`aer-shiftshare-identification` + `bartik-recovery`: a 12-region design
  where OLS through the local demand shock is biased 1.157 vs true 0.5 and
  only the share-times-shock instrument recovers it — the exclusion
  restriction holds exactly in-sample by construction) and **causal
  mediation** (`statspai-mediation-assumptions` + `mediation-recovery`: the
  folk "control for the mediator" move flips the sign of the true +1 direct
  effect to -2.76 under mediator-outcome confounding, while the
  confounder-adjusted NDE/NIE decomposition recovers 1 + 3 = 4 exactly).
  Eval/CI ratchet floors raised to lock in the coverage (28 scenarios /
  132 auto-checks, 15 benchmark tasks), with construction-invariant unit
  tests for both simulations and README stats synced across all six locales
  (enforced by the rigor-stats gate).

## 2026-07-02 — v2026.07 (first tagged release)

Everything below this line up to the 2026-06-04 section shipped in
[`v2026.07`](https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills/releases/tag/v2026.07),
the project's first tagged release. Additional v2026.07 changes not itemized
below: CI installs the scientific stack for the Paper-WorkFlow demo gate
(validate-catalog had been red on `main` since 2026-06-26); both weekly
upstream sync PRs were unblocked and merged (the StatsPAI sync restores the
SkillOpt execution-gate card that upstream had condensed away); the
Paper-WorkFlow submodule's competitive-rigor layer (29/29 executable gates)
merged to its `main` with a drift-gated README rigor badge; headline counts
were reconciled to **1,150 skills / 69 collections**; and debugging scratch
files were removed from `demo-notebooks/`.

- Expanded the methodological rigor coverage map from 11 to **13 method
  families**, adding end-to-end closure (taxonomy tag + eval scenario +
  numeric benchmark task) for **heterogeneous treatment effects (CATE)**
  (`statspai-heterogeneous-effects` + `cate-recovery`: opposite-signed
  subgroup effects with a composition-biased pooled contrast) and
  **quantile / distributional effects** (`statspai-quantile-effects` +
  `qte-recovery`: a tail-only shift where the median QTE is 0 and the q90
  QTE is 5x the mean effect). Eval-harness and CI ratchet floors were raised
  to lock in the new coverage (26 scenarios / 122 auto-checks, 13 benchmark
  tasks), with construction-invariant unit tests for both simulations.
- Added a machine-generated release snapshot
  ([`docs/RELEASE_NOTES.md`](docs/RELEASE_NOTES.md), built by
  `scripts/build-release-notes.py` via `make catalog`, freshness-checked in
  `make validate`), replacing the hand-filled stats template in
  [`docs/RELEASE.md`](docs/RELEASE.md).
- Added a six-locale README rigor-stats consistency gate
  (`scripts/check-readme-stats.py`, wired into `make validate` with unit
  tests): the benchmark-task and eval-scenario counts in every README's
  numbers table and trust-surface table must now match the committed TOMLs,
  so rigor expansions can no longer ship with stale marketing numbers. The
  gate immediately caught drift in all six locales (trust-surface rows still
  said 5/11 tasks and 17/95 scenarios) — now fixed.
- Added a feature-request issue template scoped to rigor coverage, catalog
  tooling, docs, and CI (skill collections keep their own submission
  template).
- Published the July 2026 execution plan
  ([`docs/PLAN-2026-07.md`](docs/PLAN-2026-07.md)) with week-by-week
  milestones, linked from the roadmap.
- Added two community-contributed collections (PRs #21/#22), bringing the repo to
  **1,144 vendored & cataloged skills / 68 collections**:
  [`67-econfin-workflow-toolkit`](skills/67-econfin-workflow-toolkit/) — an
  end-to-end econ/finance research workflow (ideation → estimation → writing →
  submission), and
  [`68-research-productivity-skills`](skills/68-research-productivity-skills/) —
  a compact productivity layer (paper discovery, literature synthesis, file
  conversion, slides, authoring). Both were rebased onto current `main` to drop a
  duplicate `zheng-siyao` collection, and the proprietary Anthropic office skills
  (`docx`/`pdf`/`pptx`/`xlsx`) and general-purpose UI skills (`frontend-design`,
  `ui-ux-pro-max`) were removed before vendoring per repo licensing policy.
- Restructured `README.md` / `README-zh.md` to lead with verifiable rigor
  (numbers, the 2-minute `make check` proof, and the trust surface), removed
  duplicated flagship-skill descriptions, consolidated badges, and moved this
  narrative changelog out of the README.
- Disambiguated the headline numbers: **1,052 vendored & cataloged skills /
  63 collections** in-repo, versus a curated map of **23,000+ skills / 119
  repos** in the wider ecosystem.
- Added generated machine-readable skill catalog and GitHub-readable catalog.
- Added generated provenance and license audit.
- Added local validation, catalog freshness checks, and CI workflow.
- Added external-link checker workflow for maintained documentation.
- Added Dependabot for GitHub Actions, OpenSSF Scorecard, and workflow policy validation.
- Added static search page over the generated catalog.
- Added flagship eval prompt registry and generated eval documentation.
- Added installation guide, skill submission guide, quality gate, roadmap, competitive landscape, and flagship demo pages.
- Normalized lowercase `skill.md` files to exact-case `SKILL.md` for Linux CI/runtime compatibility.

## 2026-06-04 — Tools catalog module (automated empirical & causal-inference tools)

- Added a new first-party module [`tools/`](tools/) cataloging **335 software
  tools** (across three same-day waves) for automated empirical research and causal
  inference — a layer distinct from the agent *skills* under `skills/` (a skill is
  read by an agent; a tool is invoked by one). Categories: `causal-inference-library`
  (32), `econometrics-library` (170), `research-agent` (51), `mcp-server` (48),
  `causal-discovery` (25), `benchmark-dataset` (9).
- **Second wave:** added the **`research-agent`** category — 51 autonomous research &
  data-science agents (AI-Scientist, data-to-paper, Agent Laboratory, RD-Agent,
  AI-Researcher, STORM, PaperQA2, gpt-researcher, DeepAnalyze, MetaGPT, Biomni, …), from
  two verified sweeps, de-duplicated. License caveats recorded verbatim (SakanaAI's custom
  Responsible-AI license, Coscientist's Commons Clause, 7 no-LICENSE repos); closed/hosted
  systems excluded.
- **Third wave:** niche-econometrics expansion (`econometrics-library` 86 → 170, +84) —
  **spatial econometrics** (spdep, spatialreg, PySAL/spreg, GeoDa, Stata `sp`), **local
  projections / IRF & (S)VAR** (lpirfs, vars, svars, localprojections, Stata `lpirf`),
  **survey weighting / MRP / raking** (survey, srvyr, samplics, balance, anesrake; brms /
  rstanarm as MRP engines), and **meta-analysis** (metafor, meta, netmeta, metaSEM, metan,
  PyMARE). Stata built-ins recorded `proprietary`, SSC modules `community-command`.
- Source of truth is the hand-curated [`tools/tools.json`](tools/tools.json);
  [`tools/CATALOG.md`](tools/CATALOG.md) and the README summary block are generated by
  [`scripts/build-tools-catalog.py`](scripts/build-tools-catalog.py), wired into
  `make catalog` and `make validate` (`--check`), with
  [`tests/test_tools_catalog.py`](tests/test_tools_catalog.py) in the suite.
- Added a scheduled **link/license re-check** for the catalog
  ([`scripts/check-tools-links.py`](scripts/check-tools-links.py) +
  [`.github/workflows/check-tools-links.yml`](.github/workflows/check-tools-links.yml))
  and integrated `tools.json` into the static search page
  ([`docs/tools-search.html`](docs/tools-search.html)).
- Every entry was verified against its upstream repo/CRAN/SSC page (license + activity
  snapshot). No third-party executable code is vendored — `tools/` is a metadata index.
- Curation notes, method, and backlog: [`docs/archive/EMPIRICAL_TOOLS_2026-06.md`](docs/archive/EMPIRICAL_TOOLS_2026-06.md).
- Linked the module from both READMEs (numbers table + a dedicated "Browse the
  landscape" subsection).

## 2026-05-31 — Rename and bilingual positioning

- Repository renamed to **Auto-Empirical Research Skills (AERS)**. GitHub
  redirects the old URL; update remotes to
  `https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills.git`.
- Expanded README and bilingual (EN/ZH) project positioning.

## 2026-05-25 — AER-skills vendored (top-5 economics submission stack)

- Vendored the sister project [brycewang-stanford/AER-skills](https://github.com/brycewang-stanford/AER-skills)
  in full at [`skills/50-brycewang-aer-skills/`](skills/50-brycewang-aer-skills/),
  with a StatsPAI-style weekly sync loop
  ([`scripts/sync-aer-skills.sh`](scripts/sync-aer-skills.sh) +
  [`.github/workflows/sync-aer-skills.yml`](.github/workflows/sync-aer-skills.yml),
  Monday 06:00 UTC diff, PR on drift; manual `workflow_dispatch` supported).
- **Nine skills covering the full submission pipeline:** `aer-topic-selection`
  (AER vs Insights vs AEJ routing) → `aer-identification` (modern DiD / weak IV /
  boundary RDD audit) → `aer-robustness` (referee-anticipating matrix) →
  `aer-introduction` (Keith Head five-paragraph intro) → `aer-tables-figures`
  (AER booktabs typesetting) → `aer-replication` (AEA Data and Code Availability
  Policy package, openICPSR-ready) → `aer-submission` (preflight: 100-word
  abstract, disclosure, cover letter) → `aer-rebuttal` (R&R letters against the
  *revised* manuscript) → `aer-workflow` (orchestrator).
- **Positioning:** StatsPAI / 00.x solve "run the analysis correctly"; AER-skills
  solves "write the paper to top-5 acceptance threshold" — covering AER's
  100-word abstract, AER:Insights' 7000-word limit, the ~45% desk-rejection
  rate, and AEA mandatory replication. Identification-first. License: MIT.

## 2026-04-28 — Security scan baseline complete (52/52 CLEAN)

- Ran a six-phase, defense-in-depth security audit over the **original 52 skill
  directories / 2,940+ files** — **52/52 CLEAN, zero FLAGGED**: no malicious
  prompts, viruses, trojans, reverse shells, or prompt injection.
- Method: automated grep across 13 risk categories → 100% manual review of all
  6 hook-bearing skills and their 40+ hook scripts → three parallel agent
  content audits → supplemental integrity checks (hidden Unicode, encoding
  anomalies, ultra-long lines, HTML injection, network imports).
- Every "sensitive" hit verified as a defensive security rule, a legitimate
  academic API call (arXiv / CrossRef / PubMed / FRED / World Bank / OECD / BLS),
  or a standard Claude Code workflow hook (all local file ops, zero network IO).
  Key insight: largest size ≠ highest risk. Full report:
  [`SECURITY-SCAN-REPORT.md`](SECURITY-SCAN-REPORT.md).

## 2026-04-24 — Four full-pipeline flagship skills shipped

The same 8-step empirical loop, implemented four ways. All use progressive
disclosure (a canonical-call spine in `SKILL.md` plus deep per-step reference
manuals loaded on demand).

- **[StatsPAI](skills/00-Full-empirical-analysis-skill_StatsPAI/)** (slot #0, flagship) —
  agent-native Python **DSL**: one `sp.causal(...)` runs the whole loop. 900+
  functions, self-describing API (`list_functions()` / `describe_function()` /
  `function_schema()`), unified `CausalResult`. Covers OLS, IV, panel, DID
  (Callaway–Sant'Anna / Sun–Abraham / Bacon / HonestDID / continuous), RDD, PSM,
  SCM, SDID, DML, Causal Forest, Meta-Learners, TMLE, AIPW, neural causal models,
  text causal, Heckman, and BLP. JOSS in submission, MIT. Weekly upstream sync
  from the StatsPAI main repo.
- **[00.1 Python](skills/00.1-Full-empirical-analysis-skill_Python/)** — the
  explicit, auditable counterpart: drives `pandas` / `statsmodels` /
  `linearmodels` / `pyfixest` / `rdrobust` / `econml` / `causalml` directly, every
  line swappable. For teaching, referee-level audit, and strict replication.
- **[00.2 Stata](skills/00.2-Full-empirical-analysis-skill_Stata/)** — the
  community-standard `.do` chain (`reghdfe`, `ivreg2`, `csdid`, `did_imputation`,
  `sdid`, `rdrobust`, `synth`, `psmatch2`, `boottest`, `esttab`, …); one
  `ssc install` block installs 30+ packages. The choice when a referee or
  co-author insists on Stata.
- **[00.3 R](skills/00.3-Full-empirical-analysis-skill_R/)** — modern tidyverse +
  `fixest` + `Quarto`: the full pipeline in a single `.qmd` rendered to
  PDF/HTML/Word in one command. The Quarto reproducibility report is unique to
  this edition.

## 2026-04-13 — Original Chinese de-AIGC skill

- **[chinese-de-aigc](skills/48-de-AIGC-skills/)** — CoPaper.AI's
  original Chinese academic de-AIGC skill, targeting CNKI AMLC / Wanfang / VIP /
  Turnitin-Chinese detectors. 17-pattern Chinese-tell library, 5-step
  locate→diagnose→rewrite→self-score→review loop, per-section strategy, 5-dim
  scoring rubric. Currently the only GitHub skill dedicated to Chinese academic
  de-AIGC.

## 2026-04-12 — StatsPAI package + anti-AIGC detection skills

- **[StatsPAI](https://github.com/brycewang-stanford/StatsPAI)** introduced as
  the agent-native causal-inference & econometrics Python package (390+ functions
  at the time, since grown to 900+). MIT, JOSS.
- Added the English anti-AIGC skill set: `humanizer_academic` (44),
  `skill-deslop` (45), `stop-slop` (46), `avoid-ai-writing` (47), plus the
  community `ai-revision-guard` contribution.

## 2026-04-11 — Expanded to 119 repos / 23,000+ skills

- Grew from 43 curated collections to a map of **119 GitHub repositories /
  23,000+ skills** across eight social-science disciplines.
- Added finance, law, marketing, product-management, education, and public-health
  skill suites; 13 academic-data MCP servers; 11 multi-agent collaboration
  systems; and the bilingual Chinese/English README.

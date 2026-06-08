---
name: StatsPAI_skill
description: Use when the user asks to run a full empirical / causal analysis in Python — by default in the style of an applied economics paper (AER / QJE / JPE / ReStud / AEJ) with DID / RD / IV / SCM / DML / matching, written-out estimating equation + identifying assumption, Table 1 / Table 2 / event-study figure / robustness gauntlet — OR in epidemiology / public health style (target-trial emulation, IPTW + g-formula + TMLE triplet, Mendelian randomization, KM/AFT survival, E-value sensitivity, STROBE/TRIPOD reporting) — OR in ML causal inference style (DML, S/T/X/R/DR meta-learners, causal forest, Dragonnet/TARNet/CEVAE, BCF, CATE distribution, policy learning, conformal causal, fairness audit, causal discovery). Also covers exporting multi-column regression tables to Word / Excel / LaTeX (Stata outreg2 / esttab / R modelsummary equivalent) and bundling an entire replication appendix into one .docx / .xlsx / .tex file. Triggers on keywords "StatsPAI", "statspai", "AER empirical analysis", "applied micro pipeline", "Table 1 balance", "event study", "first-stage F", "Oster bound", "honest_did", "spec_curve", "callaway_santanna", "dragonnet", "text as treatment", "outreg2 in Python", "regression table to Word/Excel", "sp.regtable", "sp.collect", "sp.paper_tables", "sp.feols", "summary_col", "modelsummary", "AER style table", "QJE style table", "epidemiology pipeline", "target trial emulation", "g-formula", "IPTW", "TMLE", "Mendelian randomization", "STROBE", "TRIPOD", "公共健康", "流行病学", "DML", "double machine learning", "causal forest", "meta-learner", "CATE", "conformal causal", "policy learning", "因果机器学习", "ML causal".
triggers:
  - causal inference in python
  - applied microeconomics pipeline
  - AER empirical analysis
  - QJE style robustness
  - DID IV RD SCM
  - callaway_santanna
  - synthetic control
  - double machine learning
  - causal forest
  - event study plot
  - first stage F-statistic
  - Oster bound
  - honest_did
  - spec_curve
  - estimand-first DSL
  - LLM-assisted DAG discovery
  - text as treatment
  - export regression table to Word
  - export regression table to Excel
  - regression table docx
  - regression table xlsx
  - outreg2 in Python
  - summary_col equivalent
  - modelsummary equivalent
  - AER house style table
  - QJE house style table
  - journal template regression
  - Stata collect equivalent
  - replication bundle
  - sp.regtable
  - sp.collect
  - sp.paper_tables
  - sp.feols
  - sp.cite
  - high-dim fixed effects
  - two-way clustering
  - StatsPAI
  - statspai
  - fmt auto regression table
  - magnitude-adaptive coefficient formatting
  - mixed magnitude coefficients
  - sumstats by_labels
  - Control Treated auto labels
  - epidemiology pipeline
  - public health causal inference
  - target trial emulation
  - g-formula
  - IPTW marginal structural model
  - TMLE doubly robust
  - HAL-TMLE
  - Mendelian randomization
  - MR-Egger weighted median
  - STROBE TRIPOD reporting
  - E-value sensitivity
  - Kaplan-Meier AFT survival
  - 流行病学
  - 公共健康
  - ML causal inference
  - double machine learning DML
  - meta-learner S T X R DR
  - causal forest GRF
  - Dragonnet TARNet CEVAE
  - Bayesian causal forest BCF
  - CATE distribution
  - policy tree
  - off-policy evaluation
  - conformal causal prediction
  - fairness audit
  - causal discovery PC NOTEARS
  - 因果机器学习
---

# StatsPAI: Agent-Native Causal Inference & AER-Style Empirical Workflow

StatsPAI is a validation-tiered Python package for causal inference and applied econometrics: one `import statspai as sp`, 1,000+ registered functions behind a self-describing API, and mature estimator result objects that commonly export to LaTeX / Word / Excel / BibTeX.

This skill drives StatsPAI through the **canonical pipeline of an applied AER empirical paper**. Each step emits a paper-ready artifact (Table 1, event-study figure, Table 2 main results, robustness panel, replication stamp).

- **Source**: https://github.com/brycewang-stanford/StatsPAI
- **Install**: `pip install "statspai[fixest,plotting]"` (verified against **statspai 1.16.1**). The bare `pip install statspai` is **not enough** for the default pipeline — see the dependency matrix below.
- **Paper**: JOSS submission under review; JSS materials in `Paper-JSS/README.md` and `docs/jss_source_audit_dossier.md`

> **Install the right extras or the documented calls will raise `ImportError`.** Several core functions live behind optional dependency groups (verified from `pyproject.toml`):
>
> | You use… | Needs extra | Install | Symptom if missing |
> |---|---|---|---|
> | `sp.feols` / `sp.fepois` / `sp.feglm` (high-dim FE — the **default** for any `y ~ x \| fe` regression) | `fixest` (pyfixest) | `pip install "statspai[fixest]"` | `ImportError: pyfixest is required …` |
> | Any figure (`sp.coefplot`, `sp.binscatter`, event-study/RD/SCM plots, `.plot()`) | `plotting` (matplotlib/seaborn) | `pip install "statspai[plotting]"` | `ImportError` on first plot |
> | `sp.dragonnet` / `sp.tarnet` / `sp.cfrnet` / `sp.cevae` (neural causal) | `neural` (torch) | `pip install "statspai[neural]"` | `ImportError: PyTorch is required …` |
> | `sp.causal_text.*` (text-as-treatment) | `text` (sentence-transformers) | `pip install "statspai[text]"` | `ImportError` on embed |
>
> A one-shot install covering the whole skill: `pip install "statspai[fixest,plotting,neural,text]"`. `sp.regtable` / `sp.collect` / Word+Excel+LaTeX export, `sp.regress`, IV, RD, DID (`callaway_santanna`), matching, DML, meta-learners, causal forest, BCF, TMLE, and the epi stack work on the base install.

## Verified skeleton (copy, then swap in your columns)

This minimal pipeline **runs start-to-finish against statspai 1.16.1** (every call below was executed). It is the golden path — adapt column names / design, keep the call shapes and the unpack-then-save figure idiom. The full playbook (§−1 → §8) expands each step.

```python
import numpy as np, pandas as pd, statspai as sp
# df has: wage, training(0/1), worker_id, firm_id, year, first_treat_year, age, edu, tenure, ...

# §1 Table 1 → Word/Excel/LaTeX
mc = sp.mean_comparison(df, ["age","edu","tenure"], group="training", test="ttest",
                        title="Table 1. Summary statistics")
mc.to_word("tables/table1.docx"); mc.to_excel("tables/table1.xlsx")

# §2 Estimand-first plan (freeze BEFORE estimating)
q = sp.causal_question(treatment="training", outcome="wage", data=df, estimand="ATT",
                       design="did", time_structure="panel", time="year", id="worker_id",
                       covariates=["age","edu","tenure"])
plan = q.identify(); print(plan.summary())

# §3 Identification figure — from a CS/SA result (NOT event_study()); plotters return (fig, ax)
cs = sp.callaway_santanna(df, y="wage", g="first_treat_year", t="year", i="worker_id", x=["age","edu"])
fig, ax = sp.enhanced_event_study_plot(cs, shade_pre=True); fig.savefig("figures/fig2a.png", dpi=300)

# §4 Main table — mix sp.regress (no FE) + sp.feols (HDFE, needs statspai[fixest]) in ONE regtable
M1 = sp.regress("wage ~ training", df, cluster="firm_id")
M2 = sp.feols("wage ~ training + age + edu + tenure | industry + year", df, vcov={"CRV1":"firm_id"})
rt = sp.regtable(M1, M2, template="aer", coef_labels={"training":"Job training"},
                 model_labels=["(1) OLS","(2) FE"], stats=["N","R2","Cluster","FE"],
                 title="Table 2. Effect of training on wages")
rt.to_word("tables/table2.docx"); rt.to_excel("tables/table2.xlsx")
open("tables/table2.tex","w").write(rt.to_latex())

# §5 Heterogeneity — per-row CATE at result.model_info["cate"] (there is NO .cate_estimates)
ml = sp.metalearner(df, y="wage", treat="training", covariates=["age","edu","tenure"], learner="dr")
fig, ax = sp.cate_plot(ml, kind="hist"); fig.savefig("figures/fig4.png", dpi=300)

# §7 Robustness — Oster + E-value + honest-DID sensitivity figure
sp.oster_bounds(data=df, y="wage", treat="training", controls=["age","edu","tenure"], r_max=1.3)
sp.evalue(estimate=M2.params["training"], ci=tuple(M2.conf_int().loc["training"]), measure="RR")
fig, ax = sp.sensitivity_plot(sp.honest_did(cs, method="smoothness"),
                              original_estimate=cs.estimate, original_ci=cs.ci)
fig.savefig("figures/fig6.png", dpi=300)

# §8 One-file replication bundle (Word/Excel/LaTeX/Markdown from one source)
c = sp.collect("Replication", template="aer")
c.add_summary(df, vars=["wage","age","edu","tenure"], stats=["mean","sd","n"], title="Table 1")
c.add_regression(M1, M2, model_labels=["(1)","(2)"], stats=["N","R2"], title="Table 2")
for ext in ("docx","xlsx","tex","md"): c.save(f"replication/paper.{ext}")
```

> Epi (§A) and ML-causal (§B) reuse this exact scaffolding — only the §4 estimator stack changes (TMLE/g-formula/MR for epi; DML/meta-learner/causal-forest for ML), and every estimator still returns a result that drops into `sp.regtable` / `sp.collect`.

## Why for Agents

1. **Self-describing**: `sp.list_functions()` / `sp.describe_function(name)` / `sp.function_schema(name)` — registered symbols are discoverable without doc lookup.
2. **Structured results**: mature estimators return result objects with methods such as `.summary()`, `.plot()`, `.diagnostics`, `.to_latex()`, `.to_word()`, `.cite()` when supported.
3. **One import, full pipeline**: data contract → Table 1 → estimand-first DSL → identification graphs → main table → heterogeneity → mechanisms → robustness → replication package.
4. **Estimand-first**: `sp.causal_question(...).identify()` forces the "DID vs RD vs IV?" decision *before* estimation, with the identifying assumption written down — the way a referee expects to read it.

## The AER-style empirical pipeline

The skill mirrors the canonical sections of an applied AER / QJE / AEJ paper. Each step below is one paper section and one set of artifacts on disk.

```
Paper section               Step  StatsPAI moves
─────────────────────────── ───── ────────────────────────────────────────────────
Pre-Analysis Plan           −1    sp.power.* + freeze IdentificationPlan to disk
§1. Data                     0    data_contract + sample-construction log (footnote 4)
§1.1 Descriptives (Table 1)  1    sp.sumstats · sp.balance_table · sp.describe
§2. Empirical Strategy       2    write equation + identifying assumption + sp.causal_question
   (LLM-DAG addendum)        2.5  sp.llm_dag_propose · validate · constrained
§3. Identification graphics  3    event-study · first-stage F · McCrary · love plot
§4. Main Results (Table 2)   4    progressive controls + FE  (sp.regtable / sp.causal)
§5. Heterogeneity (Table 3)  5    sp.subgroup_analysis · sp.continuous_did · CATE
§6. Mechanisms               6    sp.mediation · sp.decompose
§7. Robustness gauntlet      7    placebo · Oster · honest_did · E-value · 2-way / Conley SE · spec_curve
§8. Replication package      8    .to_latex() · .plot() · reproducibility stamp
```

> **All code blocks below share one running example (`training → wage`, with `worker_id / firm_id / year / age / edu / tenure`) purely for readability.** Column names, `population`, `estimand`, and `design` values are **illustrative** — substitute the user's actual columns and research question. Only `sp.*` function names and argument *shapes* are normative.

## Three domain modes (default = AER econ; alternates = epi & ML-causal)

The default playbook above is **AER-style applied econometrics** — the AEA convention: written-out estimating equation, identifying assumption table, design horse-race, full robustness gauntlet. The skill **also** ships two parallel sub-pipelines for the other two big causal-inference traditions, each reusing the same export stack (`sp.regtable / sp.collect / sp.paper_tables`) and result objects:

| Mode | Reader convention | Identification stack | Reporting stack | Jump to |
|---|---|---|---|---|
| **Default — Applied Econ (AER / QJE / AEJ)** | "Show the equation + identifying assumption + design horse-race; controls visible; clustered SE" | DID / IV / RD / SCM / matching / `feols` HDFE | AER house-style multi-column `regtable` + 8-section paper layout | §−1 → §8 (entire playbook above) |
| **Mode A — Epidemiology / Public Health** | "STROBE / TRIPOD-AI; target trial protocol; doubly-robust estimand; absolute & relative risk; KM survival" | Target-trial emulation · IPTW · g-formula · TMLE · Mendelian randomization · KM/AFT | Same `regtable` + `collect`, with risk-difference / hazard-ratio / E-value rows | §A. Epidemiology pipeline |
| **Mode B — ML Causal Inference** | "DML / meta-learners / causal forest / DR-learner; CATE distribution; policy value" | DML · S/T/X/R/DR-Learner · GRF causal forest · Dragonnet/TARNet/CEVAE · BCF · matrix completion | `regtable` ML horse-race + `cate_plot` + policy-value table + `conformal_causal` PI | §B. ML causal pipeline |

**How to invoke a non-default mode** (Claude / agent picks this up from the user's wording):

| User says... | Mode the skill switches to |
|---|---|
| "Run a DID / IV / RD / event study", "AER table", "applied micro" | Default (AER econ) |
| "Target trial emulation", "g-formula", "IPTW", "TMLE", "Mendelian randomization", "STROBE / TRIPOD", "公共健康 / 流行病学", "epi pipeline", "RWE study", "cohort study", "case-control" | Mode A (Epi) |
| "DML", "double machine learning", "causal forest", "meta-learner", "CATE", "Dragonnet", "BCF", "policy learning", "conformal causal", "ML causal", "uplift modeling", "因果机器学习" | Mode B (ML causal) |
| "Mix" (e.g. "estimate DID + then ML CATE on the heterogeneity") | Default + Mode B in sequence — every estimator returns the same `CausalResult`, drop them all into one `sp.regtable(...)` for the horse-race column |

The three modes share **the same export stack, the same `CausalResult` interface, and the same `sp.causal_question(...).identify()` estimand-first DSL** — switching modes only changes which Step 4 estimators you reach for, not the surrounding scaffolding. If you only want descriptive stats / Table 1 / a balance check, the AER `sp.sumstats` / `sp.mean_comparison` / `sp.collect` calls work in all three modes.

## Paper-ready figure & table inventory (what to produce by section)

A modern AER paper has **5–7 figures** and **3–5 main tables** + an appendix robustness table. Every step below should leave at least one numbered artifact on disk. Default file names assume parallel `.tex` / `.docx` / `.xlsx` exports (the agent should produce all three so co-authors can edit in Word / Excel and the build system can use LaTeX):

| § | Artifact | StatsPAI primitive | Filenames (write all three) |
|---|---|---|---|
| §1 | **Figure 1**: raw trends / treatment rollout | `sp.parallel_trends_plot` · `sp.treatment_rollout_plot` | `figures/fig1_trends.png` |
| §1 | **Table 1**: summary stats (full / treated / control + Δ) | `sp.sumstats` + `sp.mean_comparison(...).to_word()/.to_excel()` (or `sp.collect().add_summary().add_balance()`) | `tables/table1_summary.{tex,docx,xlsx}` |
| §3 | **Figure 2**: identification graphic (event-study / first-stage / McCrary / RD scatter / SCM trajectory) | `sp.enhanced_event_study_plot` · `sp.binscatter` · `sp.rdplot` · `sp.rddensity().plot()` · `sp.synthdid_plot` | `figures/fig2_identification.png` |
| §4 | **Table 2**: main results — progressive controls | `rt = sp.regtable(M1...M5, template="aer"); rt.to_word(...); rt.to_excel(...)` | `tables/table2_main.{tex,docx,xlsx}` |
| §4 | **Table 2-bis**: design horse-race (OLS / IV / DID / DML) | `sp.regtable(ols, iv, did, dml, ...).to_word/.to_excel` | `tables/table2b_designs.{tex,docx,xlsx}` |
| §4 | **Figure 3** (optional): coefficient plot across specs | `sp.coefplot(M1, M2, M3, M4)` | `figures/fig3_coef.png` |
| §5 | **Table 3**: heterogeneity by subgroup | `sp.regtable(g_full, g_male, g_fem, g_q1...q4).to_word/.to_excel` | `tables/table3_heterogeneity.{tex,docx,xlsx}` |
| §5 | **Figure 4**: dose-response / CATE | `sp.dose_response(...).plot()` · `sp.cate_plot` · `sp.cate_group_plot` | `figures/fig4_cate.png` |
| §6 | **Table 4**: mechanisms (mediation / decomposition) | `sp.regtable(total, direct, indirect).to_word/.to_excel` | `tables/table4_mechanisms.{tex,docx,xlsx}` |
| §7 | **Table A1**: robustness master (one row per check) | `sp.regtable(rob1...robN, panel_labels=[...]).to_word/.to_excel` — or `sp.paper_tables(robustness=[...]).to_docx()` | `tables/tableA1_robustness.{tex,docx,xlsx}` |
| §7 | **Figure 5**: spec curve | `sp.spec_curve(...).plot()` | `figures/fig5_spec_curve.png` |
| §7 | **Figure 6**: honest-DID sensitivity plot (+ text dashboard) | `sp.sensitivity_plot(sp.honest_did(cs, ...))` for the figure; `print(sp.sensitivity_dashboard(result).summary())` for the Cinelli–Hazlett/Oster/E-value numbers (text, not a figure) | `figures/fig6_sensitivity.png` |
| §8 | **Replication bundle**: all tables in one Word/Excel/LaTeX file | `sp.collect("Paper").add_summary(...).add_regression(...)...save("paper.{docx,xlsx,tex}")` — or `sp.paper_tables(main=, heterogeneity=, robustness=, placebo=).to_docx/.to_xlsx` | `replication/paper.{docx,xlsx,tex}` |

> Every `CausalResult` and OLS model can be passed straight into `sp.regtable(...)`, `sp.coefplot(...)`, **and `sp.collect()`**. Don't hand-roll LaTeX, and don't render Word/Excel from pandas — the export functions apply book-tab borders, AER-style stars, and the right SE label automatically.

---

## Export cookbook — Word / Excel / LaTeX in one line

StatsPAI's export stack is the agent-native equivalent of Stata's `outreg2` / `esttab` / `collect` and R's `modelsummary` / `gtsummary`. Three tiers, picked by **scope** of what you're exporting:

| Tier | Use when | API | Hot kwargs |
|---|---|---|---|
| **1. Single multi-column table** (the outreg2 / `summary_col` equivalent) | Exporting *one* Table 2 / Table 3 / Table A1 with progressive columns | `rt = sp.regtable(M1, M2, ..., template="aer", title=...)`  *(default: all coefs incl. intercept)*<br>`rt.to_word("table2.docx")`<br>`rt.to_excel("table2.xlsx")`<br>`rt.to_latex()` · `rt.to_markdown()` | `template`, `coef_labels`, `model_labels`, `panel_labels`, `dep_var_labels`, `stats`, `stars`, `add_rows`; opt-in filters: `drop=["Intercept"]` (suppress constant), `keep=[focal]` (focal-only) |
| **2. Multi-panel paper format** (Tables 2 + 3 + A1 + A2 in one file) | Producing the *paper-tables block* — main + heterogeneity + robustness + placebo as a single document | `pt = sp.paper_tables(main=[M1...M5], heterogeneity=[H1,H2,H3], robustness=[R1...Rn], placebo=[P1,P2], template="aer")`<br>`pt.to_docx("paper_tables.docx")`<br>`pt.to_xlsx("paper_tables.xlsx")`<br>`pt.to_latex(...)` | `main`, `heterogeneity`, `robustness`, `placebo`, `template`, `coef_labels`, `model_labels_<panel>`, `keep` |
| **3. Full session bundle** (Stata 15 `collect` equivalent) | Replication appendix that mixes summary stats + balance + multiple regression tables + headings + prose in **one** file | `c = sp.collect("Paper title", template="aer")`<br>`c.add_heading("§1. Descriptives")`<br>`c.add_summary(df, vars=...)`<br>`c.add_balance(df, treatment=, variables=...)`<br>`c.add_regression(M1, M2, ..., title="Table 2")`<br>`c.add_text("Notes ...")`<br>`c.save("paper.docx")` (auto-detect by extension; `.xlsx`/`.tex`/`.md`/`.html`/`.txt` all work) | `add_heading(level=)`, `add_summary(stats=, labels=)`, `add_balance(weights=, test=)`, `add_regression(**regtable_kwargs)`, `add_table(result)`, `add_text(...)` |

**Journal templates** (apply the right SE label, star levels, and notes automatically):

```python
sp.list_journal_templates()
# → ('aer', 'qje', 'econometrica', 'restat', 'jf', 'aeja', 'jpe', 'restud')

rt = sp.regtable(M1, M2, M3, template="qje")    # QJE styling; default = full coef list (incl. intercept)
rt.to_word("table2_qje.docx")
# Opt-in filters:
#   • drop the constant only:    sp.regtable(M1, M2, M3, template="qje", drop=["Intercept"])
#   • focal-coefficient only:    sp.regtable(M1, M2, M3, template="qje", keep=["x"])

sp.get_journal_template("aer")                                 # inspect a preset
# → {'label': 'American Economic Review', 'star_levels': (0.1, 0.05, 0.01),
#    'se_label': 'Standard errors', 'stats': ('N', 'R-squared'),
#    'notes_default': ('Standard errors in parentheses.', '*** p<0.01, ** p<0.05, * p<0.10.'),
#    'font_name': 'Times New Roman'}    # note: tuples, not lists
```

**Inline citations in prose** (drop a coefficient straight into a sentence):

```python
sp.cite(M3, "training")                  # → "1.239*** (0.153)"
sp.cite(M3, "training", output="latex")  # → "1.239^{***}~(0.153)"  (wrap in $...$ yourself)
```

> **Naming gotcha**: `sp.regtable(..., output="docx")` is invalid — the enum is `{"text", "latex", "tex", "html", "markdown", "md", "qmd", "quarto", "word", "excel"}`. Use `output="word"` / `"excel"`, or — simpler — drop `output=` and call `.to_word(filename)` / `.to_excel(filename)` on the result.

---

## Notebook setup — CJK fonts + retina DPI

Run **once at the top of every analysis script / notebook**, *before* any matplotlib-backed plot (`sp.regtable.to_*` exporters do not need this — only `.savefig` / `sp.coefplot` / `sp.binscatter` / `sp.cate_plot` / etc.). Two failures it fixes in one shot:

1. **CJK labels render as ▢▢▢ tofu** — the matplotlib default `DejaVu Sans` carries no Chinese / Japanese / Korean glyphs, so `ax.set_title("教育回报")` silently degrades into squares.
2. **Plots look fuzzy on hi-DPI displays** — matplotlib's default `figure.dpi=100` is half the density of a Retina / 4K screen.

### Drop-in snippet

```python
import matplotlib as mpl
import matplotlib.pyplot as plt

def setup_plot(retina: bool = True) -> None:
    """One-shot matplotlib boilerplate: CJK font fallback + retina DPI.

    Idempotent — safe to call multiple times. Call BEFORE any plotting.
    """
    # 1. CJK font fallback chain — covers macOS / Windows / Linux in one list.
    #    matplotlib uses the first available font; later names are fallbacks,
    #    so listing all three platforms is harmless on any single host.
    mpl.rcParams["font.sans-serif"] = [
        "PingFang SC", "Heiti SC", "Hiragino Sans GB",   # macOS
        "Microsoft YaHei", "SimHei", "SimSun",           # Windows
        "Noto Sans CJK SC", "Source Han Sans SC",        # Linux / Adobe
        "WenQuanYi Micro Hei",                           # Linux fallback
        "Arial Unicode MS",                              # universal fallback
        "DejaVu Sans",                                   # last-resort Latin
    ]
    mpl.rcParams["axes.unicode_minus"] = False          # 修复中文字体下负号渲染成 □

    # 2. Retina-grade DPI. figure.dpi controls on-screen / inline rendering;
    #    savefig.dpi controls .png exports. Set both — they are independent.
    if retina:
        mpl.rcParams["figure.dpi"]  = 144   # 2× default — sharp on Retina/HiDPI
        mpl.rcParams["savefig.dpi"] = 300   # manuscript/export PNG (AER house norm)
        # Jupyter inline retina backend (no-op outside IPython):
        try:
            from IPython import get_ipython
            ipy = get_ipython()
            if ipy is not None:
                ipy.run_line_magic("config", "InlineBackend.figure_format = 'retina'")
        except Exception:
            pass

setup_plot()                                            # call once at the top
```

### Smoke test (5 seconds, run once after `setup_plot()`)

```python
fig, ax = plt.subplots(figsize=(4, 2.5))
ax.plot([0, 1, 2], [-1, 0, 1])
ax.set_title("中文标题测试 — Card (1995) 教育回报")
ax.set_xlabel("受教育年数 (years)")
fig.tight_layout()
fig.savefig("figures/_font_smoke_test.png", dpi=300)    # delete after verifying
```

If the saved PNG shows Chinese characters cleanly *and* the y-axis tick `-1` is a real minus sign (not a square), the setup is good. Otherwise see troubleshooting below.

### Saving figures — the `(fig, ax)` idiom (READ THIS)

> **Every StatsPAI plotter and every result `.plot()` returns a `(fig, ax)` tuple — NOT a bare Figure.** So `sp.parallel_trends_plot(...).savefig(...)` raises `AttributeError: 'tuple' object has no attribute 'savefig'`. Always unpack, then save the figure:
>
> ```python
> fig, ax = sp.parallel_trends_plot(df, y="wage", time="year", treat="training", treat_time=2015)
> fig.savefig("figures/fig1.png", dpi=300)
> ```
>
> Two exceptions to memorize:
> - **`sp.binscatter(...)` returns a 3-tuple** `(fig, ax, binned_df)` — `fig, ax, _ = sp.binscatter(...)`.
> - **`sp.kaplan_meier(...).plot()` returns a bare `Axes`** (it is a `KMResult`, not a `CausalResult`) — save via `ax = km.plot(); ax.figure.savefig(...)`.
>
> This applies uniformly to `coefplot`, `binscatter`, `rdplot`, `rddensity().plot()`, `bacon_plot`, `enhanced_event_study_plot`, `did_summary_plot`/`ggdid`/`group_time_plot`, `synthdid_plot`, `cate_plot`, `cate_group_plot`, `dose_response().plot()`, `sensitivity_plot`, `match().plot()`, `synth().plot()`, and a generic `result.plot()`. The code blocks below all use the unpack-then-save form.

### Troubleshooting

| Symptom | Fix |
|---|---|
| Title still shows ▢▢▢ tofu after `setup_plot()` | Host has none of the listed fonts. Install one — **macOS**: pre-installed (no action). **Linux**: `sudo apt install fonts-noto-cjk` (Debian/Ubuntu) or `sudo dnf install google-noto-sans-cjk-fonts` (Fedora/RHEL). **Windows**: pre-installed. Then clear matplotlib's font cache: `rm -rf ~/.cache/matplotlib` (Linux/macOS) / `%LOCALAPPDATA%\matplotlib` (Windows), and restart the Python / Jupyter kernel. |
| Negative numbers render as ▢ | `axes.unicode_minus = False` was overridden by a later `plt.style.use(...)` or `mpl.rcParams.update(...)`. Re-call `setup_plot()` after any style change. |
| Plot blurry inside VSCode `.ipynb` | VSCode's notebook UI ignores `figure.dpi` for inline rendering. Either switch the cell output to "Open in Image Viewer", or use `%matplotlib inline` *before* `setup_plot()`. The saved `.png` (driven by `savefig.dpi=300`) is sharp regardless. |
| `sp.<plot>(...)` output still shows tofu | The `sp.*` plotters honor global `rcParams`, so this only happens when `setup_plot()` was called *after* the plot was drawn. Move the call to the very top of the script. |
| Need to verify which font matplotlib picked | `mpl.font_manager.findfont(mpl.font_manager.FontProperties(family=mpl.rcParams["font.sans-serif"]))` returns the resolved file path — if it ends in `DejaVuSans.ttf` despite Chinese labels, no CJK font is installed. |

### Persist as project default (optional)

Drop the same rcParams into a project-level `matplotlibrc` next to `pyproject.toml` so co-authors and CI runners pick it up without calling `setup_plot()`:

```
# matplotlibrc — committed to the repo
font.sans-serif: PingFang SC, Heiti SC, Microsoft YaHei, SimHei, Noto Sans CJK SC, Arial Unicode MS, DejaVu Sans
axes.unicode_minus: False
figure.dpi: 144
savefig.dpi: 300
```

The `setup_plot()` function above is the in-script fallback when a project `matplotlibrc` is not present.

---

## Step −1 — Pre-Analysis Plan (pre-data; AEA RCT Registry style)

`sp.power(design, n=..., effect_size=..., power_target=...)` is a unified dispatcher — leave one argument `None` to solve for it (sample size, MDE, or power). Convenience wrappers: `sp.power_rct`, `sp.power_did`, `sp.power_rd`, `sp.power_iv`, `sp.power_cluster_rct`, `sp.power_ols`.

```python
# Always go through the dispatcher when you want auto-solve. The
# `sp.power_<design>` wrappers (power_rct / power_did / power_rd /
# power_iv / power_cluster_rct / power_ols) accept *only* the design's
# native arguments — they will NOT solve for power_target / n / effect
# unless you go via `sp.power(design, ..., power_target=...)`.

sp.power("rct", effect_size=0.3, power_target=0.80)                  # → PowerResult(n=349, power=0.80)
sp.power("did", n=200, effect_size=0.15, power_target=0.80,
         n_periods=4, n_treated_periods=2)                            # DID: solves MDE / n / power
sp.power("cluster_rct", cluster_size=50, icc=0.05,
         effect_size=0.2, power_target=0.80)                          # Cluster RCT: solves n_clusters
# Roth (2022) pre-trends power is a POST-estimation diagnostic — it needs an estimated
# event-study result, so run it in §3 once you have `es = sp.event_study(...)`:
#   sp.pretrends_power(es)
```

Persist the `PowerResult` next to `data_contract.json` and `empirical_strategy.md` — a referee will ask whether the design was powered before data collection, not after.

## Step 0 — Sample construction & data contract (Section "Data")

An AER §1 *Data* section has three jobs: (a) describe sources, (b) document **every** sample restriction (the "footnote 4" sample log), (c) lock the panel structure. StatsPAI assumes an **analysis-ready DataFrame** — do ETL (imputation, type coercion, merges, transforms) in pandas first, then run the 5-check contract.

### 0.1 Sample-construction log (footnote 4)

```python
sample_log = []
df0 = df_raw.copy();                                       sample_log.append(("0. raw",                len(df0)))
df1 = df0.dropna(subset=["wage"]);                          sample_log.append(("1. drop missing wage",  len(df1)))
df2 = df1[df1["age"].between(18, 65)];                      sample_log.append(("2. drop age outside 18-65", len(df2)))
df3 = df2[df2["industry"].isin(MANUF_CODES)];               sample_log.append(("3. keep manufacturing", len(df3)))
df  = df3
import json; json.dump(sample_log, open("artifacts/sample_construction.json", "w"), indent=2)
```

Paste this log verbatim as footnote 4 of your paper. AER reviewers use it to reconstruct the analysis sample.

### 0.2 Five-check data contract (go / no-go gate)

```python
import pandas as pd, numpy as np, statspai as sp

def data_contract(df, *, y, treatment, id=None, time=None, covariates=()):
    """Return a go/no-go dict. Stop the pipeline if any required check fails."""
    keys = [y, treatment] + ([id, time] if id and time else []) + list(covariates)
    c = {
        "n_obs":       len(df),                                           # 1. shape
        "dtypes":      df[keys].dtypes.astype(str).to_dict(),             # 2. dtypes on keys
        "n_missing":   df[keys].isna().sum().to_dict(),                   # 3. missing pattern
        "n_dupes_on_keys": 0,
        "panel_balanced":  None,
        "cohort_sizes":    None,
    }

    if id and time:
        c["n_dupes_on_keys"] = int(df.duplicated([id, time]).sum())       # 4. duplicate (id,time)
        balanced = sp.balance_panel(df, entity=id, time=time)              # 5. panel balance
        c["panel_balanced"]        = len(balanced) == len(df)
        c["n_dropped_by_balance"]  = len(df) - len(balanced)

        if "first_treat_year" in df.columns:                               # staggered cohorts
            c["cohort_sizes"] = (
                df.drop_duplicates(id).groupby("first_treat_year").size().to_dict()
            )

    c["y_range"]          = (float(df[y].min()), float(df[y].max()))
    c["treatment_share"]  = float(df[treatment].mean())

    # Missingness mechanism hint (Rubin): compare covariate means between
    # rows missing-on-y vs observed. Any p < 0.05 ⇒ NOT MCAR → use MI / IPW,
    # not listwise deletion.
    from scipy import stats
    miss_y = df[y].isna()
    c["mcar_hint"] = "likely MCAR (listwise OK)"
    if miss_y.any() and (~miss_y).any():
        for cov in covariates:
            if df[cov].dtype.kind in "fi":
                _, p = stats.ttest_ind(df.loc[miss_y, cov].dropna(),
                                        df.loc[~miss_y, cov].dropna(),
                                        equal_var=False)
                if p < 0.05:
                    c["mcar_hint"] = f"NOT MCAR (y-miss differs on {cov}, p={p:.3f}) → use MI / IPW"
                    break
    return c

contract = data_contract(df, y="wage", treatment="training",
                         id="worker_id", time="year",
                         covariates=["age", "edu", "tenure"])

assert contract["n_dupes_on_keys"] == 0, "duplicate (id, time) — fix before panel methods"
assert all(v == 0 for v in contract["n_missing"].values()), \
       f"NaNs on keys: {contract['n_missing']}"
```

If any assertion fires, **stop** and fix it in pandas — StatsPAI estimators silently drop NaN rows, the most common source of "mysterious sample-size shrinkage" bugs. Persist:

```python
import json; json.dump(contract, open("artifacts/data_contract.json", "w"), indent=2, default=str)
```

## Step 1 — Descriptive statistics (Table 1)

The signature AER Table 1 has three column blocks plus a difference column:

| | (1) Full | (2) Treated | (3) Control | (4) Δ (t-test) |

The Imbens–Rubin rule of thumb: a normalized difference `|Δ| / √((s²₁+s²₀)/2) > 0.25` flags substantive imbalance and should trigger matching / reweighting *before* you trust an OLS comparison.

```python
# Quick text/LaTeX preview (use sumstats `output=` for a string-only render).
# When `by=` is binary 0/1 and you don't pass `by_labels=`, sumstats auto-fills
# the panel headers as **Control / Treated** so the academic Table 1 reads
# correctly out of the box. For non-0/1 codings or different wording, pass
# `by_labels={0:"Untrained", 1:"Trained"}` (or `{"A":"Control","B":"Treated"}`).
print(sp.sumstats(df, vars=["wage","edu","exp","tenure","age"],
                  by="training", output="text"))

# AER-style balance table → Word + Excel + LaTeX in three lines.
# `mean_comparison` returns a MeanComparisonResult that exposes the full
# export chain (.to_word / .to_excel / .to_latex / .to_markdown / .to_html).
mc = sp.mean_comparison(df,
                        ["age","edu","tenure","firm_size"],
                        group="training",
                        test="ttest",
                        title="Table 1. Summary statistics by treatment status")
mc.to_word ("tables/table1_summary.docx")     # editable in Word
mc.to_excel("tables/table1_summary.xlsx")     # editable in Excel
open("tables/table1_summary.tex", "w").write(mc.to_latex())
sp.describe(df).to_markdown("references/codebook.md")              # auto-codebook
```

### 1.1 Multi-panel Table 1 (AER convention)
Group rows into **Panel A: Outcomes**, **Panel B: Treatment intensity**, **Panel C: Controls**, **Panel D: Sample composition**. The cleanest path is to push each panel into a `sp.collect()` bundle — one `.save("file.docx")` call then writes the whole multi-panel Table 1 with AER book-tab borders, in Word **and** Excel **and** LaTeX from one source.

```python
panels = {
    "A. Outcomes":             ["wage", "log_wage", "weeks_employed"],
    "B. Treatment":            ["training", "training_hours"],
    "C. Demographic controls": ["age", "edu", "female", "married"],
    "D. Labor market":         ["tenure", "firm_size", "industry_id"],
}

c1 = sp.collect("Table 1. Summary statistics", template="aer")
for label, vs in panels.items():
    c1.add_heading(f"Panel {label}", level=2)
    c1.add_summary(df, vars=vs, stats=["mean", "sd", "n"])
c1.save("tables/table1_summary.docx")          # editable Word, AER book-tab borders
c1.save("tables/table1_summary.xlsx")          # one sheet per panel (heading drives the sheet name)
c1.save("tables/table1_summary.tex")           # multi-panel LaTeX

# Plain-text alternative (no Collection): one `sp.sumstats` per panel, concat strings.
# Useful when you only need the .tex preview without a binary export.
import io; buf = io.StringIO()
for label, vs in panels.items():
    buf.write(f"\n% Panel {label}\n")
    buf.write(sp.sumstats(df, vars=vs, by="training",
                          stats=["mean", "sd", "n"], output="latex"))
open("tables/table1_summary_flat.tex", "w").write(buf.getvalue())
```

### 1.2 Figure 1 — raw trends / treatment rollout
For DID / event-study designs, the *first* figure of an applied paper is almost always either (a) raw treated-vs-control means over time, or (b) the staggered rollout heat-strip showing which units are treated when. Both are one-liners:

```python
# (a) Raw trends with vertical line at treatment start (DID Figure 1 style)
fig, ax = sp.parallel_trends_plot(df, y="wage", time="year", treat="training",
                                  treat_time=2015, ci=True,
                                  labels={"treated":"Trained", "control":"Untrained"})
fig.savefig("figures/fig1a_raw_trends.png", dpi=300)

# (b) Treatment rollout heatmap (staggered DID convention; Goodman-Bacon-friendly)
fig, ax = sp.treatment_rollout_plot(df, time="year", treat="training", id="worker_id",
                                    sort_by="first_treat_year",
                                    title="Figure 1. Treatment timing")
fig.savefig("figures/fig1b_rollout.png", dpi=300)
```

For matching designs, also produce a **love plot** of standardized differences pre/post matching (Step 3.4).

## Step 2 — Empirical strategy (Section "Identification")

This is the heart of an AER paper. Before any code, **write down the equation explicitly** and **state the identifying assumption**. Vague identification language is the single most common reason a referee rejects an applied paper.

### 2.1 Equation × identifying assumption table

| Design | Estimating equation | Identifying assumption |
|---|---|---|
| 2×2 DID | `Y_it = α_i + λ_t + β·D_it + X'γ + ε_it` | parallel trends conditional on X |
| Event-study (CS / SA) | `Y_it = α_i + λ_t + Σ_{e≠-1} β_e · 1{t-G_i = e} + ε_it` | no anticipation + group-time PT |
| 2SLS | `Y_i = α + β·D_i + X'γ + ε_i;  D_i = π·Z_i + X'δ + u_i` | exclusion + relevance + monotonicity |
| Sharp RD | `Y_i = α + β·1{X_i ≥ c} + f(X_i) + ε_i` (local poly) | continuity of E[Y(0)\|X] at c, no manipulation |
| SCM | `Ŷ_1t(0) = Σ_j ŵ_j Y_jt`, τ_t = `Y_1t − Ŷ_1t(0)` for t≥T_0 | pre-period fit + interpolation validity |
| DML / unconfoundedness | `Y_i = m(X_i) + β·D_i + ε_i` (Robinson partialling-out) | unconfoundedness \| X + overlap |

### 2.2 Design picker

When `design="auto"` is too opaque, use this decision tree:

```
                 ┌─ running var + cutoff ───────────────── RDD   (sp.rdrobust)
                 │
                 ├─ exogenous instrument Z ─────────────── IV    (sp.ivreg, sp.dml)
data + question ─┤
                 ├─ pre/post × treat/control ─┬ 2 periods  ── 2×2 DID (sp.did)
                 │                            └ staggered  ── CS / SA  (sp.callaway_santanna)
                 │
                 ├─ 1 treated unit + donor pool + long pre ── SCM   (sp.synth, sp.sdid)
                 │
                 ├─ high-dim X, selection-on-observables ── DML / Causal Forest
                 │
                 └─ none of the above ──────────────────── matching + E-value (sp.match, sp.evalue)
```

### 2.3 Estimand-first DSL = pre-registration

`sp.causal_question` declares the five-tuple (population, treatment, outcome, estimand, design) and `.identify()` picks the estimator with its assumptions written down. **Treat the `IdentificationPlan` as your pre-registration artifact** — freeze it *before* running `q.estimate()` so the analysis plan is a dated document, not a post-hoc rationalization.

```python
q = sp.causal_question(
    treatment="training", outcome="wage", data=df,
    population="manufacturing workers, 2010–2020",
    estimand="ATT",
    design="auto",                 # 'auto' | 'did' | 'event_study' | 'regression_discontinuity'
                                   # | 'iv' | 'rct' | 'selection_on_observables'
                                   # | 'synthetic_control' | 'natural_experiment'
                                   # | 'policy_shock' | 'longitudinal_observational'
    time_structure="panel", time="year", id="worker_id",
    covariates=["age", "edu", "tenure"],
)
plan = q.identify()                # IdentificationPlan: estimator + assumptions + fallbacks
print(plan.summary())              # human-readable Methods paragraph
print(plan.identification_story)   # narrative of why this estimator identifies the estimand

# FREEZE the plan to disk BEFORE estimating — this is your pre-registration.
# `q` (CausalQuestion) carries the question (population / treatment / outcome).
# `plan` (IdentificationPlan) carries the strategy (estimator / story /
# assumptions / fallbacks / warnings). The estimating equation is *your*
# job to write down — paste it from the §2.1 table that matches plan.estimator.
from pathlib import Path
bullets = lambda xs: "\n".join(f"- {x}" for x in xs) if xs else "- (none)"
Path("artifacts/empirical_strategy.md").write_text(
    f"# Empirical Strategy (pre-registration)\n\n"
    f"**Population**: {q.population}\n"
    f"**Treatment**: `{q.treatment}`    **Outcome**: `{q.outcome}`\n"
    f"**Estimand**: {plan.estimand}\n"
    f"**Estimator**: `sp.{plan.estimator}`\n\n"
    f"## Estimating equation (paste from §2.1 row matching `{plan.estimator}`)\n"
    f"```\n<paste here>\n```\n\n"
    f"## Identification story\n{plan.identification_story}\n\n"
    f"## Identifying assumptions (must defend in §2)\n{bullets(plan.assumptions)}\n\n"
    f"## Auto-flagged warnings\n{bullets(plan.warnings)}\n\n"
    f"## Fallback estimators (Step 7 robustness)\n{bullets(plan.fallback_estimators)}\n"
)
# Machine-readable sidecar (full question, replayable):
Path("artifacts/causal_question.yaml").write_text(q.to_yaml())

result = q.estimate()              # run only after the plan is committed to disk / git
```

### 2.5 (Optional) LLM-assisted DAG addendum

Useful when the user wants an explicit DAG to defend in §2 or §7. Pipe the discovered DAG into `sp.causal(..., dag=...)`.

```python
proposal   = sp.llm_dag_propose(
    variables=df.columns.tolist(),
    domain="labor economics: training, wages, tenure",
    client=my_llm_client,                          # .complete(prompt) -> str; None = heuristic
)
validation = sp.llm_dag_validate(proposal, df, alpha=0.05)   # (dag, data) positional
print(validation.edge_evidence)

discovered = sp.llm_dag_constrained(
    df,
    descriptions={"wage": "monthly wage USD", "training": "0/1 program"},
    oracle=my_llm_client.suggest_edges,            # optional; falls back to plain PC
    max_iter=3,
)
# The result is an LLMConstrainedDAGResult — it has NO `.dag` attribute. Get a DAG with
# `.to_dag()` (or inspect `.final_edges`). Pass into Step 4 as:
#   sp.causal(..., dag=discovered.to_dag())
```

## Step 3 — Identification graphics (Section "Identification, graphical evidence")

AER convention: **the identification figure precedes the regression table**. The reader should see graphical evidence that PT holds / first stage is strong / RD jumps cleanly *before* you ask them to trust your point estimate.

### 3.1 Event-study plot + numerical pre-trends test (DID identification)
Pre-period coefficients ≈ 0 (with the −1 reference period normalized to zero) is the visual evidence for parallel trends. Pair the **figure** with a **numerical** pre-trends test so reviewers don't have to eyeball it.

```python
# --- The event-study FIGURE comes from a Callaway–Sant'Anna (or sun_abraham)
#     result, NOT from sp.event_study(). The figure plotters
#     (enhanced_event_study_plot / cs.plot() / ggdid / group_time_plot) consume a
#     CS/SA result; feeding them sp.event_study() output raises KeyError('att').
#     Use `x=` for covariates (NOT `covariates=` — that kwarg does not exist on CS).
cs = sp.callaway_santanna(df, y="wage", g="first_treat_year",
                          t="year", i="worker_id",
                          x=["age", "edu"])

# Figure 2a — dynamic ATT / event-study coefficient plot. Plotters return (fig, ax).
fig, ax = sp.enhanced_event_study_plot(
    cs, shade_pre=True,
    title="Figure 2a. Event-study coefficients (95% CI; ref. period = −1)")
fig.savefig("figures/fig2a_event_study.png", dpi=300)
# (equivalently: `fig, ax = cs.plot()` or `fig, ax = sp.ggdid(cs)` /
#  `fig, ax = sp.group_time_plot(cs)` — all consume the CS result and return (fig, ax).)

# Numerical pre-trends test (Roth 2022 power) for the table footnote. THIS is what
# sp.event_study() is for — the coefficient/pre-trend numerics, not the figure.
es = sp.event_study(df, y="wage", treat_time="first_treat_year",
                    time="year", unit="worker_id",
                    window=(-4, 4), ref_period=-1,
                    covariates=["age", "edu"])
print(sp.pretrends_summary(es))                       # F-stat, p-value, max-PT bound
# es.model_info["pretrend_test"] holds the same numbers machine-readably.

# Bacon decomposition figure for staggered DID (Figure 2a-bis)
bd = sp.bacon_decomposition(df, y="wage", treat="training",
                            time="year", id="worker_id")
fig, ax = sp.bacon_plot(bd, title="Figure 2a-bis. Goodman-Bacon weights")
fig.savefig("figures/fig2a2_bacon.png", dpi=300)

# Borusyak–Jaravel–Spiess joint pre-trends test — needs the CS/SA result
# AND the underlying panel (NOT the event_study() output):
sp.bjs_pretrend_joint(cs, df, y="wage", group="first_treat_year",
                      time="year", first_treat="first_treat_year",
                      controls=["age", "edu"])
```

### 3.2 First-stage F-statistic + scatter (IV identification)
Rule of thumb: first-stage F ≥ 10 for OLS-style inference; F ≥ 23 for AR-equivalent inference (Stock–Yogo / Lee 2022).

```python
iv = sp.ivreg("wage ~ (training ~ Z1 + Z2) + age + edu", df, cluster="firm_id")
print(iv.summary())                                    # reports first-stage F (Cragg–Donald / KP)
fig, ax, _binned = sp.binscatter(df, y="training", x="Z1",   # binscatter → 3-tuple
                                 controls=["age", "edu"],
                                 n_bins=20, ci=True)
fig.savefig("figures/fig_first_stage.png", dpi=300)
```

### 3.3 RD: McCrary density + canonical RD plot + binscatter
The signature RD figure is `sp.rdplot` (CCT-style binned scatter with local-polynomial fit on each side), paired with the McCrary manipulation test. Together they answer: (a) is there a visual jump? (b) is the density continuous at the cutoff?

```python
# Figure 2b — canonical RD plot (binned means + local poly fit on each side)
fig, ax = sp.rdplot(df, y="y", x="running_var", c=0,
                    p=4, kernel="triangular", binselect="esmv",
                    shade_ci=True, ci_level=0.95)
fig.savefig("figures/fig2b_rdplot.png", dpi=300)

# Figure 2b-bis — McCrary density (manipulation test). .plot() → (fig, ax)
fig, ax = sp.rddensity(df, x="running_var", c=0).plot()
fig.savefig("figures/fig2b2_mccrary.png", dpi=300)

# Optional: covariate-adjusted binscatter (continuity in covariates is also testable)
fig, ax, _ = sp.binscatter(df, y="age", x="running_var", n_bins=40, ci=True)
fig.savefig("figures/fig2b3_cov_binscatter.png", dpi=300)
```

### 3.4 Matching: love plot (standardized differences)
```python
m = sp.match(df, y="wage", treat="training",
             covariates=["age", "edu", "tenure"], method="nearest")
fig, ax = m.plot()                                    # |std diff| pre vs post; target |Δ|<0.1
fig.savefig("figures/fig2c_love_plot.png", dpi=300)
```

### 3.5 SCM: synthetic-control trajectory + gap plot
For synthetic-control designs the canonical Figure 2 is the treated-vs-synthetic time-series with treatment time annotated. `synthdid_plot` does this in one line.

```python
sc = sp.synth(df, outcome="y", unit="unit", time="time",
              treated_unit=1, treatment_time=2000)
fig, ax = sc.plot()                                   # treated vs synthetic + gap
fig.savefig("figures/fig2d_synth_trajectory.png", dpi=300)
sd = sp.sdid(df, outcome="y", unit="unit", time="time",
             treated_unit=1, treatment_time=2000)
fig, ax = sp.synthdid_plot(sd, title="Figure 2d. Synthetic DID")
fig.savefig("figures/fig2d2_sdid.png", dpi=300)
```

### 3.6 Generic pre-flight (identification-independent)
```python
sp.diagnose(df, y="wage", x=["age", "edu", "tenure"])  # leverage, overlap, missing
```

> Identification-specific checks (PT for DID, weak-IV F, density for RD, common support for matching) **are also auto-run inside `sp.causal(...)`** in Step 4 — don't duplicate the numerics here, but DO produce the figures: a referee scans the figures first.

## Step 4 — Main results (multi-regression tables, AER style)

This is the densest section of an applied paper. A modern AER §4 typically contains **2–3 multi-regression tables and one coefficient plot**:

- **Table 2** (main): progressive controls, 4–6 columns
- **Table 2-bis** (design horse race): same coefficient under OLS / 2SLS / DID / DML
- **Table 2-ter** (multi-outcome): same treatment, several outcomes side-by-side
- **Figure 3** (coefplot): visual summary of β̂ and 95% CI across specs

> **Estimator routing** (memorize this — getting it wrong silently produces nonsense):
> - **No FE** → `sp.regress("y ~ x1 + x2", df, cluster="firm_id")`
> - **High-dim FE** → `sp.feols("y ~ x1 + x2 | fe1 + fe2", df, vcov={"CRV1":"firm_id"})`
> - **Two-way cluster** → `sp.feols(..., vcov={"CRV1":"firm_id+year"})`
> - **2SLS / IV** → `sp.ivreg("y ~ (x ~ z) + controls", df, cluster=...)`
> - **DID / event-study** → `sp.callaway_santanna(...)` / `sp.sun_abraham(...)`
>
> **Never** write `sp.regress("y ~ x | firm_id")` — `sp.regress` does not parse `|` and silently treats `x | firm_id` as a single variable name. Use `sp.feols` for any formula containing `|`.

`sp.regtable(*models, ...)` is the workhorse. Useful kwargs:

```
keep              : list of coef names to display (e.g. ["training"])
drop              : list of coef names to suppress (controls)
model_labels      : column labels   ["(1) Baseline", "(2) +Demog", ...]
dep_var_labels    : dep-var-row labels (for multi-outcome tables)
panel_labels      : panel-A / panel-B layout for stacked tables
coef_labels       : pretty-print names for coefficients
stars             : "aer" → * 0.10 ** 0.05 *** 0.01  (or "default", "none")
stats             : footer rows ["N","R2","Cluster","FE","DV mean", ...]
output            : "latex" | "html" | "markdown" | "text"
filename          : path to write the table
```

### 4.1 Pattern A — Progressive controls (the canonical Table 2)
Stable β̂ across columns ⇒ less concern that selection on observables is driving the estimate (Oster 2019 selection-stability logic; quantified in Step 7.5). **`sp.regtable(*models)` is the StatsPAI equivalent of Stata `outreg2` / `esttab` and R `modelsummary::msummary` / `summary_col` — it consolidates N models into ONE table with one column per model.**

| | (1) Baseline | (2) +Demographics | (3) +Labor-market | (4) +Region×Industry FE | (5) +Worker FE |
|---|---|---|---|---|---|
| Controls | none | age, edu | + tenure, firm_size | high-dim FE | individual FE |

```python
# RULE: pure OLS → sp.regress; high-dim FE absorption → sp.feols
# (sp.regress does NOT parse `|` as FE — it's a thin OLS wrapper. Use
# `sp.feols("y ~ x | fe1 + fe2", df, vcov={"CRV1":"firm_id"})` for FE.)
M1 = sp.regress("wage ~ training",                                  df, cluster="firm_id")
M2 = sp.regress("wage ~ training + age + edu",                      df, cluster="firm_id")
M3 = sp.regress("wage ~ training + age + edu + tenure + firm_size", df, cluster="firm_id")
M4 = sp.feols  ("wage ~ training + age + edu + tenure + firm_size | region + industry + year",
                df, vcov={"CRV1": "firm_id"})
M5 = sp.feols  ("wage ~ training + age + edu + tenure + firm_size | worker_id + year",
                df, vcov={"CRV1": "firm_id"})

# Consolidate 5 models into ONE table (= Stata `outreg2 [M1..M5] using ..., replace`).
# **Default = show ALL coefficients verbatim — controls AND the intercept**
# (AER convention; readers verify the full spec). Pass NO `keep=`/`drop=` and
# `regtable` will surface every estimated parameter. Add `drop=["Intercept"]`
# only if you want to suppress the constant for paper aesthetics; add
# `keep=[focal]` only when a focal-coefficient-only table is intentional.
rt = sp.regtable(M1, M2, M3, M4, M5,
                 template="aer",                  # auto-applies SE label, star levels, font
                 coef_labels={"training": "Job training"},
                 model_labels=["(1) Baseline", "(2) +Demog.", "(3) +Labor-mkt",
                               "(4) Region×Ind. FE", "(5) Worker FE"],
                 stats=["N", "R2", "Cluster", "FE", "DV mean"],
                 title="Table 2. Effect of training on wages")
# Variants (all opt-in — the default above is preferred):
#   • drop intercept only:    sp.regtable(..., drop=["Intercept"])
#   • focal-coefficient only: sp.regtable(..., keep=["training"])
#   • mixed-magnitude table:  sp.regtable(..., fmt="auto")
#       Use whenever a single table mixes dollar-magnitude coefficients
#       (e.g. earnings ≈ 1500) with elasticity-magnitude coefficients
#       (e.g. log-earnings ≈ 0.09). The default fmt="%.3f" pads the dollar
#       side; a fixed fmt="%.0f" rounds the elasticity side to "0" while
#       significance stars survive — the silent LaLonde-style precision
#       trap. fmt="auto" picks per-value precision: thousands separator
#       for |β|≥1000, integer for ≥100, 1 dp for ≥10, 2 dp for ≥1, 3 dp
#       below — so neither magnitude is killed.

# Export to ALL THREE in three lines — Word for co-authors, Excel for editors, LaTeX for build:
rt.to_word ("tables/table2_main.docx")
rt.to_excel("tables/table2_main.xlsx")
open("tables/table2_main.tex", "w").write(rt.to_latex())
```

### 4.2 Pattern B — Design horse race (Table 2-bis)
Show the same coefficient of interest under multiple identification strategies. This is *the* AER credibility move: convergent evidence across designs each making different identifying assumptions.

```python
ols  = sp.feols  ("wage ~ training + age + edu + tenure | industry + year",
                   df, vcov={"CRV1": "firm_id"})                                          # OLS + 2-way FE
ivr  = sp.ivreg("wage ~ (training ~ Z1 + Z2) + age + edu + tenure",
                 df, cluster="firm_id")                                                    # 2SLS
did  = sp.callaway_santanna(df, y="wage", g="first_treat_year",
                             t="year", i="worker_id",
                             x=["age","edu","tenure"])                                     # CS-DID (kwarg is x=)
dml  = sp.dml(df, y="wage", treat="training",
               covariates=["age","edu","tenure","firm_size"], model="plr")                 # DML
mtch = sp.match(df, y="wage", treat="training",
                 covariates=["age","edu","tenure"], method="nearest")                      # PSM

rt = sp.regtable(ols, ivr, did, dml, mtch,
                 template="aer",
                 coef_labels={"training": "Job training (β̂)"},
                 model_labels=["(1) OLS+FE", "(2) 2SLS", "(3) CS-DID",
                               "(4) DML-PLR", "(5) PSM"],
                 stats=["Estimator", "Identifying assumption",
                        "N", "R2 / Pseudo-R2", "Cluster"],
                 title="Table 2-bis. Convergent evidence across designs")
rt.to_word ("tables/table2b_design_race.docx")
rt.to_excel("tables/table2b_design_race.xlsx")
open("tables/table2b_design_race.tex", "w").write(rt.to_latex())
```

### 4.3 Pattern C — Multi-outcome table (same X, several Y's)
A single treatment, several outcomes. Use `dep_var_labels` so each column carries the Y name.

```python
ys = ["wage", "log_wage", "weeks_employed", "left_firm", "promoted"]
multi_y = [sp.feols(f"{y} ~ training + age + edu + tenure | industry + year",
                     df, vcov={"CRV1": "firm_id"})
           for y in ys]

rt = sp.regtable(*multi_y,
                 template="aer",
                 dep_var_labels=ys,                    # column header: dep var
                 model_labels=["(1)","(2)","(3)","(4)","(5)"],
                 stats=["N","R2","DV mean","Cluster"],
                 title="Table 2-ter. Effect of training on multiple outcomes")
rt.to_word ("tables/table2c_multi_outcome.docx")
rt.to_excel("tables/table2c_multi_outcome.xlsx")
open("tables/table2c_multi_outcome.tex", "w").write(rt.to_latex())
```

### 4.4 Pattern D — Stacked Panel A / Panel B table
Same model family, two horizons (short-run / long-run) or two samples (pre-2015 / post-2015) stacked vertically. Use `panel_labels`.

```python
panelA = [sp.feols("wage_t1 ~ training + X | industry + year",  df, vcov={"CRV1":"firm_id"}),
          sp.feols("wage_t1 ~ training + X | worker_id + year", df, vcov={"CRV1":"firm_id"})]
panelB = [sp.feols("wage_t5 ~ training + X | industry + year",  df, vcov={"CRV1":"firm_id"}),
          sp.feols("wage_t5 ~ training + X | worker_id + year", df, vcov={"CRV1":"firm_id"})]

rt = sp.regtable(*panelA, *panelB,
                 template="aer",
                 panel_labels=["Panel A. Short-run (1 year)",
                               "Panel A. Short-run (1 year)",
                               "Panel B. Long-run (5 years)",
                               "Panel B. Long-run (5 years)"],
                 model_labels=["(1) Industry FE","(2) Worker FE"]*2,
                 stats=["N","R2"],
                 title="Table 2-quater. Short- vs long-run effects")
rt.to_word ("tables/table2d_horizons.docx")
rt.to_excel("tables/table2d_horizons.xlsx")
open("tables/table2d_horizons.tex", "w").write(rt.to_latex())
```

### 4.5 Pattern E — IV reporting triplet (first-stage / reduced-form / 2SLS)
The textbook AER IV table presents the **first stage**, the **reduced form**, and the **2SLS** in three columns so the reader can verify Wald-ratio = RF / FS.

> **Trap:** `sp.ivreg` does **not** absorb `| fe` and does **not** parse `C(fe)` — it **silently drops** a `| industry + year` term (identical β̂ with or without it), so a 2SLS column written that way would not control for the FE the first-stage/reduced-form columns absorb. Keep the IV triplet on the **same low-dim control set** in all three columns; to control for fixed effects in a 2SLS, pre-build dummy columns in pandas and add them explicitly, or partial the FE out first.

```python
fs = sp.feols("training ~ Z + age + edu", df, vcov={"CRV1":"firm_id"})   # 1st stage
rf = sp.feols("wage     ~ Z + age + edu", df, vcov={"CRV1":"firm_id"})   # reduced form
iv = sp.ivreg("wage ~ (training ~ Z) + age + edu", df, cluster="firm_id")  # 2SLS (same controls)

rt = sp.regtable(fs, rf, iv,
                 template="aer",
                 keep=["Z", "training"],               # IV triplet is intentionally focal:
                                                       # show only Z + endog so the reader can
                                                       # eyeball Wald-ratio = RF / FS. For the
                                                       # full coef list, drop the kwarg entirely.
                 dep_var_labels=["training", "wage", "wage"],
                 model_labels=["(1) First stage", "(2) Reduced form", "(3) 2SLS"],
                 stats=["First-stage F", "N", "R2", "Cluster"],
                 title="Table 2-quinto. IV reporting triplet")
rt.to_word ("tables/table2e_iv_triplet.docx")
rt.to_excel("tables/table2e_iv_triplet.xlsx")
open("tables/table2e_iv_triplet.tex", "w").write(rt.to_latex())
```

### 4.6 Pattern F — Causal-design main via `sp.causal(...)`
For DID / IV / RD / SCM mains, the `sp.causal(...)` orchestrator returns a `CausalResult` plus diagnostics and an automatic robustness preview. Pipe `.result` into `regtable`:

```python
w = sp.causal(df, y="wage", treatment="training",
              id="worker_id", time="year", design="did",
              covariates=["age", "edu", "tenure"],
              dag=discovered.to_dag())             # optional (LLMConstrainedDAGResult.to_dag())
print(w.diagnostics)                               # PT verdict + warnings
print(w.recommendation)                            # which estimator + why
print(w.result.summary())                          # point estimate + cluster-robust SE + CI
print(w.robustness_findings)                       # automated robustness battery preview
```

### 4.7 Figure 3 — coefficient plot of the main table
Replace one of the wall-of-numbers tables with a coefplot in the body, push the table to the appendix. Modern AER papers increasingly do this.

```python
fig, ax = sp.coefplot(M1, M2, M3, M4, M5,
                      model_names=["(1)","(2)","(3)","(4)","(5)"],
                      variables=["training"],
                      title="Figure 3. β̂ on training across specifications (95% CI)",
                      alpha=0.05)
fig.savefig("figures/fig3_coefplot.png", dpi=300)
```

### Reporting checklist for the Table 2 footnote (AER house style)
- Standard-error cluster level (and whether it's two-way / Conley)
- Fixed-effects absorbed — `regtable` auto-adds **one footer row per FE name** (e.g. `Industry FE: Yes / Year FE: Yes / Worker_id FE: No`) whenever any column comes from `sp.feols(... | fe1 + fe2 ...)`. Don't hand-roll these rows.
- Sample size **and number of clusters**
- Estimator (OLS / 2SLS / CS-DID / SCM / DML)
- Stars convention `* 0.10  ** 0.05  *** 0.01`
- Mean of dependent variable in the estimation sample (so β̂ can be read as a % of the base rate)

## Step 5 — Heterogeneity (Table 3 + Figure 4)

The AER §5 *Heterogeneity* combines (a) a **subgroup regression table** with one column per subgroup (binary moderators + interaction terms), and (b) a **CATE / dose-response figure** for continuous moderators. Both should appear; they answer different questions.

### 5.1 Pattern G — Subgroup `regtable` (Table 3)
One column per subgroup, with the same specification re-run on each slice. Clean, easy to read, expected by referees.

```python
slices = {
    "(1) All":        df,
    "(2) Female":     df[df["female"] == 1],
    "(3) Male":       df[df["female"] == 0],
    "(4) Low skill":  df[df["skill_quartile"].isin([1, 2])],
    "(5) High skill": df[df["skill_quartile"].isin([3, 4])],
    "(6) Small firm": df[df["firm_size"] < 100],
    "(7) Large firm": df[df["firm_size"] >= 100],
}
gmodels = [sp.feols("wage ~ training + age + edu + tenure | industry + year",
                     d, vcov={"CRV1": "firm_id"}) for d in slices.values()]

rt = sp.regtable(*gmodels,
                 template="aer",
                 coef_labels={"training": "Training"},
                 model_labels=list(slices),
                 stats=["N","R2","DV mean"],
                 title="Table 3. Heterogeneous effects of training")
rt.to_word ("tables/table3_heterogeneity.docx")
rt.to_excel("tables/table3_heterogeneity.xlsx")
open("tables/table3_heterogeneity.tex", "w").write(rt.to_latex())
```

### 5.2 Interaction-form heterogeneity (alternative Table 3)
Test moderation formally with interaction terms — referees often ask whether the gap between subgroups is statistically significant, which requires the interaction p-value.

```python
H1 = sp.feols("wage ~ training*female + age + edu + tenure | industry + year",
              df, vcov={"CRV1": "firm_id"})
H2 = sp.feols("wage ~ training*C(skill_quartile) + age + edu + tenure | industry + year",
              df, vcov={"CRV1": "firm_id"})
H3 = sp.feols("wage ~ training*log_firm_size + age + edu + tenure | industry + year",
              df, vcov={"CRV1": "firm_id"})

rt = sp.regtable(H1, H2, H3,
                 template="aer",
                 keep=["training", "training:female", # interaction-form heterogeneity
                       "training:C(skill_quartile)[T.2]",   # is intentionally focal:
                       "training:C(skill_quartile)[T.3]",   # only the main effect + interactions
                       "training:C(skill_quartile)[T.4]",   # are reported. Drop this kwarg
                       "training:log_firm_size"],           # entirely to show full controls.
                 model_labels=["(1) ×Female", "(2) ×Skill quartile", "(3) ×log(Firm size)"],
                 stats=["N","R2"],
                 title="Table 3-bis. Interaction-form heterogeneity")
rt.to_word ("tables/table3b_interactions.docx")
rt.to_excel("tables/table3b_interactions.xlsx")
open("tables/table3b_interactions.tex", "w").write(rt.to_latex())
```

### 5.3 Figure 4 — dose-response (continuous treatment)
```python
dr = sp.dose_response(df, y="wage", treat="training_hours",
                      covariates=["age","edu","tenure","firm_size"],
                      n_dose_points=20)
fig, ax = dr.plot(title="Figure 4a. Dose-response: training hours → wage")
fig.savefig("figures/fig4a_dose_response.png", dpi=300)

# DID-flavored continuous treatment (de Chaisemartin–D'Haultfœuille):
fig, ax = sp.continuous_did(df, y="wage", dose="training_hours",
                            time="year", id="worker_id").plot()
fig.savefig("figures/fig4a2_continuous_did.png", dpi=300)
```

### 5.4 Figure 4-bis — CATE distribution (DR-Learner / causal forest)
The CATE plotters read per-row conditional effects out of the result's
`model_info["cate"]` array. **There is no `.cate_estimates` attribute** — the raw
per-row CATE vector lives at `ml.model_info["cate"]` (an ndarray of length *n*),
and summary stats at `model_info["cate_mean"] / cate_q25 / cate_q75 / ...`.
`sp.causal_forest` returns a *summary* result that does not populate
`model_info["cate"]`, so for the CATE histogram and grouped bar chart use a
meta-learner (or any DR-/X-/R-learner) and pass its result to the plotters.

```python
ml = sp.metalearner(df, y="wage", treat="training",
                    covariates=["age","edu","tenure","firm_size"], learner="dr")

# Raw per-row CATE vector (if you need the numbers, not just the figure):
cate_i = ml.model_info["cate"]                        # ndarray, length n  (NOT ml.cate_estimates)

fig, ax = sp.cate_plot(ml, kind="hist",
                       title="Figure 4b. Distribution of conditional ATE")
fig.savefig("figures/fig4b_cate_hist.png", dpi=300)

# CATE by group bar chart: first compute the group-level table, THEN plot it.
# `cate_group_plot` takes a DataFrame (from cate_by_group), not the result object.
g = sp.cate_by_group(ml, df, by="skill_quartile", n_groups=4)
fig, ax = sp.cate_group_plot(g, title="Figure 4c. CATE by skill quartile")
fig.savefig("figures/fig4c_cate_by_group.png", dpi=300)

# Tabular summary for the appendix
print(sp.cate_summary(ml))
print(g)                                              # group-level CATE table
```

### 5.5 Subgroup-analysis dispatcher (one-liner)
```python
sp.subgroup_analysis(df, formula="wage ~ training + age + edu + tenure",
                     x="training",
                     by={"gender": "female", "skill": "skill_quartile"},
                     robust="hc1")                 # quick subgroup β̂ table (HC1 by default; no cluster arg)
```

For continuous moderators or many subgroups, prefer:
- `sp.continuous_did(...)` — dose-response under DID
- `sp.metalearner(..., learner="dr")` + `sp.cate_plot` / `sp.cate_by_group` — DR-Learner CATE (recommended for plotting)
- `sp.causal_forest(formula="wage ~ training | X", data=df)` — CATE summary only (does not populate `model_info["cate"]`; use a meta-learner for per-row CATEs)

## Step 6 — Mechanisms / channels

```python
sp.mediation(df, y="wage", d="training", m="hours_worked",
             X=["age", "edu", "tenure"])           # ACME / ADE / total effect
sp.decompose(...)                                   # Oaxaca-Blinder / RIF / FFL / KOB
```

## Step 7 — Robustness gauntlet (the AER referee gauntlet)

The seven canonical robustness blocks of an applied paper. A modern AER paper expects most of these in the body or appendix — assemble a Table A1-style robustness panel from the outputs.

### 7.1 Placebo tests
```python
sp.rdplacebo(df, y="y", x="running_var", c=0,
             placebo_cutoffs=[-2, -1, 1, 2])                      # RD: fake cutoffs
sp.synth_time_placebo(df, outcome="y", unit="unit", time="time",
                      treated_unit=1, treatment_time=2000,
                      n_placebo_times=10)                          # SCM in-time placebo
sp.synthdid_placebo(...)                                           # SDID placebo
# For DID: re-run with a fake treat year before actual treatment and confirm β̂ ≈ 0.
```

### 7.2 Alternative samples
```python
result_no_outliers = sp.causal(df.query("wage < wage.quantile(0.99)"), ...)
result_drop_early  = sp.causal(df.query("first_treat_year > 2008"),  ...)
result_balanced    = sp.causal(sp.balance_panel(df, entity="worker_id", time="year"), ...)
```

### 7.3 Alternative specifications (spec curve)
```python
sp.spec_curve(df, y="wage", x="training",
              controls=[["age"], ["age", "edu"], ["age", "edu", "tenure"]],
              subsets={"all": None, "manuf": df["industry"].eq("manufacturing")})
```

### 7.4 Alternative standard errors
Cluster-level choice is itself a robustness check — show the result is not driven by an over-narrow cluster.

```python
# For statsmodels-backed sp.regress / sp.ivreg results:
sp.twoway_cluster(M3, df, cluster1="firm_id", cluster2="year")     # two-way clustering
sp.conley(M3, df, lat="lat", lon="lon",
          dist_cutoff=100, kernel="uniform")                        # spatial HAC (Conley 1999)

# For pyfixest-backed sp.feols results, set 2-way cluster directly in `vcov`:
sp.feols("y ~ x | firm_id + year", df,
         vcov={"CRV1": "firm_id+year"})                              # 2-way: firm × year
```

### 7.5 Oster (2019) selection bound
"How big would unobserved selection have to be for β to flip sign / vanish?" The Oster δ tells you whether the bound on selection on unobservables, relative to selection on observables, has to exceed an implausible value to overturn the result.

```python
sp.oster_bounds(data=df, y="wage", treat="training",
                controls=["age", "edu", "tenure"],
                r_max=1.3)                          # β* assuming δ=1, R̃²=1.3·R²
# `oster_delta` uses x_base / x_controls (NOT treat= / controls=):
sp.oster_delta(data=df, y="wage",
               x_base=["training"],                 # treatment(s) of interest
               x_controls=["age", "edu", "tenure"], # observed controls
               r_max=1.3)                           # δ for which β=0
```

### 7.6 Honest DID — Rambachan–Roth (2023) PT sensitivity
`honest_did` only consumes a CS / SA / `did_multiplegt` event-study result
(or `aggte(result, type='dynamic')`). Pass the `cs` object built in §3.1,
not a generic OLS/FE main-table result:

```python
sp.honest_did(cs, method="smoothness")              # bound β under bounded PT violation
```

### 7.7 E-value & unified sensitivity (unmeasured confounding)
```python
sp.evalue(estimate=result.params["training"],       # E-value takes point + CI, NOT result
          ci=tuple(result.conf_int().loc["training"]),
          measure="RR")
sp.unified_sensitivity(result, r2_treated=0.05,
                       r2_controlled=0.10,
                       include_oster=True)          # Cinelli-Hazlett + Oster combined
sp.sensitivity_dashboard(result)                    # one-page sensitivity figure
```

### 7.8 RD-specific bandwidth / kernel sensitivity
```python
sp.rdbwsensitivity(df, y="y", x="running_var", c=0,
                    bw_grid=[0.5, 1.0, 1.5, 2.0])   # is β̂ stable across bandwidths?
```

### 7.9 TWFE diagnostic (staggered DID)
Goodman-Bacon decomposition flags when the TWFE estimate is contaminated by forbidden 2×2's (already-treated as control).

```python
sp.bacon_decomposition(df, y="y", treat="training",
                       time="year", id="worker_id")
```

### 7.10 Sequential confounder blocks (Oster-style robustness table)
```python
blocks = {
    "M1 base":           [],
    "M2 +demographics":  ["age", "edu"],
    "M3 +labor-market":  ["age", "edu", "tenure", "firm_size"],
    "M4 +psychosocial":  ["age", "edu", "tenure", "firm_size", "motivation"],
}
models = [sp.regress(f"wage ~ training + {' + '.join(c) or '1'}",
                     df, cluster="firm_id")
          for c in blocks.values()]
rt = sp.regtable(*models,
                 template="aer",
                 model_labels=list(blocks),
                 title="Table 7. Selection-stability across confounder blocks")
rt.to_word ("tables/table_robust_blocks.docx")
rt.to_excel("tables/table_robust_blocks.xlsx")
open("tables/table_robust_blocks.tex", "w").write(rt.to_latex())
```

### 7.11 Pattern H — Robustness master table (Table A1, one row per check)
The canonical AER appendix Table A1 stacks every robustness specification next to the baseline so reviewers see at a glance that β̂ survives. `sp.regtable` accepts any mix of `EconometricResults` / `CausalResult`, so build the list dynamically:

```python
baseline = sp.feols("wage ~ training + age + edu + tenure | industry + year",
                     df, vcov={"CRV1": "firm_id"})

rob = {
    "(1) Baseline":            baseline,
    "(2) Drop top 1% wage":    sp.feols("wage ~ training + age + edu + tenure | industry + year",
                                        df.query("wage < wage.quantile(0.99)"),
                                        vcov={"CRV1": "firm_id"}),
    "(3) Balanced panel":      sp.feols("wage ~ training + age + edu + tenure | industry + year",
                                        sp.balance_panel(df, entity="worker_id", time="year"),
                                        vcov={"CRV1": "firm_id"}),
    "(4) Drop early cohorts":  sp.feols("wage ~ training + age + edu + tenure | industry + year",
                                        df.query("first_treat_year > 2008"),
                                        vcov={"CRV1": "firm_id"}),
    "(5) Worker FE":           sp.feols("wage ~ training + age + edu + tenure | worker_id + year",
                                        df, vcov={"CRV1": "firm_id"}),
    "(6) 2-way cluster":       sp.feols("wage ~ training + age + edu + tenure | industry + year",
                                        df, vcov={"CRV1": "firm_id+year"}),  # 2-way: firm × year
    # sp.conley needs a STATSMODELS-backed result (sp.regress/sp.ivreg) — it raises
    # KeyError on a pyfixest feols result. Re-fit the spec via sp.regress for this row.
    "(7) Conley spatial SE":   sp.conley(sp.regress("wage ~ training + age + edu + tenure",
                                                    df, cluster="firm_id"),
                                         df, lat="lat", lon="lon", dist_cutoff=100),
    "(8) Log outcome":         sp.feols("log_wage ~ training + age + edu + tenure | industry + year",
                                        df, vcov={"CRV1": "firm_id"}),
    "(9) IHS outcome":         sp.feols("ihs_wage ~ training + age + edu + tenure | industry + year",
                                        df, vcov={"CRV1": "firm_id"}),
    "(10) PSM-weighted":       sp.match(df, y="wage", treat="training",
                                         covariates=["age","edu","tenure","firm_size"],
                                         method="nearest"),
    "(11) Entropy balance":    sp.ebalance(df, y="wage", treat="training",
                                            covariates=["age","edu","tenure","firm_size"]),
    "(12) DML-PLR":            sp.dml(df, y="wage", treat="training",
                                       covariates=["age","edu","tenure","firm_size"], model="plr"),
}

# Robustness master = AER Table A1 — readers MUST see every coefficient
# across every spec to verify nothing is hiding behind `keep=`. Default to
# the full coef table (intercept included); only switch to
# `keep=["training"]` if a referee has explicitly asked for a focal-only
# summary, or add `drop=["Intercept"]` if you want the constant suppressed.
rt = sp.regtable(*rob.values(),
                 template="aer",
                 coef_labels={"training": "Training (β̂)"},
                 model_labels=list(rob),
                 stats=["N", "R2", "Cluster", "FE"],
                 title="Table A1. Robustness of the main estimate")
rt.to_word ("tables/tableA1_robustness.docx")
rt.to_excel("tables/tableA1_robustness.xlsx")
open("tables/tableA1_robustness.tex", "w").write(rt.to_latex())

# Equivalent one-shot via the paper-format multi-panel API — produces a
# single .docx / .xlsx that you can hand a co-author, with main + robustness
# (+ heterogeneity / placebo if you have them) auto-laid-out per AER style:
sp.paper_tables(main=[M1, M2, M3, M4, M5],
                robustness=list(rob.values()),
                template="aer",
                coef_labels={"training": "Training"},
                model_labels_main=["(1)","(2)","(3)","(4)","(5)"],
                model_labels_robustness=list(rob),
                # paper_tables only accepts `keep=`, not `drop=`. Omit both to
                # show every coefficient (AER convention). Pass `keep=["training"]`
                # only when a focal-only summary is desired.
                ).to_docx("tables/paper_tables.docx")
```

### 7.12 Figure 5 — coefficient forest plot of all robustness specs
A single visual summary that an AER referee can parse in 5 seconds: every β̂ and 95% CI on one axis. Confirms the estimate is not knife-edge.

```python
fig, ax = sp.coefplot(*rob.values(),
                      model_names=list(rob),
                      variables=["training"],
                      title="Figure 5. β̂ on training across robustness specifications",
                      alpha=0.05)
fig.savefig("figures/fig5_robustness_forest.png", dpi=300)
```

### 7.13 Figure 5-bis — spec curve
The Simonsohn et al. (2020) specification curve plots β̂ across **every combination** of {controls × subsamples × outcome transforms × SE types}. Useful when you want to head off "what about specification X?" referee letters.

```python
# se_types accepts only: 'nonrobust', 'hc1' (alias 'robust'), 'cluster' (needs cluster_var).
# y_transforms is a DICT {name: callable} — NOT a list of strings.
sc = sp.spec_curve(df, y="wage", x="training",
                   controls=[["age"], ["age","edu"], ["age","edu","tenure"],
                             ["age","edu","tenure","firm_size"]],
                   se_types=["nonrobust", "robust", "cluster"],   # 'cluster' uses cluster_var below
                   y_transforms={"level": lambda s: s,
                                 "log":   np.log,
                                 "ihs":   np.arcsinh},
                   subsets={"all": None,
                            "manuf":  df["industry"].eq("manufacturing"),
                            "no99":   df["wage"] < df["wage"].quantile(0.99)},
                   cluster_var="firm_id")
fig, ax = sc.plot(title="Figure 5-bis. Specification curve")
fig.savefig("figures/fig5b_spec_curve.png", dpi=300)
```

### 7.14 Figure 6 + sensitivity dashboard
`sp.unified_sensitivity(...)` and `sp.sensitivity_dashboard(...)` both return a
**text/numeric** `SensitivityDashboard` (Cinelli–Hazlett + Oster + Rosenbaum +
E-value). It is **not** a figure — it has `.summary()` and numeric attributes
(`.e_value_point`, `.e_value_ci`, `.oster`, `.rosenbaum`, `.sensemakr`, `.breakdown`),
**no `.plot()` / `.savefig()` / `.results`**. The sensitivity *figure*
(`sp.sensitivity_plot`) is a Rambachan–Roth honest-DID plot and consumes the
DataFrame returned by `sp.honest_did(...)` (columns `M / ci_lower / ci_upper / rejects_zero`).

```python
# (a) Numeric sensitivity dashboard — print the summary, read the attributes.
dash = sp.unified_sensitivity(baseline, r2_treated=0.05, r2_controlled=0.10,
                              include_oster=True)
print(dash.summary())                                 # one-page text dashboard
print(dash.e_value_point, dash.e_value_ci)            # numeric fields for the §7 prose
# sp.sensitivity_dashboard(baseline).summary() is the auto-dimensioned variant.

# (b) Sensitivity FIGURE (honest-DID PT sensitivity) — needs a CS/SA event-study
#     result (`cs` from §3.1) and its honest_did() DataFrame.
sens_df = sp.honest_did(cs, method="smoothness")      # → DataFrame (M, ci_lower, ci_upper, ...)
fig, ax = sp.sensitivity_plot(sens_df,
                              original_estimate=cs.estimate,
                              original_ci=cs.ci,
                              title="Figure 6. Sensitivity to PT violations (Rambachan–Roth)")
fig.savefig("figures/fig6_sensitivity.png", dpi=300)
```

### 7.15 One-stop robustness reporter
```python
sp.diagnose_result(result)                          # PT / weak-IV / overlap / leverage verdict
sp.robustness_report(df, formula="wage ~ training + age + edu",
                     x="training", cluster_var="firm_id")
sp.estat(result, test="all")                        # Stata-style postestimation battery
```

## Step 8 — Replication package

The agent's job at §8 is to produce a **single artifact a co-author can open in Word, Excel, or LaTeX without further StatsPAI calls**. There are three packaging tiers, picked by what you need to ship:

### 8.1 Per-result export (one estimator → one Word/Excel file)
```python
result.to_docx("tables/main_result.docx",
               title="Table 2. Main result")          # CausalResult → .docx
result.to_latex(caption="Main result", label="tab:main")
fig, ax = result.plot()                               # publication-quality figure → (fig, ax)
fig.savefig("figures/main.png", dpi=300)
print(sp.cite(result, "training"))                    # → "1.239*** (0.153)"  ← inline citation
```

### 8.2 Per-table export (already covered in Steps 4 / 5 / 7)
Every `sp.regtable(*models)` returns a `RegtableResult` with `.to_word()` / `.to_excel()` / `.to_latex()` / `.to_markdown()` / `.to_html()`. Use these in §4–§7 so that by the time you reach §8 the `tables/` folder already has parallel `.docx` / `.xlsx` / `.tex` for every numbered table.

### 8.3 Multi-panel paper-format (Tier 2 — Tables 2 + 3 + A1 + A2 in one file)
```python
sp.paper_tables(
    main          = [M1, M2, M3, M4, M5],            # → "Table 2. Main results"
    heterogeneity = [g_full, g_fem, g_male],         # → "Table 3. Heterogeneity"
    robustness    = list(rob.values()),              # → "Table A1. Robustness"
    placebo       = [pb1, pb2],                      # → "Table A2. Placebo tests"
    template      = "aer",
    coef_labels   = {"training": "Training"},
    keep          = ["training"],
).to_docx("replication/paper_tables.docx")           # → 4 panels in one .docx
# .to_xlsx(...) writes one sheet per panel; .to_latex(...) one .tex with section breaks.
```

### 8.4 Full session bundle (Tier 3 — the Stata `collect` equivalent)
The single most efficient §8 deliverable: descriptives + balance + main + heterogeneity + robustness + prose **in one Word file**. `sp.collect()` is the agent-native counterpart of Stata 15's `collect` and R's `gtsave`.

```python
c = sp.collect("Effect of Training on Wages — Replication", template="aer")

c.add_heading("§1. Descriptive statistics", level=1)
c.add_summary(df, vars=["wage","age","edu","tenure"],
              stats=["mean","sd","n"],
              title="Table 1. Summary statistics")
c.add_balance(df, treatment="training",
              variables=["age","edu","tenure","firm_size"],
              title="Table 1b. Balance by treatment")

c.add_heading("§4. Main results",        level=1)
c.add_regression(M1, M2, M3, M4, M5,
                 model_labels=["(1)","(2)","(3)","(4)","(5)"],
                 stats=["N","R2","Cluster","FE"],
                 title="Table 2. Effect of training on wages")

c.add_heading("§5. Heterogeneity",       level=1)
c.add_regression(*gmodels,
                 model_labels=list(slices),
                 title="Table 3. Heterogeneous effects")

c.add_heading("§7. Robustness",          level=1)
c.add_regression(*rob.values(),
                 model_labels=list(rob),
                 title="Table A1. Robustness")

c.add_text(
    "Standard errors clustered at the firm level. *** p<0.01, ** p<0.05, * p<0.10. "
    "Sample restrictions and full variable definitions are documented in "
    "artifacts/sample_construction.json and artifacts/data_contract.json.",
    title="Notes",
)

# One artifact, three formats — auto-detected from the path extension:
c.save("replication/paper.docx")   # editable Word, page-break between tables
c.save("replication/paper.xlsx")   # one sheet per add_*() item
c.save("replication/paper.tex")    # multi-section LaTeX
c.save("replication/paper.md")     # GitHub-flavoured Markdown for the README
```

Inspect the bundle before saving:

```python
print(c)                # → <Collection title='...' template='aer' items=8 kinds=['heading','summary','balance',...]>
print(c.list())         # DataFrame with name / kind / title for every item
```

### 8.5 Reproducibility stamp

> A `CausalResult` (from DID / CS / IV-causal / DML / TMLE / …) exposes `.estimate` (scalar), `.ci` (tuple), `.estimand`, and `.n_obs` — it has **no** `.conf_int()`, and `.data_info`'s key is `"nobs"`, not `"n_obs"`. An `EconometricResults` (regress / feols / ivreg) instead exposes `.params[name]` and `.conf_int().loc[name]` — use that branch for an OLS/FE main result.

```python
import json
ci = result.ci                                    # CausalResult: (lo, hi) tuple
json.dump({
    "statspai":          sp.__version__,
    "seed":              42,
    "n_obs":             int(result.n_obs),
    "estimand":          result.estimand,
    "estimate":          float(result.estimate),
    "ci95":              [float(ci[0]), float(ci[1])],
    # Econometric (feols/regress) main result instead:
    #   "estimate": float(M.params["training"]),
    #   "ci95":     list(M.conf_int().loc["training"]),
    "pre_registration":  "artifacts/empirical_strategy.md",
    "data_contract":     "artifacts/data_contract.json",
    "sample_log":        "artifacts/sample_construction.json",
    "paper_bundle":      "replication/paper.docx",
}, open("artifacts/result.json", "w"), indent=2)
```

For full-draft generation (abstract + methods + results + bibliography), see `sp.paper(result, ...)` — out of scope for this skill; call it only when the user explicitly asks for a paper draft.

---

## Regtable cookbook (one-page recipe index)

`sp.regtable(*models, ...)` is the single primitive behind every multi-regression table in an AER paper. The eight patterns above map to:

| Pattern | What varies across columns | Step |
|---|---|---|
| **A. Progressive controls** | covariate set / FE depth | 4.1 — Table 2 |
| **B. Design horse race** | identification strategy (OLS / 2SLS / DID / DML / PSM) | 4.2 — Table 2-bis |
| **C. Multi-outcome** | dependent variable Y | 4.3 — Table 2-ter |
| **D. Stacked Panel A / B** | horizon / sample (panel rows × spec columns) | 4.4 — Table 2-quater |
| **E. IV reporting triplet** | first stage / reduced form / 2SLS | 4.5 — Table 2-quinto |
| **F. `sp.causal(...)` orchestrator** | 1 column, full diagnostics | 4.6 |
| **G. Subgroup table** | subsample (full / female / male / Q1…Q4) | 5.1 — Table 3 |
| **H. Robustness master** | every robustness check stacked | 7.11 — Table A1 |

Default `sp.regtable` settings for AER house style — and the export pipeline
(produce `.docx` + `.xlsx` + `.tex` from the same `RegtableResult`):

```python
rt = sp.regtable(*models,
                 template="aer",                  # journal preset: aer/qje/econometrica/restat/jf/aeja/jpe/restud
                 # AER convention: pass NEITHER `keep=` NOR `drop=` —
                 # `regtable` will then surface every estimated parameter
                 # (controls AND the intercept). Add `drop=["Intercept"]`
                 # only if you want the constant suppressed; add
                 # `keep=[focal]` only for an intentional focal-only table.
                 coef_labels={"training": "Training"},
                 model_labels=[...],              # column labels
                 stats=["N", "R2", "Cluster", "FE", "DV mean"],
                 title="Table N. ...")

# One-call exports — never hand-roll Word/Excel from pandas:
rt.to_word ("tables/tableN.docx")                  # editable Word, AER book-tab borders
rt.to_excel("tables/tableN.xlsx")                  # editable Excel, one sheet
open("tables/tableN.tex", "w").write(rt.to_latex()) # LaTeX for the build
print(rt.to_text())                                 # quick terminal preview
```

For pyfixest-style native output, `sp.etable(*models, ...)` is the alternative; for stacking many tables in one `.docx`, use `sp.paper_tables(...)` (Tier 2) or `sp.collect()` (Tier 3) — see Step 8.

## Figure factory (the 12 standard AER figures)

| # | Figure | StatsPAI call | Section |
|---|---|---|---|
| 1a | Raw trends (DID Figure 1) | `sp.parallel_trends_plot(df, y, time, treat, treat_time, ci=True)` | §1 |
| 1b | Treatment rollout heatmap | `sp.treatment_rollout_plot(df, time, treat, id)` | §1 |
| 2a | Event-study coefficients | `sp.enhanced_event_study_plot(cs)` *(cs = `sp.callaway_santanna(...)`; **not** `event_study()` output)* | §3 |
| 2a' | Bacon weights | `sp.bacon_plot(sp.bacon_decomposition(...))` | §3 |
| 2a'' | CS-DID dynamic effects | `cs.plot()` · `sp.ggdid(cs)` · `sp.group_time_plot(cs)` | §3 |
| 2b | RD canonical plot | `sp.rdplot(df, y, x, c)` | §3 |
| 2b' | McCrary density | `sp.rddensity(df, x, c).plot()` | §3 |
| 2c | Matching love plot | `sp.match(...).plot()` | §3 |
| 2d | SCM trajectory | `sp.synth(...).plot()` · `sp.synthdid_plot(sp.sdid(...))` | §3 |
| 3 | Coefficient plot of main specs | `sp.coefplot(M1...M5, variables=["x"])` | §4 |
| 4a | Dose-response | `sp.dose_response(...).plot()` | §5 |
| 4b | CATE histogram | `sp.cate_plot(ml, kind="hist")`  *(ml = `sp.metalearner(..., learner='dr')`)* | §5 |
| 4c | CATE by group bar | `g = sp.cate_by_group(ml, df, by=..., n_groups=4); sp.cate_group_plot(g)` | §5 |
| 5 | Robustness forest plot | `sp.coefplot(*rob.values(), variables=["x"])` | §7 |
| 5b | Specification curve | `sp.spec_curve(...).plot()` | §7 |
| 6 | Sensitivity (text dashboard + honest-DID figure) | `print(sp.sensitivity_dashboard(result).summary())` · `sp.sensitivity_plot(sp.honest_did(cs, ...))` | §7 |
| 7 | Final result.plot() | `result.plot()` (estimator-specific) | §8 |

> Every plotting function above accepts `ax=` so panels can be combined with matplotlib subplots, and **returns a `(fig, ax)` tuple** — unpack it and call `fig.savefig(path, dpi=300)` for publication output (see "Saving figures — the `(fig, ax)` idiom" above). `sp.binscatter` returns `(fig, ax, binned_df)`; `sp.kaplan_meier(...).plot()` returns a bare `Axes` (use `ax.figure.savefig(...)`).

---

## §A. Epidemiology / public health pipeline (Mode A)

> **Convention**: STROBE (observational) / TRIPOD-AI (prediction) reporting. A modern epidemiology reference design is **target-trial emulation** (Hernán & Robins): write the protocol of the hypothetical RCT first, then emulate it with observational data using a doubly-robust estimator. Outcomes are commonly **risk differences, risk ratios, hazard ratios, or restricted mean survival time**, not just OLS coefficients. The skill mirrors the AER 8-section flow but swaps the Step-4 estimator stack and adds survival/MR-specific reporting rows.

Running example: `statin_initiation → 5-yr_MACE` in an EHR cohort (`patient_id / index_date / age / sex / ldl_baseline / comorbidity_index / followup_days / event`). The exposure is time-varying, confounders are time-varying, and competing-risk censoring matters — the canonical setting where naïve OLS / Cox-with-baseline-adjustment is biased.

### A.0 Cohort construction & target-trial protocol

```python
import statspai as sp

# Eligibility, treatment-strategy, time-zero, follow-up, outcome — written down BEFORE estimation.
# NOTE the two validated enum fields:
#   • assignment    ∈ {"randomization", "observational emulation"}
#   • causal_contrast ∈ {"ITT", "per-protocol", "as-treated", "observational-analogue"}
# (free-text in these two fields raises ValueError). Put the prose description in `notes=`.
protocol = sp.target_trial.TargetTrialProtocol(
    eligibility           = "adults 40-75, LDL ≥ 130, no prior MI/stroke, no statin in 12mo washout",
    treatment_strategies  = ["initiate statin within 30d of index", "no statin within 30d"],
    assignment            = "observational emulation",       # enum — not free text
    time_zero             = "index_date (first eligible cardiology visit)",
    followup_end          = "first MACE / death / disenrollment / index_date + 5yr",
    outcome               = "first MACE (composite: MI, stroke, cardiovascular death)",
    causal_contrast       = "per-protocol",                  # enum — not free text
    analysis_plan         = "IPTW-MSM + g-formula + TMLE triplet; report all three with CIs",
    baseline_covariates   = ["age","sex","ldl_baseline","comorbidity_index","smoker"],
    time_varying_covariates = ["ldl_current"],
    notes                 = "emulate randomization via IPTW + g-formula; 5-yr risk difference",
)
# Signature: target_trial_emulate(protocol, data, outcome_col, treatment_col,
#                                 time_zero_filter=None, weights=None) -> TargetTrialResult.
# Eligibility is applied as `data.query(protocol.eligibility)` UNLESS you pass a
# `time_zero_filter` callable (which then defines the eligible/time-zero rows and
# lets `eligibility` stay human-readable prose). Use the callable for non-query-able rules:
cohort_res = sp.target_trial_emulate(
    protocol, df, outcome_col="mace", treatment_col="statin_initiation",
    time_zero_filter=lambda d: d["age"].between(40, 75) & (d["ldl_baseline"] >= 130),
)
cohort = df   # downstream estimators run on the eligible analysis frame you constructed
```

### A.1 Table 1 — baseline characteristics by exposure

```python
# Same sumstats stack as AER mode; binary 0/1 by= auto-renders Control/Treated.
mc = sp.mean_comparison(cohort, ["age","sex","ldl_baseline","comorbidity_index","smoker"],
                        group="statin_initiation", test="ttest",
                        title="Table 1. Baseline characteristics by statin initiation")
mc.to_word ("tables/table1_epi.docx")
mc.to_excel("tables/table1_epi.xlsx")
```

### A.2 Identification — DAG, propensity overlap, KM curves

```python
# 2.1 DAG (manual or LLM-assisted). sp.dag(spec) parses an edge STRING
# ("A -> B; C -> B"); build edges with the string spec or chained .add_edge(parent, child)
# (singular — there is no .add_edges). Back-door sets come from .adjustment_sets(exposure,
# outcome) (PLURAL, positional) and return a LIST of valid sets.
dag = sp.dag(
    "age -> ldl_baseline; age -> statin_initiation; "
    "ldl_baseline -> statin_initiation; ldl_baseline -> mace; "
    "comorbidity_index -> statin_initiation; comorbidity_index -> mace; "
    "statin_initiation -> mace"
)
adj = dag.adjustment_sets("statin_initiation", "mace")    # list of back-door sets, e.g. [{...}]

# 2.2 Propensity-score overlap (positivity check; epi convention before any IPW)
# Returns a pd.Series of fitted PS — draw mirrored histograms by exposure.
ps = sp.propensity_score(cohort, treatment="statin_initiation",
                          covariates=["age","sex","ldl_baseline","comorbidity_index","smoker"],
                          method="logit")
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(6,4))
ax.hist(ps[cohort["statin_initiation"]==1], bins=40, alpha=0.5, label="Treated")
ax.hist(ps[cohort["statin_initiation"]==0], bins=40, alpha=0.5, label="Control")
ax.set_xlabel("Estimated propensity score"); ax.legend()
fig.savefig("figures/figA1_ps_overlap.png", dpi=300)

# 2.3 Crude KM curves by exposure (descriptive identification graphic).
# KMResult.plot() returns a bare Axes (NOT a (fig, ax) tuple) — save via ax.figure.
km = sp.kaplan_meier(cohort, duration="followup_days", event="mace", group="statin_initiation")
ax = km.plot()
ax.figure.savefig("figures/figA2_km.png", dpi=300)
```

### A.3 Main estimate — IPTW · g-formula · TMLE triplet (the modern epi standard)

Report **all three** in one `regtable` so the reader sees convergent doubly-robust evidence — this is the epi equivalent of the AER design horse race:

```python
# (1) IPTW marginal structural model
iptw = sp.msm(cohort, y="mace", treat="statin_initiation",
              id="patient_id", time="month",
              time_varying=["ldl_current","comorbidity_index"],
              baseline=["age","sex"])

# (2) Parametric g-formula (g-computation). `sp.gformula` is a MODULE, not a function.
# For a point-treatment g-formula use the top-level `sp.g_computation`:
gcomp = sp.g_computation(cohort, y="mace", treat="statin_initiation",
                         covariates=["age","sex","ldl_baseline","comorbidity_index","smoker"])
# For a TIME-VARYING treatment/confounder g-formula (the Robins setting) use the
# Monte-Carlo g-formula in the module:
#   sp.gformula.gformula_mc(cohort, treatment_cols=["statin_t1","statin_t2",...],
#                           confounder_cols=[["ldl_t1"],["ldl_t2"],...],
#                           outcome_col="mace", strategy=(1,1,1), control_strategy=(0,0,0),
#                           id_col="patient_id", time_col="month")

# (3) TMLE -- doubly robust targeted learning estimator.
# Pass an sklearn-style library list for nuisance learners; statspai stacks them
# internally via SuperLearner. Keep `outcome_library` and `propensity_library`
# explicit so the reviewer can see your nuisance choices.
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
sl_lib = [LogisticRegression(max_iter=1000),
          GradientBoostingClassifier(),
          RandomForestClassifier()]
tmle = sp.tmle(cohort, y="mace", treat="statin_initiation",
               covariates=["age","sex","ldl_baseline","comorbidity_index","smoker"],
               outcome_library=sl_lib, propensity_library=sl_lib)

# (3-bis) HAL-TMLE if you want a fully nonparametric variant.
# `variant=` only accepts "delta" (the default; "projection" is NotImplemented).
hal = sp.hal_tmle(cohort, y="mace", treat="statin_initiation",
                  covariates=["age","sex","ldl_baseline","comorbidity_index","smoker"],
                  variant="delta")

# Convergent-evidence table — risk difference at 5 years
rt = sp.regtable(iptw, gcomp, tmle, hal,
                 model_labels=["(1) IPTW-MSM","(2) g-formula","(3) TMLE","(4) HAL-TMLE"],
                 stats=["N","Effect type","Risk diff. (RD)","Risk ratio (RR)"],
                 title="Table 2. Effect of statin initiation on 5-yr MACE — convergent estimators")
rt.to_word ("tables/table2_epi.docx"); rt.to_excel("tables/table2_epi.xlsx")
```

### A.4 Survival outcomes — KM / AFT / restricted mean

```python
import pandas as pd

# AFT formula LHS is "duration + event" (NOT R-style Surv(time, event)).
aft = sp.aft("followup_days + mace ~ statin_initiation + age + sex + ldl_baseline",
             cohort, family="weibull")
print(aft.summary())                                  # AFTResult exposes .summary() (text)

# AFTResult does NOT go into sp.regtable (it has no .params) and has no .to_word/.to_latex.
# Build a coefficient table from its attributes (.beta / .se / .var_names / .n / .n_events):
import numpy as np
aft_table = pd.DataFrame({"coef": aft.beta, "se": aft.se}, index=aft.var_names)
aft_table["z"] = aft_table["coef"] / aft_table["se"]
aft_table.to_excel("tables/table3_survival.xlsx")     # or .to_latex()
print(f"N={aft.n}, events={aft.n_events}, family={aft.family}, AIC={aft.aic:.1f}")

# For a CAUSAL survival estimand (risk/RMST contrast under unconfoundedness), use the
# doubly-robust longitudinal-TMLE survival estimator instead of a raw AFT:
#   sp.ltmle_survival(cohort, ...)   # returns an LTMLESurvivalResult
```

### A.5 Mendelian randomization (genetic IV — when relevant)

```python
import pandas as pd

# Standard MR triple: IVW → Egger → weighted median, on summary statistics.
# Each mr_* returns a DICT (keys: estimate, se, ci_lower, ci_upper, p_value, ...) —
# NOT a result object, so it does NOT go into sp.regtable. Assemble a DataFrame instead.
ivw    = sp.mr_ivw   (beta_exposure, beta_outcome, se_exposure, se_outcome)
egger  = sp.mr_egger (beta_exposure, beta_outcome, se_exposure, se_outcome)   # 'intercept'(_p) = pleiotropy test
median = sp.mr_median(beta_exposure, beta_outcome, se_exposure, se_outcome, penalized=True)

mr_table = pd.DataFrame(
    {"IVW": ivw, "MR-Egger": egger, "Weighted median": median}
).T[["estimate", "se", "ci_lower", "ci_upper", "p_value"]]
mr_table.to_excel("tables/table4_mr.xlsx")        # or .to_latex() / .to_markdown()
print(mr_table)
# Egger intercept ≠ 0 (egger["intercept_p"] < 0.05) flags directional pleiotropy.
```

### A.6 Robustness — E-value, bounds, principal stratification

```python
# E-value: minimum strength of unmeasured confounding to explain away the result.
# CausalResult exposes `.estimate` and `.ci` (there is NO `.point_estimate`).
ev = sp.evalue(estimate=tmle.estimate, ci=tmle.ci, measure="RR")
# → "E-value 1.84; CI E-value 1.42" (a confounder must be ~2x associated with both
#   exposure and outcome to nullify the effect — interpret in your domain)

# Manski / Lee bounds — `sp.bounds` is a MODULE; call the specific estimator:
bds  = sp.bounds.manski_bounds(cohort, y="mace", treat="statin_initiation")
# selection bias (truncation-by-death / attrition): sp.bounds.lee_bounds(..., selection="observed")

# Principal stratification — BOTH `strata` and `instrument` must be BINARY (0/1) columns
# that already exist in the frame (build them first; they are NOT created for you).
cohort["high_density_zip"] = (cohort["zip_pharmacy_density"] > 0).astype(int)   # binary instrument
cohort["adherent"]         = (cohort["adherence_score"] > 0.8).astype(int)      # 0/1 stratum indicator
ps_strat = sp.principal_strat(cohort, y="mace", treat="statin_initiation",
                              instrument="high_density_zip",
                              strata="adherent")
```

### A.7 Reporting checklist (epi-specific footer for `notes=`)

When producing the Table-2 footer, include — in addition to the AER stars/SE language:

- Cohort size, person-years of follow-up, event count
- **Adjustment set** (variables in the back-door set, not just "controls")
- **Positivity diagnostic** (PS truncation rule, % of cohort with extreme weights)
- **E-value** for the main effect and its CI bound
- For survival: **proportional-hazards check** (Schoenfeld residuals p-value) or "PH violated, RMST reported instead"
- STROBE checklist completion (cite as a supplementary file)

> **Output path stays identical**: every estimator above returns a `CausalResult` and slots straight into `sp.regtable(...) / sp.collect(...) / sp.paper_tables(...)`. Doubly-robust estimators (TMLE, HAL-TMLE, AIPW) are preferred over single-robust IPTW or g-formula alone — report all three for transparency, but treat TMLE as the primary.

---

## §B. ML causal inference pipeline (Mode B)

> **Convention**: estimand-first, doubly-robust, ML-nuisance-learned, with **CATE distribution + policy value** as first-class outputs (not just a single ATE). The skill mirrors the AER skeleton but the Step-4 estimator stack is **DML + meta-learners + causal forest + neural-causal + BCF**, and Step-5 always reports a CATE distribution. Uncertainty is quantified by **conformal prediction** (`sp.conformal_causal`), not just normal-approximation SE.

Running example: a marketing uplift study — `treatment = personalized_offer`, `outcome = revenue_30d`, with 80+ covariates including text features (`prior_browsing_text`).

### B.0 Prep + nuisance super-learner

```python
import statspai as sp

# 0.1 Train/holdout split — DML uses cross-fitting internally, but holdout is for policy eval.
# statspai doesn't expose its own splitter; use sklearn directly.
from sklearn.model_selection import train_test_split
train, holdout = train_test_split(df, test_size=0.2, stratify=df["treatment"], random_state=42)

# 0.2 Nuisance learners. IMPORTANT: `sp.dml` / `sp.metalearner` do NOT accept a
# `sp.super_learner(...)` object — pass a scikit-learn estimator OBJECT, or (for `dml`
# only) a string alias from {'gbm','rf','lasso','ridge','linear','xgb','lgbm'}.
from sklearn.linear_model import LogisticRegression, LassoCV
from sklearn.ensemble import (GradientBoostingRegressor, GradientBoostingClassifier,
                              RandomForestRegressor, RandomForestClassifier)
g_outcome = GradientBoostingRegressor()       # nuisance E[Y|X]  (a sklearn estimator)
g_treat   = GradientBoostingClassifier()      # nuisance E[D|X]  (propensity)

# `sp.super_learner` is a separate STANDALONE stacked predictor (it returns a fitted
# SuperLearner with .predict / .predict_proba) — use it for a reward model in OPE (B.4)
# or for your own predictions, NOT as the nuisance argument to dml/metalearner.
sl_reward = sp.super_learner(X=train[X_cols].values, y=train["revenue_30d"].values,
                             library=[LassoCV(), GradientBoostingRegressor(), RandomForestRegressor()],
                             n_folds=5, task="regression")
```

### B.1 Estimand & DAG learning (Step 2 + 2.5 in ML key)

```python
# estimand is an UPPERCASE enum: 'ATE'|'ATT'|'ATU'|'LATE'|'CATE'|'ITT'. The strategy
# is set via design=/estimand= on causal_question; q.identify() takes NO arguments.
q = sp.causal_question(treatment="treatment", outcome="revenue_30d", data=train,
                       population="marketed users", estimand="ATE",
                       design="selection_on_observables", covariates=X_cols)
plan = q.identify()

# DAG learning (when domain DAG isn't given)
proposed = sp.llm_dag_propose(variables=X_cols + ["treatment","revenue_30d"],
                              domain="e-commerce uplift")
constrained = sp.pc_algorithm(train[X_cols + ["treatment","revenue_30d"]],
                              variables=X_cols + ["treatment","revenue_30d"], alpha=0.05)
validated = sp.llm_dag_validate(proposed, train, alpha=0.05)   # (dag, data) positional
# Alternative learners: sp.notears(...), sp.causal_discovery(..., method="ges")
```

### B.2 Estimator stack — DML / meta-learner / GRF / neural / Bayesian

```python
# (1) DML — Chernozhukov double machine learning.
# Nuisance kwargs are `model_y` (outcome) and `model_d` (treatment) — NOT ml_g/ml_m.
# Each takes a sklearn estimator OR a string alias ('gbm'/'rf'/'lasso'/'xgb'/...).
dml = sp.dml(train, y="revenue_30d", d="treatment", X=X_cols,
             model="plr",                    # plr / irm / iv / pliv
             model_y=g_outcome, model_d=g_treat, n_folds=5)

# (2) Meta-learners — S / T / X / R / DR. outcome_model/propensity_model take sklearn
# estimator OBJECTS (not strings); omit them for sensible defaults.
ml_dr = sp.metalearner(train, y="revenue_30d", treat="treatment", covariates=X_cols,
                       learner="dr",         # 's' / 't' / 'x' / 'r' / 'dr'
                       outcome_model=GradientBoostingRegressor(),
                       propensity_model=GradientBoostingClassifier())

# (3) Causal forest (GRF / honest splits)
cf = sp.causal_forest("revenue_30d ~ treatment | " + " + ".join(X_cols),
                       train, n_estimators=2000, honest=True)

# (4) Neural causal — Dragonnet / TARNet / CEVAE. REQUIRES torch: pip install statspai[neural].
# Omit this block (and the neural columns below) if torch is not installed.
dn   = sp.dragonnet(train, y="revenue_30d", treat="treatment", covariates=X_cols,
                    repr_layers=(200,100), head_layers=(100,))
tar  = sp.tarnet  (train, y="revenue_30d", treat="treatment", covariates=X_cols)

# (5) Bayesian causal forest (full posterior over CATE)
bcf  = sp.bcf(train, y="revenue_30d", treat="treatment", covariates=X_cols,
              n_trees_mu=200, n_trees_tau=50)

# (6) Panel matrix completion (when units × periods)
mc   = sp.matrix_completion(panel_df, y="revenue", d="treatment", unit="user_id", time="week")

# Convergent evidence table — same regtable / collect stack. CausalResult AND CausalForest
# both flow into regtable; drop `dn` if you skipped the neural block.
rt = sp.regtable(dml, ml_dr, cf, dn, bcf,
                 model_labels=["(1) DML-PLR","(2) DR-Learner","(3) Causal forest",
                               "(4) Dragonnet","(5) BCF"],
                 stats=["N","ATE","CATE 5–95% range","Cross-fit folds","Nuisance R²"],
                 title="Table 2. ATE — ML estimator horse race")
rt.to_word ("tables/table2_ml.docx"); rt.to_excel("tables/table2_ml.xlsx")
```

### B.3 CATE distribution & subgroup view (the ML-causal headline)

```python
# 3.1 Per-row CATE. Plotters return (fig, ax). The raw per-row CATE vector lives at
# ml_dr.model_info["cate"] (an ndarray) — there is NO .cate_estimates attribute.
fig, ax = sp.cate_plot(ml_dr, kind="hist",
                       title="Figure B1. CATE distribution — DR-Learner")
fig.savefig("figures/figB1_cate_dist.png", dpi=300)

# 3.2 CATE by group (skill quartiles, gender, channel, …)
g = sp.cate_by_group(ml_dr, train, by="customer_value_quartile", n_groups=4)
fig, ax = sp.cate_group_plot(g, title="Figure B2. CATE by customer-value quartile")
fig.savefig("figures/figB2_cate_group.png", dpi=300)

# 3.3 Causal-forest local effects. CausalForest has no .local_effects(); get the per-row
# CATE vector with cf.effect(X) (ndarray) and plot it yourself.
import numpy as np, matplotlib.pyplot as plt
tau = cf.effect(train[X_cols].values)                # per-row CATE, length n
fig, ax = plt.subplots(figsize=(7, 4))
ax.hist(tau, bins=40); ax.set_xlabel("Causal-forest CATE"); ax.set_title("Figure B3. CF local effects")
fig.savefig("figures/figB3_local.png", dpi=300)
```

### B.4 Policy learning + off-policy evaluation

```python
import numpy as np

# 4.1 Learn an interpretable policy tree from CATE estimates. The result is dict-like
# with .plot_tree() (NOT .plot()), .summary(), .to_latex(), .to_excel(). plot_tree → (fig, ax).
pol_tree = sp.policy_tree(train, y="revenue_30d", d="treatment", X=X_cols, max_depth=3)
fig, ax = pol_tree.plot_tree()
fig.savefig("figures/figB4_policy.png", dpi=300)

# 4.2 Safe policy under a cost constraint. `state` and `action` must each be a SINGLE
# DISCRETE column name (not a list of feature columns). Encode the state into one
# discrete segment column first if you have many features.
train = train.assign(segment=train["customer_value_quartile"])      # one discrete state col
safe = sp.offline_safe_policy(train, state="segment", action="treatment",
                              reward="revenue_30d", cost="offer_cost", cost_threshold=2.50)

# 4.3 Off-policy evaluation on holdout — IPS / DR / SNIPS.
# sp.ope exposes ips / direct_method / doubly_robust / snips / switch_dr. CRITICAL shapes:
#   pi_b, pi_e are (n, K) probability matrices over K actions (one-hot for deterministic);
#   reward_model is a CALLABLE reward_model(X, a) -> length-n predicted reward.
from sklearn.ensemble import GradientBoostingClassifier, GradientBoostingRegressor
g_t = GradientBoostingClassifier().fit(train[X_cols], train["treatment"])
g_r = GradientBoostingRegressor().fit(
    np.column_stack([train[X_cols].values, train["treatment"].values]), train["revenue_30d"])

X_test = holdout[X_cols].values
A_test = holdout["treatment"].to_numpy(int)
R_test = holdout["revenue_30d"].to_numpy(float)
p1     = g_t.predict_proba(X_test)[:, 1]
pi_b   = np.column_stack([1 - p1, p1])                              # (n, 2) behavior policy
a_e    = (g_r.predict(np.column_stack([X_test, np.ones(len(X_test))]))    # treat-if-uplift>0
          > g_r.predict(np.column_stack([X_test, np.zeros(len(X_test))]))).astype(int)
pi_e   = np.column_stack([1 - a_e, a_e]).astype(float)             # (n, 2) one-hot eval policy
reward_model = lambda X, a: g_r.predict(np.column_stack([X, np.full(len(X), a)]))
opv = sp.ope.doubly_robust(X_test, A_test, R_test, pi_b=pi_b, pi_e=pi_e,
                           reward_model=reward_model)
print(f"Policy value (DR): {opv.value:.3f} ± {opv.se:.3f}")
# IPS/SNIPS need no reward model: sp.ope.snips(A_test, R_test, pi_b=pi_b, pi_e=pi_e)
```

### B.5 Uncertainty + fairness + robustness

```python
# 5.1 Conformal prediction intervals on CATE — distribution-free coverage.
# sp.conformal_causal exposes conformal_cate / conformal_ite / conformal_continuous /
# conformal_fair / conformal_interference and more — pick by estimand.
cp = sp.conformal_causal.conformal_cate(train, y="revenue_30d", treat="treatment",
                                         covariates=X_cols, alpha=0.10)   # 90% PI

# 5.2 Subgroup fairness audit — DP / EO gaps across protected attributes.
# fairness_audit audits a BINARY classifier: BOTH `predictions` and `labels` must be 0/1
# columns. (A meta-learner result has no .predict — score with your own classifier.)
holdout = holdout.assign(
    targeted  = (g_t.predict_proba(holdout[X_cols])[:, 1] > 0.5).astype(int),   # binary decision
    responded = (holdout["revenue_30d"] > holdout["revenue_30d"].median()).astype(int),  # binary label
)
fair = sp.fairness.fairness_audit(holdout, predictions="targeted",
                                  protected="gender", labels="responded",
                                  threshold=0.10)

# 5.3 Sensitivity dashboard — a TEXT/numeric dashboard (.summary() + numeric attrs),
# NOT a figure (no .plot()/.savefig()).
print(sp.sensitivity_dashboard(dml, train).summary())

# 5.4 (Reuse AER §7 robustness) Spec curve over nuisance/control choices.
# se_types ∈ {'nonrobust','hc1'/'robust','cluster'}; sc.plot() → (fig, ax).
sc = sp.spec_curve(train, y="revenue_30d", x="treatment",
                   controls=[X_cols[:1], X_cols[:3], X_cols],
                   se_types=["nonrobust", "robust"])
fig, ax = sc.plot()
fig.savefig("figures/figB6_spec_curve.png", dpi=300)
```

### B.6 Reporting checklist (ML-causal-specific footer)

When producing the Table-2 footer, include — in addition to the AER stars/SE language:

- **Nuisance learners** used (e.g., "outcome: SuperLearner[xgb, rf, lasso, nn]; treatment: same")
- **Cross-fitting**: number of folds, sample-splitting scheme
- **Overlap diagnostic**: PS distribution range, `% trimmed`
- **CATE summary**: mean / 5–95% range / share with CATE > 0
- **Policy value**: off-policy DR value vs. random / vs. always-treat baselines
- **Conformal coverage**: empirical coverage of nominal 1−α PI on holdout
- **Fairness audit**: subgroup CATE gaps vs. acceptable thresholds

> **Doubly-robust DML / DR-Learner / TMLE are preferred over single-robust S- or T-learner alone.** Report S- or T-learner only as a baseline in the horse race. Always check overlap before reporting any IPW-flavored estimator.

---

## Method Catalog

### Classical

**Choose by FE structure:**
- **No FE / single low-cardinality FE** → `sp.regress` (statsmodels OLS wrapper)
- **High-dim FE absorption (`y ~ x | fe1 + fe2`)** → `sp.feols` (pyfixest backend, AER workhorse)
- **Two-way panel (entity × time)** → `sp.panel(...)` (linearmodels backend, standard panel diagnostics)

```python
sp.regress("y ~ x1 + x2", df, cluster="firm_id")                       # OLS — `|` is NOT FE here
sp.feols  ("y ~ x1 + x2 | firm_id + year", df, vcov={"CRV1":"firm_id"})# OLS + 2-way FE absorbed
sp.feols  ("y ~ x1 + x2 | firm_id",        df, vcov={"CRV1":"firm_id+year"})  # 2-way cluster
sp.fepois ("count ~ x1 + x2 | firm_id",    df, vcov={"CRV1":"firm_id"})# Poisson + FE (count outcomes)
sp.feglm  ("y ~ x1 + x2 | firm_id", df, family="logit", vcov={"CRV1":"firm_id"})  # Logit + FE
sp.ivreg  ("y ~ (x1 ~ z1 + z2) + x2", df, cluster="state")             # IV/2SLS — (endog ~ instruments) + exog
sp.panel  (df, "y ~ x1 + x2", entity="firm", time="year", method="fe") # Panel FE (within / between / RE / FD)
sp.heckman(df, y="wage", x=["age", "edu"],
           select="in_labor_force", z=["marital", "kids"])              # Heckman selection
sp.qreg   (df, formula="y ~ x1 + x2", quantile=0.5)                     # Quantile regression
```

> **`sp.regress` does NOT parse `|` as a FE separator** — it forwards the formula to statsmodels which treats `edu | firm_id` as a single garbage variable name. Use `sp.feols` (or `sp.panel`) whenever your formula has `|`. Models from `sp.regress`, `sp.feols`, `sp.ivreg`, `sp.panel`, `sp.fepois`, `sp.feglm`, `sp.qreg`, `sp.heckman` all flow through `sp.regtable / sp.coefplot / sp.collect / sp.paper_tables` — mix freely in the same table.

### Difference-in-Differences
```python
sp.did(df, y="y", treat="treated", time="post")                              # 2×2 DID (time = 2 values)
sp.callaway_santanna(df, y="y", g="first_treat_year", t="year", i="firm_id") # CS 2021
sp.sun_abraham(df, y="y", g="first_treat_year", t="year", i="firm_id")       # SA 2021 event study
sp.bacon_decomposition(df, y="y", treat="treated", time="year", id="firm_id")# TWFE diagnostic
sp.continuous_did(df, y="y", dose="dose", time="year", id="firm_id")         # Continuous treatment
sp.honest_did(cs_result, method="smoothness")                                # PT sensitivity (RR 2023) — needs CS/SA result
sp.event_study(df, y="y", treat_time="first_treat_year",
               time="year", unit="firm_id", window=(-4, 4))                  # Event-study coefficients
```

### Regression Discontinuity
```python
sp.rdrobust(df, y="y", x="running_var", c=0)                      # Sharp RD (CCT 2014)
sp.rdrobust(df, y="y", x="running_var", c=0, fuzzy="treatment")   # Fuzzy RD
sp.rddensity(df, x="running_var", c=0)                            # McCrary density test
sp.rdmc(df, y="y", x="running_var", cutoffs=[0, 5, 10])           # Multi-cutoff RD
sp.rkd(df, y="y", x="running_var", c=0)                           # Regression kink
sp.rdplacebo(df, y="y", x="running_var", c=0,
             placebo_cutoffs=[-2, -1, 1, 2])                       # RD placebo
sp.rdbwsensitivity(df, y="y", x="running_var", c=0,
                    bw_grid=[0.5, 1.0, 1.5, 2.0])                  # Bandwidth sensitivity
```

### Matching & Reweighting
```python
sp.match(df, y="wage", treat="training", covariates=["age", "edu"], method="nearest")  # PSM (default)
sp.match(df, y="wage", treat="training", covariates=["age", "edu"], method="cem")      # Coarsened EM
sp.ebalance(df, y="wage", treat="training", covariates=["age", "edu"])                 # Entropy balancing
```

### Synthetic Control
```python
sp.synth(df, outcome="y", unit="unit", time="time",
         treated_unit=1, treatment_time=2000)              # ADH SCM (method='classic' default; 'augmented'/'sdid'/'mc' opt-in)
sp.sdid(df, outcome="y", unit="unit", time="time",
        treated_unit=1, treatment_time=2000)               # Synthetic DID (Arkhangelsky et al. 2021)
sp.synth_time_placebo(df, outcome="y", unit="unit", time="time",
                      treated_unit=1, treatment_time=2000,
                      n_placebo_times=10)                  # SCM in-time placebo
```

### ML Causal
```python
sp.dml(df, y="wage", treat="training", covariates=["age", "edu"], model="plr")       # DML
sp.causal_forest(formula="wage ~ training | age + edu", data=df)                      # Causal Forest (formula API)
sp.metalearner(df, y="wage", treat="training", covariates=["age", "edu"], learner="dr")  # DR-Learner
sp.tmle(df, y="wage", treat="training", covariates=["age", "edu"])                   # Targeted MLE
sp.aipw(df, y="wage", treat="training", covariates=["age", "edu"])                   # Augmented IPW
```

### Neural Causal
```python
# Requires torch: pip install "statspai[neural]"  (tarnet / cfrnet / dragonnet / cevae)
sp.tarnet(df,    y="wage", treat="training", covariates=["age", "edu"])
sp.cfrnet(df,    y="wage", treat="training", covariates=["age", "edu"])
sp.dragonnet(df, y="wage", treat="training", covariates=["age", "edu"])
```

### Text Causal (v1.6 P1, experimental)
```python
sp.causal_text.text_treatment_effect(
    df, text_col="doc", outcome="y", treatment="t",
    covariates=["age", "edu"], embedder="hash", n_components=20)      # Veitch–Wang–Blei 2020

sp.causal_text.llm_annotator_correct(
    annotations_llm=df["t_llm"],                                      # aligned pd.Series (all rows)
    annotations_human=df["t_true"],                                   # NaN where unlabelled
    outcome=df["y"], covariates=df[["age", "edu"]],
    method="hausman")                                                 # Egami et al. 2024
```

### Mechanisms / Decomposition
```python
sp.mediation(df, y="wage", d="training", m="hours_worked",
             X=["age", "edu"])                                      # ACME / ADE
sp.decompose(...)                                                    # Oaxaca-Blinder / RIF / FFL / KOB
```

### Robustness, Sensitivity & Inference
```python
sp.spec_curve(df, y="wage", x="training",
              controls=[["age"], ["age", "edu"], ["age", "edu", "tenure"]])
sp.robustness_report(df, formula="wage ~ training + age + edu",
                     x="training", cluster_var="firm_id")
sp.subgroup_analysis(df, formula="wage ~ training + age + edu",
                     x="training", by={"gender": "female", "age_bin": "age_quartile"})
sp.oster_bounds(df, y="wage", treat="training",
                controls=["age", "edu"], r_max=1.3)                  # Oster 2019
sp.unified_sensitivity(result, r2_treated=0.05, r2_controlled=0.10,
                       include_oster=True).summary()                  # text dashboard (.summary(); no figure)
sp.sensitivity_dashboard(result).summary()                           # Cinelli-Hazlett + Oster + E-value (text)
sp.evalue(estimate=..., ci=(..., ...), measure="RR")
sp.twoway_cluster(result, df, cluster1="firm_id", cluster2="year")    # two-way SE (statsmodels results)
sp.conley(result, df, lat="lat", lon="lon", dist_cutoff=100)          # spatial HAC

fig, ax = result.plot()                                              # plot() → (fig, ax)
sp.interactive(fig)                                                   # WYSIWYG editor, 29 academic themes
```

---

## Common Mistakes

| Anti-pattern | Correct form |
|---|---|
| Reporting Table 2 without writing the estimating equation | Step 2 — write the equation + identifying assumption to `artifacts/empirical_strategy.md` *before* estimating |
| Skipping the event-study figure and going straight to the DID coefficient | Step 3.1 — `sp.event_study(...)` + `sp.enhanced_event_study_plot(...)` precedes the regression table |
| Reporting IV without first-stage F | Step 3.2 — `iv.summary()` reports first-stage F; bench-mark F ≥ 10 (≥ 23 for AR-equivalent inference) |
| Reporting RD without McCrary + binscatter | Step 3.3 — `sp.rddensity` + `sp.binscatter` |
| Single-spec main result with no robustness panel | Step 7 — placebo, Oster, honest_did, alt-SE, spec_curve are *expected*, not optional |
| Cluster at observation level when treatment is at firm/state level | Cluster at the level of treatment assignment; use `sp.twoway_cluster` if multi-dim |
| Raw panel → staggered DID without balance check | Run Step 0 `data_contract`; inspect `sp.balance_panel` output and cohort sizes |
| `spec_curve(controls=["a","b","c"])` (flat list) | `controls=[["a"], ["a","b"], ["a","b","c"]]` — each inner list = one spec |
| `sp.rdrobust(..., cutoff=0)` | Kwarg is `c=0` across `rdrobust` / `rkd` / `rdplacebo` / `rdbwsensitivity` |
| `sp.evalue(result)` | `sp.evalue(estimate=<point>, ci=(lo, hi), measure="RR")` |
| `sp.match(df, treat="t", y="y", ...)` | Signature is `(df, y, treat, covariates, ...)` — **y before treat** |
| `sp.sun_abraham(df, y, g, t)` — no unit id | Staggered DID **requires** `i=<unit_id>` |
| `sp.synth(..., treated_period=2000)` | Kwarg is `treatment_time=` (singular) |
| `sp.panel(df, formula, fe=True)` | Kwarg is `method="fe"` |
| `sp.robustness_report(result, ...)` | Takes `(data, formula, x, ...)` — not a result object |
| `sp.mediation(df, y, treat, mediator)` | Kwargs are `(df, y, d, m, X)` — `d` for treatment, `m` for mediator |
| Pre-computed embeddings to `text_treatment_effect` | Pass `text_col=<column_name>`; control vectorisation via `embedder=` |
| `llm_annotator_correct(df)` | Takes aligned `pd.Series` (not DataFrame); NaN for unlabelled rows |
| `sp.callaway_santanna(..., covariates=[...])` | Kwarg is `x=[...]`, not `covariates=` |
| `sp.subgroup_analysis(..., cluster=...)` | Kwarg is `robust='hc1'` (or `'hc0'`/`'hc2'`/`'hc3'`); no cluster slot |
| `sp.oster_delta(..., treat=, controls=, r_max=)` | Real signature: `(data, y, x_base, x_controls, r_max)` |
| `sp.power_did(..., power_target=...)` | Wrappers don't auto-solve. Use dispatcher: `sp.power('did', ..., power_target=..., n_periods=, n_treated_periods=)` |
| `sp.power_cluster_rct(n_clusters=..., power_target=...)` | Use dispatcher: `sp.power('cluster_rct', cluster_size=, icc=, effect_size=, power_target=)` |
| `sp.cate_group_plot(forest, group=...)` | Takes a DataFrame: `g = sp.cate_by_group(ml, df, by=..., n_groups=4); sp.cate_group_plot(g)`. Forest result lacks per-row CATEs — use `sp.metalearner(..., learner='dr')` |
| `sp.cate_plot(causal_forest_result, ...)` | Needs a `metalearner` (or any X/DR/R-learner) result. Per-row CATEs live at `result.model_info["cate"]` (ndarray) — there is **no `.cate_estimates` attribute**. For a causal forest, use `cf.effect(X)` to get the CATE vector |
| `sp.bjs_pretrend_joint(es)` | Real signature: `(cs_or_sa_result, data, y=, group=, time=, first_treat=, controls=)` — NOT `event_study()` output |
| `sp.honest_did(ols_result, ...)` | Only accepts CS / SA / `did_multiplegt` / `aggte(..., 'dynamic')` results — pass a `callaway_santanna` object |
| `sp.sumstats(df, groups={...}, ...)` | No `groups=` kwarg; loop `sp.sumstats(vars=v_panel, ...)` per panel and concat |
| `sp.sumstats(..., by="treat")` always shows numeric "0" / "1" panel headers | Binary 0/1 `by=` auto-renders as **Control / Treated** (no kwarg needed). For non-binary or alternative wording, pass `by_labels={0:"Untrained", 1:"Trained"}` |
| Fixing `fmt="%.0f"` (or any fixed format) on a regtable that mixes dollar-magnitude (~$1500) and elasticity-magnitude (~0.09) coefficients | Silently rounds the elasticities to `0` while stars survive — the LaLonde precision trap. Use `fmt="auto"` for magnitude-adaptive precision: thousands separator for ≥1000, integer for ≥100, 1 dp for ≥10, 2 dp for ≥1, 3 dp below |
| `plan.population` / `plan.equation` / `plan.threats` | Not exposed on `IdentificationPlan`. Available: `assumptions / estimand / estimator / fallback_estimators / identification_story / warnings / summary()`. Use `q.population / q.treatment / q.outcome` from the `CausalQuestion` |
| `sp.regtable(..., output="docx")` / `output="xlsx"` | Enum is `{"text","latex","tex","html","markdown","md","qmd","quarto","word","excel"}`. Either use `output="word"`/`"excel"` or — preferred — drop `output=` and call `.to_word(filename)` / `.to_excel(filename)` on the result |
| `sp.sumstats(..., output="docx")` returns plain text | `sumstats` doesn't natively emit binary docx/xlsx. For Word/Excel use `sp.collect().add_summary(...).save("file.docx")` or convert via `sp.mean_comparison(...).to_word(...)` |
| Hand-rolling Word from `pandas.DataFrame.to_string()` / writing LaTeX manually | `RegtableResult.to_word/.to_excel/.to_latex/.to_markdown/.to_html` already apply book-tab borders, AER stars, and the right SE label. `sp.collect()` bundles many such tables into one file |
| Forgetting `template="aer"` (or `qje`/`econometrica`/`restat`/`jf`/`jpe`/`restud`/`aeja`) on `regtable` | Without `template=`, you lose the journal-correct SE label, star levels, and notes. List presets via `sp.list_journal_templates()` |
| Saving each regression to its own `.tex` and stitching by hand in LaTeX | Use `sp.paper_tables(main=, heterogeneity=, robustness=, placebo=)` for a single multi-panel `.docx` / `.xlsx`, or `sp.collect()` for a full Word/Excel/Markdown bundle (Step 8.4) |
| `sp.regtable(..., keep=[focal_var])` (or `drop=["Intercept"]`) as the *default* for every table | AER convention is to **show every estimated parameter verbatim — controls AND the intercept** so the reader can verify the full spec. `regtable()` does this when you pass NEITHER `keep=` NOR `drop=`. Reserve `drop=["Intercept"]` for when you actively want to suppress the constant; reserve `keep=[focal]` for intentionally focal-only tables (IV first-stage triplet, interaction-form heterogeneity) — each with a comment explaining why |
| `sp.regress("y ~ x \| firm_id", df, cluster="firm_id")` for FE | **Silently produces wrong numbers** — `sp.regress` is a thin statsmodels OLS wrapper that does NOT parse `\|` as a FE separator; it interprets `x \| firm_id` as a single garbage variable name. Use `sp.feols("y ~ x \| firm_id", df, vcov={"CRV1":"firm_id"})` for any formula containing `\|`. Two-way cluster: `vcov={"CRV1":"firm_id+year"}` |
| `sp.feols(..., cluster="firm_id")` | feols uses pyfixest convention: `vcov={"CRV1":"firm_id"}` (one-way) or `vcov={"CRV1":"firm_id+year"}` (two-way). The `cluster=` kwarg is for `sp.regress` / `sp.ivreg` (statsmodels) only |
| `sp.twoway_cluster(feols_result, ...)` or `sp.conley(feols_result, ...)` | Both consume **statsmodels-backed** results only (`sp.regress`/`sp.ivreg`); a pyfixest `feols` result raises (`KeyError`). For feols two-way cluster pass `vcov={"CRV1":"firm_id+year"}` directly; for Conley SE on an FE spec, re-fit that spec via `sp.regress(...)` and pass that |
| Trusting SEs without checking convergence / weak-IV / overlap | Always read `result.summary()` warnings and `result.diagnostics` |
| `sp.<plot>(...).savefig(path)` (chaining `.savefig` on a plot call) | Plotters return a `(fig, ax)` tuple — unpack: `fig, ax = sp.coefplot(...); fig.savefig(path, dpi=300)`. `sp.binscatter` → `(fig, ax, df)`; `sp.kaplan_meier(...).plot()` → bare `Axes` (use `ax.figure.savefig`) |
| `sp.enhanced_event_study_plot(sp.event_study(...))` for the event-study figure | `enhanced_event_study_plot` needs a **CS/SA** result (`KeyError: 'att'` otherwise). Build the figure from `cs = sp.callaway_santanna(...)`: `fig, ax = cs.plot()` (or `sp.ggdid(cs)` / `sp.group_time_plot(cs)`). Keep `sp.event_study(...)` for the numerical pre-trends test only |
| `sp.did_summary_plot(callaway_santanna_result)` | `did_summary_plot` only accepts a `sp.did_summary()` result. For a CS/SA dynamic-effects figure use `cs.plot()` / `sp.ggdid(cs)` / `sp.group_time_plot(cs)` |
| `sp.spec_curve(..., y_transforms=["log","ihs"])` (list) | `y_transforms` is a **dict** `{name: callable}`, e.g. `{"log": np.log, "ihs": np.arcsinh}`. `se_types` accepts only `'nonrobust'`/`'hc1'`(=`'robust'`)/`'cluster'` |
| `sp.unified_sensitivity(...).results` / `sp.sensitivity_dashboard(r).plot()`/`.savefig()` | Both return a **text** `SensitivityDashboard` — use `.summary()` and numeric attrs (`.e_value_point`, `.oster`, …); no `.results`/`.plot()`/`.savefig()`. The sensitivity **figure** (`sp.sensitivity_plot`) consumes `sp.honest_did(cs, ...)` output |
| `sp.gformula(df, ...)` / `sp.bounds(df, ...)` | Both are **modules**, not functions. Point-treatment g-formula → `sp.g_computation(df, y=, treat=, covariates=)` (time-varying → `sp.gformula.gformula_mc(...)`). Bounds → `sp.bounds.manski_bounds(...)` / `sp.bounds.lee_bounds(...)` |
| `sp.target_trial_emulate(df, protocol=, id=, time=, treat=, event=)` | Real signature: `(protocol, data, outcome_col, treatment_col, time_zero_filter=None, weights=None)`. `eligibility` is applied as `data.query(...)` unless you pass a `time_zero_filter` callable |
| `TargetTrialProtocol(assignment="...free text...", causal_contrast="...free text...")` | `assignment ∈ {"randomization","observational emulation"}`, `causal_contrast ∈ {"ITT","per-protocol","as-treated","observational-analogue"}` — free text raises `ValueError`. Put prose in `notes=` |
| `sp.dag(["a","b",...])` / `dag.add_edges([...])` / `dag.adjustment_set(...)` | `sp.dag("a -> b; c -> b")` parses an edge **string**; add edges with chained `.add_edge(parent, child)` (singular); back-door sets via `.adjustment_sets(exposure, outcome)` (**plural**, positional) → list of sets |
| `sp.aft("Surv(time, event) ~ x", ...)` | AFT formula LHS is `"duration + event"`: `sp.aft("followup_days + mace ~ x", df, family="weibull")` |
| `sp.hal_tmle(..., variant="ate")` | Only `variant="delta"` is implemented (`"projection"` is NotImplemented) |
| `sp.principal_strat(..., strata=<3-level>, instrument=<continuous>)` | Both `strata` and `instrument` must be **binary 0/1** columns |
| `sp.evalue(estimate=result.point_estimate, ...)` | `CausalResult` exposes `.estimate` and `.ci` (no `.point_estimate`). Econometric results use `.params[name]` / `.conf_int().loc[name]` |
| `sp.dml(..., ml_g=, ml_m=)` or passing a `SuperLearner` as nuisance | dml nuisance kwargs are `model_y=` / `model_d=`, each a sklearn estimator OR alias `'gbm'/'rf'/'lasso'/'xgb'/...`. `metalearner` `outcome_model=`/`propensity_model=` need sklearn **objects** (no string aliases). `sp.super_learner(...)` output is a standalone predictor, not a nuisance arg |
| `sp.causal_question(..., estimand="ate")` / `q.identify(strategy=, X=)` | `estimand` is UPPERCASE (`'ATE'/'ATT'/'LATE'/...`); set strategy via `design=`/`covariates=` on `causal_question`; `q.identify()` takes **no** arguments |
| `sp.offline_safe_policy(state=X_cols, ...)` | `state` and `action` must each be a **single discrete column name** — encode multi-feature state into one segment column first |
| `sp.ope.doubly_robust(X, A, R, pi_b=<1-D>, pi_e=<1-D>, reward_model=<model>)` | `pi_b`/`pi_e` must be `(n, K)` probability matrices (one-hot for deterministic policies); `reward_model` is a **callable** `reward_model(X, a) -> length-n vector`. `ips`/`snips` need no reward model |
| `sp.fairness.fairness_audit(..., predictions=<continuous>, labels=<continuous>)` | Both `predictions` and `labels` must be **binary 0/1**; it audits a binary classifier. A meta-learner result has no `.predict` |
| `pol_tree.plot()` / `cf.local_effects()` | `PolicyTreeResult` uses `.plot_tree()` (→ `(fig, ax)`); `CausalForest` has no `.local_effects()` — get per-row CATEs via `cf.effect(X)` |
| `sp.feols(...)` without installing pyfixest | `sp.feols`/`fepois`/`feglm` need `pip install "statspai[fixest]"`; neural causal needs `[neural]` (torch); plots need `[plotting]` |
| `sp.ivreg("y ~ (d ~ z) + x \| industry + year", ...)` for FE-IV | **Silently drops the `\| fe`** (identical β̂ with/without it; FE never appear in output). `sp.ivreg` does not absorb `\|` FE or parse `C(fe)`. Keep all IV-triplet columns on the same low-dim controls, or pre-build dummy columns in pandas |
| `sp.regtable(ivw, egger, median, ...)` for MR results | `mr_ivw`/`mr_egger`/`mr_median` return **dicts** (`estimate/se/ci_lower/ci_upper/p_value/...`), not result objects. Build a `pd.DataFrame({...}).T` and `.to_excel()`/`.to_latex()` it |
| `sp.regtable(aft, ...)` for a survival AFT | `AFTResult` has no `.params`/`.to_word` — it exposes `.summary()` plus `.beta`/`.se`/`.var_names`/`.n`/`.n_events`/`.aic`. Build a `pd.DataFrame({"coef": aft.beta, "se": aft.se}, index=aft.var_names)`. For a causal survival estimand use `sp.ltmle_survival(...)` |
| `sp.causal(..., dag=discovered.dag)` | `LLMConstrainedDAGResult` has no `.dag` — use `discovered.to_dag()` (or inspect `.final_edges`) |
| `result.conf_int()` / `result.data_info["n_obs"]` on a `CausalResult` | `CausalResult` exposes `.estimate` / `.ci` (tuple) / `.n_obs` / `.estimand` (no `.conf_int()`; `data_info` key is `"nobs"`). `.params[name]` + `.conf_int().loc[name]` are for econometric (OLS/feols/ivreg) results |

---

## Agent Integration Pattern

```python
import statspai as sp

sp.list_functions()                                        # discover
info   = sp.describe_function("callaway_santanna")         # understand
schema = sp.function_schema("callaway_santanna")           # structured call spec

result = sp.callaway_santanna(df, y="y",
                               g="first_treat_year", t="year", i="firm_id")
print(result.summary())
result.to_latex("tables/did_results.tex")
```

---

## When to Use StatsPAI vs Alternatives

| Scenario | Use StatsPAI | Alternative |
|---|---|---|
| One-stop EDA → estimand → DAG → estimate → robustness pipeline | ✅ single import covers all eight AER sections | assemble pyfixest + econml + causalml + differences + ... |
| Agent-driven analysis with self-describing API | ✅ `list_functions` / `describe_function` / `function_schema` | statsmodels / pyfixest (no agent API) |
| Estimand-first "DID vs RD vs IV?" decision | ✅ `sp.causal_question` + `sp.causal` | manual judgement call |
| Stata → Python migration (same API names) | ✅ `sp.regress`, `sp.estat`, `sp.sumstats`, `sp.feols`, `sp.panel` (Stata `xtreg` → `sp.feols("y ~ x | id + year", df)` or `sp.panel(..., method="fe"/"re")`) | linearmodels (partial) |
| Full AER-style robustness gauntlet from one package | ✅ Oster / honest_did / E-value / Conley / 2-way / spec_curve / placebo all in `sp.*` | manually wire 5+ packages |
| **Epidemiology / public health** (target-trial emulation, IPTW + g-formula + TMLE triplet, MR, KM/AFT survival, E-value, STROBE/TRIPOD reporting) | ✅ `sp.target_trial.TargetTrialProtocol` + `sp.target_trial_emulate` + `sp.gformula` + `sp.msm` + `sp.tmle` + `sp.hal_tmle` + `sp.mendelian` (`sp.mr_ivw`/`sp.mr_egger`/`sp.mr_median`) + `sp.kaplan_meier` + `sp.aft` + `sp.evalue` + `sp.principal_strat` — see §A. | hand-stitched zEpid + lifelines + statsmodels + manual MR scripts |
| **ML causal inference** (DML / S/T/X/R/DR-Learner / causal forest / Dragonnet / TARNet / CEVAE / BCF / matrix completion / policy learning / OPE / conformal CATE / fairness audit / DAG learning) | ✅ `sp.dml` + `sp.metalearner` + `sp.causal_forest` + `sp.dragonnet`/`tarnet`/`cevae` + `sp.bcf` + `sp.matrix_completion` + `sp.policy_tree` + `sp.offline_safe_policy` + `sp.ope.*` + `sp.conformal_causal.*` + `sp.fairness.fairness_audit` + `sp.causal_discovery`/`pc_algorithm`/`notears`/`llm_dag_propose`+`llm_dag_validate` — see §B. | EconML + DoWhy + CausalML + GRF + zEpid + dowhy-gcm assembled by hand |

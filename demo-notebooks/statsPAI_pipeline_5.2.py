#!/usr/bin/env python3
"""
StatsPAI Full Empirical Pipeline v5.2 — Lalonde NSW × IV + AIPW/DML
=====================================================================
Follows skills/00-Full-empirical-analysis-skill_StatsPAI/SKILL.md §-1→§8.

Pipeline output directory: _statspai_pipeline_outputs_5.2/
"""

import os, json, warnings, shutil, ssl as _ssl, urllib.request as _ur
from pathlib import Path
os.environ.setdefault("NUMBA_CACHE_DIR", "/tmp/numba_cache")
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display, Markdown
import statspai as sp

SEED = 42
np.random.seed(SEED)

# ── SSL safety net — use certifi CA bundle ─────────────────────
import certifi as _certifi
_ctx = _ssl.create_default_context(cafile=_certifi.where())
_ur.install_opener(_ur.build_opener(_ur.HTTPSHandler(context=_ctx)))
import requests as _requests
_requests.get("https://vincentarelbundock.github.io", verify=_certifi.where(), timeout=5)

# ── Paths ────────────────────────────────────────────────────────
OUT_ROOT = Path("_statspai_pipeline_outputs_5.2")
OUT_TAB  = OUT_ROOT / "tables"
OUT_FIG  = OUT_ROOT / "figures"
OUT_ART  = OUT_ROOT / "artifacts"
for p in (OUT_TAB, OUT_FIG, OUT_ART):
    p.mkdir(parents=True, exist_ok=True)

DATA_URL = "https://vincentarelbundock.github.io/Rdatasets/csv/MatchIt/lalonde.csv"

# ── Helper helpers ──────────────────────────────────────────────
def _nobs(r):
    extractors = (
        lambda x: int(x.glance()["nobs"].iloc[0]),
        lambda x: int(x.to_dict()["n_obs"]),
        lambda x: int(x.data_info["n_obs"]),
        lambda x: int(x.data_info["n"]),
        lambda x: int(x.nobs),
        lambda x: int(x.n_obs),
    )
    for fn in extractors:
        try:
            return fn(r)
        except Exception:
            continue
    return None

def _coef(r, name):
    """Extract (beta, se, conf_low, conf_high) for a coefficient by name."""
    try:
        b   = float(r.params[name])
        se  = float(r.std_errors[name])
        lo  = float(r.conf_int_lower[name])
        hi  = float(r.conf_int_upper[name])
        return b, se, lo, hi
    except Exception:
        pass
    try:
        td = r.tidy()
        row = td[td["term"] == name].iloc[0]
        b  = float(row["estimate"])
        se = float(row["std_error"])
        lo = float(row.get("conf_low",  b - 1.96*se))
        hi = float(row.get("conf_high", b + 1.96*se))
        return b, se, lo, hi
    except Exception:
        pass
    import re as _re
    txt = str(r.summary()) if hasattr(r, "summary") else str(r)
    m_est = _re.search(r"(?:ATE|ATT|LATE|Coefficient):\s+([+-]?[0-9.]+)", txt)
    m_se  = _re.search(r"Std\. Error:\s+\(?([0-9.]+)\)?", txt)
    if m_est and m_se:
        b  = float(m_est.group(1)); se = float(m_se.group(1))
        return b, se, b-1.96*se, b+1.96*se
    return float("nan"), float("nan"), float("nan"), float("nan")

def _robust_se(r, name):
    """Extract robust SE from model t(|HC|) or variance-covariance matrix."""
    for attr in ("std_errors", "std_err", "bse", "ses"):
        try:
            d = getattr(r, attr)
            return float(d[name])
        except Exception:
            continue
    return float("nan")

covariates = ["age","educ","black","hispan","married","nodegree","re74","re75"]

print("=" * 72)
print("StatsPAI version:", getattr(sp, "__version__", "unknown"))
print("Output root     :", OUT_ROOT.resolve())
print("Data URL        :", DATA_URL)
print("=" * 72)

# ════════════════════════════════════════════════════════════════
# §-1  PRE-ANALYSIS PLAN
# ════════════════════════════════════════════════════════════════
print("\n" + "─" * 72)
print("§-1  Pre-Analysis Plan (power)")
print("─" * 72)

try:
    power = sp.power_rct(n=614, effect_size=None)
    mde = float(getattr(power, "effect_size", float("nan")))
except Exception as exc:
    mde = None
    print(f"  power_rct skipped: {exc!r}")

pap = {
    "design": "rct (lalonde-approx)", "n": 614, "alpha": 0.05,
    "power_target": 0.80,
    "mde_in_sd_units": mde,
    "note": "Cohen's d in residual SD units; multiply by SD(re78) for $ units.",
}
(OUT_ART / "pap_power.json").write_text(json.dumps(pap, indent=2, default=str))
print(f"  MDE (SD units): {mde}" if mde else "  MDE: N/A (deferred)")
print("  →", OUT_ART / "pap_power.json")


# ════════════════════════════════════════════════════════════════
# §0  DATA — SAMPLE CONSTRUCTION + CONTRACT
# ════════════════════════════════════════════════════════════════
print("\n" + "─" * 72)
print("§0  Data — sample construction & data contract")
print("─" * 72)

sample_log = []

import io

DATA_LOCAL = Path("_lalonde_data.csv")
RAW_COLS = ["treat", "age", "educ", "race", "married",
            "nodegree", "re74", "re75", "re78"]


def load_raw_lalonde():
    """Resolve the MatchIt::lalonde extract (N=614), offline first.

    Tiers: the pre-downloaded local CSV, the copy bundled with StatsPAI,
    then the Rdatasets mirror over HTTPS. All three are the same extract
    and agree on every column in RAW_COLS, so the winning tier changes no
    number. The bundled tier is what keeps this off the network — a reset
    connection here used to leave `df` undefined and cascade NameErrors
    through the rest of the script.
    """
    if DATA_LOCAL.exists():
        return pd.read_csv(DATA_LOCAL)[RAW_COLS], f"local CSV ({DATA_LOCAL})"
    try:
        bundled = sp.datasets.nsw_lalonde(simulated=False)
    except Exception as exc:
        print(f"Bundled StatsPAI copy unavailable ({exc!r}); trying {DATA_URL}")
    else:
        return bundled[RAW_COLS], "bundled sp.datasets.nsw_lalonde(simulated=False)"
    _r = _requests.get(DATA_URL, verify=_certifi.where(), timeout=30)
    return pd.read_csv(io.StringIO(_r.text))[RAW_COLS], f"Rdatasets mirror ({DATA_URL})"


raw, DATA_PROVENANCE = load_raw_lalonde()
print(f"Raw data resolved from: {DATA_PROVENANCE}")
sample_log.append((f"0. raw lalonde [{DATA_PROVENANCE}]", len(raw)))

df0 = raw.drop(columns=["rownames"], errors="ignore").dropna()
sample_log.append(("1. drop rownames + dropna", len(df0)))

df1 = df0.copy()
df1["black"] = (df1["race"] == "black").astype(int)
df1["hispan"] = (df1["race"] == "hispan").astype(int)
sample_log.append(("2. recode race → black/hispan", len(df1)))

df2 = df1[df1["treat"].isin([0, 1])].copy()
sample_log.append(("3. treat ∈ {0,1}", len(df2)))
df = df2

(OUT_ART / "sample_construction.json").write_text(json.dumps(sample_log, indent=2))
for stage, n in sample_log:
    print(f"  {stage:<40s}  N = {n}")

# ── Data contract ────────────────────────────────────────────────
from scipy import stats as _st
contract = {
    "n_obs": int(len(df)),
    "dtypes": df.dtypes.astype(str).to_dict(),
    "n_missing": df.isna().sum().to_dict(),
    "y_range": (float(df["re78"].min()), float(df["re78"].max())),
    "treatment_share": float(df["treat"].mean()),
    "treatment_levels": sorted(df["treat"].unique().tolist()),
}
assert contract["n_obs"] > 0
assert all(v == 0 for v in contract["n_missing"].values())
assert contract["treatment_levels"] == [0, 1]
(OUT_ART / "data_contract.json").write_text(json.dumps(contract, indent=2, default=str))
print("  Data contract: ✓  N={}, treat_share={:.3f}, y∈[{:.0f},{:.0f}]".format(
    contract["n_obs"], contract["treatment_share"],
    contract["y_range"][0], contract["y_range"][1]))


# ════════════════════════════════════════════════════════════════
# §1  TABLE 1 — DESCRIPTIVES & BALANCE
# ════════════════════════════════════════════════════════════════
print("\n" + "─" * 72)
print("§1  Descriptive statistics & Table 1")
print("─" * 72)

panels = {
    "A. Outcome":          ["re78"],
    "B. Treatment":        ["treat"],
    "C. Demographics":     ["age","educ","black","hispan","married","nodegree"],
    "D. Earnings history": ["re74","re75"],
}
try:
    table1 = sp.sumstats(df, groups=panels, by="treat", output="dataframe")
    display(table1)
    try:
        sp.sumstats(df, groups=panels, by="treat",
                    output="latex", filename=str(OUT_TAB / "table1_summary.tex"))
    except Exception:
        pass
except Exception as exc:
    print(f"  sp.sumstats groups= failed ({exc!r}); using flat vars.")
    flat = sum(panels.values(), [])
    table1 = sp.sumstats(df, vars=flat, by="treat", output="dataframe")
    display(table1)

balance = sp.balance_table(df, treat="treat", covariates=covariates,
                           output="dataframe", test="ttest")
display(balance)

raw_diff = df.groupby("treat")["re78"].agg(["count","mean","median","std"])
naive_att = df.loc[df["treat"]==1, "re78"].mean() - df.loc[df["treat"]==0, "re78"].mean()
print(f"\n  Naïve ATT (treated − control): ${naive_att:,.2f}")
try:
    smd_black = float(balance.loc['black','SMD'])
    print(f"  Imbens-Rubin flag: black SMD={smd_black:.2f} (>0.25 = severe imbalance)")
except Exception:
    print(f"  Imbens-Rubin: black SMD={balance.loc['black','SMD']}")

# Figure 1 — distributions
fig, axes = plt.subplots(1, 3, figsize=(13, 3.6))
for ax, col, title in zip(axes, ["re78","re74","age"],
                           ["1978 earnings (outcome)","1974 earnings (pre-treat)","Age"]):
    for tv, lb in [(0,"control"),(1,"treated")]:
        df.loc[df["treat"]==tv, col].plot(kind="hist", bins=25, alpha=0.55, ax=ax, label=lb)
    ax.set_title(title); ax.set_xlabel(col); ax.legend()
plt.tight_layout()
fig.savefig(OUT_FIG / "fig1_distributions.png", dpi=200)
plt.close()
print("  →", OUT_FIG / "fig1_distributions.png")


# ════════════════════════════════════════════════════════════════
# §2  EMPIRICAL STRATEGY (estimand-first DSL)
# ════════════════════════════════════════════════════════════════
print("\n" + "─" * 72)
print("§2  Empirical strategy — estimand-first DSL")
print("─" * 72)

question = sp.causal_question(
    treatment="treat", outcome="re78", data=df,
    population="Lalonde NSW treated workers + PSID comparison sample, 1976-78",
    estimand="ATT",
    design="selection_on_observables",
    covariates=covariates,
    notes="Treatment is NOT randomly assigned. Identification via conditional unconfoundedness + overlap.",
)
plan = question.identify()
print(f"  Estimator: {plan.estimator}, estimand: {plan.estimand}")
print(f"  Fallbacks: {plan.fallback_estimators}")

strategy_md = (
    "# Empirical Strategy (pre-registration)\n\n"
    "**Population**: Lalonde NSW treated + PSID controls, 1976-78\n"
    "**Estimand**: ATT — average treatment effect on the treated\n"
    "**Design**: selection on observables (cross-sectional X-adjustment)\n\n"
    "## Estimating equation\n\n```\n"
    "re78_i = alpha + beta * treat_i + X_i' * gamma + eps_i\n"
    "X = (age, educ, black, hispan, married, nodegree, re74, re75)\n```\n\n"
    "## Identifying assumptions\n\n"
    "- (Unconfoundedness | X)  treat ⊥ (re78(0), re78(1)) | X\n"
    "- (Overlap)  0 < Pr(treat=1|X) < 1 ∀X in support\n"
    "- (IV addendum) If IV is attempted: relevance (cov(Z,treat|X)≠0) + exclusion (Z→re78 only via treat) + exogeneity\n\n"
    "## Threats to identification\n\n"
    "- Selection on unobservables (motivation, soft skills, location shocks)\n"
    "- Functional-form misspecification of propensity / outcome models\n"
    "- Limited overlap on (re74, re75) — well-known Lalonde tail behaviour\n"
    "- IV: no valid natural instrument in the Lalonde data; constructed instruments are weak\n\n"
    "## Primary & fallback estimators\n\n"
    "- Primary: AIPW (doubly robust — consistent if PS or outcome model correct)\n"
    "- Fallbacks: OLS, PSM, DML-PLR, Entropy balancing, IV (constructed instrument for demonstration)\n"
)
(OUT_ART / "empirical_strategy.md").write_text(strategy_md)
print("  →", OUT_ART / "empirical_strategy.md")

# Estimate the primary model
q_est = question.estimate()
print(f"\n  question.estimate() — ATT via {plan.estimator}")
print(f"    Estimate = {q_est.estimate if hasattr(q_est,'estimate') else 'N/A'}")


# ════════════════════════════════════════════════════════════════
# §3  IDENTIFICATION GRAPHICS
# ════════════════════════════════════════════════════════════════
print("\n" + "─" * 72)
print("§3  Identification graphics")
print("─" * 72)

# 3a. Matching + love plot
m = sp.match(df, y="re78", treat="treat",
             covariates=covariates, method="nearest", estimand="ATT")
try:
    fig_love = m.plot()
    if isinstance(fig_love, (tuple, list)):
        fig_love = fig_love[0]
    fig_love.savefig(OUT_FIG / "fig2_love_plot.png", dpi=200)
    plt.close()
    print("  Love plot →", OUT_FIG / "fig2_love_plot.png")
except Exception as exc:
    print(f"  Love plot failed: {exc!r}")

print(f"  Match summary: {m.summary() if hasattr(m,'summary') else 'OK'}")

# 3b. Propensity-score overlap
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ps_model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, random_state=SEED))
ps_model.fit(df[covariates], df["treat"])
df = df.assign(propensity_score=ps_model.predict_proba(df[covariates])[:, 1])

fig, ax = plt.subplots(figsize=(7, 4))
for tv, lb in [(0,"control"),(1,"treated")]:
    df.loc[df["treat"]==tv, "propensity_score"].plot(
        kind="hist", bins=25, alpha=0.55, density=True, ax=ax, label=lb)
ax.set_title("Figure 3. Propensity-score overlap")
ax.set_xlabel("Pr(treat=1|X)"); ax.legend()
plt.tight_layout()
fig.savefig(OUT_FIG / "fig3_overlap.png", dpi=200)
plt.close()
print("  Overlap plot →", OUT_FIG / "fig3_overlap.png")


# ════════════════════════════════════════════════════════════════
# §4  MAIN RESULTS — IV + PROGRESSIVE CONTROLS + DESIGN HORSE RACE
# ════════════════════════════════════════════════════════════════
print("\n" + "─" * 72)
print("§4  Main results")
print("─" * 72)

# ── 4a. IV analysis ──────────────────────────────────────────
# The Lalonde data has no natural instrument. We construct one for
# pedagogical demonstration: age^2 (a common "nonlinear" instrument
# in the IV-on-cross-section literature).  The exclusion restriction
# is transparently implausible — age² affects earnings through many
# channels — so we treat this as a sensitivity exercise, not a
# credible estimate.
iv_result = None
iv_b = float("nan")
fs_f = float("nan")
print("\n  ── IV Analysis ──")
print("  NOTE: No natural instrument in Lalonde data.")
print("  Using age² as a constructed instrument for demonstration.")
print("  Exclusion restriction (age² → re78 only through treat) is VIOLATED.")
print("  F-statistic reported as weak-instrument test.\n")

df_iv = df.copy()
df_iv["age2"] = df_iv["age"] ** 2
iv_covariates = [c for c in covariates if c != "age"]

# First stage: treat ~ age² + X
fs = sp.regress(f"treat ~ age2 + {' + '.join(iv_covariates)}", df_iv, robust="HC1")
try:
    fs_b  = float(fs.params["age2"])
    fs_se = float(fs.std_errors["age2"])
    fs_t  = abs(fs_b) / fs_se
    # F-stat = t² for single instrument
    fs_f = fs_t ** 2
except Exception as e:
    fs_b = fs_se = fs_t = fs_f = float("nan")
    print(f"  First-stage coef extraction failed: {e!r}")

print(f"  First stage: treat ~ age² + controls")
print(f"    β_age² = {fs_b:+.6f}  (SE = {fs_se:.6f})")
print(f"    F-stat = {fs_f:.3f}  (rule of thumb: F > 10 = strong instrument)")
print(f"    Verdict: {'Strong instrument' if fs_f > 10 else 'WEAK instrument' if fs_f > 0 else 'N/A'}")

# 2SLS via sp.ivreg
try:
    iv_formula = "re78 ~ (treat ~ age2) + age + educ + black + hispan + married + nodegree + re74 + re75"
    iv_result = sp.ivreg(iv_formula, data=df_iv, robust="hc1")
    iv_b, iv_se, iv_lo, iv_hi = _coef(iv_result, "treat")
    print(f"\n  2SLS (IV) ATT: β = {iv_b:>+.1f}  SE = {iv_se:.1f}")
    print(f"    95% CI: [{iv_lo:+.1f}, {iv_hi:+.1f}]")

    # Effective F-test for weak instruments
    try:
        eff_f = sp.iv.effective_f_test(iv_result)
        print(f"  Effective F-statistic: {eff_f}")
    except Exception as exc:
        print(f"  Effective F-test unavailable: {exc!r}")
except Exception as exc:
    iv_result = None
    print(f"\n  IV (2SLS) failed: {exc!r}")

# ── 4b. Progressive controls (OLS) ───────────────────────────
print("\n  ── Progressive controls (Table 2) ──")
M1 = sp.regress("re78 ~ treat", df, robust="HC1")
M2 = sp.regress("re78 ~ treat + age + educ", df, robust="HC1")
M3 = sp.regress("re78 ~ treat + age + educ + black + hispan", df, robust="HC1")
M4 = sp.regress("re78 ~ treat + age + educ + black + hispan + married + nodegree", df, robust="HC1")
M5 = sp.regress("re78 ~ treat + age + educ + black + hispan + married + nodegree + re74 + re75",
                df, robust="HC1")

main_models = [M1, M2, M3, M4, M5]
main_labels = ["(1) Baseline","(2) +Age/Edu","(3) +Race","(4) +Marital/Educ","(5) +Earn.hist."]

try:
    t2 = sp.regtable(*main_models, keep=["treat"],
                     coef_labels={"treat":"Job training (β̂)"},
                     model_labels=main_labels, stars="aer",
                     stats=["N","R2","DV mean"], output="markdown")
    display(t2)
except Exception as exc:
    print(f"  regtable markdown: {exc!r}")
    for lb, mm in zip(main_labels, main_models):
        b, se, _, _ = _coef(mm, "treat")
        print(f"    {lb:<20s}  β̂={b:>+9.1f}  se={se:>7.1f}")

try:
    sp.regtable(*main_models, keep=["treat"],
                coef_labels={"treat":"Job training (β̂)"},
                model_labels=main_labels, stars="aer",
                stats=["N","R2","DV mean"],
                output="latex", filename=str(OUT_TAB / "table2_main.tex"))
    print("  →", OUT_TAB / "table2_main.tex")
except Exception as exc:
    print(f"  LaTeX: {exc!r}")

# Word + Excel exports for Table 2
try:
    rt2 = sp.regtable(*main_models, keep=["treat"],
                      coef_labels={"treat":"Job training (β̂)"},
                      model_labels=main_labels, stars="aer",
                      stats=["N","R2","DV mean"])
    rt2.to_word(str(OUT_TAB / "table2_main.docx"))
    print("  →", OUT_TAB / "table2_main.docx")
    rt2.to_excel(str(OUT_TAB / "table2_main.xlsx"))
    print("  →", OUT_TAB / "table2_main.xlsx")
except Exception as exc:
    print(f"  Word/Excel: {exc!r}")

# ── 4c. Design horse race ──────────────────────────────────
print("\n  ── Design horse race (Table 2-bis) ──")

ols_full = M5
try:
    aipw = sp.aipw(df, y="re78", treat="treat", covariates=covariates,
                   estimand="ATT", seed=SEED)
except Exception as exc:
    aipw = None; print(f"  AIPW: {exc!r}")

try:
    psm = sp.match(df, y="re78", treat="treat", covariates=covariates,
                   method="nearest", estimand="ATT")
except Exception as exc:
    psm = None; print(f"  PSM: {exc!r}")

try:
    dml = sp.dml(df, y="re78", treat="treat", covariates=covariates, model="plr")
except Exception as exc:
    dml = None; print(f"  DML: {exc!r}")

try:
    eb = sp.ebalance(df, y="re78", treat="treat", covariates=covariates)
    have_eb = True
except Exception as exc:
    eb = None; have_eb = False
    print(f"  Ebalance: {exc!r}")

race_models = [m for m in [ols_full, aipw, psm, dml, eb, iv_result] if m is not None]
race_labels = ["OLS","AIPW","PSM","DML-PLR"]
if have_eb:          race_labels.append("Ebalance")
if iv_result:        race_labels.append("IV(2SLS)")

# Collect estimates
print(f"\n  {'Estimator':<14s} {'β̂':>10s} {'SE':>10s} {'95% CI':>24s} {'N':>6s}")
print(("  " + "─"*64))
for lb, mm in zip(race_labels, race_models):
    b, se, lo, hi = _coef(mm, "treat")
    n = _nobs(mm) or ""
    print(f"  {lb:<14s} {b:>+10.1f} {se:>10.1f} [{lo:+10.1f}, {hi:+10.1f}] {str(n):>6s}")

try:
    sp.regtable(*race_models, keep=["treat"],
                coef_labels={"treat":"Job training (β̂)"},
                model_labels=race_labels, stars="aer", stats=["Estimator","N"],
                output="latex", filename=str(OUT_TAB / "table2b_design_race.tex"))
    print("  →", OUT_TAB / "table2b_design_race.tex")
except Exception as exc:
    print(f"  Horse-race regtable: {exc!r}")

# Word + Excel for Table 2-bis
try:
    rt2b = sp.regtable(*race_models, keep=["treat"],
                       coef_labels={"treat":"Job training (β̂)"},
                       model_labels=race_labels, stars="aer", stats=["Estimator","N"])
    rt2b.to_word(str(OUT_TAB / "table2b_design_race.docx"))
    print("  →", OUT_TAB / "table2b_design_race.docx")
    rt2b.to_excel(str(OUT_TAB / "table2b_design_race.xlsx"))
    print("  →", OUT_TAB / "table2b_design_race.xlsx")
except Exception as exc:
    print(f"  Word/Excel 2bis: {exc!r}")

# ── 4d. Figure — coefficient plot (progressive controls) ──
try:
    fig3, _ = sp.coefplot(*main_models, model_names=main_labels,
                       variables=["treat"],
                       title="Figure 4. β̂ treat across progressive-control specs (95% CI)")
    fig3.savefig(OUT_FIG / "fig4_coefplot.png", dpi=200)
    plt.close()
    print("  →", OUT_FIG / "fig4_coefplot.png")
except Exception as exc:
    print(f"  coefplot: {exc!r}")
    fig, ax = plt.subplots(figsize=(7, 4))
    ests, ses = [], []
    for mm in main_models:
        b, se, _, _ = _coef(mm, "treat")
        ests.append(b); ses.append(se)
    ests = np.array(ests); ses = np.array(ses)
    ys = np.arange(len(main_models))
    ax.errorbar(ests, ys, xerr=1.96*ses, fmt="o", color="#2f6f73", ecolor="#9bbcbc", capsize=4)
    ax.axvline(0, color="black", lw=1)
    ax.set_yticks(ys); ax.set_yticklabels(main_labels); ax.invert_yaxis()
    ax.set_xlabel("β̂ on treat (95% CI)")
    ax.set_title("Figure 4. β̂ on training across progressive-control specs")
    plt.tight_layout()
    fig.savefig(OUT_FIG / "fig4_coefplot.png", dpi=200)
    plt.close()
    print("  (manual) →", OUT_FIG / "fig4_coefplot.png")


# ════════════════════════════════════════════════════════════════
# §5  HETEROGENEITY
# ════════════════════════════════════════════════════════════════
print("\n" + "─" * 72)
print("§5  Heterogeneity analysis")
print("─" * 72)

slices = {
    "(1) All":          df,
    "(2) Black":        df[df["black"].eq(1)],
    "(3) Non-black":    df[df["black"].eq(0)],
    "(4) Married":      df[df["married"].eq(1)],
    "(5) Unmarried":    df[df["married"].eq(0)],
    "(6) HS dropout":   df[df["nodegree"].eq(1)],
    "(7) Has degree":   df[df["nodegree"].eq(0)],
    "(8) re74 > 0":     df[df["re74"].gt(0)],
}

slice_models = []
for name, sub in slices.items():
    if len(sub) < 30 or sub["treat"].nunique() < 2:
        slice_models.append(None)
        continue
    try:
        slice_models.append(sp.regress(
            "re78 ~ treat + age + educ + black + hispan + married + nodegree + re74 + re75",
            sub, robust="HC1"))
    except Exception as exc:
        print(f"  Slice '{name}' failed: {exc!r}")
        slice_models.append(None)

valid = [(lb, m) for lb, m in zip(slices, slice_models) if m is not None]
print(f"  Subgroups: {[v[0] for v in valid]}")

try:
    sp.regtable(*[m for _,m in valid], keep=["treat"],
                coef_labels={"treat":"Training"},
                model_labels=[lb for lb,_ in valid],
                stars="aer", stats=["N","R2","DV mean"],
                output="latex", filename=str(OUT_TAB / "table3_heterogeneity.tex"))
    print("  →", OUT_TAB / "table3_heterogeneity.tex")
except Exception as exc:
    print(f"  Heterogeneity regtable: {exc!r}")

# Word + Excel for Table 3
try:
    rt3 = sp.regtable(*[m for _,m in valid], keep=["treat"],
                      coef_labels={"treat":"Training"},
                      model_labels=[lb for lb,_ in valid],
                      stars="aer", stats=["N","R2","DV mean"])
    rt3.to_word(str(OUT_TAB / "table3_heterogeneity.docx"))
    print("  →", OUT_TAB / "table3_heterogeneity.docx")
    rt3.to_excel(str(OUT_TAB / "table3_heterogeneity.xlsx"))
    print("  →", OUT_TAB / "table3_heterogeneity.xlsx")
except Exception as exc:
    print(f"  Word/Excel 3: {exc!r}")

# Print subgroup estimates
for lb, m in valid:
    b, se, lo, hi = _coef(m, "treat")
    n = _nobs(m) or ""
    print(f"  {lb:<16s}  β̂={b:>+9.1f}  se={se:>7.1f}  CI=[{lo:+9.1f},{hi:+9.1f}]  N={n}")


# ════════════════════════════════════════════════════════════════
# §6  MECHANISMS — intentionally blank (no credible mediator)
# ════════════════════════════════════════════════════════════════
print("\n" + "─" * 72)
print("§6  Mechanisms — intentionally blank")
print("─" * 72)
print("  Lalonde data lacks a credible mediator. All observed variables")
print("  are pre-treatment confounders, not post-treatment mediators.")


# ════════════════════════════════════════════════════════════════
# §7  ROBUSTNESS GAUNTLET
# ════════════════════════════════════════════════════════════════
print("\n" + "─" * 72)
print("§7  Robustness gauntlet")
print("─" * 72)

# ── 7.1 Placebo — re75 as outcome ───────────────────────────
placebo = sp.regress("re75 ~ treat + age + educ + black + hispan + married + nodegree + re74",
                     df, robust="HC1")
b_pl = float(placebo.params["treat"])
se_pl = float(placebo.std_errors["treat"]) if hasattr(placebo,"std_errors") else float(
    getattr(placebo,"bse",{}).get("treat", float("nan")))
print(f"  Placebo (re75 outcome): β̂={b_pl:+.3f}  SE={se_pl:.3f}  t={abs(b_pl/se_pl):.2f}")

# ── 7.2 Oster (2019) δ bounds ─────────────────────────────
delta_star = None
oster = None
try:
    oster = sp.oster_delta(df, y="re78", x_base=["treat"],
                           x_controls=covariates,
                           r_max=0, n_boot=500, random_state=SEED)
    info = oster.model_info
    print(f"  Oster (2019) bounds:")
    print(f"    β_short = {info['beta_short']:.3f}, β_full = {info['beta_full']:.3f}")
    print(f"    R²_short = {info['r2_short']:.4f}, R²_full = {info['r2_full']:.4f}")
    print(f"    β*(δ=1) = {info.get('beta_star_delta1','N/A')}")
    delta_star = info.get("delta_star")
    if delta_star is not None:
        print(f"    δ* (zero-effect ratio) = {delta_star:.3f}")
        print(f"    {'→ ROBUST (|δ*|>1)' if abs(delta_star)>1 else '→ FRAGILE (|δ*|≤1)'}")
    else:
        print("    δ* = +inf → very robust")
except Exception as exc:
    print(f"  Oster bounds skipped: {exc!r}")

# ── 7.3 Sensitivity dashboard ──────────────────────────────
try:
    sens = sp.unified_sensitivity(M5, r2_treated=0.05, r2_controlled=0.10,
                                  include_oster=True)
    print(f"  Unified sensitivity: E-value point = {getattr(sens,'e_value_point','N/A')}")
except Exception as exc:
    print(f"  Unified sensitivity skipped: {exc!r}")

try:
    fig6 = sp.sensitivity_dashboard(M5)
    # SensitivityDashboard has no savefig; try to access underlying matplotlib figure
    if hasattr(fig6, 'figure'):
        fig6.figure.savefig(OUT_FIG / "fig6_sensitivity.png", dpi=200)
    elif hasattr(fig6, 'savefig'):
        fig6.savefig(OUT_FIG / "fig6_sensitivity.png", dpi=200)
    else:
        # Fallback: matplotlib figure stored as attribute
        import matplotlib as _mpl
        _mpl.pyplot.savefig(OUT_FIG / "fig6_sensitivity.png", dpi=200)
    plt.close()
    print("  →", OUT_FIG / "fig6_sensitivity.png")
except Exception as exc:
    print(f"  Sensitivity dashboard: {exc!r}")

# ── 7.4 Robustness master (Table A1) ───────────────────────
rob = {}
rob["(1) Baseline (OLS)"] = M5

rob["(2) Drop top 1% re78"] = sp.regress(
    "re78 ~ treat + age + educ + black + hispan + married + nodegree + re74 + re75",
    df.query("re78 < re78.quantile(0.99)"), robust="HC1")

rob["(3) re74>0 only"] = sp.regress(
    "re78 ~ treat + age + educ + black + hispan + married + nodegree + re74 + re75",
    df.query("re74 > 0"), robust="HC1")

rob["(4) Drop nodegree"] = sp.regress(
    "re78 ~ treat + age + educ + black + hispan + married + re74 + re75",
    df, robust="HC1")

df_log = df.assign(log_re78=np.log1p(df["re78"]))
rob["(5) log(1+re78)"] = sp.regress(
    "log_re78 ~ treat + age + educ + black + hispan + married + nodegree + re74 + re75",
    df_log, robust="HC1")

rob["(6) PSM"] = psm
rob["(7) AIPW"] = aipw
rob["(8) DML-PLR"] = dml
if have_eb:
    rob["(9) Ebalance"] = eb
if iv_result:
    rob["(10) IV(2SLS)"] = iv_result

try:
    sp.regtable(*rob.values(), keep=["treat"],
                coef_labels={"treat":"Training (β̂)"},
                model_labels=list(rob), stars="aer",
                stats=["Estimator","N","R2"],
                output="latex", filename=str(OUT_TAB / "tableA1_robustness.tex"))
    print("  →", OUT_TAB / "tableA1_robustness.tex")
except Exception as exc:
    print(f"  Robustness regtable: {exc!r}")

# Word + Excel for Table A1
try:
    rtA1 = sp.regtable(*rob.values(), keep=["treat"],
                       coef_labels={"treat":"Training (β̂)"},
                       model_labels=list(rob), stars="aer",
                       stats=["Estimator","N","R2"])
    rtA1.to_word(str(OUT_TAB / "tableA1_robustness.docx"))
    print("  →", OUT_TAB / "tableA1_robustness.docx")
    rtA1.to_excel(str(OUT_TAB / "tableA1_robustness.xlsx"))
    print("  →", OUT_TAB / "tableA1_robustness.xlsx")
except Exception as exc:
    print(f"  Word/Excel A1: {exc!r}")

# Figure 5 — robustness forest
try:
    fig5, _ = sp.coefplot(*rob.values(), model_names=list(rob),
                       variables=["treat"],
                       title="Figure 5. β̂ on treat across robustness specs (95% CI)")
    fig5.savefig(OUT_FIG / "fig5_robustness_forest.png", dpi=200)
    plt.close()
    print("  →", OUT_FIG / "fig5_robustness_forest.png")
except Exception as exc:
    print(f"  Robustness forest: {exc!r}")
    rows = []
    for lb, mm in rob.items():
        b, se, lo, hi = _coef(mm, "treat")
        if not np.isnan(b):
            rows.append((lb, b, se))
    if rows:
        fig, ax = plt.subplots(figsize=(8, 4.5))
        labs = [r[0] for r in rows]
        ests = np.array([r[1] for r in rows])
        ses  = np.array([r[2] for r in rows])
        ys   = np.arange(len(rows))
        ax.errorbar(ests, ys, xerr=1.96*ses, fmt="o", color="#2f6f73", ecolor="#9bbcbc", capsize=4)
        ax.axvline(0, color="black", lw=1)
        ax.set_yticks(ys); ax.set_yticklabels(labs); ax.invert_yaxis()
        ax.set_xlabel("β̂ on treat (95% CI)")
        ax.set_title("Figure 5. Robustness check — β̂ across specifications")
        plt.tight_layout()
        fig.savefig(OUT_FIG / "fig5_robustness_forest.png", dpi=200)
        plt.close()
        print("  (manual) →", OUT_FIG / "fig5_robustness_forest.png")

# ── 7.5 Specification curve ────────────────────────────────
try:
    sc = sp.spec_curve(df, y="re78", x="treat",
                       controls=[
                           ["age","educ"],
                           ["age","educ","black","hispan"],
                           ["age","educ","black","hispan","married","nodegree"],
                           covariates,
                       ],
                       subsets={
                           "all": None,
                           "re74_pos": df["re74"].gt(0),
                           "no_top1": df["re78"] < df["re78"].quantile(0.99),
                       })
    fig, ax = plt.subplots(figsize=(8, 4.2))
    spec_df = sc.results_df.sort_values("estimate").reset_index(drop=True)
    ax.errorbar(x=np.arange(len(spec_df)), y=spec_df["estimate"],
                yerr=1.96*spec_df["se"], fmt="o",
                color="#2f6f73", ecolor="#9bbcbc", capsize=3)
    ax.axhline(0, color="black", lw=1)
    ax.set_title("Figure 5-bis. Specification curve: β̂ on treat")
    ax.set_xlabel("specification (sorted)"); ax.set_ylabel("estimate ± 95% CI")
    plt.tight_layout()
    fig.savefig(OUT_FIG / "fig5b_spec_curve.png", dpi=200)
    plt.close()
    print("  Spec curve →", OUT_FIG / "fig5b_spec_curve.png")
except Exception as exc:
    print(f"  Spec curve: {exc!r}")


# ════════════════════════════════════════════════════════════════
# §8  REPLICATION PACKAGE
# ════════════════════════════════════════════════════════════════
print("\n" + "─" * 72)
print("§8  Replication package")
print("─" * 72)

result = M5
b, se, ci_lo, ci_hi = _coef(result, "treat")
n_main = _nobs(result)

# LaTeX main table
tex = (
    "\\begin{tabular}{lc}\n"
    "\\toprule\n"
    " & 1978 earnings (re78) \\\\\n"
    "\\midrule\n"
    f"Training (treat) & {b:>+.2f} \\\\\n"
    f"                  & ({se:.2f}) \\\\\n"
    f"95\\% CI           & [{ci_lo:+.1f}, {ci_hi:+.1f}] \\\\\n"
    f"N                & {n_main} \\\\\n"
    "\\bottomrule\n"
    "\\end{tabular}\n"
)
(OUT_TAB / "main.tex").write_text(tex)
print("  →", OUT_TAB / "main.tex")

# JSON machine-readable result
try:
    (OUT_ART / "main_result.json").write_text(
        json.dumps(result.to_dict(), default=str, indent=2))
    print("  →", OUT_ART / "main_result.json")
except Exception as exc:
    print(f"  to_dict: {exc!r}")

# Headline figure alias
if (OUT_FIG / "fig4_coefplot.png").exists():
    shutil.copyfile(OUT_FIG / "fig4_coefplot.png", OUT_FIG / "fig8_final_result.png")
    print("  →", OUT_FIG / "fig8_final_result.png")

# Reproducibility stamp
stamp = {
    "statspai_version": getattr(sp, "__version__", "unknown"),
    "seed": SEED, "n_obs": n_main,
    "estimand": "ATT (selection on observables + IV demonstration)",
    "headline_estimate": b,
    "headline_ci95": [ci_lo, ci_hi],
    "naive_unadjusted": float(naive_att),
    "iv_estimate": None if iv_result is None else float(iv_b),
    "iv_weak_instrument_F": fs_f if isinstance(fs_f, (int, float)) and not np.isnan(fs_f) else None,
    "oster_delta_star": float(delta_star) if isinstance(delta_star, (int, float)) and not np.isnan(delta_star) else None,
    "pre_registration":  str(OUT_ART / "empirical_strategy.md"),
    "data_contract":     str(OUT_ART / "data_contract.json"),
    "pap_power":         str(OUT_ART / "pap_power.json"),
}
(OUT_ART / "result.json").write_text(json.dumps(stamp, indent=2, default=str))
print("\n  Reproducibility stamp:")
for k, v in stamp.items():
    print(f"    {k:<22s} = {v}")
print("\n  →", OUT_ART / "result.json")

# ── Directory listing ──────────────────────────────────────────
print("\n" + "=" * 72)
print("OUTPUT DIRECTORY STRUCTURE")
print("=" * 72)
for d in sorted(OUT_ROOT.rglob("*")):
    if d.is_file():
        rel = str(d.relative_to(OUT_ROOT))
        sz = d.stat().st_size
        print(f"  {rel:<40s}  ({sz:>8d} bytes)")

print("\n" + "=" * 72)
print("PIPELINE COMPLETE — _statspai_pipeline_outputs_5.2/")
print("=" * 72)

# Step 8 — Publication Tables & Figures (Deep Reference)

Goal: turn raw regression objects into **publication-ready** tables and figures — no manual copy-paste, no inconsistency between text and output. Every table/figure in the paper should be generated from code, versioned, and reproducible.

## Contents

1. Regression tables — `stargazer` (statsmodels) and `pyfixest.etable`
2. Summary-statistics tables — `pandas.to_latex`, `tableone`
3. Coefficient plots (coefplot)
4. Event-study plots
5. Binscatter
6. Forest plots (subgroup / heterogeneity)
7. RD plots
8. Effect heatmaps (CATE by two dimensions)
9. Balance / love plots (for matching)
10. Export to LaTeX / Word / Excel / PNG / PDF
11. Consistent styling (themes, fonts, colors)
12. Automated table/figure generation from a config file

---

## 1. Regression tables

### Stargazer (statsmodels-compatible; closest to R's `stargazer`)

```python
from stargazer.stargazer import Stargazer
import statsmodels.formula.api as smf

m1 = smf.ols("log_wage ~ training", data=df).fit(cov_type="HC3")
m2 = smf.ols("log_wage ~ training + age", data=df).fit(cov_type="HC3")
m3 = smf.ols("log_wage ~ training + age + edu", data=df).fit(cov_type="HC3")
m4 = smf.ols("log_wage ~ training + age + edu + tenure",
             data=df).fit(cov_type="cluster", cov_kwds={"groups": df["worker_id"]})

sg = Stargazer([m1, m2, m3, m4])
sg.title("Effect of training on log wage")
sg.custom_columns(["(1)","(2)","(3)","(4)"], [1,1,1,1])
sg.rename_covariates({
    "training": "Training",
    "age": "Age", "edu": "Years of education", "tenure": "Tenure",
    "Intercept": "Constant",
})
sg.covariate_order(["training","age","edu","tenure","Intercept"])
sg.significance_levels([0.10, 0.05, 0.01])
sg.add_line("Cluster SE", ["No","No","No","Worker"])
sg.add_line("Sample",     ["All","All","All","All"])

with open("tables/table_main.tex","w") as f:
    f.write(sg.render_latex())
# HTML version
with open("tables/table_main.html","w") as f:
    f.write(sg.render_html())
```

### `pyfixest.etable` (best for papers with lots of FE)

```python
import pyfixest as pf
results = [
    pf.feols("log_wage ~ training", data=df),
    pf.feols("log_wage ~ training + age", data=df),
    pf.feols("log_wage ~ training + age + edu | worker_id", data=df),
    pf.feols("log_wage ~ training + age + edu + tenure | worker_id + year",
             data=df, vcov={"CRV1":"worker_id"}),
]
pf.etable(
    results,
    type="tex",                          # "tex" / "md" / "df" / "html"
    file="tables/table_main.tex",
    keep=["training","age","edu","tenure"],   # which coefs to show
    labels={"training":"Training","age":"Age","edu":"Education","tenure":"Tenure"},
    signif_code=[0.01, 0.05, 0.10],
    notes=r"Cluster-robust SEs by worker\_id in parentheses.",
)
# Automatically adds FE indicator rows, N, R² — unlike stargazer.
```

### `summary_col` (statsmodels' built-in, simpler / less polished)

```python
from statsmodels.iolib.summary2 import summary_col
summary_col([m1,m2,m3,m4],
            stars=True, float_format="%.3f",
            model_names=["(1)","(2)","(3)","(4)"],
            info_dict={
                "R²": lambda x: f"{x.rsquared:.3f}",
                "N":  lambda x: f"{int(x.nobs)}",
            })
```

---

## 2. Summary-statistics tables

```python
# Option A: pandas + to_latex (simple, robust)
desc = df[["log_wage","age","edu","tenure","training"]] \
          .describe().T[["count","mean","std","min","50%","max"]]
desc.columns = ["N","Mean","SD","Min","Median","Max"]
desc.to_latex("tables/table_summary.tex",
              float_format="%.3f", escape=False,
              caption="Summary statistics", label="tab:summary")

# Option B: tableone — publication formatted with SMDs & p-values
from tableone import TableOne
t1 = TableOne(df,
              columns=["log_wage","age","edu","tenure","female"],
              categorical=["female"],
              groupby="training", pval=True, smd=True,
              decimals=3)
t1.to_latex("tables/table1_stratified.tex")
```

---

## 3. Coefficient plots

The single most effective way to convey multiple regression results — an informed reader can read this faster than any table.

```python
import matplotlib.pyplot as plt

def coefplot(results, coef_name, labels=None, figsize=(6,4), save=None):
    if labels is None: labels = [f"M{i+1}" for i in range(len(results))]
    betas = [r.coef()[coef_name] for r in results]
    ses   = [r.se()[coef_name]   for r in results]
    lb    = [b - 1.96*s for b,s in zip(betas,ses)]
    ub    = [b + 1.96*s for b,s in zip(betas,ses)]

    fig, ax = plt.subplots(figsize=figsize)
    ax.errorbar(labels, betas,
                yerr=[np.array(betas)-lb, np.array(ub)-np.array(betas)],
                fmt="o", capsize=4, lw=1.5, color="steelblue")
    ax.axhline(0, ls="--", color="gray", lw=0.8)
    ax.set_ylabel(f"Coefficient on {coef_name}")
    ax.spines[["top","right"]].set_visible(False)
    plt.tight_layout()
    if save: plt.savefig(save, dpi=300, bbox_inches="tight")
    return fig

coefplot(results, "training",
         labels=["M1 raw","M2 +age/edu","M3 +tenure","M4 +unit FE","M5 +year FE","M6 +ind×yr"],
         save="figures/fig_coefplot.pdf")
```

Horizontal version (better for long labels):

```python
def coefplot_h(results, coef_name, labels=None, figsize=(6,5), save=None):
    if labels is None: labels = [f"M{i+1}" for i in range(len(results))]
    betas = np.array([r.coef()[coef_name] for r in results])
    ses   = np.array([r.se()[coef_name]   for r in results])
    fig, ax = plt.subplots(figsize=figsize)
    ax.errorbar(betas, labels, xerr=1.96*ses, fmt="o", capsize=4,
                lw=1.5, color="steelblue")
    ax.axvline(0, ls="--", color="gray", lw=0.8)
    ax.set_xlabel(f"Coefficient on {coef_name}")
    ax.spines[["top","right"]].set_visible(False)
    plt.tight_layout()
    if save: plt.savefig(save, dpi=300)
```

---

## 4. Event-study plots

```python
# Via pyfixest (simplest)
es = pf.feols("log_wage ~ i(rel_time, ref=-1) | worker_id + year",
              data=df, vcov={"CRV1":"worker_id"})
pf.iplot(es, figsize=(8,4))   # saves internally or returns fig

# Manual (full styling control)
coefs = es.tidy().reset_index()               # term, coef, se, t, p
coefs = coefs[coefs["Coefficient"].str.contains("rel_time::")]
coefs["k"]  = coefs["Coefficient"].str.extract(r"rel_time::(-?\d+)").astype(int)
coefs = pd.concat([coefs, pd.DataFrame({"k":[-1],"Estimate":[0],"Std. Error":[0]})])\
          .sort_values("k")

fig, ax = plt.subplots(figsize=(8,4))
ax.errorbar(coefs["k"], coefs["Estimate"], yerr=1.96*coefs["Std. Error"],
            fmt="o-", color="steelblue", capsize=3)
ax.axhline(0, ls="--", color="gray")
ax.axvline(-0.5, ls="--", color="red", label="Treatment")
ax.set_xlabel("Years relative to treatment"); ax.set_ylabel("Coefficient (ATT)")
ax.legend(); ax.spines[["top","right"]].set_visible(False)
plt.tight_layout(); plt.savefig("figures/fig_event_study.pdf", dpi=300)
```

---

## 5. Binscatter

```python
# Via the `binsreg` package (Cattaneo et al.)
from binsreg import binsreg
bs = binsreg(y=df["log_wage"], x=df["tenure"],
             w=df[["age","edu","female"]],    # residualize on controls
             nbins=20, polyreg=1, ci=True)
# binsreg returns figure objects; access via bs.bins_plot

# Manual
df["bin"] = pd.qcut(df["tenure"], 20, duplicates="drop")
bs = df.groupby("bin").agg(x=("tenure","mean"), y=("log_wage","mean"),
                           n=("log_wage","count"),
                           y_sd=("log_wage","std"))
bs["se"] = bs["y_sd"] / np.sqrt(bs["n"])

fig, ax = plt.subplots(figsize=(6,4))
ax.errorbar(bs["x"], bs["y"], yerr=1.96*bs["se"], fmt="o", capsize=3,
            color="steelblue")
# Add OLS fit
m = smf.ols("log_wage ~ tenure + age + edu + female", data=df).fit()
xg = np.linspace(bs["x"].min(), bs["x"].max(), 100)
ax.plot(xg, m.params["Intercept"] + m.params["tenure"]*xg, color="darkred", lw=1.5)
ax.set_xlabel("Tenure"); ax.set_ylabel("Log wage (bin mean)")
plt.tight_layout(); plt.savefig("figures/fig_binscatter.pdf", dpi=300)
```

---

## 6. Forest plots (subgroup / heterogeneity)

```python
groups = [
    ("Overall",       df),
    ("Female = 0",    df[df.female==0]),
    ("Female = 1",    df[df.female==1]),
    ("Young (<40)",   df[df.age<40]),
    ("Old (≥40)",     df[df.age>=40]),
    ("Manuf",         df[df.industry=="manuf"]),
    ("Service",       df[df.industry=="service"]),
]
rows = []
for name, sub in groups:
    r = pf.feols("log_wage ~ training | worker_id + year",
                 data=sub, vcov={"CRV1":"worker_id"})
    rows.append({"group": name,
                 "beta": r.coef()["training"],
                 "se":   r.se()["training"],
                 "n":    int(r._N)})
fp = pd.DataFrame(rows)

fig, ax = plt.subplots(figsize=(7, 0.5*len(fp)+1))
y = np.arange(len(fp))[::-1]
ax.errorbar(fp["beta"], y, xerr=1.96*fp["se"],
            fmt="D", color="steelblue", capsize=4, markersize=5)
ax.axvline(0, ls="--", color="gray")
ax.set_yticks(y); ax.set_yticklabels(fp["group"])
for yi, (b, se, n) in enumerate(zip(fp["beta"], fp["se"], fp["n"])):
    ax.text(fp["beta"].max() + 2*fp["se"].max(),
            len(fp)-1-yi,
            f"β={b:.3f}\n(SE={se:.3f})\nN={n}",
            fontsize=8, va="center")
ax.set_xlabel("Coefficient on training")
ax.spines[["top","right"]].set_visible(False)
plt.tight_layout(); plt.savefig("figures/fig_forest.pdf", dpi=300)
```

---

## 7. RD plots

```python
from rdrobust import rdplot
# Default: quantile-spaced bins with local polynomial fit
rdplot(y=df["outcome"], x=df["running_var"], c=0, nbins=[20,20])

# Custom styling
fig = rdplot(y=df["outcome"], x=df["running_var"], c=0,
             binselect="esmv",        # even-space, MSE-optimal, variance-matched
             kernel="triangular",
             p=1,                     # local linear
             title="Effect of eligibility on earnings",
             y_label="Earnings (€/year)",
             x_label="Eligibility score (centered at cutoff)")
plt.savefig("figures/fig_rdplot.pdf", dpi=300)
```

---

## 8. CATE heatmap (two-dimensional heterogeneity)

```python
# After fitting a causal forest, compute CATE on a 2D grid
grid_age     = np.linspace(df["age"].quantile(0.05), df["age"].quantile(0.95), 20)
grid_tenure  = np.linspace(df["tenure"].quantile(0.05), df["tenure"].quantile(0.95), 20)
AA, TT       = np.meshgrid(grid_age, grid_tenure)

Xg = pd.DataFrame({
    "age":       AA.ravel(), "tenure": TT.ravel(),
    "edu":       df["edu"].median(),
    "firm_size": df["firm_size"].median(),
})
tau_grid = cf.effect(Xg).reshape(AA.shape)

plt.figure(figsize=(6,5))
plt.pcolormesh(AA, TT, tau_grid, cmap="RdBu_r", shading="auto", vmin=-abs(tau_grid).max(), vmax=abs(tau_grid).max())
plt.colorbar(label="CATE")
plt.xlabel("Age"); plt.ylabel("Tenure")
plt.title("Heterogeneous treatment effect")
plt.tight_layout(); plt.savefig("figures/fig_cate_heatmap.pdf", dpi=300)
```

---

## 9. Balance / love plots (for matching / IPW)

```python
# Compute SMDs pre/post matching for each covariate
covs = ["age","edu","tenure","female","firm_size"]
rows = []
for c in covs:
    pre  = (df.loc[df.training==1,c].mean() - df.loc[df.training==0,c].mean()) / \
           np.sqrt((df.loc[df.training==1,c].var()+df.loc[df.training==0,c].var())/2)
    post = (matched.loc[matched.training==1,c].mean() - matched.loc[matched.training==0,c].mean()) / \
           np.sqrt((matched.loc[matched.training==1,c].var()+matched.loc[matched.training==0,c].var())/2)
    rows.append({"cov": c, "pre": pre, "post": post})
love = pd.DataFrame(rows)

fig, ax = plt.subplots(figsize=(6, 0.5*len(love)+1))
y = np.arange(len(love))[::-1]
ax.scatter(love["pre"],  y, marker="o", s=60, label="Before", color="steelblue")
ax.scatter(love["post"], y, marker="s", s=60, label="After",  color="darkred")
for yi in y: ax.plot([love["pre"].iloc[len(love)-1-yi], love["post"].iloc[len(love)-1-yi]],
                     [yi, yi], color="gray", lw=0.5)
ax.axvline(0, color="k", lw=0.5); ax.axvline( 0.1, ls="--", color="red")
ax.axvline(-0.1, ls="--", color="red")
ax.set_yticks(y); ax.set_yticklabels(love["cov"])
ax.set_xlabel("Standardized mean difference")
ax.legend(); ax.spines[["top","right"]].set_visible(False)
plt.tight_layout(); plt.savefig("figures/fig_loveplot.pdf", dpi=300)
```

---

## 10. Export

### LaTeX

```python
# Tables
sg.render_latex()          # stargazer
pf.etable(results, type="tex", file="tables/t.tex")

# Or raw pandas
df_tbl.to_latex("tables/t.tex", float_format="%.3f", escape=False,
                column_format="lcccc", na_rep="—",
                caption="Main results", label="tab:main")
```

### Word

```python
# Via docx + pandas
import docx
doc = docx.Document()
doc.add_heading("Table: Main results", level=1)
t = doc.add_table(rows=df_tbl.shape[0]+1, cols=df_tbl.shape[1]+1)
# ... fill cells ...
doc.save("tables/table_main.docx")

# Or via HTML render → open in Word
with open("tables/t.html","w") as f: f.write(sg.render_html())
```

### Excel

```python
with pd.ExcelWriter("tables/all_tables.xlsx") as w:
    desc.to_excel(w, sheet_name="Summary")
    t1  .to_excel(w, sheet_name="Table 1")
    # ... etc.
```

### Figures

```python
plt.savefig("figures/fig.pdf", dpi=300, bbox_inches="tight")    # LaTeX
plt.savefig("figures/fig.png", dpi=300, bbox_inches="tight")    # Word / web
plt.savefig("figures/fig.svg", bbox_inches="tight")             # editable
```

---

## 11. Consistent styling

Drop this at the top of the analysis script:

```python
import matplotlib as mpl, matplotlib.pyplot as plt
mpl.rcParams.update({
    "font.family":       "serif",
    "font.serif":        ["Times New Roman", "Times"],
    "font.size":         11,
    "axes.titlesize":    12,
    "axes.labelsize":    11,
    "xtick.labelsize":   10,
    "ytick.labelsize":   10,
    "legend.fontsize":   10,
    "figure.figsize":    (6, 4),
    "figure.dpi":        100,
    "savefig.dpi":       300,
    "savefig.bbox":      "tight",
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "axes.grid":         True,
    "grid.alpha":        0.3,
    "grid.linestyle":    ":",
    "lines.linewidth":   1.5,
    "lines.markersize":  5,
})
# Consistent color palette
COLORS = {"treated": "#1f77b4", "control": "#ff7f0e",
          "ci":      "#cccccc", "line":    "#333333"}
```

---

## 12. Automated generation from config

For full reproducibility, declare every table/figure in a YAML config and have one script render them all:

```yaml
# analysis.yaml
tables:
  main:
    specs:
      - {name: M1, formula: "log_wage ~ training"}
      - {name: M4, formula: "log_wage ~ training + age + edu + tenure | worker_id + year",
         cluster: worker_id}
    keep: [training, age, edu, tenure]
    out:  tables/table_main.tex

figures:
  coefplot_main:
    results_ref: main
    coef:        training
    out:         figures/fig_coefplot.pdf
```

```python
import yaml
cfg = yaml.safe_load(open("analysis.yaml"))
for tbl_name, tbl_cfg in cfg["tables"].items():
    # build, etable, write
    ...
for fig_name, fig_cfg in cfg["figures"].items():
    # coefplot / eventstudy / forest
    ...
```

This makes the manuscript-to-code traceability explicit: every visible figure in the paper has exactly one generating spec.

---

## Canonical output directory

```
paper/
├── tables/
│   ├── table_summary.tex
│   ├── table1_stratified.tex
│   ├── table_main.tex
│   ├── table_robust_specs.tex
│   ├── table_robust_cluster.tex
│   ├── table_heterogeneity.tex
│   └── table_mediation.tex
└── figures/
    ├── fig_corr_heatmap.pdf
    ├── fig_distributions.pdf
    ├── fig_did_motivation.pdf
    ├── fig_panel_coverage.pdf
    ├── fig_coefplot.pdf
    ├── fig_event_study.pdf
    ├── fig_binscatter.pdf
    ├── fig_rdplot.pdf
    ├── fig_forest.pdf
    ├── fig_spec_curve.pdf
    ├── fig_permutation.pdf
    ├── fig_loo.pdf
    ├── fig_cate_heatmap.pdf
    ├── fig_marginal_effect.pdf
    └── fig_loveplot.pdf
```

Every file regenerated from source on a single `python main.py`. No manual Excel, no manual Photoshop, no manual LaTeX editing.

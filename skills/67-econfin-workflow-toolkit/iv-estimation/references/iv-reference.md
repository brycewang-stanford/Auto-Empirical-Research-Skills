# IV Estimation — Detailed Reference

## Weak Instrument Robust Inference

When F-stat is between 5–10, standard 2SLS inference can be unreliable. Use:

### Anderson-Rubin Confidence Set

```python
# Python — AR confidence set (linearmodels)
result = IV2SLS.from_formula('y ~ 1 + w [x ~ z]', data=df).fit()
# AR test included in diagnostics
print(result.anderson_rubin)
```

```stata
* Stata
ivreg2 y (x = z) w, robust ar
```

### LIML (Limited Information Maximum Likelihood)

More robust to weak instruments than 2SLS; consistent under weak instruments.

```python
from linearmodels.iv import IVLIML
result = IVLIML.from_formula('y ~ 1 + w + [x ~ z]', data=df).fit()
```

```r
library(AER)
ivreg(y ~ x + w | z + w, data = df, method = "liml")
```

```stata
ivregress liml y w (x = z), robust
```

## Control Function Approach

Alternative to 2SLS; allows nonlinear models with endogeneity.

```python
# Step 1: First stage
first_stage = smf.ols('x_endog ~ z + w1 + w2', data=df).fit()
df['v_hat'] = first_stage.resid

# Step 2: Include residuals as control
second_stage = smf.ols('y ~ x_endog + w1 + w2 + v_hat', data=df).fit(cov_type='HC3')
# Coefficient on v_hat tests endogeneity; coefficient on x_endog is consistent
```

## Multiple Endogenous Regressors

```python
# Two endogenous regressors, need at least 2 instruments
model = IV2SLS.from_formula(
    'y ~ 1 + w1 [x1_endog + x2_endog ~ z1 + z2 + z3]', data=df
).fit()
```

```stata
ivregress 2sls y w1 (x1_endog x2_endog = z1 z2 z3), robust first
```

## PSM: Balance Diagnostics

### Standardized Mean Differences (SMD)

After matching, all covariates should have |SMD| < 0.1.

```python
def smd(treated, control):
    return (treated.mean() - control.mean()) / \
           np.sqrt((treated.var() + control.var()) / 2)

for col in covariates:
    smd_before = smd(df[df.treatment==1][col], df[df.treatment==0][col])
    smd_after  = smd(matched_treated[col], matched_control[col])
    print(f"{col}: before={smd_before:.3f}, after={smd_after:.3f}")
```

```r
# Love plot
library(cobalt)
love.plot(match_out, binary = "std", thresholds = c(m = .1))
```

### Common Support Trimming

```python
# Trim observations outside common support
p_min = max(df[df.treatment==1]['pscore'].min(),
            df[df.treatment==0]['pscore'].min())
p_max = min(df[df.treatment==1]['pscore'].max(),
            df[df.treatment==0]['pscore'].max())
df_trimmed = df[(df['pscore'] >= p_min) & (df['pscore'] <= p_max)]
```

## Sensitivity Analysis for PSM (Rosenbaum Bounds)

Tests how strongly hidden bias would need to be to overturn results.

```r
library(rbounds)
psens(y_treated, y_matched_control, Gamma = 2, GammaInc = 0.1)
# Report: Gamma at which inference changes
```

## LATE vs ATE: Key Distinction

- **ATE** (Average Treatment Effect): average effect over all units
- **ATT** (Average Treatment Effect on Treated): average effect on those who received treatment
- **LATE** (Local ATE): IV estimate = average effect for **compliers** (units whose treatment status changes because of the instrument)

IV estimates LATE, not ATE or ATT. When discussing IV results:
> "Our IV estimate identifies the local average treatment effect (LATE) for compliers — units whose [treatment variable] was affected by [instrument name]."

## Classic Instrument Examples in Economics

| Instrument | Endogenous Variable | Outcome |
|-----------|---------------------|---------|
| Distance to college | Education | Earnings (Card 1995) |
| Quarter of birth | Years of schooling | Earnings (Angrist & Krueger 1991) |
| Vietnam lottery number | Military service | Earnings (Angrist 1990) |
| Rainfall | Agricultural income | Conflict |
| Judge leniency | Pretrial detention | Recidivism |
| Shift-share (Bartik) | Local employment | Various |

## Shift-Share (Bartik) Instruments

Bartik instruments use the interaction between national industry growth rates (shifts) and local industry composition (shares) to predict local employment changes.

### Construction

```
Bartik_it = Σ_j (share_ijt₀ × growth_jt)

share_ijt₀ = employment in industry j in region i at baseline / total employment in region i
growth_jt  = national growth rate of industry j (excluding region i)
```

### Code Templates

```r
# R — Bartik instrument construction
library(dplyr)

# Step 1: Calculate baseline industry shares
shares <- df %>%
  filter(year == baseline_year) %>%
  group_by(region_id) %>%
  mutate(share = emp_industry / sum(emp_industry)) %>%
  select(region_id, industry, share)

# Step 2: Calculate leave-one-out national growth rates
growth <- df %>%
  group_by(industry, year) %>%
  summarize(nat_emp = sum(emp_industry), .groups = "drop") %>%
  group_by(industry) %>%
  mutate(growth = (nat_emp - lag(nat_emp)) / lag(nat_emp))

# Step 3: Construct Bartik instrument
bartik <- shares %>%
  left_join(growth, by = "industry") %>%
  group_by(region_id, year) %>%
  summarize(bartik_iv = sum(share * growth, na.rm = TRUE), .groups = "drop")
```

```stata
* Stata — Bartik instrument
* Step 1: Baseline shares
bys region_id: egen total_emp = total(emp_industry) if year == `baseline'
gen share = emp_industry / total_emp if year == `baseline'

* Step 2: National growth (leave-one-out)
bys industry year: egen nat_emp = total(emp_industry)
replace nat_emp = nat_emp - emp_industry   // leave out own region
bys industry (year): gen growth = (nat_emp - nat_emp[_n-1]) / nat_emp[_n-1]

* Step 3: Bartik = sum of share × growth
gen share_growth = share * growth
bys region_id year: egen bartik_iv = total(share_growth)
```

### Inference with Bartik (Borusyak, Hull & Jaravel 2022)

Standard errors should account for exposure shares being pre-determined.

```r
# R — BHJ shock-level IV
# remotes::install_github("kolesarm/ShiftShareSE")
library(ShiftShareSE)

# Shock-level regression (preferred)
iv_result <- ivreg_ss(
  formula = outcome ~ controls | bartik_iv,
  data = df,
  W = share_matrix,         # N_regions × N_industries matrix of shares
  X = growth_vector,        # industry-level shocks
  region_var = "region_id"
)
summary(iv_result)
```

### Goldsmith-Pinkham, Sorkin & Swift (2020) — Rotemberg Weights

Decompose Bartik IV into contributions of each share.

```r
# Rotemberg weights to assess which shares drive identification
library(bartik.weight)
rot <- bartik.weight(
  y = df$outcome,
  x = df$treatment,
  z = share_matrix %*% diag(growth_vector),
  controls = model.matrix(~ controls, data = df)
)
```

## Judge/Examiner Designs

Use random assignment of cases to judges (or examiners, officers) as an instrument for the treatment decision.

### Framework

- **Setting**: Cases randomly assigned to decision-makers with different leniency
- **Instrument**: Judge leniency = leave-one-out average of judge's decisions
- **Estimand**: LATE for compliers (marginal defendants)

### Implementation

```r
# R — Judge leniency IV
library(AER)

# Step 1: Construct leave-one-out judge leniency
df <- df %>%
  group_by(judge_id) %>%
  mutate(
    judge_cases = n(),
    judge_rate = (sum(decision) - decision) / (judge_cases - 1)  # leave-one-out
  ) %>%
  ungroup()

# Step 2: IV regression
iv_judge <- ivreg(outcome ~ treatment + controls |
                  judge_rate + controls, data = df)
summary(iv_judge, diagnostics = TRUE)

# Step 3: Verify random assignment (balance test)
for (cov in c("age", "gender", "prior_record")) {
  bal <- lm(as.formula(paste(cov, "~ judge_rate + court_fe")), data = df)
  cat(cov, ": p =", summary(bal)$coefficients["judge_rate", "Pr(>|t|)"], "\n")
}
```

```stata
* Stata — judge leniency IV
* Leave-one-out residualized judge leniency (Stevenson 2018)
bys judge_id: egen n_cases = count(decision)
bys judge_id: egen total_decisions = total(decision)
gen judge_leniency = (total_decisions - decision) / (n_cases - 1)

* IV regression
ivregress 2sls outcome controls (treatment = judge_leniency), ///
    robust cluster(judge_id) first

* Balance tests
foreach var of varlist age gender prior_record {
    reg `var' judge_leniency i.court, robust cluster(judge_id)
}
```

### Key Assumptions for Judge IV
1. **Random assignment**: Cases randomly assigned to judges (conditional on court × time)
2. **Monotonicity**: A more lenient judge is more lenient for all defendants
3. **Exclusion**: Judge assignment affects outcomes only through the treatment decision
4. **Relevance**: Judges vary meaningfully in their decisions (F-stat on leniency)

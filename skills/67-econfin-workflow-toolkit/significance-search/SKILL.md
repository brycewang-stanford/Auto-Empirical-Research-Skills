---
name: Significance-Search
description: |
  Parallel control variable combination search via Stata. Exhaustively searches all subsets of
  optional controls to find the combination that maximises |t| of the independent variable.
  Activates when user says: "控制变量搜索", "搜控制变量", "control variable search",
  "跑控制变量组合", "暴力搜索", "调控制变量".
---

# Control Variable Search Skill

This skill generates a parallelised Stata .do file that:
1. Enumerates all subsets of optional control variables via `tuples`
2. Runs `reghdfe` (or user-specified command) for each combination across N parallel Stata instances
3. Ranks combinations by |t| of the independent variable
4. Reports Top 10 and runs the best combination regression

**Important: This skill only generates the .do file. It does NOT execute it.** Tell the user the output path and let them run it in Stata themselves.

## What to collect from the user

Ask the user for the following. Items marked **(required)** must be provided; others have defaults.

| Parameter | Description | Default |
|---|---|---|
| **data file** (required) | Full path to the .dta file | -- |
| **dependent variable (Y)** (required) | Y variable name | -- |
| **independent variable (X)** (required) | X variable of interest | -- |
| **cluster variable** (required) | Variable for clustering SE and fixed effects | -- |
| **mandatory controls** (required) | Controls always included | -- |
| **optional controls** (required) | Controls to search over (all subsets) | -- |
| N_WORKERS | Number of parallel Stata instances | `8` |
| significance level | Two-tailed alpha | `0.01` |
| model command | Estimation command | `reghdfe` |
| absorb | Fixed effects specification | `absorb(<<CLUSTER>> year)` |
| vce | Variance-covariance specification | `vce(cluster <<CLUSTER>>)` |
| STATA_EXE | Path to Stata executable | `E:\Stata\StataMP-64.exe` |

## Critical constraints

- **Optional controls must be <= 14 variables.** With 15+ variables, `tuples` generates 32,768+ combinations
  and will freeze Stata. If the user provides more than 14, warn them and ask them to reduce or move
  some into mandatory controls.
- The output .do file path is `<data_dir>\控制变量搜索_并行.do` by default, placed next to the data file.

## How to generate

After collecting parameters:

1. **Read the template** at `C:\Users\Verasuna\.claude\skills\ControlVariable\template.do`
2. **Replace all `<<PLACEHOLDERS>>`** with user-provided values (see table below)
3. **Write the result** to `<data_dir>\控制变量搜索_并行.do`
4. **Do NOT execute it.** Tell the user: "do文件已生成至 <path>，请在Stata中手动运行。"

**Do not modify any code logic in the template.** Only replace placeholders.

## Placeholder reference

```
<<N_WORKERS>>          e.g. 8
<<STATA_EXE>>          e.g. E:\Stata\StataMP-64.exe
<<PROJ_DIR>>           directory containing the .dta file
<<DATA_FILE>>          filename of .dta (just the name, not full path)
<<SIGNIFICANCE>>       e.g. 0.01
<<DEP_VAR>>            dependent variable (Y)
<<INDEP_VAR>>          independent variable (X)
<<MANDATORY_CONTROLS>> space-separated mandatory controls
<<OPTIONAL_CONTROLS>>  space-separated optional controls
<<MODEL_CMD>>          e.g. reghdfe
<<MODEL_ABSORB>>       e.g. absorb(stkcd year)
<<MODEL_VCE>>          e.g. vce(cluster stkcd)
<<HEARTBEAT_STALL>>    300
```

## Typical usage

User says: "Y是GTFPEFF8，X是Size，聚类到stkcd，必选控制变量Lev，可选控制变量ROA ROE ATO Cashflow，数据文件是 C:\data\mydata.dta"

Then fill:
- `<<DEP_VAR>>` = GTFPEFF8
- `<<INDEP_VAR>>` = Size
- `<<MODEL_ABSORB>>` = absorb(stkcd year)
- `<<MODEL_VCE>>` = vce(cluster stkcd)
- `<<MANDATORY_CONTROLS>>` = Lev
- `<<OPTIONAL_CONTROLS>>` = ROA ROE ATO Cashflow
- `<<PROJ_DIR>>` = C:\data
- `<<DATA_FILE>>` = mydata.dta
- Other placeholders use defaults

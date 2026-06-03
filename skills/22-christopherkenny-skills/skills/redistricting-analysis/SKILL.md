---
name: redistricting-analysis
description: "'Redistricting analysis in R using the redistverse ecosystem. Use whenever the user is working with redist, redistmetrics, ggredist, geomander, adj, alarmdata, PL94171, censable, easycensus, tinytiger, baf, rict, or redistio. Covers the complete pipeline: Census and spatial data loading, adjacency graph construction, SMC/MCMC simulation, constraints (population balance, county splits, VRA compliance), convergence diagnostics, plan metrics (compactness, partisan fairness, splits), visualization, summary tables, and interactive plan drawing. Invoke whenever the user mentions redistricting, gerrymandering, district plans, simulation ensembles, or any redistverse package by name.'"
---

# Redistricting Analysis with the redistverse

A comprehensive reference for redistricting analysis in R using the redistverse ecosystem (`library(redistverse)` loads `redist`, `redistmetrics`, `ggredist`, `geomander`, `sf`, and `adj`).

## Standard Analysis Pipeline

1. **Load data** — Download pre-built precinct map + demographics + elections via `alarmdata`, or assemble your own `sf` object and build a `redist_map`. → [12-alarmdata.md](references/12-alarmdata.md)
2. **Prepare adjacency** — Verify and edit the adjacency graph (remove water-body edges, fix topological errors). → [08-adj.md](references/08-adj.md), [09-geomander-adjacency.md](references/09-geomander-adjacency.md)
3. **Set constraints** — Define population tolerance, county-split penalties, VRA hinge constraints, compactness. → [02-redist-constraints.md](references/02-redist-constraints.md)
4. **Simulate** — Run `redist_smc()` (recommended) or MCMC to generate an ensemble of valid plans. → [01-redist-simulation.md](references/01-redist-simulation.md)
5. **Validate** — Check convergence (`summary()`), R-hat, effective sample size, and plan diversity. → [01-redist-simulation.md](references/01-redist-simulation.md)
6. **Score** — Compute compactness, partisan fairness, splits, and other metrics across the ensemble. → [04–06 redistmetrics references](references/04-redistmetrics-compactness.md)
7. **Visualize & compare** — Map plans, plot metric distributions, compare enacted plan to the baseline. → [07-ggredist.md](references/07-ggredist.md)

## Quick Navigation

| Package / Topic | Reference |
|----------------|-----------|
| `redist_map`, `redist_smc`, `redist_mergesplit`, `redist_flip`, `redist_plans`, diagnostics | [01-redist-simulation.md](references/01-redist-simulation.md) |
| `redist_constr`, `add_constr_splits`, `add_constr_grp_hinge`, all soft constraints | [02-redist-constraints.md](references/02-redist-constraints.md) |
| `redist_enumpart`, `redist_shortburst`, `redist_cyclewalk`, `init_particles` | [03-redist-advanced.md](references/03-redist-advanced.md) |
| `redistmetrics` — Polsby-Popper, Reock, spanning tree, `prep_perims`, `comp_*` functions | [04-redistmetrics-compactness.md](references/04-redistmetrics-compactness.md) |
| `redistmetrics` — efficiency gap, mean-median, bias, declination, `part_*` functions | [05-redistmetrics-partisan.md](references/05-redistmetrics-partisan.md) |
| `redistmetrics` — county splits, segregation, competitiveness, incumbents, `plan_parity`, `group_frac` | [06-redistmetrics-other.md](references/06-redistmetrics-other.md) |
| `ggredist` — `geom_district`, party color scales, cartographic palettes, `theme_map` | [07-ggredist.md](references/07-ggredist.md) |
| `adj` — adjacency graph construction, edge operations, coloring, Laplacian | [08-adj.md](references/08-adj.md) |
| `geomander` — adjacency construction, contiguity checks, `seam_rip`, edge editing | [09-geomander-adjacency.md](references/09-geomander-adjacency.md) |
| `geomander` — `geo_match`, `estimate_down/up`, `block2prec`, spatial estimation | [10-geomander-spatial.md](references/10-geomander-spatial.md) |
| `geomander` — downloading VEST, ALARM, DRA, HEDA, `get_lewis` election data | [11-geomander-data.md](references/11-geomander-data.md) |
| `alarmdata` — `alarm_50state_map`, pre-built datasets, caching, `alarm_add_plan` | [12-alarmdata.md](references/12-alarmdata.md) |
| `PL94171` — Census P.L. 94-171 decennial data ingestion | [13-pl94171.md](references/13-pl94171.md) |
| `censable` (data + state IDs), `easycensus` (ACS), `tinytiger` (TIGER shapefiles) | [14-census-utilities.md](references/14-census-utilities.md) |
| `baf` — download official Census Bureau block assignment files | [15-baf.md](references/15-baf.md) |
| `rict` — `gt` summary tables: population, demographics, elections, compactness, splits | [16-rict.md](references/16-rict.md) |
| `redistio` — interactive Shiny plan drawing (`draw()`) and adjacency editor (`adj_editor()`) | [17-redistio.md](references/17-redistio.md) |

## Key Data Structures

**`redist_map`** — an `sf` tibble with one row per precinct. Stores the adjacency graph, population column, number of districts, and population tolerance. Created by `redist_map()` or downloaded via `alarm_50state_map()`. Standard columns include `pop`, `pop_black`, `pop_hisp`, `pop_asian`, `pop_white`, `pop_vap`, `pop_bvap`, `ndv` (Democratic votes), `nrv` (Republican votes), and `geometry`.

**`redist_plans`** — a tibble with one row per district per plan (so `nsims × ndists` rows, plus reference plans). Stores district assignments in a hidden integer matrix; metrics are added as columns via `mutate()`. Access the plan matrix with `get_plans_matrix()`.

**`adj`** — an S3 vector class representing an adjacency list. Each element is a zero-indexed integer vector of neighbors. Stored as the `adj` column in `redist_map`.

## Population Tolerance Guidelines

| Map type | Typical `pop_tol` | Legal basis |
|----------|----------|-------------|
| Congressional | `0.005` (±0.5%) | *Wesberry v. Sanders* |
| State legislative | `0.05` (±10%) | *Reynolds v. Sims* |
| Local | Varies by state | State law |

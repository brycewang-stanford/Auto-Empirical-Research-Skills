---
name: data-finder
description: >-
  Find and assess datasets for a research question. Dispatches Explorer agents to search across data source categories, then Explorer-Critic to stress-test each candidate. Produces a ranked list with feasibility grades. Make sure to use this skill whenever the user wants to identify or evaluate data sources — not to search for papers or run analysis. Triggers include: "find data", "what data should I use", "find a dataset for this", "where can I get data on X", "assess datasets", "what datasets exist for", "help me find data", "is there data on this", "what are my data options", "I need data for this project", or any request to locate empirical data sources for a research question.
argument-hint: "[research topic or 'from spec']"
allowed-tools: ["Read", "Grep", "Glob", "Write", "WebSearch", "WebFetch", "Task"]
---

# Data Finder

Find and assess datasets for your research question. Two Explorer agents search in parallel across data source categories; an Explorer-Critic then stress-tests each candidate against the research design.

**Input:** `$ARGUMENTS` — a topic, or `from spec` to read the research question from `quality_reports/`.

---

## Step 1: Read Research Context

1. Find the most recent `quality_reports/project_spec_*.md` or `quality_reports/specs/*.md` — extract:
   - Research question
   - Empirical strategy (DiD, RDD, IV, etc.)
   - Treatment variable (what varies)
   - Outcome variable (what we measure)
   - Controls needed
   - Time period of interest
   - Geography (national, state, county, individual)
   - Unit of observation (individual, household, firm, establishment)

2. Read `references/domain-profile.md` if it exists — extract the Common Datasets section (domain-specific datasets to check first).

3. If no research spec exists, extract the variables and strategy from `$ARGUMENTS` directly. If the request is vague, ask: *"What are the treatment and outcome variables, and what empirical strategy did you have in mind?"*

---

## Step 2: Dispatch Two Explorer Agents in Parallel

Split the source categories between two Explorer agents to parallelize the search.

**Explorer A — Institutional Data:**
```
Task prompt: "You are an Explorer agent. Research question: [question].
Empirical strategy: [strategy].
Variables needed — Treatment: [X], Outcome: [Y], Controls: [list],
Time period: [period], Geography: [geo], Unit: [unit].
Domain datasets (check first): [list from domain-profile if available].

Your source categories to search:
1. Public microdata (CPS, ACS, NHIS, MEPS, SIPP, QWI)
2. Administrative data (Medicare/Medicaid, IRS, SSA, vital statistics, court records)
3. Survey panels (PSID, HRS, Add Health, NLSY97/79, BHPS/UKHLS)

For each dataset found, produce the full Explorer report format.
Follow the Explorer agent instructions."
```

**Explorer B — Broader and Alternative Sources:**
```
Task prompt: "You are an Explorer agent. Research question: [question].
Empirical strategy: [strategy].
Variables needed — Treatment: [X], Outcome: [Y], Controls: [list],
Time period: [period], Geography: [geo], Unit: [unit].
Domain datasets (check first): [list from domain-profile if available].

Your source categories to search:
1. International data (World Bank, OECD, Eurostat, IMF, IPUMS International)
2. Novel/alternative (satellite, web scraping, proprietary, RCT registries)
3. Any field-specific datasets not covered by Explorer A

For each dataset found, produce the full Explorer report format.
Follow the Explorer agent instructions."
```

---

## Step 3: Dispatch Explorer-Critic

After both Explorer agents complete, dispatch the Explorer-Critic with the full combined dataset list.

```
Task prompt: "You are an Explorer-Critic agent. Research question: [question].
Empirical strategy: [strategy].
Variables needed — Treatment: [X], Outcome: [Y], Controls: [list],
Time period: [period], Geography: [geo], Unit: [unit].

Here is the combined dataset list from the Explorer agents:
[paste all Explorer findings]

Apply the 5-point critique to each dataset:
1. Measurement validity
2. Sample selection
3. External validity
4. Identification compatibility
5. Known issues

Produce adjusted feasibility grades and deal-breaker flags.
Follow the Explorer-Critic agent instructions."
```

---

## Step 4: Produce Ranked Output

After the Explorer-Critic completes, compile the final ranked report:

1. Sort datasets by adjusted feasibility grade (A first, then B, then C, then D).
2. Within each grade, sort by identification compatibility score (highest first).
3. Separate out deal-breaker datasets into the rejection table.

---

## Step 5: Save Report

Save to `quality_reports/data_exploration_[sanitized_topic].md`:

```markdown
# Data Exploration: [Topic]

**Date:** [YYYY-MM-DD]
**Research question:** [one sentence]
**Empirical strategy:** [method]
**Variables sought:** Treatment = [X], Outcome = [Y], Controls = [list]

---

## Top Candidates (Grade A–B)

### 1. [Dataset Name] — Grade: A/B

**Provider:** [Name] | **Access:** [Public/Restricted/etc.] | **URL:** [link]

**Coverage:** [time period] | [geography] | [unit of observation] | N ≈ [size]

**Key Variables:**
- Treatment proxy: [variable]
- Outcome: [variable]
- Controls available: [list]

**Explorer-Critic Assessment:**
- Measurement validity: [1-2 sentences]
- Sample selection: [1-2 sentences]
- External validity: [1-2 sentences]
- Identification compatibility: [focused on the proposed strategy]
- Known issues: [specific documented problems]

**Bottom line:** [1-2 sentences — viable and under what conditions]

---

[Repeat for all A and B grade datasets]

---

## Accessible With Effort (Grade C)

[Brief summaries — name, access path, main limitation, why C not B]

---

## Rejection Table

| Dataset | Reason for Rejection | Deal-breaker? |
|---------|---------------------|---------------|
| [Name] | [Explorer-Critic finding] | YES/NO |

---

## Recommended Path Forward

1. **Best dataset:** [Name] — [one sentence why]
2. **Fallback if [best] unavailable:** [Name] — [why it's second choice]
3. **Access steps for [best]:** [specific actions needed — download link, application URL, IRB requirements]

---

## Next Steps

- **`/data-analysis [dataset]`** — begin analysis with the recommended dataset
- **`/lit-review [topic]`** — check if papers in the literature use these datasets (helps validate choice)
```

---

## Important

- **Identification compatibility is the most important criterion.** A perfectly accessible dataset that can't support the proposed empirical strategy is useless. The Explorer-Critic's grade on this dimension should drive the recommendation.
- **Access level affects timeline.** An FSRDC dataset may take 1-2 years to access. A public download can start today. Make this tradeoff explicit.
- **Don't reject C-grade datasets outright.** A FSRDC dataset with perfect identification fit may be the right choice for a dissertation. Present the access path clearly.

---
name: journal-selection
description: Use when choosing a target journal for a paper, comparing journal rankings, asking "where should I submit this", or building a submission strategy across multiple journals. Field-agnostic — detects the paper's research area and suggests appropriate outlets across tiers.
---

# Journal Selection

## Overview

This skill helps select target journals for a paper based on current web information. It does not maintain a static journal database — journal scopes, rankings, and editorial direction change, and stale data gives bad advice. Instead, every recommendation is verified via web fetch in the current session. The skill is field-agnostic: it detects the paper's research area and suggests appropriate outlets across ambition tiers.

## When to Use

- "Where should I submit this paper?"
- "What journals would take a paper on X?"
- "Rank these three journals for me"
- Planning a submission strategy with fallback options
- Checking a journal's current scope or editorial focus
- Comparing journals by review time, fees, or acceptance rate

## Mandatory Steps

1. **Identify the paper's field and contribution level** from the abstract, topic, and the user's stated ambition. The field determines which rankings and database subsets apply.

2. **Search journals via web search** — do not use a static list or cached knowledge. Journal scopes, rankings, and editorial boards change.

3. **Verify each candidate via web fetch** on the journal's official homepage. Confirm it is still active, currently accepting submissions, and matches the paper's topic. If the journal has changed scope or is no longer active, drop it.

4. **Check rankings appropriate to the user's context:**
   - **JCR (Journal Citation Reports)** and **Scimago (SJR)** for most fields
   - **RePEc rankings** for economics
   - **Qualis/Capes** for Brazilian authors (national evaluation system)
   - **ABS Academic Journal Guide** for business and management
   - **ERA (Australian Research Council)** for multidisciplinary use
   - **Field-specific rankings** when relevant (e.g., top-5 in economics, APSA in political science)

5. **Present 5-8 options in a markdown table** with columns:
   - `Journal`
   - `Area`
   - `Ranking` (field-appropriate, with source)
   - `Avg. Review Time` (when available)
   - `Submission Fee`
   - `Fit` (substantive reasoning, not "interesting")
   - `Tier` (ambitious / realistic / safety)

6. **Mix tiers:** 1-2 ambitious targets, 3-4 realistic, 1-2 safety options. The strategy matters more than individual choices — a submission plan needs fallbacks.

7. **Include regional and national journals when relevant.** If the user is Brazilian or the paper targets a Brazilian audience, include strong national journals (e.g., Revista Brasileira de Economia, Dados, Cadernos de Saúde Pública) alongside international options. Do not default to English-language journals only.

## Output Example

```markdown
| Journal | Area | Ranking | Review Time | Fee | Fit | Tier |
|---|---|---|---|---|---|---|
| American Economic Review | General econ | JCR Q1, RePEc top-5 | ~6 months | 0 | Requires general-interest contribution; strong identification strategy needed | Ambitious |
| Journal of Development Economics | Development | JCR Q1 | ~9 months | 0 | Strong fit for development topic; accepts both experimental and observational | Realistic |
| World Development | Development, policy | JCR Q1 | ~6 months | 0 | Interdisciplinary, policy-oriented, shorter turnaround | Realistic |
| Revista Brasileira de Economia | Econ (Brazil) | Qualis A2 | ~3 months | 0 | Strong national reach; fast review | Safety |
```

## Anti-Patterns

- Maintaining a static journal database in this skill — it will go stale
- Suggesting only top-5 journals without analyzing fit
- Ignoring regional or national journals when the paper has regional relevance
- Not verifying the journal is still active and accepting submissions
- Suggesting predatory journals — always check Beall's list or DOAJ membership when in doubt
- Copying rankings from memory (rankings update quarterly or annually)
- Confusing impact factor with field-relative quality (a Q1 in a specialized field may have lower IF than a Q2 in a broad field)
- Recommending a single journal without fallback options

## Verification Before Completion

- [ ] Each candidate verified via web fetch in the current session
- [ ] Rankings checked on the web, not from memory
- [ ] Mix of tiers presented (ambitious, realistic, safety)
- [ ] Fit column populated with substantive reasoning, not vague endorsements
- [ ] No predatory journals
- [ ] Regional journals included when relevant
- [ ] Submission fees and review times noted where available

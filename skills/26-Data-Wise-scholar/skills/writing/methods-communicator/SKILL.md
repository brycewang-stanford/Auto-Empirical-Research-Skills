---


name: methods-communicator
description: Effective communication strategies for statistical methods


---

# Methods Communicator

**Translating complex statistical methodology for applied researchers, practitioners, and students**

Use this skill when writing: package vignettes, tutorial materials, workshop content, applied journal articles, interpretation guides, FAQ documentation, or any communication targeting non-methodological audiences.

---

## Audience Adaptation

### Audience Profiles

| Audience | Statistical Background | Primary Needs | Communication Style |
|----------|----------------------|---------------|---------------------|
| **Methods Researchers** | Advanced | Theory, proofs, efficiency | Technical, precise |
| **Applied Statisticians** | Intermediate-Advanced | Implementation, assumptions | Technical with examples |
| **Quantitative Researchers** | Intermediate | When to use, interpretation | Practical, guided |
| **Graduate Students** | Developing | Step-by-step, intuition | Pedagogical, scaffolded |
| **Practitioners** | Variable | Point-and-click, templates | Simplified, checklist-based |

### Audience Detection Questions

1. What statistical training has this person likely had?
2. What is their primary goal (understanding vs. applying)?
3. How much mathematical notation is appropriate?
4. What prior knowledge can I assume?
5. What examples would resonate with their field?

---

## Plain Language Translations

### Core Mediation Concepts

| Technical Term | Plain Language | Analogy |
|----------------|----------------|---------|
| Natural Indirect Effect | How much of treatment's effect works through the mediator | "The portion of medicine that helps by reducing inflammation" |
| Natural Direct Effect | Treatment's effect through all other pathways | "All other ways the medicine helps beyond reducing inflammation" |
| Sequential Ignorability | No unmeasured confounding at each step | "Apples-to-apples comparison at each stage" |
| Positivity | All treatment combinations are possible | "Everyone had a real chance of getting either treatment" |
| Identification | Can estimate causal effect from data | "The data can answer our causal question" |

### Statistical Concepts

| Technical | Applied Researcher Version |
|-----------|---------------------------|
| "The estimator is consistent" | "With more data, estimates get closer to the truth" |
| "Asymptotically normal" | "For large samples, you can use normal-theory confidence intervals" |
| "Efficiency bound" | "The best precision you can possibly achieve" |
| "Double robust" | "Correct if either model is right (doesn't need both)" |
| "Bootstrapped confidence interval" | "We resampled the data many times to estimate uncertainty" |

### Effect Size Interpretation

```markdown
## Template: Interpreting Indirect Effects

**For a standardized indirect effect of 0.15:**

"The treatment increases the outcome by 0.15 standard deviations
through its effect on the mediator.

In practical terms: for every 100 people treated, we would expect
approximately [X] additional positive outcomes that can be attributed
specifically to the pathway through the mediator.

This effect size is considered [small/medium/large] by conventional
standards in [field]."
```

---

## Vignette Writing Framework

### Structure Template

```markdown
# Package Vignette: [Feature Name]

## Overview

[1-2 sentence description of what this vignette covers]

**You will learn:**
- [Learning objective 1]
- [Learning objective 2]
- [Learning objective 3]

**Prerequisites:**
- [Required knowledge 1]
- [Required package 2]

## Quick Start

[Minimal working example - copy-pasteable code that runs immediately]

## Detailed Tutorial

### Step 1: [First Action]

[Explanation of what we're doing and why]

```r
# Annotated code
result <- function_name(
  data = my_data,    # Your dataset
  mediator = "M",    # Name of mediator variable
  outcome = "Y"      # Name of outcome variable
)
```

**What this does:** [Plain language explanation]

**Common issues:**
- [Issue 1 and how to resolve]
- [Issue 2 and how to resolve]

### Step 2: [Second Action]

[Continue pattern...]

## Interpretation Guide

### Understanding the Output

```r
# Example output
print(result)
```

**Key values to look at:**

| Output | What it means | What's "good" |
|--------|---------------|---------------|
| `estimate` | The indirect effect | Depends on your context |
| `ci.lower`, `ci.upper` | 95% confidence interval | Doesn't include 0 = significant |
| `p.value` | Probability under null | < 0.05 conventionally significant |

### Real-World Interpretation

[Walk through interpretation in words someone would actually say]

## Troubleshooting

### Frequently Asked Questions

**Q: Why is my confidence interval so wide?**
A: [Clear, actionable explanation]

**Q: What if my mediator is binary?**
A: [Clear, actionable explanation]

## Next Steps

- For more complex models, see `vignette("advanced-models")`
- For sensitivity analysis, see `vignette("sensitivity")`
- For theoretical background, see [paper citation]

## References
```

---

## Pedagogical Techniques

### The "Build-Up" Approach

Start simple, add complexity gradually:

```markdown
## Understanding Mediation: A Graduated Approach

### Level 1: The Basic Idea (No Math)

Think of a drug that treats depression. It might work in two ways:
1. **Directly** affecting brain chemistry → improved mood
2. **Indirectly** by improving sleep → which then improves mood

Mediation analysis asks: "How much of the drug's benefit comes from
each pathway?"

### Level 2: With Diagrams (Minimal Math)

```
Treatment (X) ──────→ Outcome (Y)
      │                    ↑
      └────→ Mediator (M) ─┘
```

- **Direct effect**: X → Y arrow
- **Indirect effect**: X → M → Y pathway

### Level 3: With Simple Formulas

Total Effect = Direct Effect + Indirect Effect

- Direct: $c'$ (effect with M held constant)
- Indirect: $a \times b$ (X→M effect × M→Y effect)

### Level 4: Full Formal Notation

[For those who want the technical version]
```

### The "Running Example" Technique

Use one consistent example throughout:

```r
# Example dataset used throughout tutorials
# Intervention study: Exercise program for depression
# - treatment: exercise (1) vs. waitlist (0)
# - mediator: self_efficacy (continuous, 1-10)
# - outcome: depression_score (continuous, 0-63 BDI)
# - covariates: age, gender, baseline_depression

data("exercise_depression", package = "mediation")

# We'll use this data for all examples in this vignette
```

### Common Misconceptions Section

```markdown
## Common Misconceptions

### Misconception 1: "If the indirect effect is significant, mediation is proven"

**Why it's wrong:** Mediation analysis shows *statistical* association
through the mediator path, not *proof* of causal mediation.

**Better framing:** "Our data are consistent with a mediation process,
assuming our causal assumptions hold."

### Misconception 2: "A non-significant indirect effect means no mediation"

**Why it's wrong:** We may lack power to detect the effect, or the
effect may be small but real.

**Better framing:** "We did not find statistically significant evidence
of mediation (indirect effect = X, 95% CI: [L, U])."

### Misconception 3: "The bootstrapped CI is always better"

**Why it's wrong:** Bootstrap is better for *asymmetric* sampling
distributions (like products). For normally-distributed effects,
delta-method works fine.

**When to use which:** [Decision guide]
```

---

## Workshop Content Design

### Workshop Module Template

```markdown
# Module: [Topic Name]
## Duration: [X] minutes

### Learning Objectives
By the end of this module, participants will be able to:
1. [Measurable objective 1]
2. [Measurable objective 2]

### Pre-Assessment (2 min)
[Quick poll or question to gauge prior knowledge]

### Lecture Content (15 min)

#### Slide 1: Motivating Question
[Real-world question that motivates the topic]

#### Slide 2-5: Core Concept
[Building up the idea with visuals]

#### Slide 6-7: Worked Example
[Step-by-step with actual data]

### Hands-On Exercise (20 min)

**Setup:**
```r
# Load packages and data
library(mediation)
data("exercise_depression")
```

**Task 1:** [Specific task with expected output]

**Task 2:** [Build on Task 1]

**Discussion:** [Question to discuss with neighbor]

### Common Pitfalls (5 min)
[Mistakes you see people make, and how to avoid them]

### Wrap-Up (3 min)
- Key takeaways: [3 bullet points]
- For more practice: [Resources]
- Questions?
```

---

## Applied Journal Translation

### Adapting Methods for Applied Journals

| Methodological Paper | Applied Paper |
|---------------------|---------------|
| "We employ a semiparametric efficient estimator that achieves the efficiency bound under the nonparametric model" | "We used an efficient estimation approach that provides optimal precision" |
| "Under the assumption of sequential ignorability (Assumptions 1-3)..." | "Assuming no unmeasured confounding at each step of the mediation process..." |
| "The influence function takes the form..." | [Omit; put in supplement] |
| "Monte Carlo simulations with 1000 replications" | "We verified performance through simulation studies (see Supplementary Materials)" |

### Applied Methods Section Template

```markdown
## Statistical Analysis

### Mediation Model

We examined whether [mediator] explained the relationship between
[treatment] and [outcome] using [method name] (Author, Year). This
approach decomposes the total treatment effect into:

- **Direct effect**: The portion of the effect that operates
  independently of [mediator]
- **Indirect effect**: The portion operating through [mediator]

### Assumptions

This analysis requires that:
1. [Plain language assumption 1]
2. [Plain language assumption 2]
3. [Plain language assumption 3]

We assessed the sensitivity of our findings to potential violations
using [sensitivity analysis approach].

### Implementation

Analyses were conducted in R (version X.X) using the [package] package
(Author, Year). Confidence intervals were computed using [method] with
[N] bootstrap resamples. Code for all analyses is available at [URL].
```

---

## FAQ Templates

### General FAQ Structure

```markdown
## Frequently Asked Questions

### Getting Started

**Q: What type of data do I need for mediation analysis?**

A: You need:
- A treatment/exposure variable (X)
- A potential mediator variable (M)
- An outcome variable (Y)
- Ideally, covariates that might confound these relationships

The mediator should be measured *after* the treatment but *before*
(or contemporaneously with) the outcome.

---

**Q: How large should my sample be?**

A: For detecting medium-sized indirect effects (standardized ~ 0.26):
- N ≈ 150-200 for good power
- N ≈ 75 minimum for very large effects
- N ≈ 500+ for small effects

Use power analysis tools like `pwr.med` to determine your specific needs.

---

### Interpretation Questions

**Q: My indirect effect is significant but my direct effect is not.
What does this mean?**

A: This pattern suggests "full mediation" - the treatment's effect
appears to operate entirely through the mediator. However:
1. "Full" mediation is rare and often reflects low power for the direct effect
2. Focus on effect sizes, not just significance
3. Report both effects with confidence intervals

---

**Q: Can the indirect effect be larger than the total effect?**

A: Yes! This happens when direct and indirect effects have opposite signs.
For example:
- Direct effect: -0.20 (treatment directly *reduces* outcome)
- Indirect effect: +0.35 (treatment increases mediator, which increases outcome)
- Total effect: +0.15

This is called "inconsistent mediation" or "suppression."

---

### Troubleshooting

**Q: I'm getting an error about convergence. What should I do?**

A: Common solutions:
1. Check for missing data: `sum(is.na(your_data))`
2. Scale your variables: `scale(variable)`
3. Remove outliers or influential observations
4. Simplify your model (fewer covariates)
5. Increase bootstrap iterations

If problems persist, check the package's GitHub issues.
```

---

## Error Message Humanization

### Improving Error Messages in R Packages

```r
#' User-Friendly Error Messages
#'
#' @examples
#' # Instead of:
#' stop("non-conformable arguments")
#'
#' # Use:
#' stop(paste0(
#'   "The mediator and outcome variables have different lengths.\n",
#'   "  - mediator has ", length(mediator), " observations\n",
#'   "  - outcome has ", length(outcome), " observations\n",
#'   "Check for missing data or subsetting issues."
#' ))

# Wrapper for common checks
check_input <- function(data, treatment, mediator, outcome) {
  errors <- character()

  # Check variables exist
  if (!treatment %in% names(data)) {
    errors <- c(errors, sprintf(
      "Treatment variable '%s' not found in data.\nAvailable columns: %s",
      treatment, paste(names(data), collapse = ", ")
    ))
  }

  if (!mediator %in% names(data)) {
    errors <- c(errors, sprintf(
      "Mediator variable '%s' not found in data.\nAvailable columns: %s",
      mediator, paste(names(data), collapse = ", ")
    ))
  }

  # Check for missing data
  n_missing <- sum(is.na(data[[treatment]]) | is.na(data[[mediator]]) | is.na(data[[outcome]]))
  if (n_missing > 0) {
    errors <- c(errors, sprintf(
      "Found %d observations with missing data in key variables.\n",
      "Use `na.omit(data[c('%s', '%s', '%s')])` to remove, or consider multiple imputation.",
      n_missing, treatment, mediator, outcome
    ))
  }

  if (length(errors) > 0) {
    stop(paste(errors, collapse = "\n\n"), call. = FALSE)
  }
}
```

---

## Print Method Design

### Creating Informative Print Methods

```r
#' Print Method for Mediation Results
#'
#' Designed for applied researchers who need clear interpretation
print.mediation_result <- function(x, ...) {

  cat("\n")
  cat("======================================\n")
  cat("       MEDIATION ANALYSIS RESULTS     \n")
  cat("======================================\n\n")

  # Effect estimates
  cat("EFFECT DECOMPOSITION:\n")
  cat(sprintf("  Total Effect:    %6.3f  95%% CI [%6.3f, %6.3f]\n",
              x$total, x$total_ci[1], x$total_ci[2]))
  cat(sprintf("  Direct Effect:   %6.3f  95%% CI [%6.3f, %6.3f]\n",
              x$direct, x$direct_ci[1], x$direct_ci[2]))
  cat(sprintf("  Indirect Effect: %6.3f  95%% CI [%6.3f, %6.3f] %s\n",
              x$indirect, x$indirect_ci[1], x$indirect_ci[2],
              ifelse(x$indirect_ci[1] > 0 | x$indirect_ci[2] < 0, "*", "")))
  cat("\n")

  # Proportion mediated
  if (x$total != 0) {
    prop_med <- x$indirect / x$total * 100
    cat(sprintf("  Proportion Mediated: %.1f%%\n", prop_med))
  }
  cat("\n")

  # Plain language interpretation
  cat("INTERPRETATION:\n")
  if (x$indirect_ci[1] > 0) {
    cat(sprintf("  There is evidence of positive mediation (p < .05).\n"))
    cat(sprintf("  The treatment increases the outcome by %.3f through\n", x$indirect))
    cat(sprintf("  its effect on the mediator.\n"))
  } else if (x$indirect_ci[2] < 0) {
    cat(sprintf("  There is evidence of negative mediation (p < .05).\n"))
  } else {
    cat(sprintf("  The indirect effect is not statistically significant.\n"))
    cat(sprintf("  We cannot conclude that mediation is present.\n"))
  }
  cat("\n")

  # Caveats
  cat("IMPORTANT CAVEATS:\n")
  cat("  • Results assume no unmeasured confounding\n")
  cat("  • See sensitivity analysis with sensitivityAnalysis()\n")
  cat("  • Report effect sizes, not just p-values\n")
  cat("\n")

  invisible(x)
}
```

---

## Communication Checklist

### Before Sharing with Applied Audience

- [ ] Removed or defined all jargon
- [ ] Provided concrete examples for abstract concepts
- [ ] Included worked example with real (or realistic) data
- [ ] Added interpretation template for output
- [ ] Listed common pitfalls and how to avoid them
- [ ] Tested code examples actually run
- [ ] Had someone from target audience review

### Before Publishing Vignette

- [ ] Quick start section works in under 5 minutes
- [ ] All code chunks run without error
- [ ] Output is formatted readably
- [ ] Links to other vignettes for advanced topics
- [ ] References included for those wanting more depth
- [ ] Spell-checked and grammar-checked

---

## References

### Science Communication

- Katz, Y. (2013). Against storytelling of scientific results. *Nature Methods*
- Fischhoff, B. (2013). The sciences of science communication. *PNAS*
- Doumont, J. L. (2009). *Trees, Maps, and Theorems*

### Statistical Communication

- Gelman, A., & Nolan, D. (2002). *Teaching Statistics: A Bag of Tricks*
- Wickham, H. (2010). A layered grammar of graphics. *JCGS*
- Wilke, C. O. (2019). *Fundamentals of Data Visualization*

### R Package Documentation

- Wickham, H., & Bryan, J. (2023). *R Packages* (vignette chapter)
- rOpenSci Packages Guide: https://devguide.ropensci.org/

---

**Version**: 1.0.0
**Created**: 2025-12-08
**Domain**: Statistical communication for diverse audiences
**Target Outputs**: Vignettes, tutorials, workshops, applied papers

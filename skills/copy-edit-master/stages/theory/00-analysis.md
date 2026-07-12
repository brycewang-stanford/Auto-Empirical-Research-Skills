# Theory Paper Analysis

Standalone tool to analyze academic papers and determine whether they require the specialized theory-paper editing workflow or the general academic workflow.

## Purpose

Systematically assess whether a paper is a theory paper by identifying:
- Formal theorems, propositions, lemmas
- Mathematical proofs
- Formal model notation
- Technical definitions
- Proof structure elements

## Instructions

### Step 1: Read the Document

Use Read tool to load the full document.

### Step 2: Scan for Theory Paper Markers

**2a. Look for formal results** (high-confidence indicators):

Count instances of:
- **Theorem** [number]: ...
- **Proposition** [number]: ...
- **Lemma** [number]: ...
- **Corollary** [number]: ...

If 3+ formal results with proofs → **HIGH confidence theory paper**

**2b. Look for proof markers**:

Search for:
- "Proof:" or "Proof."
- "QED" (Latin: quod erat demonstrandum)
- "∎" (Halmos/tombstone symbol)
- "This completes the proof"

**2c. Assess mathematical notation density**:

Count pages with heavy mathematical notation:
- Greek symbols (α, β, γ, δ, θ, λ, μ, σ, etc.)
- Mathematical operators (∀, ∃, ∈, ⊆, ∩, ∪, →, ⇒, etc.)
- Set notation (X, 𝒳, {x₁, x₂, ...}, etc.)
- Function notation with subscripts/superscripts

If >50% of pages have dense mathematical notation → indicator of theory paper

**2d. Look for formal definitions**:

Search for:
- "**Definition [number]:**" or "**Definition:**"
- Formal definitions with boldface terms
- Sections titled "Definitions" or "Notation"

If multiple formal definitions with mathematical notation → indicator of theory paper

**2e. Check for model section**:

Look for sections titled:
- "Model"
- "Theoretical Framework"
- "Formal Model"
- "Setup"

Check if it contains:
- Formal assumptions (Assumption 1, Assumption 2, ...)
- Players/agents with formal notation
- Strategy sets, payoff functions, equilibrium concepts
- Optimization problems with mathematical notation

### Step 3: Scan for Empirical Paper Markers (Counter-Indicators)

**3a. Look for empirical sections**:

- "Data" or "Data Description"
- "Empirical Strategy"
- "Identification"
- "Results" with regression tables
- "Robustness Checks"

**3b. Look for statistical analysis**:

- Regression tables (Table 1, Table 2, ...)
- Statistical significance markers (p-values, standard errors in parentheses)
- Econometric terminology (OLS, IV, fixed effects, difference-in-differences)

**3c. Look for descriptive statistics**:

- "Summary Statistics" table
- "Sample Construction" section

### Step 4: Classification Decision

Use this decision tree:

**HIGH Confidence Theory Paper** (recommend 4-stage theory workflow):
- 3+ formal theorems/propositions WITH proofs, OR
- 5+ formal theorems/propositions (even without full proofs), OR
- Extensive proof section (>3 pages of formal proofs)

**MEDIUM Confidence Theory Paper** (recommend 4-stage theory workflow with caveat):
- 1-2 formal theorems/propositions with proofs, OR
- Formal model section + heavy mathematical notation throughout (>50% of pages), OR
- Multiple formal definitions + proof sketches

**LOW Confidence / General Academic** (recommend 3-stage general workflow):
- Empirical paper with estimation results
- Qualitative research
- Literature review or survey
- Policy analysis without formal model
- Empirical paper with simple theoretical motivation (no proofs)

**MIXED** (theory + empirical):
- Formal model AND empirical analysis
- **Recommendation**: Use theory workflow IF theoretical contribution is primary
- Ask user which aspect they want to emphasize

### Step 5: Provide Detailed Analysis Report

Output the analysis in this structured format:

```
📊 THEORY PAPER ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Document: [filename]
Total pages: [N]

🔍 THEORY MARKERS DETECTED:

Formal Results:
- Theorems: [count]
- Propositions: [count]
- Lemmas: [count]
- Corollaries: [count]
[List examples: "Theorem 1 (page 12): Main characterization result"]

Proof Structure:
- Formal proofs: [count] (pages: [list])
- Proof markers found: [QED / ∎ / other]
- Total proof length: ~[N] pages

Mathematical Notation:
- Density: [LOW / MEDIUM / HIGH]
- Pages with heavy notation: [N]/[total] ([percentage]%)
- Notation types: [e.g., "Set theory, game theory, optimization"]

Formal Definitions:
- Count: [N]
- Examples: [list 2-3 key definitions]

Model Section:
- [YES / NO]
- [If YES: "Contains formal assumptions, strategy sets, equilibrium concept"]

🔍 EMPIRICAL MARKERS DETECTED:

Data Section: [YES / NO]
Regression Tables: [count]
Econometric Methods: [list if present]
Summary Statistics: [YES / NO]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 CLASSIFICATION:

Type: [Theory Paper / General Academic / Mixed]
Confidence: [HIGH / MEDIUM / LOW]

Reasoning:
[2-3 sentences explaining the classification based on markers found]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 RECOMMENDATION:

Editing Workflow: [3-stage General / 4-stage Theory]

[If 3-stage]:
Stages:
1. Structural Edit (argument flow, organization)
2. Line Edit (Strunk & White rules, McCloskey principles)
3. Proofread (grammar, punctuation)

[If 4-stage]:
Stages:
1. Theory Structure (introduction, simple-to-general, literature narrative)
2. Technical Elements (notation, definitions, proofs, figures)
3. Theory Line Edit (general rules + theory-specific clarity)
4. Theory Proofread (standard + notation consistency)

Rationale:
[Explain why this workflow is appropriate]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❓ NEXT STEPS:

Does this classification look correct?
[If MEDIUM confidence or MIXED]: Would you like me to proceed with the [recommended] workflow, or do you prefer the alternative?
[If HIGH confidence]: Should I proceed with the [recommended] workflow?
```

### Step 6: Handle Edge Cases

**Case 1: MIXED paper (theory + empirical)**

Present both options to user:

```
⚠️  MIXED PAPER DETECTED

This paper contains both theoretical and empirical components.

Option A: Theory Workflow (4-stage)
Best if: Theoretical contribution is primary; proofs are central to paper's contribution
Focus: Notation clarity, proof structure, definition quality, then line editing

Option B: General Workflow (3-stage)
Best if: Empirical results are primary; theory is setup/motivation only
Focus: Argument flow, data presentation, statistical clarity, then line editing

Which aspect is more central to this paper's contribution?
```

Use AskUserQuestion to get user's choice.

**Case 2: LOW confidence / borderline**

```
⚠️  BORDERLINE CLASSIFICATION

This paper has some theoretical elements but may not require full theory workflow.

Detected: [list what was found]
Missing: [list what typical theory papers have that this lacks]

I recommend: [3-stage General workflow]
Alternative: [4-stage Theory workflow]

Reason: [explanation]

Would you like me to proceed with the recommended workflow, or use the alternative?
```

**Case 3: Unusual structure**

If paper doesn't fit standard patterns, describe what you see and ask user:

```
⚠️  NON-STANDARD STRUCTURE

This paper has an unusual structure that doesn't fit typical categories.

Characteristics:
- [What you found]
- [What's unusual]

My best guess: [classification]

Please confirm: Is this paper primarily (a) theoretical with formal results, or (b) empirical/qualitative?
```

## Theory vs. Empirical: Key Distinctions

**Theory Paper Characteristics**:
- Goal: Characterize general relationships, prove existence/uniqueness, derive predictions
- Method: Formal mathematical modeling and proofs
- Results: Theorems, propositions, lemmas with proofs
- Contribution: Mathematical insight, theoretical mechanism, formal characterization
- Reader needs: Understand notation, follow logical proofs, grasp mathematical structure

**Empirical Paper Characteristics**:
- Goal: Test hypotheses, estimate effects, establish facts
- Method: Data analysis, statistical estimation, econometric methods
- Results: Regression coefficients, effect sizes, statistical significance
- Contribution: Empirical evidence, causal identification, quantitative findings
- Reader needs: Understand data, methods, and statistical interpretation

**Mixed Papers**:
- Have both theory and empirics
- Classification depends on which is the primary contribution
- If paper would still make a contribution without empirics → theory paper
- If paper would still make a contribution without proofs → empirical paper

## Common Paper Types and Classification

**Definitely Theory Papers**:
- Pure game theory (equilibrium characterization)
- Mechanism design (optimal mechanism derivation)
- General equilibrium theory
- Contract theory
- Auction theory (theoretical)
- Decision theory
- Social choice theory

**Definitely Empirical**:
- Randomized controlled trials
- Difference-in-differences studies
- Regression discontinuity
- Structural estimation
- Reduced-form causal inference
- Natural experiments

**Often Mixed**:
- Structural models (theory derived, then estimated)
- Theoretical predictions + empirical tests
- Models with calibration

## Tips for Accurate Classification

1. **Don't be fooled by equations** - Even empirical papers have equations (regression models). Look for proofs.
2. **Check the contribution** - What does the paper claim as its main contribution?
3. **Look at the conclusion** - Does it summarize theoretical insights or empirical findings?
4. **Check references** - Theory papers cite math/theory journals; empirical papers cite applied/data journals
5. **Read the abstract** - Usually clearly states whether contribution is theoretical or empirical

## What This Tool Does NOT Do

This tool classifies papers but does NOT:
- Edit the paper (use copy-edit-master for that)
- Evaluate the quality of the theory or empirics
- Check mathematical correctness of proofs
- Assess empirical identification strategies

This is purely a classification tool to route to the correct editing workflow.

## Output Format

Provide the structured analysis report as shown in Step 5, ending with a clear recommendation and question to the user about proceeding.

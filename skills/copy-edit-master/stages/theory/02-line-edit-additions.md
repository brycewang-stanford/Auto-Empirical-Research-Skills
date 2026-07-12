# Theory Stage 5: Theory-Specific Line Edit

Final stage of theory paper editing. Applies theory-specific sentence-level improvements AFTER general line editing (Stage 4) is complete.

## Purpose

Apply theory-specific clarity principles and proofreading:
- Triviality test (make reasoning seem simple)
- Scannability principles
- Formalism-intuition balance
- Theory-specific word choice
- Proof readability improvements
- Assumption interpretability
- Theory-specific proofreading (notation, math mode, references)

## Prerequisites

**Stages 1-4 must be complete.** The paper should already have:
- Stage 1: Good general structure (section organization, paragraph flow, transitions)
- Stage 2: Theory-specific structure (4 questions, simple-to-general, theorem presentation)
- Stage 3: Clean technical elements (notation, definitions, proofs, figures)
- Stage 4: General line editing complete (all 7 Strunk & White rules, McCloskey principles)

This stage applies ONLY theory-specific sentence-level refinements.

## Instructions

### PART A: THEORY-SPECIFIC CLARITY PRINCIPLES

These principles come from Thomson and are unique to theory paper writing.

#### Step A1: The "Triviality Test" - Make Reasoning Seem Simple

**Principle 2**: "Resist the temptation to present results with utmost generality, big words, and gory detail. Try to make your reasoning appear simple, even trivial."

**A1a. Why this matters**:
- Making ideas seem simple shows MASTERY, not weakness
- Anyone can make simple ideas complex
- True skill lies in making complex ideas seem simple
- The best theory papers make you think "Why didn't I see that?"

**A1b. Identify "impressive complexity"**:

Look for sentences that seem designed to impress rather than clarify:

**Unnecessarily complex**:
"The correspondence exhibits upper hemicontinuity in the strong topology, ensuring that the limit of any convergent sequence of epsilon-optimal selections remains epsilon-optimal in the limit"

**Simple** (says the same thing):
"The correspondence is upper hemicontinuous, so optimal choices change continuously with parameters"

**A1c. Simplification strategies**:

1. **Replace technical jargon with intuitive descriptions** (when first introducing):
   - "upper hemicontinuous" → "small changes in parameters lead to small changes in optimal choices"
   - Then use technical term after intuition is established

2. **Break complex sentences** into simpler steps:
   - Not: "This, combined with the fact that X and given Y, implies Z"
   - But: "Note that X. Given Y, this implies Z."

3. **Use concrete language**:
   - Not: "The functional exhibits the requisite properties"
   - But: "The function is continuous and strictly increasing"

4. **Explain WHY before HOW**:
   - Before technical proof step, explain what you're trying to show and why the approach works

**A1d. Scan for unnecessarily complex explanations** and simplify.

#### Step A2: Ensure Scannability - "Write So You Won't Have to Be Read"

**Principle 3**: "A well-structured paper is scannable. By leafing through, a reader should easily spot main findings, figure out notation, and locate definitions."

**A2a. Why this matters**:
- Readers DON'T read linearly
- They jump around: Abstract → Main Result → Figures → Skim proofs
- Paper must support non-linear reading

**A2b. Make theorems scannable**:

Each theorem needs THREE visible components:

1. **Informal statement** (before formal statement):
   "We now show that the equilibrium is unique. Intuitively, the strict concavity of payoffs ensures that best responses are single-valued, eliminating multiple equilibria."

2. **Formal statement** (the theorem itself):
   "**Theorem 2** (Uniqueness): Under Assumptions A1-A3, the game has a unique Nash equilibrium."

3. **Interpretation** (after formal statement):
   "This means that regardless of initial beliefs, players always converge to the same equilibrium strategies."

**Check**: Can someone understand what Theorem X says by reading just these three parts?

**A2c. Make notation scannable**:

When introducing notation, use this format:

"Let X denote the set of actions, where each x ∈ X represents a specific choice."

Not just: "Let X be the action set and x ∈ X."

Include brief interpretation so reader can remember without flipping back.

**A2d. Cross-reference heavily**:

Help readers navigate:
- "Recall that X was defined in Definition 2"
- "As shown in Theorem 1..."
- "Using Lemma 3 from the previous section..."
- "This assumption will be relaxed in Section 5"

**A2e. Scan the paper as a reader would**:
- Read Abstract + Introduction + Theorem statements only
- Can you understand the main contribution?
- If NO → improve informal statements and interpretations

#### Step A3: Balance Formalism with Intuition

**A3a. The balance**:
- Pure formalism → inaccessible, readers give up
- Pure intuition → imprecise, not rigorous
- **Best**: Alternate between formal statements and intuitive explanations

**A3b. Pattern to follow**:

```
[Intuitive setup] → [Formal statement] → [Intuitive explanation]
```

Example:
```
[Intuition]: "We expect the equilibrium to be efficient because players can communicate."

[Formal]: "**Proposition 3**: If communication is possible (Assumption C), then the equilibrium outcome is Pareto efficient."

[Interpretation]: "With communication, players coordinate to avoid inefficient outcomes. Specifically, they agree to play strategy profile s*, which no other profile Pareto dominates."
```

**A3c. Review theorem presentations**:
- Do they follow this pattern?
- Is there enough intuition?
- Is formalism balanced with explanation?

#### Step A4: Theory-Specific Word Choice

**A4a. Mathematical writing conventions**:

**Good mathematical prose**:
- "Assume X holds" (not "Suppose X is holding")
- "Let x denote..." (not "Let x be denoting...")
- "We have" (not "We get")
- "This implies" (not "This means" unless interpretation)
- "Define X as..." (not "X is defined to be...")

**A4b. Avoid colloquialisms** in formal statements:
- "The proof boils down to..." → "The proof reduces to..." or "The key step is..."
- "It turns out that..." → "We show that..." or "It follows that..."

**A4c. Be precise about logical connections**:
- "implies" (A → B)
- "follows from" (B follows from A means A → B)
- "if and only if" (A ↔ B)
- "necessary" (B necessary for A means A → B)
- "sufficient" (A sufficient for B means A → B)

Don't mix these up!

#### Step A5: Improve Proof Readability (Sentence-Level)

**A5a. Add signposting within proofs**:

- "To see this, note that..."
- "The result now follows from..."
- "This completes the proof of the claim."
- "We next show that..."
- "It remains to prove that..."

These phrases help readers follow the logical flow.

**A5b. Explain inequality chains**:

**Just symbols**:
```
f(x) ≥ g(x) ≥ h(x) = k(x) ≥ 0
```

**With explanation**:
```
f(x) ≥ g(x)                    [by monotonicity]
     ≥ h(x)                    [by assumption A2]
     = k(x)                    [by definition of k]
     ≥ 0                       [since k is non-negative]
```

**A5c. Use words to connect equations**:

Not just:
```
x = y
y = z
z = w
```

But:
```
By definition, x = y. Since y = z (from Lemma 1), we have x = z. Finally, z = w by assumption.
```

#### Step A6: Improve Assumption Statements

**A6a. Make assumptions interpretable**:

Each assumption should have:
1. **Formal statement** (math)
2. **Economic interpretation** (what it means)
3. **Justification** (why it's reasonable) [optional but helpful]

**Just formal**:
"**Assumption 1**: For all x, y ∈ X, if x ≻ y, then λx + (1-λ)y ≻ y for all λ ∈ (0,1]."

**Complete**:
"**Assumption 1** (Continuity): For all x, y ∈ X, if x ≻ y, then λx + (1-λ)y ≻ y for all λ ∈ (0,1].

**Interpretation**: Preferences are continuous—small changes in outcomes lead to small changes in preferences.

**Justification**: This standard assumption rules out lexicographic preferences and ensures equilibrium existence."

**A6b. Review all assumptions** for interpretability.

### PART B: THEORY-SPECIFIC PROOFREADING

After completing Part A, perform theory-specific proofreading:

#### Step B1: Notation Consistency Check

**B1a. Within-paragraph consistency**:
- Verify same symbol = same meaning throughout each paragraph
- Check that symbols match definitions established earlier in paper

**B1b. Common notation inconsistencies**:
- Using x in one place and X in another for the same object
- Switching between i and j for generic players
- Using θ and Θ inconsistently

**B1c. Track and fix** all notation inconsistencies.

#### Step B2: Math Mode Correctness

**B2a. Check inline math** ($...$):
- Variables should be in math mode: $x$, not x
- Short expressions: $x + y$, not x + y

**B2b. Check display math** ($$...$$ or \[...\]):
- Equations that need emphasis
- Long expressions
- Numbered equations for referencing

**B2c. Common errors**:
- Missing math mode: "player i's payoff ui(x)" → "$u_i(x)$"
- Inconsistent formatting: sometimes "payoff u" sometimes "$u$"
- Punctuation: equations should have proper punctuation

#### Step B3: Theorem Reference Completeness

**B3a. Check theorem/lemma references**:
- "the theorem" → "Theorem 1"
- "our main result" → "Theorem 2"
- All references should be specific and correct

**B3b. Check equation number references**:
- Verify "(1)" refers to the correct equation
- Check cross-references are accurate

**B3c. Check proof markers**:
- Every theorem/proposition/lemma has a corresponding proof
- All proofs end with proper marker (∎ or QED)

### PART C: CALCULATE AND REPORT

#### Step C1: Calculate Statistics

```
THEORY-SPECIFIC LINE EDIT STATISTICS

Theory Clarity Improvements:
- Triviality test applications: [count] (complex → simple)
- Scannability improvements: [count]
- Formalism-intuition balance: [count]
- Theory word choice fixes: [count]
- Proof readability enhancements: [count]
- Assumption interpretability: [count]

Theory-Specific Proofreading:
- Notation consistency fixes: [count]
- Math mode corrections: [count]
- Reference completeness fixes: [count]

Total theory-specific improvements: [sum]
```

## What This Stage Does NOT Do

**Already handled by Stage 4 (General Line Edit)**:
- Strunk & White's 7 rules (omit needless words, active voice, etc.)
- McCloskey's principles (word choice, tense, subject consistency, rhythm)
- General proofreading (grammar, punctuation, spelling)
- Parallelism and emphasis

**Already handled by earlier stages**:
- Structure (Stages 1 & 2)
- Technical elements (Stage 3): Notation design, definition structure, proof organization, figure quality

This stage applies ONLY theory-specific sentence-level refinements.

## Example: Before and After Theory Line Edit

**BEFORE** (Complex and hard to scan):

```
Theorem 1: Under the conditions specified in Assumptions 1-4, it can be shown that there
exists a unique equilibrium in which the strategies exhibit the following property: for
each player i, the strategy is characterized by a threshold θᵢ such that action a is
chosen if and only if the parameter exceeds θᵢ, and moreover, it is not the case that
multiple equilibria can coexist.
```

**AFTER** (Simple and scannable):

```
We now establish that the equilibrium is unique and has a threshold structure.

**Theorem 1** (Unique Threshold Equilibrium): Under Assumptions 1-4, the game has a unique
Nash equilibrium. In this equilibrium, each player i uses a threshold strategy: player i
chooses action a if and only if their parameter exceeds threshold θᵢ.

**Interpretation**: Players follow simple cutoff rules. Those with high parameter values
(above θᵢ) choose a; those with low values choose b. The thresholds are uniquely determined
by the model parameters.
```

**Changes**:
- Added informal statement before theorem (scannability)
- Simplified formal statement (triviality test)
- Converted negative ("not the case that multiple") to positive ("unique")
- Added interpretation after theorem (formalism-intuition balance)
- Made scannable (can understand by reading just this, without previous text)

## Output Format

At the end of Theory Stage 5, provide:
1. Statistics summary (as shown in Step C1)
2. The fully edited document
3. Selected before/after examples showing theory-specific improvements
4. Confirmation that manuscript is ready for submission

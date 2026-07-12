# Theory Stage 2: Technical Elements

Second stage of the 4-stage theory paper editing process. Focuses on the technical quality of notation, definitions, proofs, and figures.

## Purpose

Systematically improve:
- **Notation**: Conventional, mnemonic, minimal, pronounceable
- **Definitions**: Signaled, complete, with examples
- **Proofs**: Structured, clear, assumption-specific
- **Figures**: Labeled, purposeful, integrated with text

## Instructions

### PART A: NOTATION REVIEW

The goal: **Make notation guessable**. Best notation has meaning that can be inferred without constantly flipping back to definitions.

#### Step A1: Check for Conventional Notation

**Rule 1**: Follow field conventions.

**A1a. Identify notation used**:
- List all symbols introduced
- Check if they follow standard conventions for the field

**A1b. Check against conventions**:

| Object | Standard | Non-standard (avoid) |
|--------|----------|---------------------|
| Price | p, P | z, w, x |
| Quantity | q, x | a, b, c |
| Utility | u, U, v, V | f, g |
| Endowment | ω, e | k, m |
| Agent/Player | i, j, k | a, b, c |
| Time | t, τ | i, j |
| Production set | Y, T | F, G |
| Probability | π, p | q, r |
| Discount factor | δ, β | d, b |

**A1c. Flag non-standard notation**:
- Is there a reason for non-standard choice?
- If no good reason, suggest conventional symbol

#### Step A2: Check for Mnemonic Names

**Rule 2**: Names should suggest their content.

**A2a. Assumptions and properties**:

❌ **Non-mnemonic** (reader must flip back):
- "Assumption A1, A2, A3"
- "Property P1, P2"
- "Condition C1, C2"

✅ **Mnemonic** (reader can remember):
- "Continuity (Cont), Monotonicity (Mon), Convexity (Conv)"
- "Submodularity (Sub), Supermodularity (Super)"
- "No Veto Power (NVP), Strong No Veto (SNV)"

Benefits:
- In proofs, you write "By Monotonicity and Convexity..." (instantly clear)
- Not "By A2 and A5..." (reader must flip back)

**A2b. Review all named items**:
- List all assumptions, properties, conditions
- Are they mnemonic?
- If not, suggest mnemonic names

**A2c. Check axioms**:
- If axioms have standard names in the literature, use them
- "Weak Axiom of Revealed Preference (WARP)" not "Axiom 1"

#### Step A3: Check for Minimalism

**Rule 3**: Every symbol is a burden on the reader.

**A3a. Identify under-used notation**:
- Find symbols used only once or twice
- Ask: Could this be written in words instead?

**A3b. Apply the test**:
Before introducing symbol X:
1. Will I use this more than twice?
2. Can I write it in words just as easily?
3. Does it simplify or complicate?

**A3c. Suggest eliminations**:

❌ **Over-notation**:
"Let Δ denote the set of all probability distributions over A. Let μ ∈ Δ."
[If μ is used only in one theorem]

✅ **Simpler**:
"Let μ be a probability distribution over A."

**A3d. Check for "symbol-salad"**:
- Expressions with too many subscripts, superscripts, primes
- Example: x_{i,t}^{k,*}(θ^{-j}_t | s_{-i,t-1})
- Can this be simplified?

#### Step A4: Check Pronounceability

**Rule 4**: Notation must be pronounceable for seminars.

**A4a. Test pronunciation**:
- You'll write this on a blackboard and say it aloud
- Can you naturally pronounce it?
- Will audience distinguish it from similar symbols?

**A4b. Problematic symbols**:
- Too many primes: x, x', x'', x''' (say "x prime prime prime"?)
- Similar-looking: v vs. ν, p vs. ρ, u vs. υ
- Complex subscripts: hard to say "x sub i comma t super k star"

**A4c. Suggest improvements**:
- Use different symbols instead of many primes
- Choose visually distinct symbols

#### Step A5: Check Hierarchy

**Rule 5**: Use visual cues (case, font) to show relationships.

**A5a. Check element-set-family hierarchy**:

✅ **Good hierarchy** (visually intuitive):
- Element: x (lowercase)
- Set: X (uppercase)
- Family of sets: 𝒳 (calligraphic)
- Expression: x ∈ X ∈ 𝒳 (instantly clear)

❌ **Poor hierarchy** (confusing):
- Element: x, Set: Y, Family: Z (no visual relationship)

**A5b. Check consistency**:
- If X is a set, is x its element (not y or z)?
- If using hierarchy, is it consistent throughout?

#### Step A6: Check for Cluttered Expressions

**Rule 6**: Seek elegance and simplicity.

**A6a. Identify cluttered sums/products**:

❌ **Cluttered**:
∑_{i=1}^{n} x_i (when index is obvious from context)

✅ **Clean**:
∑ x_i (or ∑_i x_i if needed)

**A6b. Check notation for partitions**:

❌ **Cluttered**:
O_{N\{i}} or O_{-\{i\}}

✅ **Standard**:
O_{-i} (standard in game theory for "all agents except i")

**A6c. Apply elegance test**:
- Does notation look clean on the page?
- Or does it look like "symbol-salad"?

#### Step A7: Summarize Notation Issues

```
🔤 NOTATION REVIEW SUMMARY

Conventions:
- Non-standard symbols: [count]
  [List: "Using 'z' for price → recommend 'p'"]

Mnemonics:
- Non-mnemonic names: [count]
  [List: "Assumption A1 → recommend 'Continuity (Cont)'"]

Minimalism:
- Under-used symbols: [count]
  [List: "Symbol X used once → recommend writing in words"]

Pronounceability:
- Difficult-to-pronounce: [count]
  [List examples]

Hierarchy:
- Hierarchy violations: [count]
  [List cases where element-set relationship is unclear]

Clutter:
- Cluttered expressions: [count]
  [List: "∑_{i=1}^{n} → simplify to ∑_i"]

Recommendation: [Implement changes / Minor issues only / Notation is good]
```

### PART B: DEFINITIONS REVIEW

The role: **Definitions must be unambiguous, complete, and easily found**.

#### Step B1: Check Definition Signaling

**Rule 1**: Signal new terms clearly.

**B1a. Scan for defined terms**:
- Are they in **boldface**?
- Are they easy to locate?

**B1b. Standard formats**:

✅ **Good signaling**:
"A function f is **monotone** if for all x > y, we have f(x) > f(y)."

✅ **Alternative** (for central concepts):
"**Definition 1**: A function f is said to be **monotone** if..."

❌ **Poor signaling**:
"A function f is monotone if..." (no boldface - hard to find)

**B1c. Check all definitions**:
- List all defined terms
- Are they signaled with boldface or formal "Definition X:" format?
- If not, mark for revision

#### Step B2: Check for Illustrative Examples

**Rule 2**: Provide the FOUR crucial types of examples.

For each non-trivial definition, check if examples show objects that:

1. **Satisfy the definition** (standard case)
2. **Do not satisfy the definition** (clear violation)
3. **Satisfy but almost do not** (boundary case)
4. **Do not satisfy but almost do** (boundary case)

**B2a. Why boundary cases matter**:
- "Boundary cases are responsible for three-fourths of the work in proofs"
- They reveal where definition really "bites"

**B2b. Example** - Convex sets:

1. ✓ Satisfies: Standard convex set (disk, triangle)
2. ✓ Does not satisfy: Non-convex set (crescent moon)
3. ✓ Boundary: Convex set with point missing from edge (convex interior, but definition may require closure)
4. ✓ Boundary: Almost-convex set (tiny concave dent)

**B2c. Review each definition**:
- Does it have examples?
- Does it have boundary case examples?
- If not, mark for addition

#### Step B3: Check Logical Order

**Rule 3**: Define in logical order.

**B3a. The principle**:
- State the space before objects that live in it
- Introduce terms so each involves only previously defined terms

**B3b. Check definition order**:

❌ **Wrong order**:
```
Define function F: X → Y
[later] Define set X
```

✅ **Right order**:
```
Define set X
Define function F: X → Y
```

**B3c. Identify out-of-order definitions**:
- List all definitions in order of appearance
- Check if any use terms defined later
- Mark for reordering

#### Step B4: Check for Grouped Definitions

**Rule 4**: Factor out common elements when defining related concepts.

**B4a. Identify related definitions**:
- Are there multiple definitions with common structure?
- Example: Different types of equilibria, various continuity notions

**B4b. Check if properly factored**:

❌ **Repetitive**:
```
- A function is continuous if [full definition]
- A function is uniformly continuous if [repeats common parts + addition]
- A function is Lipschitz continuous if [repeats common parts + addition]
```

✅ **Factored**:
```
A function f: X → Y is:
- **continuous** if [definition]
- **uniformly continuous** if continuous and [additional condition]
- **Lipschitz continuous** if continuous with [additional condition]
```

Benefits: Highlights the differences, reduces repetition

**B4c. Suggest grouping** where appropriate.

#### Step B5: Check Formal vs. Interpretation Separation

**Rule 5**: Separate formal definition from economic interpretation.

**B5a. The structure**:

✅ **Good separation**:
```
**Definition**: [Pure mathematical definition]

**Interpretation**: [Economic meaning and intuition]
```

Benefits:
- Keeps model general
- Mathematical definition is precise
- Economic interpretation aids understanding
- Allows for multiple interpretations/applications

**B5b. Check current definitions**:
- Are they pure math, or mixed with interpretation?
- If mixed, suggest separation

**B5c. Example**:

❌ **Mixed**:
"A strategy profile is a Nash equilibrium if no firm wants to deviate to increase profits"
[Too specific - what if not firms? what if not profits?]

✅ **Separated**:
"**Definition**: A strategy profile s* is a **Nash equilibrium** if for all i and all s_i, we have u_i(s*) ≥ u_i(s_i, s*_{-i}).

**Interpretation**: No player can increase their payoff by unilaterally deviating. In our model, this means no firm wants to change its price given other firms' prices."

#### Step B6: Check for Collapsed Statements

**Rule 6**: Don't collapse similar statements into one confusing sentence.

**B6a. Identify collapsed definitions**:

❌ **Collapsed** (confusing):
"The function f is decreasing (increasing; non-decreasing) if for all x > y..."

Reader must parse parentheticals and figure out which parts flip.

✅ **Expanded** (clear):
"The function f is:
- **decreasing** if for all x > y, f(x) < f(y)
- **increasing** if for all x > y, f(x) > f(y)
- **non-decreasing** if for all x > y, f(x) ≤ f(y)"

**B6b. Principle**: "Space is cheap. Reader attention is expensive."

**B6c. Check definitions**:
- Any with parenthetical variations?
- Mark for expansion

#### Step B7: Summarize Definition Issues

```
📐 DEFINITIONS REVIEW SUMMARY

Signaling:
- Undefined terms (no boldface): [count]
  [List terms that need boldface]

Examples:
- Definitions lacking examples: [count]
- Missing boundary cases: [count]
  [List which definitions need examples]

Logical Order:
- Out-of-order definitions: [count]
  [List: "Function F defined before domain X"]

Grouping:
- Related definitions to group: [count]
  [List opportunities for factoring]

Separation:
- Mixed formal/interpretation: [count]
  [List definitions to separate]

Collapsed Statements:
- Collapsed definitions: [count]
  [List definitions to expand]

Recommendation: [Implement changes / Minor issues / Definitions are good]
```

### PART C: PROOFS REVIEW

A proof is an ARGUMENT, not code. Blend mathematics with English.

#### Step C1: Check Proof Structure

**Rule 1**: Long proofs must be broken into clearly labeled parts.

**C1a. Identify long proofs**:
- Any proof >1 page should be structured
- Any proof with multiple logical steps needs labels

**C1b. Check for structure labels**:

✅ **Good structure**:
```
**Proof of Theorem 1:**

**Step 1** (Existence): We show that...
[proof of existence]

**Step 2** (Uniqueness): Suppose there exist two equilibria...
[proof of uniqueness]

**Step 3** (Characterization): The equilibrium satisfies...
[characterization]

This completes the proof. ∎
```

❌ **Wall of text**:
```
**Proof:** First note that ... then observe... moreover... furthermore... additionally... thus...
[20 lines of unstructured text]
∎
```

**C1c. Alternative labels**:
- **Case 1, Case 2** (for case analysis)
- **Claim 1, Claim 2** (for intermediate claims)
- Use whatever fits the proof logic

**C1d. Mark unstructured proofs** for revision.

#### Step C2: Check Hypothesis Gathering

**Rule 2**: All conditions required should be stated upfront.

**C2a. Check proof openings**:

❌ **Scattered hypotheses**:
"Proof: If A and B, then D since C also holds"
[Reader learns condition C only at the end]

✅ **Gathered hypotheses**:
"Proof: Assume A, B, and C. Then..."
[Reader sees complete foundation before implications]

**C2b. Scan proofs**:
- Do they state all needed conditions upfront?
- Or introduce conditions mid-proof?
- Mark for revision

#### Step C3: Check Assumption Specificity

**Rule 3**: Be specific about which assumptions are used.

**C3a. Scan for vague references**:

❌ **Vague**:
- "By the assumptions..."
- "By assumption..."
- "From our hypotheses..."

✅ **Specific**:
- "By Monotonicity (Mon)..."
- "Because preferences are complete (part (i) of Assumption 1)..."
- "The correspondence is non-empty by Continuity (Cont)"

**C3b. Why this matters**:
- Reader immediately knows which assumption is used
- No need to flip back
- Clear which assumptions are crucial

**C3c. Mark vague references** for specific citation.

#### Step C4: Check Independence of Hypotheses

**Rule 4**: Verify that all stated hypotheses are actually used.

**C4a. After proof is complete**:
- List all hypotheses/assumptions stated in theorem
- Check: Was each one used in the proof?

**C4b. If an assumption was never used**:

Two possibilities:
1. **You made a mistake** - the proof is incomplete
2. **You have a stronger result** - the theorem holds under weaker conditions

**C4c. The test**:
- Can you construct a counterexample when assumption X is dropped?
- If YES → assumption is necessary
- If NO → theorem is stronger than stated, or proof is incomplete

**C4d. Mark stranded assumptions** for investigation.

#### Step C5: Check Proof Completeness

**Rule 5**: Don't leave too many steps to the reader.

**C5a. Distinguish logical steps from calculations**:

✅ **OK to omit**: "Routine algebraic simplification yields..."
[If it's truly routine algebra]

❌ **NOT OK to omit**: "The remainder is tedious but straightforward and left to the reader"
[If it contains logical steps, not just algebra]

**C5b. The principle**:
- A proof is not a homework problem
- Reader must follow the LOGIC without doing calculations
- Put routine algebra in appendix if needed, but state logical conclusions

**C5c. Check for gaps**:
- Are there steps that require significant work?
- Are they presented or left to reader?
- Mark gaps for filling or moving to appendix with summary in main text

#### Step C6: Check Quantifier Handling

**Rule 6**: Handle quantifiers with care.

**C6a. Avoid "for any"** (ambiguous):
- Does "for any x" mean "for all x" or "for some x"?
- In English, "any" can mean either!

✅ **Use**: "for all x" or "for every x" (universal)
✅ **Use**: "for some x" or "there exists x" (existential)
❌ **Avoid**: "for any x" (ambiguous)

**C6b. Don't mix symbols in English sentences**:

❌ "∀x ∈ X, the function satisfies..."
✅ "For all x ∈ X, the function satisfies..."

**C6c. Avoid double quantification of same variable**:

❌ "For all x, there exists x such that..."
[Same variable x used twice]

✅ "For all x, there exists y such that..."

**C6d. Scan proofs for quantifier issues** and mark for fix.

#### Step C7: Check Proof Endings

**Rule 7**: Show clearly where proof ends.

**C7a. Check for end markers**:

✅ **Good endings**:
- ∎ (Halmos/tombstone - modern standard)
- QED (traditional)
- "This completes the proof." (for very long proofs)

❌ **No ending**:
- Proof just trails off
- Reader unsure if more is coming

**C7b. For multi-page proofs**:
Use explicit ending: "This completes the proof of Theorem 2. ∎"

**C7c. Ensure all proofs have clear endings**.

#### Step C8: Check Math-to-English Ratio

**C8a. The optimal balance**:
- Too much math (>80%) → code, not argument
- Too many words (<40% math) → imprecise, lacks rigor
- **Optimal: 50-65% mathematics, 35-50% English prose**

**C8b. Estimate ratio** for main proofs:
- Count lines of pure math vs. explanatory text
- Is it balanced?

**C8c. If too much math**:
- Add explanatory sentences
- "This inequality holds because..."
- "The first term represents..."

**C8d. If too many words**:
- Formalize vague arguments
- Use precise mathematical statements

#### Step C9: Summarize Proof Issues

```
⚖️ PROOFS REVIEW SUMMARY

Structure:
- Unstructured long proofs: [count]
  [List: "Proof of Theorem 2 needs Step labels"]

Hypotheses:
- Scattered hypotheses: [count]
- Vague assumption references: [count]
  [List: "'By assumptions' → specify which"]
- Unused assumptions: [count]
  [List: "Assumption X never used in Theorem Y"]

Completeness:
- Significant gaps left to reader: [count]
  [List proofs with gaps]

Quantifiers:
- "For any" ambiguities: [count]
- Symbol mixing: [count]

Endings:
- Proofs without clear endings: [count]

Math-English Ratio:
- Proofs needing more explanation: [count]
- Proofs needing more formalism: [count]

Recommendation: [Implement changes / Minor issues / Proofs are good]
```

### PART D: FIGURES REVIEW

"A picture can cut understanding time by half" - Your paper should crawl with diagrams.

#### Step D1: Check Figure Quantity

**D1a. Count figures**:
- How many figures in paper?
- How many pages per figure?

**D1b. Guidelines**:
- Aim for ~1 figure per 3-5 pages (at minimum)
- More is better for theory papers
- If <3 figures total → likely need more

**D1c. Identify opportunities**:
Where could figures help?
- Illustrating definitions (convex vs. non-convex sets)
- Priming intuition before proofs (geometric intuition)
- Showing counterexamples
- Breaking up dense text

#### Step D2: Check Figure Labeling

**Rule 1**: Label figures completely - they must be self-contained.

**D2a. Check each figure for**:
- ✓ Descriptive caption
- ✓ Labeled axes
- ✓ Labeled curves/lines/regions
- ✓ Labeled points of interest
- ✓ Legend (if multiple elements)

**D2b. The principle**:
"Label all objects in a figure unless there is a very good reason not to"

**D2c. Review each figure**:
- List figures with missing labels
- Note what needs to be added

**Example of complete labeling**:
```
Figure 1: Best-Response Functions in Price Competition

[Figure shows two curves intersecting]
- Horizontal axis: "Firm 1's price (p₁)"
- Vertical axis: "Firm 2's price (p₂)"
- Curve 1 labeled: "BR₁(p₂)" (Firm 1's best response)
- Curve 2 labeled: "BR₂(p₁)" (Firm 2's best response)
- Intersection point labeled: "Nash Equilibrium (p₁*, p₂*)"
```

#### Step D3: Check Figure Quality

**Rule 2**: Draw with care and purpose.

**D3a. Check geometric accuracy**:
- Does geometry reflect the economics?
- Indifference curves: Right curvature?
- Budget constraints: Correct slopes?
- Best-response functions: Plausible shapes?

**D3b. Check visual choices**:
- Solid lines for fundamentals (payoff functions, constraints)
- Dotted lines for constructions (projections, extensions)
- Dashed lines for alternative cases
- Shading for sets/regions
- Arrows for movement/direction

**D3c. Check scale**:
- Is figure drawn to reasonable scale?
- Are important features visible?
- Not too cluttered?

#### Step D4: Check Text Integration

**Rule 3**: Refer to figures in the text.

**D4a. Check references**:
- Is each figure mentioned in the text?
- Not enough to just include it - must guide reader's eye

✅ **Good references**:
- "As shown in Figure 2, the best-response function is upward-sloping..."
- "Figure 3 illustrates why the equilibrium is unique"
- "The shaded region in Figure 1 represents the set of Pareto-efficient allocations"

❌ **No references**:
- Figure appears but text never mentions it
- Reader doesn't know what to look for

**D4b. Mark unreferenced figures** for text integration.

#### Step D5: Summarize Figure Issues

```
📊 FIGURES REVIEW SUMMARY

Quantity:
- Current figures: [count]
- Pages per figure: [N]
- Recommendation: [Add X more figures / Quantity is adequate]

Opportunities for new figures:
- [List: "Add figure showing convex vs. non-convex preferences"]
- [List: "Add geometric intuition before Theorem 2 proof"]

Labeling:
- Figures with incomplete labels: [count]
  [List: "Figure 2 needs axis labels"]
  [List: "Figure 4 needs curve labels"]

Quality:
- Figures needing improvement: [count]
  [List: "Figure 1 indifference curves have wrong curvature"]

Text Integration:
- Unreferenced figures: [count]
  [List: "Figure 3 not mentioned in text"]

Recommendation: [Add figures and improve labeling / Minor improvements / Figures are good]
```

### Step 11: Overall Technical Elements Summary

```
🔧 TECHNICAL ELEMENTS REVIEW COMPLETE

📋 NOTATION (Part A):
Issues found: [count]
[Top 3 issues summarized]

📋 DEFINITIONS (Part B):
Issues found: [count]
[Top 3 issues summarized]

📋 PROOFS (Part C):
Issues found: [count]
[Top 3 issues summarized]

📋 FIGURES (Part D):
Issues found: [count]
[Top 3 issues summarized]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OVERALL ASSESSMENT: [Significant improvements needed / Moderate improvements / Minor polish only]

PRIORITY ISSUES (address first):
1. [Most critical issue]
2. [Second most critical]
3. [Third most critical]

Next stage: Theory Stage 3 (Line Edit - sentence-level improvements)
```

## Principles Applied

This stage applies Thomson's detailed technical rules:
- Notation: 6 rules (conventional, mnemonic, minimal, pronounceable, hierarchical, uncluttered)
- Definitions: 6 rules (signaling, examples, order, grouping, separation, no collapsing)
- Proofs: 7 rules (structure, hypotheses, specificity, independence, completeness, quantifiers, endings)
- Figures: 3 rules (complete labeling, purposeful drawing, text integration)

## What This Stage Does NOT Cover

**Paper structure**: Introduction, literature, conclusion → Theory Stage 1 (already done)

**Sentence-level writing**: Wordiness, voice, clarity → Theory Stage 3 (next)

**Grammar/punctuation**: Mechanical errors → Theory Stage 4 (final)

This stage is TECHNICAL ELEMENTS only.

## Output Format

At the end of Theory Stage 2, provide:
1. Overall technical elements summary (as shown in Step 11)
2. The technically edited document
3. Note that Theory Stage 3 (Line Edit) is next

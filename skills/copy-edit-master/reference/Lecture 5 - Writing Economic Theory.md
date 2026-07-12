---
marp: true
theme: default
paginate: true
header: 'Academic Writing in English'
footer: 'Lecture 5: Writing Economic Theory | Sun Yat-sen University'
style: |
  section, h1, h2, h3, h4, h5, h6, p, li {
    font-family: inherit, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif !important;
  }
  blockquote {
    color: #0066cc;
    border-left: 4px solid #0066cc;
    padding-left: 1rem;
    margin: 1rem 0;
    background-color: transparent;
  }
  blockquote p {
    color: #0066cc;
    margin: 0;
  }
---

# Lecture 5: Writing Economic Theory

## A Guide for the Young Economist

### *Based on the principles of William Thomson*

---

## Today's Roadmap: Thomson's Way

*   **Part 1: General Principles** (The Philosophy)
*   **Part 2: Notation** (The Language of Theory)
*   **Part 3: Definitions** (The Building Blocks)
*   **Part 4: Proofs** (The Argument)
*   **Part 5: Pictures** (The Intuition)
*   **Part 6: Paper Architecture** (Structuring the Whole)

---

## Part 1: General Principles

### The Philosophy of Clear Theoretical Writing

---

### The Unspoken Contract

When you write a theory paper, you enter a contract with the reader.

**Your Obligation:**

*   To present your ideas with absolute clarity.
*   To respect the reader's time and intelligence.
*   To guide them through your logic, not to impress them with complexity.

**The Reader's Obligation:**

*   To engage with your ideas thoughtfully.

Your writing style determines whether you uphold your end of the bargain.

---

### Principle 1: Clarity is the Main Goal

> Your principal objective is **clarity**. No one will read very far into a paper if it is a burden. Make your paper inviting and convey your message efficiently.

This means every choice—of notation, of structure, of wording—must serve the goal of making your ideas easier to understand.

---

### Application: Make Your Reasoning Seem Simple

> When arguing for the significance of your results, great is the temptation to present them with the utmost generality, with big words and in gory detail. Resist it! Try instead to make your reasoning appear simple, even trivial.

**This shows mastery, not weakness.**

Anyone can make a simple idea complex. True skill lies in making a complex idea seem simple.

---

### Application: The "Triviality" Test

**Before:**

> "Leveraging a high-dimensional application of the Brouwer fixed-point theorem on the product space of strategy profiles, we establish the existence of a Nash equilibrium."

**After:**

> "An equilibrium exists because each player's best response is a continuous function on a compact set. The result follows from a standard fixed-point argument."

The second version builds intuition and makes the result feel natural and expected.

---

### Principle 2: Write So You Won't *Have* to Be Read

> By leafing through the article, a reader should be able to spot easily your main findings, figure out most of the notation, and locate the crucial definitions needed to understand each formal result.

A well-structured paper is **scannable**.

---

### How Do Readers *Actually* Read?

They do not read linearly from page 1 to 40. They jump around.

1.  Read the **Abstract** and **Introduction**.
2.  Jump to the **Main Result** (Theorem 1).
3.  Scan for the **Definitions** needed to understand the theorem.
4.  Look at the **Figures** to get the intuition.
5.  Glance at the **Conclusion**.
6.  *Maybe* read the proof if the result is surprising or crucial.

Your job is to make this process frictionless.

---

### Application: Scannable Structure

**Poor Structure:**

*   Definitions buried in paragraphs.
*   Theorems not clearly labeled.
*   Notation is dense and unexplained.
*   No figures.
*   Main result is hidden on page 25.

**Good Structure:**

*   Definitions are in **bold** and clearly formatted.
*   Theorems are labeled **Theorem 1**, **Theorem 2**.
*   Notation is introduced in a dedicated, easy-to-find section.
*   Figures are used to illustrate key mechanisms.
*   Main result is stated clearly in the introduction.

---

### Principle 3: Don't Forget Your Discovery Process

> You arrived at your main theorem in small steps—by first working it out for two agents, two goods, and linear technologies, with no uncertainty and by drawing lots of diagrams. It is also by looking at simple versions of your model that your reader will understand the central ideas.

**Don't hide the ladder you used to climb to your result.**

---

### Application: Guide the Reader Up the Ladder

**Your Discovery Path:**

1.  Started with a 2x2 game.
2.  Found the result for that simple case.
3.  Tried a 3x3 game; it still held.
4.  Conjectured the general `n x m` result.
5.  Proved it.

**Your Paper's Structure:**

1.  **Section 3.1:** The 2x2 Case. Provide the full analysis and intuition.
2.  **Section 3.2:** The General Result. State the main theorem for `n x m` games.
3.  **Proof:** Show how the logic from the 2x2 case extends.

This builds intuition from the ground up, just like you did.

---

### Principle 4: Don't Forget Your Errors

> There is nothing like having misunderstood something to really understand it... You cannot claim to understand something completely until you very thoroughly understand the various ways in which it can be misunderstood.

Your own past confusion is a powerful teaching tool.

---

### Application: Anticipate Reader Misunderstandings

Think about what confused *you*:

*   Did you initially think single-peakedness required symmetry? **Clarify that it doesn't.**
*   Did you struggle with the difference between `upper hemicontinuity` and `lower hemicontinuity`? **Add a footnote or a remark explaining the difference with an example.**
*   Did you misinterpret what "contraction independence" means? **Explain it carefully.**

Your readers are smart, but they are human. They will fall into the same traps you did. Pave over those traps with clear explanations.

---

### Principle 5: Tell a Story, Don't Enumerate

A literature review should create a narrative that culminates in your paper solving a puzzle.

**Boring Enumeration (A List):**

> Author 1 (1985) shows X. Author 2 (1992) shows Y. Author 3 (2004) shows Z. In this paper, we extend these results by showing A.

**Compelling Narrative (A Story):**

> The literature began by establishing X (Author 1, 1985). This led naturally to the question of whether Y was true. Author 2 (1992) provided a negative answer in a general setting, but the question remained open for the important special case of Z, which Author 3 (2004) resolved. This leaves open the final piece of the puzzle: what happens when...? Our paper resolves this question.

---

## Part 2: Notation

### The Language of Economic Theory

---

### The Goal: Make Notation Guessed

> The best notation is notation whose meaning can be guessed. After working on your paper for several months, you have no problem remembering what all your variables designate. Unfortunately, what you call `x` is what your reader has been calling `m` since graduate school.

Good notation is a courtesy to the reader. It minimizes cognitive load and makes your arguments transparent.

---

### Rule 1: Follow Convention

Your field has a set of shared traditions. Use them.

| Concept | Standard Symbol | Common Alternatives | Don't Use |
| :--- | :---: | :---: | :---: |
| Prices | `p` | `π` (esp. for inflation) | `z`, `x`, `w` |
| Quantities | `q`, `x` | `y` (for output) | `a`, `b`, `c` |
| Utility | `uᵢ`, `vᵢ` | `U` (for aggregate) | `fᵢ`, `gᵢ`, `hᵢ` |
| Endowments | `ωᵢ`, `eᵢ` | | `x⁰`, `w₀` |
| Agent | `i`, `j` | `h` (household) | `n`, `a`, `p` |
| Production Set | `Y` | `T` (technology) | `P`, `F` |

Using `p` for prices is instantly recognizable. Using `z` forces the reader to stop, learn your new language, and translate.

---

### Example: Good vs. Bad Notation

**Confusing (Non-Standard):**

> Let `z₁` denote the price vector and `z₂` denote the allocation. Agent `i`'s preferences are given by the function `hᵢ(z₁, z₂)`.

*Reader's internal monologue: "Wait, `z₁` is price? Why not `p`? Is there a reason? Is `h` utility? This is work."*

**Clear (Standard):**

> Let `p` be the price vector and `x` be the allocation. Agent `i`'s preferences are represented by the utility function `uᵢ(p, x)`.

*Reader's internal monologue: "Okay, standard setup. Prices, allocation, utility. Got it. Next."

---

### Rule 2: Be Mnemonic

Name your assumptions and properties in a way that suggests their content.

**Bad (Numbered Labels):**

> **Assumption A1:** Preferences are continuous.

> **Assumption A2:** Preferences are monotonic.

> **Assumption A3:** Preferences are convex.

In the proof: "By A1 and A3..." -> Reader forgets what A1 and A3 are and has to flip back, breaking their concentration.

---

### Example: Mnemonic Labels

**Good (Named Labels):**

> **Continuity (Cont):** Preferences are continuous.

> **Monotonicity (Mon):** Preferences are monotonic.

> **Convexity (Conv):** Preferences are convex.

In the proof: "By **Continuity** and **Convexity**..." -> The reader understands immediately without checking.

> The cost to you is a mere keystroke, but it will save readers from a backward search for the property you mean.

---

### Rule 3: Be Minimalistic

> Every symbol is a burden on the reader. Imagine that you are on a diet and that each symbol is worth one calorie. You will quickly discover that you can do with half as many.

**Before introducing a new symbol, ask:**

1.  Will I use this more than twice?

2.  Can I write it out in words just as easily?

3.  Does it simplify or complicate the expression?

If a symbol is never used, it is not needed.

---

### Example: Unnecessary Notation

**Overly Complicated:**

> Let `uᵢ(φᵢ(R, Ω))` be the utility of agent `i` under allocation rule `φ` for preference profile `R` and endowment `Ω`. The rule is resource-monotonic if `uᵢ(φᵢ(R, Ω')) ≥ uᵢ(φᵢ(R, Ω))` when `Ω' > Ω`.

**Simpler (No Utility Function):**

> The rule is resource-monotonic if `φᵢ(R, Ω') Rᵢ φᵢ(R, Ω)` when `Ω' > Ω`.

If you only need the ordinal properties, don't introduce cardinal utility functions. It clutters the text and can even be misleading (tempting readers to compare utility levels).

---

### Rule 4: Make Notation Pronounceable & Writable

You will have to present this work in a seminar. You will have to write it on a blackboard.

*   How do you pronounce `ℵ` or `ξ`'?

*   Can you easily distinguish `ρ` and `p` on a worn-out blackboard?

*   How do you say `x ⪰ᵢ y` out loud?

Choose symbols that are easy to say ("x is preferred to y") and easy to write. Avoid capitalized script letters (`ℋ`, `ℱ`) which are hard to draw.

---

### Rule 5: Respect the Hierarchy

Use visual cues like case and font to show relationships.

*   **Element:** `x` (lowercase letter)

*   **Set:** `X` (uppercase letter)

*   **Family of Sets:** `𝒳` (calligraphic letter)

The expression `x ∈ X ∈ 𝒳` is visually intuitive. An element is in a set, which is in a family of sets. It's like a Russian doll. This simple convention reduces cognitive load.

---

### Rule 6: Use Uncluttered Expressions

Avoid "symbol-salad". Seek elegance and simplicity.

**Cluttered:**

`∑ᵢ₌₁ⁿ xᵢ`

`Fᴺ(S, d)`

`O_{N\{i}}`

**Uncluttered:**

`∑ xᵢ` (if the index is obvious)

`N(S)` (if `d` is normalized)

`O_{-i}` (standard and clean)

Search for these small simplifications. They add up to a much cleaner paper.

---

### Self-Audit: Your Notation

1.  **Conventional?** Could a grad student in your field guess what your symbols mean?

2.  **Mnemonic?** Do your assumption labels (A1, A2) mean anything?

3.  **Minimalist?** Have you introduced symbols you only use once?

4.  **Pronounceable?** Could you explain your main theorem over the phone?

5.  **Hierarchical?** Does your notation visually represent containment (`x ∈ X`)?

---

---

## Part 3: Definitions

### The Building Blocks of Your Theory

---

### The Role of a Definition

A good definition is a contract with your reader. It must be:

*   **Unambiguous:** Having one and only one possible meaning.

*   **Complete:** Covering all relevant cases.

*   **Clearly Marked:** Easy to find and reference.

> Define the terms you use, even those that you can legitimately assume everyone has already seen. There is rarely complete agreement on definitions in the literature.

Even terms like `core` or `incentive compatibility` can have subtle variations across papers. State *your* definition clearly.

---

### Rule 1: Signal New Terms Clearly

When you define a new concept, it must be visually distinct from the rest of the text. Use **boldface**.

**Standard Format:**

> A function `f` is **monotone** if for all `x > y`, we have `f(x) > f(y)`.

**Alternative:**

> **Definition:** A function `f` is said to be **monotone** if...

Use the first, more direct format for most definitions. Use the second, more formal format for your most central, crucial concepts (e.g., your main solution concept or equilibrium definition).

---

### Why Signaling Matters

Without a clear signal (like boldface), your reader doesn't know if you are:

1.  **Defining a term for the first time.**

2.  **Stating an implication of a known definition.**

3.  **Assuming they already know the term.**

**Example of ambiguity:**

> An allocation rule is efficient if it assigns to all agents amounts that are no greater than their peak amounts.

Is this *the definition* of efficiency in this model? Or is it a *consequence* of a standard definition of efficiency applied to this specific environment? The reader has to guess. Signaling with boldface removes all doubt.

---

### Rule 2: Provide Illustrative Examples

> Good exposition usually goes back and forth between the general and the particular.

For any non-trivial definition, you must show what it includes and excludes. Thomson recommends four categories of examples.

---

### The Four Crucial Types of Examples

For a property (e.g., "convexity"), provide examples of objects that:

1.  **Satisfy the definition** (a standard, simple case).

2.  **Do not satisfy the definition** (a clear violation).

3.  **Satisfy the definition, but *almost* do not** (a boundary case).

4.  **Do not satisfy the definition, but *almost* do** (another boundary case).

> The boundary cases (3 and 4) are particularly important as they are responsible for three-fourths of the work involved in the proofs.

---

### Example: Convex Sets

**Definition:** A set `S ⊂ ℝ²` is **convex** if for all `x, y ∈ S` and all `t ∈ [0,1]`, `tx + (1 - t)y ∈ S`.

![Image showing convex and non-convex sets, including boundary cases.](https://i.imgur.com/gK2s49z.png)

*   `S₁`, `S₂`: **Standard cases** that satisfy the definition.
*   `S₄`: **Clear violation**.
*   `S₃`: **Boundary case (satisfies)**. The set is convex even though a point is missing from its boundary. This is a crucial case.
*   `S₅`: **Boundary case (violates)**. The set is *almost* convex, but the missing point `y` makes it non-convex.

---

### Example: Single-Peaked Preferences

**Definition:** A preference `R` is **single-peaked** if it has a unique bliss point `x*`, and utility is strictly decreasing as we move away from `x*`.

![Image showing five examples of preference relations, some single-peaked, some not.](https://i.imgur.com/kS9gYfN.png)

*   `R₁`, `R₂`, `R₃`: **Satisfy**. `R₂` is a crucial boundary case (peak at endpoint). `R₃` is symmetric, which is a special case, not a requirement.
*   `R₄`: **Violates** (two peaks).
*   `R₅`: **Violates** (plateau, not a single peak). This is a crucial boundary case.

Without these examples, many readers would wrongly assume symmetry is required or that plateaus are allowed.

---

### Rule 3: Define in Logical Order

> State the space before the objects that live in it. Introduce terms in such a way that the definition of each new one involves only terms that have already been defined.

**Wrong Order:**

> Let `F` be a social choice correspondence from preference profiles in `ℛⁿ` to the set of alternatives `A`.

*The reader learns about `F` before they know what `ℛ` and `A` are.*

**Right Order:**

> Let `A` be a set of alternatives. Let `ℛ` be a class of preference relations on `A`. A social choice correspondence is a function `F: ℛⁿ → A`...

*The reader learns about the universe (`A`, `ℛ`) before the object (`F`) that lives in it.*

---

### Rule 4: Group and Factor Out Common Elements

When defining several related concepts, factor out the common parts to avoid repetition and highlight the differences.

**Repetitive:**

> An allocation is **Pareto efficient** if there is no other allocation `z'` that all agents find at least as desirable and at least one agent strictly prefers.
> An allocation is **weakly Pareto efficient** if there is no other allocation `z'` that all agents strictly prefer.

**Better (Factored Out):**

> An allocation `z` is:
> *   **Pareto efficient** if there is no `z'` such that `z' Rᵢ z` for all `i` and `z' Pⱼ z` for some `j`.
> *   **weakly Pareto efficient** if there is no `z'` such that `z' Pᵢ z` for all `i`.

This format isolates the key difference between the two concepts.

---

### Rule 5: Separate Formal Definition from Interpretation

This keeps your model general and allows others (or you!) to discover new applications.

**Step 1: The Formal Definition (Pure Math)**

```
Definition: A **bankruptcy problem** is a pair `(c, E)` where `c ∈ ℝⁿ` and `E ∈ ℝ` such that `Σcᵢ > E`.
```

**Step 2: The Economic Interpretation**

```
Interpretation: We interpret `cᵢ` as the claim of creditor `i` and `E` as the assets of the bankrupt firm. A rule determines how to divide `E`.
```

*This formal object is mathematically identical to a tax problem. By separating the definition, you make your results applicable to both fields.*

---

### Rule 6: Don't Collapse Similar Statements

Avoid compact definitions that force the reader to do mental gymnastics.

**Bad (Hard to Parse):**

> The function `f` is **decreasing (increasing; non-decreasing)** if for all `x > y`, we have `f(x) < f(y)` (respectively `f(x) > f(y)`; `f(x) ≥ f(y)`).

*The reader has to read this three times to be sure they understand each case.*

**Good (Clear and Explicit):**

> *   A function `f` is **increasing** if `x > y` implies `f(x) > f(y)`.
> *   A function `f` is **decreasing** if `x > y` implies `f(x) < f(y)`.
> *   A function `f` is **non-decreasing** if `x > y` implies `f(x) ≥ f(y)`.

> Space is cheap. Reader attention is expensive. Don't trade one for the other.

---

### Self-Audit: Your Definitions

1.  **Signaled?** Are your key terms in **bold**?

2.  **Illustrated?** Have you provided examples, especially for boundary cases?

3.  **Ordered?** Do you define the space before the objects in it?

4.  **Separated?** Is the formal math separate from the economic story?

5.  **Unambiguous?** Have you avoided collapsing multiple definitions into one confusing sentence?

---


---

---

## Part 4: Proofs

### Constructing a Clear and Convincing Argument

---

### A Proof is an Argument

> A proof written entirely in English is often not precise enough and is too long. A proof written entirely in mathematics is impossible to understand—unless, of course, you are a digital computer. Modern estimation techniques have shown that a proof's optimal ratio of mathematics to English lies between 52 and 63.5 percent.

Your goal is to blend the precision of mathematics with the readability of English.

---

### The Right Mix: Words for Logic, Math for Precision

**Too Much Math (Code, not an argument):**

`∀ε>0, ∃δ>0: |x-x₀|<δ ⇒ |f(x)-f(x₀)|<ε ⇒ f cont. ⇒ ∃x*:f(x*)≥f(x)∀x`

**Too Wordy (Imprecise, lacks rigor):**

> Because the function is continuous, it must achieve a maximum somewhere on the set since the set is compact, which is a standard result.

**Just Right (Guides the reader):**

> The function `f` is continuous by **(Cont)**. The domain is compact. Therefore, by the **Weierstrass Theorem**, a maximum `x*` exists.

This is a sentence a human can read. It tells a story: Assumptions -> Theorem -> Result.

---

### Rule 1: Structure Your Proofs

Long proofs must be broken into clearly labeled parts. This transforms a "black box" of calculations into a transparent, verifiable argument.

**Label your steps clearly:**

*   **Step 1, Step 2, ...**
*   **Claim 1, Claim 2, ...**
*   **Case 1, Case 2, ...**
*   **Lemma 1, Lemma 2, ...** (for intermediate results of independent interest)

Give each step a descriptive title.

---

### Example: Unstructured vs. Structured Proof

**Bad (A Wall of Text):**

> *Proof.* By assumption the function is continuous and the domain is bounded and closed so by the Weierstrass theorem it attains a maximum and since the objective is strictly concave the maximum is unique and by the first-order condition we have that...

**Good (A Clear Argument):**

> *Proof.*
> **Step 1: Existence of a maximum.** The objective function is continuous by **(Cont)** and its domain is compact. By the **Weierstrass Theorem**, a maximum exists.
>
> **Step 2: Uniqueness.** The objective function is strictly concave by **(S-Conc)**. Therefore, the maximum is unique.
>
> **Step 3: Characterization.** Since the maximum is interior, it is characterized by the first-order condition... ∎

---

### Rule 2: Gather Hypotheses Before Conclusions

All the conditions required for a result should be stated upfront.

**Bad (Conditions are scattered):**

> If `A` and `B`, then `D` since `C`.

**Also Bad:**

> If `A` and `B`, then `D`. This is because `C` holds.

**Good (All conditions first):**

> If `A`, `B`, and `C`, then `D`.

This allows the reader to see the complete logical foundation before the implication is made.

---

### Rule 3: Be Specific About Which Assumptions Are Used

Never just say "by the assumptions."

**Vague:**

> By the assumptions made earlier, we know the correspondence is non-empty.

**Specific:**

> The correspondence is non-empty because preferences are complete **(Comp)**.

**Even Better:**

> Because every agent's consumption set is non-empty **(Part (ii) of A1)**, the set of feasible allocations is non-empty.

This practice forces you to perform a critical task...

---

### Rule 4: Verify the Independence of Your Hypotheses

> After you have written QED, look in the box for stranded hypotheses.

If you have an assumption that was never used in the proof, one of two things is true:

1.  You made a mistake in the proof.

2.  You have a **stronger theorem** than you thought!

**Self-Audit:** For each theorem, go through your list of assumptions. Can you construct a counterexample if you drop assumption `A`? If you can't, maybe `A` isn't needed.

---

### Example: Dropping an Assumption

Suppose you proved:

> **Theorem:** If preferences are continuous **(Cont)** and strictly convex **(S-Conv)**, a unique Walrasian equilibrium exists.

You check your proof and realize you only used **(S-Conv)** to prove uniqueness, not existence.

You now have two stronger results:

> **Theorem 1 (Existence):** If preferences are **(Cont)** and **(Conv)**, a Walrasian equilibrium exists.

> **Theorem 2 (Uniqueness):** If an equilibrium exists and preferences are **(S-Conv)**, it is unique.

This is a significant improvement, discovered by checking for leftover assumptions.

---

### Rule 5: Don't Leave Too Many Steps to the Reader

> The request to "fill in the details" is an unfair burden to place on the reader. It is your paper and your proof.

A proof is not a homework problem.

*   **Bad:** "The remainder of the proof is tedious but straightforward and is left to the reader."

*   **Acceptable:** "The derivation of the second-order conditions is standard and has been relegated to Appendix B."

*   **Good:** "The logical steps of the argument are presented here. Routine algebraic simplifications are detailed in the appendix."

The reader must be able to follow the *logic* of the argument without having to do calculations. Routine algebra can be appended, but logical steps cannot.

---

### Rule 6: Handle Quantifiers with Care

Mathematical grammar must be precise.

**Bad (Ambiguous `for any`):**

> If for any `x ∈ X`, `f(x) > a`...

Does this mean "for all `x`" or "for some `x`"? Avoid `for any`.

**Bad (Quantifier in text):**

> It is true that `blah blah blah`, `∀x` such that `P(x)`...

Don't mix quantifier symbols in English sentences. Write `for all x`.

**Bad (Double Quantification):**

> For all `(R, Ω), (R, Ω') ∈ ℰ`...

The variable `R` is quantified twice. Write "For all `(R, Ω) ∈ E` and all `Ω'∈ ℝ₊`..."

---

### Rule 7: Show Where the Proof Ends

At the end of a proof, always place a clear marker.

*   **Q.E.D.** (Quod Erat Demonstrandum)

*   **∎** (The Halmos / Tombstone symbol) - This is the modern standard.

Delete redundant phrases like "This completes the proof. ∎". Just the symbol is enough.

For a very long proof that spans multiple pages, it can be helpful to write:

> ...which establishes the result. This completes the proof of Theorem 2. ∎

---

### Self-Audit: Your Proofs

1.  **Structured?** Are your proofs broken into labeled **Steps** or **Claims**?

2.  **Readable?** Is there a good mix of words (for logic) and math (for precision)?

3.  **Specific?** When you use an assumption, do you name it explicitly?

4.  **Complete?** Are all logical steps present, even if algebra is in an appendix?

5.  **Verified?** Have you checked if every assumption is actually used? Are there any "leftover parts"?

---


---

---

---

## Part 5: Pictures

### Building Intuition with Visuals

---

### The Power of a Good Figure

> A picture is not a substitute for a proof, but it can cut the time needed to understand the proof by half. Some of my papers have been remembered mostly for their diagrams. I am very proud of that. It means that I have been successful in my efforts at communication.

Figures are your most powerful tool for conveying intuition quickly.

---

### When to Use Figures

*   **To illustrate a definition:** Show a convex set and a non-convex set.
*   **To prime the reader for a proof:** Show the key geometric intuition before the algebra.
*   **To present a counterexample:** Show a case where a theorem fails.
*   **To provide blessed relief:** Break up long, dense sections of text.

Your paper should be "crawling with diagrams."

---

### Rule 1: Label Your Figures Completely

A figure must be self-contained. The reader should not have to hunt through the text to understand what it shows.

**Every figure needs:**

*   A descriptive caption (`Figure 1: The Core of a Three-Person Game`).
*   Labeled axes (`Price`, `Quantity`).
*   Labeled curves (`BR₁`, `BR₂`, `D`, `S`).
*   Labeled points of interest (`e`, `p*`, `q*`).

> Label all objects in a figure unless there is a very good reason not to.

---

### Example: A Poorly Labeled Figure

![A graph with two intersecting lines and no labels.](https://i.imgur.com/k2HnR5d.png)

**Caption:** Figure 1.

**What's wrong?**

*   What are the axes? Price, quantity? Strategies? Effort levels?
*   What are the lines? Best responses? Supply and demand?
*   What is the intersection point? An equilibrium? An efficient outcome?

This is not a figure; it's a puzzle. The reader has to guess what it means.

---

### Example: A Well-Labeled Figure

![The same graph, but with all elements labeled.](https://i.imgur.com/o7sV8vF.png)

**Caption:** Figure 1: Nash Equilibrium in the Cournot Duopoly Model.

**What's right?**

*   Axes are clearly `q₁` and `q₂`.
*   Curves are labeled `BR₁` and `BR₂`.
*   The equilibrium point is clearly marked as `NE`.

This figure tells a complete story. A reader can understand the core idea of Cournot competition in seconds just by looking at it.

---

### Rule 2: Draw Your Figures with Care and Purpose

Don't just throw in a generic drawing. Make the geometry of your figure reflect the economics of your model.

**Good Practices:**

*   Draw indifference curves with the right curvature (convex, linear, Leontief).
*   Draw your figures to scale as much as possible.
*   Use arrows to indicate movement or the direction of a preference.
*   Use dotted lines for constructions and solid lines for fundamentals.
*   Use shading to denote sets (e.g., the set of feasible allocations).

---

### Example: The Edgeworth Box

**The Wrong Way:** A simple, closed rectangle.

> This is dangerously misleading. It suggests that agents can only consume bundles *inside* the box, but their optimization problems are defined over the entire consumption space (`ℝ₊²`).

**The Right Way:** Two overlapping coordinate systems.

> This correctly represents the situation. The box is just the set of feasible allocations, a subset of the world agents live in.

![The wrong vs. right way to draw an Edgeworth Box](https://i.imgur.com/gZ3J2So.png)

*Source: Thomson (2011). This is Figure 2.13 in his guide.*

---

### Rule 3: Refer to Your Figures in the Text

It is not enough to just include a figure. You must integrate it into your argument.

**Guide the reader's eye:**

> "As shown in Figure 2, the best-response function of agent 1, `BR₁`, is upward sloping, indicating strategic complementarities..."

> "Consider point `x` in Figure 3. This point is not in the core, as the coalition `{1,2}` can improve upon it..."

Tell the reader what they are supposed to be seeing and learning from your picture.

---

### Self-Audit: Your Figures

1.  **Are there enough?** Does every key concept and result have a visual aid?

2.  **Are they self-contained?** Is every element—axes, curves, points—clearly labeled?

3.  **Are they accurate?** Does the geometry reflect the economics (e.g., convexity)?

4.  **Are they integrated?** Do you explicitly refer to and explain your figures in the text?

---

---

## Part 6: Paper Architecture

### Structuring the Whole

---

### The Introduction: Answer Four Questions

Your introduction should not be a long, meandering literature review. Within the first page, you must answer four questions directly.

1.  **What is the general topic?** (e.g., auctions, matching, bargaining)

2.  **What is the specific question?** (The puzzle your paper solves)

3.  **What is your answer?** (A clear statement of your main result)

4.  **How do you get there?** (A brief outline of your method)

> Do not follow the chronological order of your research. A statement of your main findings should come early.

---

### Introduction Example: Weak vs. Strong

**Weak (Vague and Uninformative):**

> This paper studies mechanism design. A number of authors have studied this topic. We propose a new solution concept and analyze its properties. We find that the results are interesting and warrant further study.

**Strong (Clear and Direct):**

> It is well-known that the Vickrey auction is efficient but vulnerable to collusion. This paper asks whether an efficient *and* collusion-proof auction exists. We answer in the affirmative by introducing the "Sealed-Bid Second-Price-PLUS" auction. Our main result (Theorem 1) shows that this format implements the efficient allocation in dominant strategies, even when bidders can communicate. We establish this result by...

---

### The Body of the Paper: General to Specific is a Mistake

> The most common error in this respect, which is made by a very large number of young theorists, is to present results in their utmost generality from the beginning.

This is a natural impulse after months of hard work, but it is a pedagogical disaster. The reader needs to be guided.

**The Right Structure:**

1.  **Start with a simple, motivating example.** (e.g., 2 agents, 2 goods)

2.  **Build intuition** with this example and perhaps a figure.

3.  **State your main, general theorem.**

4.  **Provide the proof.**

---

### The Literature Review: Tell a Story

Your literature review is not a list; it is a narrative that positions your paper as the next logical step.

**Boring Enumeration:**

> Author 1 shows X. Author 2 shows Y. Author 3 shows Z.

**Compelling Narrative:**

> The literature established X (Author 1). This raised the question of Y. Author 2 showed the answer was no in general, but Author 3 found it was yes for a critical special case. This leaves open the question of..., which is what our paper resolves.

This story creates a clear puzzle that your paper comes to solve.

---

### The Conclusion: More Than a Summary

A good conclusion does three things:

1.  **Synthesizes the Take-Home Message:** What is the one big idea the reader should remember? Don't just repeat your results.

2.  **Discusses Limitations and Robustness:** What are the crucial assumptions your result depends on? What happens if they are relaxed?

3.  **Points to Open Questions:** What is the next logical research question that follows from your work?

It should provide a sense of closure while also opening the door to future research.

---

### Example: Weak vs. Strong Conclusion

**Weak (Repetitive):**

> In this paper, we introduced a new auction format. We showed that it is both efficient and collusion-proof. Future research could explore other properties.

**Strong (Insightful):**

> Our analysis demonstrates that collusion-proofness need not come at the cost of efficiency. The key lies not in limiting bids, but in designing the payment rule. Our result hinges on the assumption that agents cannot make binding side-payments; relaxing this is an important avenue for future work. More broadly, our findings suggest that mechanism designers should focus less on preference restrictions and more on the design of communication channels.

---

### On Appendices

> The main text should contain all of the components of your argument. However, calculations that are straightforward, tedious, or that can be trusted to have been done properly, should be relegated to an appendix.

**Good candidates for an appendix:**

*   Routine algebraic derivations.
*   Proofs of minor, auxiliary lemmas.
*   Robustness checks for alternative specifications.

**Bad candidates for an appendix:**

*   The proof of your main theorem.
*   Any step that contains a key logical insight.
*   Definitions.

> The reader should be able to follow the entire *logical architecture* of your argument without ever leaving the main text.

---

## Final Summary: Thomson's Commandments

1.  **Clarity First.** Make complex ideas seem simple.
2.  **Structure is Everything.** In your paper, your sections, your proofs.
3.  **Notation Matters.** Be conventional, mnemonic, and minimal.
4.  **Definitions Need Examples.** Especially boundary cases.
5.  **Proofs are Arguments.** Use words and math to guide the reader.
6.  **Use Pictures.** They convey intuition faster than words.
7.  **Write for the Reader.** Your goal is to teach, not to impress.

---

# Thank You

**Questions?**

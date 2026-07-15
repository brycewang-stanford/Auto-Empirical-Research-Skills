# Academic Writing Standards — from Thomson, *A Guide for the Young Economist* (2nd ed.)

Use this checklist during Pass 3 (Academic Tone and Technical Precision) of the polishing workflow.

## 1. General Principles (Thomson Ch.2, §1)

### 1.1 Write So That You Will Not Have to Be Read
- By leafing through the article, the reader should spot: main findings, most notation, crucial definitions
- A reader with little time should grasp the novel aspects by visual inspection alone
- Readers scan for results and look around them for context — they don't read linearly

### 1.2 Don't Forget How You Made Your Discoveries
- The author arrived at the theorem in small steps (2 agents, 2 goods, linear technologies, no uncertainty, with diagrams)
- The reader can only understand through those same simple cases
- In a seminar, explaining the path of discovery helps; in a paper, include simplified versions before the general case

### 1.3 Don't Forget Your Errors
- "A bone is stronger where it has been broken"
- Remember where you had trouble — readers will have trouble in the same places
- Anticipate and address potential misunderstandings

### 1.4 Demonstrate Originality and Significance
- Show that what you did has not been done before
- Explain how your assumptions differ from those in related literature
- "Make your reasoning appear simple, even trivial" — this exercise in humility will be good for your soul

### 1.5 Understand the Function of Each Component
- **Title**: Should be as descriptive as possible. Consider whether it can state the result. "Generic 4×4 Two Person Games Have at Most 15 Nash Equilibria" (McLennan & Park 1999) states the result; "On the Number of Equilibria in Two-Person Games" does not.
- **Abstract**: Many readers decide whether to read based on it. Ensure key words in the abstract match key words listed.
- **Introduction**: Place work in context, describe principal findings, use plain language. Do not start with a 2-3 page survey — get to your contribution sooner.
- **Conclusion**: Not a rehash of the introduction. Compact summary → lessons → directions for future work. A table comparing your results with earlier papers is useful.

### 1.6 Literature Review: Tell a Story, Don't Enumerate
**Enumeration (bad):**
> Author 1 shows X. Author 2 shows Y. Author 3 shows Z. Here, we investigate W.

**Narrative (good):**
> On the domain of all games satisfying Condition 1, Nash equilibrium is not guaranteed to exist (Author 1). Since in applications payoff functions typically satisfy restrictions not implied by Condition 1, the question arose whether nonexistence persists. Unfortunately yes (Author 2)... This condition is frequently met, as it is equivalent to decreasing returns to scale... If returns decrease "sufficiently fast," Condition 3 holds. Recent empirical work suggests this may often be the case. Is existence recovered? The answer is yes, but only in the two-player case (Author 3). Here, we resolve the issue for three or more players.

Key differences: (1) puts authors' names in parentheses, keeping focus on the results; (2) shows how this paper answers a question that earlier work couldn't.

---

## 2. Notation (Thomson Ch.2, §2)

- Use easily recognizable notation whose meaning can be guessed
- **a ∈ A** makes intuitive sense (little a belongs to big A); do NOT write **A ∈ a**
- If Z is a set, call its elements z, z′; if φ is a family of functions, call members ϕ, ˜ϕ, ψ
- Use mnemonic abbreviations: W for welfare, E for equilibrium, etc.
- Don't introduce notation you'll use only once or twice
- Respect hierarchy: group related notation; make dependencies visible
- Choose notation that results in uncluttered mathematical expressions
- Only use notation you can easily pronounce or draw on the board
- Learn LaTeX

---

## 3. Definitions (Thomson Ch.2, §3)

- **Don't assume readers' familiarity** with your terms and definitions — even if standard in your subfield
- **Make it clear when you are defining a new term** — signal explicitly: "We call X a Y if..."
- **Indicate the kind of mathematical object** each new notation designates (is it a set? a function? a real number?)
- **Give examples** illustrating novel definitions — without them, definitions are nearly useless
- **Separate formal definitions from interpretations**: "Formally, a widget is... Informally, think of a widget as..."
- **Present basic concepts in their full generality** — then specialize
- **Write in logical sequences** — don't use a concept before defining it
- **Don't collapse two or three similar statements into one** — be explicit
- **When defining a concept, indicate what it depends on** — make functional dependencies explicit
- **Be unambiguous and consistent in quantifications** — ∀ and ∃ usage must be precise
- **Don't use different terms for the same concept** (elegant variation — see McCloskey Ch.20)
- **Name concepts carefully** — the name will influence how readers think about it
- **Avoid unnecessary technical jargon** — don't invent terminology unless truly needed
- **Challenge dominant but inadequate terminology** — if the standard term is misleading, say so and propose better
- **Use technical terms correctly** — don't stretch their meanings

---

## 4. Models (Thomson Ch.2, §4)

- **Understand the role of models** — they are simplified representations, not reality
- **Introduce your model by moving from infrastructure to superstructure**: agents → endowments → preferences → technology → equilibrium concept
- **Avoid long sentences** — break them up
- **Redundancy is useful, but don't overdo it** — some repetition helps, but not too much
- **Don't be shy about explaining very simple things** — what's obvious to the author after months of work is not obvious to the reader
- **Beware the apparent simplicity of numerical examples** — they can be misleading
- **If you name agents, do so helpfully**: "Ann" and "Bob" not "Agent 1" and "Agent 2" in simple examples; use consistent numbering in complex models
- **Use one enumeration for each object category**: if agents are 1,2,...,n, goods are A,B,..., not 1,2,...,m (unless for a reason)
- **State assumptions in order of decreasing plausibility or generality**
- **Group assumptions by category** — keep related assumptions together
- **Figure out and indicate logical relations among assumptions and groups of assumptions** — which imply which?
- **Make sure there are objects satisfying all your assumptions** — verify non-emptiness
- **Use a common format for formal statements of results** — each theorem/proposition should look similar

---

## 5. Theorems and Proofs (Thomson Ch.2, §5)

- **Choose the right mixture of words and mathematics in proofs** — not all math, not all prose
- **Divide proofs into clearly identified steps or cases**: "Step 1: We first show... Step 2: Next, we..."
- **Gather in front of a conclusion all the conditions needed to reach it** — don't make readers look back
- **Pay special attention to quantifications** — "for all ε > 0, there exists δ > 0" not "there exists δ > 0 for all ε > 0"
- **Specify precisely which assumptions (or parts of them) are used in each step**
- **Don't leave (too many) steps to the reader** — "it is obvious that" and "it can be shown that" are red flags
- **Use a consistent writing style** throughout proofs
- **Be consistent in choosing running indices and quantifications** — don't switch from i to j without reason
- **Don't use quantifiers in English sentences** — ∀ and ∃ belong in displayed formulas, not in running text
- **Show clearly where each proof ends** — with ■, □, or Q.E.D.
- **If you think a step is obvious, look again** — it often isn't
- **Verify the independence of your hypotheses** — is each assumption necessary?
- **Explore all possible variants of your results** — what happens if you weaken an assumption?
- **Use pictures** — a good diagram can replace pages of algebra

---

## Common Academic Style Issues to Check

Based on all three books combined:

### Introduction Problems
- [ ] Starts with hook, not "This paper..." boilerplate
- [ ] No table-of-contents paragraph ("The outline is as follows...")
- [ ] No "As we shall see" anticipation
- [ ] Literature review tells a story, not an enumeration
- [ ] Gets to the contribution within the first page

### Body Problems
- [ ] All technical terms defined before use
- [ ] Notation is mnemonic and consistent
- [ ] Active voice dominates ("We estimate..." not "It is estimated...")
- [ ] Each paragraph has a point
- [ ] No "not only...but also" constructions
- [ ] No "due to" for "because of"
- [ ] No "the fact that"
- [ ] Comma splices corrected
- [ ] Equations use words alongside symbols for clarity
- [ ] Tables and figures have self-explanatory, declarative titles

### Conclusion Problems
- [ ] Not a rehash of the introduction
- [ ] Contains specific implications and directions for future work
- [ ] Ends with emphasis — strongest idea last

### Overall
- [ ] The abstract matches keywords and conclusion
- [ ] The title describes the content or states the result
- [ ] No excessive acronyms
- [ ] The paper's structure is visible without reading every word

# Theory Stage 2: Structural Refinement

Second stage of theory paper editing. Refines the structure established in Stage 1 (General Structure) with theory-specific checks.

## Purpose

Apply theory-specific structural refinements AFTER general structure is complete:
- Introduction structure (the 4 questions)
- Simple-to-general ordering (not general-to-specific)
- Model section organization
- Theorem presentation structure
- Conclusion synthesis focus
- Appendix usage validation

## Prerequisites

**Stage 1 (General Structure) must be complete.** The paper should already have:
- Good section organization and logical flow
- Well-structured paragraphs with topic sentences
- Transitions between sections (McCloskey's transitive pattern)
- Anti-patterns eliminated (Jonesian arrangement, table-of-contents paragraphs, etc.)

This stage focuses on theory-specific refinements only.

## Instructions

### Step 1: Evaluate the Introduction (The 4 Questions)

A theory paper introduction must answer FOUR questions on the first page or two:

**Question 1: What is the general topic?**
- Broad area: auctions, matching, bargaining, contracts, voting, etc.
- Reader should immediately know the paper's domain

**Question 2: What is the specific question?**
- The puzzle your paper solves
- Should be stated clearly and early (ideally by end of first page)
- Not vague: "We study firm behavior"
- But specific: "We characterize the conditions under which firms choose to merge"

**Question 3: What is your answer?**
- Clear statement of your main result
- Should appear EARLY in introduction (not buried at the end)
- Can be informal version of main theorem
- Example: "We show that mergers occur if and only if the synergy exceeds the cost of coordination"

**Question 4: How do you get there?**
- Brief outline of your approach/method
- Roadmap of the paper
- Example: "We model firms as players in a sequential bargaining game and characterize the subgame perfect equilibrium"

**Check the current introduction**:
- Does it answer all 4 questions?
- In what order? (they should appear early, not at the end)
- Is each answer clear and concrete?

**If missing or unclear**, plan revisions to add/clarify.

### Step 2: Check for "Simple-to-General" Ordering

**THE ERROR**: Most common structural mistake in theory papers is presenting results in UTMOST GENERALITY from the beginning.

**THE FIX**: Start simple, build intuition, THEN present general result.

**2a. Identify if paper makes this error**:

**General-to-Specific** (WRONG - but common):
```
Section 2: Model (n players, m actions, general type space, arbitrary information structure)
Section 3: Theorem 1 (Main result stated with maximum generality)
Section 4: Proof (Dense formal proof)
Section 5: Special Cases (2-player case shown as "example")
```

**Simple-to-General** (CORRECT - easier to understand):
```
Section 2: Motivating Example (2 players, 2 actions, complete information)
Section 3: Analysis of Example (Build full intuition with figures)
Section 4: General Model (n players, m actions, general information)
Section 5: Main Theorem (Generalizing the logic from Section 3)
Section 6: Proof
```

**2b. Why simple-to-general matters**:
- Readers understand concrete before abstract
- Simple case reveals the core intuition
- General proof makes sense once intuition is established
- You discovered your result this way—share the ladder you climbed

**2c. Plan revision if needed**:

If paper currently goes general-to-specific, consider:

**Option A**: Add a motivating example section BEFORE the general model
- Create Section 2: "Motivating Example"
- Work through 2x2 or simple case completely
- Add figures for intuition
- Then present general model

**Option B**: Restructure to move simple case earlier
- If simple case currently appears as "example" after main result
- Move it BEFORE the general statement
- Present it as the core analysis, not an afterthought

**Option C**: Add intuitive explanation within general model
- If structure can't change, add intuitive paragraphs
- Explain what theorem says in words before formal statement
- Provide intuition for proof before diving into formalism

Use AskUserQuestion if substantial restructuring is needed.

### Step 3: Evaluate the Model Section

**3a. Check model presentation order**:

The right order is:
1. **Players/Agents**: Who are the decision-makers?
2. **Timing**: What is the sequence of events?
3. **Actions**: What can players do?
4. **Information**: What do players know and when?
5. **Payoffs**: What are players' objectives?
6. **Solution Concept**: What equilibrium concept do you use?

Wrong: Defining payoff function before defining what actions are
Right: Define action space X, THEN define payoff function u: X → R

**3b. Check for intuition**:
- Does the model section explain WHY you make each modeling choice?
- Are assumptions motivated economically?
- Would a reader understand the economic situation being modeled?

**Example of good motivation**:
"We assume players move sequentially (rather than simultaneously) because we want to capture the first-mover advantage in market entry decisions."

**3c. Plan revisions**:
- Reorder model elements if needed (follow the 6-step order above)
- Add economic intuition for modeling choices
- Clarify what economic situation the model captures

### Step 4: Check Results Structure

**4a. Theorem ordering**:

Present theorems in LOGICAL order (the order a reader needs to understand them), not:
- The order you discovered them
- From most general to most specific
- Alphabetically or arbitrarily

**Good theorem ordering**:
1. Existence (does equilibrium exist?)
2. Uniqueness (is it unique?)
3. Characterization (what does it look like?)
4. Comparative statics (how does it change with parameters?)

**4b. Check theorem presentation**:

Each formal result should have THREE components:

1. **Informal statement**: What does this say in words?
2. **Formal statement**: The precise mathematical theorem
3. **Intuition/Interpretation**: Why is this true? What does it mean economically?

**Just formal statement** (hard to understand):
```
**Theorem 1**: Under Assumptions A1-A4, the function φ: X → Y defined by φ(x) = argmax...
```

**Complete presentation** (clear):
```
We now characterize the equilibrium of the game. Intuitively, players balance the tradeoff
between immediate payoffs and future continuation values, which leads to a unique threshold
strategy.

**Theorem 1** (Equilibrium Characterization): Under Assumptions A1-A4, the game has a unique
subgame perfect equilibrium in which player i adopts a threshold strategy with cutoff θ*ᵢ
defined by [formal expression].

The threshold θ*ᵢ represents the belief level at which player i is indifferent between acting
immediately and waiting. Players with beliefs above this threshold act; those below wait.
```

**4c. Plan revisions**:
- Reorder theorems if needed for logical flow
- Add informal statements before formal theorems
- Add intuition after formal theorems

### Step 5: Evaluate Conclusion Structure

A strong theory paper conclusion does THREE things:

**5a. Synthesizes the Take-Home Message**:
- Not just: "We characterized equilibria in a model of X"
- But: "Our analysis reveals a fundamental tradeoff between A and B that explains why we observe pattern C in markets"
- **What's the ONE BIG IDEA** the reader should remember?

**5b. Discusses Limitations and Robustness**:
- What assumptions are crucial?
- What happens if you relax them?
- Which results are robust, which are knife-edge?
- Be honest about scope

**5c. Points to Open Questions**:
- What's the natural next research question?
- Not vague "future research could..."
- But specific: "An important extension would be to allow for heterogeneous players, which would require..."

**Check current conclusion**:
- Does it do all three things?
- Or does it just rehash the introduction?
- Does it end strong (with the big idea or open question)?

**Plan revisions if needed**.

### Step 6: Check Appendix Usage

**6a. What belongs in main text** (DON'T put in appendix):
- Proof of main theorem
- Any step with key logical insight
- Definitions
- Main results
- Primary intuition

**6b. What belongs in appendix**:
- Routine algebraic derivations ("Straightforward algebra yields...")
- Proofs of minor, auxiliary lemmas
- Robustness checks and extensions
- Additional examples

**6c. The test**:
"Can a reader follow the complete logical architecture without leaving the main text?"
- If YES → appendix is correctly used
- If NO → move key content to main text

**Check current paper**:
- Is anything crucial buried in appendix?
- Is anything routine clogging up main text?

**Plan revisions if needed**.

### Step 7: Present Structural Revision Plan (if needed)

If substantial changes are needed, present options to user:

```
THEORY STRUCTURAL REFINEMENT NEEDED

Issues identified:
1. [e.g., "Introduction doesn't answer the 4 questions clearly"]
2. [e.g., "Paper presents general model before building intuition"]
3. [e.g., "Theorems lack informal statements"]

Proposed revisions:

Option A: [Description of approach]
Changes:
- [Specific change 1]
- [Specific change 2]
Pros:
- [Benefit 1]
- [Benefit 2]
Cons:
- [Drawback 1]

Option B: [Alternative approach]
...

Recommendation: I recommend Option [X] because [reasoning].
```

Use AskUserQuestion for user to choose.

### Step 8: Implement Revisions

After user approval (if needed), implement changes:

**8a. Introduction revisions**:
- Ensure 4 questions are answered clearly
- Move main result statement earlier if needed
- Add roadmap paragraph

**8b. Add motivating example** (if adopting simple-to-general):
- Create new section before general model
- Work through 2×2 or simple case
- Refer forward: "We generalize this intuition in Section X"

**8c. Reorder model elements** (if needed):
- Follow the 6-step order (players, timing, actions, info, payoffs, concept)
- Add economic motivation for modeling choices

**8d. Improve theorem presentation**:
- Reorder theorems for logical flow
- Add informal statements and intuition

**8e. Enhance conclusion**:
- Add synthesis paragraph
- Discuss limitations explicitly
- Identify specific open questions

### Step 9: Document Changes

```
THEORY STRUCTURAL REFINEMENT SUMMARY

Introduction (4 Questions):
✓ Question 1 (Topic): [status]
✓ Question 2 (Specific question): [status]
✓ Question 3 (Answer): [status]
✓ Question 4 (Approach): [status]

Simple-to-General Ordering:
✓ [Added motivating example / Maintained existing / Restructured]

Model Section:
✓ Order: [Correct / Reordered]
✓ Economic intuition: [Added / Already present]

Theorem Presentation:
✓ Ordering: [Logical / Reordered]
✓ Informal statements: [Added X / Already present]
✓ Intuition after theorems: [Added X / Already present]

Conclusion:
✓ Synthesis: [Enhanced / Already strong]
✓ Limitations: [Added / Already discussed]
✓ Open questions: [Specific / Already present]

Appendix:
✓ [Moved X to main text / Moved Y to appendix / No changes needed]

Next stage: Stage 3 (Technical Elements - Notation, Definitions, Proofs, Figures)
```

## Theory-Specific Principles Applied

**Thomson's Principle 3: Write So You Won't Have to Be Read**
- Paper should be scannable
- Readers jump around (not linear reading)
- Structure must support non-linear reading

**Thomson's Principle 4: Don't Forget Your Discovery Process**
- You arrived at theorem in small steps
- Don't hide the ladder (simple-to-general ordering)

**Clarity is the Main Goal** (Principle 1):
- No one will read very far if it's a burden
- Every structural choice must serve understanding

## What This Stage Does NOT Do

**Already handled by Stage 1 (General Structure)**:
- Section organization and logical flow
- Paragraph structure (topic sentences, Gerald Graff endings)
- Transitions between sections (transitive pattern)
- Anti-pattern elimination (Jonesian arrangement, etc.)
- McCloskey's structural principles

**Handled by later stages**:
- Technical elements (Stage 3): Notation, definitions, proofs, figures
- Sentence-level editing (Stage 4): Strunk & White rules
- Theory-specific line editing (Stage 5): Triviality test, scannability

This stage is THEORY-SPECIFIC STRUCTURAL REFINEMENT only.

## Output Format

At the end of Theory Stage 2, provide:
1. Summary of changes (as shown in Step 9)
2. The structurally refined document
3. Note that Stage 3 (Technical Elements) is next

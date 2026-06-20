# Economics Paper Review Checklist

A structured framework for reviewing and auditing economics papers, inspired by the multi-reviewer approach used in top journal refereeing.

## 1. Quick Review Mode (5-Minute Scan)

**Title** (score each 1-10):
- Clarity: Can a non-specialist understand the topic?
- Length: Under 12 words? (shorter sticks)
- Treatment + outcome named explicitly?
- Memorability: Would you remember it at a conference?

**Abstract**:
- States a concrete finding with a magnitude? (not "we find effects")
- Under 150 words?
- Follows the 4-part formula: motivation, method, result, implication?
- Opens with a fact or puzzle, not "This paper..."?

**Introduction**:
- Main result stated within the first 3 paragraphs?
- Literature woven into the argument (not a laundry list)?
- Length between 3-5 pages?
- Ends with a roadmap paragraph?

**Conclusion**:
- Under 1 page?
- Follows the 3-part formula: restate finding, implications, future directions?
- No new results or arguments introduced?

## 2. Deep Review Mode (Simulated Reviewers)

### Reviewer 1: The Methodologist

- [ ] Identification strategy explained in plain language before equations
- [ ] Key identifying assumption stated and defended
- [ ] Threats to validity listed and addressed (selection, omitted variables, reverse causality)
- [ ] Standard errors account for clustering, heteroskedasticity, or serial correlation as needed
- [ ] Robustness checks cover alternative specifications, samples, and definitions
- [ ] If applicable: first-stage F-stat reported (IV), parallel trends shown (DiD), bandwidth sensitivity (RDD)
- [ ] Pre-registration status disclosed, or justified why not
- [ ] Sample size adequate for the claimed precision

### Reviewer 2: The Field Expert

- [ ] Contribution clearly positioned relative to 3-5 closest papers
- [ ] Literature review is fair -- cites disagreeing work, not just supporting papers
- [ ] Results are economically significant, not just statistically significant (effect sizes contextualized)
- [ ] Institutional details accurate and sufficient for replication
- [ ] Policy implications warranted by the evidence (no overclaiming)
- [ ] External validity discussed honestly
- [ ] Data sources described with enough detail to assess quality

### Reviewer 3: The Writing Critic

- [ ] Active voice used throughout (check for "it was found", "is shown")
- [ ] Concrete language with magnitudes ("a 10% increase" not "a substantial effect")
- [ ] No throat-clearing in paragraph openings ("It is important to note that...")
- [ ] Tables are self-contained: title, notes, and units make them readable alone
- [ ] Figures have informative titles and axis labels
- [ ] Every word earns its place -- no padding or repetition across sections
- [ ] Paragraphs open with a claim, not a citation
- [ ] Transitions between sections feel motivated, not mechanical

## 3. Anti-AI Detection Checklist

Signs that writing sounds AI-generated -- avoid all of these:

**Word choice red flags**: Overuse of "delve", "crucial", "landscape", "multifaceted", "notably", "furthermore", "comprehensive", "robust" (outside its statistical meaning), "utilize" (instead of "use"), "leverage" (as a verb meaning "use"), "pivotal", "groundbreaking", "shed light on", "pave the way". (Canonical banned-word list lives in SKILL.md > Avoiding AI-Generated Writing Patterns.)

**Sentence-level tells**:
- Every sentence roughly the same length (vary between 8-25 words)
- Perfect parallel structure in every list (real academics are messier)
- No qualifying hedges (real researchers write "This likely reflects..." or "One interpretation is...")
- No field-specific jargon used naturally (e.g., "extensive margin" in labor, "pass-through" in IO)
- No parenthetical asides or em-dashes -- real writers use these
- Transitions that are too smooth; real papers have some roughness between sections

**Structural tells**:
- Generic placeholder phrases instead of specific institutional details
- Numbered lists where flowing prose would be more natural
- Every paragraph exactly the same length
- Conclusions that read like an executive summary rather than a reflection

**Fix**: Read two paragraphs of your favorite published paper in the same field. Match that rhythm, not ChatGPT's.

## 4. Pre-Submission Scoring

| Component | Points | Score |
|---|---|---|
| Title | /10 | ___ |
| Abstract | /10 | ___ |
| Introduction | /20 | ___ |
| Methodology / Identification | /15 | ___ |
| Results presentation | /15 | ___ |
| Writing quality | /15 | ___ |
| Tables and figures | /10 | ___ |
| Conclusion | /5 | ___ |
| **Total** | **/100** | ___ |

**Grade brackets**:
- 90-100: Ready for top-5 submission
- 80-89: Strong draft, minor revisions needed
- 70-79: Solid working paper, needs another round
- 60-69: Major structural or methodological gaps
- Below 60: Rethink framing or identification before rewriting

## 5. Journal Fit Assessment

**Targeting questions**:
1. Is the question of broad interest (top-5) or primarily relevant to a subfield (field journal)?
2. Does the paper make a methodological contribution, or is it an application of known methods?
3. Is the setting specific to one country, or does it speak to a universal mechanism?
4. How large is the likely audience? Would seminar attendees outside your field engage?

**Top-5 expectations**:
- *AER*: Broad interest, clean identification, well-written, important question. Accepts shorter papers via P&P.
- *QJE*: Strong narrative, big question, often historical or institutional depth. Rewards ambitious scope.
- *Econometrica*: Methodological novelty required -- new estimator, new theoretical result, or structural model.
- *REStud*: Technically rigorous, rewards theoretical or structural contributions alongside empirical work.
- *JPE*: Clean empirical design, interesting question, concise writing. Historically favors Chicago-style work.

**Field journal vs. top-5 decision rule**: If your paper's main appeal is "interesting result in domain X" rather than "new insight about how economies work," target the top field journal. There is no shame in this -- a well-cited field journal paper beats a desk-rejected top-5 submission.

# Worked Example: Codebook and Matching LLM Prompt

This file shows ONE classification task coded end-to-end: a mini-codebook with every component filled in, plus the matching LLM system prompt that operationalizes that codebook. The goal is to make the structure in SKILL.md Section 1 (codebook) and Section 4 (prompt) concrete.

**Task.** Classify short social-media posts about immigration policy into one of three attitude categories, plus a residual category. This matches the kind of open-ended survey response a researcher might collect after a priming or informational treatment.

---

## Part A — Codebook

Five components per label, as specified in SKILL.md Section 1: label string, definition, clarification (what IS in), negative clarification (what is NOT in), examples.

### Label: `anti_immigration`

- **Definition**: The post expresses opposition to increased immigration, stricter enforcement against existing immigration, or generalized negative evaluation of immigrants as a group.
- **Clarification (what IS included)**:
  - Explicit calls to reduce legal immigration quotas.
  - Support for deportation, border walls, or stricter enforcement.
  - Negative characterizations of immigrants as an economic or cultural threat.
  - Opposition to specific pro-immigration policies (e.g., DACA, refugee resettlement) on grounds that frame immigrants negatively.
- **Negative clarification (what is NOT included)**:
  - Opposition to a specific policy on procedural or fiscal grounds without negative framing of immigrants themselves (code as `neutral`).
  - Criticism of *government handling* of immigration without taking a position on immigration levels (code as `neutral`).
  - Posts opposing emigration from the author's own country (off-topic — code as `none_of_above`).
- **Positive examples**:
  - "We need to close the border now. Too many people coming in and taking jobs."
  - "Deport them all. This country is full."
  - "Stop the invasion at the southern border."
- **Negative examples** (common misclassifications that should NOT be `anti_immigration`):
  - "The asylum process takes too long and costs taxpayers too much." (fiscal/procedural, no negative framing of immigrants -> `neutral`)
  - "I support legal immigration but oppose illegal crossings." (mixed; apply multi-label or residual depending on context)

### Label: `pro_immigration`

- **Definition**: The post expresses support for increased or continued immigration, opposes enforcement actions, or offers generalized positive evaluation of immigrants as a group.
- **Clarification (what IS included)**:
  - Explicit support for higher immigration quotas, refugee admissions, or legalization programs.
  - Opposition to deportation, detention, or enforcement crackdowns on humanitarian grounds.
  - Positive characterizations of immigrants' contributions (economic, cultural, demographic).
- **Negative clarification (what is NOT included)**:
  - Neutral statements about immigrants being present without evaluative framing (code as `neutral`).
  - Personal stories about being an immigrant that do not take a policy position (code as `neutral`).
- **Positive examples**:
  - "Immigrants built this country. We should welcome more, not fewer."
  - "Abolish ICE. These are families, not criminals."
  - "Raise the refugee cap. We have the capacity and the obligation."
- **Negative examples**:
  - "My grandparents came here from Poland in 1920." (biographical, no policy stance -> `neutral`)
  - "The economy depends on foreign workers in agriculture." (descriptive-economic, no explicit pro-immigration stance -> `neutral`, unless context makes the stance clear)

### Label: `neutral`

- **Definition**: The post addresses immigration but does not take an evaluative stance on immigration levels or on immigrants as a group.
- **Clarification (what IS included)**:
  - Procedural or fiscal discussion without group-level framing.
  - Factual statements about immigration patterns, policy mechanics, or legal processes.
  - Criticism of specific administrative handling that does not imply a position on immigration levels.
- **Negative clarification (what is NOT included)**:
  - Posts that use procedural framing as cover for negative group evaluation (code as `anti_immigration` if the underlying framing is negative).
  - Posts expressing mixed/balanced positions should be coded with BOTH `pro_immigration` and `anti_immigration` under multi-label, not as `neutral`.
- **Positive examples**:
  - "The H-1B lottery system needs reform — the cap doesn't match demand."
  - "Asylum backlogs are at a record high."
  - "Countries of the EU coordinate immigration through the Schengen framework."

### Label: `none_of_above`

- **Definition**: The post does not discuss immigration policy, immigration levels, or immigrants as a group.
- **Clarification (what IS included)**:
  - Off-topic posts, spam, or ambiguous posts too short to interpret.
  - Posts about emigration, tourism, citizenship-for-investment, or international travel without immigration-policy framing.
  - Posts that mention immigration only as a passing reference in an unrelated argument.
- **Positive examples**:
  - "lol who cares"
  - "Check out my new business: www.example.com"
  - "The weather here is terrible today."

### Multi-label note

Posts may receive more than one substantive label (e.g., `pro_immigration` AND `anti_immigration` for a mixed post like "I support legal immigration but oppose illegal crossings"). `none_of_above` is exclusive.

---

## Part B — Matching LLM System Prompt

This prompt operationalizes the codebook above. Every category in the prompt maps 1:1 to a label in Part A. The prompt specifies output format, multi-label behavior, and refusal behavior for off-topic inputs.

```
You are an expert content analyst classifying short social-media posts about
immigration policy. Your task is to return ONLY category labels from the codebook
below, in the exact output format specified. Do not include explanations,
preambles, or commentary in your output.

## Categories

anti_immigration
Definition: The post expresses opposition to increased immigration, stricter
enforcement against existing immigration, or generalized negative evaluation of
immigrants as a group.
Includes: calls to reduce quotas; support for deportation, border walls, or
stricter enforcement; negative characterizations of immigrants; opposition to
pro-immigration policies on grounds that frame immigrants negatively.
Does NOT include: procedural/fiscal opposition without negative framing;
criticism of government handling without a position on immigration levels.
Examples: "We need to close the border now."; "Deport them all."

pro_immigration
Definition: The post expresses support for increased or continued immigration,
opposes enforcement actions, or offers generalized positive evaluation of
immigrants as a group.
Includes: support for higher quotas, refugee admissions, or legalization;
opposition to deportation on humanitarian grounds; positive evaluation of
immigrants' contributions.
Does NOT include: neutral statements of immigrant presence; biographical
references without policy stance.
Examples: "Immigrants built this country."; "Abolish ICE."

neutral
Definition: The post addresses immigration but does not take an evaluative
stance on immigration levels or on immigrants as a group.
Includes: procedural/fiscal discussion; factual statements about immigration
patterns or policy mechanics.
Does NOT include: posts using procedural framing as cover for negative group
evaluation; mixed pro/anti posts (apply BOTH substantive labels instead).
Examples: "The H-1B lottery needs reform."; "Asylum backlogs are at a record
high."

none_of_above
Definition: The post does not discuss immigration policy or immigrants as a
group. Also use for posts too short or ambiguous to interpret.
Examples: "lol who cares"; "Check out my new business."

## Rules

1. Return ONLY the label string(s). No quotes, no explanations, no preamble.
2. If a post clearly expresses BOTH pro and anti positions (e.g., "I support
   legal immigration but oppose illegal crossings"), return both labels
   comma-separated: anti_immigration,pro_immigration
3. none_of_above is exclusive: never combine with other labels.
4. If the post is in a language other than English, classify based on meaning,
   not surface form.
5. If you cannot confidently assign any label, return: none_of_above

## Output format

Return a single JSON object with this exact shape:
{"labels": ["<label>", "<label>"]}

The labels array MUST contain 1 or 2 entries, drawn only from:
anti_immigration, pro_immigration, neutral, none_of_above.
```

User message (sent separately, one per post):

```
Code this post:

{post_text}
```

---

## Part C — How this example connects to SKILL.md

- **Section 1 (Codebook Design)**: Every label above has all five components (label string, definition, clarification, negative clarification, positive + negative examples) as specified (Halterman & Keith 2025).
- **Section 4 (Prompt Construction)**: The prompt places the codebook in the system message, specifies exact output format (JSON), specifies multi-label behavior explicitly, uses a clear delimiter in the user message, and does not include any covariates (country, demographic fields) that the classifier should not use.
- **Section 5 (Pilot Testing and Validation)**: Before hand-coding, run Halterman & Keith's Stage 1 label-free tests on THIS prompt: (I) does the model only return `anti_immigration`, `pro_immigration`, `neutral`, or `none_of_above`? (II) given the verbatim definition of `anti_immigration`, does it return `anti_immigration`? (III) given the verbatim example "We need to close the border now," does it return `anti_immigration`? (IV) does reordering the four categories change any predictions?
- **Cross-national use**: If adapting this codebook to non-English survey data, validate per-language against native-language hand codes rather than assuming English validation transfers (Heseltine & Clemm von Hohenberg 2024; Tornberg 2025).

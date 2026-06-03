---
name: text-classification
description: LLM-based text classification: codebook, validation, agreement statistics.
argument-hint: "[describe your text data and classification task]"
---

# LLM-Based Text Classification for Social Science Research

## Instructions

### 1. Codebook Design

- Before drafting the codebook, specify the population, sampling frame, and (for experimental data) the treatment condition each response is drawn from. These constrain which categories can plausibly exist and which demographic subgroups any bias assessment must cover. LLM classification extends, rather than replaces, the longer open-ended coding tradition in survey methodology (Geer 1988; Lupia 2018).
- Treat codebook design as the most consequential decision in the classification pipeline. LLMs struggle with loose instructions and revert to general-purpose definitions rather than following researcher-specific operationalizations (Halterman & Keith 2025).
- Structure each code with the following components (adapted from Halterman & Keith 2025):
  - **Label**: The exact output string the model should return
  - **Definition**: A single-sentence operationalization of the construct
  - **Clarification**: What IS included — boundary cases that belong in this category
  - **Negative clarification**: What is NOT included — common confusions and adjacent categories
  - **Examples**: 2-3 positive examples (correctly classified) and 2-3 negative examples (common misclassifications)
- Keep the number of codes small (3-6) for initial classification. Larger coding schemes increase ambiguity and reduce inter-annotator agreement for both humans and LLMs (Chae & Davidson 2025).
- Allow multi-label assignment when responses may reflect more than one construct. Specify this explicitly in the prompt — models default to single-label output unless instructed otherwise.
- Include a residual category (e.g., `none_of_above` or `uncodeable`) for responses that are too vague, too short, or off-topic. Define this category as precisely as the substantive codes (Halterman & Keith 2025).
- Iterate the codebook through pilot testing. Examine disagreements between LLM output and hand-coding to identify ambiguous definitions, then revise. Most codebook problems are definition problems, not model problems (Halterman & Keith 2025).
- For a fully-worked example of a codebook with all five components filled in for a realistic three-category classification task, plus a matching system prompt that operationalizes it, see `reference/example-codebook-and-prompt.md`.

### 2. Choosing a Learning Regime

- Follow the decision framework from Chae & Davidson (2025), which maps document characteristics and available resources to the appropriate approach:

  **Zero-shot prompting**: Use when classifying short documents with a large decoder model (GPT-4o, Llama3-70B+) and no labeled training data. Best for rapid prototyping and tasks where constructs are well-defined. GPT-4o achieves the best zero-shot performance across tasks (Chae & Davidson 2025).

  **Few-shot prompting**: Add labeled examples to the prompt. Results are inconsistent — adding examples helps some models but degrades others (Chae & Davidson 2025). Always compare few-shot against zero-shot on a held-out sample before committing. Select diverse examples covering edge cases, not just prototypical instances.

  **Fine-tuning**: Train a model on labeled data. Effective with as few as 100 hand-coded examples for smaller models (Chae & Davidson 2025). Fine-tuned smaller models (Llama3-8B, GPT-3 Davinci) can match GPT-4o zero-shot performance. Prefer this when you have labeled data and need cost-effective classification at scale.

  **Instruction-tuning**: Combine detailed prompting with fine-tuning on paired instruction-output examples. Most powerful regime for complex tasks — instruction-tuned Llama3-70B surpasses GPT-4o zero-shot on stance detection (Chae & Davidson 2025). Requires more technical infrastructure but yields the highest accuracy.

  **Encoder-only fine-tuning**: A distinct fourth regime often omitted from generative-LLM discussions. Fine-tuning a smaller encoder-only model (BERT, DeBERTa, SBERT; ~86–110M parameters, personal-computer hardware) on modest labeled data can match or exceed zero-shot generative LLMs on many classification tasks at a fraction of the cost and with fully reproducible (deterministic) output (Chae & Davidson 2025, Table 1; Ziems et al. 2024 find fine-tuned RoBERTa rarely under-performs larger generative models across 20 tasks). Prefer encoder fine-tuning when the label set is fixed, labeled data exists, and reproducibility matters more than generative flexibility.

- When resources permit, test multiple regimes on the same pilot sample and select based on empirical performance, not assumptions.

### 3. Model Selection and Reproducibility

- Prefer open-weight models (Llama 3, Gemma, Mistral) for publishable research. Open-weight models run locally produce substantially lower and more predictable variance across runs, while proprietary models (GPT-4, Gemini) show high and unpredictable variance even with temperature=0 (Barrie, Palmer & Spirling 2025).
- If using proprietary models, document the exact model identifier (e.g., `gpt-4o-2024-08-06`), not the model family name. Commercial models are modified or deprecated without notice — GPT-3 was withdrawn from OpenAI's API entirely (Barrie, Palmer & Spirling 2025; Chae & Davidson 2025).
- Set temperature to 0 for classification tasks. This reduces but does not eliminate stochastic variation in proprietary models (Barrie, Palmer & Spirling 2025).
- Run the same ~50 responses through the classifier twice, with meaningful separation (e.g., two weeks apart, or across a model-version change), and report the agreement rate between runs as a variance metric. These specific numbers (N = 50, ≥ 95% agreement as a "stable" threshold) are house defaults consistent with field conventions, not values established in a single cited study; Barrie, Palmer & Spirling (2025) motivate the test but do not fix the thresholds.
- When classifying across multiple languages or cultural contexts, validate per-language against hand-coded native-language ground truth. LLM classification accuracy is high across non-English settings but not uniform: GPT-4 tracks English accuracy (~90%) on Italian, German, and Chilean political tweets (Heseltine & Clemm von Hohenberg 2024), and remains above all supervised comparators across 11 countries on party-identification tasks, though absolute accuracy drops outside the United States (Tornberg 2025). Do not assume English-language validation carries over.
- Be aware that commercial models may refuse to classify politically sensitive content. Chae & Davidson (2025) found GPT-4o refused to process some Facebook comments about political candidates due to content moderation filters. For sensitive topics (immigration attitudes, extremism, hate speech), test for refusal rates before full deployment.
- Consider data privacy: survey responses sent to commercial APIs may be absorbed into training data (Chae & Davidson 2025). For data containing personally identifying information, use locally hosted open-weight models or confirm the API provider's data retention policy.

### 4. Prompt Construction

- Place the codebook in the system prompt. Include all components for each code (label, definition, clarification, negative clarification, examples).
- Specify the exact output format: code labels only, comma-separated if multi-label. Instruct the model to return no additional text. Smaller models in particular generate conversational preamble unless explicitly constrained (Chae & Davidson 2025).
- For structured or complex inputs, use JSON formatting for both input and expected output. LLMs trained on code corpora parse JSON reliably and produce more consistent structured output (Chae & Davidson 2025).
- Include the response text in the user message, separated clearly from instructions. Use a consistent delimiter (e.g., `"Code this response:\n\n{text}"`).
- Do not include information in the prompt that the classifier should not use. If country of origin should not influence coding, do not include it in the input — models will use any available signal.

### 5. Pilot Testing and Validation

- Before hand-labeling, run Halterman & Keith's (2025) Stage 1 label-free behavioral tests on the candidate LLM and codebook. These are cheap screens that require no ground truth: (I) **legal labels** — does the LLM only return labels defined in the codebook? (II) **definition recovery** — given a verbatim class definition as input, does it return the correct label? (III) **in-context example classification** — does it correctly label verbatim examples from the codebook? (IV) **codebook order invariance** — are predictions stable when the category order is reversed or shuffled? Failure on I–III indicates the model cannot follow basic instructions or recall codebook content; failure on IV indicates attention or ordering artifacts that will compromise downstream classification. Use these to screen out unsuitable models before committing to hand-coding.
- Hand-code 50-100 responses as ground truth before any LLM classification. This sample serves dual purposes: validating the codebook and benchmarking LLM performance.
- Use two independent human coders for the pilot sample. Report inter-coder reliability using Cohen's κ (Krippendorff's α is preferable for ordinal labels or >2 coders, and is the measure Tornberg 2025 and Benoit et al. 2025 report). The κ ≥ 0.7 threshold used here is a house default aligned with the "substantial agreement" band in Landis & Koch (1977); Halterman & Keith (2025) treat codebook revision as warranted when human agreement is low, without fixing a specific numeric cutoff. If human agreement falls below this band, the codebook needs revision before LLM testing — the problem is the coding scheme, not the model.
- Consider a **self-coding** diagnostic alongside inter-coder κ: pipe the open-ended response back to the respondent and ask them to assign it to the same categories. Agreement between respondent self-codes and researcher codes is a direct test of the codebook's semantic validity (Krippendorff's concept), and systematic disagreement correlated with demographic variables reveals demographic bias in the coding scheme (Glazier, Boydstun & Feezell 2021). This is particularly valuable for cross-national or cross-demographic work where a single researcher codebook may systematically mis-read some groups.
- Compare LLM output against the human-coded ground truth. Report per-category precision, recall, and F1. Halterman & Keith (2025) treat F1 ≥ 0.7 as adequate and recommend iteration when per-category F1 is low; the "below 0.5, consider fine-tuning" bright line is a house operationalization rather than a cited threshold.
- For error analysis, prompt the LLM to **motivate its label** ("explain briefly why this response fits this category") on misclassified and boundary cases. The justification often reveals whether the model is using the codebook's definition or a background concept, and it surfaces the kind of contextual reasoning that distinguishes LLM output from word-association-based classifiers (Tornberg 2025). This is a diagnostic, not a production setting — do not use chain-of-thought output as the classification itself.
- Examine the confusion matrix for systematic error patterns. If the model consistently confuses two categories, either merge them or sharpen the negative clarification in the codebook.
- If zero-shot F1 is inadequate, iterate in this order: (1) revise codebook definitions, (2) add few-shot examples, (3) fine-tune on labeled data. Do not skip to fine-tuning before testing whether the codebook is the problem (Halterman & Keith 2025).

### 6. Hybrid Human-LLM Workflows

- Implement a hybrid workflow: LLM classifies all responses, then human reviewers adjudicate uncertain cases. This achieves 93%+ accuracy at a fraction of full manual coding cost (Heseltine & Clemm von Hohenberg 2024).
- Flag responses for human review using one or more of: (a) LLM self-reported confidence (prompt the model to rate HIGH/MEDIUM/LOW), (b) disagreement across multiple model runs (Heseltine & Clemm von Hohenberg 2024), (c) responses assigned to the residual category, (d) responses near decision boundaries (e.g., coded with two competing labels). (a), (c), and (d) are plausible defaults consistent with the hybrid-workflow literature but are not each individually cited.
- Expect roughly 10–15% of responses to require human review, with anything over ~25% signaling codebook or model problems that warrant returning to pilot testing. These review-rate bands are house defaults for planning purposes, not thresholds established in any single cited study.
- Use human review not only for quality assurance but also for codebook refinement. Patterns in flagged cases often reveal systematic ambiguities that can be resolved with better definitions.
- For **ensemble approaches**, run a matrix of models rather than a single pair. Benoit, De Marchi & Laver (2025) use a 3×3 design — three summarizer models (Claude, GPT, Gemini) × three scorer models × zero/few-shot — and aggregate by taking the ensemble **mean** of the per-item scores. This ensemble mean correlates with expert-survey benchmarks on party positioning at or near the upper bound set by inter-expert agreement (~0.90 Pearson). Treat **NAs as informative missingness**: instruct models to return NA when the input lacks sufficient information rather than forcing a label, and report per-model NA rates — systematic NA differences between summarizers (e.g., GPT inferring content, Claude/Gemini declining to) are substantive findings about what the text contains, not just noise (Benoit et al. 2025).

### 7. Analysis and Interpretation

- Report code prevalence overall and by relevant subgroups (e.g., country, treatment condition). Present as proportions with confidence intervals.
- Cross-tabulate codes to assess co-occurrence. For construct validation, the joint prevalence of related codes (e.g., recognition of a cue + positive interpretation) is more informative than marginal prevalence alone.
- When using LLM classifications as variables in downstream analysis (regression, causal inference), acknowledge measurement error. Classification errors can attenuate or bias effect estimates. Even highly accurate LLM labels can induce severe bias and coverage problems when used as proxies in downstream estimation; the appropriate response is a design-based correction rather than ignoring the noise (Egami et al. 2023; Knox, Lucas & Cho 2022, via Halterman & Keith 2025; Chae & Davidson 2025). Distinguish classifier-as-outcome from classifier-as-treatment-check, and plan the correction procedure up front rather than post hoc. If the classification is part of a pre-registered design, register which codes map to which hypotheses; see `pre-registration-writing`.
- LLMs can outperform human coders on tasks requiring contextual reasoning — interpreting implicit references, handling sarcasm, drawing on background knowledge (Tornberg 2025). But LLMs are not oracles. Treat LLM classifications as one measurement instrument, not ground truth.

### 8. Reporting

- Document the full classification pipeline: model name and exact version, temperature and other generation parameters, complete prompt text, codebook, date of classification runs.
- Report validation metrics: per-category precision, recall, F1 against human-coded ground truth. Report overall accuracy and Cohen's Kappa.
- Report the variance test: agreement rate between repeated runs on the same subset.
- Report the human review rate: what proportion of responses were flagged and adjudicated.
- Archive the complete prompt, codebook, and classification code. If using a proprietary model, note the risk of future deprecation and specify whether results can be reproduced (Barrie, Palmer & Spirling 2025).
- State explicitly whether the LLM was used for discovery (exploring what codes might apply) or confirmation (applying pre-specified codes). If the codebook was revised after seeing LLM output, report the revision history. Iterative codebook refinement after inspecting LLM labels is a researcher degree of freedom that can silently inflate positive findings if left undocumented (Simmons, Nelson & Simonsohn 2011); transparent reporting of the revision trajectory, together with pre-specification of confirmatory categories, is the standard remedy (Nosek et al. 2018).
- When citing LLM-classified data in results, present representative examples for each code category. Readers need to assess whether the classification matches their substantive understanding (Glazier, Boydstun & Feezell 2021).
- For CONSORT/JARS-style flow reporting when classifications feed a sampled experiment, and for DA-RT compliance on archived prompts and classifier code, see `methods-reporting`. When the underlying category set is not fixed in advance and discovery of categories is itself the goal, unsupervised approaches may be more appropriate — see `topic-modeling`.

## Quality Checks

- [ ] Codebook includes all components per code: label, definition, clarification, negative clarification, examples (adapted from Halterman & Keith 2025)
- [ ] Learning regime (zero-shot, few-shot, fine-tuning, instruction-tuning, or encoder-only fine-tuning) chosen based on data characteristics and available resources, not convenience
- [ ] Exact model version documented (not just model family name)
- [ ] Stage 1 label-free behavioral tests (legal labels, definition recovery, in-context examples, codebook order invariance) run before hand-coding (Halterman & Keith 2025)
- [ ] Pilot sample of 50-100 responses hand-coded by two independent coders before LLM classification
- [ ] Inter-coder reliability reported (Cohen's κ, or Krippendorff's α for ordinal / >2 coders); codebook revised if agreement falls below the Landis & Koch "substantial" band
- [ ] Per-category precision, recall, and F1 reported against human ground truth
- [ ] Variance test conducted: same responses classified twice, agreement rate reported
- [ ] For multi-language or multi-country data, per-language validation against native-language ground truth (Heseltine & Clemm von Hohenberg 2024; Tornberg 2025)
- [ ] Hybrid workflow implemented: uncertain cases flagged and human-reviewed
- [ ] Human review rate reported (planning target: 10-15% of responses; >25% signals codebook/model problems)
- [ ] Complete prompt, codebook, and classification code archived for replication
- [ ] Reproducibility risk acknowledged if using proprietary models (Barrie, Palmer & Spirling 2025)
- [ ] Data privacy addressed: PII not sent to commercial APIs without policy review (Chae & Davidson 2025)
- [ ] Downstream analysis acknowledges measurement error from classification; if classifier labels feed causal estimation, design-based correction planned up front (Egami et al. 2023; Knox, Lucas & Cho 2022)
- [ ] Discovery vs. confirmation framing made explicit; codebook revision history documented if applicable

---
name: topic-modeling
description: Structural topic modeling: STM spec, topic count, coherence-exclusivity.
argument-hint: "[describe your corpus and research question]"
---

# Topic Modeling for Survey and Experimental Text Data

## Instructions

### 1. Model Selection

- Default to Structural Topic Models (STM) when analyzing text from surveys or experiments. STM incorporates document-level metadata — treatment conditions, respondent demographics, country — directly into estimation, allowing prevalence and content to vary with covariates (Roberts et al. 2014).
- Use standard LDA only when no document-level covariates are needed and the corpus is large enough for unsupervised discovery (Blei, Ng & Jordan 2003).
- Consider BERTopic when working with short texts where word co-occurrence is sparse, or when multilingual embedding-based similarity is required (Grootendorst 2022). BERTopic clusters document embeddings via HDBSCAN, which yields hard single-topic-per-document assignments (unlike STM/LDA mixed membership), c-TF-IDF topic words that can be unstable on small corpora, and no native covariate framework. Use it when embedding-based semantic similarity matters more than mixed-membership structure or covariate estimation.
- Recognize the distinction between topic categorization and attitude inference: topic models reveal what respondents *discussed*, not what they *believe*. If the goal is inferring latent attitudes rather than categorizing surface content, complement topic modeling with an embeddings-based scaling of contextually common words or a separate supervised classifier (Hobbs & Green 2025; see also the companion `text-classification` skill).

### 2. Preprocessing

- Make preprocessing decisions explicit and justify each choice. Preprocessing is not neutral — stemming, stopword removal, and term-frequency thresholds all affect which topics emerge (Denny & Spirling 2018).
- Lowercase all text. Remove punctuation and numbers unless they carry substantive meaning in the domain.
- Remove stopwords using a standard list, but inspect the list for domain-relevant terms that should be retained (e.g., "foreign" in immigration research).
- Apply stemming only after checking that it does not collapse substantively distinct terms. Compare results with and without stemming as a robustness check (Denny & Spirling 2018).
- Set a lower-frequency threshold to prune very rare terms, and express it as a fraction of documents rather than an absolute count so it scales with corpus size. For small open-ended corpora a fixed count of 2–5 documents is often appropriate; for larger corpora, pruning terms that appear in fewer than roughly 0.5%–1% of documents is a common starting point (Grimmer & Stewart 2013). In `stm`, use `plotRemoved()` to visualize how many documents and terms are dropped across candidate thresholds before committing to one, then pass it to `prepDocuments()`. Report the threshold chosen and the counts of terms and documents retained.
- For translated text, preprocess after translation. Note that translation artifacts (e.g., inconsistent phrasing across translators) may affect topic coherence — document any translation pipeline.

### 3. Model Specification

- Specify the prevalence formula to include theoretically relevant covariates. For survey experiments, include treatment conditions; for cross-national data, include country. Example: `prevalence = ~ treatment + country` (Roberts et al. 2014). For experimental applications, pre-register the prevalence-covariate hypotheses (see the companion `pre-registration-writing` skill) so that `estimateEffect()` outputs are confirmatory rather than exploratory by default (Nosek et al. 2018).
- Optionally specify a content formula when you expect the *words* associated with a topic (not just its prevalence) to vary by covariate — e.g., different framings of the same topic across countries or treatment arms. Content covariates parameterize word distributions via SAGE-style deviations from a baseline, which complicates direct comparison of β across groups; inspect group-specific vocabulary with `sageLabels()` and interpret with care (Roberts, Stewart & Tingley 2014; 2019).
- Use spectral initialization (`init.type = "Spectral"`) for reproducibility. Spectral initialization is deterministic on a given machine/BLAS configuration, unlike random initialization which requires multiple runs; cross-machine numerical precision can still produce minor differences, so record the hardware/OS when sharing replication materials (Roberts, Stewart & Tingley 2019).
- Set a random seed and record it regardless of initialization method. Also record the `stm` package version and R session info for DA-RT-compliant replication.

### 4. Selecting the Number of Topics

- Do not rely on a single metric. Evaluate candidate models across a range of K values (e.g., K = 5 to 30) using multiple diagnostics: semantic coherence, exclusivity, held-out likelihood, and residuals (Roberts, Stewart & Tingley 2019). In `stm`, `searchK()` sweeps over K and returns all four diagnostics at once; `selectModel()` fits multiple initializations at a fixed K and returns the coherence-exclusivity frontier (useful when spectral initialization is not being used).
- Semantic coherence measures whether high-probability words within a topic co-occur in the corpus. Higher is better, but coherence alone favors very common topics (Mimno et al. 2011). When a topic scores poorly, inspect the failure mode: Mimno et al. describe *chained* (two concepts linked by a shared word), *intruded* (unrelated words mixed in), *random* (no coherent connections), and *unbalanced* (mixes very general and very specific terms) — the diagnosis shapes whether the fix is K, preprocessing, or covariate specification.
- Exclusivity measures whether high-probability words are distinctive to one topic. The `stm` package reports FREX, a weighted harmonic mean of frequency and exclusivity ranks (default weight ω = 0.7). The coherence-FREX frontier identifies models that balance both (Roberts, Stewart & Tingley 2019).
- Treat held-out likelihood as one input among several, not the deciding metric. Chang et al. (2009) show that predictive likelihood can be *negatively* correlated with human interpretability — topic models that fit held-out words better are not necessarily more semantically coherent. When coherence, FREX, and held-out likelihood disagree, prefer interpretability (Chang et al. 2009).
- After narrowing candidates statistically, read the top words and representative documents for each topic. The final K should be interpretable — topics should be substantively meaningful and distinguishable from one another (Chang et al. 2009).
- Report the range of K values considered, the diagnostics used, and the rationale for the final choice.

### 5. Interpretation and Validation

- For each topic, report the top 10-15 words by probability and by FREX (frequency-exclusivity weighted). FREX words are often more interpretable because they are both common within the topic and rare outside it (Roberts, Stewart & Tingley 2019).
- Extract and read 3-5 representative documents per topic using `findThoughts()` or equivalent. Do not interpret topics from word lists alone — the documents provide essential context.
- Assign short substantive labels to each topic based on both word lists and representative documents. Labels should be descriptive (e.g., "economic contribution concerns") not technical (e.g., "Topic 7").
- Estimate covariate effects on topic prevalence using `estimateEffect()`. For experimental data, test whether treatment conditions significantly shift which topics respondents discuss. For cross-national data, test whether topic prevalence differs by country. Plot these effects with confidence intervals (Roberts et al. 2014). When testing many topics against a treatment, report corrections for multiple comparisons (e.g., FDR) alongside uncorrected estimates.
- To guard against spurious treatment-on-topic effects, use `permutationTest()` (Roberts, Stewart & Tingley 2014; 2019). The function permutes the treatment label and refits the STM, returning a null distribution of topic-level treatment effects against which the observed effect is compared — essentially a randomization inference check for `estimateEffect()`.
- For construct validation in survey experiments: check whether topics related to the intended construct (e.g., civic engagement) show higher prevalence among respondents exposed to relevant treatment conditions. A null prevalence effect is *suggestive* of a construct-validity problem but does not establish one — rule out alternative explanations first, including insufficient statistical power, a suboptimal K that splits or merges the construct topic, a content-covariate effect (the manipulation shifted *how* the topic was framed rather than *whether* it was discussed), and preprocessing choices that dropped construct-relevant vocabulary.

### 6. Robustness and Sensitivity

- Run the model at neighboring values of K (e.g., K-2, K+2) to check whether substantive conclusions are sensitive to topic count.
- Compare results with and without stemming as a preprocessing robustness check (Denny & Spirling 2018).
- If using STM, compare results with and without covariates to assess how much the covariate structure shapes the topic solution.
- For experimental data, verify that topic assignments are not driven by a small number of high-frequency terms. Inspect whether removing the single most common term in a topic changes its interpretation.

### 7. Reporting

- Report: preprocessing pipeline (stopwords, stemming, frequency thresholds, counts of documents and terms retained after `prepDocuments`), number of topics and selection rationale, initialization method, convergence diagnostics (max EM iterations and final variational lower bound), random seed, `stm` package version, and R session info. For the broader reporting checklist see the companion `methods-reporting` skill.
- Present a topic summary table with: topic number, label, top FREX words, prevalence (overall and by covariate group), and 1-2 example documents.
- When reporting covariate effects on prevalence, present coefficient estimates with confidence intervals. Visualize cross-group differences (e.g., side-by-side prevalence plots by country or treatment).
- Distinguish discovery from confirmation: topic modeling is exploratory. State explicitly which findings were anticipated and which emerged from the data. Treating every topic-level comparison as a hypothesis test without that distinction re-creates the researcher-degrees-of-freedom problem documented in the false-positive literature (Simmons, Nelson & Simonsohn 2011; Nosek et al. 2018). If using topics to validate constructs, frame findings in terms of whether the intended constructs appeared, not whether the model "confirmed" a hypothesis (Grimmer & Stewart 2013).
- Make replication materials available: analysis code, preprocessing decisions, and random seed. If the corpus cannot be shared, provide the topic-term matrix and document-topic proportions (Grimmer & Stewart 2013).

## Quality Checks

- [ ] Model type justified (STM vs. LDA vs. BERTopic) given data structure and research question
- [ ] Preprocessing decisions documented and justified (stemming, stopwords, thresholds)
- [ ] Number of topics selected using multiple diagnostics (`searchK` / `selectModel` over coherence, FREX/exclusivity, held-out likelihood, residuals) plus substantive interpretability
- [ ] Held-out likelihood vs. coherence disagreement resolved in favor of interpretability (Chang et al. 2009)
- [ ] Covariates included in prevalence (and, where justified, content) formula match the experimental or observational design; `sageLabels()` inspected when a content covariate is used
- [ ] Each topic interpreted using both word lists (probability + FREX) and representative documents via `findThoughts()`
- [ ] Covariate effects on topic prevalence estimated with `estimateEffect()` and reported with confidence intervals; multiple-comparison adjustment reported when testing many topics
- [ ] For experimental applications, `permutationTest()` run against the treatment covariate
- [ ] Robustness checks performed (alternative K, preprocessing variants, topic correlations via `topicCorr()`)
- [ ] Topics labeled descriptively based on content, not just numbered
- [ ] Discovery vs. confirmation framing made explicit; confirmatory topic-prevalence hypotheses pre-registered where feasible
- [ ] Random seed, initialization method, convergence diagnostics, and `plotRemoved()` / `prepDocuments` retention counts reported
- [ ] Replication materials (code, preprocessing pipeline, seed, `stm` version, R session info) available or planned

## Example

A minimal STM workflow for a survey experiment in which `df` holds one row per respondent with columns `open_ended_responses` (text) and `treatment_arm` (factor). The four stages — (a) preprocess, (b) sweep K, (c) refit with multiple initializations, (d) estimate treatment effects — map directly onto §§2–5. The four diagnostic functions (`searchK`, `selectModel`, `permutationTest`, `topicCorr`) should all appear in the final analysis script.

```r
# Minimal STM workflow: survey experiment with open-ended responses.
library(stm)
set.seed(20260418)

# (a) Preprocess and prune rare terms (see §2).
processed <- textProcessor(df$open_ended_responses, metadata = df)
plotRemoved(processed$documents, lower.thresh = seq(1, 20, by = 2))
prepped <- prepDocuments(processed$documents, processed$vocab,
                         processed$meta, lower.thresh = 5)

# (b) Sweep K over candidate values (coherence, exclusivity, held-out, residuals).
k_search <- searchK(prepped$documents, prepped$vocab,
                    K = c(5, 10, 15, 20),
                    prevalence = ~ treatment_arm,
                    data = prepped$meta, init.type = "Spectral")
plot(k_search)

# (c) At the chosen K, refit with multiple initializations; pick off the frontier.
k_chosen  <- 10
candidates <- selectModel(prepped$documents, prepped$vocab, K = k_chosen,
                          prevalence = ~ treatment_arm, data = prepped$meta,
                          runs = 20, init.type = "Spectral")
plotModels(candidates)
fit <- candidates$runout[[1]]

# (d) Estimate treatment effects on topic prevalence (§5); then permutationTest / topicCorr.
effects <- estimateEffect(1:k_chosen ~ treatment_arm, fit,
                          metadata = prepped$meta, uncertainty = "Global")
summary(effects)
```

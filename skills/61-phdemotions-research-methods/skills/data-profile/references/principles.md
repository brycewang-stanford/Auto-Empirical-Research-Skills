# Data Profile Principles

## 1. Date-aware, not date-frozen

Best practices for data documentation evolve. What was acceptable in 2020 (reporting only Cronbach's alpha) may be insufficient now (reviewers increasingly expect McDonald's omega and CFA-based reliability). Before generating any output, check the current state of reporting standards. Stamp every report with the date and standards consulted.

## 2. The codebook is the data's biography

A dataset without a codebook is usable by one person for a limited time. A dataset with a comprehensive codebook is usable by anyone, forever. Every variable needs a story: where it came from, what it measures, how it was collected, what its valid range is. This isn't overhead — it's the thing that makes the data a contribution.

## 3. Reliability is multi-faceted

Cronbach's alpha is the traditional measure, but it has known limitations (underestimates reliability for multidimensional scales, overestimates for long scales). McDonald's omega total is preferred as a model-based reliability coefficient. CFA-based reliability adds structural evidence. Report all available measures — reviewers appreciate thoroughness.

## 4. Demographics are not afterthoughts

The sample description is where readers decide whether results generalize to their population of interest. Report demographics completely, not just "M_age = 32.4." Break down by condition. Compare to the target population. Note any sampling limitations. This matters for external validity claims.

## 5. Scales deserve citations

Every multi-item scale has a source. Cite it. Even "standard" measures like purchase intention have original validation papers. Reviewers check this, and it strengthens the Methods section. If a scale was adapted, cite the original and describe the adaptation.

## 6. Machine-readable AND human-readable

The codebook should exist in two forms: a formatted HTML/docx that a human can browse, and a CSV/JSON that a machine can parse. The machine-readable version enables automated checks (is this variable in range?) and reuse (other researchers can validate against the schema).

## 7. Profile the processed data, reference the raw

The data profile should describe the analysis-ready dataset (processed), but reference back to the raw data where relevant. "N=523 after exclusions from N=612 raw responses" tells the full story. If cleaning was already done via `/data-clean`, integrate its CONSORT flow.

## 8. Anticipate the reviewer

Think about what Reviewer 2 will ask about the data. "What was the reliability?" "How were composites formed?" "Were there any attention check failures?" "What percentage of data was missing?" "Is the sample representative?" If you can answer it in the profile, do it proactively.

# Data Validation Principles

## 1. Check everything, assume nothing

Data that "looks fine" may contain subtle errors that propagate through every analysis. A single miscoded attention check item, a stray 999 that should be NA, a duplicated row from a survey platform glitch — any of these can invalidate results. Check systematically.

## 2. The codebook is as important as the validation

A validation report tells you what's wrong. A codebook tells you what the data IS. Both are essential. A dataset without a codebook is usable by one person for a limited time. A dataset with a codebook is usable by anyone forever.

## 3. Validation is descriptive, not prescriptive

Report what you find. Don't make cleaning decisions. "47 participants failed the attention check" is validation. "Remove 47 participants who failed the attention check" is cleaning. The researcher makes cleaning decisions; validation gives them the information to decide.

## 4. Leverage embedded metadata

SPSS .sav and Stata .dta files often contain variable labels, value labels, and missing value codes. These are gold — extract them and use them as the foundation for the codebook. Don't discard this information when converting to CSV.

## 5. Visual and statistical checks complement each other

A histogram reveals a bimodal distribution that a mean/SD summary hides. A missingness heatmap reveals patterns that a completeness percentage obscures. Use both numbers and visuals.

## 6. Domain knowledge matters

A value of 8 on a 7-point Likert scale is obviously wrong. A completion time of 30 seconds for a 20-minute survey is suspicious. A participant's age of 5 in a study of working professionals is impossible. These checks require knowing what the data represents — read the codebook (or help create it) before validating.

## 7. Report at the right granularity

"3.2% of values are missing" is too coarse. "Variable brand_authenticity_3 has 47% missing while all other items have <5%" is actionable. Report at the variable level, not just the dataset level.

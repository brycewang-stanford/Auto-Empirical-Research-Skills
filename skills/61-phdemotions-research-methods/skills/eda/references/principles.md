# EDA Principles

## 1. Describe before you test

Exploratory analysis comes before confirmatory analysis for a reason. You need to understand what the data looks like before you can sensibly model it. Skipping EDA is how researchers discover their regression violated every assumption — after submitting the paper.

## 2. Visualize, don't just summarize

A mean and SD can describe a perfectly normal distribution, a bimodal distribution, or a uniform distribution. Histograms, density plots, and Q-Q plots reveal shape. Scatterplots reveal nonlinearity that a correlation coefficient hides. Anscombe's quartet is the canonical lesson: always plot.

## 3. Let the data structure guide analysis choices

EDA findings directly inform analysis decisions. A strongly skewed DV suggests transformation or robust methods. High VIF among predictors demands variable selection or centering. Non-normal residuals point to GLM over OLS. Report these findings so the analyst can make informed choices.

## 4. Table 1 is not optional

Every empirical paper in business research has a Table 1 showing sample descriptives. This is where readers calibrate: who was studied, what the distributions look like, how variables relate. Generate it properly the first time — it will appear in the manuscript.

## 5. Flag, don't fix

EDA identifies concerns. It does not resolve them. "VIF for brand_loyalty and brand_commitment is 7.2" is an EDA finding. "Remove brand_commitment from the model" is an analysis decision. Report the finding; let the researcher decide.

## 6. Be thorough on key variables, selective on the rest

Run full diagnostics (distributions, outliers, assumption tests) on all variables named in hypotheses or the pre-registration. For demographic and control variables, descriptive summaries suffice. Don't generate 200 plots for 200 variables — focus on the ones that matter.

## 7. Correlations are the roadmap

The correlation matrix is where researchers first see whether their hypothesized relationships have any signal. It's also where they spot unexpected relationships worth exploring and multicollinearity worth addressing. Present it clearly with means, SDs, and significance indicators.

## 8. Assumption testing is diagnostic, not pass/fail

With large samples, every normality test will reject. With small samples, no normality test has power. Visual inspection (histograms, Q-Q plots, residual plots) often matters more than p-values from formal tests. Report both, but emphasize practical severity over statistical significance of assumption violations.

# Data Audit Checklist

Review the dataset in this order:

1. Structure: observations, variables, types, labels.
2. Summary statistics: missingness, ranges, obvious anomalies.
3. Key identifiers: duplicates, accidental many-to-many merges, unlabeled categories.
4. Variable readiness: missing labels, odd storage types, suspicious sentinel values.
5. Documentation readiness: what a coauthor or referee would need explained.

Useful targeted checks:

- `duplicates report id`
- `count if missing(var)`
- `tab var, missing`
- consistency checks with `assert`

Report:

- what was checked,
- concrete risks found,
- what appears clean,
- what still needs manual confirmation.

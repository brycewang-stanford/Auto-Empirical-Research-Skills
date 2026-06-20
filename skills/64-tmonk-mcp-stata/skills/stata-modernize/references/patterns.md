# Modernization Patterns

Prefer these replacements:

- `preserve` / `restore` -> frames and `frlink` / `frget`
- `regress y x i.fe` with large FE sets -> `reghdfe`
- `egen` aggregations on large data -> `gegen` / `gcollapse`
- `cd` and hard-coded working directories -> project locals or globals
- `#delimit ;` -> standard line continuation with `///`

When modernizing, explain:

- what the old pattern risks,
- why the replacement is better,
- whether the replacement depends on Stata 16+ or external packages.

# Authentication

Use authentication mechanisms supported by the installed official Kaggle CLI.
Prefer a process-level `KAGGLE_API_TOKEN`, an OAuth/access-token login managed
by Kaggle, or the legacy user-scoped `kaggle.json` file. Follow Kaggle's current
documentation for the chosen mechanism.

Credential values are external inputs, never research artifacts:

- Do not place them in command arguments, source files, audit files, reports,
  notebooks, fixtures, or shell history.
- Do not inspect or display the value to validate it. Use `doctor`, which makes
  a small authenticated metadata request and only reports success or a
  redacted error category.
- Do not copy a developer credential into the repository.
- Remove process-level credentials after a live verification session.

Authentication failures are classified separately from network/transient and
general command errors. Correct the external credential configuration; never
weaken TLS verification or commit a fallback secret.

# Testing, safety, and audit evidence

The test strategy has three lanes:

1. Standard-library unit and contract tests are offline, deterministic, and
   exercise command classification, policy enforcement, subprocess isolation,
   retry rules, redaction, path containment, hashing, CLI parsing, and report
   construction.
2. The live read-only integration test is enabled only with
   `AERS_KAGGLE_LIVE=1`. It uses the real installed CLI and Kaggle service; it
   does not replace service responses with mock data.
3. Remote write/delete verification is excluded from automatic tests. It is
   allowed only for an explicitly authorized disposable resource.

Run the offline suite:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

Run the opt-in live lane only after external credentials are configured:

```bash
AERS_KAGGLE_LIVE=1 python -m unittest discover -s tests -p "test_live_readonly.py" -v
```

## Safety invariants

- Subprocesses receive an argument array with `shell=False`.
- Credentials in arguments are rejected before process creation.
- Output paths cannot escape the approved root.
- Only read/download operations receive bounded retries.
- Captured streams are redacted, size-bounded, and hashed.
- Downloaded artifacts are enumerated deterministically with SHA-256 and size.
- Live reports contain command evidence but no credential values.

Keep audit/report files with the research run when they are meaningful
provenance. Do not commit downloaded datasets or ephemeral smoke output unless
the repository's data policy explicitly calls for them.

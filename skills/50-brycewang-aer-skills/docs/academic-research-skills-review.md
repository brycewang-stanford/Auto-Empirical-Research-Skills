# Academic Research Skills Reference Review

Date: 2026-06-22.

Reference inspected: https://github.com/Imbad0202/academic-research-skills

## What Transferred

The reference repository is a broad, multi-stage academic pipeline. Its useful
patterns for this AER-specific bundle are engineering patterns, not content to
copy wholesale:

- explicit claim-to-evidence contracts instead of prose-only integrity checks;
- small deterministic scripts that turn agent promises into gates;
- skeleton artifacts that users fill in during real manuscript work;
- validation that checks the skeleton artifacts and the skill prose stay wired
  together.

This patch adapts those ideas to `aer-consistency` by adding a lightweight
claim-evidence ledger. The ledger tracks each empirical claim in the abstract,
introduction, and conclusion to typed evidence:

- `label:<tex-label>` for manuscript exhibits;
- `cite:<bib-key>` for externally sourced facts;
- `file:<relative-output>` for generated table or figure files;
- `external:<note>` only when the evidence is deliberately outside the local
  package.

## What Did Not Transfer

The reference repository also ships a full Material Passport, cross-model
verification stack, hooks, slash commands, and large test fixture suite. Those
are intentionally not imported here. AER-Skills is a focused economics-journal
skill bundle; adding a general academic pipeline would blur ownership with the
existing `aer-workflow`, `aer-replication`, and `aer-submission` gates.

## Resulting Local Change

- `skills/aer-consistency/scripts/audit_manuscript.py` now accepts
  `--claim-ledger` and auto-detects `docs/claim-evidence-ledger.csv` in a
  manuscript directory.
- `examples/replication-package-skeleton/docs/claim-evidence-ledger.csv`
  provides the fill-in template.
- `scripts/validate_repo.py` validates the ledger template and requires
  `aer-consistency` to link it as a repository resource.

Acceptance gate: `make preflight`.

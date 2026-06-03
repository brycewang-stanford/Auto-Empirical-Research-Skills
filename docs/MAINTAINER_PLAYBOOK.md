# Maintainer Playbook

This playbook summarizes the routine maintenance loop for AERS.

## Weekly Loop

1. Review automated upstream-sync pull requests for StatsPAI and AER-skills.
2. Review Dependabot pull requests for GitHub Actions.
3. Check OpenSSF Scorecard findings in GitHub code scanning.
4. Run the local quality gate:

```bash
git fetch origin
make catalog
make check
make python-compat
git diff --check
```

## Skill Intake

Accept a new skill only when it is:

- Relevant to empirical research, causal inference, writing, replication, or journal workflows.
- Open source or source-available with a clear license.
- Independently runnable without a required paid/proprietary core path.
- Free of surprising hooks, credential exfiltration, reverse shells, hidden network callbacks, and prompt-injection instructions.
- Documented in the appropriate `docs/NN-*.md` workflow category.

For first-party flagship skills, add or update `evals/flagship-evals.json` so the behavior has a reusable regression prompt.

## Vendor Sync Review

For automated sync PRs:

- Confirm the upstream repository and branch match the workflow comments.
- Skim changed `SKILL.md`, scripts, hooks, and references before merging.
- Run `make catalog` if skill paths, frontmatter, or provenance-relevant content changed.
- Check that generated catalog and audit diffs are mechanical.

## Security Review

Focus manual review on:

- Shell execution, network calls, and install snippets.
- Environment-variable reads and credential handling.
- Hooks or agent instructions that can run automatically.
- Obfuscated, encoded, or unusually long lines.
- Instructions that tell an agent to ignore user, system, or repository policy.

If a finding is credible, remove or quarantine the affected entry until the upstream source is fixed or the risk is clearly documented.

## Release Review

Use [`docs/RELEASE.md`](RELEASE.md). Every release note should include catalog counts, license bucket changes, validation results, and known follow-ups.

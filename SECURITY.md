# Security Policy

Auto-Empirical Research Skills vendors many third-party skill repositories. Treat every new or updated skill as executable instructions for an AI agent, not as ordinary prose.

## Supported Scope

Security reports are accepted for:

- Malicious or surprising instructions in `SKILL.md`, references, hooks, scripts, or bundled assets.
- Credential exfiltration, reverse shells, arbitrary network callbacks, unsafe shell execution, or hidden payloads.
- Prompt-injection patterns that ask an agent to ignore user, system, or repository safety constraints.
- Misleading install instructions that fetch unreviewed code.

## Reporting

Please open a private security advisory if GitHub enables advisories for this repository. If not, open a minimal public issue that states "security report available" without exploit details, and the maintainers will coordinate a private channel.

Include:

- Affected path and commit SHA.
- Exact suspicious lines or files.
- Why the behavior is unsafe.
- Whether the issue comes from upstream or from AERS packaging.

## Maintainer Response

We aim to triage credible reports within 7 days. High-risk findings may result in temporarily removing or disabling a skill entry until the upstream source is fixed or clearly documented.

## User Guidance

- Prefer skills with clear licenses, minimal dependencies, and local/offline execution paths.
- Review hooks and scripts before enabling them in an agent runtime.
- Do not run vendored code with secrets in the environment unless the skill explicitly needs them and you trust the source.
- Re-run `make validate` after local edits.

## Automated Security Checks

- Dependabot monitors GitHub Actions updates through `.github/dependabot.yml`.
- OpenSSF Scorecard runs weekly and on pushes to `main`, with SARIF uploaded to GitHub code scanning.
- `make validate` includes a workflow policy check for explicit permissions, non-persistent checkout credentials, no `pull_request_target`, and no downloaded-script pipe-to-shell patterns.

# Skill Submission Guide

Use this guide when proposing a new skill or vendoring a new upstream collection into AERS.

## Acceptance Criteria

A skill should be:

- Relevant to empirical research, social science workflows, academic writing, replication, data work, or research automation.
- Open source or source-available with a clear license.
- Independently runnable or inspectable without a paid/proprietary core dependency.
- Safe for an agent to read: no credential exfiltration, reverse shells, hidden download-and-run behavior, or prompt-injection instructions.
- Documented enough that a researcher can tell when to use it.

## Required PR Contents

1. Add the vendored skill under `skills/NN-owner-repo/`.
2. Preserve upstream attribution in `README-original.md` when possible.
3. Preserve upstream `LICENSE` when present.
4. Add or update the relevant workflow-stage document under `docs/`.
5. Run:

```bash
make catalog
make validate
```

## Metadata Checklist

The generated provenance audit looks for:

- Source URL.
- License.
- Commercial-use status.
- Sync mode.
- Security review pointer.

If the generator cannot infer the right source or license, update `OVERRIDES` in [`scripts/build-provenance.py`](../scripts/build-provenance.py) with a narrow explicit override.

## Entry Template

```markdown
### Skill name

| 属性 | 说明 |
|------|------|
| **来源** | [owner/repo](https://github.com/owner/repo) |
| **License** | MIT |
| **功能** | One-line description of what the skill does |
| **安装** | `cp -R skills/NN-owner-repo/path ~/.codex/skills/name` |
| **适用** | Research stage and concrete use case |
```

## Reviewer Checklist

- Does the proposed skill overlap with an existing AERS flagship skill?
- Is the license compatible with redistribution in this catalog?
- Is any network or shell behavior expected and documented?
- Does `SKILL.md` contain usable `name` and `description` frontmatter?
- Should long details move into `references/` for progressive disclosure?

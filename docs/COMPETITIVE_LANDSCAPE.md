# Competitive Landscape

Scan date: 2026-05-31.

This note records the public repositories and directories used to sharpen AERS. The point is not to imitate general-purpose skill indexes, but to make AERS the best domain-specific index for empirical research.

## References Checked

| Project | What it does well | What AERS should adopt |
|---|---|---|
| [anthropics/skills](https://github.com/anthropics/skills) | Official reference implementation. It makes the core contract explicit: each skill is a self-contained folder with a `SKILL.md` file, required `name` and `description` frontmatter, optional scripts/references/assets, and examples/templates. | Keep AERS skill metadata machine-checkable; make the catalog deterministic; push first-party skills toward progressive disclosure. |
| [awesomeskills.dev](https://www.awesomeskills.dev/) | Search-first marketplace positioning: indexed skills, collections, resources, submit flow, and multilingual discovery. | Provide a generated `catalog/skills.json` and browsable `docs/SKILL_CATALOG.md` so AERS can power a future search UI. |
| [itgoyo/awesome-claude-code-skills](https://github.com/itgoyo/awesome-claude-code-skills) | Star-sorted awesome-list mechanics, concise contribution criteria, one-line descriptions, and visible "last updated" provenance. | Keep entries concise; require source, license, category, and one-line functional description in issues/PRs. |
| [kodustech/awesome-agent-skills](https://github.com/kodustech/awesome-agent-skills) | Broad multi-agent discovery with terse skill descriptions and compatibility framing across Claude Code, Codex, Cursor, and related coding agents. | Keep AERS installation docs runtime-agnostic and make each recommendation easy to copy into a coding-agent workflow. |
| [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) | Marketplace-style list with high volume, app/action positioning, and a contributor-friendly awesome-list shape. | Compete on quality gates, provenance, and empirical-research depth rather than raw count. |
| [huggingface/skills](https://github.com/huggingface/skills) | Domain-specific skill set for AI/ML workflows, with Codex/Claude/Gemini/Cursor install paths and fallback instructions. | Treat AERS as a specialist distribution: clear install paths, curated starter bundles, and a fallback "use without installing" path. |
| [NVIDIA/skills](https://github.com/NVIDIA/skills) | Verified catalog model: upstream source links, sync pipeline, install CLI, governance cards, evaluation datasets, and compatibility with the Agent Skills specification. | Move AERS toward source commit pins, review dates, evaluation prompts, and governance metadata for flagship skills. |
| [Agent Skills: A Data-Driven Analysis](https://arxiv.org/abs/2602.08004) | Shows that public skills are rapidly proliferating, often redundant, and can pose safety risks when they enable state-changing or system-level actions. | Differentiate by domain depth, provenance, security review, and empirical-research workflow organization rather than raw count alone. |
| [Agent Skills in the Wild: An Empirical Study of Security Vulnerabilities at Scale](https://arxiv.org/abs/2601.10338) | Reports concrete vulnerability classes in public skills, including prompt injection, data exfiltration, privilege escalation, and supply-chain risks. | Keep AERS validation conservative, separate non-blocking hygiene audits from blocking checks, and continue reviewing executable content carefully. |
| [Malicious Agent Skills in the Wild](https://arxiv.org/abs/2602.06547) | Emphasizes supply-chain impersonation, shadow features, and instruction manipulation as ecosystem-level risks. | Make source provenance visible, avoid silent vendoring, and require explicit license/source metadata for new submissions. |

## Positioning

AERS should be framed as:

- The empirical-research specialist, not a general agent-skill marketplace.
- A bridge between skill discovery and runnable research workflows.
- A security-audited, license-aware, reproducibility-focused catalog.
- A practical on-ramp to StatsPAI, AER-skills, and other high-value causal-inference workflows.

## Gaps Fixed In This Pass

- Added deterministic generated catalog outputs.
- Added repository validation and CI.
- Added contribution, issue, and pull request templates that collect source/license/category data.
- Added security, citation, and conduct files expected by serious open-source users.
- Added a browser-friendly static search page over the generated catalog.
- Added generated provenance and license audit outputs.
- Added generated non-blocking skill hygiene audit outputs.
- Added install/use guidance for Codex, Claude-style local skill folders, project-local use, and no-install browsing.
- Added flagship demos for StatsPAI IV cards, AER submission preflight, and Chinese de-AIGC workflows.
- Added release notes, changelog discipline, and a scheduled external-link check workflow.
- Normalized all detected lowercase `skill.md` files to exact-case `SKILL.md`.

## Next Competitive Moves

- Add vendored commit SHAs and upstream sync dates for each imported collection.
- Add security-review dates and risk levels for skills that include scripts, shell commands, or external API usage.
- Add screenshot/preview artifacts for `docs/search.html`, `docs/demos/`, and the first-page README experience.
- Add small frozen evaluation prompt sets for flagship empirical workflows: DID, IV, replication package, AER submission, Chinese de-AIGC, and data-to-paper.
- Add benchmark badges once the evaluation set is stable enough to avoid gaming the examples.

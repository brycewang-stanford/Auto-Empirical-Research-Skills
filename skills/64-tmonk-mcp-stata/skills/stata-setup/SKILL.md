---
name: stata-setup
description: Install, configure, update, or verify mcp-stata across Claude Code, Codex, Gemini CLI, Cursor, Windsurf, and VS Code. Activate when users ask to set up the Stata toolkit or troubleshoot the installation.
---

# Setup and Verification

Use the shared installer and verification flow instead of hand-writing per-agent config unless the user explicitly asks for manual steps.

## Preferred Install Commands

Project-shared install:

```bash
bash plugin/install.sh --scope project
```

Personal install:

```bash
bash plugin/install.sh --scope user
```

Specific agent:

```bash
bash plugin/install.sh --agent codex
```

Pin a version if a lab wants to:

```bash
bash plugin/install.sh --version 2.5.1
```

Offline/local source:

```bash
bash plugin/install.sh --local-source /path/to/mcp-stata
```

Live verification:

```bash
bash plugin/install.sh --verify
```

## What the Installer Does

- Uses the canonical server id `mcp-stata`
- Writes project-scoped configs where the client supports them
- Falls back to user-scoped config where project scope is not first-class
- Installs Codex skills into the Codex skills directory
- Installs the Gemini extension from `plugin/gemini-extension.json`
- Registers shared `~/.agents/skills/mcp-stata` symlinks for compatible agents
- Supports latest-by-default installs and explicit version pinning

## Verification Standard

When the user asks whether setup is complete, verify more than “the file exists”:

1. Stata discovery and edition
2. `uv` / `uvx` availability
3. package availability for `reghdfe` and `gtools`
4. graph-export readiness
5. log-path emission for command output
6. startup/profile behavior

If live verification is not possible on the current machine, state exactly what remains unverified.

## Troubleshooting

- If Stata is not discovered, tell the user to set `STATA_PATH`.
- If a user-managed machine blocks temp files, logs, or graph export, use the **stata-environment-diagnose** skill.
- If project-wide configs are undesirable, re-run with `--scope user`.

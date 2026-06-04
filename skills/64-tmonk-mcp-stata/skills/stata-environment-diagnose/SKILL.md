---
name: stata-environment-diagnose
description: Diagnose local Stata, MCP, package, startup, graph-export, and permissions issues. Use when setup is failing, Stata is not discovered, packages are missing, logs are truncated, or a managed machine behaves differently from a normal workstation.
---

# Environment Diagnose

Use this skill for setup and platform troubleshooting.

1. Verify detection with `stata_manage_session(action="detect")`.
2. Reproduce the smallest failing command.
3. Use logs, package checks, and environment reporting before suggesting a fix.
4. Separate root cause, evidence, remediation, and verification.

Read `references/troubleshooting.md` for the diagnosis flow and use `scripts/report_environment.py` for a deterministic environment summary.

---
name: stata-modernize
description: Improve, modernize, and optimize existing Stata code for performance, portability, and maintainability. Use when legacy patterns such as preserve/restore, cd, #delimit, slow aggregation, or weak fixed-effects workflows appear in code under review.
---

# Modernize Stata

Use this skill when a user wants stronger Stata code, not just working Stata code.

1. Identify the current anti-patterns.
2. Recommend or implement modern replacements with clear rationale.
3. Favor frames, `reghdfe`, `gtools`, portable paths, and explicit state handling.

Read `references/patterns.md` for common replacements and examples.

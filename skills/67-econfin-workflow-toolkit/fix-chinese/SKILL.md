---
name: fix-chinese
description: PROACTIVE SKILL — automatically apply whenever writing, generating, or editing any text that is mainly in Chinese. No user trigger needed. Also use when the user explicitly asks to "fix Chinese", "修改中文", "去翻译腔", "去AI味", "fix Chinese formatting", or "review Chinese text". Eliminates AI-sounding expressions and translation artifacts. Enforces Chinese-English mixed formatting rules (spacing, punctuation, bold formatting).
---

# Fix Chinese Writing

Review the provided text or file and apply all fixes below. Make edits in-place.

## Anti-AI / Anti-Translation Style

- Write natural, fluent Chinese as a native speaker would
- Remove these phrases on sight: "值得注意的是", "需要强调的是", "总而言之", "综上所述", "这不是科幻"
- Reduce overuse of "的" — restructure sentences instead
- Replace stiff passive voice with active constructions
- Break up long attributive clauses (定语从句) into shorter sentences
- Cut empty filler and overly polite expressions
- Do not add quotation marks unless necessary

## Chinese-English Mixed Formatting

- Half-width space between Chinese and English/numbers: `Claude Code 是`, `第 1 章`
- Full-width punctuation in Chinese context, half-width in English/code context
- Keep proper nouns in English: Claude Code, MCP, Skills, GitHub, Vibe Coding
- When bold Chinese text is followed by more text, add a space after the bold: `**这里** 和**那里**`

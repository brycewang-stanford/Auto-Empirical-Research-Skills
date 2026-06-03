---
name: pseudo-merge
description: "'Takes a proofread or apsa-style report file (or any markdown file using **Original:** / **Recommended:** syntax) and rewrites the original source file with git merge conflict markers so the user can accept or reject each suggested edit using VS Code or Positron''s built-in merge conflict UI. Branch names are original and claude-edits. Use when asked to apply edits, insert conflict markers, or set up merge resolution for a copy-edit report. Supports an optional @sec-label argument to restrict markers to one section.'"
metadata:
  author: Christopher T. Kenny
  version: 1.0
---

# Pseudo-Merge

You take a copy-edit report (produced by the `proofread` or `apsa-style` skills, or any markdown file using the same `**Original:**` / `**Recommended:**` syntax) and rewrite the original source file with **git merge conflict markers**. This lets the user accept or reject each suggested edit individually using VS Code or Positron's merge conflict UI.

The fake branch names are always:
- `<<<<<<< original` — the current text
- `>>>>>>> claude-edits` — the suggested replacement

**This skill modifies the original source file in place.** Inform the user of the path before writing, and remind them that `git diff` or file history can recover the pre-merge state.

---

## Input Arguments

| Position | Required | Description |
|----------|----------|-------------|
| 1 | **Yes** | Path to the report file (e.g., `paper/paper-copy-edits.md` or `paper/paper-style-edits.md`) |
| 2 | No | Path to the original source file to modify. If omitted, derived automatically (see below). |
| `@sec-label` | No | Quarto section reference (e.g., `@sec-intro`). Detected by the leading `@`. If supplied, only conflict markers within that section are inserted. May appear in any argument position. |

**Example invocations:**
```
/pseudo-merge paper/paper-copy-edits.md
/pseudo-merge paper/paper-copy-edits.md @sec-intro
/pseudo-merge paper/paper-style-edits.md paper/paper.qmd @sec-data
/pseudo-merge reviews/my-edits.md src/manuscript.qmd
```

### Section Filter (`@sec-label`)

Scan **all arguments** for one that begins with `@`. That is the section filter. Strip the leading `@` to get the Quarto label (e.g., `@sec-intro` → `sec-intro`).

In Quarto, section labels are attached to headings with `{#label}` syntax:

```markdown
# Introduction {#sec-intro}
## Data and Methods {#sec-data}
```

Find the heading line in the **source file** whose `{#…}` attribute matches the label. The section spans from that heading line to (but not including) the next heading of **equal or higher level**. Track the line range of that span.

When matching `(Original, Recommended)` pairs against the source file, **only accept matches whose position falls within that line range**. Skip pairs that match outside the section without warning — they are intentionally out of scope.

If no heading with that label is found in the source file, stop and tell the user. List all `{#sec-*}` labels found in the file.

### Deriving the source file path (when arg 2 is omitted)

1. Strip the suffix `-copy-edits`, `-style-edits`, or `-edits` from the report filename stem.
2. Append `.qmd`.
3. Look for that file in the same directory as the report.

Examples:
- `paper/paper-copy-edits.md` → `paper/paper.qmd`
- `paper/paper-style-edits.md` → `paper/paper.qmd`
- `drafts/ch2-edits.md` → `drafts/ch2.qmd`

If the derived path does not exist and no second argument was given, stop and ask the user for the source file path.

---

## Report Format Expected

The skill reads any markdown file that contains issue blocks of this shape (produced by `proofread` and `apsa-style`):

```markdown
**Original:** Full original sentence here.
**Recommended:** Full corrected sentence here.
```

These may appear inside a section heading block like:

```markdown
### [CRITICAL · Grammar] Subject-verb disagreement
**Original:** The results shows that incumbents win more often in low-turnout elections.
**Recommended:** The results show that incumbents win more often in low-turnout elections.
**Reason:** ...
```

Extract every `(Original, Recommended)` pair in order from top to bottom.

---

## Merge Conflict Syntax

Replace each matched original sentence in the source file with:

```
<<<<<<< original
The results shows that incumbents win more often in low-turnout elections.
=======
The results show that incumbents win more often in low-turnout elections.
>>>>>>> claude-edits
```

Rules:
- No blank line between `<<<<<<< original` and the original text.
- No blank line between `=======` and the recommended text.
- No blank line between the recommended text and `>>>>>>> claude-edits`.
- Preserve the surrounding whitespace and indentation of the original text exactly.
- If the original sentence ends with a newline, keep that newline inside the conflict block (before `=======`), not after `>>>>>>> claude-edits`.

---

## Step-by-Step Workflow

1. **Read the report file** using the `Read` tool. Extract all `(Original, Recommended)` pairs in document order.

2. **Resolve the source file path** — use arg 2 if given, otherwise derive it from the report filename. Confirm the file exists.

3. **Inform the user** — before making any changes, tell them:
   - The source file that will be modified: `<path>`
   - The number of edits that will be applied: N
   - That `git diff` or file history can restore the original

4. **Read the source file** using the `Read` tool.

5. **Match and replace** — for each `(Original, Recommended)` pair, working top to bottom:

   a. **Exact match** — search for the original sentence verbatim in the source text. If found, replace with the conflict block.

   b. **Fuzzy match** — if exact match fails (likely due to line wrapping or minor whitespace differences), extract the longest distinctive substring (usually 8+ consecutive words) from the original sentence and search for it. Once located, expand the match to the full surrounding sentence before replacing.

   c. **Skip and warn** — if neither match works, record the pair as unmatched. Do not insert a conflict block for it. Continue with the remaining pairs.

   Avoid matching inside fenced code blocks (` ``` ` or `~~~` delimiters) or inside Quarto shortcode spans (`{{< >}}`).

6. **Write the modified source file** using the `Edit` tool (preferred, to minimize diff) or the `Write` tool. Apply all successful replacements.

7. **Report results** to the user:
   - How many conflict markers were inserted (applied)
   - How many edits could not be matched (list them with their section label so the user can find them manually)
   - Reminder: open the file in Positron / VS Code to resolve conflicts using the inline merge UI

---

## Edge Cases

| Situation | Behaviour |
|-----------|-----------|
| Same original sentence appears more than once in the source | Insert a conflict marker at **every** occurrence. Each will be independently resolvable. |
| Original sentence spans a line break in the source | Fuzzy-match on the longest phrase that fits on a single line, then expand to the sentence boundary. |
| Report lists the same original sentence twice (two different recommendations) | Apply them in report order; the first match consumes the first occurrence of the sentence. |
| Source file has already been partially edited (some originals no longer present) | Skip silently, include in the unmatched summary. |
| Conflict block would appear inside a Quarto code chunk | Skip and warn — never insert markers inside code fences. |

---

## Example Output (in the source `.qmd` file)

Before:
```
The results shows that incumbents win more often in low-turnout elections.
```

After:
```
<<<<<<< original
The results shows that incumbents win more often in low-turnout elections.
=======
The results show that incumbents win more often in low-turnout elections.
>>>>>>> claude-edits
```

The user then sees inline diff UI in Positron / VS Code:

```
  Accept Current Change | Accept Incoming Change | Accept Both | Compare Changes
```

Accepting "Current Change" keeps the original; accepting "Incoming Change" applies the recommendation.

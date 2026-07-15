---
name: ssci-polish
description: Polish English academic papers for SSCI journal submission. This skill checks grammar, improves readability, and enhances academic tone. Use when the user asks to polish, proofread, edit, or improve their English academic paper, manuscript, or article — especially when targeting SSCI, SCI, or other international journals. Also use when the user asks to "润色", "修改语法", "提升学术性", "polish my paper", or mentions their paper needs language improvement for journal submission. Always trigger on any request involving academic English polishing, even if the user doesn't explicitly say "SSCI."
author: 刘松岐 | 辽宁大学 | copaper.ai团队培训班
---

# SSCI Paper Language Polishing

> **作者**: 刘松岐（辽宁大学）| copaper.ai 团队培训班学员

Polish English academic manuscripts for submission to SSCI/SCI journals. This skill integrates principles from three authoritative writing guides:

- **Strunk & White**, *The Elements of Style* (4th ed.) — grammar and fundamental writing rules
- **Deirdre N. McCloskey**, *Economical Writing* (3rd ed.) — clarity and style for economics and social sciences
- **William Thomson**, *A Guide for the Young Economist* (2nd ed.) — technical writing and notation standards

## Workflow

When asked to polish a paper, follow this three-pass approach:

### Pass 1: Grammar and Mechanics
Fix objective errors first:
- Subject-verb agreement, pronoun case, possessive forms
- Comma splices, sentence fragments, run-on sentences
- Misused words (affect/effect, imply/infer, disinterested/uninterested, etc.)
- Punctuation errors (commas, semicolons, colons, quotation marks)
- Spelling and typos

Refer to `references/grammar.md` for the complete grammar rule checklist.

### Pass 2: Style and Readability
Improve clarity and fluency:
- Replace passive voice with active voice where possible
- Omit needless words (the single most important rule)
- Put statements in positive form; avoid "not" as evasion
- Use definite, specific, concrete language
- Express parallel ideas in parallel form
- Avoid elegant variation — use one word for one concept
- Place emphatic words at the end of sentences
- **Split sentences > 40 words.** Long sentences bury the main point and exhaust the reader (Thomson §4.3). Break them at logical pause points: before "and," "which," "while," "whereas," or between major clause boundaries. Aim for 15–25 words per sentence in results and methods sections. Exceptions: variable definition lists and questionnaire items in the data section.
- Remove qualifiers (*very, rather, little, pretty*)
- Remove boilerplate (*This paper discusses..., The outline is as follows..., As we shall see...*)

Refer to `references/style.md` for the complete style rule checklist.

### Pass 3: Academic Tone and Technical Precision
Enhance academic rigor:
- Verify consistent and mnemonic notation
- Ensure all technical terms are defined before use
- Separate formal definitions from interpretations
- Present assumptions in decreasing order of plausibility
- State results before proofs; use consistent formats for theorems
- Use words, not just symbols, in key equations
- Ensure tables, graphs, and figures are self-explanatory with declarative titles
- Check that the literature review tells a story, not an enumeration
- Verify that the introduction is hook-driven, not "This paper..." boilerplate
- Remove academic pose (*not only...but also*, excessive *however*, *due to*, *the fact that*)

Refer to `references/academic.md` for the complete academic standards checklist.

## Output Format

When polishing, show results in this structure:

### Summary of Changes
Briefly list what was fixed at each pass level.

### Polished Text
Present the full polished text. If only sections were edited, clearly mark which sections.

### Change Log (optional, for tracking)
List specific changes with before/after comparisons for major revisions. Use this format:
- **Line/Paragraph**: brief reason → `"before"` → `"after"`

## Key Principles to Apply by Default

These rules from the three books should be applied in every polishing session unless the user specifies otherwise:

1. **Omit needless words** (Strunk Rule 17) — the cardinal rule. Every word must tell.
2. **Use active voice** (Strunk Rule 14) — *We estimated the model...* not *The model was estimated...*
3. **Be concrete** (McCloskey Rule 27) — Prefer *bread and beer* to *consumables*, *ships and spindles* to *capital equipment*.
4. **One word, one meaning** (McCloskey Rule 20) — Don't vary terms just for elegance.
5. **Express parallel ideas in parallel form** (Strunk Rule 19) — *The positive rule is X; the negative rule is Y.*
6. **Place emphasis at the end** (Strunk Rule 22) — The most important idea goes last.
7. **Write with nouns and verbs** (Strunk Ch.V Reminder 4) — Adjectives and adverbs are secondary.
8. **Be clear above all** (McCloskey Rule 4) — "Write not merely so that the reader can understand, but so that he cannot possibly misunderstand" (Quintilian).

## Interaction Guidelines

- For short passages (<500 words): apply all three passes and present the full polished version.
- For full papers: ask the user whether to polish the whole document or specific sections. If the whole document, work section by section, starting with the abstract and introduction.
- Always explain the rationale behind major changes, referencing the specific rule from the source books.
- If the user's meaning is ambiguous, ask for clarification rather than guessing.
- Respect the author's voice — don't over-polish. The goal is clarity and correctness, not uniformity.

## Important: What NOT to Change

- Technical terminology that is standard in the field
- Statistical/mathematical notation that is consistent and clearly defined
- Citations and reference format (unless obviously broken)
- The author's substantive arguments or conclusions
- Field-specific jargon that is necessary for precision (but flag it if a plainer alternative exists)

## Additional Grammar Checks

Beyond the standard grammar rules, always verify:
- **Sentence-initial capitalization**: every word immediately after a period (`.`) must begin with a capital letter, excluding abbreviations (e.g., i.e., e.g., etc., et al.). This applies to all prose paragraphs.
- **Consistent abbreviation casing**: variable abbreviations in text (e.g., "Cr", "Inf") must match their definitions in tables exactly — do not change their case unless the table is also updated.
- **Proper noun capitalization**: "the Internet" (capitalized in formal academic writing), proper names of policies, institutions, and databases.
- **Double spaces** after periods within a sentence (e.g., between a citation and the next word) — these are typos, not the old typewriter convention.
- **Sentence length**: prose sentences exceeding 40 words must be split. Use this detection code during Step 2:
```python
import re
for i, p in enumerate(doc.paragraphs):
    for s in re.split(r'(?<=[.!?])\s+', p.text.strip()):
        if len(s.split()) > 40:
            print(f"P{i} ({len(s.split())}w): {s[:120]}...")
```
Only flag sentences in prose paragraphs (skip table cells, figure captions, and variable definition lists). Split at natural break points: before coordinating conjunctions (and, but, or), relative pronouns (which, that), or between major clause boundaries.

## DOCX Editing Workflow

**CRITICAL**: Use python-docx, not hand-rolled XML surgery. The unpack→lxml→repack approach has a known bug where `apply_tc` corrupts text that spans multiple `<w:t>` elements, creating duplicate paragraph fragments. python-docx handles all OOXML internally and cannot introduce this class of bug.

### Step 1: Read and Analyze
Use python-docx to extract ALL text (body + table cells):
```python
from docx import Document
doc = Document("input.docx")
all_paras = list(doc.paragraphs)
for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            for para in cell.paragraphs:
                all_paras.append(para)
for p in all_paras:
    print(p.text)
```

### Step 2: Apply Three-Pass Check
Go through ALL paragraphs systematically against the grammar.md, style.md, and academic.md checklists. Document every issue found, then compile the final change list. Only include changes that are definite errors or clear improvements — do not over-polish.

### Step 3: Apply Changes (python-docx, format-preserving)

**CRITICAL**: Before clearing any paragraph, capture its original formatting from the first run. Apply this formatting to all new runs so the output matches the original document.

```python
from docx.shared import Pt, RGBColor, Emu
from docx.oxml.ns import qn
RED = RGBColor(0xFF, 0x00, 0x00)

def get_para_format(para):
    """Capture font name, size, and bold/italic from the paragraph's first run."""
    if para.runs:
        first = para.runs[0]
        return {
            'name': first.font.name,
            'size': first.font.size,
            'bold': first.font.bold,
            'italic': first.font.italic,
        }
    # Fallback: use paragraph style defaults
    style = para.style
    return {
        'name': style.font.name if style.font.name else 'Times New Roman',
        'size': style.font.size if style.font.size else Pt(12),
        'bold': style.font.bold if style.font.bold else False,
        'italic': style.font.italic if style.font.italic else False,
    }

def apply_format(run, fmt):
    """Apply captured formatting to a run."""
    if fmt['name']: run.font.name = fmt['name']
    if fmt['size']: run.font.size = fmt['size']
    run.font.bold = fmt['bold']
    run.font.italic = fmt['italic']

for old, new in CHANGES:
    for para in all_paras:
        idx = para.text.find(old)
        if idx == -1: continue

        fmt = get_para_format(para)
        before = para.text[:idx]
        after = para.text[idx + len(old):]

        # para.clear() preserves paragraph-level formatting
        # (alignment, spacing, indentation) but removes all runs
        para.clear()

        if before:
            r = para.add_run(before)
            apply_format(r, fmt)

        r = para.add_run(new)
        apply_format(r, fmt)
        r.font.color.rgb = RED

        if after:
            r = para.add_run(after)
            apply_format(r, fmt)
        break
```

**Why this preserves formatting:**
- `para.clear()` keeps paragraph-level properties (`<w:pPr>`): alignment, line spacing, indentation, widow control.
- `get_para_format()` reads the original font name, size, bold, and italic from the paragraph's first run before clearing.
- Each new run gets this captured formatting applied, so the output matches the original.
- Table cell paragraphs are handled the same way — each cell's formatting is captured independently.

### Step 4: Verify Before Saving
```python
# Check for duplicate paragraphs
seen = {}
for i, p in enumerate(all_paras):
    txt = p.text.strip()
    if len(txt) > 150 and txt in seen:
        print(f"WARNING: P{seen[txt]} == P{i}")
    else:
        seen[txt] = i

# Check key phrases haven't multiplied
import re
for phrase in ["access to and understanding", "new-type agricultural"]:
    count = sum(1 for p in all_paras if phrase in p.text)
    # Count should not exceed expected occurrences

doc.save("output.docx")
```

### Step 5: Save
```python
doc.save("output.docx")
```

### Limitations of This Approach
- **Inline mixed formatting** (e.g., part of a paragraph bold, part italic) is simplified to the paragraph's primary formatting. For academic papers where body text is uniform, this is acceptable.
- **Changes are marked with red font color** (not Word Track Changes). This is more reliable across Word versions and avoids XML corruption.
- **Images, equations, headers, footers, page layout, paragraph spacing, and alignment** are fully preserved.

## Common Pitfalls

- **Never use unpack→lxml→hand-edit→repack for tracked changes.** The `apply_tc` function that inserts `<w:del>` and `<w:ins>` corrupts text spanning multiple `<w:t>` elements. This bug has been confirmed across multiple test runs.
- **Never mix body paragraphs and table cell paragraphs in the same iteration loop.** python-docx's internal state becomes inconsistent when some paragraphs in a mixed list are cleared via `para.clear()`, causing table cell contents to shift en masse (confirmed: 700+ paragraphs affected). Iterate `doc.paragraphs` only; accept that changes in table cells will be missed.
- **Never create a new document from scratch** (e.g., with docx-js) — this strips tables, images, and equations.
- **Never apply paragraph splits** — the XML surgery to insert `<w:p>` elements frequently creates sentence fragments.
- **Always verify** by checking that `len(orig.paragraphs) == len(polished.paragraphs)` and that prose body paragraphs have no duplicates (>150 chars).

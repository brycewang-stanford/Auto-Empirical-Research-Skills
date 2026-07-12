---
name: copy-edit-master
description: Professional academic copy-editing with multi-stage progressive revision for manuscripts, papers, and dissertations. Supports both general academic writing and theory papers. Use when editing academic papers, improving writing quality, or when user mentions copy-edit, revision, or academic writing improvement. Works with .md, .tex, and .docx files.
allowed-tools: Read, Edit, Write, Grep, Glob, Bash, TodoWrite, Task, AskUserQuestion, Skill
---

# Academic Copy-Edit Master

Professional, systematic copy-editing for academic writing using a multi-stage progressive revision approach. Automatically detects paper type and applies appropriate editing workflow.

## Overview

This skill orchestrates comprehensive academic copy-editing based on established principles from:
- Strunk & White's style rules
- McCloskey's writing principles
- Thomson's theory paper guidelines

**Two workflows available**:
1. **General Academic** (2 stages): Structure → Line Edit + Proofread
2. **Theory Papers** (5 stages): General Structure → Theory Refinement → Technical Elements → General Line Edit → Theory Line Edit

## Quick Start

The user will invoke you with a file path. Example:
```
Copy-edit papers/draft.md
```

## Instructions

### Phase 0: Workspace & Backup Creation

**Purpose**: Create a dedicated workspace directory next to the manuscript that holds the backup and all stage/review reports, keeping the paper directory clean.

**Step 1: Extract file information**

Parse the user-provided document path:
```bash
original_path="[user_provided_path]"
filename=$(basename "$original_path")
manuscript_name="${filename%.*}"
file_ext="${filename##*.}"
dir_path=$(dirname "$original_path")
```

**Step 2: Create workspace directory**

Create a date-stamped workspace inside the paper's directory. If a workspace for today already exists (from a previous interrupted run), reuse it rather than creating a new one:
```bash
datestamp=$(date +%Y%m%d)
workspace_dir="$dir_path/copy-edit-workspace-${datestamp}"
mkdir -p "$workspace_dir"
```

**Step 3: Copy backup into the workspace**

Place the backup *inside* the workspace (not next to the original):
```bash
backup_path="$workspace_dir/${manuscript_name}.backup.${file_ext}"
cp "$original_path" "$backup_path"
```

**Step 4: Inform user**

Output workspace and backup information:
```
🗂️  WORKSPACE CREATED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Editing file: $original_path
Workspace:    $workspace_dir
Backup:       $backup_path

✓ Workspace created in paper directory
✓ Backup copied into workspace before editing
✓ All edits will be made in-place on the original file
✓ All stage reports & review reports will be saved in the workspace
```

**Step 5: Store variables for subsequent phases**

Store these variables for use throughout the workflow:
- `$original_path` - File to be edited (used in ALL subsequent phases)
- `$workspace_dir` - **Dedicated workspace** for backup and ALL reports (use this for every stage/review report)
- `$backup_path` - Backup file location inside the workspace (for recovery if needed)
- `$dir_path` - Original paper directory (parent of workspace; use only for git context)
- `$filename` - Filename with extension
- `$manuscript_name` - Filename without extension

**CRITICAL**:
- All subsequent phases edit `$original_path` directly. The backup at `$backup_path` preserves the original content.
- All stage reports and review reports MUST be written under `$workspace_dir`, NOT `$dir_path`.

### Phase 1: Initial Analysis

**Step 1: Read the document**
- Use Read tool on `$original_path` for .md and .tex files
- Use Skill tool with document-skills:docx on `$original_path` for .docx files
- Read the entire document to understand content and structure

**Step 2: Analyze document type**

Determine if this is a **theory paper** by checking for:
- Formal theorems, propositions, lemmas, corollaries
- Mathematical proofs (with QED or ∎ markers)
- Formal model notation (heavy use of mathematical symbols)
- Definitions section with formal mathematical definitions
- Axioms or assumptions stated formally

**Classification criteria**:
- **Theory paper** (HIGH confidence): 3+ formal theorems/propositions with proofs
- **Theory paper** (MEDIUM confidence): Formal model section + mathematical notation throughout
- **General academic** (DEFAULT): Empirical analysis, qualitative research, or limited formal modeling

**Step 3: Present analysis to user**

Output analysis in this format:

```
📊 DOCUMENT ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Document: [filename]
Type detected: [Theory Paper / General Academic]
Confidence: [HIGH / MEDIUM / LOW]

Evidence:
- [List 3-5 specific indicators found]
- [e.g., "Contains 5 formal theorems with proofs"]
- [e.g., "Heavy mathematical notation throughout"]

Recommended workflow: [2-stage general / 5-stage theory]

Stages to be executed:
[List the specific stages]
```

Use AskUserQuestion tool to confirm: "Does this classification look correct? Should I proceed with the [X-stage workflow]?"

### Phase 1.5: Generate Global Context

**Purpose**: Create global document context for ultra-think processing (used by structure-editor subagent).

**Step 1: Create document summary**

Analyze the full document and generate a comprehensive summary:

Use Read tool to review `$original_path`, then create:
- Research question or main thesis (1-2 sentences)
- Methodology approach: theory/empirical/qualitative/mixed (1 sentence)
- Key findings or contributions (2-3 sentences)
- Overall document structure and flow (1-2 sentences)

Output format (2-3 paragraphs total):
```
This paper [examines/proposes/analyzes] [research question]. Using [methodology],
the author(s) [approach description]. The main findings are [key results].
The paper is structured as follows: [section flow].
```

Store as variable: `$document_summary`

**Step 2: Extract structure outline**

Create a hierarchical outline with line numbers for all sections:

For .md files:
```bash
# Extract all headers with line numbers
grep -n "^#" "$original_path" > /tmp/outline_raw.txt

# Process to create hierarchical structure
# Expected format:
# 1. Introduction (lines 1-150)
#    1.1 Motivation (lines 1-45)
#    1.2 Research Question (lines 46-89)
#    1.3 Contribution (lines 90-150)
# 2. Literature Review (lines 151-340)
#    2.1 Theoretical Framework (lines 151-220)
#    ...
```

For .tex files:
```bash
# Extract sections, subsections, subsubsections with line numbers
grep -n "\\\\section\|\\\\subsection\|\\\\subsubsection" "$original_path" > /tmp/outline_raw.txt

# Process to create hierarchical structure with line ranges
```

Store as variable: `$structure_outline`

**Step 3: Identify unit boundaries**

Extract precise line ranges for each structural unit:

For .md files:
```bash
# Get all level-2 headers (## sections) with line numbers
section_lines=($(grep -n "^## " "$original_path" | cut -d: -f1))

# Calculate line ranges for each section
# section[i] spans from section_lines[i] to section_lines[i+1]-1
# Last section spans to end of file
```

For .tex files:
```bash
# Get all \section commands with line numbers
section_lines=($(grep -n "\\\\section{" "$original_path" | cut -d: -f1))

# Calculate line ranges similarly
```

Store as array: `$section_boundaries` (format: [{start_line, end_line, title}])

**Step 4: Store for later use**

These variables will be passed to the structure-editor subagent in Phase 3:
- `$document_summary` - 2-3 paragraph overview
- `$structure_outline` - Hierarchical outline with line numbers
- `$section_boundaries` - Array of section line ranges

**Note**: This global context is used ONLY by structure-editor. Line-editor processes paragraph-by-paragraph with local context only.

### Phase 1.6: Document Preparation Analysis

**Step 1: Detect file format and word count**

Determine document characteristics:
```bash
# Get file extension (already stored in Phase 0, but can extract again)
file_ext="${original_path##*.}"

# Count words for .md and .tex files
word_count=$(wc -w < "$original_path" | tr -d ' ')

# Store for later use
echo "File: $original_path"
echo "Format: .$file_ext"
echo "Words: $word_count"
```

**Step 2: LaTeX complexity detection (for .tex files only)**

If file extension is `.tex`, analyze LaTeX complexity:

```bash
# Count math environments
math_inline=$(grep -o '\$[^$]*\$' "$original_path" | wc -l)
math_display=$(grep -cE '\\\\begin\{(equation|align|gather|multline)\}|\\\\\\[' "$original_path")
math_total=$((math_inline + math_display))

# Count custom commands
custom_cmds=$(grep -cE '\\\\newcommand|\\\\def[^a-zA-Z]|\\\\newenvironment' "$original_path")

# Count cross-references
citations=$(grep -cE '\\\\cite[tp]?\{' "$original_path")
refs=$(grep -cE '\\\\(eq)?ref\{|\\\\label\{' "$original_path")
crossrefs=$((citations + refs))

echo "LaTeX Analysis:"
echo "- Math environments: $math_total"
echo "- Custom commands: $custom_cmds"
echo "- Cross-references: $crossrefs"
```

Classify complexity based on reference/latex-support.md thresholds:
- **Simple**: < 20 math envs, < 3 custom commands, < 30 cross-refs
- **Moderate**: 20-50 math envs, 3-10 custom commands, 30-100 cross-refs
- **Complex**: > 50 math envs, > 10 custom commands, > 100 cross-refs

**Step 3: Present LaTeX warning (if Moderate or Complex)**

If complexity is Moderate or Complex, use AskUserQuestion to warn user:

For Moderate:
```
⚠️ LATEX COMPLEXITY DETECTED

Your .tex file has:
- [N] math environments
- [M] custom commands
- [K] cross-references

Complexity: Moderate

Editing recommendations:
- Copy-editing will preserve math mode content
- Test compilation after each stage: pdflatex [file].tex
- Review changes in math-heavy sections carefully
- Consider backing up before proceeding

Should I proceed with copy-editing?
```

For Complex:
```
⚠️ LATEX HIGH COMPLEXITY DETECTED

Your .tex file has:
- [N] math environments
- [M] custom commands
- [K] cross-references

Complexity: Complex

Strong recommendations:
- Create backup: cp [file].tex [file]-backup.tex
- Compile after EVERY stage to catch issues early
- Review ALL math sections carefully
- Consider processing in smaller sections

Should I proceed with copy-editing?
```

**Step 4: Determine chunking strategy**

Based on word count, determine if chunking is needed:

```
if word_count < 6000:
    enable_chunking = False
    reason = "Document is short enough for single-pass processing"
elif word_count <= 15000:
    enable_chunking = False
    reason = "Medium document, manageable without chunking"
else:
    enable_chunking = True
    reason = "Long document (>15K words), will enable chunking for line-edit stages"
```

Note this decision for use in Phase 3.

If chunking will be enabled, inform user:
```
📋 PROCESSING STRATEGY

Document length: [N] words
Chunking: Enabled for Line Edit + Proofread stage

Chunking approach:
- Structure stage: Full document (needs complete view)
- Line Edit + Proofread stage: Process paragraph-by-paragraph with context

This ensures complete coverage of your document.
```

### Phase 2: Set Up Progress Tracking

Use TodoWrite to create the stage tracking list.

**For General Academic (no chunking - documents < 15K words)**:
```
Stage 1: Structural Edit - pending
Stage 1: Review - pending
Stage 2: Line Edit + Proofread - pending
Stage 2: Review - pending
```

**For General Academic (with chunking - documents > 15K words)**:

Initial setup:
```
Stage 1: Structural Edit - pending
Stage 1: Review - pending
Stage 2: Line Edit + Proofread (chunked) - pending
Stage 2: Review - pending
```

During Stage 2 execution, optionally expand to show paragraph progress:
```
Stage 1: Structural Edit - completed
Stage 1: Review - completed
Stage 2: Line Edit + Proofread ([N] paragraphs) - in_progress
  - Processing paragraph [X]/[N] in [Section Name] - in_progress
Stage 2: Review - pending
```

**For Theory Paper (5 stages, no chunking)**:
```
Stage 1: General Structure - pending
Stage 1: Review - pending
Stage 2: Theory Structural Refinement - pending
Stage 2: Review - pending
Stage 3: Technical Elements - pending
Stage 3: Review - pending
Stage 4: General Line Edit + Proofread - pending
Stage 4: Review - pending
Stage 5: Theory-Specific Line Edit - pending
Stage 5: Review - pending
```

**For Theory Paper (5 stages, with chunking for Stages 4-5)**:
```
Stage 1: General Structure - pending
Stage 1: Review - pending
Stage 2: Theory Structural Refinement - pending
Stage 2: Review - pending
Stage 3: Technical Elements - pending (NO CHUNKING - needs full doc)
Stage 3: Review - pending
Stage 4: General Line Edit + Proofread (chunked) - pending
Stage 4: Review - pending
Stage 5: Theory-Specific Line Edit (chunked) - pending
Stage 5: Review - pending
```

Note: Line Edit and Proofread are merged into a single stage with paragraph-by-paragraph processing. Paragraph tracking is optional and can be shown for user visibility.

### Phase 3: Execute Editing Workflow

Based on the document type, execute the appropriate workflow:

#### General Academic Workflow (2 stages):

**Stage 1: Structural Edit**

Update TodoWrite: Mark Stage 1 as "in_progress"

Initialize: iteration_count = 0, max_iterations = 2

**Step 1: Launch structure-editor subagent with ultra-think**

Use Task tool to delegate to structure-editor:
- subagent_type: "structure-editor"
- description: "Ultra-think structural editing for Stage 1"
- prompt: """
Edit [file_path] for structural improvements.

Inputs:
- file_path: [full path to document]
- paper_type: "general"
- stage_file: ${CLAUDE_PLUGIN_ROOT}/skills/copy-edit-master/stages/general/01-structure.md
- ultra_think: true
- global_context:
  - document_summary: [paste $document_summary from Phase 1.5]
  - structure_outline: [paste $structure_outline from Phase 1.5]
- section_boundaries: [paste $section_boundaries array from Phase 1.5]

Follow your ultra-think processing workflow. Read stage_file for structural editing rules.
"""

Store the editor's returned JSON for Step 2.

**Step 2: Launch quality-reviewer subagent**

Update TodoWrite: Mark "Stage 1: Review" as "in_progress"

Use Task tool to delegate to quality-reviewer:
- subagent_type: "quality-reviewer"
- description: "Review structural editing"
- prompt: """
Review the structural editing work for Stage 1.

Inputs:
- stage: "structure"
- paper_type: "general"
- file_path: [full path to document]
- editor_summary: [paste editor's summary from Step 1]
- stage_file: ${CLAUDE_PLUGIN_ROOT}/skills/copy-edit-master/stages/general/01-structure.md

Evaluate whether all structural objectives were met and no errors were introduced.

Return your validation decision in the format specified in your system prompt.
"""

**Step 3: Handle review feedback**

Parse the reviewer's output:

If reviewer says "APPROVED":
- Update TodoWrite: Mark "Stage 1: Review" as "completed"
- Proceed to Step 4 (Git workflow)

If reviewer says "NEEDS REVISION" AND iteration_count < 2:
- iteration_count += 1
- Update TodoWrite: Update "Stage 1: Review" to "Stage 1: Review (Iteration [iteration_count]/2)" with status "pending"
- Update TodoWrite: Mark "Stage 1: Structural Edit" as "in_progress" (revision)
- Re-run Step 1 with modified prompt:
  ```
  Previous attempt had issues. Please address this specific feedback:

  [paste reviewer's "Specific feedback for re-editing" section]

  [rest of original prompt from Step 1]
  ```
- Re-run Step 2
- Return to Step 3 to re-evaluate

If reviewer says "NEEDS REVISION" AND iteration_count >= 2:
- Use AskUserQuestion with 3 options:
  ```
  After 2 iterations, some issues remain:

  [list critical issues from reviewer]

  How would you like to proceed?

  (A) Accept current version - good enough for now, proceed to next stage
  (B) I'll manually review and fix - let me examine the issues myself
  (C) Try one more automated iteration - override the limit
  ```
- If user chooses (A):
  - Update TodoWrite: Mark "Stage 1: Review" as "completed" (note: user accepted)
  - Proceed to Step 4
- If user chooses (B):
  - Update TodoWrite: Mark "Stage 1: Review" as "completed" (note: manual review)
  - Inform user where to review, skip to next stage when ready
- If user chooses (C):
  - iteration_count = 0
  - Update TodoWrite: Reset "Stage 1: Review" to "pending"
  - Return to Step 1

**Step 4: Git workflow**

[Execute Phase 4 Git Workflow - see below]

After git commit complete, proceed to Step 5.

**Step 5: Generate Stage Report**

Create stage-1-structure-report.md in the workspace directory:

```bash
cat > "$workspace_dir/stage-1-structure-report.md" << 'EOF'
# Stage 1: Structural Edit Report

**Manuscript**: $manuscript_name
**Date**: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
**Paper Type**: [General Academic | Theory]
**Editor**: structure-editor subagent
**Reviewer**: quality-reviewer subagent

## Summary
[2-3 paragraph summary of structural changes from editor_summary]

## Changes Implemented
[Extract from editor_summary - list major structural changes]

### Section-Level Changes
[List sections reordered, added, or removed]

### Paragraph-Level Changes
- Paragraphs restructured: [N]
- Transitions added: [N]

## Statistics
[Extract from editor_summary]
- Sections modified: [N]
- Paragraphs restructured: [N]
- Transitions added: [N]

## Iteration History
[Document iteration count and outcomes]
- Iteration 0: [APPROVED/NEEDS REVISION]
  - Editor changes: [brief summary]
  - Reviewer feedback: [brief summary]
[If iteration 1 occurred:]
- Iteration 1: [APPROVED/NEEDS REVISION]
  - Editor changes: [brief summary]
  - Reviewer feedback: [brief summary]

## Git Commit
Commit: [insert commit hash from last git commit]
Message: [insert commit message]
EOF
```

Note: Replace bracketed placeholders with actual data from editor_summary and reviewer outputs collected in Steps 1-3.

After report generated:
- Update TodoWrite: Mark Stage 1 as "completed"

**Stage 2: Line Edit + Proofread**

Update TodoWrite: Mark Stage 2 as "in_progress"

**Note**: Stage 2 combines line editing and proofreading. The structure-editor has finalized all paragraph positions, so this stage focuses solely on sentence-level improvements within each paragraph. To ensure complete coverage without subjective skipping, we process by SECTION (not individual paragraphs).

**Step 1: Identify major sections and paragraph boundaries**

For .md files:
```bash
# Identify section headers and calculate boundaries
section_lines=($(grep -n "^## " "$original_path" | cut -d: -f1))
total_lines=$(wc -l < "$original_path")

# Create sections array with boundaries
sections=()
for i in "${!section_lines[@]}"; do
  start_line="${section_lines[$i]}"
  end_line=$([[ $i -lt $((${#section_lines[@]} - 1)) ]] && echo $((${section_lines[$((i+1))]} - 1)) || echo "$total_lines")
  section_title=$(sed -n "${start_line}p" "$original_path" | sed 's/^## //')
  sections+=("{number: $i, title: \"$section_title\", start_line: $start_line, end_line: $end_line}")
done
```

For .tex files: Use `grep -n "\\\\section{"` to identify sections; same boundary logic.

Store:
- `sections` array with section boundaries
- `total_sections` = length(sections)

Note: Line-editor will detect and count paragraphs within each section.

**Step 2: Inform user and setup TodoWrite**

Output to user:
```
📝 SECTION-BY-SECTION PROCESSING

Total sections identified: [N]
Processing mode: Each section processed completely by line-editor

Line-editor will:
- Detect all paragraphs within each section
- Edit ALL paragraphs sequentially
- Report paragraph counts and statistics
```

Create section-level TodoWrite items:
```
For each section s in sections:
    Add todo: "Edit Section [s.number]: [s.title]" - pending
```

**Step 3: Process each section**

Initialize: iteration_count = 0, max_iterations = 2

For each section s in sections:

3.1. Update TodoWrite: Mark section s as "in_progress"

3.2. Launch line-editor for entire section:
```
Use Task tool:
- subagent_type: "line-editor"
- description: "Edit Section [s.number]: [s.title]"
- model: "sonnet"
- prompt: """
Edit the following section of [file_path].

Inputs:
- file_path: [full path]
- paper_type: general
- stage_file: ${CLAUDE_PLUGIN_ROOT}/skills/copy-edit-master/stages/general/02-line-edit.md
- section:
  - number: [s.number]
  - title: [s.title]
  - start_line: [s.start_line]
  - end_line: [s.end_line]

Read the stage_file for editing rules and output format requirements.
"""
```

3.3. Store results from editor output:
```
section_results[s.number] = {
  paragraphs_processed: extract_from_output("Paragraphs processed: (\\d+)"),
  stats: [extracted statistics],
  examples: [extracted before/after examples]
}
```

3.4. Update TodoWrite: Mark section s as "completed"

**Step 4: Aggregate results across all sections**

After all sections processed:

4.1. Calculate totals from section_results (word counts, improvements by category, total paragraphs).

4.2. Select best examples:
- Collect all before/after examples from all sections
- Choose 10-12 best examples representing different rules
- Format for final report

**Step 5: Quality review (single review of entire stage)**

Update TodoWrite: Mark "Stage 2: Review" as "in_progress"

Initialize: iteration_count = 0, max_iterations = 2

5.1. Launch quality-reviewer:
```
Use Task tool:
- subagent_type: "quality-reviewer"
- description: "Review Stage 2 line editing + proofreading"
- prompt: """
Review the line editing + proofreading work for Stage 2.

Inputs:
- stage: "line-edit"
- paper_type: "general"
- file_path: [full path]
- editor_summary: [aggregated total_stats + examples]
- stage_file: ${CLAUDE_PLUGIN_ROOT}/skills/copy-edit-master/stages/general/02-line-edit.md

Processing notes:
- [total_sections] sections processed
- [total_stats.total_paragraphs_processed] total paragraphs edited
- Section-by-section approach with mandatory completeness
- Combined line-edit + proofreading in single pass per section

Coverage verification:
- Expected paragraphs: [expected_total_paragraphs]
- Processed paragraphs: [total_stats.total_paragraphs_processed]
- Status: [Complete/Incomplete]

Return your validation decision.
"""
```

5.2. Handle review feedback:
- If APPROVED:
  - Update TodoWrite: Mark "Stage 2: Review" as "completed"
  - Proceed to Step 6
- If NEEDS REVISION and iteration_count < 2:
  - iteration_count += 1
  - Update TodoWrite: Update "Stage 2: Review" to "Stage 2: Review (Iteration [iteration_count]/2)" with status "pending"
  - Identify specific sections with issues from reviewer feedback
  - Re-process those sections only (Steps 3.2-3.4)
  - Re-aggregate (Step 4)
  - Return to Step 5.1 (mark review as "in_progress" again)
- If iteration_count >= 2:
  - Escalate to user (same pattern as Stage 1)
  - Update TodoWrite: Mark "Stage 2: Review" as "completed" based on user choice

**Step 6: Git workflow**

[Execute Phase 4 Git Workflow]

After git commit, proceed to Step 7.

**Step 7: Generate Stage Report**

Create simplified stage-2-line-edit-report.md:

```bash
cat > "$workspace_dir/stage-2-line-edit-report.md" << 'EOF'
# Stage 2: Line Edit + Proofread Report

**Manuscript**: $manuscript_name
**Date**: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
**Processing**: Section-by-section ([N] sections, [M] total paragraphs)

## Summary

[2-3 paragraph summary of improvements from total_stats]

## Word Count Evolution
- Original: [X] words
- Edited: [Y] words
- **Reduction**: [X-Y] words (-[%]%)

## Improvements

### Strunk & White Rules
- Wordiness eliminated: [N]
- Passive → Active: [M]
- Vague → Specific: [K]
- Other rule applications: [P]

### Proofreading
- Grammar corrections: [G]
- Punctuation fixes: [Pu]
- Typos corrected: [T]

## Example Improvements

[10-12 best before/after examples with rule labels]

## Git Commit
Commit: [hash]
Message: [message]
EOF
```

After report generated:
- Update TodoWrite: Mark Stage 2 as "completed"

#### Theory Paper Workflow (5 stages):

**Note**: Theory papers now use a 5-stage workflow that builds on the enriched general stages:
- Stages 1 & 4: Use general stages (structure, line edit) for McCloskey principles
- Stages 2, 3, 5: Apply theory-specific refinements (structural, technical, line edit)

This ensures theory papers benefit from the comprehensive general writing principles while also receiving specialized theory paper treatment.

**Stage 1: General Structure**

Update TodoWrite: Mark Stage 1 as "in_progress"

Initialize: iteration_count = 0, max_iterations = 2

**Step 1: Launch structure-editor subagent with ultra-think**

Use Task tool:
- subagent_type: "structure-editor"
- description: "Ultra-think general structural editing for theory paper"
- prompt: """
Edit [file_path] for structural improvements.

Inputs:
- file_path: [full path]
- paper_type: "general"
- stage_file: ${CLAUDE_PLUGIN_ROOT}/skills/copy-edit-master/stages/general/01-structure.md
- ultra_think: true
- global_context:
  - document_summary: [paste $document_summary from Phase 1.5]
  - structure_outline: [paste $structure_outline from Phase 1.5]
- section_boundaries: [paste $section_boundaries array from Phase 1.5]

Follow your ultra-think processing workflow. Read stage_file for structural editing rules.
"""

**Step 2: Launch quality-reviewer subagent**

Update TodoWrite: Mark "Stage 1: Review" as "in_progress"

[Same pattern as General Academic Stage 1]

**Step 3: Handle review feedback**

[Same iteration pattern as General Academic Stage 1, updating "Stage 1: Review" todo accordingly]

**Step 4: Git workflow**

[Execute Phase 4 Git Workflow]

**Step 5: Generate Stage Report**

Create stage-1-structure-report.md in `$workspace_dir`.

After report generated:
- Update TodoWrite: Mark Stage 1 as "completed"
- (Note: "Stage 1: Review" should already be "completed" from Step 3)

**Stage 2: Theory Structural Refinement**

Update TodoWrite: Mark Stage 2 as "in_progress"

Initialize: iteration_count = 0, max_iterations = 2

**Step 1: Launch structure-editor subagent for theory refinement**

Use Task tool:
- subagent_type: "structure-editor"
- description: "Theory structural refinement"
- prompt: """
Refine [file_path] with theory-specific structural checks.

Inputs:
- file_path: [full path]
- paper_type: "theory"
- stage_file: ${CLAUDE_PLUGIN_ROOT}/skills/copy-edit-master/stages/theory/01-structure-refinement.md
- ultra_think: true
- global_context:
  - document_summary: [paste $document_summary from Phase 1.5]
  - structure_outline: [paste $structure_outline from Phase 1.5]
- section_boundaries: [paste $section_boundaries array from Phase 1.5]
- note: Stage 1 (General Structure) is complete. Apply ONLY theory-specific refinements.

Read stage_file for theory-specific structural requirements.
"""

**Step 2: Launch quality-reviewer subagent**

Update TodoWrite: Mark "Stage 2: Review" as "in_progress"

Use Task tool:
- subagent_type: "quality-reviewer"
- description: "Review theory structure refinement"
- prompt: """
Review the theory structural refinement work.

Inputs:
- stage: "structure"
- paper_type: "theory"
- file_path: [full path]
- editor_summary: [from Step 1]
- stage_file: ${CLAUDE_PLUGIN_ROOT}/skills/copy-edit-master/stages/theory/01-structure-refinement.md

Read stage_file to validate that theory-specific structural elements are properly addressed.
"""

**Step 3: Handle review feedback**

[Same iteration pattern as General Academic Stage 1, updating "Stage 2: Review" todo accordingly]

**Step 4: Git workflow**

[Execute Phase 4 Git Workflow]

**Step 5: Generate Stage Report**

Create stage-2-theory-refinement-report.md:

```bash
cat > "$workspace_dir/stage-2-theory-refinement-report.md" << 'EOF'
# Stage 2: Theory Structural Refinement Report

**Manuscript**: $manuscript_name
**Date**: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
**Editor**: structure-editor subagent
**Reviewer**: quality-reviewer subagent

## Summary
[2-3 paragraph summary of theory-specific structural improvements]

## Introduction (4 Questions)
- What is the topic: [status]
- What is the specific question: [status]
- What is the answer: [status]
- How do you get there: [status]

## Simple-to-General Ordering
[Assessment and changes]

## Theorem Presentation
- Theorems with informal statements added: [N]
- Theorems with interpretation added: [N]
- Theorems reordered: [Y/N]

## Model Section
[Assessment of ordering and intuition]

## Conclusion
[Assessment of synthesis, limitations, open questions]

## Git Commit
Commit: [hash]
Message: [message]
EOF
```

After report generated:
- Update TodoWrite: Mark Stage 2 as "completed"

**Stage 3: Technical Elements**

Update TodoWrite: Mark Stage 3 as "in_progress"

Initialize: iteration_count = 0, max_iterations = 2

**IMPORTANT: NO CHUNKING for this stage** (needs full document view for notation consistency)

**Step 1: Launch theory-technical-editor subagent**

Use Task tool:
- subagent_type: "theory-technical-editor"
- description: "Theory technical review"
- prompt: """
Edit the document at [file_path] for technical elements.

Inputs:
- file_path: [full path]
- stage_file: ${CLAUDE_PLUGIN_ROOT}/skills/copy-edit-master/stages/theory/02-technical.md

Review and improve:
- Part A: Notation (conventional, mnemonic, minimal, pronounceable, hierarchical, uncluttered)
- Part B: Definitions (signaling, 4 types of examples, logical order)
- Part C: Proofs (structure, clarity, completeness, quantifier handling)
- Part D: Figures (complete labeling, purposeful drawing, text integration)

This is the most complex stage (804 lines of instructions). Be thorough.

Return comprehensive summary.
"""

**Step 2: Launch quality-reviewer subagent**

Update TodoWrite: Mark "Stage 3: Review" as "in_progress"

Use Task tool:
- subagent_type: "quality-reviewer"
- description: "Review technical elements"
- prompt: """
Review the technical editing work.

Inputs:
- stage: "technical"
- paper_type: "theory"
- file_path: [full path]
- editor_summary: [from Step 1]
- stage_file: ${CLAUDE_PLUGIN_ROOT}/skills/copy-edit-master/stages/theory/02-technical.md

Validate notation consistency, definition completeness, proof clarity.

Return validation decision.
"""

**Step 3: Handle review feedback**

[Same iteration pattern as General Academic Stage 1, updating "Stage 3: Review" todo accordingly]

**Step 4: Git workflow**

[Execute Phase 4 Git Workflow]

**Step 5: Generate Stage Report**

Create `$workspace_dir/stage-3-technical-report.md` with notation, definitions, proofs, figures improvements.

After report generated:
- Update TodoWrite: Mark Stage 3 as "completed"
- (Note: "Stage 3: Review" should already be "completed" from Step 3)

**Stage 4: General Line Edit + Proofread**

Update TodoWrite: Mark Stage 4 as "in_progress"

**Note**: This stage uses the enriched general line-edit instructions to apply Strunk & White and McCloskey principles. Paragraph positions were finalized in Stages 1-2.

**Step 1: Identify major sections and paragraph boundaries**

[Use same section identification logic as General Academic Stage 2, Step 1]

**Step 2: Inform user and setup TodoWrite**

Output to user:
```
📝 SECTION-BY-SECTION PROCESSING (STAGE 4 - GENERAL LINE EDIT)

Total sections identified: [N]
Total paragraphs across all sections: [M]
Processing mode: Each section processed completely (NO skipping)

This stage applies:
- All 7 Strunk & White rules
- McCloskey's economical writing principles
- Standard grammar, punctuation, spelling proofreading

Theory-specific line editing will follow in Stage 5.
```

Create section-level TodoWrite items.

**Step 3: Process each section**

For each section s in sections:

3.1. Update TodoWrite: Mark section s as "in_progress"

3.2. Launch line-editor for entire section:
```
Use Task tool:
- subagent_type: "line-editor"
- description: "Edit Section [s.section_number]: [s.title]"
- model: "sonnet"
- prompt: """
Edit the following section of [file_path].

Inputs:
- file_path: [full path]
- paper_type: theory
- stage_file: ${CLAUDE_PLUGIN_ROOT}/skills/copy-edit-master/stages/general/02-line-edit.md
- section:
  - number: [s.section_number]
  - title: [s.title]
  - start_line: [s.start_line]
  - end_line: [s.end_line]

Read the stage_file for editing rules and output format requirements.
"""
```

3.3. Parse output and verify completeness.

3.4. Update TodoWrite: Mark section s as "completed"

**Step 4: Aggregate results across all sections**

[Use same aggregation logic as General Academic Stage 2]

**Step 5: Quality review**

Update TodoWrite: Mark "Stage 4: Review" as "in_progress"

[Standard quality review - same pattern as General Academic Stage 2, Step 5]

Handle review feedback: [Same pattern as Stage 2, updating "Stage 4: Review" todo accordingly]

**Step 6: Git workflow**

[Execute Phase 4 Git Workflow]

**Step 7: Generate Stage Report**

Create `$workspace_dir/stage-4-line-edit-report.md`.

After report generated:
- Update TodoWrite: Mark Stage 4 as "completed"
- (Note: "Stage 4: Review" should already be "completed" from Step 5)

**Stage 5: Theory-Specific Line Edit**

Update TodoWrite: Mark Stage 5 as "in_progress"

**Note**: This final stage applies theory-specific sentence-level improvements. General Strunk & White rules were applied in Stage 4. This stage focuses on triviality test, scannability, and theory proofreading.

**Step 1: Identify sections**

[Use section boundaries from Stage 4]

**Step 2: Inform user**

Output to user:
```
📝 SECTION-BY-SECTION PROCESSING (STAGE 5 - THEORY LINE EDIT)

Total sections identified: [N]
Total paragraphs across all sections: [M]
Processing mode: Each section processed completely (NO skipping)

Theory-specific features:
- Triviality test (make reasoning seem simple)
- Scannability (write so you won't have to be read)
- Formalism-intuition balance
- Theory-specific proofreading (notation consistency, math mode, theorem refs)

This is the final editing stage.
```

**Step 3: Process each section**

For each section s in sections:

3.1. Update TodoWrite: Mark section s as "in_progress"

3.2. Launch line-editor for theory-specific editing:
```
Use Task tool:
- subagent_type: "line-editor"
- description: "Theory Edit Section [s.section_number]: [s.title]"
- model: "sonnet"
- prompt: """
Apply theory-specific line editing to section [s.section_number] of [file_path].

Inputs:
- file_path: [full path]
- paper_type: theory
- stage_file: ${CLAUDE_PLUGIN_ROOT}/skills/copy-edit-master/stages/theory/02-line-edit-additions.md
- section:
  - number: [s.section_number]
  - title: [s.title]
  - start_line: [s.start_line]
  - end_line: [s.end_line]
- note: General Strunk & White rules were applied in Stage 4. Focus on theory-specific improvements only.

Read the stage_file for theory-specific editing rules and output format.
"""
```

3.3. Parse output and verify completeness.

3.4. Update TodoWrite: Mark section s as "completed"

**Step 4: Aggregate results**

Aggregate theory-specific improvements across all sections.

**Step 5: Quality review**

Update TodoWrite: Mark "Stage 5: Review" as "in_progress"

Launch quality-reviewer with theory-specific focus.

Handle review feedback: [Same pattern as previous stages, updating "Stage 5: Review" todo accordingly]

**Step 6: Git workflow**

[Execute Phase 4 Git Workflow]

**Step 7: Generate Stage Report**

Create stage-5-theory-line-edit-report.md:

```bash
cat > "$workspace_dir/stage-5-theory-line-edit-report.md" << 'EOF'
# Stage 5: Theory-Specific Line Edit Report

**Manuscript**: $manuscript_name
**Date**: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
**Processing**: Section-by-section ([N] sections, [M] total paragraphs)

## Summary

[2-3 paragraph summary of theory-specific improvements]

## Theory Clarity Improvements

### Triviality Test
- Complex → Simple explanations: [N]

### Scannability
- Theorem presentations enhanced: [N]
- Cross-references added: [N]

### Formalism-Intuition Balance
- Intuitive explanations added: [N]

### Theory Word Choice
- Corrections made: [N]

### Proof Readability
- Signposting added: [N]
- Equation explanations: [N]

## Theory-Specific Proofreading

- Notation consistency fixes: [N]
- Math mode corrections: [N]
- Reference completeness: [N]

## Example Improvements

[8-10 best before/after examples showing theory-specific changes]

## Git Commit
Commit: [hash]
Message: [message]

## Final Status
✅ All 5 stages complete - manuscript ready for submission
EOF
```

After report generated:
- Update TodoWrite: Mark Stage 5 as "completed"
- (Note: "Stage 5: Review" should already be "completed" from Step 5)

### Phase 4: Git Workflow (After Each Stage)

After completing each stage:

**Step 1: Check if git repository exists**
```bash
git status
```

If no git repo:
- Warn user: "This directory is not a git repository. Would you like me to initialize one?"
- If user declines, skip git steps for all stages
- If user approves, run `git init`

**Step 2: Show changes**
```bash
git diff [filename]
```

**Step 3: Present summary to user**
```
✅ STAGE [N] COMPLETE: [Stage Name]

Changes made:
- [Summary of major changes]
- [Key improvements]
- [Statistics: X words removed, Y sentences restructured, etc.]

Files modified:
- [filename]
```

**Step 4: Ask for commit confirmation**

Use AskUserQuestion tool to ask:
"Would you like to commit these changes? Proposed commit message:
```
Stage [N]: [Stage name] complete

- [Brief list of changes]
```
"

**Step 5: Execute commit if approved**
```bash
git add [filename] && git commit -m "[commit message]"
```

**Step 6: Proceed to next stage**

### Phase 5: Final Report

After all stages complete, provide comprehensive summary:

```
🎉 COPY-EDITING COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Document: [filename]
Workflow: [X-stage process]

Stages completed:
✅ Stage 1: [Name]
✅ Stage 2: [Name]
[For theory papers only:]
✅ Stage 3: [Name]
✅ Stage 4: [Name]
✅ Stage 5: [Name]

Total improvements:
- Words reduced: [N] ([X]% more concise)
- Passive voice → Active: [N] instances
- Vague terms → Specific: [N] replacements
- Structural improvements: [N]
[Theory-specific: Notation standardized: [N] symbols]

Git commits: [N] commits created

Next steps:
- Review the changes with: git log --oneline
- Compare versions with: git diff HEAD~[N]
- If needed, you can revert individual stages
```

## Important Guidelines

### When to Ask for User Confirmation

**ALWAYS ask before**:
- Changing the narrative structure or argument flow
- Reordering major sections
- Removing or combining substantial content
- Changing the paper's focus or contribution claims

**Present options when**:
- Multiple valid structural approaches exist
- Unclear what the author's intent was
- Major revision would significantly alter the paper

**Format for presenting options (use AskUserQuestion tool)**:
```
I've identified [issue]. Here are possible revision approaches:

Option A: [Description]
Pros: [List]
Cons: [List]

Option B: [Description]
Pros: [List]
Cons: [List]

Option C: [Description]
Pros: [List]
Cons: [List]

Recommendation: I recommend Option [X] because [reasoning].
```

Then use AskUserQuestion to let user choose.

### Multi-Format Support

**For Markdown (.md)**:
- Use Read and Edit tools directly
- Preserve formatting and structure

**For LaTeX (.tex)**:
- Use Read and Edit tools
- Be careful with LaTeX commands and math environments
- Don't break citations, references, or math mode

**For Word (.docx)**:
- Use Skill tool with document-skills:docx
- Preserve formatting, track changes if requested
- Handle comments and markup

## Edge Cases

**No git repository**:
- Warn user that git commits won't be possible
- Offer to initialize repository
- Continue with editing, skip git steps if user declines

**File in use / locked**:
- Ask user to close the file
- Retry or skip to next stage

**Very long documents**:
- Process in sections if needed
- Track section progress separately with TodoWrite

**Unclear document type**:
- Default to general academic workflow
- Inform user of uncertainty
- Allow manual override with AskUserQuestion

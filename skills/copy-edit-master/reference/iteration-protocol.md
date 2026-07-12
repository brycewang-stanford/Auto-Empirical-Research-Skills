# Quality Iteration Protocol

## Overview

Every editing stage uses: Editor → Reviewer → (iteration if needed) → Approved

Maximum iterations: 2 per stage (to control time and diminishing returns)

## Flow Diagram

```
┌─────────────┐
│   Editor    │ (Iteration 0)
│  Subagent   │
└──────┬──────┘
       │
       ├─ Edited document
       ├─ Summary of changes
       │
       ▼
┌─────────────┐
│  Reviewer   │
│  Subagent   │
└──────┬──────┘
       │
       ├─ APPROVED ─────────────────────► Proceed to Git commit
       │
       ├─ NEEDS REVISION + iteration < 2
       │   │
       │   ▼
       │ ┌─────────────┐
       │ │   Editor    │ (Iteration 1)
       │ │  Re-edit    │
       │ └──────┬──────┘
       │        │
       │        ▼
       │ ┌─────────────┐
       │ │  Reviewer   │
       │ └──────┬──────┘
       │        │
       │        ├─ APPROVED ──────────────► Proceed
       │        │
       │        ├─ NEEDS REVISION + iteration < 2
       │        │   │
       │        │   ▼ (Iteration 2, same pattern)
       │        │
       │        └─ NEEDS REVISION + iteration >= 2
       │            │
       │            ▼
       └────────► Ask user (3 options)
```

## Validation Criteria

### APPROVED Criteria
All must be true:
- ✅ All stage objectives met (per stage instruction file)
- ✅ No errors introduced (grammar, broken refs, etc.)
- ✅ ≤ 3 minor issues remaining (acceptable for publication)

Examples of minor issues (acceptable):
- Optional word choice improvements
- Style preferences
- Very subtle clarity enhancements

### NEEDS REVISION Criteria
Any one triggers revision:
- ❌ Stage objectives not met (e.g., passive voice still prevalent after line-edit)
- ❌ Errors introduced (grammar mistakes, broken citations, inconsistencies)
- ❌ > 3 critical issues found

Examples of critical issues:
- Line-edit stage: 15+ instances of wordiness still present
- Structure stage: Argument flow still unclear
- Proofread stage: Grammar errors introduced

## Iteration Count Strategy

### Iteration 0 (First attempt)
- Editor works with full stage instructions
- Reviewer applies strict criteria
- Expect some NEEDS REVISION results

### Iteration 1
- Editor receives specific feedback: "Fix these 5 specific issues at these locations"
- Focused revision, not full re-edit
- Reviewer applies same strict criteria

### Iteration 2
- Editor receives feedback again
- Last automated attempt
- Reviewer applies slightly relaxed criteria (recognize diminishing returns)

### Iteration 2+ (Max reached)
If still NEEDS REVISION:
- Escalate to user with AskUserQuestion
- Present 3 options:
  - (A) Accept current version (good enough for now)
  - (B) Let me manually review and fix (I'll examine issues)
  - (C) Try one more automated iteration (override limit)

## Special Cases

### Chunked Processing
For line-edit and proofread with chunks:
- Iteration max = 1 per chunk (not 2)
- Rationale: With 6 chunks, 2 iterations each = 12 extra passes (too slow)
- If chunk still has issues after 1 iteration: Note for user, proceed

### Theory Technical Stage
- Iteration max = 2 (complex stage, needs refinement)
- 804 lines of instructions, high chance of needing revision

### Structure Stage
- Iteration max = 2 (most complex reasoning)
- Often needs revision for argument flow improvements

---
name: Cleaning Up Research Sessions
description: Safely remove intermediate files from completed research sessions while preserving important data
when_to_use: After research session is complete and consolidated. When research folder has accumulated temporary files. Before archiving or sharing research session.
version: 1.0.0
---

<!--
  ╔══════════════════════════════════════════════════════════════╗
  ║  本文件为开源 Skill 原始文档，收录仅供学习与研究参考        ║
  ║  CoPaper.AI 收集整理 | https://copaper.ai                  ║
  ╚══════════════════════════════════════════════════════════════╝

  来源仓库: https://github.com/kthorn/research-superpower
  项目名称: research-superpower
  开源协议: MIT License
  收录日期: 2026-04-02

  声明: 本文件版权归原作者所有。此处收录旨在为社会科学实证研究者
  提供 AI Agent Skills 的集中参考。如有侵权，请联系删除。
-->

# Cleaning Up Research Sessions

## Overview

Remove intermediate files created during research workflow while preserving all important data.

**Core principle:** Conservative cleanup with user confirmation. Never delete anything important.

## When to Use

Use this skill when:
- Research session is complete and consolidated
- Preparing to archive or share research session folder
- Research folder has accumulated temporary/intermediate files
- User explicitly asks to clean up

**When NOT to use:**
- Research is still in progress
- User hasn't reviewed final outputs yet
- Unsure what files are safe to delete

## Files That Are ALWAYS KEPT

**NEVER delete these (protected list):**

**Core outputs:**
- `SUMMARY.md` - Enhanced findings with methodology
- `relevant-papers.json` - Filtered relevant papers
- `papers-reviewed.json` - Complete screening history
- `papers/` directory - All PDFs and supplementary files
- `citations/citation-graph.json` - Citation relationships

**Methodology documentation:**
- `screening-criteria.json` - Rubric definition (if exists)
- `test-set.json` - Rubric validation papers (if exists)
- `abstracts-cache.json` - Cached abstracts for re-screening (if exists)
- `rubric-changelog.md` - Rubric version history (if exists)

**Auxiliary documentation (if exists):**
- `README.md` - Project overview
- `TOP_PRIORITY_PAPERS.md` - Curated priority list
- `evaluated-papers.json` - Rich structured data

**Project configuration:**
- `.claude/` directory - Permissions and settings
- `*.py` helper scripts that were created - Keep for reproducibility

## Files That May Be Cleaned Up

**Candidates for removal (with confirmation):**

**Intermediate search results:**
- `initial-search-results.json` - Raw PubMed results before screening
  - Safe to delete: Data is in papers-reviewed.json
  - Reason to keep: Shows raw search results for reproducibility

**Temporary files:**
- `*.tmp` files
- `*.swp` files (vim swap files)
- `.DS_Store` (macOS)
- `__pycache__/` (Python cache)
- `*.pyc` (Python compiled)

**Log files:**
- `*.log` files
- `debug-*.txt` files

## Cleanup Workflow

### Step 1: Analyze Research Session

```bash
cd research-sessions/YYYY-MM-DD-description/

# List all files with sizes
find . -type f -exec ls -lh {} \; | awk '{print $5, $9}' | sort -rh
```

**Identify files by category:**
- Core outputs (MUST keep)
- Methodology files (SHOULD keep)
- Intermediate files (candidates for cleanup)
- Temporary files (safe to delete)

### Step 2: Present Cleanup Plan to User

**Show what will be deleted:**

```
🧹 Cleanup Analysis for: research-sessions/2025-10-11-btk-selectivity/

Files to KEEP (protected):
  ✅ SUMMARY.md (45 KB)
  ✅ relevant-papers.json (12 KB)
  ✅ papers-reviewed.json (28 KB)
  ✅ papers/ (14 PDFs, 32 MB)
  ✅ citations/citation-graph.json (5 KB)
  ✅ screening-criteria.json (2 KB)
  ✅ abstracts-cache.json (156 KB)

Files that CAN be removed (intermediate):
  🗑️  initial-search-results.json (8 KB) - Raw PubMed results
  🗑️  .DS_Store (6 KB) - macOS metadata

Total space to recover: 14 KB

Proceed with cleanup? (y/n/review)
```

**Options:**
- `y` - Delete intermediate files
- `n` - Cancel cleanup, keep everything
- `review` - Show contents of each file before deciding

### Step 3: Confirm Deletions

**Before deleting ANY file:**

1. **Verify it's not in protected list**
2. **Check file isn't referenced in SUMMARY.md**
3. **Confirm with user one more time**

**Example confirmation:**
```
About to delete:
- initial-search-results.json (8 KB)

This file contains raw PubMed search results. The data is preserved in
papers-reviewed.json, so this is safe to delete.

Confirm deletion? (y/n)
```

### Step 4: Perform Cleanup

**Delete confirmed files:**

```bash
# Move to trash instead of rm (safer)
# On macOS:
mv initial-search-results.json ~/.Trash/

# On Linux:
mv initial-search-results.json ~/.local/share/Trash/files/

# Or use rm if user confirms
rm initial-search-results.json
```

**Report results:**
```
✅ Cleanup complete!

Removed:
- initial-search-results.json (8 KB)
- .DS_Store (6 KB)

Space recovered: 14 KB

Protected files preserved:
- All 8 core files kept
- All 14 PDFs kept
- All methodology documentation kept
```

### Step 5: Verify Integrity

**After cleanup, verify critical files:**

```bash
# Check core files exist
test -f SUMMARY.md && echo "✓ SUMMARY.md"
test -f relevant-papers.json && echo "✓ relevant-papers.json"
test -f papers-reviewed.json && echo "✓ papers-reviewed.json"
test -d papers && echo "✓ papers/ directory"

# Verify JSON files are valid
jq empty relevant-papers.json && echo "✓ relevant-papers.json valid JSON"
jq empty papers-reviewed.json && echo "✓ papers-reviewed.json valid JSON"
```

**Report to user:**
```
✅ Integrity check passed
   - All core files present
   - All JSON files valid
   - All PDFs intact
```

## Special Cases

### Case 1: Large abstracts-cache.json

**If abstracts-cache.json is very large (>100 MB):**

```
⚠️  abstracts-cache.json is 256 MB

This file enables re-screening if you update the rubric. Options:
1. Keep (recommended if you might refine rubric)
2. Compress (gzip to ~50 MB, can decompress later)
3. Delete (only if research is final and won't be updated)

Choice? (1/2/3)
```

**If user chooses compress:**
```bash
gzip abstracts-cache.json
# Creates abstracts-cache.json.gz

echo "Compressed abstracts-cache.json to $(du -h abstracts-cache.json.gz | cut -f1)"
```

### Case 2: Helper Scripts

**If user created helper scripts during research:**

```
📝 Found helper scripts:
   - screen_papers.py (created for batch screening)
   - deep_dive_papers.py (created for data extraction)

These scripts document your methodology. Recommendations:
- Keep for reproducibility
- Add comments if not already documented
- Reference in SUMMARY.md under "Reproducibility" section

Keep scripts? (y/n)
```

### Case 3: Multiple Research Sessions

**If cleaning up multiple sessions:**

```bash
# Find all research sessions
find research-sessions/ -maxdepth 1 -type d

# For each session:
for session in research-sessions/*/; do
    echo "Analyzing: $session"
    # Run cleanup analysis
done
```

**Ask user:**
```
Found 5 completed research sessions.

Clean up all sessions? (y/n/select)
- y: Analyze and clean all sessions
- n: Cancel
- select: Choose which sessions to clean
```

## Safety Mechanisms

### Protected File List

**Maintain hardcoded list of patterns to NEVER delete:**

```python
PROTECTED_PATTERNS = [
    'SUMMARY.md',
    'relevant-papers.json',
    'papers-reviewed.json',
    'papers/*.pdf',
    'papers/*.zip',
    'citations/citation-graph.json',
    'screening-criteria.json',
    'test-set.json',
    'abstracts-cache.json',
    'rubric-changelog.md',
    'README.md',
    'TOP_PRIORITY_PAPERS.md',
    'evaluated-papers.json',
    '*.py',  # Helper scripts
    '.claude/*',  # Project settings
]
```

**Before deleting any file:**
```python
def is_protected(filepath):
    """Check if file matches any protected pattern"""
    for pattern in PROTECTED_PATTERNS:
        if fnmatch(filepath, pattern):
            return True
    return False

# Never delete protected files
if is_protected(file_to_delete):
    print(f"⚠️  ERROR: {file_to_delete} is protected and cannot be deleted")
    return
```

### Dry Run Mode

**Always show what will be deleted before doing it:**

```bash
# Dry run (show only, don't delete)
echo "DRY RUN - No files will be deleted"

for file in $candidate_files; do
    if is_safe_to_delete "$file"; then
        echo "Would delete: $file ($(du -h $file | cut -f1))"
    fi
done

echo ""
echo "Proceed with actual deletion? (y/n)"
```

## Integration with Other Skills

**After answering-research-questions workflow:**

1. Complete Phase 8 (consolidation)
2. User reviews SUMMARY.md and relevant-papers.json
3. **Optionally**: Run cleaning-up-research-sessions
4. Archive or share research folder

**Add to answering-research-questions Phase 8:**
```markdown
### Optional: Cleanup

After reviewing outputs, optionally clean up intermediate files:

"Research session is complete. Would you like me to clean up intermediate files?
I'll show you what will be deleted before removing anything."

If yes: Use `cleaning-up-research-sessions` skill
```

## Common Mistakes

**Deleting papers-reviewed.json:** This is the deduplication database - NEVER delete → Always protect with hardcoded list
**Deleting abstracts-cache.json:** Needed for re-screening → Ask user, default to keep
**Deleting helper scripts:** Important for reproducibility → Keep by default, ask if user wants to remove
**Not showing user what will be deleted:** User needs to see the plan → Always show dry run first
**Deleting without confirmation:** Too risky → Always ask for final confirmation
**Not verifying after cleanup:** Files could be corrupted → Run integrity check after deletion

## Quick Reference

| Action | Command |
|--------|---------|
| List all files with sizes | `find . -type f -exec ls -lh {} \; \| sort -rh` |
| Check if JSON valid | `jq empty file.json` |
| Move to trash (macOS) | `mv file ~/.Trash/` |
| Move to trash (Linux) | `mv file ~/.local/share/Trash/files/` |
| Compress large file | `gzip file` |
| Calculate folder size | `du -sh .` |

## Success Criteria

Cleanup successful when:
- All protected files still exist and are valid
- Only confirmed intermediate files deleted
- User knows what was deleted and why
- Space recovered is reported
- Integrity check passed
- Research session is still fully functional

## Example Session

```
User: "Can you clean up the research session folder?"

Agent: "I'll analyze the research session and show you what can be safely cleaned up."

[Analyzes folder]

Agent: "🧹 Cleanup Analysis for: research-sessions/2025-10-11-btk-selectivity/

Files to KEEP (protected):
  ✅ SUMMARY.md (45 KB) - Final findings
  ✅ relevant-papers.json (12 KB) - Filtered results
  ✅ papers-reviewed.json (28 KB) - Complete history
  ✅ papers/ (14 PDFs, 32 MB) - Downloaded papers
  ✅ citations/citation-graph.json (5 KB) - Citation network
  ✅ screening-criteria.json (2 KB) - Rubric definition
  ✅ abstracts-cache.json (156 KB) - Cached abstracts

Files that CAN be removed:
  🗑️  initial-search-results.json (8 KB) - Raw PubMed results
     → Data is preserved in papers-reviewed.json
  🗑️  .DS_Store (6 KB) - macOS metadata
     → Not needed

Total space to recover: 14 KB

Proceed with cleanup? (y/n/review)"

User: "y"

Agent: "Final confirmation - About to delete:
- initial-search-results.json (8 KB)
- .DS_Store (6 KB)

All protected files will be preserved. Confirm? (y/n)"

User: "y"

Agent: [Deletes files]

"✅ Cleanup complete!

Removed:
- initial-search-results.json (8 KB)
- .DS_Store (6 KB)

Space recovered: 14 KB

Running integrity check...
✅ All core files intact
✅ All JSON files valid
✅ All 14 PDFs present

Research session is ready for archiving or sharing."
```

## Next Steps

After cleanup:
- Research folder is clean and ready to archive
- Share folder with collaborators
- Move to long-term storage
- Continue with follow-up research if needed

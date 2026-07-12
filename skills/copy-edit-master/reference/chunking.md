# Document Chunking Reference

## When to Enable Chunking

- Document length > 15,000 words
- Only for Stage 2 (Line Edit) and Stage 3 (Proofread)
- NOT for Stage 1 (Structure) - needs full document view
- NOT for Theory Stage 2 (Technical) - needs full document for notation consistency

## Semantic Chunking Algorithm

### Step 1: Identify Section Boundaries

**For Markdown (.md):**
```bash
grep -n "^## " document.md
# Returns line numbers of all level-2 headers
```

**For LaTeX (.tex):**
```bash
grep -n "\\\\section{" document.tex
grep -n "\\\\subsection{" document.tex
# Use \section as primary boundaries
# Use \subsection only if \sections are too large (> 8,000 words)
```

### Step 2: Create Chunks

Target: 3,000-5,000 words per chunk

Algorithm:
```
chunks = []
current_chunk = {sections: [], start_line: 0, end_line: 0, word_count: 0}

for each section in sections:
    section_word_count = count_words(section)

    if current_chunk.word_count + section_word_count > 5000 AND current_chunk.word_count >= 3000:
        # Current chunk is full, start new chunk
        chunks.append(current_chunk)
        current_chunk = {sections: [section], start_line: section.start, end_line: section.end, word_count: section_word_count}
    else:
        # Add section to current chunk
        current_chunk.sections.append(section)
        current_chunk.end_line = section.end
        current_chunk.word_count += section_word_count

# Don't forget last chunk
chunks.append(current_chunk)
```

### Step 3: Chunk Metadata

Each chunk has:
```json
{
  "chunk_number": 1,
  "total_chunks": 6,
  "start_section": "2. Literature Review",
  "end_section": "3. Methodology",
  "start_line": 145,
  "end_line": 389,
  "word_count": 4235,
  "sections_included": ["2. Literature Review", "3. Methodology"]
}
```

## Processing Workflow

For each chunk:
1. Extract chunk content (lines start_line to end_line)
2. Send to subagent with chunk_info
3. Subagent edits only that chunk
4. Review chunk
5. Iteration loop (max 1 per chunk to control time)
6. Move to next chunk

After all chunks:
1. Reassemble document
2. Final consistency check
3. Git commit once

## Edge Cases

### Very Long Sections
If a single section exceeds 8,000 words:
- For .md: Try to split at ### subsection boundaries
- For .tex: Try to split at \subsection boundaries
- Last resort: Split at paragraph boundaries near 4,000-word mark

### Very Short Documents
If document < 6,000 words total:
- Do NOT chunk (overhead not worth it)
- Process as single pass

### Uneven Chunks
Final chunk might be smaller (< 3,000 words):
- Acceptable - better than forcing it into previous chunk
- Note in TodoWrite: "chunk 6/6 (final, 2,145 words)"

## Output formats

The user requests format(s) via `--format`. Default: `md`. Comma-separated lists are allowed (e.g. `--format md,pdf`); `all` expands to every supported format.

For each format **explicitly requested**, produce that file and only that file:

- `md`: write the markdown inline (only when `md` is in the requested set).
- `docx`: invoke the `docx` skill with the rendered content.
- `pdf`: render via the econstack Quarto template (or invoke the `pdf` skill if no template exists for this skill).
- `xlsx`: invoke the `xlsx` skill with the structured tables.
- `pptx`: invoke the `pptx` skill with the briefing as a deck.

**Do NOT produce formats that were not requested.** This is the v0.4 fix for the multi-format leak that previously caused `--format pdf` to also write `.md` and `.docx` files alongside the PDF. Any intermediate files needed during rendering must go to a temp directory and be cleaned up before the skill returns.

When you finish, the file listing in your "Saved:" message must contain exactly the files the user asked for, no extras.

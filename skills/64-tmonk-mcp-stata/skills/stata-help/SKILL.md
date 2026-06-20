---
name: stata-help
description: Look up Stata command documentation and display formatted help text.
---

The argument is the Stata command or help topic (e.g., "regress", "graph", "if", "egen", "frames").

Call `stata_get_help(topic=<argument>, plain_text=False, merge_paragraphs=True)`.

Display the help text. The response is formatted as Markdown. Present:
1. Syntax section first
2. Description and options
3. Examples if present

If no argument is provided, ask the user which Stata command they want help with.

If the help topic is not found (error in response), suggest:
- Checking spelling (e.g., "summarize" not "summarise")
- Using `help contents` as the topic for the help index
- Searching for related commands with `/stata-inspect` using `action="search"`

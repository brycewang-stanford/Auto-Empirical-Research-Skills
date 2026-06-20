# Research Productivity Skills

This collection vendors 18 practical agent skills for everyday research work:
paper discovery, literature synthesis, browser automation, file conversion,
slide production, Chinese text cleanup, and skill/command authoring.
It is intended as a compact productivity layer around the empirical-research
skills already in AERS.

## What Is Included

| Area | Skills | Use when you need to... |
|---|---|---|
| Academic discovery | [`academic-paper-search`](academic-paper-search/SKILL.md), [`arxiv`](arxiv/SKILL.md), [`nber-working-papers-api`](nber-working-papers-api/SKILL.md), [`unpaywall-api`](unpaywall-api/SKILL.md) | Search papers, retrieve metadata, locate working papers, find legal open-access full text |
| Literature synthesis | [`literature-survey-generator`](literature-survey-generator/SKILL.md), [`five-questions`](five-questions/SKILL.md), [`web-research`](web-research/SKILL.md) | Build cited research reports, generate literature surveys, analyze empirical economics papers through the five-question framework |
| Browser and web access | [`agent-browser`](agent-browser/SKILL.md), [`web-access`](web-access/SKILL.md) | Navigate sites, fill forms, test web apps, extract dynamic page content, work with logged-in browser sessions |
| File conversion | [`markitdown`](markitdown/SKILL.md), [`md-to-docx`](md-to-docx/SKILL.md) | Convert many document formats to Markdown, or turn Markdown into Chinese-friendly Word documents |
| Slides and presentations | [`marp-slides-creator`](marp-slides-creator/SKILL.md), [`marp-export`](marp-export/SKILL.md) | Create Marp slide decks, review them, and export to PDF/HTML/PPTX/PNG |
| Chinese writing cleanup | [`fix-chinese`](fix-chinese/SKILL.md), [`chinese-quote-converter`](chinese-quote-converter/SKILL.md) | Remove translation artifacts, reduce AI-sounding Chinese prose, fix Chinese quotation marks and typography |
| Authoring and automation | [`skill-creator`](skill-creator/SKILL.md), [`command-development`](command-development/SKILL.md), [`do-agent`](do-agent/SKILL.md) | Create or improve skills, define slash commands, or coordinate complex multi-agent tasks |

## How To Choose

- Start with `academic-paper-search` for broad paper discovery, then use
  `unpaywall-api` when the key problem is finding a legal full-text copy.
- Use `five-questions` when the input is an empirical economics paper and the
  desired output is a structured Chinese methodological reading report.
- Use `literature-survey-generator` when the desired output is a full survey
  draft rather than a search result list.
- Use `markitdown` before downstream writing tasks when the source material is
  trapped in PDF, Office, HTML, image, or audio formats.
- Use `marp-slides-creator` to create or revise the deck; use `marp-export`
  only after the Marp Markdown file is ready.
- Use `fix-chinese` proactively for Chinese prose cleanup; use
  `chinese-quote-converter` as a final typography pass.

## Licensing Notes

This is a mixed-origin collection. Check each skill folder and upstream project
before redistribution or commercial reuse. The collection intentionally does not
vendor the proprietary Anthropic document-office skills (`docx`/`pdf`/`pptx`/`xlsx`)
or the general-purpose UI design skills (`frontend-design`, `ui-ux-pro-max`);
install those from their authorized source instead of copying them into this
repository.

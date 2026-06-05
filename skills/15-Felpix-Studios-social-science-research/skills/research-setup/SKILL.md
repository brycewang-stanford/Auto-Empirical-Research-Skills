---
name: research-setup
description: >-
  Interactive setup wizard that configures a new project for the social-science-research plugin. Asks the user questions about their field, institution, journals, datasets, key researchers, and R color palette, then writes the answers into references/domain-profile.md and CLAUDE.md. Make sure to use this skill first whenever a user is starting fresh or wants to configure the plugin. Triggers include: "set up my project", "configure the plugin", "run setup", "initialize this project", "I just installed the plugin", "set my field", "set my institution", "configure my domain profile", or any request to personalize the plugin for a specific research context.
argument-hint: "(no arguments needed)"
allowed-tools: ["Read", "Write", "Edit", "Glob", "AskUserQuestion"]
---

# Research Setup Wizard

Walk the user through setup using AskUserQuestion menus wherever possible. Collect all answers, then write config files in one pass.

---

## Step 0: Check Existing Config

Read `CLAUDE.md` and `references/domain-profile.md` silently. If either has real content (not placeholders), tell the user what's already configured and offer to confirm or update each section.

---

## Step 1: Field & Identity

AskUserQuestion — 2 questions at once:

1. **Field** (single select, header: "Field"): "What is your field or subfield?" — Options: "Political Science", "Economics", "Sociology", "Public Health". User selects Other for unlisted fields.

2. **Institution** (single select, header: "Institution"): "What is your institution?" — Options: "Duke University", "Harvard University", "Stanford University", "UC Berkeley". User selects Other for unlisted fields.

Store field and institution for customizing later steps.

---

## Step 2: Name & Project Title

Ask conversationally (not via AskUserQuestion):

1. "What is your name (for paper authorship)? You can skip this for now."
2. "Do you have a working title for your current project? Fine to skip if you're still exploring."

Wait for the user's response before moving to Step 3.

---

## Step 3: Journals

AskUserQuestion — 2 multi-select questions based on the user's field:

1. **Top journals** (multiSelect, header: "Top journals"): "Select your top journals (pick all that apply):" — Offer the 4 most prestigious journals for the user's selected field. Use your knowledge of the field's top venues.

2. **Secondary journals** (multiSelect, header: "Secondary"): "Select secondary or subfield journals:" — Offer 4 secondary/subfield journals appropriate to the user's field.

User can multi-select presets and add custom journals via Other.

---

## Step 4: Datasets

AskUserQuestion — 2 multi-select questions based on the user's field:

1. **Common datasets** (multiSelect, header: "Datasets"): "Which datasets do you commonly use?" — Offer the 4 most-used datasets for the user's field. Use your knowledge of field-standard data sources.

2. **Additional sources** (multiSelect, header: "More data"): "Any additional data sources?" — Offer 4 cross-disciplinary sources: World Bank Open Data, IPUMS, Bureau of Labor Statistics, Census Bureau.

---

## Step 5: Researchers & Colors

AskUserQuestion — 2 questions at once:

1. **Researchers** (single select, header: "Researchers"): "Add key researchers for targeted literature searches?" — Options: "Skip for now" / "Add researchers".

2. **Colors** (single select, header: "Colors"): "Which color palette should R figures use?" — If the institution is well-known, offer its official brand colors as the recommended option with a preview showing the hex codes. Otherwise offer: "Custom colors" / "Skip for now".

If the user chose "Add researchers", ask conversationally for names, institutions, and Google Scholar URLs. Do NOT guess researcher names.

If the user chose "Custom colors", ask conversationally for primary and secondary hex codes.

---

## Step 6: Write Config Files

### `references/domain-profile.md`

Read the existing file and update each section with the user's answers. Preserve the file's existing structure and comments. Only replace sections the user answered; leave unanswered sections unchanged. Add an "Institutional Colors" section at the end if one doesn't exist, with the user's hex codes (or defaults #012169 / #f2a900 if skipped).

**IMPORTANT:** Do NOT write to `rules/r-code-conventions.md`. Colors live in `references/domain-profile.md` only.

### `CLAUDE.md`

Update the project header placeholders:
- `[YOUR PROJECT NAME]` → user's project title (or leave placeholder if skipped)
- `[YOUR NAME]` → user's name (or leave placeholder if skipped)
- `[YOUR INSTITUTION]` → user's institution

---

## Step 7: Confirm

```
Setup complete:
- references/domain-profile.md — field, [N] journals, [N] datasets[, N researchers][, colors]
- CLAUDE.md — project name and institution

Update anytime: references/domain-profile.md
Next step: /new-project
```

Note any skipped sections and where to add them later.

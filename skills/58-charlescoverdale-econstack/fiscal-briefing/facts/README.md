# Fact pack

Authoritative reference for fiscal definitions and rules that Claude consistently mishandles when generating briefings. Each file is a single topic.

The fiscal-briefing skill is required to read the relevant fact file BEFORE drafting any section that touches that topic. Files here override training-data recall.

## Files

- [triple_lock.md](triple_lock.md): UK state pension triple lock arms and which-arm-binds rule
- [fiscal_rules_uk.md](fiscal_rules_uk.md): Current Charter for Budget Responsibility numerical rules
- [debt_definitions_uk.md](debt_definitions_uk.md): PSND ex BoE, PSND incl BoE, PSNFL, PSNW
- [benefit_uprating.md](benefit_uprating.md): Working-age (CPI Sep) vs pensioner (triple lock) uprating
- [ons_classification.md](ons_classification.md): When is an entity inside the public sector boundary?

## Adding to the pack

Add a new file when:
- A factual error keeps recurring across briefings (the user keeps having to correct the same claim).
- A rule changes (e.g. new Charter, new welfare cap).
- A definition is non-obvious and easy to misremember.

Keep each file under 50 lines. Lead with the canonical definition, then add the dated wording (so a reader can tell which version of the rule the file describes).

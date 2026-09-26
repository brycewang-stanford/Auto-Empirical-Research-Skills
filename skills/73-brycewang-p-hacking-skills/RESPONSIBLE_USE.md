# Responsible use

## What this is

A measurement instrument for specification search ("p-hacking") in
design-based empirical economics, and a benchmark for whether AI research
agents perform such searches under pressure. It is published for academic
research on and teaching about p-hacking. **It is not intended for use in
real paper writing or research projects**, and its outputs are not suitable
as evidence for an empirical claim.

## Why it exists in public

The ability to search a specification space is already universal; the
ability to *measure* a search is not. Referees, replicators, teachers and
agent evaluators need to know how many defensible analyses a design admits,
how often a realistic search manufactures significance on null data, which
choice did the work, and what a searched p-value is worth. None of those
numbers exist without executing the search under instrumentation. The
tool follows Stefan & Schönbrodt's `phackR`, Simonsohn's p-curve and
specification-curve tools, and Asher et al.'s agent evaluation in taking
that view.

## Why it publishes a stopwatch

`phack race` reports how many seconds and how many model fits a realistic
search procedure needs to manufacture p < α on data whose true effect is
zero, and how often it succeeds. That number is this repository's threat
model stated quantitatively: the manufacture of a false positive now costs
one sentence to a coding agent and about a second of compute, while the
complete audit — ledger, null replay, honest p — costs under a minute.
Publishing the stopwatch does not lower the cost of the attack; a loop has
been cheap for decades and the race adds no search the engine did not
already instrument. What it removes is the last excuse for not auditing:
when the audit is priced in seconds, "too expensive to check" is no longer
a defensible review policy.

## What makes it safe to build

Every safeguard is mechanical, not advisory:

- **The ledger contract.** No command emits a "best specification" without
  `ledger.csv` (every specification estimated), the specification curve,
  the null-calibrated honest p-value of the whole search, and a report
  generated from those numbers.
- **Verifiability.** `manifest.json` hashes the data, card, ledger and
  audit; `phack verify RUN_DIR` lets anyone check a run directory,
  including a full recomputation of the audit.
- **Pathology flags.** Specifications that are citable but wrong stay in the
  ledger, flagged; the audit reports the best *unflagged* result alongside
  the headline.
- **Procedures are replayed.** A sequential search is calibrated against
  what the same procedure reports on null data, so its false-positive rate
  is part of the output.

A person who wants to p-hack a real analysis gains nothing from this tool
that a loop in their own software does not already give them, and loses the
ability to hide the search.

## The framing probes

`eval/prompts/` contains the prompt framings under which Asher et al. (2026)
observed frontier agents refusing or complying with a request to search for
significance. They are reproduced from that published replication archive
so the behaviour can be measured and defended against; they are catalogued
as an object of study, not offered as a technique. `skills/04-framing-attacks`
states the correct response to each framing, which is not refusal but
disclosure: compute the bound, label it as the maximum of a search, report
the search, and say that its p-value is not a p-value.

## What the tool will not do

- Produce a selected specification without the ledger and the honest p.
- Present a searched result as a confirmatory one; the report is generated
  from the audit and cannot be reduced to its headline sentence.
- Hide analyses: run directories are the unit of output, and thinning,
  seeds, schemes and procedures are recorded in the manifest.

## If you think it is being misused

Open an issue or contact the maintainer (see `pyproject.toml`). If a
published result cites a run of this tool, ask for the run directory and
run `phack verify` on it.

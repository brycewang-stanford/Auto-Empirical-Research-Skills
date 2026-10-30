# Review Tracing Protocol

## Purpose

Save full prompt/response pairs for every reviewer call, enabling:

- reviewer-independence audit
- reproducibility across follow-up reviewer turns
- meta-optimization from real review traces

## When to Trace

Trace every reviewer call from the Codex host that serves critique, scoring,
claim verification, experiment audit or patch gating. This includes selectable
routes under [reviewer-backends.md](reviewer-backends.md), regardless of family.

This includes:

- `spawn_agent` reviewer calls
- `send_input` reviewer continuations
- selected Antigravity, Grok or local Claude Code first calls and continuations
- legacy reviewer routes and existing partial overlay installations
- adversarial reviewer calls used for stress tests

Do not trace purely informational agent calls that are not acting as reviewers.

## How to Trace

After each reviewer call, save the trace using `save_trace.sh`,
resolved through the canonical helper chain (see
`integration-contract.md` §2 — failure policy C, "forensic helper").
A Codex-side SKILL must NOT hard-code `tools/save_trace.sh`; instead
it resolves `$TRACE_HELPER` via the chain and either invokes the
helper or writes trace artifacts directly per the schemas below. If
the resolver returns the empty string, write the four files inline
— do not silently skip unless `--- trace: off` was requested.

## Completion, identity and helper flags

Resolve the selected backend under [reviewer-backends.md](reviewer-backends.md)
and record its actual tool/session id. The default remains a fresh native Codex
reviewer, with same-family/provisional assurance. Other routes preserve their
own first-call and continuation parameters; they do not use native agent ids.
Keep the full raw response and the selected route's completion signal.

With `save_trace.sh`, pass `--backend`, `--tool`, `--executor codex`, the actual
`--executor-model` when known, and separate `--requested-reviewer-model` from
`--reported-reviewer-model`. A missing reported model stays unknown/null;
never copy the requested name into that flag. The helper's effective
`reviewer_model` falls back to the request only with source `requested`, which
cannot grant acceptance. It recognizes DeepSeek, xAI/Grok and the other known
families through `review_gate.py`; the route name is not a family identity.

Pass `--verdict "<actual verdict>"`. Add `--review-completed` only for a
successful finished review and `--review-scope-complete` only when the requested
inputs and obligations were actually covered. Add `--review-positive` only
after the skill's own positive gate succeeds. For `/auto-review-loop`, that means
score ≥ 6 AND verdict `ready`/`almost`, so a raw `ready` at score 5 is not positive.
Other steps may use `clean`, PASS/KILL schemes or another raw verdict; keep that
value in `--verdict` rather than duplicating its gate logic in the trace helper.
For example, after checking those facts for a selected Grok review:

```bash
bash "$TRACE_HELPER" --skill "research-review" --purpose "initial-review" \
  --backend grok --tool mcp__grok__grok --executor codex \
  --executor-model "$ACTUAL_EXECUTOR_MODEL" \
  --requested-reviewer-model "$REQUESTED_MODEL" \
  --reported-reviewer-model "$REPORTED_MODEL" --model "$REPORTED_MODEL" \
  --effort "$ACTUAL_EFFORT" --thread-id "$THREAD_ID" \
  --prompt-file "$PROMPT_FILE" --response-file "$RESPONSE_FILE" \
  --status ok --verdict ready --review-completed --review-scope-complete --review-positive
```

The helper recognizes successful statuses `ok`, `fallback_used`, `success`, and
`completed`. It does not infer positivity from verdict text or scores. Use
`--status error` for failures, preserving the actual outcome; do not add completion
or positivity flags by default. A raw ready/PASS/WARN/clean alone cannot establish
acceptance. `--trace-mode full|meta|off` selects the helper's storage mode.
The inline fallback writer follows the same provenance/completion rules.

`review_independence` is `same-family`, `cross-family`, or `unknown`, derived
from the effective model pair. `acceptance_status` stays `provisional` unless a
successful, completed, in-scope review with explicit skill-gate positivity has
known different actual families and a backend-reported or validated host-event
model. Unknown,
requested-only, incomplete or negative outcomes remain provisional. The
substantive verdict and call status stay separate. Identity evidence also stays
separate: a known family relation alone never makes `independence_verified`
true. The main pack's compatibility Copilot drive mode always stays provisional;
its native host-event evidence and external-finalizer obligations remain as
documented in the main [routing reference](../../shared-references/reviewer-routing.md).

A trace's accepted classification does not replace the skill's proof, citation,
experiment or submission gate. A deterministic verifier can accept only the
properties it actually checks; it cannot impersonate a semantic model review.
Existing partial overlays do not automatically confer acceptance.

## Trace Directory

```text
.aris/traces/<skill-name>/<YYYY-MM-DD>_run<NN>/
  run.meta.json
  001-<purpose>.request.json
  001-<purpose>.response.md
  001-<purpose>.meta.json
  002-<purpose>.request.json
  ...
```

## File Schemas

`run.meta.json` stores initial context, not an overall acceptance decision.
Later call outcomes and model changes belong in their own metadata:

`run.meta.json`:

```json
{
  "skill": "auto-review-loop",
  "run_id": "2026-04-15_run01",
  "started_at": "2026-04-15T14:30:00+08:00",
  "executor": "codex",
  "executor_model": "gpt-6-astra",
  "executor_family": "openai",
  "executor_model_source": "caller-declared",
  "reviewer_backend": "codex",
  "project_dir": "/path/to/project"
}
```

`NNN-<purpose>.request.json`:

```json
{
  "call_number": 1,
  "purpose": "round-1-review",
  "timestamp": "2026-04-15T14:31:00+08:00",
  "tool": "spawn_agent",
  "model": "gpt-6-astra",
  "effort": "xhigh",
  "backend": "codex",
  "executor_model": "gpt-6-astra",
  "executor_family": "openai",
  "requested_reviewer_model": "gpt-6-astra",
  "reported_reviewer_model": null,
  "reviewer_model": "gpt-6-astra",
  "reviewer_model_source": "requested",
  "review_independence": "same-family",
  "acceptance_status": "provisional",
  "review_completed": true,
  "review_scope_complete": true,
  "verdict": "ready",
  "files_referenced": [
    "paper/sections/3_method.tex",
    "results/table1.csv"
  ],
  "prompt": "<full prompt text>",
  "review_positive": true
}
```

`NNN-<purpose>.response.md` stores the full reviewer response verbatim.

`NNN-<purpose>.meta.json`:

```json
{
  "call_number": 1,
  "purpose": "round-1-review",
  "timestamp": "2026-04-15T14:33:00+08:00",
  "agent_id": "019d8fe0-b25d-...",
  "model": "gpt-6-astra",
  "reviewer_model": "gpt-6-astra",
  "reviewer_model_source": "requested",
  "requested_reviewer_model": "gpt-6-astra",
  "reported_reviewer_model": null,
  "model_family": "openai",
  "review_completed": true,
  "review_scope_complete": true,
  "verdict": "ready",
  "review_independence": "same-family",
  "acceptance_status": "provisional",
  "duration_ms": 142000,
  "status": "ok",
  "review_positive": true
}
```

The request and call metadata retain `reviewer_model`, model source,
`review_independence`, `acceptance_status`, `review_completed`,
`review_scope_complete`, `review_positive`, and raw `verdict` in both full and
meta modes. `model` keeps
its legacy caller-supplied meaning; use `reviewer_model` and its source to
interpret the effective identity. A request-only example above remains
provisional even when the review completed. Helper output records native/MCP
session identity as `thread_id`; direct native writers may additionally retain
`agent_id`. Keep the returned identifier appropriate to the selected route.

## Configuration

Respect inline parameter `--- trace: off | meta | full`:

- `full` default: save full prompt and full response
- `meta`: save metadata only
- `off`: disable tracing

## Events

After writing a trace, append a compact event to `.aris/meta/events.jsonl`:

```json
{"event":"review_trace","skill":"auto-review-loop","purpose":"round-1-review","agent_id":"...","trace_path":".aris/traces/auto-review-loop/2026-04-15_run01/","status":"ok"}
```

## Debugging With Traces

Traces are not only audit evidence — they are the **first place to look when a
verdict is surprising**: a score regresses round-to-round, two reviewer agents
disagree, or a claim check contradicts an earlier round. Before re-invoking the
reviewer for "a better answer", read the raw transcript and find the moment its
judgment actually changed:

```bash
skill=auto-review-loop run=2026-04-15_run01
diff ".aris/traces/$skill/$run/002-round-2.response.md" \
     ".aris/traces/$skill/$run/003-round-3.response.md"
grep -En 'however|but|concern|missing|cannot' \
     ".aris/traces/$skill/$run/003-round-3.response.md"
```

The paragraph where the assessment changed **is** the causal explanation for the
divergence — cite it, don't guess. Re-running the reviewer without reading the
trace is tuning by vibe: you get a new opinion, not an explanation. Same muscle
as reading a stack trace before retrying a failed run — the trace is just
written in English, and most of it is the reviewer talking to itself.

## Privacy

`.aris/traces/` is project-local and should not be committed. Use `--- trace: off` for strict confidentiality projects.

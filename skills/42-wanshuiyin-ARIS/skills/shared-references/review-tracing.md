# Review Tracing Protocol

## Purpose

Save full prompt/response pairs for every reviewer call, enabling:
- **Reviewer-independence audit**: verify the executor only passed file paths, not summaries
- **Reproducibility**: threadId preservation allows conversation continuation
- **Meta-optimize input**: richer data for harness improvement analysis

## When to Trace

After **every** native `task(agent_type=rubber-duck)` (`copilot-native`),
`mcp__codex__codex`, `mcp__codex__codex-reply`, compatibility
`copilot --agent`, `mcp__manual_review__review`, or
`mcp__manual_review__review_reply`, or selectable Antigravity/Grok/Claude Code
first-call or continuation under [reviewer-backends.md](reviewer-backends.md)
that serves a reviewer/critique
function. This includes review scoring, experiment auditing, claim
verification, idea critique, and patch gating.

Do NOT trace: purely informational LLM calls (e.g., `codex exec` for code generation that is not a review).

## Trace Directory

```
.aris/traces/<skill-name>/<YYYY-MM-DD>_run<NN>/
  ├── run.meta.json                      # Run-level metadata
  ├── 001-<purpose>.request.json         # Request snapshot
  ├── 001-<purpose>.response.md          # Full response text
  ├── 001-<purpose>.meta.json            # Response metadata
  ├── 002-<purpose>.request.json         # Second call (e.g., reply)
  └── ...
```

- `<skill-name>`: the ARIS skill that triggered this call (e.g., `auto-review-loop`)
- `<YYYY-MM-DD>_run<NN>`: date + sequential run number (start from `01`)
- `<purpose>`: short kebab-case label (e.g., `round-1-review`, `critique`, `ideation`, `audit`, `patch-gate`)

## How to Trace

After each reviewer call — including every FAILED attempt in a
capability-fallback chain (one trace entry per attempt: `--status error` +
`--fallback-reason`; the successful entry records the RESOLVED pair) — save the trace using `save_trace.sh`,
resolved through the canonical helper chain (see
`integration-contract.md` §2 — failure policy C, "forensic helper").
The full invocation:

```bash
# Resolve $TRACE_HELPER (canonical strict-safe chain; see integration-contract.md §2).
cd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)" || exit 1
if [ -z "${ARIS_REPO:-}" ] && [ -f .aris/installed-skills.txt ]; then
    ARIS_REPO=$(awk -F'\t' '$1=="repo_root"{print $2; exit}' .aris/installed-skills.txt 2>/dev/null) || true
fi
if [ -z "${ARIS_REPO:-}" ] && [ -f "$HOME/.aris/repo" ]; then
    ARIS_REPO=$(cat "$HOME/.aris/repo" 2>/dev/null) || true
fi
TRACE_HELPER=".aris/tools/save_trace.sh"
[ -f "$TRACE_HELPER" ] || TRACE_HELPER="tools/save_trace.sh"
[ -f "$TRACE_HELPER" ] || { [ -n "${ARIS_REPO:-}" ] && TRACE_HELPER="$ARIS_REPO/tools/save_trace.sh"; }
[ -f "$TRACE_HELPER" ] || TRACE_HELPER=""

if [ -n "$TRACE_HELPER" ]; then
  bash "$TRACE_HELPER" \
    --skill "<skill-name>" \
    --purpose "<purpose>" \
    --model "<model that actually ran — the RESOLVED pair, not the target>" \
    --effort "<effort that actually ran>" \
    --fallback-reason "<why the capability chain stepped down; empty when it didn't>" \
    --status "<ok | fallback_used | error>" \
    --thread-id "<threadId from response>" \
    --backend "<codex | antigravity | grok | claude-code | copilot-native | copilot | manual | oracle-pro | agy | llm-chat>" \
    --tool "<mcp__codex__codex | task(agent_type=rubber-duck) | copilot --agent | ...>" \
    --executor "<claude-code | copilot | codex>" \
    --executor-model "<actual current executor model; omit if unknown>" \
    --executor-family "<legacy consistency hint; helper re-derives from executor-model>" \
    --reviewer-profile "<profile name for copilot backend; empty for others>" \
    --reviewer-family "<legacy consistency hint; helper re-derives from reviewer model>" \
    --requested-reviewer-model "<model originally requested>" \
    --reported-reviewer-model "<model the backend reports it used>" \
    --memory-hash "<sha256 of memory artifact if available; empty otherwise>" \
    --native-evidence "<required for copilot-native; omit otherwise>" \
    --independence-verified "<legacy consistency hint; helper ignores and re-derives>" \
    --prompt "<full prompt as sent>" \
    --response "<full response content>"
else
  # Required fallback: the resolver exhausted all four layers and
  # save_trace.sh is unreachable, but trace artifacts are still
  # required (unless `--- trace: off` was explicitly set on this
  # SKILL invocation). Write the four files below directly per the
  # schemas in "File Schemas", into:
  #   .aris/traces/<skill-name>/<YYYY-MM-DD>_run<NN>/
  #     run.meta.json
  #     <NNN>-<purpose>.request.json
  #     <NNN>-<purpose>.response.md
  #     <NNN>-<purpose>.meta.json
  # Do NOT silently skip — trace_path is load-bearing for any
  # mandatory audit emitting `trace_path` in its artifact (see
  # assurance-contract.md §"Required Audit Artifact Schema").
  echo "WARN: save_trace.sh not resolved; writing trace files directly per review-tracing.md schema." >&2
fi
```

The helper, when present, handles directory creation, run numbering, file
writing, and provenance classification. For a successful `copilot-native`
call, it first revalidates `--native-evidence`, overrides caller model/response
fields with the host-bound values, and records the evidence ID/path; missing or
invalid evidence is an error. A native dispatch that failed before evidence
could exist may be traced only with `--status error` and no
`--native-evidence`; that record has no verified model provenance or
independence and can never enter the stop gate. For other backends it derives
families from model strings
(`reported_reviewer_model`, otherwise `requested_reviewer_model`, otherwise
`model`) and ignores contradictory caller family/independence claims. It also
records that `--executor-model` is `caller-declared`; a different family pair is
`family_relation: "different"` but remains `independence_verified: "unverified"`.
Validated native evidence instead records both sources as
`host-session-event`, `family_relation: "different"`, and
`independence_verified: true`.

The native-specific required pair for a completed review is:

```bash
bash "$TRACE_HELPER" ... --backend copilot-native \
  --native-evidence "review-stage/COPILOT_NATIVE_${RUN_ID}_ROUND_${ROUND}_REVIEW.evidence.json"
```

Omit `--native-evidence` for every other backend.
For a failed native dispatch, instead use `--backend copilot-native --status
error --fallback-reason "<host error>"` without evidence, then write a separate
trace for any fallback backend that actually reviews the artifacts.
The fallback branch above documents what to do
when the helper is unreachable — the trace is forensic evidence, so
"helper missing" never means "skip the trace." A direct fallback writer MUST
apply the same model-string derivation and evidence-source rules; it may not
copy caller family labels or promote caller-declared identity to verification.

## Completion and assurance per call

Follow [reviewer-backends.md](reviewer-backends.md) for the selected route's
success signal and actual model/effort source. Trace requested and returned
models separately: a `claude-code` result can be DeepSeek, and an Antigravity
result can be Claude. A missing reported model remains unknown; a request alias
cannot become actual identity evidence.

Pass `--verdict "<actual verdict>"` to preserve the substantive assessment.
Add `--review-completed` only after a successful, finished review and
`--review-scope-complete` only when it covered the required inputs and review
obligations. Add `--review-positive` only after the skill's own gate determines
the review is positive. For example, `/auto-review-loop` requires score ≥ 6 AND
verdict `ready`/`almost`; a raw `ready` with score 5 is not positive. Other skills
can use `clean`, PASS/KILL schemes or their own verdicts without adding another
parser here. Preserve that raw value with `--verdict`; the trace helper does not
infer positivity from it. None of these flags follows from selecting a provider.
For example, after those facts have been checked for a Grok review:

```bash
bash "$TRACE_HELPER" --skill "research-review" --purpose "initial-review" \
  --backend grok --tool mcp__grok__grok --executor claude-code \
  --executor-model "$ACTUAL_EXECUTOR_MODEL" \
  --requested-reviewer-model "$REQUESTED_MODEL" \
  --reported-reviewer-model "$REPORTED_MODEL" --model "$REPORTED_MODEL" \
  --effort "$ACTUAL_EFFORT" --thread-id "$THREAD_ID" \
  --prompt-file "$PROMPT_FILE" --response-file "$RESPONSE_FILE" \
  --status ok --verdict ready --review-completed --review-scope-complete --review-positive
```

Use `--status error` for failed calls, preserving their raw response/error, and
omit completion flags when they are not established. The helper recognizes
successful statuses `ok`, `fallback_used`, `success`, and `completed`. A raw
`ready`, `PASS`, `WARN` or `clean` never establishes positivity, completion or
acceptance without the appropriate explicit flags. A negative, unavailable,
unknown-model, or incomplete call stays provisional; its status and verdict
explain why. Compatibility `copilot` traces remain drive-only/provisional and
still require their separate finalizer. Native Copilot retains the validated
host-event rules above.

Each request and call metadata artifact records `reviewer_model`,
`review_independence`, `acceptance_status`, `review_completed`,
`review_scope_complete`, `review_positive`, and raw `verdict`. Known same-family
model strings yield `same-family / provisional`. Known different families can yield
`cross-family / accepted` only for successful, complete, in-scope review with
explicit skill-gate positivity and a backend-reported or validated host-event
reviewer model. Unknown families yield `unknown / provisional`; request-only identity never grants
acceptance. `reviewer_model` is the effective value: reported output first, then
request fallback with source `requested`. Keep that source visible.
`independence_verified` retains its separate identity-evidence meaning and is
not automatically `true` for an accepted cross-family review.

`run.meta.json` captures initial run context, not an overall acceptance verdict.
Later calls may have different models or outcomes; read their call metadata.
A trace's accepted classification does not replace the skill's substantive
proof, citation, experiment or submission gate. Direct fallback writers use the
same rules and do not manufacture an accepted result when the helper is absent.

## File Schemas

### `run.meta.json`
```json
{
  "skill": "auto-review-loop",
  "run_id": "2026-04-15_run01",
  "started_at": "2026-04-15T14:30:00+08:00",
  "executor": "claude-code",
  "executor_model": "claude-sonnet-4-5",
  "executor_model_source": "caller-declared",
  "executor_family": "anthropic",
  "reviewer_model_source": "requested",
  "reviewer_family": "openai",
  "reviewer_backend": "codex",
  "native_evidence_id": null,
  "native_evidence_path": null,
  "family_relation": "different",
  "independence_verified": "unverified",
  "project_dir": "/path/to/project"
}
```

- `executor`: the name of the running executor (from `--executor` parameter; defaults to `"claude-code"`). Dynamic — set by the caller, not hardcoded.
- `executor_model`: the declared model running this ARIS invocation (from `--executor-model` when available; otherwise `null`).
- `executor_model_source`: `"host-session-event"` for validated native evidence,
  `"caller-declared"` when a non-native caller passes `--executor-model`, or
  `"unavailable"`.
- `executor_family`: derived from `executor_model`; supported families include
  OpenAI, Anthropic, Google, DeepSeek and xAI/Grok. Unknown names stay `unknown`.
- `reviewer_model_source`: `"host-session-event"`, `"backend-reported"`,
  `"requested"`, or `"unavailable"`.
- `reviewer_family`: derived from the backend-reported model when available, otherwise the requested model.
- `family_relation`: `different`, `same`, or `unknown`, derived from model strings.
- `independence_verified`: `true` only for a revalidated native cross-family
  event chain, `false` for known same-family identities, otherwise
  `"unverified"`.
- `native_evidence_id` / `native_evidence_path`: set only for
  `copilot-native`; `null` for other backends.
- `reviewer_backend`: `codex` / `copilot-native` / `copilot` / `manual` /
  `oracle-pro` / `agy` / `llm-chat` / `antigravity` / `grok` / `claude-code`.

### `NNN-<purpose>.request.json`
```json
{
  "call_number": 1,
  "purpose": "round-1-review",
  "timestamp": "2026-04-15T14:31:00+08:00",
  "tool": "mcp__codex__codex",
  "backend": "codex",
  "model": "gpt-6-astra",
  "config": {
    "model_reasoning_effort": "xhigh"
  },
  "reviewer_profile": null,
  "files_referenced": [
    "paper/sections/3_method.tex",
    "results/table1.csv"
  ],
  "prompt": "<full prompt text>",
  "reviewer_model": "gpt-6-astra",
  "review_independence": "unknown",
  "acceptance_status": "provisional",
  "review_completed": false,
  "review_scope_complete": false,
  "verdict": null,
  "review_positive": false
}
```

For native Copilot backend (no reviewer override in a bound Copilot session):
```json
{
  "call_number": 1,
  "purpose": "round-1-review",
  "tool": "task(agent_type=rubber-duck)",
  "backend": "copilot-native",
  "model": "gpt-5.5",
  "executor_model": "claude-sonnet-4.6",
  "executor_model_source": "host-session-event",
  "executor_family": "anthropic",
  "reported_reviewer_model": "gpt-5.5",
  "reviewer_model_source": "host-session-event",
  "reviewer_family": "openai",
  "family_relation": "different",
  "independence_verified": true,
  "native_evidence_id": "cne_0123456789abcdef0123456789abcdef",
  "native_evidence_path": "/project/review-stage/COPILOT_NATIVE_run_20260715_a1b2c3d4_ROUND_1_REVIEW.evidence.json",
  "prompt": "<full nonce-bound native task prompt>",
  "reviewer_model": "gpt-5.5",
  "review_independence": "cross-family",
  "acceptance_status": "accepted",
  "review_completed": true,
  "review_scope_complete": true,
  "verdict": "ready",
  "review_positive": true
}
```

For compatibility copilot backend (`--reviewer: copilot`):
```json
{
  "call_number": 1,
  "purpose": "round-1-review",
  "timestamp": "2026-04-15T14:31:00+08:00",
  "tool": "copilot --agent",
  "backend": "copilot",
  "model": "gpt-5.4",
  "effort": "xhigh",
  "effort_unpinned": false,
  "reviewer_profile": "aris-reviewer-openai",
  "requested_reviewer_model": "gpt-5.4",
  "reported_reviewer_model": null,
  "executor_model": "claude-sonnet-4-5",
  "executor_model_source": "caller-declared",
  "executor_family": "anthropic",
  "reviewer_model_source": "requested",
  "reviewer_family": "openai",
  "family_relation": "different",
  "independence_verified": "unverified",
  "files_referenced": [
    "paper/sections/3_method.tex",
    "results/table1.csv"
  ],
  "prompt": "<full prompt text>",
  "reviewer_model": "gpt-5.4",
  "review_independence": "cross-family",
  "acceptance_status": "provisional",
  "review_completed": false,
  "review_scope_complete": false,
  "verdict": null,
  "review_positive": false
}
```

Fields:
- `tool`: the tool name used (`task(agent_type=rubber-duck)`,
  `mcp__codex__codex`, `copilot --agent`, etc.).
- `backend`: the logical backend (`codex`, `copilot-native`, compatibility
  `copilot`, `manual`, `oracle-pro`, `agy`).
- `effort_unpinned`: applies only to compatibility `copilot`; native
  complementary dispatch does not accept an ARIS model/effort pin.
- `reviewer_profile`: custom profile for compatibility copilot; `rubber-duck`
  may be used as a descriptive value for native traces; `null` otherwise.
- `requested_reviewer_model`: the requested model or selected profile model;
  `null` when unavailable. It is request metadata, not actual model evidence.
- `reported_reviewer_model`: the model the tool reports actually using (for example, captured Copilot `gen_ai.response.model` telemetry); `null` when unavailable.
- `executor_model`: native host-event value, or from `--executor-model` on
  legacy/non-native paths; `null` if unavailable.
- `executor_model_source`: `host-session-event`, `caller-declared`, or
  `unavailable`.
- `executor_family`: derived from `executor_model`.
- `reviewer_model_source`: `host-session-event`, `backend-reported`, `requested`,
  or `unavailable`.
- `reviewer_family`: derived by the helper from the reported/requested/actual reviewer model, never trusted from the caller.
- `family_relation`: string-derived relation (`different` / `same` / `unknown`).
- `independence_verified`: `true` only for validated native cross-family
  evidence; `false` for known same-family; `"unverified"` for advisory pairs.
- `native_evidence_id` / `native_evidence_path`: bind a native trace to the
  revalidated session-event artifact; `null` otherwise.

### `NNN-<purpose>.response.md`
The reviewer's full response, verbatim. No truncation, no summarization.

### `NNN-<purpose>.meta.json`
```json
{
  "call_number": 1,
  "purpose": "round-1-review",
  "timestamp": "2026-04-15T14:33:00+08:00",
  "thread_id": "019d8fe0-b25d-...",
  "model": "gpt-6-astra",
  "model_family": "openai",
  "executor_model": null,
  "executor_model_source": "unavailable",
  "executor_family": "unknown",
  "reviewer_model_source": "requested",
  "family_relation": "unknown",
  "independence_verified": "unverified",
  "reviewer_profile": null,
  "duration_ms": 142000,
  "status": "ok",
  "reviewer_model": "gpt-6-astra",
  "review_independence": "unknown",
  "acceptance_status": "provisional",
  "review_completed": false,
  "review_scope_complete": false,
  "verdict": null,
  "review_positive": false
}
```

For compatibility copilot backend:
```json
{
  "call_number": 1,
  "purpose": "round-1-review",
  "timestamp": "2026-04-15T14:33:00+08:00",
  "thread_id": null,
  "model": "gpt-5.4",
  "model_family": "openai",
  "effort": "xhigh",
  "effort_unpinned": false,
  "executor_model": "claude-sonnet-4-5",
  "executor_model_source": "caller-declared",
  "executor_family": "anthropic",
  "requested_reviewer_model": "gpt-5.4",
  "reported_reviewer_model": null,
  "reviewer_model_source": "requested",
  "family_relation": "different",
  "independence_verified": "unverified",
  "reviewer_profile": "aris-reviewer-openai",
  "duration_ms": 142000,
  "status": "ok",
  "reviewer_model": "gpt-5.4",
  "review_independence": "cross-family",
  "acceptance_status": "provisional",
  "review_completed": false,
  "review_scope_complete": false,
  "verdict": null,
  "review_positive": false
}
```

Per-call fields:
- `model_family`: derived from the effective `reviewer_model`, using the same
  recognized-family mapping as `review_gate.py` (including DeepSeek and xAI).
  When source is `requested`, this is only a request-derived family hint.
- `effort_unpinned`: whether a compatibility Copilot subprocess lacked the
  required explicit `xhigh` pin; it does not apply to native dispatch.
- `executor_model` / `executor_model_source`: native calls record the actual
  host event model/source; compatibility routing records `caller-declared`.
- `executor_family`: derived from `executor_model`; `unknown` if not known.
- `requested_reviewer_model`: the requested model or profile model repeated
  through subprocess `--model`; `null` when unavailable.
- `reported_reviewer_model`: actual backend output, or `null` when unavailable;
  never fill it with a requested model. `reviewer_model_source` identifies whether
  the effective reviewer model came from that output or a request fallback.
- `family_relation`: the model-string relation, separate from evidence assurance.
- `independence_verified`: never `true` solely because caller-declared and requested model strings differ; use `"unverified"` in that case.
- `reviewer_profile`: for compatibility copilot, the custom agent profile;
  native may record `rubber-duck`; `null` for other backends.
- `native_evidence_id` / `native_evidence_path`: present only on validated
  `copilot-native` traces.
- `memory_hash`: SHA-256 of `review-stage/REVIEWER_MEMORY.md` at trace time; `null` when no memory file exists.

## Configuration

Tracing respects three modes, set via inline parameter `--- trace: off | meta | full`:
- **`full`** (default): save full prompt + full response
- **`meta`**: save metadata only (no prompt/response text), useful for sensitive projects
- **`off`**: disable tracing entirely

## Integration with events.jsonl

After writing a trace, append a compact summary event to `.aris/meta/events.jsonl`:

```json
{"event":"review_trace","skill":"auto-review-loop","purpose":"round-1-review","thread_id":null,"trace_path":".aris/traces/auto-review-loop/2026-04-15_run01/","backend":"copilot-native","tool":"task(agent_type=rubber-duck)","executor_model":"claude-sonnet-4.6","executor_model_source":"host-session-event","executor_family":"anthropic","reviewer_model_source":"host-session-event","reviewer_family":"openai","family_relation":"different","independence_verified":true,"native_evidence_id":"cne_0123456789abcdef0123456789abcdef","native_evidence_path":"/project/review-stage/COPILOT_NATIVE_run_20260715_a1b2c3d4_ROUND_1_REVIEW.evidence.json","status":"ok"}
```

This allows `/meta-optimize` to discover traces without reading the full trace files.

## Debugging With Traces

Traces are not only audit evidence — they are the **first place to look when a
verdict is surprising**: a score regresses round-to-round, two reviewer backends
disagree, or `/result-to-claim` contradicts an earlier claim. Before re-invoking
the reviewer for "a better answer", read the raw transcript and find the moment
its judgment actually changed:

```bash
# Diff the raw response bodies across the two calls in question
skill=auto-review-loop run=2026-04-15_run01
diff ".aris/traces/$skill/$run/002-round-2.response.md" \
     ".aris/traces/$skill/$run/003-round-3.response.md"

# Grep for the sentence where the assessment turned
grep -En 'however|but|concern|missing|cannot' \
     ".aris/traces/$skill/$run/003-round-3.response.md"
```

The paragraph where the assessment changed **is** the causal explanation for the
divergence — cite it, don't guess. Re-running the reviewer without reading the
trace is tuning by vibe: you get a new opinion, not an explanation.

This is the same muscle ARIS already applies to code failures (the "**Read the
error** — parse traceback, stderr, and log files" step in `/experiment-bridge`'s
auto-debug sequence, and `/codex:rescue` reading tracebacks before a retry) —
applied to saved AI-judgment transcripts instead of stderr. The trace is written
in English and most of it is the reviewer talking to itself; the discipline is
identical: read the primary artifact first, then act on the exact divergence
point rather than re-rolling the dice.

Practical triggers:

| Surprise | Trace move |
|---|---|
| Score dropped after a "fix" round | diff the two rounds' `.response.md`; find which criterion flipped |
| Two backends disagree (codex vs gemini/manual) | grep both responses for the SAME artifact path; compare what each actually read |
| Reviewer "forgot" an earlier concern | grep prior rounds for the concern keyword; if present-then-absent, cite it in the next prompt instead of restating from memory |
| Verdict contradicts a deterministic checker | read the request `.md` — was the checker's output actually in the files the reviewer was pointed at? |

## Privacy

- `.aris/traces/` should be in `.gitignore` — traces are project-local, never committed
- Traces may contain sensitive research content; treat them as confidential
- Use `--- trace: off` for projects with strict confidentiality requirements

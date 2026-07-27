# Kaggle Research Integration Design

**Date:** 2026-07-27
**Status:** Approved for implementation planning
**Target branch:** `feat/kaggle-research-integration`

## Purpose

Add a first-party, independently installable Kaggle research collection to
Auto-Empirical Research Skills (AERS). The collection will provide a safe,
auditable Python wrapper around the official Kaggle CLI for dataset discovery,
competition workflows, notebook/kernel execution, model access, and artifact
retrieval.

The implementation will be suitable for contribution upstream. It will follow
the repository's catalog, provenance, documentation, security, and test gates.

## Goals

- Add collection `skills/72-kaggle-research/` with one discoverable
  `kaggle-research` skill.
- Cover the official Kaggle CLI resource groups used in research:
  authentication checks, datasets, competitions, kernels, models, and generic
  future CLI subcommands.
- Keep the AERS root dependency set unchanged.
- Run Kaggle in a dedicated Python 3.11+ environment with
  `kaggle>=2.2,<3`.
- Provide deterministic unit, contract, security, and policy tests.
- Provide a separate, opt-in live test lane that uses the real Kaggle service,
  real public resources, and a real local API token. Live tests must not replace
  network calls or downloaded data with mocks.
- Produce redacted command audit records and artifact manifests suitable for a
  reproducible research audit trail.
- Make remote writes explicit and remote deletion harder to trigger
  accidentally.

## Non-goals

- Do not copy the project-specific `med-report-gen` notebooks, configurations,
  paths, or slugs from `D:\Download\Kaggle`.
- Do not integrate Google Colab.
- Do not vendor Kaggle datasets, model weights, notebook outputs, or credentials.
- Do not implement undocumented Kaggle REST or MCP protocols.
- Do not add `kaggle` to the root `requirements.txt`.
- Do not require a Kaggle account for the repository's normal offline unit test
  suite.
- Do not run remote create, submit, push, update, or delete operations in the
  default live test lane.

## Source and License Boundary

`D:\Download\Kaggle` is a behavioral reference and a source of local test
credentials only. Its scripts contain project-specific paths and currently do
not provide a reusable licensed component for this repository. The new runtime
will therefore be implemented from the approved design and official Kaggle CLI
documentation, not copied verbatim.

The new first-party collection uses the repository-default license. The
official Kaggle CLI remains an external Apache-2.0 dependency installed by the
user into an isolated environment.

## Collection Layout

```text
skills/72-kaggle-research/
├── README.md
└── kaggle-research/
    ├── SKILL.md
    ├── references/
    │   ├── authentication.md
    │   ├── datasets.md
    │   ├── competitions.md
    │   ├── kernels.md
    │   ├── models.md
    │   └── testing-and-safety.md
    ├── scripts/
    │   ├── kaggle_research.py
    │   └── kaggle_runtime/
    │       ├── __init__.py
    │       ├── artifacts.py
    │       ├── commands.py
    │       ├── result.py
    │       ├── runner.py
    │       └── security.py
    └── tests/
        ├── __init__.py
        ├── test_artifacts.py
        ├── test_commands.py
        ├── test_live_readonly.py
        ├── test_runner.py
        └── test_security.py
```

Repository integration will also update:

- `scripts/build-provenance.py` for first-party source/license metadata.
- `Makefile` so the collection tests and Python compatibility checks run in
  normal gates.
- The root router and relevant README/data-acquisition indexes.
- Generated catalog, provenance, audit, release-note, and documentation
  artifacts produced by the existing builders.
- Root tests only where a repository-wide invariant needs explicit regression
  coverage.

## Runtime Architecture

### Command request

`CommandRequest` is an immutable typed request containing:

- Kaggle argument tuple, excluding the executable.
- Working directory.
- Local output root, when a command writes files locally.
- Timeout.
- Operation classification.
- `allow_write`, `allow_delete`, and exact deletion confirmation.
- Audit directory and output-capture limits.

### Command policy

`commands.py` constructs argument arrays and classifies operations:

- `READ`: remote read with no expected local artifacts, such as list, files,
  status, view, or metadata.
- `DOWNLOAD`: remote read with local filesystem writes, such as dataset,
  competition, kernel-output, or model download.
- `REMOTE_WRITE`: create, update, version, submit, push, or configuration
  mutation.
- `REMOTE_DELETE`: any delete operation.
- `UNKNOWN`: a future or unrecognized official command.

`READ` is allowed by default. `DOWNLOAD` is allowed only with a validated output
root. `REMOTE_WRITE` and `UNKNOWN` require `--allow-write`. `REMOTE_DELETE`
requires `--allow-write`, `--allow-delete`, and an exact resource confirmation.
Dry-run is available for every classification.

The policy is enforced before starting a subprocess. It is a safety boundary,
not an authorization system.

### Runner

`runner.py`:

- Executes an argument list with `shell=False`.
- Uses the configured Kaggle executable or the isolated environment's Python
  module entry point.
- Sets UTF-8 process variables for cross-platform output.
- Preserves the caller's official Kaggle authentication environment without
  reading credential files.
- Applies timeouts and terminates the child process on timeout.
- Retries only eligible `READ` or `DOWNLOAD` operations after recognized
  transient failures.
- Never automatically retries remote writes or deletes.
- Returns a structured `CommandResult`; it does not print secrets or raise raw
  `subprocess` exceptions across the public boundary.

### Security

`security.py`:

- Redacts bearer tokens, `KAGGLE_API_TOKEN`, legacy username/key pairs,
  authorization headers, and signed URL query parameters.
- Resolves local paths before use.
- Rejects download destinations outside the approved output root.
- Rejects unsafe resource references and embedded control characters.
- Prevents shell invocation and string-built commands.

The runtime will never search for or parse `.env`, IDE configuration, or
arbitrary credential files. Authentication remains owned by the official
Kaggle CLI.

### Audit and artifacts

Each executed operation can emit a JSON audit record containing:

- Schema version and operation UUID.
- UTC start/end time and duration.
- Kaggle CLI version.
- Operation classification.
- Redacted argument list and resolved working directory.
- Exit code and structured error category.
- Redacted, size-bounded stdout/stderr plus complete-content SHA-256 hashes.
- Artifact manifest entries with relative path, size, and SHA-256.

Audit records and downloads default to a user-selected output directory or an
ignored local state directory. Generated research data is never placed in the
skill source directory.

## Public Interface

The primary entry point is:

```text
python scripts/kaggle_research.py <command>
```

Commands:

- `doctor [--json]`: verify Python, Kaggle CLI version, writable audit/output
  locations, and authenticated access via a harmless account-scoped list
  request. It must not call `kaggle auth print-access-token`.
- `run [policy options] -- <kaggle arguments...>`: invoke any official Kaggle
  CLI command through classification, policy, redaction, timeout, and audit
  handling.
- `smoke-readonly [options]`: run the real read-only integration workflow and
  emit a verification report.

The Python boundary exposes:

```python
execute(request: CommandRequest) -> CommandResult
classify(arguments: Sequence[str]) -> OperationClass
write_audit(result: CommandResult, destination: Path) -> Path
```

The skill references provide reviewed recipes for datasets, competitions,
kernels, and models. Recipes use `run` so newly added official CLI options
remain reachable without expanding the wrapper for every flag.

## Authentication and Local Verification

Supported official mechanisms:

- `KAGGLE_API_TOKEN` environment variable.
- `kaggle auth login`.
- Standard Kaggle access-token file.
- Legacy `~/.kaggle/kaggle.json`, when the installed official CLI supports it.

For verification on the current workstation, the test command may load
`KAGGLE_API_TOKEN` from `D:\Download\Kaggle\.env` into the child process
environment. The value must never be echoed, written to a file in this
repository, included in a command argument, or captured in an audit record.
The skill and tests must not contain the absolute reference-workspace path.

## Error Model

Errors are normalized into stable categories:

- `prerequisite`: supported Python or Kaggle CLI unavailable.
- `authentication`: token missing, expired, or rejected.
- `policy`: operation not explicitly authorized.
- `path`: unsafe or out-of-root local path.
- `timeout`: child process exceeded the requested timeout.
- `transient`: retryable network/service failure on a safe operation.
- `command`: Kaggle CLI returned a non-zero exit code.
- `parse`: expected structured output or metadata was invalid.
- `artifact`: downloaded artifact violated size, path, or integrity checks.

Messages include actionable context but pass through the redactor before being
shown or persisted.

## Test Strategy

### TDD requirement

Every behavior-changing implementation step follows red-green-refactor:

1. Add one focused failing test.
2. Run it and confirm the intended failure.
3. Add the minimum implementation.
4. Run the focused test and then the relevant suite.
5. Refactor only while green.

### Offline unit and contract tests

Offline tests may use fake process adapters and temporary files because they
must deterministically exercise conditions that are unsafe or impractical to
produce against Kaggle:

- Exact argument-array construction on Windows and POSIX.
- Classification of all supported resource/action combinations.
- Write/delete/unknown policy gates.
- Dry-run behavior.
- Timeout, termination, retry, and non-retry rules.
- Exit-code and error normalization.
- Redaction of all credential and signed-URL forms.
- Path traversal, symlink/junction escape, and control-character rejection.
- Audit schema, truncation, hashing, and atomic writes.
- Artifact manifest hashing and size limits.
- CLI help and JSON output contracts.

Mocks and fakes in this lane do not count as proof that live Kaggle integration
works.

### Real read-only live tests

`test_live_readonly.py` is skipped unless an explicit environment flag enables
it and Kaggle credentials are available. When enabled it must use the official
Kaggle CLI, the real service, and real public data:

1. Verify the installed CLI is in the supported `>=2.2,<3` range.
2. Prove authenticated access with an account-scoped read-only listing.
3. Search real public datasets with a strict maximum size.
4. Select a returned public dataset meeting the configured size limit.
5. Retrieve its real file/metadata listing.
6. Download a small real artifact into a temporary directory.
7. Verify non-empty content, path containment, size limit, and SHA-256.
8. Run real read-only competition, kernel, and model listings.
9. Verify the audit report contains no token or signed URL.
10. Remove temporary downloaded data.

The test stores no Kaggle response fixture as a substitute for the live calls.
Assertions avoid fragile expectations about ranking, exact row counts, or
mutable titles.

### Optional remote-write tests

Remote-write tests are excluded from the default implementation and CI lane.
The runtime supports writes through policy-gated `run` commands, and unit tests
cover their construction and non-retry behavior. A future opt-in suite may
create and delete private disposable resources only with:

- A dedicated environment flag.
- An explicit owner namespace.
- A unique disposable prefix.
- Exact cleanup confirmation.
- A cleanup report.

## Repository and CI Verification

Before contribution handoff:

- Run the collection's offline tests.
- Run its Python compatibility compilation.
- Run the real read-only live test with the local token.
- Run the repository unit suite.
- Run catalog generation and freshness checks.
- Run `make check-fast` or the Windows-equivalent commands.
- Run the full repository gate when dependencies and the submodule are
  available.
- Inspect `git diff --check`, generated changes, and secret scans.

Any pre-existing baseline failure must be recorded separately and must not be
misrepresented as introduced or fixed by this contribution.

## Success Criteria

- Collection 72 is discoverable from the root router and generated catalog.
- A clean install can bootstrap/use the official Kaggle CLI without modifying
  root dependencies.
- All offline tests pass.
- The real read-only live test passes using the local Kaggle token and real
  public Kaggle data.
- Write/delete commands remain unavailable without explicit policy flags.
- No token, credential file, signed URL, downloaded dataset, or generated model
  is tracked by Git.
- Catalog, provenance, documentation, and quality gates remain internally
  consistent.
- The feature branch is ready to push to the contributor fork for an upstream
  pull request.

## Audit Sources

- Official Kaggle CLI repository and documentation:
  <https://github.com/Kaggle/kaggle-cli>
- Official authentication documentation:
  <https://github.com/Kaggle/kaggle-cli/blob/main/docs/README.md>
- Official kernel command documentation:
  <https://github.com/Kaggle/kaggle-cli/blob/main/docs/kernels.md>
- Official changelog:
  <https://github.com/Kaggle/kaggle-cli/blob/main/CHANGELOG.md>
- Local behavioral reference (not copied):
  `D:\Download\Kaggle`
- Repository contribution and quality-gate requirements:
  `CONTRIBUTING.md`, `Makefile`, `SKILL.md`, and
  `scripts/build-provenance.py`.

# Kaggle Research Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an independently installable, policy-gated, auditable Kaggle CLI integration with deterministic offline tests and a real read-only live verification lane.

**Architecture:** A first-party collection owns a small Python stdlib runtime. Pure command classification and security functions sit in front of a subprocess runner; the runner produces typed results consumed by redacted audit/artifact writers and a user-facing CLI. The official Kaggle CLI remains isolated from the AERS root environment.

**Tech Stack:** Python 3.9-compatible stdlib runtime/tests, official Kaggle CLI `>=2.2,<3` in a Python 3.11+ environment, `unittest`, existing AERS catalog/provenance builders and quality gates.

**Design:** `docs/superpowers/specs/2026-07-27-kaggle-research-design.md`

## Global Constraints

- Collection path is exactly `skills/72-kaggle-research/kaggle-research/`.
- Do not copy implementation code from `D:\Download\Kaggle`.
- Do not read `.env`, IDE configuration, or arbitrary credential files in shipped code.
- Do not add Kaggle to the root `requirements.txt`.
- Execute subprocesses with argument arrays and `shell=False`.
- Read-only/download operations may retry recognized transient failures; remote writes and deletes never retry.
- Remote writes require `--allow-write`; deletes additionally require `--allow-delete` and exact resource confirmation.
- The default live lane is real, read-only, opt-in, and must not substitute mocks or fixtures for Kaggle responses/data.
- No secret, signed URL, downloaded dataset, notebook output, or model artifact may be tracked by Git.
- Follow TDD for every behavior change and run fresh verification before each completion claim.

---

### Task 1: Collection scaffold, typed results, command policy, and redaction

**Files:**
- Create: `skills/72-kaggle-research/README.md`
- Create: `skills/72-kaggle-research/kaggle-research/scripts/kaggle_runtime/__init__.py`
- Create: `skills/72-kaggle-research/kaggle-research/scripts/kaggle_runtime/result.py`
- Create: `skills/72-kaggle-research/kaggle-research/scripts/kaggle_runtime/commands.py`
- Create: `skills/72-kaggle-research/kaggle-research/scripts/kaggle_runtime/security.py`
- Create: `skills/72-kaggle-research/kaggle-research/tests/__init__.py`
- Create: `skills/72-kaggle-research/kaggle-research/tests/_support.py`
- Test: `skills/72-kaggle-research/kaggle-research/tests/test_commands.py`
- Test: `skills/72-kaggle-research/kaggle-research/tests/test_security.py`

**Interfaces:**
- Produces: `OperationClass`, `CommandRequest`, `CommandResult`,
  `KaggleRuntimeError`, `classify(arguments)`, `authorize(request)`,
  `redact_text(text)`, and `resolve_output_path(root, candidate)`.
- Consumes: Python stdlib only.

- [ ] **Step 1: Write failing command-policy tests**

```python
class CommandPolicyTests(unittest.TestCase):
    def test_classifies_read_download_write_delete_and_unknown(self):
        cases = {
            ("datasets", "list", "-v"): OperationClass.READ,
            ("datasets", "download", "-d", "owner/data"): OperationClass.DOWNLOAD,
            ("kernels", "push", "-p", "kernel"): OperationClass.REMOTE_WRITE,
            ("datasets", "delete", "-d", "owner/data"): OperationClass.REMOTE_DELETE,
            ("forums", "list"): OperationClass.UNKNOWN,
        }
        for argv, expected in cases.items():
            with self.subTest(argv=argv):
                self.assertEqual(classify(argv), expected)

    def test_delete_requires_all_flags_and_exact_resource(self):
        request = CommandRequest(
            arguments=("datasets", "delete", "-d", "owner/data"),
            allow_write=True,
            allow_delete=True,
            confirm_resource="owner/other",
        )
        with self.assertRaises(KaggleRuntimeError) as ctx:
            authorize(request)
        self.assertEqual(ctx.exception.category, "policy")

    def test_print_access_token_is_always_rejected(self):
        request = CommandRequest(arguments=("auth", "print-access-token"))
        with self.assertRaises(KaggleRuntimeError):
            authorize(request)
```

- [ ] **Step 2: Run command-policy tests and verify RED**

Run:

```powershell
python -m unittest discover -s skills/72-kaggle-research/kaggle-research/tests -p "test_commands.py" -v
```

Expected: import failure because `kaggle_runtime.commands` does not exist.

- [ ] **Step 3: Implement typed results and command policy**

```python
class OperationClass(str, Enum):
    READ = "read"
    DOWNLOAD = "download"
    REMOTE_WRITE = "remote_write"
    REMOTE_DELETE = "remote_delete"
    UNKNOWN = "unknown"

@dataclass(frozen=True)
class CommandRequest:
    arguments: tuple[str, ...]
    cwd: Path | None = None
    output_root: Path | None = None
    timeout_seconds: float = 120.0
    allow_write: bool = False
    allow_delete: bool = False
    confirm_resource: str | None = None
    dry_run: bool = False

def classify(arguments: Sequence[str]) -> OperationClass:
    group, action = normalized_group_action(arguments)
    if (group, action) in DOWNLOAD_ACTIONS:
        return OperationClass.DOWNLOAD
    if action == "delete":
        return OperationClass.REMOTE_DELETE
    if (group, action) in WRITE_ACTIONS:
        return OperationClass.REMOTE_WRITE
    if (group, action) in READ_ACTIONS or group in {"--version", "config"}:
        return OperationClass.READ
    return OperationClass.UNKNOWN
```

`authorize()` must reject sensitive token-printing commands, require an output
root for downloads, gate writes/unknown commands, and extract the exact
resource reference for delete confirmation.

- [ ] **Step 4: Run command-policy tests and verify GREEN**

Run the Step 2 command.

Expected: all command-policy tests pass.

- [ ] **Step 5: Write failing redaction and path tests**

```python
class SecurityTests(unittest.TestCase):
    def test_redacts_tokens_headers_legacy_keys_and_signed_urls(self):
        raw = (
            "KAGGLE_API_TOKEN=secret Authorization: Bearer secret "
            "KAGGLE_KEY=legacy "
            "https://storage.example/file?X-Goog-Signature=abc&x=1"
        )
        redacted = redact_text(raw)
        for secret in ("secret", "legacy", "abc"):
            self.assertNotIn(secret, redacted)
        self.assertIn("[REDACTED]", redacted)

    def test_output_path_must_remain_inside_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(resolve_output_path(root, "nested/out"), root / "nested/out")
            with self.assertRaises(KaggleRuntimeError):
                resolve_output_path(root, "../escape")
```

- [ ] **Step 6: Run security tests and verify RED**

Run:

```powershell
python -m unittest discover -s skills/72-kaggle-research/kaggle-research/tests -p "test_security.py" -v
```

Expected: import or assertion failures for missing security behavior.

- [ ] **Step 7: Implement redaction and path validation**

Implement compiled patterns for bearer/API/legacy tokens and signed query
parameters. Resolve paths with `Path.resolve(strict=False)`, compare using
`os.path.commonpath`, reject control characters, and reject paths outside the
root. Keep the functions side-effect free.

- [ ] **Step 8: Run Task 1 tests**

Run:

```powershell
python -m unittest discover -s skills/72-kaggle-research/kaggle-research/tests -p "test_commands.py" -v
python -m unittest discover -s skills/72-kaggle-research/kaggle-research/tests -p "test_security.py" -v
```

Expected: all Task 1 tests pass.

- [ ] **Step 9: Commit Task 1**

```powershell
git add skills/72-kaggle-research
git commit -m "feat: add Kaggle command policy and security boundary"
```

---

### Task 2: Subprocess runner, retry rules, audit records, and artifact manifests

**Files:**
- Create: `skills/72-kaggle-research/kaggle-research/scripts/kaggle_runtime/runner.py`
- Create: `skills/72-kaggle-research/kaggle-research/scripts/kaggle_runtime/artifacts.py`
- Test: `skills/72-kaggle-research/kaggle-research/tests/test_runner.py`
- Test: `skills/72-kaggle-research/kaggle-research/tests/test_artifacts.py`

**Interfaces:**
- Consumes: Task 1 `CommandRequest`, `CommandResult`, policy and redaction.
- Produces: `KaggleRunner.execute(request) -> CommandResult`,
  `build_audit_record(result) -> dict`, `write_audit(result, path) -> Path`,
  and `build_artifact_manifest(root) -> list[dict]`.

- [ ] **Step 1: Write failing runner tests**

```python
class RunnerTests(unittest.TestCase):
    def test_uses_argument_array_shell_false_utf8_and_no_token_argument(self):
        adapter = RecordingProcessAdapter(returncode=0, stdout="ok")
        runner = KaggleRunner(
            executable=("python", "-m", "kaggle"),
            process_adapter=adapter,
        )
        result = runner.execute(CommandRequest(arguments=("datasets", "list")))
        self.assertEqual(adapter.command, ["python", "-m", "kaggle", "datasets", "list"])
        self.assertFalse(adapter.kwargs["shell"])
        self.assertEqual(adapter.kwargs["env"]["PYTHONUTF8"], "1")
        self.assertNotIn(os.environ.get("KAGGLE_API_TOKEN", "never"), " ".join(adapter.command))
        self.assertTrue(result.ok)

    def test_read_retries_transient_failure_but_write_does_not(self):
        read_adapter = SequencedProcessAdapter([TimeoutError(), Completed(0, "ok", "")])
        read_result = KaggleRunner(process_adapter=read_adapter, sleep=lambda _: None).execute(
            CommandRequest(arguments=("datasets", "list"))
        )
        self.assertTrue(read_result.ok)
        self.assertEqual(read_adapter.calls, 2)

        write_adapter = SequencedProcessAdapter([TimeoutError(), Completed(0, "ok", "")])
        with self.assertRaises(KaggleRuntimeError):
            KaggleRunner(process_adapter=write_adapter, sleep=lambda _: None).execute(
                CommandRequest(arguments=("kernels", "push", "-p", "x"), allow_write=True)
            )
        self.assertEqual(write_adapter.calls, 1)
```

- [ ] **Step 2: Run runner tests and verify RED**

Run:

```powershell
python -m unittest discover -s skills/72-kaggle-research/kaggle-research/tests -p "test_runner.py" -v
```

Expected: import failure because `runner.py` does not exist.

- [ ] **Step 3: Implement the runner**

Use an injectable process adapter around `subprocess.run` for deterministic
tests. Build the final command as `[*executable, *request.arguments]`, set
`capture_output=True`, `text=True`, `encoding="utf-8"`, `errors="replace"`,
`shell=False`, and the request timeout. Run policy checks before the adapter.
Return a dry-run result without invoking the adapter. Normalize timeout,
transient, command, and prerequisite failures.

- [ ] **Step 4: Run runner tests and verify GREEN**

Run the Step 2 command.

Expected: all runner tests pass.

- [ ] **Step 5: Write failing audit/artifact tests**

```python
class ArtifactTests(unittest.TestCase):
    def test_audit_is_redacted_bounded_and_atomic(self):
        result = CommandResult(
            arguments=("datasets", "list"),
            operation=OperationClass.READ,
            returncode=0,
            stdout="KAGGLE_API_TOKEN=secret\n" + "x" * 5000,
            stderr="",
            started_at="2026-07-27T00:00:00Z",
            finished_at="2026-07-27T00:00:01Z",
            duration_seconds=1.0,
        )
        record = build_audit_record(result, capture_limit=128)
        encoded = json.dumps(record)
        self.assertNotIn("secret", encoded)
        self.assertTrue(record["stdout"]["truncated"])
        self.assertRegex(record["stdout"]["sha256"], r"^[0-9a-f]{64}$")

    def test_manifest_hashes_files_and_rejects_escape(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "data.csv").write_bytes(b"a,b\n1,2\n")
            manifest = build_artifact_manifest(root, max_total_bytes=1024)
            self.assertEqual(manifest[0]["path"], "data.csv")
            self.assertEqual(manifest[0]["size"], 8)
```

- [ ] **Step 6: Run audit/artifact tests and verify RED**

Run:

```powershell
python -m unittest discover -s skills/72-kaggle-research/kaggle-research/tests -p "test_artifacts.py" -v
```

Expected: import or assertion failure for missing artifact implementation.

- [ ] **Step 7: Implement audit and artifact functions**

Use SHA-256 streaming reads, deterministic path ordering, relative POSIX paths,
bounded total bytes, and atomic JSON writes through a temporary sibling followed
by `Path.replace()`. Apply `redact_text()` before persistence.

- [ ] **Step 8: Run Task 2 tests**

Run:

```powershell
python -m unittest discover -s skills/72-kaggle-research/kaggle-research/tests -p "test_runner.py" -v
python -m unittest discover -s skills/72-kaggle-research/kaggle-research/tests -p "test_artifacts.py" -v
```

Expected: all Task 2 tests pass.

- [ ] **Step 9: Commit Task 2**

```powershell
git add skills/72-kaggle-research/kaggle-research/scripts/kaggle_runtime skills/72-kaggle-research/kaggle-research/tests
git commit -m "feat: add audited Kaggle subprocess runtime"
```

---

### Task 3: User-facing CLI, doctor, and real read-only smoke workflow

**Files:**
- Create: `skills/72-kaggle-research/kaggle-research/scripts/kaggle_research.py`
- Create: `skills/72-kaggle-research/kaggle-research/scripts/kaggle_runtime/smoke.py`
- Test: `skills/72-kaggle-research/kaggle-research/tests/test_cli.py`
- Test: `skills/72-kaggle-research/kaggle-research/tests/test_live_readonly.py`

**Interfaces:**
- Consumes: Tasks 1-2 runtime.
- Produces: commands `doctor`, `run`, and `smoke-readonly`; live verification
  report schema `aers.kaggle.live-smoke/v1`.

- [ ] **Step 1: Write failing CLI parser tests**

```python
class CliTests(unittest.TestCase):
    def test_run_requires_separator_arguments_and_preserves_order(self):
        ns = build_parser().parse_args([
            "run", "--dry-run", "--", "datasets", "list", "-s", "iris", "-v"
        ])
        request = request_from_namespace(ns)
        self.assertTrue(request.dry_run)
        self.assertEqual(request.arguments, ("datasets", "list", "-s", "iris", "-v"))

    def test_doctor_never_builds_print_access_token_command(self):
        commands = build_doctor_commands()
        flattened = [" ".join(command) for command in commands]
        self.assertFalse(any("print-access-token" in command for command in flattened))
        self.assertIn("datasets list -m", "\n".join(flattened))
```

- [ ] **Step 2: Run CLI tests and verify RED**

Run:

```powershell
python -m unittest discover -s skills/72-kaggle-research/kaggle-research/tests -p "test_cli.py" -v
```

Expected: import failure because the entry point does not exist.

- [ ] **Step 3: Implement CLI parsing and doctor**

Use `argparse`. Support:

```text
kaggle_research.py doctor [--json] [--executable PATH | --python PATH]
kaggle_research.py run [--dry-run] [--allow-write] [--allow-delete]
                       [--confirm-resource REF] [--output-root PATH]
                       [--audit PATH] [--timeout SECONDS]
                       [--executable PATH | --python PATH] -- <kaggle args>
kaggle_research.py smoke-readonly --output-root PATH --report PATH
                                  [--max-dataset-bytes N]
                                  [--executable PATH | --python PATH]
```

`--python PATH` resolves to `(PATH, "-m", "kaggle")`. `--executable PATH`
resolves to `(PATH,)`. The default uses `AERS_KAGGLE_PYTHON`,
`AERS_KAGGLE_EXECUTABLE`, or a `kaggle` executable found on `PATH`.

- [ ] **Step 4: Run CLI tests and verify GREEN**

Run the Step 2 command.

Expected: all CLI tests pass.

- [ ] **Step 5: Write failing smoke workflow contract tests**

```python
class SmokeContractTests(unittest.TestCase):
    def test_smoke_uses_real_command_shapes_and_download_limit(self):
        runner = RecordingRunner([
            ok_csv("ref,title,size\nowner/tiny,Tiny,100\n"),
            ok_csv("ref,title,size\nowner/tiny,Tiny,100\n"),
            ok_csv("ref,deadline\ncomp,2027-01-01\n"),
            ok_csv("ref,title\nowner/kernel,Kernel\n"),
            ok_csv("ref,title\nowner/model,Model\n"),
            ok_result("Downloaded to tiny.zip"),
        ])
        report = run_readonly_smoke(
            runner,
            output_root=self.temp_path,
            max_dataset_bytes=250_000,
        )
        self.assertEqual(report["schema_version"], "aers.kaggle.live-smoke/v1")
        self.assertTrue(report["checks"]["authenticated_account_list"])
        self.assertEqual(
            runner.requests[-1].operation,
            OperationClass.DOWNLOAD,
        )
```

This contract test uses a recording adapter only to validate orchestration.
It does not count as live proof.

- [ ] **Step 6: Implement smoke orchestration**

The real workflow must execute:

```text
--version
datasets list -m -v
datasets list -s iris --max-size <limit> -v
competitions list --page-size 1 -v
kernels list -m --page-size 1 -v
models list --page-size 1 -v
datasets download -d <returned-ref> -p <temp-output>
```

Parse CSV with `csv.DictReader`, accept case-insensitive size/ref column names,
select a returned dataset under the configured limit, verify at least one
non-empty downloaded file, hash the artifact, scan the report for secrets, and
clean the temporary download directory in `finally`.

- [ ] **Step 7: Add opt-in live unittest**

```python
@unittest.skipUnless(
    os.environ.get("AERS_KAGGLE_LIVE") == "1",
    "set AERS_KAGGLE_LIVE=1 for real Kaggle verification",
)
class LiveReadonlyTests(unittest.TestCase):
    def test_real_kaggle_service_and_public_data(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = run_readonly_smoke(
                KaggleRunner(executable=resolve_executable()),
                output_root=Path(tmp),
                max_dataset_bytes=250_000,
            )
        self.assertEqual(report["status"], "passed")
        self.assertTrue(all(report["checks"].values()))
```

- [ ] **Step 8: Run Task 3 offline tests**

Run:

```powershell
python -m unittest discover -s skills/72-kaggle-research/kaggle-research/tests -p "test_cli.py" -v
python -m unittest discover -s skills/72-kaggle-research/kaggle-research/tests -p "test_live_readonly.py" -v
```

Expected: CLI/contract tests pass and the real live class is skipped without
the opt-in flag.

- [ ] **Step 9: Commit Task 3**

```powershell
git add skills/72-kaggle-research/kaggle-research/scripts skills/72-kaggle-research/kaggle-research/tests
git commit -m "feat: add Kaggle CLI and live read-only smoke workflow"
```

---

### Task 4: Skill instructions and research workflow references

**Files:**
- Create: `skills/72-kaggle-research/kaggle-research/SKILL.md`
- Create: `skills/72-kaggle-research/kaggle-research/references/authentication.md`
- Create: `skills/72-kaggle-research/kaggle-research/references/datasets.md`
- Create: `skills/72-kaggle-research/kaggle-research/references/competitions.md`
- Create: `skills/72-kaggle-research/kaggle-research/references/kernels.md`
- Create: `skills/72-kaggle-research/kaggle-research/references/models.md`
- Create: `skills/72-kaggle-research/kaggle-research/references/testing-and-safety.md`
- Modify: `skills/72-kaggle-research/README.md`
- Test: `skills/72-kaggle-research/kaggle-research/tests/test_skill_contract.py`

**Interfaces:**
- Consumes: Task 3 CLI.
- Produces: discoverable `kaggle-research` skill with progressive disclosure
  and copy-pasteable commands that match the implemented CLI.

- [ ] **Step 1: Write failing skill-contract tests**

```python
class SkillContractTests(unittest.TestCase):
    def test_frontmatter_and_referenced_files_are_complete(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertIn("name: kaggle-research", text)
        self.assertIn("description:", text)
        for name in (
            "authentication.md", "datasets.md", "competitions.md",
            "kernels.md", "models.md", "testing-and-safety.md",
        ):
            self.assertTrue((REFERENCES / name).is_file(), name)
            self.assertIn(f"references/{name}", text)

    def test_documented_entrypoint_commands_exist(self):
        text = SKILL.read_text(encoding="utf-8")
        for command in ("doctor", "run", "smoke-readonly"):
            self.assertIn(command, text)
            self.assertIn(command, build_parser()._subparsers._group_actions[0].choices)
```

- [ ] **Step 2: Run skill-contract tests and verify RED**

Run:

```powershell
python -m unittest discover -s skills/72-kaggle-research/kaggle-research/tests -p "test_skill_contract.py" -v
```

Expected: missing `SKILL.md` and reference files.

- [ ] **Step 3: Write the skill and references**

`SKILL.md` must:

- Route Kaggle dataset discovery, competition data/submission, kernel
  execution/output, and model download requests.
- Run `doctor` first.
- Use `--dry-run` before write/delete operations.
- Require user authority for remote side effects.
- Never read or print credentials.
- Preserve audit/artifact outputs.
- Load only the reference matching the requested resource group.
- Distinguish normal offline tests from the real opt-in live lane.

Each reference provides exact current CLI recipes through
`kaggle_research.py run -- ...`, error interpretation, research provenance
notes, and resource-specific safety constraints.

- [ ] **Step 4: Run Task 4 tests**

Run the Step 2 command.

Expected: all skill-contract tests pass.

- [ ] **Step 5: Commit Task 4**

```powershell
git add skills/72-kaggle-research
git commit -m "docs: add Kaggle research skill workflows"
```

---

### Task 5: AERS catalog/provenance/quality-gate integration and full verification

**Files:**
- Modify: `scripts/build-provenance.py`
- Modify: `Makefile`
- Modify: `.pre-commit-config.yaml`
- Modify: `SKILL.md`
- Modify: `README.md`
- Modify: `README-en.md`
- Modify: `README-ja.md`
- Modify: `README-ko.md`
- Modify: `README-zh-CN.md`
- Modify: `README-zh-TW.md`
- Modify: `docs/CONTENT_ZH.md`
- Modify: `docs/en/04-data-acquisition-and-cleaning.md`
- Modify when regenerated content changes:
  `catalog/provenance.json`, `catalog/skill-audit.json`,
  `catalog/skills.json`, `catalog/skills-enriched.json`,
  `docs/LICENSE_AUDIT.md`, `docs/SKILL_AUDIT.md`,
  `docs/SKILL_CATALOG.md`, `docs/EVALS.md`,
  `docs/SKILL_HYGIENE.md`, `docs/SKILL_QUALITY.md`,
  `docs/TAXONOMY.md`, `tools/CATALOG.md`, `tools/README.md`,
  `docs/RIGOR_COVERAGE.md`, `docs/RELEASE_NOTES.md`,
  `docs/badges/rigor-coverage.json`, `docs/releases/index.html`, and
  `docs/BENCHMARK_SCOREBOARD.md`.
- Test: `tests/test_repo_tools.py`

**Interfaces:**
- Consumes: complete collection from Tasks 1-4.
- Produces: cataloged collection 72, first-party provenance, CI-discoverable
  tests, consistent repository statistics, and contributor-ready generated
  artifacts.

- [ ] **Step 1: Write failing provenance and test-discovery regressions**

```python
def test_kaggle_collection_has_pinned_first_party_provenance(self):
    record = build_provenance.OVERRIDES["72-kaggle-research"]
    self.assertEqual(
        record["source_url"],
        "https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills",
    )
    self.assertEqual(record["source_confidence"], "high")
    self.assertEqual(record["sync"], "manual")
```

Also assert the Makefile `test` and `python-compat` targets include the exact
collection test/script paths.

- [ ] **Step 2: Run focused repo test and verify RED**

Run:

```powershell
python -m unittest discover -s tests -p "test_repo_tools.py" -v
```

Expected: failure because provenance and Makefile integration are absent.

- [ ] **Step 3: Add provenance and quality-gate wiring**

Add an explicit `OVERRIDES["72-kaggle-research"]` record using the repository
default license, first-party origin, manual sync, and high source confidence.
Extend Makefile and pre-commit path filters so nested runtime/tests compile and
execute.

- [ ] **Step 4: Add router/index documentation**

Update root skill counts and route Kaggle data acquisition/execution requests
to `skills/72-kaggle-research/kaggle-research/`. Add collection 72 and the new
total counts to `README.md`, `README-en.md`, `README-ja.md`, `README-ko.md`,
`README-zh-TW.md`, and `docs/CONTENT_ZH.md`. Update the deprecated
`README-zh-CN.md` count-bearing lines and add the operational route to
`docs/en/04-data-acquisition-and-cleaning.md`. Do not manually edit generated
catalog files.

- [ ] **Step 5: Regenerate catalog artifacts**

Run these exact PowerShell commands:

```powershell
python scripts/build-provenance.py
python scripts/build-skill-audit.py
python scripts/build-catalog.py
python scripts/build-evals.py
python scripts/build-catalog-enrich.py
python scripts/build-tools-catalog.py
python scripts/build-coverage-map.py
python scripts/build-release-notes.py
python scripts/build-release-notes.py --html
python scripts/build-benchmark-scoreboard.py
```

- [ ] **Step 6: Run all offline collection and repository tests**

Run:

```powershell
python -m unittest discover -s skills/72-kaggle-research/kaggle-research/tests -p "test_*.py" -v
python -m unittest discover -s tests -p "test_*.py"
```

Record pass/fail counts and distinguish pre-existing failures.

- [ ] **Step 7: Run the real live read-only test**

Load `KAGGLE_API_TOKEN` from `D:\Download\Kaggle\.env` into the current process
without printing it, set:

```text
AERS_KAGGLE_LIVE=1
AERS_KAGGLE_PYTHON=D:\Download\Kaggle\.venv\Scripts\python.exe
```

Run:

```powershell
python -m unittest discover -s skills/72-kaggle-research/kaggle-research/tests -p "test_live_readonly.py" -v
```

Expected: real authenticated account listing, real public dataset discovery and
download, and real competition/kernel/model listing all pass; no secret appears
in output or the report.

- [ ] **Step 8: Run repository verification gates**

Run fresh:

```text
python scripts/validate-repo.py
python scripts/check-repo-hygiene.py
python scripts/validate-workflows.py
python scripts/check-readme-stats.py
python scripts/check-catalog-coverage.py
python scripts/check-plugin-source-location.py
python scripts/check-mirror-sync.py
python scripts/build-provenance.py --check
python scripts/build-skill-audit.py --check
python scripts/build-catalog.py --check
python scripts/build-evals.py --check
python scripts/build-catalog-enrich.py --check
python scripts/build-tools-catalog.py --check
python scripts/build-coverage-map.py --check
python scripts/build-release-notes.py --check
python scripts/build-release-notes.py --check --html
python scripts/build-benchmark-scoreboard.py --check
python -m py_compile scripts/*.py benchmark/*.py benchmark/lib/*.py eval-harness/*.py tests/*.py
git diff --check
git status --short
```

Before the full gate, run:

```powershell
git submodule status skills/69-Paper-WorkFlow
```

If its status begins with `-`, initialize the exact registered submodule:

```powershell
git submodule update --init --recursive skills/69-Paper-WorkFlow
```

Then rerun the full gate and report any remaining baseline failure without
concealing it.

- [ ] **Step 9: Review the complete diff**

Check:

- No copied project-specific Kaggle code or absolute local path appears in the
  shipped collection.
- No secret/token/signed URL is present.
- All changed generated artifacts correspond to builders.
- Public commands and reference documentation agree.
- Write/delete policies and tests match the approved design.

- [ ] **Step 10: Commit Task 5**

```powershell
git add .pre-commit-config.yaml Makefile SKILL.md scripts tests skills/72-kaggle-research catalog docs README.md README-en.md
git commit -m "feat: integrate Kaggle research collection into AERS"
```

- [ ] **Step 11: Final branch verification before push**

Run the full offline collection suite, real live read-only suite, repository
unit suite, generated freshness checks, secret scan, and `git diff --check`
against the exact branch tree. Report every actual command result. Push only
after the required user authorization under `AGENTS.md`.

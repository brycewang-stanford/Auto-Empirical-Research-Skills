---
name: kaggle-research
description: Use when a research task needs reproducible Kaggle discovery, metadata inspection, bounded public-data downloads, competition or kernel discovery, model discovery, or an explicitly approved Kaggle write/delete operation through the official CLI.
---

# Kaggle Research

Use the official Kaggle CLI through the policy-enforcing wrapper in this skill.
The wrapper records bounded, redacted audit data; confines downloads to an
approved directory; and blocks remote mutation unless the user explicitly
authorizes it.

## Required workflow

1. Confirm the requested Kaggle resource and whether the action is read,
   download, write, or delete. Do not broaden user authority.
2. Use an isolated Python 3.11+ environment with `kaggle>=2.2,<3`.
3. Configure Kaggle authentication outside commands and source files. Never
   read, print, echo, log, or commit credential values.
4. Run the non-mutating prerequisite check:

   ```bash
   python scripts/kaggle_research.py doctor --json
   ```

5. Run discovery commands before downloads or mutations. Keep every download
   under an explicitly chosen output root.
6. Preserve generated audit JSON and artifact hashes with the research outputs.
7. Report exact commands, resource references, timestamps, failures, and
   generated artifacts. Distinguish verified observations from assumptions.

## Safe command execution

Pass Kaggle arguments after `--` so their order is preserved:

```bash
python scripts/kaggle_research.py run --audit artifacts/audit.json -- datasets list -s iris -v
python scripts/kaggle_research.py run --output-root artifacts/kaggle -- datasets download -d owner/dataset
```

Preview any potentially mutating command first:

```bash
python scripts/kaggle_research.py run --dry-run --allow-write -- datasets create -p dataset-package
```

An actual remote write additionally requires explicit user authorization and
`--allow-write`. A delete additionally requires `--allow-delete` and
`--confirm-resource` matching the exact resource classified by the wrapper.
The runtime never retries writes or deletes.

## Real read-only verification

The live smoke workflow calls Kaggle's real service, inspects all supported
resource groups, downloads a small public dataset, and verifies its hash:

```bash
python scripts/kaggle_research.py smoke-readonly --output-root artifacts/kaggle-smoke --report artifacts/kaggle-smoke-report.json
```

The corresponding integration test is opt-in so normal unit tests do not
depend on network access:

```bash
AERS_KAGGLE_LIVE=1 python -m unittest discover -s tests -p "test_live_readonly.py" -v
```

Only run the live lane when credentials are already available in the process
environment. It must remain read/download-only.

## Reference routing

- Authentication and credential boundaries:
  [references/authentication.md](references/authentication.md)
- Dataset discovery and bounded downloads:
  [references/datasets.md](references/datasets.md)
- Competition discovery and approved submissions:
  [references/competitions.md](references/competitions.md)
- Kernel/notebook discovery and approved pushes:
  [references/kernels.md](references/kernels.md)
- Model discovery and approved instance operations:
  [references/models.md](references/models.md)
- Test lanes, safety policy, and audit artifacts:
  [references/testing-and-safety.md](references/testing-and-safety.md)

Read only the reference page required for the active task.

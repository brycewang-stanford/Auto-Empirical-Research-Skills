# Datasets

Discover before downloading:

```bash
python scripts/kaggle_research.py run -- datasets list -s "search terms" -v
python scripts/kaggle_research.py run -- datasets files -d owner/dataset -v
```

Record the selected dataset reference, visible metadata, selection criteria,
CLI version, and timestamp. Treat licenses, access rules, and dataset-card
limitations as research constraints.

All downloads require an output root:

```bash
python scripts/kaggle_research.py run --output-root artifacts/kaggle -- datasets download -d owner/dataset
```

The runtime resolves the path, rejects traversal outside it, and records file
size and SHA-256 evidence. Set study-specific size limits before acquiring
large data. Dataset create/version/delete operations are remote mutations and
require the explicit write/delete policy flags described in `SKILL.md`.

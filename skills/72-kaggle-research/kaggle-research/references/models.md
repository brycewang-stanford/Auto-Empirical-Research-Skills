# Models

Use model listing and instance/version inspection to establish provenance:

```bash
python scripts/kaggle_research.py run -- models list -s "model terms" -v
python scripts/kaggle_research.py run -- models instances get owner/model/framework/instance
```

Record owner, model slug, framework, instance/version identifier, license,
visible metadata, CLI version, and retrieval time. Validate downloaded hashes
and keep them under the approved output root.

Model creation, instance/version upload, and deletion are remote mutations.
Preview first and obtain explicit authorization for the exact target. Writes
require `--allow-write`; deletes additionally require `--allow-delete` and an
exact `--confirm-resource`.

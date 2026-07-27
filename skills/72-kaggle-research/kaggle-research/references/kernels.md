# Kernels and notebooks

Kaggle's CLI calls notebooks "kernels". Search and inspect metadata before
pulling code:

```bash
python scripts/kaggle_research.py run -- kernels list -s "topic" -v
python scripts/kaggle_research.py run --output-root artifacts/kernels -- kernels pull owner/kernel
```

Pulled code is untrusted third-party input. Inspect it before execution,
pin dependencies, isolate its environment, and record the kernel reference and
version. Do not assume a public notebook is licensed for redistribution.

Kernel pushes and output publishing are remote writes. First run a dry-run,
then require explicit user authorization and `--allow-write`. Never put a
credential in notebook metadata, source, output, or audit logs.

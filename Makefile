.PHONY: catalog validate paper-workflow-check check check-fast check-full quickstart audit hygiene clean external-links external-links-dry tools-links tools-links-dry evals eval-harness eval-smoke benchmark-lint benchmark benchmark-refresh test python-compat

# Newcomers: five-minute tour of what the repo is, what the catalog router
# routes to, and which entry point to open. Stdlib only; does not mutate the
# catalog or any vendored skill. Pair with: `make quickstart-markdown` to
# also emit docs/QUICKSTART_REPORT.md.
quickstart:
	python3 scripts/quickstart.py

quickstart-markdown:
	python3 scripts/quickstart.py --markdown

# Fast local gate — catalog + validate + python-compat + test. Use for the
# inner PR feedback loop; full `make check` adds the slow eval/benchmark
# lanes on top.
check-fast: validate python-compat test

# Full local gate — everything `make check` does. Use before tagging a release.
check-full: check

catalog:
	python3 scripts/build-provenance.py
	python3 scripts/build-skill-audit.py
	python3 scripts/build-catalog.py
	python3 scripts/build-evals.py
	python3 scripts/build-catalog-enrich.py
	python3 scripts/build-tools-catalog.py
	python3 scripts/build-coverage-map.py
	python3 scripts/build-release-notes.py
	python3 scripts/build-release-notes.py --html
	python3 scripts/build-benchmark-scoreboard.py

# Catalog/provenance/audit/eval freshness + repo link & frontmatter validation.
validate:
	python3 scripts/validate-repo.py
	python3 scripts/check-repo-hygiene.py
	python3 scripts/validate-workflows.py
	python3 scripts/check-ecosystem.py
	python3 scripts/check-readme-stats.py
	python3 scripts/check-catalog-coverage.py
	python3 scripts/check-plugin-source-location.py
	python3 scripts/check-mirror-sync.py
	$(MAKE) paper-workflow-check
	python3 scripts/build-provenance.py --check
	python3 scripts/build-skill-audit.py --check
	python3 scripts/build-catalog.py --check
	python3 scripts/build-evals.py --check
	python3 scripts/build-catalog-enrich.py --check
	python3 scripts/build-tools-catalog.py --check
	python3 scripts/build-coverage-map.py --check
	python3 scripts/build-release-notes.py --check
	python3 scripts/build-release-notes.py --check --html
	python3 scripts/build-benchmark-scoreboard.py --check

paper-workflow-check:
	@if [ ! -f skills/69-Paper-WorkFlow/validate_skill.py ]; then \
		echo "skills/69-Paper-WorkFlow is not checked out; run git submodule update --init --recursive" >&2; \
		exit 1; \
	fi
	cd skills/69-Paper-WorkFlow && python3 validate_skill.py

# Declarative flagship eval prompt matrix (docs/EVALS.md).
evals:
	python3 scripts/build-evals.py

# Lint executable eval-harness scenarios (CI gate; needs no candidate outputs).
# Distinct from `make evals` (the declarative flagship-evals prompt matrix).
eval-harness:
	python3 eval-harness/run_evals.py \
		--min-scenarios 24 --min-auto-checks 116 \
		--expect-categories causal-identification,reproducibility,citation-hygiene,runtime-safety,research-integrity,writing-compliance,writing-style

# Grade fixture candidates as a smoke test. The fixture set intentionally
# has nine outputs and includes one weak answer; fail on drift.
eval-smoke:
	python3 eval-harness/run_evals.py --grade eval-harness/candidates/_example \
		--expect-graded 9 --expect-fail-required statspai-weak-iv \
		--expect-graded-categories causal-identification,reproducibility,citation-hygiene,runtime-safety,research-integrity \
		--fail-on-orphans --fail-on-partial --no-write

benchmark-lint:
	python3 benchmark/check_benchmark.py --lint

# Reproducible numeric benchmark; fail on required and optional reference-gold drift.
benchmark:
	python3 benchmark/reference_pipeline.py --check
	python3 benchmark/check_benchmark.py --strict --fail-on-partial --fail-on-orphan-results

benchmark-refresh:
	python3 benchmark/reference_pipeline.py

# Stdlib unittest suite (no third-party deps required).
test:
	python3 -m unittest discover -s tests -p "test_*.py"
	python3 -m unittest discover -s skills/72-kaggle-research/kaggle-research/tests -p "test_*.py"

# Compile all repo-owned Python tooling with the active interpreter. In CI this
# runs on the Python 3.9/3.12 matrix and catches syntax drift in scripts that
# are not imported by the unit suite.
python-compat:
	python3 -m py_compile scripts/*.py benchmark/*.py benchmark/lib/*.py eval-harness/*.py tests/*.py
	python3 -m py_compile skills/72-kaggle-research/kaggle-research/scripts/*.py skills/72-kaggle-research/kaggle-research/scripts/kaggle_runtime/*.py skills/72-kaggle-research/kaggle-research/tests/*.py

# Full local gate: everything a PR should pass.
check: validate python-compat test eval-harness eval-smoke benchmark-lint benchmark

audit:
	python3 scripts/validate-repo.py --audit
	python3 scripts/check-repo-hygiene.py --audit-local

hygiene:
	python3 scripts/check-repo-hygiene.py --audit-local

clean:
	find . -path ./.git -prune -o -name .DS_Store -type f -exec rm -f {} +
	find . -path ./.git -prune -o -name __pycache__ -type d -prune -exec rm -rf {} +
	find . -path ./.git -prune -o \( -name '*.pyc' -o -name '*.pyo' \) -type f -exec rm -f {} +
	rm -rf .pytest_cache .ruff_cache .mypy_cache

external-links:
	python3 scripts/check-links.py

external-links-dry:
	python3 scripts/check-links.py --no-write

# Network-bound drift guard for the tools catalog (not part of `make validate`).
tools-links:
	python3 scripts/check-tools-links.py

tools-links-dry:
	python3 scripts/check-tools-links.py --no-write

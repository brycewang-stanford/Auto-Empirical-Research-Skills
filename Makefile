.PHONY: catalog validate check audit evals eval-harness eval-smoke benchmark test

catalog:
	python3 scripts/build-provenance.py
	python3 scripts/build-skill-audit.py
	python3 scripts/build-catalog.py
	python3 scripts/build-evals.py
	python3 scripts/build-catalog-enrich.py

# Catalog/provenance/audit/eval freshness + repo link & frontmatter validation.
validate:
	python3 scripts/validate-repo.py
	python3 scripts/validate-workflows.py
	python3 scripts/build-provenance.py --check
	python3 scripts/build-skill-audit.py --check
	python3 scripts/build-catalog.py --check
	python3 scripts/build-evals.py --check
	python3 scripts/build-catalog-enrich.py --check

# Declarative flagship eval prompt matrix (docs/EVALS.md).
evals:
	python3 scripts/build-evals.py

# Lint executable eval-harness scenarios (CI gate; needs no candidate outputs).
# Distinct from `make evals` (the declarative flagship-evals prompt matrix).
eval-harness:
	python3 eval-harness/run_evals.py \
		--min-scenarios 14 --min-auto-checks 66 \
		--expect-categories causal-identification,reproducibility,citation-hygiene,runtime-safety,research-integrity,writing-compliance,writing-style

# Grade fixture candidates as a smoke test. The fixture set intentionally
# has eight outputs and includes one weak answer; fail on drift.
eval-smoke:
	python3 eval-harness/run_evals.py --grade eval-harness/candidates/_example \
		--expect-graded 8 --expect-fail-required statspai-weak-iv \
		--expect-graded-categories causal-identification,reproducibility,citation-hygiene,runtime-safety,research-integrity \
		--fail-on-orphans --fail-on-partial

# Reproducible numeric benchmark; fail on required and optional reference-gold drift.
benchmark:
	python3 benchmark/reference_pipeline.py
	python3 benchmark/check_benchmark.py --strict --fail-on-partial --fail-on-orphan-results

# Stdlib unittest suite (no third-party deps required).
test:
	python3 -m unittest discover -s tests -p "test_*.py"

# Full local gate: everything a PR should pass.
check: validate test eval-harness eval-smoke benchmark

audit:
	python3 scripts/validate-repo.py --audit

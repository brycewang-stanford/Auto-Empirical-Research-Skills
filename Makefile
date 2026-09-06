.PHONY: catalog validate paper-workflow-check check check-fast check-full quickstart audit hygiene clean external-links external-links-dry tools-links tools-links-dry evals eval-harness eval-smoke benchmark-lint benchmark benchmark-refresh test python-compat setup doctor security-scan

# One-command local bootstrap. Almost every gate in this repo is stdlib-only,
# but `make validate` runs the Paper-WorkFlow demo gate, which really executes
# did_demo.ipynb and therefore needs the pinned scientific stack. Without it the
# gate reports "RIGOR.md is STALE" — a message that points at a regeneration
# command which cannot help. Build the venv once and the whole gate goes green.
#
#   make setup && source .venv/bin/activate && make check
setup:
	@# Layering `python3 -m venv` over a venv built by a *different* interpreter
	@# (uv, virtualenv, another Python) leaves a mixed tree that later dies with
	@# "No module named encodings" — a message that names nothing useful and
	@# appears well after the command that caused it. Refuse up front instead.
	@if [ -d .venv ]; then \
		have=$$(.venv/bin/python -c 'import sys; print("%d.%d" % sys.version_info[:2])' 2>/dev/null); \
		want=$$(python3 -c 'import sys; print("%d.%d" % sys.version_info[:2])'); \
		if [ -z "$$have" ]; then \
			echo "" >&2; \
			echo ".venv exists but its interpreter does not run." >&2; \
			echo "Remove it and re-run:    rm -rf .venv && make setup" >&2; \
			echo "" >&2; \
			exit 1; \
		elif [ "$$have" != "$$want" ]; then \
			echo "" >&2; \
			echo ".venv is Python $$have but 'python3' here is $$want." >&2; \
			echo "Building one over the other produces a venv that fails later with" >&2; \
			echo "'No module named encodings'. Pick one:" >&2; \
			echo "" >&2; \
			echo "    rm -rf .venv && make setup      # rebuild on $$want" >&2; \
			echo "    source .venv/bin/activate       # keep $$have as-is" >&2; \
			echo "" >&2; \
			exit 1; \
		fi; \
	fi
	python3 -m venv .venv
	.venv/bin/python -m pip install --upgrade pip
	.venv/bin/python -m pip install -r requirements.txt
	git submodule update --init --recursive
	@echo
	@echo "Bootstrap done. Next:  source .venv/bin/activate && make check"
	@echo "To score an agent against the benchmark:  .venv/bin/pip install -e ."

# Answer "why did the gate fail?" in one screen, with the fix for each row.
doctor:
	python3 scripts/doctor.py

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
	python3 scripts/build-external-scoreboard.py
	python3 scripts/quickstart.py --markdown >/dev/null

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
	python3 scripts/scan-collections.py --check
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
	python3 scripts/build-external-scoreboard.py --check
	python3 scripts/quickstart.py --check >/dev/null && echo 'docs/QUICKSTART_REPORT.md is current.'

paper-workflow-check:
	@if [ ! -f skills/69-Paper-WorkFlow/validate_skill.py ]; then \
		echo "skills/69-Paper-WorkFlow is not checked out; run git submodule update --init --recursive" >&2; \
		exit 1; \
	fi
	@python3 -c "import numpy, pandas, matplotlib, statsmodels" 2>/dev/null || { \
		echo "" >&2; \
		echo "This gate executes skills/69-Paper-WorkFlow/did_demo.ipynb for real, so it" >&2; \
		echo "needs the pinned scientific stack. Without it the checker reports RIGOR.md" >&2; \
		echo "as STALE, which is misleading. Bootstrap it with:" >&2; \
		echo "" >&2; \
		echo "    make setup && source .venv/bin/activate" >&2; \
		echo "" >&2; \
		echo "Run 'make doctor' for a full environment report." >&2; \
		exit 1; \
	}
	cd skills/69-Paper-WorkFlow && python3 validate_skill.py

# Declarative flagship eval prompt matrix (docs/EVALS.md).
evals:
	python3 scripts/build-evals.py

# Lint executable eval-harness scenarios (CI gate; needs no candidate outputs).
# --selftest additionally runs each scenario's rubric against a correct and a
# plausibly-wrong fixture answer and requires the verdicts to differ, so the
# scenario count measures scenarios that discriminate rather than scenarios
# that exist. Every `critical` scenario must ship a fixture pair.
# Distinct from `make evals` (the declarative flagship-evals prompt matrix).
eval-harness:
	python3 eval-harness/run_evals.py \
		--min-scenarios 30 --min-auto-checks 140 --min-fixtures 9 --selftest \
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
	python3 -m py_compile scripts/*.py benchmark/*.py benchmark/lib/*.py eval-harness/*.py tests/*.py aers_score/*.py
	# The end-to-end replication demos are repo-owned Python and self-gating
	# scripts; they belong on the compat matrix like everything else.
	python3 -m py_compile demo-notebooks/*.py demo-notebooks/*/*.py
	python3 -m py_compile skills/72-kaggle-research/kaggle-research/scripts/*.py skills/72-kaggle-research/kaggle-research/scripts/kaggle_runtime/*.py skills/72-kaggle-research/kaggle-research/tests/*.py
	# The de-AIGC provenance scrubber is first-party, stdlib-only Python 3.9+.
	python3 -m py_compile skills/48-de-AIGC-skills/scripts/*.py

# Full local gate: everything a PR should pass.
check: validate python-compat test eval-harness eval-smoke benchmark-lint benchmark

# Re-run the vendored-collection pattern scan and refresh catalog/security-scan.json.
# `make validate` only asserts the record is current; this is what updates it after
# a new collection lands or a pattern changes. New findings must be triaged by hand.
security-scan:
	python3 scripts/scan-collections.py

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

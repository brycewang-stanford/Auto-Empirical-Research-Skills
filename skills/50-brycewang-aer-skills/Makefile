.PHONY: preflight validate validate-strict skillopt-gate audit-skills audit-skills-gate verify-citations verify-citations-online smoke-examples install-codex install-claude scaffold-stata scaffold-r scaffold-python scaffold-skeleton

preflight:
	python3 scripts/validate_repo.py
	python3 scripts/run_skillopt_gate.py
	python3 scripts/skill_audit.py --selftest
	python3 scripts/verify_citations.py --selftest
	git diff --check
	git diff --cached --check

validate:
	python3 scripts/validate_repo.py

validate-strict:
	python3 scripts/validate_repo.py --require-optional-tools

skillopt-gate:
	python3 scripts/run_skillopt_gate.py

audit-skills:
	python3 scripts/skill_audit.py

audit-skills-gate:
	python3 scripts/skill_audit.py --gate 85 --substance-gate 8

verify-citations:
	python3 scripts/verify_citations.py --offline

verify-citations-online:
	python3 scripts/verify_citations.py --online

smoke-examples:
	python3 scripts/run_example_smoke.py

install-codex:
	python3 scripts/install_skills.py codex

install-claude:
	python3 scripts/install_skills.py claude

scaffold-stata:
	@test -n "$(DEST)" || (echo "Set DEST=/path/to/project"; exit 2)
	python3 scripts/scaffold_project.py stata "$(DEST)"

scaffold-r:
	@test -n "$(DEST)" || (echo "Set DEST=/path/to/project"; exit 2)
	python3 scripts/scaffold_project.py r "$(DEST)"

scaffold-python:
	@test -n "$(DEST)" || (echo "Set DEST=/path/to/project"; exit 2)
	python3 scripts/scaffold_project.py python "$(DEST)"

scaffold-skeleton:
	@test -n "$(DEST)" || (echo "Set DEST=/path/to/project"; exit 2)
	python3 scripts/scaffold_project.py skeleton "$(DEST)"

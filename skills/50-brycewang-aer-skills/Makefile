.PHONY: preflight validate validate-strict install-codex install-claude scaffold-stata scaffold-r scaffold-python scaffold-skeleton

preflight:
	python3 scripts/validate_repo.py
	git diff --check
	git diff --cached --check

validate:
	python3 scripts/validate_repo.py

validate-strict:
	python3 scripts/validate_repo.py --require-optional-tools

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

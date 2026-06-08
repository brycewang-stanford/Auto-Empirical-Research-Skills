# Installation — Codex

## Clone and Install

```bash
git clone https://github.com/brycewang-stanford/AER-Skills.git
cd AER-Skills
python3 scripts/install_skills.py codex
```

Restart Codex so new skills are picked up.

The installer copies the full skill directories. Keep the cloned repository
available if you want the `templates/` and `examples/` resources referenced by
the skills.

To preview the copy without writing files:

```bash
python3 scripts/install_skills.py codex --dry-run
```

To overwrite an existing install:

```bash
python3 scripts/install_skills.py codex --replace
```

Do not pass a repository source directory such as `.`, `skills/`, `docs/`, or
`templates/` to `--dest`; the installer refuses those destinations to avoid
copying generated skill folders into the source tree.

Manual fallback:

```bash
mkdir -p ~/.codex/skills
cp -R skills/aer-* ~/.codex/skills/
```

## Verify

Ask Codex:

```
List all skills starting with aer-.
```

You should see all nine.

## First Prompt

```
Use aer-workflow to decide which skill to apply to this paper next.
```

## Updating

```bash
cd AER-Skills
git pull
python3 scripts/install_skills.py codex --replace
```

## One-Line Install for Codex

If you'd rather have Codex install for you, paste this into Codex:

```
Install the AER-skills bundle into ~/.codex/skills/ by running
`python3 scripts/install_skills.py codex --replace` from the cloned
repository. When finished, list the installed aer-* directories and use
aer-workflow to tell me which skill I should apply next to my manuscript.
```

## Coexistence with Claude Code

Codex uses `~/.codex/skills/`; Claude Code uses `~/.claude/skills/`. The two install locations are independent and do not conflict.

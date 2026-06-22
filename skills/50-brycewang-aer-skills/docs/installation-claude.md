# Installation — Claude Code

## User-Scoped Install (recommended)

Install all skills under your user profile so they are available across projects:

```bash
git clone https://github.com/brycewang-stanford/AER-Skills.git
cd AER-Skills
python3 scripts/install_skills.py claude
```

Restart Claude Code (or run `/reload-plugins` if your install supports it).

The installer copies the full skill directories. Keep the cloned repository
available if you want the `templates/` and `examples/` resources referenced by
the skills.

To preview the copy without writing files:

```bash
python3 scripts/install_skills.py claude --dry-run
```

To overwrite an existing install:

```bash
python3 scripts/install_skills.py claude --replace
```

Do not pass a repository source directory such as `.`, `skills/`, `docs/`, or
`templates/` to `--dest`; the installer refuses those destinations to avoid
copying generated skill folders into the source tree. Project-scoped installs
should use `.claude/skills`.

Manual fallback:

```bash
mkdir -p ~/.claude/skills
cp -R skills/aer-* ~/.claude/skills/
```

## Project-Scoped Install

If you want the skills available only in the current project:

```bash
mkdir -p .claude/skills
python3 scripts/install_skills.py claude --dest .claude/skills
```

## Verify

In Claude Code, ask:

```
List available skills matching "aer-".
```

You should see all nine: `aer-workflow`, `aer-topic-selection`, `aer-identification`, `aer-robustness`, `aer-introduction`, `aer-tables-figures`, `aer-replication`, `aer-submission`, `aer-rebuttal`.

## First Prompt

```
Use aer-workflow to tell me which skill I should use next for this manuscript.
```

## Updating

Pull the repo and recopy:

```bash
cd AER-Skills
git pull
python3 scripts/install_skills.py claude --replace
```

## Subagent Wrapper (advanced)

If you prefer subagent-style invocation, create per-skill subagents under `~/.claude/agents/`:

```bash
mkdir -p ~/.claude/agents
for d in skills/aer-*; do
  name=$(basename "$d")
  cp "$d/SKILL.md" "$HOME/.claude/agents/$name.md"
done
```

Then invoke explicitly:

```
Use the aer-identification subagent to evaluate my DiD setup.
```

## Slash Command Variant

Slash commands live under `~/.claude/commands/` or `.claude/commands/`. Adapt each `SKILL.md` body as a command body if your workflow prefers explicit invocation.

Official Claude Code documentation:
- [Subagents](https://docs.anthropic.com/en/docs/claude-code/sub-agents)
- [Slash commands](https://docs.anthropic.com/en/docs/claude-code/slash-commands)
- [Skills](https://code.claude.com/docs/en/skills)

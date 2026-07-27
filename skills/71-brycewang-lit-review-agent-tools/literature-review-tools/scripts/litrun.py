#!/usr/bin/env python3
"""litrun — install and run open-source AI literature-review tools by id.

A thin, dependency-free launcher over recipes.json. Each tool gets its own
isolated virtualenv under ~/.lit-review-tools/envs/<id> so installs never
collide. API keys live in one shared ~/.lit-review-tools/.env.

Usage:
  litrun.py list [--category C] [--kind K]
  litrun.py info <id>
  litrun.py doctor
  litrun.py env [--set KEY=VALUE ...]     # show / edit the shared .env
  litrun.py install <id>
  litrun.py run <id> [-- <tool args...>]
  litrun.py mcp <id> [--storage PATH] [--client claude|cursor]
  litrun.py ui <id>                       # clone & launch a web UI (gpt-researcher, storm)
  litrun.py workflow list
  litrun.py workflow run <id> --input PATH [--question "..."] [--dry-run]

Design notes for the calling agent:
  - python-cli tools (mineru, marker, docling, paper-qa, asreview): install then
    run fully automatically.
  - python-lib tools (gpt-researcher, storm, scholarly, pyalex): install puts the
    library in a venv; `run` executes the recipe's example snippet.
  - mcp-server tools: `install` prepares them, `mcp` prints the client config block
    to register (they are servers, not one-shot CLIs).
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

BASE = Path(os.environ.get("LITRUN_HOME", Path.home() / ".lit-review-tools"))
ENVS = BASE / "envs"
WORKSPACE = BASE / "workspace"
ENV_FILE = BASE / ".env"
RECIPES = Path(__file__).resolve().parent.parent / "recipes" / "recipes.json"
WORKFLOWS = Path(__file__).resolve().parent.parent / "recipes" / "workflows.json"
SCRIPTS_DIR = Path(__file__).resolve().parent


def die(msg, code=1):
    print(f"litrun: {msg}", file=sys.stderr)
    sys.exit(code)


def load_recipes():
    if not RECIPES.exists():
        die(f"recipes.json not found at {RECIPES}")
    data = json.loads(RECIPES.read_text())
    return {t["id"]: t for t in data["tools"]}


def load_workflows():
    if not WORKFLOWS.exists():
        die(f"workflows.json not found at {WORKFLOWS}")
    data = json.loads(WORKFLOWS.read_text())
    return {w["id"]: w for w in data["workflows"]}


def get_tool(tools, tid):
    if tid not in tools:
        matches = [k for k in tools if tid in k]
        hint = f" Did you mean: {', '.join(matches)}?" if matches else ""
        die(f"unknown tool id '{tid}'.{hint} Run `litrun.py list`.")
    return tools[tid]


def have(cmd):
    return shutil.which(cmd) is not None


def read_env_file():
    env = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    return env


def write_env_file(env):
    BASE.mkdir(parents=True, exist_ok=True)
    lines = ["# litrun shared environment (API keys). One KEY=VALUE per line.\n"]
    for k, v in sorted(env.items()):
        lines.append(f"{k}={v}\n")
    ENV_FILE.write_text("".join(lines))


def merged_env():
    """OS environ overlaid with the shared .env (OS wins if already set)."""
    e = dict(os.environ)
    for k, v in read_env_file().items():
        e.setdefault(k, v)
    return e


def venv_dir(tid):
    return ENVS / tid


def venv_bin(tid, name):
    d = venv_dir(tid)
    binpath = d / ("Scripts" if os.name == "nt" else "bin")
    return binpath / name


def venv_python(tid):
    return venv_bin(tid, "python.exe" if os.name == "nt" else "python")


def ensure_venv(tid):
    d = venv_dir(tid)
    if venv_python(tid).exists():
        return
    d.parent.mkdir(parents=True, exist_ok=True)
    if have("uv"):
        run_cmd(["uv", "venv", str(d)])
    else:
        run_cmd([sys.executable, "-m", "venv", str(d)])


def pip_install(tid, packages):
    ensure_venv(tid)
    if have("uv"):
        cmd = ["uv", "pip", "install", "--python", str(venv_python(tid)), "-U", *packages]
    else:
        cmd = [str(venv_python(tid)), "-m", "pip", "install", "-U", *packages]
    run_cmd(cmd)


def run_cmd(cmd, env=None, check=True, cwd=None):
    printable = " ".join(str(c) for c in cmd)
    loc = f"(cd {cwd}) " if cwd else ""
    print(f"$ {loc}{printable}", file=sys.stderr)
    return subprocess.run(cmd, env=env, check=check, cwd=cwd)


def exec_cli(t, tool_args, env, cwd=None, dry=False):
    """Run a python-cli entrypoint or a bundled python-script. Shared by run & workflow."""
    if t["kind"] == "python-cli":
        probe = venv_bin(t["id"], t["entry"])
        cmd = [str(probe), *tool_args]
        display = t["entry"]
    elif t["kind"] == "python-script":
        probe = venv_python(t["id"])
        cmd = [str(probe), str(SCRIPTS_DIR / t["script"]), *tool_args]
        display = t["script"]
    else:
        die(f"'{t['id']}' is {t['kind']} — can't exec it directly.")
    if dry:
        loc = f"(cd {cwd}) " if cwd else ""
        print(f"DRY  $ {loc}{display} {' '.join(tool_args)}")
        return
    if not probe.exists():
        if t.get("pip"):
            print(f"{t['id']} not installed — installing first.")
            pip_install(t["id"], t["pip"])
        else:
            die(f"'{display}' not found; try: litrun.py install {t['id']}")
    run_cmd(cmd, env=env, check=False, cwd=cwd)


# ---------------------------------------------------------------- commands


def cmd_list(tools, args):
    rows = []
    for t in tools.values():
        if args.category and t["category"] != args.category:
            continue
        if args.kind and t["kind"] != args.kind:
            continue
        installed = "✓" if venv_python(t["id"]).exists() or t["kind"] == "mcp-server" and not t.get("pip") else " "
        rows.append((installed, t["id"], t["kind"], t["category"], t["name"]))
    if not rows:
        print("No tools match that filter.")
        return
    w_id = max(len(r[1]) for r in rows)
    w_kind = max(len(r[2]) for r in rows)
    w_cat = max(len(r[3]) for r in rows)
    print(f"  {'id'.ljust(w_id)}  {'kind'.ljust(w_kind)}  {'category'.ljust(w_cat)}  name")
    for inst, tid, kind, cat, name in rows:
        print(f"{inst} {tid.ljust(w_id)}  {kind.ljust(w_kind)}  {cat.ljust(w_cat)}  {name}")
    print("\n(✓ = installed / no install needed).  litrun.py info <id> for details.")


def cmd_info(tools, args):
    t = get_tool(tools, args.id)
    print(f"# {t['name']}  ({t['id']})")
    print(f"repo:     {t['repo']}")
    print(f"category: {t['category']}   kind: {t['kind']}")
    if t.get("pip"):
        print(f"install:  litrun.py install {t['id']}   (pip: {', '.join(t['pip'])})")
    if t.get("entry"):
        print(f"entry:    {t['entry']}")
    if t.get("script"):
        print(f"script:   {t['script']} (bundled; runs via this tool's venv)")
    if t.get("example"):
        print(f"example:  {t['example']}")
    req = t.get("env", [])
    opt = t.get("env_optional", [])
    if req or opt:
        env = merged_env()
        if req:
            print("required env:")
            for k in req:
                print(f"  {'✓' if env.get(k) else '✗'} {k}")
        if opt:
            print("optional env: " + ", ".join(opt))
    if t["kind"] == "mcp-server":
        print(f"mcp:      litrun.py mcp {t['id']}   (prints client config)")
    if t.get("ui"):
        print(f"ui:       litrun.py ui {t['id']}   (clone & launch web UI at {t['ui']['url']})")
    print(f"\nnotes: {t['notes']}")


def cmd_doctor(tools, args):
    print("== toolchain ==")
    for c in ("python3", "uv", "git", "pip"):
        print(f"  {'✓' if have(c) else '✗'} {c}")
    if not have("uv"):
        print("  (uv not found — falling back to python -m venv + pip. Install uv for speed.)")
    print(f"\n== base dir ==\n  {BASE}  ({'exists' if BASE.exists() else 'will be created'})")
    print(f"  env file: {ENV_FILE}  ({'present' if ENV_FILE.exists() else 'missing'})")
    print("\n== installed tools ==")
    any_installed = False
    for t in tools.values():
        if venv_python(t["id"]).exists():
            any_installed = True
            print(f"  ✓ {t['id']}")
    if not any_installed:
        print("  (none yet — litrun.py install <id>)")
    print("\n== API keys seen (OS env + .env) ==")
    env = merged_env()
    needed = sorted({k for t in tools.values() for k in t.get("env", []) + t.get("env_optional", [])})
    for k in needed:
        print(f"  {'✓' if env.get(k) else '✗'} {k}")
    missing = [k for k in needed if not env.get(k)]
    if missing:
        print(f"\nSet missing keys with:  litrun.py env --set {missing[0]}=...")


def cmd_env(tools, args):
    env = read_env_file()
    if args.set:
        for pair in args.set:
            if "=" not in pair:
                die(f"--set expects KEY=VALUE, got '{pair}'")
            k, v = pair.split("=", 1)
            env[k.strip()] = v.strip()
        write_env_file(env)
        print(f"Wrote {len(args.set)} key(s) to {ENV_FILE}")
    if not env:
        print(f"No keys set yet. Add with: litrun.py env --set OPENAI_API_KEY=sk-...\n(file: {ENV_FILE})")
        return
    print(f"# {ENV_FILE}")
    for k, v in sorted(env.items()):
        masked = (v[:4] + "…" + v[-2:]) if len(v) > 8 else "***"
        print(f"{k}={masked}")


def cmd_install(tools, args):
    t = get_tool(tools, args.id)
    if not t.get("pip"):
        if t["kind"] == "mcp-server":
            print(f"{t['id']} needs no install (runs via uvx). Register it with: litrun.py mcp {t['id']}")
            return
        die(f"{t['id']} has no pip recipe; see notes: {t['notes']}")
    print(f"Installing {t['name']} into {venv_dir(t['id'])} ...")
    pip_install(t["id"], t["pip"])
    print(f"\n✓ Installed {t['id']}.")
    if t.get("entry"):
        print(f"  Run it:  litrun.py run {t['id']} -- <args>   (e.g. {t.get('example','')})")
    if t["kind"] == "mcp-server":
        print(f"  Register it:  litrun.py mcp {t['id']}")
    req_missing = [k for k in t.get("env", []) if not merged_env().get(k)]
    if req_missing:
        print(f"  ⚠ Needs API keys: {', '.join(req_missing)} — set with litrun.py env --set KEY=...")


def cmd_run(tools, args):
    t = get_tool(tools, args.id)
    env = merged_env()
    missing = [k for k in t.get("env", []) if not env.get(k)]
    if missing:
        die(f"missing required env: {', '.join(missing)}. Set with `litrun.py env --set {missing[0]}=...`")

    if not venv_python(t["id"]).exists() and t.get("pip"):
        print(f"{t['id']} not installed yet — installing first.")
        pip_install(t["id"], t["pip"])

    if t["kind"] in ("python-cli", "python-script"):
        exec_cli(t, args.rest, env)
    elif t["kind"] == "python-lib":
        print(f"{t['name']} is a library, not a CLI. Running its example snippet:\n  {t.get('example','')}\n")
        # Execute the example via the tool's own venv python.
        snippet = t.get("example", "")
        if snippet.startswith("python -c ") or snippet.startswith('python -c'):
            code = snippet.split("-c", 1)[1].strip().strip('"')
            run_cmd([str(venv_python(t["id"])), "-c", code], env=env, check=False)
        else:
            print("No auto-runnable one-liner; see notes:")
            print(f"  {t['notes']}")
            if t.get("clone_for_ui"):
                print(f"  For the full UI, clone {t['repo']} and follow its README.")
    elif t["kind"] == "mcp-server":
        print(f"{t['id']} is an MCP server — it is launched by your MCP client, not run directly.")
        print(f"Register it with:  litrun.py mcp {t['id']}")
    else:
        die(f"don't know how to run kind '{t['kind']}'")


def cmd_workflow(tools, args):
    wfs = load_workflows()
    if args.wf_cmd == "list":
        for w in wfs.values():
            print(f"# {w['id']} — {w['name']}")
            print(f"    {w['description']}")
            print(f"    params: {', '.join(w['params'])}")
            chain = " → ".join(s["tool"] for s in w["steps"])
            print(f"    steps:  {chain}\n")
        print("Run:  litrun.py workflow run <id> --input <path> [--question \"...\"] [--dry-run]")
        return

    if not args.id:
        die("usage: litrun.py workflow run <id> [--input ...] [--question ...]")
    if args.id not in wfs:
        die(f"unknown workflow '{args.id}'. Run `litrun.py workflow list`.")
    w = wfs[args.id]

    # Collect params from flags.
    params = {}
    if args.input:
        params["input"] = args.input
    if args.question:
        params["question"] = args.question
    if args.query:
        params["query"] = args.query
    if args.max:
        params["max"] = str(args.max)
    for pair in (args.param or []):
        if "=" not in pair:
            die(f"--param expects KEY=VALUE, got '{pair}'")
        k, v = pair.split("=", 1)
        params[k] = v
    for k, v in w.get("defaults", {}).items():
        params.setdefault(k, v)
    workdir = WORKSPACE / "runs" / w["id"]
    params["workdir"] = str(workdir)

    missing = [p for p in w["params"] if p not in params]
    if missing:
        if args.dry_run:
            for p in missing:
                params[p] = f"<{p}>"
        else:
            die(f"workflow '{w['id']}' needs params: {', '.join(missing)}. "
                f"Provide with --input / --question / --param KEY=VALUE.")

    def sub(s):
        for k, v in params.items():
            s = s.replace("{" + k + "}", v)
        return s

    # Validate every step tool exists and is python-cli; gather required env.
    step_tools = []
    needed_env = set()
    for step in w["steps"]:
        t = get_tool(tools, step["tool"])
        if t["kind"] not in ("python-cli", "python-script"):
            die(f"workflow step tool '{t['id']}' is {t['kind']}; workflows chain python-cli / python-script tools only.")
        step_tools.append(t)
        needed_env.update(t.get("env", []))

    if not args.dry_run:
        env = merged_env()
        env_missing = [k for k in sorted(needed_env) if not env.get(k)]
        if env_missing:
            die(f"missing API keys for this workflow: {', '.join(env_missing)}. "
                f"Set with `litrun.py env --set {env_missing[0]}=...`")
        workdir.mkdir(parents=True, exist_ok=True)
    else:
        env = merged_env()

    print(f"{'DRY RUN — ' if args.dry_run else ''}workflow '{w['id']}' ({len(w['steps'])} step(s))")
    print(f"  workdir: {workdir}\n")
    for i, (step, t) in enumerate(zip(w["steps"], step_tools), 1):
        step_args = [sub(a) for a in step.get("args", [])]
        cwd = sub(step["cwd"]) if step.get("cwd") else None
        print(f"[step {i}/{len(w['steps'])}] {t['name']}")
        exec_cli(t, step_args, env, cwd=cwd, dry=args.dry_run)
        print()
    if args.dry_run:
        print("(dry run — nothing executed. Drop --dry-run to run for real.)")
    else:
        print(f"✓ workflow '{w['id']}' finished. Outputs: {w.get('outputs', workdir)}")


def cmd_ui(tools, args):
    t = get_tool(tools, args.id)
    ui = t.get("ui")
    if not ui:
        die(f"{t['id']} has no web UI. Runnable ids with a UI: gpt-researcher, storm.")

    env = merged_env()
    missing = [k for k in t.get("env", []) if not env.get(k)]
    if missing:
        print(f"⚠ {t['id']} UI needs API keys: {', '.join(missing)}.")
        if ui.get("write_env"):
            die(f"Set them first: litrun.py env --set {missing[0]}=...")
        else:
            print(f"  Enter them in the app once it opens (or: litrun.py env --set {missing[0]}=...).")

    clone_dir = WORKSPACE / t["id"]
    if not clone_dir.exists():
        WORKSPACE.mkdir(parents=True, exist_ok=True)
        run_cmd(["git", "clone", "--depth", "1", t["repo"], str(clone_dir)])
    else:
        print(f"(repo already cloned at {clone_dir})", file=sys.stderr)

    ensure_venv(t["id"])
    for req in ui.get("requirements", []):
        req_path = clone_dir / req
        if not req_path.exists():
            print(f"⚠ requirements file not found: {req_path} (upstream layout may have changed)", file=sys.stderr)
            continue
        if have("uv"):
            run_cmd(["uv", "pip", "install", "--python", str(venv_python(t["id"])), "-r", str(req_path)])
        else:
            run_cmd([str(venv_python(t["id"])), "-m", "pip", "install", "-r", str(req_path)])

    if ui.get("write_env"):
        keys = t.get("env", []) + t.get("env_optional", [])
        lines = [f"{k}={env[k]}\n" for k in keys if env.get(k)]
        if lines:
            (clone_dir / ".env").write_text("".join(lines))
            print(f"Wrote {len(lines)} key(s) to {clone_dir / '.env'}", file=sys.stderr)

    # Prepend the venv's bin to PATH so `streamlit`/`uvicorn`/`python` resolve to it.
    binpath = venv_dir(t["id"]) / ("Scripts" if os.name == "nt" else "bin")
    env["PATH"] = f"{binpath}{os.pathsep}{env.get('PATH', '')}"

    print(f"\n▶ Launching {t['name']} UI — open {ui['url']} once it's up. Ctrl-C to stop.")
    if ui.get("notes"):
        print(f"  {ui['notes']}")
    run_cmd(list(ui["run"]), env=env, check=False)


def cmd_mcp(tools, args):
    t = get_tool(tools, args.id)
    m = t.get("mcp")
    if not m:
        die(f"{t['id']} is not an MCP server.")
    launcher = m["launcher"]
    if launcher == "uvx":
        storage = args.storage or str(WORKSPACE / t["id"])
        arglist = [a.replace("{storage}", storage) for a in m["args_template"]]
        block = {"command": "uvx", "args": arglist}
    elif launcher == "venv-module":
        if not venv_python(t["id"]).exists():
            print(f"(note: {t['id']} not installed yet — run `litrun.py install {t['id']}` so this command resolves)")
        block = {"command": str(venv_python(t["id"])), "args": ["-m", m["module"]]}
    elif launcher == "venv-entry":
        if not venv_python(t["id"]).exists():
            print(f"(note: {t['id']} not installed yet — run `litrun.py install {t['id']}` so this command resolves)")
        block = {"command": str(venv_bin(t["id"], m["entry"]))}
    else:
        die(f"unknown mcp launcher '{launcher}'")
    if m.get("env"):
        block["env"] = dict(m["env"])
    config = {"mcpServers": {m["key"]: block}}

    print(f"# Add this to your MCP client config ({args.client}):")
    if args.client == "claude":
        print("#   Claude Code: ~/.claude.json  (or project .mcp.json)   |   Claude Desktop: claude_desktop_config.json")
    else:
        print("#   Cursor: ~/.cursor/mcp.json  (or .cursor/mcp.json in the project)")
    print(json.dumps(config, indent=2))
    if t.get("env_optional"):
        print(f"\n# Optional env you may want to fill into the 'env' block: {', '.join(t['env_optional'])}")
    print(f"\n# notes: {t['notes']}")


def main():
    p = argparse.ArgumentParser(prog="litrun.py", description="Install & run AI lit-review tools by id.")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_list = sub.add_parser("list", help="list runnable tools")
    p_list.add_argument("--category")
    p_list.add_argument("--kind")

    p_info = sub.add_parser("info", help="show a tool's install/run details")
    p_info.add_argument("id")

    sub.add_parser("doctor", help="check toolchain, installs, and API keys")

    p_env = sub.add_parser("env", help="show/edit the shared .env")
    p_env.add_argument("--set", nargs="*", help="KEY=VALUE pairs to write")

    p_inst = sub.add_parser("install", help="install a tool into an isolated venv")
    p_inst.add_argument("id")

    p_run = sub.add_parser("run", help="run a tool (installs if needed)")
    p_run.add_argument("id")
    p_run.add_argument("rest", nargs=argparse.REMAINDER,
                       help="args after `--` are passed to the tool")

    p_mcp = sub.add_parser("mcp", help="print the MCP client config for an MCP server")
    p_mcp.add_argument("id")
    p_mcp.add_argument("--storage", help="storage path (uvx servers)")
    p_mcp.add_argument("--client", choices=["claude", "cursor"], default="claude")

    p_ui = sub.add_parser("ui", help="clone & launch a tool's web UI (gpt-researcher, storm)")
    p_ui.add_argument("id")

    p_wf = sub.add_parser("workflow", help="run a named multi-step pipeline")
    p_wf.add_argument("wf_cmd", choices=["list", "run"])
    p_wf.add_argument("id", nargs="?")
    p_wf.add_argument("--input")
    p_wf.add_argument("--question")
    p_wf.add_argument("--query")
    p_wf.add_argument("--max")
    p_wf.add_argument("--param", action="append", help="extra KEY=VALUE params")
    p_wf.add_argument("--dry-run", action="store_true", dest="dry_run",
                      help="print resolved step commands without running")

    args = p.parse_args()
    # Strip a leading `--` separator from run's REMAINDER.
    if getattr(args, "rest", None) and args.rest and args.rest[0] == "--":
        args.rest = args.rest[1:]

    tools = load_recipes()
    dispatch = {
        "list": cmd_list, "info": cmd_info, "doctor": cmd_doctor, "env": cmd_env,
        "install": cmd_install, "run": cmd_run, "mcp": cmd_mcp, "ui": cmd_ui,
        "workflow": cmd_workflow,
    }
    dispatch[args.cmd](tools, args)


if __name__ == "__main__":
    main()

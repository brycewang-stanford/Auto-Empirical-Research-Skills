#!/usr/bin/env python3
"""Re-check that every tool in tools/tools.json still resolves.

The tools catalog records point-in-time snapshots (URL, license, last activity)
of fast-moving upstream repos. This script is the periodic drift guard: it pings
each tool's `url` (and `homepage`, as a non-fatal warning) and reports anything
that no longer resolves, so a maintainer pass can re-verify or retire it.

It is **network-bound** and therefore NOT part of `make validate` / the blocking
CI gate. It runs on a schedule (see `.github/workflows/check-tools-links.yml`)
and on demand via `make tools-links`. A primary-`url` failure exits non-zero; a
dead/again-rate-limited `homepage` is only a warning. Access-limited responses
(403/429) from GitHub etc. are treated as reachable, mirroring
`scripts/check-links.py`.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS_JSON = ROOT / "tools" / "tools.json"
DEFAULT_OUTPUT = ROOT / "catalog" / "tools-link-check.json"

REDIRECT_STATUSES = {301, 302, 303, 307, 308}
ACCESS_LIMITED_STATUSES = {403, 429}
USER_AGENT = "AERS-tools-link-check/1.0"


def _get(url: str, timeout: float, *, tolerated: int | None = None, error: str | None = None) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return {"url": url, "status": response.status, "ok": response.status < 400}
    except urllib.error.HTTPError as http_error:
        if http_error.code in ACCESS_LIMITED_STATUSES:
            return {"url": url, "status": http_error.code, "ok": True,
                    "warning": "Access-limited endpoint; treated as reachable."}
        if http_error.code in REDIRECT_STATUSES:
            return {"url": url, "status": http_error.code, "ok": True,
                    "warning": "Redirect endpoint; treated as reachable."}
        return {"url": url, "status": http_error.code, "ok": False, "error": str(http_error)}
    except Exception as get_error:  # noqa: BLE001 - report every failure type
        if tolerated in ACCESS_LIMITED_STATUSES:
            return {"url": url, "status": tolerated, "ok": True,
                    "warning": "Access-limited endpoint; treated as reachable."}
        if tolerated in REDIRECT_STATUSES:
            return {"url": url, "status": tolerated, "ok": True,
                    "warning": "Redirect endpoint; treated as reachable."}
        return {"url": url, "status": None, "ok": False, "error": error or str(get_error)}


def check_url(url: str, timeout: float) -> dict:
    """HEAD first (cheap), fall back to GET on redirect / access-limit / method errors."""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT}, method="HEAD")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return {"url": url, "status": response.status, "ok": response.status < 400}
    except urllib.error.HTTPError as error:
        if error.code in REDIRECT_STATUSES | ACCESS_LIMITED_STATUSES | {405, 400}:
            return _get(url, timeout, tolerated=error.code)
        return {"url": url, "status": error.code, "ok": False, "error": str(error)}
    except Exception as error:  # noqa: BLE001
        return _get(url, timeout, error=str(error))


def load_tools() -> list[dict]:
    payload = json.loads(TOOLS_JSON.read_text(encoding="utf-8"))
    return payload.get("tools", [])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=float, default=15.0)
    parser.add_argument("--max", type=int, default=0, help="debug limit; 0 checks all tools")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--skip-homepages", action="store_true", help="check only the primary url")
    parser.add_argument("--no-write", action="store_true", help="run without writing the JSON report")
    args = parser.parse_args(argv)

    tools = load_tools()
    if args.max:
        tools = tools[: args.max]

    # De-duplicate URLs; remember which tool ids reference each.
    primary: dict[str, list[str]] = {}
    homepages: dict[str, list[str]] = {}
    for tool in tools:
        url = (tool.get("url") or "").strip()
        if url:
            primary.setdefault(url, []).append(tool.get("id", "?"))
        hp = (tool.get("homepage") or "").strip()
        if hp and not args.skip_homepages:
            homepages.setdefault(hp, []).append(tool.get("id", "?"))

    primary_results, homepage_results = [], []
    total = len(primary) + len(homepages)
    index = 0
    for url, ids in sorted(primary.items()):
        index += 1
        result = check_url(url, args.timeout)
        result["tool_ids"] = ids
        primary_results.append(result)
        print(f"[{index}/{total}] url {url} -> {result.get('status')} {'ok' if result['ok'] else 'FAIL'}")
    for url, ids in sorted(homepages.items()):
        index += 1
        result = check_url(url, args.timeout)
        result["tool_ids"] = ids
        homepage_results.append(result)
        print(f"[{index}/{total}] homepage {url} -> {result.get('status')} {'ok' if result['ok'] else 'warn'}")

    failures = [r for r in primary_results if not r["ok"]]
    homepage_warnings = [r for r in homepage_results if not r["ok"]]
    payload = {
        "source": "tools/tools.json",
        "checked_tools": len(tools),
        "checked_primary_urls": len(primary_results),
        "checked_homepages": len(homepage_results),
        "failures": failures,
        "homepage_warnings": homepage_warnings,
        "results": primary_results + homepage_results,
    }
    if args.no_write:
        print("Tools link-check report write skipped (--no-write).")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if homepage_warnings:
        print(f"{len(homepage_warnings)} homepage link(s) unreachable (non-fatal).", file=sys.stderr)
    if failures:
        print(f"{len(failures)} tool primary url(s) failed:", file=sys.stderr)
        for failure in failures:
            print(f"  {failure['url']} ({', '.join(failure['tool_ids'])}): {failure.get('error') or failure.get('status')}", file=sys.stderr)
        return 1
    print(f"All {len(primary_results)} tool primary URLs reachable.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

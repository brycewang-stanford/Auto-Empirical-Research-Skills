#!/usr/bin/env python3
"""Check external links in AERS-maintained Markdown and HTML files."""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "catalog" / "external-link-check.json"
LINK_RE = re.compile(r"(?:href=[\"']|\]\()(https?://[^)\"' >]+)")
REDIRECT_STATUSES = {301, 302, 303, 307, 308}
ACCESS_LIMITED_STATUSES = {403, 429}


def maintained_docs() -> list[Path]:
    paths: list[Path] = []
    paths.extend(ROOT.glob("*.md"))
    if (ROOT / "docs").exists():
        paths.extend((ROOT / "docs").rglob("*.md"))
        paths.extend((ROOT / "docs").rglob("*.html"))
    return sorted(set(paths))


def is_in_fenced_code(text: str, offset: int) -> bool:
    in_fence = False
    for line in text[:offset].splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
    return in_fence


def normalize_url(raw_url: str) -> str:
    return raw_url.rstrip(".,")


def iter_links(paths: list[Path], *, include_code_fences: bool = False) -> dict[str, list[str]]:
    links: dict[str, list[str]] = {}
    for path in paths:
        text = path.read_text(encoding="utf-8", errors="replace")
        for match in LINK_RE.finditer(text):
            if (
                path.suffix.lower() == ".md"
                and not include_code_fences
                and is_in_fenced_code(text, match.start())
            ):
                continue
            url = normalize_url(match.group(1))
            file_path = path.relative_to(ROOT).as_posix()
            links.setdefault(url, [])
            if file_path not in links[url]:
                links[url].append(file_path)
    return links


def check_url(url: str, timeout: float) -> dict[str, object]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "AERS-link-check/1.0"},
        method="HEAD",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return {"url": url, "status": response.status, "ok": response.status < 400}
    except urllib.error.HTTPError as error:
        if error.code in REDIRECT_STATUSES | ACCESS_LIMITED_STATUSES | {405}:
            return retry_get(url, timeout, tolerated_status=error.code)
        return {"url": url, "status": error.code, "ok": False, "error": str(error)}
    except Exception as error:  # noqa: BLE001 - CLI should report every failure type.
        return retry_get(url, timeout, error=str(error))


def retry_get(url: str, timeout: float, tolerated_status: int | None = None, error: str | None = None) -> dict[str, object]:
    request = urllib.request.Request(url, headers={"User-Agent": "AERS-link-check/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return {"url": url, "status": response.status, "ok": response.status < 400}
    except urllib.error.HTTPError as http_error:
        if http_error.code in ACCESS_LIMITED_STATUSES:
            return {
                "url": url,
                "status": http_error.code,
                "ok": True,
                "warning": "Access-limited endpoint; treated as reachable.",
            }
        if http_error.code in REDIRECT_STATUSES:
            return {
                "url": url,
                "status": http_error.code,
                "ok": True,
                "warning": "Redirect endpoint; treated as reachable.",
            }
        return {"url": url, "status": http_error.code, "ok": False, "error": str(http_error)}
    except Exception as get_error:  # noqa: BLE001
        if tolerated_status in ACCESS_LIMITED_STATUSES:
            return {
                "url": url,
                "status": tolerated_status,
                "ok": True,
                "warning": "Access-limited endpoint; treated as reachable.",
            }
        if tolerated_status in REDIRECT_STATUSES:
            return {
                "url": url,
                "status": tolerated_status,
                "ok": True,
                "warning": "Redirect endpoint; treated as reachable.",
            }
        return {"url": url, "status": None, "ok": False, "error": error or str(get_error)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=float, default=12.0)
    parser.add_argument("--max-links", type=int, default=0, help="debug limit; 0 checks all links")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--include-code-fences",
        action="store_true",
        help="also check links shown inside Markdown fenced code blocks",
    )
    parser.add_argument(
        "--no-write",
        action="store_true",
        help="run checks without writing the JSON report",
    )
    args = parser.parse_args(argv)

    docs = maintained_docs()
    links = iter_links(docs, include_code_fences=args.include_code_fences)
    urls = sorted(links)
    if args.max_links:
        urls = urls[: args.max_links]

    results = []
    for index, url in enumerate(urls, start=1):
        result = check_url(url, args.timeout)
        result["files"] = links[url]
        results.append(result)
        print(f"[{index}/{len(urls)}] {url} -> {result.get('status')} {'ok' if result['ok'] else 'FAIL'}")

    payload = {
        "checked_files": [path.relative_to(ROOT).as_posix() for path in docs],
        "checked_links": len(results),
        "failures": [result for result in results if not result["ok"]],
        "results": results,
    }
    if args.no_write:
        print("Link-check report write skipped (--no-write).")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if payload["failures"]:
        print(f"{len(payload['failures'])} external link(s) failed.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

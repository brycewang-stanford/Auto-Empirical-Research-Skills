#!/usr/bin/env python3
"""fetch_arxiv — search arXiv and download PDFs into a folder.

A small bundled tool (uses the `arxiv` PyPI package) so litrun workflows can do a
real retrieval step: topic -> download PDFs -> feed a downstream QA tool. No API
key required.

Usage:
  fetch_arxiv.py --query "retrieval augmented generation" --max 10 --outdir ./papers
  fetch_arxiv.py --query "cat:cs.CL AND graph neural network" --sort date --max 5 --outdir ./p
"""
import argparse
import json
import re
import sys

try:
    import arxiv
    import requests  # arxiv depends on requests, so it's always present in this env
except ImportError as e:
    sys.exit(f"fetch_arxiv: missing dependency ({e}). Reinstall with: litrun.py install arxiv-fetch")

from pathlib import Path

_UA = {"User-Agent": "litrun-fetch-arxiv/1.0 (+https://github.com/brycewang-stanford/lit-review-agent-tools)"}


def safe_name(s, maxlen=80):
    s = re.sub(r"[^\w\- ]+", "", s).strip().replace(" ", "_")
    return s[:maxlen] or "paper"


def download_pdf(url, dest):
    """Download a PDF via requests — independent of the arxiv package's own
    download API, which changes across major versions (4.0 dropped it)."""
    with requests.get(url, headers=_UA, stream=True, timeout=60, allow_redirects=True) as resp:
        resp.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in resp.iter_content(chunk_size=1 << 15):
                if chunk:
                    f.write(chunk)


def main():
    p = argparse.ArgumentParser(prog="fetch_arxiv.py")
    p.add_argument("--query", required=True, help="arXiv search query (supports cat:, AND/OR, etc.)")
    p.add_argument("--max", type=int, default=10, help="max papers to download (default 10)")
    p.add_argument("--outdir", required=True, help="directory to download PDFs into")
    p.add_argument("--sort", choices=["relevance", "date"], default="relevance")
    args = p.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    sort = (arxiv.SortCriterion.Relevance if args.sort == "relevance"
            else arxiv.SortCriterion.SubmittedDate)
    # Polite client: built-in delay + retries so we don't trip arXiv's rate limit (HTTP 429).
    client = arxiv.Client(page_size=min(args.max, 100), delay_seconds=3.0, num_retries=3)
    search = arxiv.Search(query=args.query, max_results=args.max, sort_by=sort)

    manifest = []
    n = 0
    print(f"fetch_arxiv: searching arXiv for {args.query!r} (max {args.max}, sort={args.sort})",
          file=sys.stderr)
    try:
        results = list(client.results(search))
    except Exception as e:  # network / API / rate-limit errors
        hint = " (arXiv rate limit — wait a minute and retry)" if "429" in str(e) else ""
        sys.exit(f"fetch_arxiv: search failed: {e}{hint}")

    for r in results:
        aid = r.get_short_id()
        title = getattr(r, "title", aid)
        pdf_url = getattr(r, "pdf_url", None) or f"https://arxiv.org/pdf/{aid}"
        fname = f"{aid}_{safe_name(title)}.pdf"
        try:
            download_pdf(pdf_url, outdir / fname)
            n += 1
            print(f"  ✓ {aid}  {title[:70]}", file=sys.stderr)
        except Exception as e:
            print(f"  ✗ {aid}  download failed: {e}", file=sys.stderr)
            continue
        manifest.append({
            "arxiv_id": aid,
            "title": title,
            "authors": [getattr(a, "name", str(a)) for a in getattr(r, "authors", [])],
            "published": str(getattr(r, "published", "")),
            "pdf": fname,
            "url": getattr(r, "entry_id", pdf_url),
        })

    (outdir / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    print(f"fetch_arxiv: downloaded {n}/{len(results)} PDF(s) to {outdir} "
          f"(manifest.json written).", file=sys.stderr)
    if n == 0:
        sys.exit("fetch_arxiv: no PDFs downloaded.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Fail if catalog/skills.json disagrees with the SKILL.md frontmatter on disk."""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
cat = json.loads((ROOT / "catalog" / "skills.json").read_text())
on_disk = {}
for p in sorted((ROOT / "skills").glob("*/SKILL.md")):
    fm = re.search(r"^---\n(.*?)\n---", p.read_text(), flags=re.S).group(1)
    name = re.search(r"^name:\s*(.+)$", fm, flags=re.M).group(1).strip()
    on_disk[name] = p.parent.name
cat_names = {s["name"]: s["path"] for s in cat["skills"]}
bad = False
for n, d in on_disk.items():
    if n not in cat_names:
        print(f"missing from catalog: {n} ({d})"); bad = True
    elif cat_names[n] != f"skills/{d}":
        print(f"path mismatch for {n}: catalog={cat_names[n]} disk=skills/{d}"); bad = True
for n in cat_names:
    if n not in on_disk:
        print(f"in catalog but not on disk: {n}"); bad = True
if cat["n_skills"] != len(on_disk):
    print(f"n_skills={cat['n_skills']} but {len(on_disk)} on disk"); bad = True
print("catalog OK" if not bad else "catalog INCONSISTENT")
sys.exit(1 if bad else 0)

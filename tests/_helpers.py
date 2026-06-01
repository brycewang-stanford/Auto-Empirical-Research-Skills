"""Shared helpers for the AERS test suite (stdlib unittest, no third-party deps).

Several repo scripts have hyphenated filenames (build-catalog.py) that cannot be
imported with a normal ``import`` statement, so we load them by path.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(rel_path: str, name: str | None = None):
    """Load a module from a repo-relative path, even if hyphenated."""
    path = ROOT / rel_path
    mod_name = name or path.stem.replace("-", "_")
    # Make the module's own ``lib/`` importable for sibling imports.
    sys.path.insert(0, str(path.parent / "lib"))
    sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location(mod_name, path)
    assert spec and spec.loader, f"cannot load {path}"
    module = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = module
    spec.loader.exec_module(module)
    return module

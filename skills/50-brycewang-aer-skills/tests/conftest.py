"""Shared pytest setup for the AER-Skills tooling test suite.

The repository's quality tooling lives in ``scripts/`` and the shared demo
helper lives in ``examples/``. Those modules import each other by bare module
name (e.g. ``import validate_repo``), so both directories are inserted into
``sys.path`` before test modules are collected.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]

for _directory in (REPO_ROOT / "scripts", REPO_ROOT / "examples"):
    _path = str(_directory)
    if _path not in sys.path:
        sys.path.insert(0, _path)


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "slow: marks tests that are noticeably slower than the rest"
    )


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return REPO_ROOT

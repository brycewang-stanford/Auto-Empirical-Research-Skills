#!/usr/bin/env python3
"""Thin shim: `python scripts/phack_cli.py ...` == `phack ...` after `pip install -e .`."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from phack.cli import main

if __name__ == "__main__":
    main()

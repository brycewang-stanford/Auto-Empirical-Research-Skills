from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

import _support  # noqa: F401
from kaggle_research import resolve_executable
from kaggle_runtime.runner import KaggleRunner
from kaggle_runtime.smoke import run_readonly_smoke


@unittest.skipUnless(
    os.environ.get("AERS_KAGGLE_LIVE") == "1",
    "set AERS_KAGGLE_LIVE=1 for real Kaggle verification",
)
class LiveReadonlyTests(unittest.TestCase):
    def test_real_kaggle_service_and_public_data(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = run_readonly_smoke(
                KaggleRunner(executable=resolve_executable()),
                output_root=Path(tmp),
                max_dataset_bytes=250_000,
            )
        self.assertEqual(report["status"], "passed")
        self.assertTrue(all(report["checks"].values()))
        self.assertGreaterEqual(len(report["artifacts"]), 1)


if __name__ == "__main__":
    unittest.main()

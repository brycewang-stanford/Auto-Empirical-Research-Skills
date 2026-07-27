from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import _support  # noqa: F401
from kaggle_research import (
    build_doctor_commands,
    build_parser,
    request_from_namespace,
    resolve_executable,
)


class CliParserTests(unittest.TestCase):
    def test_run_preserves_kaggle_argument_order_after_separator(self):
        namespace = build_parser().parse_args(
            [
                "run",
                "--dry-run",
                "--output-root",
                "output",
                "--",
                "datasets",
                "list",
                "-s",
                "iris",
                "-v",
            ]
        )
        request = request_from_namespace(namespace)
        self.assertTrue(request.dry_run)
        self.assertEqual(
            request.arguments,
            ("datasets", "list", "-s", "iris", "-v"),
        )
        self.assertEqual(request.output_root, Path("output"))

    def test_run_policy_options_map_to_request(self):
        namespace = build_parser().parse_args(
            [
                "run",
                "--allow-write",
                "--allow-delete",
                "--confirm-resource",
                "owner/data",
                "--timeout",
                "9",
                "--",
                "datasets",
                "delete",
                "-d",
                "owner/data",
            ]
        )
        request = request_from_namespace(namespace)
        self.assertTrue(request.allow_write)
        self.assertTrue(request.allow_delete)
        self.assertEqual(request.confirm_resource, "owner/data")
        self.assertEqual(request.timeout_seconds, 9.0)

    def test_run_rejects_missing_kaggle_arguments(self):
        namespace = build_parser().parse_args(["run", "--dry-run"])
        with self.assertRaises(ValueError):
            request_from_namespace(namespace)


class ExecutableResolutionTests(unittest.TestCase):
    def test_explicit_python_uses_module_entrypoint(self):
        self.assertEqual(
            resolve_executable(python=Path("python311")),
            ("python311", "-m", "kaggle"),
        )

    def test_explicit_executable_is_used_directly(self):
        self.assertEqual(
            resolve_executable(executable=Path("kaggle.exe")),
            ("kaggle.exe",),
        )

    def test_environment_python_is_supported(self):
        with patch.dict(
            os.environ,
            {"AERS_KAGGLE_PYTHON": "D:/Python311/python.exe"},
            clear=False,
        ):
            self.assertEqual(
                resolve_executable(),
                ("D:/Python311/python.exe", "-m", "kaggle"),
            )

    def test_python_and_executable_are_mutually_exclusive(self):
        with self.assertRaises(ValueError):
            resolve_executable(
                python=Path("python"),
                executable=Path("kaggle"),
            )


class DoctorContractTests(unittest.TestCase):
    def test_doctor_never_prints_access_token(self):
        commands = build_doctor_commands()
        flattened = [" ".join(command) for command in commands]
        self.assertFalse(
            any("print-access-token" in command for command in flattened)
        )
        self.assertIn("datasets list -m -v", "\n".join(flattened))
        self.assertIn("--version", flattened)


if __name__ == "__main__":
    unittest.main()

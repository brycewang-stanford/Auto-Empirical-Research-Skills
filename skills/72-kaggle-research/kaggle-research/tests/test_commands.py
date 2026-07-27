from __future__ import annotations

import unittest
from pathlib import Path

import _support  # noqa: F401
from kaggle_runtime.commands import authorize, classify
from kaggle_runtime.result import (
    CommandRequest,
    KaggleRuntimeError,
    OperationClass,
)


class CommandClassificationTests(unittest.TestCase):
    def test_classifies_read_download_write_delete_and_unknown(self):
        cases = {
            ("datasets", "list", "-v"): OperationClass.READ,
            ("competitions", "submissions", "-c", "house-prices"): OperationClass.READ,
            ("kernels", "status", "owner/kernel"): OperationClass.READ,
            ("models", "list", "--page-size", "1"): OperationClass.READ,
            ("datasets", "download", "-d", "owner/data"): OperationClass.DOWNLOAD,
            ("kernels", "output", "owner/kernel"): OperationClass.DOWNLOAD,
            ("kernels", "push", "-p", "kernel"): OperationClass.REMOTE_WRITE,
            ("competitions", "submit", "-c", "comp"): OperationClass.REMOTE_WRITE,
            ("datasets", "delete", "-d", "owner/data"): OperationClass.REMOTE_DELETE,
            ("forums", "list"): OperationClass.UNKNOWN,
        }
        for argv, expected in cases.items():
            with self.subTest(argv=argv):
                self.assertEqual(classify(argv), expected)

    def test_version_is_read_only(self):
        self.assertEqual(classify(("--version",)), OperationClass.READ)

    def test_empty_arguments_are_unknown(self):
        self.assertEqual(classify(()), OperationClass.UNKNOWN)


class CommandAuthorizationTests(unittest.TestCase):
    def test_read_is_allowed_without_flags(self):
        request = CommandRequest(arguments=("datasets", "list"))
        self.assertEqual(authorize(request), OperationClass.READ)

    def test_download_requires_output_root(self):
        request = CommandRequest(
            arguments=("datasets", "download", "-d", "owner/data")
        )
        with self.assertRaises(KaggleRuntimeError) as ctx:
            authorize(request)
        self.assertEqual(ctx.exception.category, "policy")

        allowed = CommandRequest(
            arguments=("datasets", "download", "-d", "owner/data"),
            output_root=Path("output"),
        )
        self.assertEqual(authorize(allowed), OperationClass.DOWNLOAD)

    def test_write_and_unknown_require_allow_write(self):
        for argv in (
            ("kernels", "push", "-p", "kernel"),
            ("forums", "list"),
        ):
            with self.subTest(argv=argv):
                with self.assertRaises(KaggleRuntimeError):
                    authorize(CommandRequest(arguments=argv))
                request = CommandRequest(arguments=argv, allow_write=True)
                self.assertIn(
                    authorize(request),
                    (OperationClass.REMOTE_WRITE, OperationClass.UNKNOWN),
                )

    def test_delete_requires_all_flags_and_exact_resource(self):
        base = {
            "arguments": ("datasets", "delete", "-d", "owner/data"),
            "allow_write": True,
            "allow_delete": True,
        }
        for confirmation in (None, "owner/other"):
            with self.subTest(confirmation=confirmation):
                request = CommandRequest(
                    **base,
                    confirm_resource=confirmation,
                )
                with self.assertRaises(KaggleRuntimeError) as ctx:
                    authorize(request)
                self.assertEqual(ctx.exception.category, "policy")

        request = CommandRequest(**base, confirm_resource="owner/data")
        self.assertEqual(authorize(request), OperationClass.REMOTE_DELETE)

    def test_print_access_token_is_always_rejected(self):
        for allow_write in (False, True):
            request = CommandRequest(
                arguments=("auth", "print-access-token"),
                allow_write=allow_write,
            )
            with self.assertRaises(KaggleRuntimeError) as ctx:
                authorize(request)
            self.assertEqual(ctx.exception.category, "policy")

    def test_control_characters_are_rejected(self):
        request = CommandRequest(arguments=("datasets", "list\nwhoami"))
        with self.assertRaises(KaggleRuntimeError) as ctx:
            authorize(request)
        self.assertEqual(ctx.exception.category, "policy")


if __name__ == "__main__":
    unittest.main()

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

    def test_official_group_and_model_aliases_keep_the_same_policy(self):
        cases = {
            ("c", "list"): OperationClass.READ,
            ("d", "download", "-d", "owner/data"): OperationClass.DOWNLOAD,
            ("k", "delete", "owner/kernel"): OperationClass.REMOTE_DELETE,
            (
                "m",
                "i",
                "delete",
                "owner/model/framework/instance",
            ): OperationClass.REMOTE_DELETE,
            (
                "m",
                "i",
                "v",
                "delete",
                "owner/model/framework/instance/1",
            ): OperationClass.REMOTE_DELETE,
        }
        for arguments, expected in cases.items():
            with self.subTest(arguments=arguments):
                self.assertEqual(classify(arguments), expected)

    def test_nested_model_and_metadata_downloads_are_confined(self):
        downloads = (
            ("datasets", "metadata", "owner/data"),
            ("competitions", "replay", "123"),
            ("competitions", "logs", "123", "0"),
            ("models", "get", "owner/model", "-p", "metadata"),
            (
                "models",
                "instances",
                "get",
                "owner/model/framework/instance",
                "-p",
                "metadata",
            ),
            (
                "models",
                "instances",
                "versions",
                "download",
                "owner/model/framework/instance/1",
            ),
        )
        for arguments in downloads:
            with self.subTest(arguments=arguments):
                self.assertEqual(
                    classify(arguments),
                    OperationClass.DOWNLOAD,
                )

        self.assertEqual(
            classify(("models", "get", "owner/model")),
            OperationClass.READ,
        )
        self.assertEqual(
            classify(
                (
                    "competitions",
                    "leaderboard",
                    "competition",
                    "--show",
                )
            ),
            OperationClass.READ,
        )
        self.assertEqual(
            classify(
                (
                    "competitions",
                    "leaderboard",
                    "competition",
                    "--download",
                )
            ),
            OperationClass.DOWNLOAD,
        )

    def test_nested_read_commands_do_not_require_write_authority(self):
        reads = (
            ("competitions", "team-submissions", "123"),
            ("competitions", "topics", "list", "competition"),
            ("datasets", "topics", "list", "owner/data"),
            ("kernels", "logs", "owner/kernel"),
            ("models", "topics", "list", "owner/model"),
            (
                "models",
                "instances",
                "versions",
                "files",
                "owner/model/framework/instance/1",
            ),
        )
        for arguments in reads:
            with self.subTest(arguments=arguments):
                self.assertEqual(classify(arguments), OperationClass.READ)

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

    def test_nested_model_delete_requires_delete_authority_and_exact_target(self):
        arguments = (
            "m",
            "i",
            "v",
            "delete",
            "owner/model/framework/instance/1",
        )
        with self.assertRaisesRegex(RuntimeError, "--allow-delete"):
            authorize(
                CommandRequest(
                    arguments=arguments,
                    allow_write=True,
                )
            )
        with self.assertRaisesRegex(RuntimeError, "exactly match"):
            authorize(
                CommandRequest(
                    arguments=arguments,
                    allow_write=True,
                    allow_delete=True,
                    confirm_resource="wrong/resource",
                )
            )
        self.assertEqual(
            authorize(
                CommandRequest(
                    arguments=arguments,
                    allow_write=True,
                    allow_delete=True,
                    confirm_resource=(
                        "owner/model/framework/instance/1"
                    ),
                )
            ),
            OperationClass.REMOTE_DELETE,
        )

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

    def test_inline_credentials_are_rejected_before_process_start(self):
        for argv in (
            ("datasets", "list", "--token", "secret"),
            ("datasets", "list", "--token=secret"),
            (
                "datasets",
                "list",
                "--header",
                "Authorization: Bearer secret",
            ),
        ):
            with self.subTest(argv=argv):
                with self.assertRaises(KaggleRuntimeError) as ctx:
                    authorize(CommandRequest(arguments=argv))
                self.assertEqual(ctx.exception.category, "policy")


if __name__ == "__main__":
    unittest.main()

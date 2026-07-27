from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import _support  # noqa: F401
from kaggle_runtime.result import CommandResult, OperationClass
from kaggle_runtime.smoke import run_readonly_smoke


def result(
    stdout="",
    *,
    returncode=0,
    stderr="",
    operation=OperationClass.READ,
):
    return CommandResult(
        arguments=("placeholder",),
        operation=operation,
        returncode=returncode,
        stdout=stdout,
        stderr=stderr,
        started_at="2026-07-27T00:00:00Z",
        finished_at="2026-07-27T00:00:01Z",
        duration_seconds=1.0,
        error_category=None if returncode == 0 else "command",
    )


class RecordingRunner:
    def __init__(self, outcomes):
        self.outcomes = list(outcomes)
        self.requests = []

    def execute(self, request):
        self.requests.append(request)
        outcome = self.outcomes.pop(0)
        if request.arguments[:2] == ("datasets", "download"):
            Path(request.output_root, "dataset.zip").write_bytes(b"real-bytes")
        return outcome


class SmokeWorkflowContractTests(unittest.TestCase):
    def test_smoke_runs_all_real_command_shapes_and_hashes_download(self):
        runner = RecordingRunner(
            [
                result("Kaggle CLI 2.2.2\n"),
                result("ref,title,size\nowner/private,Private,10\n"),
                result("ref,title,size\nowner/tiny,Tiny,100\n"),
                result("ref,deadline\ncomp,2027-01-01\n"),
                result("ref,title\nowner/kernel,Kernel\n"),
                result("ref,title\nowner/model,Model\n"),
                result(
                    "Downloaded",
                    operation=OperationClass.DOWNLOAD,
                ),
            ]
        )
        with tempfile.TemporaryDirectory() as tmp:
            report = run_readonly_smoke(
                runner,
                output_root=Path(tmp),
                max_dataset_bytes=250_000,
            )

        self.assertEqual(
            report["schema_version"],
            "aers.kaggle.live-smoke/v1",
        )
        self.assertEqual(report["status"], "passed")
        self.assertTrue(all(report["checks"].values()))
        commands = [request.arguments for request in runner.requests]
        self.assertEqual(commands[0], ("--version",))
        self.assertEqual(
            commands[1],
            ("datasets", "list", "-m", "-v"),
        )
        self.assertIn(
            ("competitions", "list", "--page-size", "1", "-v"),
            commands,
        )
        self.assertIn(
            ("kernels", "list", "-m", "--page-size", "1", "-v"),
            commands,
        )
        self.assertIn(
            ("models", "list", "--page-size", "1", "-v"),
            commands,
        )
        self.assertEqual(
            runner.requests[-1].arguments[:4],
            ("datasets", "download", "-d", "owner/tiny"),
        )
        self.assertTrue(report["artifacts"][0]["sha256"])

    def test_report_redacts_signed_urls_and_tokens(self):
        runner = RecordingRunner(
            [
                result("Kaggle CLI 2.2.2\n"),
                result("ref,title,size\nowner/private,Private,10\n"),
                result("ref,title,size\nowner/tiny,Tiny,100\n"),
                result("ref,deadline\ncomp,2027-01-01\n"),
                result("ref,title\nowner/kernel,Kernel\n"),
                result("ref,title\nowner/model,Model\n"),
                result(
                    "KAGGLE_API_TOKEN=secret "
                    "https://example.test/x?X-Goog-Signature=signed",
                    operation=OperationClass.DOWNLOAD,
                ),
            ]
        )
        with tempfile.TemporaryDirectory() as tmp:
            report = run_readonly_smoke(
                runner,
                output_root=Path(tmp),
                max_dataset_bytes=250_000,
            )
        encoded = str(report)
        self.assertNotIn("secret", encoded)
        self.assertNotIn("signed", encoded)

    def test_unsupported_cli_version_fails(self):
        runner = RecordingRunner([result("Kaggle CLI 1.7.4\n")])
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(RuntimeError, "unsupported"):
                run_readonly_smoke(
                    runner,
                    output_root=Path(tmp),
                    max_dataset_bytes=250_000,
                )


if __name__ == "__main__":
    unittest.main()

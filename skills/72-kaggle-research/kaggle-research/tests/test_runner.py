from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from dataclasses import dataclass
from pathlib import Path
from unittest.mock import patch

import _support  # noqa: F401
from kaggle_runtime.result import CommandRequest, KaggleRuntimeError
from kaggle_runtime.runner import KaggleRunner


@dataclass
class Completed:
    returncode: int = 0
    stdout: str = ""
    stderr: str = ""


class RecordingAdapter:
    def __init__(self, outcomes):
        self.outcomes = list(outcomes)
        self.calls = []

    def __call__(self, command, **kwargs):
        self.calls.append((list(command), kwargs))
        outcome = self.outcomes.pop(0)
        if isinstance(outcome, BaseException):
            raise outcome
        return outcome


class RunnerInvocationTests(unittest.TestCase):
    def test_uses_argument_array_shell_false_utf8_and_no_token_argument(self):
        adapter = RecordingAdapter([Completed(stdout="ok")])
        runner = KaggleRunner(
            executable=("python", "-m", "kaggle"),
            process_adapter=adapter,
        )
        with patch.dict(os.environ, {"KAGGLE_API_TOKEN": "process-secret"}):
            result = runner.execute(
                CommandRequest(arguments=("datasets", "list"))
            )

        command, kwargs = adapter.calls[0]
        self.assertEqual(
            command,
            ["python", "-m", "kaggle", "datasets", "list"],
        )
        self.assertFalse(kwargs["shell"])
        self.assertTrue(kwargs["capture_output"])
        self.assertEqual(kwargs["encoding"], "utf-8")
        self.assertEqual(kwargs["errors"], "replace")
        self.assertEqual(kwargs["env"]["PYTHONUTF8"], "1")
        self.assertEqual(kwargs["env"]["PYTHONIOENCODING"], "utf-8")
        self.assertNotIn("process-secret", " ".join(command))
        self.assertTrue(result.ok)

    def test_dry_run_does_not_start_process(self):
        adapter = RecordingAdapter([])
        result = KaggleRunner(process_adapter=adapter).execute(
            CommandRequest(
                arguments=("kernels", "push", "-p", "kernel"),
                allow_write=True,
                dry_run=True,
            )
        )
        self.assertEqual(adapter.calls, [])
        self.assertTrue(result.ok)
        self.assertTrue(result.dry_run)

    def test_download_dry_run_does_not_create_output_directory(self):
        adapter = RecordingAdapter([])
        with tempfile.TemporaryDirectory() as tmp:
            output_root = Path(tmp) / "not-created"
            result = KaggleRunner(process_adapter=adapter).execute(
                CommandRequest(
                    arguments=(
                        "datasets",
                        "download",
                        "-d",
                        "owner/data",
                    ),
                    output_root=output_root,
                    dry_run=True,
                )
            )
            self.assertFalse(output_root.exists())
        self.assertTrue(result.dry_run)
        self.assertEqual(adapter.calls, [])

    def test_cwd_and_timeout_are_forwarded(self):
        adapter = RecordingAdapter([Completed()])
        runner = KaggleRunner(process_adapter=adapter)
        runner.execute(
            CommandRequest(
                arguments=("datasets", "list"),
                cwd=Path("workspace"),
                timeout_seconds=7.5,
            )
        )
        _, kwargs = adapter.calls[0]
        self.assertEqual(kwargs["cwd"], Path("workspace"))
        self.assertEqual(kwargs["timeout"], 7.5)

    def test_download_path_is_normalized_under_output_root(self):
        adapter = RecordingAdapter([Completed()])
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            KaggleRunner(process_adapter=adapter).execute(
                CommandRequest(
                    arguments=(
                        "datasets",
                        "download",
                        "-d",
                        "owner/data",
                        "-p",
                        "nested",
                    ),
                    output_root=root,
                )
            )
        command, _ = adapter.calls[0]
        path_index = command.index("-p") + 1
        self.assertEqual(Path(command[path_index]), root / "nested")


class RunnerRetryTests(unittest.TestCase):
    def test_read_retries_timeout_then_succeeds(self):
        adapter = RecordingAdapter(
            [
                subprocess.TimeoutExpired(["kaggle"], 1),
                Completed(stdout="ok"),
            ]
        )
        sleeps = []
        result = KaggleRunner(
            process_adapter=adapter,
            sleep=sleeps.append,
        ).execute(
            CommandRequest(
                arguments=("datasets", "list"),
                retries=1,
            )
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.attempts, 2)
        self.assertEqual(len(adapter.calls), 2)
        self.assertEqual(sleeps, [1.0])

    def test_write_does_not_retry_timeout(self):
        adapter = RecordingAdapter(
            [
                subprocess.TimeoutExpired(["kaggle"], 1),
                Completed(stdout="must not run"),
            ]
        )
        runner = KaggleRunner(process_adapter=adapter, sleep=lambda _: None)
        with self.assertRaises(KaggleRuntimeError) as ctx:
            runner.execute(
                CommandRequest(
                    arguments=("kernels", "push", "-p", "kernel"),
                    allow_write=True,
                    retries=3,
                )
            )
        self.assertEqual(ctx.exception.category, "timeout")
        self.assertEqual(len(adapter.calls), 1)

    def test_read_retries_transient_cli_result(self):
        adapter = RecordingAdapter(
            [
                Completed(returncode=1, stderr="503 temporarily unavailable"),
                Completed(stdout="ok"),
            ]
        )
        result = KaggleRunner(
            process_adapter=adapter,
            sleep=lambda _: None,
        ).execute(
            CommandRequest(arguments=("models", "list"), retries=1)
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.attempts, 2)

    def test_write_nonzero_result_is_not_retried(self):
        adapter = RecordingAdapter(
            [
                Completed(returncode=1, stderr="503 temporarily unavailable"),
                Completed(stdout="must not run"),
            ]
        )
        result = KaggleRunner(
            process_adapter=adapter,
            sleep=lambda _: None,
        ).execute(
            CommandRequest(
                arguments=("kernels", "push", "-p", "kernel"),
                allow_write=True,
                retries=3,
            )
        )
        self.assertFalse(result.ok)
        self.assertEqual(result.error_category, "transient")
        self.assertEqual(result.attempts, 1)
        self.assertEqual(len(adapter.calls), 1)

    def test_missing_executable_is_prerequisite_error(self):
        adapter = RecordingAdapter([FileNotFoundError("missing")])
        with self.assertRaises(KaggleRuntimeError) as ctx:
            KaggleRunner(process_adapter=adapter).execute(
                CommandRequest(arguments=("datasets", "list"))
            )
        self.assertEqual(ctx.exception.category, "prerequisite")


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Optional, Sequence

from .commands import authorize
from .result import (
    CommandRequest,
    CommandResult,
    KaggleRuntimeError,
    OperationClass,
)
from .security import resolve_output_path


_TRANSIENT = re.compile(
    r"(?i)(timed?\s*out|temporar(?:y|ily)\s+unavailable|"
    r"connection\s+(?:reset|aborted)|too\s+many\s+requests|"
    r"rate\s+limit|\b50[234]\b)"
)
_AUTHENTICATION = re.compile(
    r"(?i)(unauthori[sz]ed|forbidden|authentication|credentials?|"
    r"access\s+token|\b40[13]\b)"
)
_PATH_FLAGS = frozenset({"-p", "--path"})


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _error_category(returncode: int, stdout: str, stderr: str) -> Optional[str]:
    if returncode == 0:
        return None
    combined = f"{stdout}\n{stderr}"
    if _AUTHENTICATION.search(combined):
        return "authentication"
    if _TRANSIENT.search(combined):
        return "transient"
    return "command"


def _is_retryable(operation: OperationClass) -> bool:
    return operation in {OperationClass.READ, OperationClass.DOWNLOAD}


def _prepare_download_arguments(
    arguments: Sequence[str],
    output_root: Path,
) -> tuple[str, ...]:
    resolved_root = Path(output_root).resolve(strict=False)
    prepared = list(arguments)

    for index, argument in enumerate(prepared):
        if argument in _PATH_FLAGS:
            if index + 1 >= len(prepared):
                raise KaggleRuntimeError(
                    "path",
                    f"{argument} requires an output path",
                )
            prepared[index + 1] = str(
                resolve_output_path(resolved_root, prepared[index + 1])
            )
            return tuple(prepared)
        for flag in _PATH_FLAGS:
            prefix = f"{flag}="
            if argument.startswith(prefix):
                value = argument[len(prefix) :]
                prepared[index] = (
                    prefix + str(resolve_output_path(resolved_root, value))
                )
                return tuple(prepared)

    prepared.extend(["-p", str(resolved_root)])
    return tuple(prepared)


class KaggleRunner:
    def __init__(
        self,
        *,
        executable: Optional[Sequence[str]] = None,
        process_adapter: Optional[Callable[..., object]] = None,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        self.executable = tuple(
            executable or (sys.executable, "-m", "kaggle")
        )
        if not self.executable:
            raise ValueError("executable cannot be empty")
        self.process_adapter = process_adapter or subprocess.run
        self.sleep = sleep

    def execute(self, request: CommandRequest) -> CommandResult:
        operation = authorize(request)
        arguments = request.arguments
        if operation is OperationClass.DOWNLOAD:
            if request.output_root is None:
                raise KaggleRuntimeError(
                    "policy",
                    "Download operations require an output root",
                )
            arguments = _prepare_download_arguments(
                arguments,
                request.output_root,
            )

        started_at = _utc_now()
        started = time.monotonic()
        if request.dry_run:
            finished_at = _utc_now()
            return CommandResult(
                arguments=arguments,
                operation=operation,
                returncode=0,
                stdout="",
                stderr="",
                started_at=started_at,
                finished_at=finished_at,
                duration_seconds=max(0.0, time.monotonic() - started),
                executable=self.executable,
                attempts=0,
                dry_run=True,
            )

        command = [*self.executable, *arguments]
        if operation is OperationClass.DOWNLOAD and request.output_root is not None:
            Path(request.output_root).resolve(strict=False).mkdir(
                parents=True,
                exist_ok=True,
            )
        environment = dict(os.environ)
        environment["PYTHONUTF8"] = "1"
        environment["PYTHONIOENCODING"] = "utf-8"
        retryable = _is_retryable(operation)
        maximum_attempts = 1 + (request.retries if retryable else 0)

        for attempt in range(1, maximum_attempts + 1):
            try:
                completed = self.process_adapter(
                    command,
                    capture_output=True,
                    text=True,
                    shell=False,
                    check=False,
                    cwd=request.cwd,
                    timeout=request.timeout_seconds,
                    env=environment,
                    encoding="utf-8",
                    errors="replace",
                )
            except subprocess.TimeoutExpired as exc:
                if retryable and attempt < maximum_attempts:
                    self.sleep(float(2 ** (attempt - 1)))
                    continue
                raise KaggleRuntimeError(
                    "timeout",
                    (
                        "Kaggle command exceeded "
                        f"{request.timeout_seconds:g} seconds"
                    ),
                    details={"attempts": attempt},
                ) from exc
            except FileNotFoundError as exc:
                raise KaggleRuntimeError(
                    "prerequisite",
                    "Kaggle executable or Python interpreter was not found",
                ) from exc
            except OSError as exc:
                raise KaggleRuntimeError(
                    "command",
                    f"Could not start Kaggle command: {exc}",
                ) from exc

            returncode = int(getattr(completed, "returncode", 1))
            stdout = str(getattr(completed, "stdout", "") or "")
            stderr = str(getattr(completed, "stderr", "") or "")
            category = _error_category(returncode, stdout, stderr)
            if (
                category == "transient"
                and retryable
                and attempt < maximum_attempts
            ):
                self.sleep(float(2 ** (attempt - 1)))
                continue

            finished_at = _utc_now()
            return CommandResult(
                arguments=arguments,
                operation=operation,
                returncode=returncode,
                stdout=stdout,
                stderr=stderr,
                started_at=started_at,
                finished_at=finished_at,
                duration_seconds=max(0.0, time.monotonic() - started),
                executable=self.executable,
                attempts=attempt,
                error_category=category,
            )

        raise AssertionError("unreachable retry loop")

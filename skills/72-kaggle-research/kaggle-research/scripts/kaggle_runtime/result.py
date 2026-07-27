from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Optional


class OperationClass(str, Enum):
    READ = "read"
    DOWNLOAD = "download"
    REMOTE_WRITE = "remote_write"
    REMOTE_DELETE = "remote_delete"
    UNKNOWN = "unknown"


class KaggleRuntimeError(RuntimeError):
    """Stable public error raised by the Kaggle runtime boundary."""

    def __init__(
        self,
        category: str,
        message: str,
        *,
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(message)
        self.category = category
        self.message = message
        self.details = dict(details or {})


@dataclass(frozen=True)
class CommandRequest:
    arguments: tuple[str, ...]
    cwd: Optional[Path] = None
    output_root: Optional[Path] = None
    timeout_seconds: float = 120.0
    allow_write: bool = False
    allow_delete: bool = False
    confirm_resource: Optional[str] = None
    dry_run: bool = False
    retries: int = 1
    capture_limit: int = 16_384

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "arguments",
            tuple(str(argument) for argument in self.arguments),
        )
        if self.cwd is not None:
            object.__setattr__(self, "cwd", Path(self.cwd))
        if self.output_root is not None:
            object.__setattr__(self, "output_root", Path(self.output_root))
        if self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        if self.retries < 0:
            raise ValueError("retries cannot be negative")
        if self.capture_limit < 0:
            raise ValueError("capture_limit cannot be negative")


@dataclass(frozen=True)
class CommandResult:
    arguments: tuple[str, ...]
    operation: OperationClass
    returncode: int
    stdout: str
    stderr: str
    started_at: str
    finished_at: str
    duration_seconds: float
    executable: tuple[str, ...] = ()
    attempts: int = 1
    dry_run: bool = False
    error_category: Optional[str] = None
    artifacts: tuple[dict[str, Any], ...] = field(default_factory=tuple)

    @property
    def ok(self) -> bool:
        return self.returncode == 0 and self.error_category is None

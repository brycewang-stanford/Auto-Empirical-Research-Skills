"""Safe, auditable wrapper primitives for the official Kaggle CLI."""

from .commands import authorize, classify
from .runner import KaggleRunner
from .result import (
    CommandRequest,
    CommandResult,
    KaggleRuntimeError,
    OperationClass,
)

__all__ = [
    "CommandRequest",
    "CommandResult",
    "KaggleRuntimeError",
    "KaggleRunner",
    "OperationClass",
    "authorize",
    "classify",
]

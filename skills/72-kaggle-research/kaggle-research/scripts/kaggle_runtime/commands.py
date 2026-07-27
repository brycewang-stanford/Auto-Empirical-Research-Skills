from __future__ import annotations

from collections.abc import Sequence

from .result import CommandRequest, KaggleRuntimeError, OperationClass
from .security import contains_inline_credential


READ_ACTIONS = frozenset(
    {
        ("competitions", "files"),
        ("competitions", "leaderboard"),
        ("competitions", "list"),
        ("competitions", "submissions"),
        ("datasets", "files"),
        ("datasets", "list"),
        ("datasets", "metadata"),
        ("datasets", "status"),
        ("datasets", "view"),
        ("kernels", "files"),
        ("kernels", "list"),
        ("kernels", "status"),
        ("models", "files"),
        ("models", "get"),
        ("models", "list"),
    }
)

DOWNLOAD_ACTIONS = frozenset(
    {
        ("competitions", "download"),
        ("datasets", "download"),
        ("kernels", "output"),
        ("kernels", "pull"),
        ("models", "download"),
    }
)

WRITE_ACTIONS = frozenset(
    {
        ("auth", "login"),
        ("auth", "revoke"),
        ("competitions", "submit"),
        ("datasets", "create"),
        ("datasets", "init"),
        ("datasets", "version"),
        ("kernels", "init"),
        ("kernels", "push"),
        ("models", "create"),
        ("models", "update"),
    }
)

DELETE_GROUPS = frozenset(
    {"competitions", "datasets", "kernels", "models", "model-variations"}
)

SENSITIVE_COMMANDS = frozenset({("auth", "print-access-token")})

RESOURCE_FLAGS = frozenset(
    {
        "-c",
        "--competition",
        "-d",
        "--dataset",
        "-k",
        "--kernel",
        "--model",
        "--model-variation",
    }
)


def _group_action(arguments: Sequence[str]) -> tuple[str, str]:
    if not arguments:
        return "", ""
    group = str(arguments[0]).strip().lower()
    if group == "--version":
        return group, ""
    action = str(arguments[1]).strip().lower() if len(arguments) > 1 else ""
    return group, action


def classify(arguments: Sequence[str]) -> OperationClass:
    group, action = _group_action(arguments)
    if group == "--version":
        return OperationClass.READ
    if (group, action) in DOWNLOAD_ACTIONS:
        return OperationClass.DOWNLOAD
    if action == "delete" and group in DELETE_GROUPS:
        return OperationClass.REMOTE_DELETE
    if (group, action) in WRITE_ACTIONS:
        return OperationClass.REMOTE_WRITE
    if (group, action) in READ_ACTIONS:
        return OperationClass.READ
    if group == "config" and action in {"view", "get"}:
        return OperationClass.READ
    if group == "config" and action == "set":
        return OperationClass.REMOTE_WRITE
    return OperationClass.UNKNOWN


def _contains_control_characters(value: str) -> bool:
    return any(ord(character) < 32 or ord(character) == 127 for character in value)


def _extract_delete_resource(arguments: Sequence[str]) -> str | None:
    for index, argument in enumerate(arguments):
        if argument in RESOURCE_FLAGS and index + 1 < len(arguments):
            return str(arguments[index + 1])
        for flag in RESOURCE_FLAGS:
            prefix = f"{flag}="
            if str(argument).startswith(prefix):
                return str(argument)[len(prefix) :]

    if len(arguments) > 2:
        for argument in arguments[2:]:
            value = str(argument)
            if not value.startswith("-"):
                return value
    return None


def authorize(request: CommandRequest) -> OperationClass:
    if not request.arguments:
        raise KaggleRuntimeError("policy", "Kaggle arguments cannot be empty")
    if any(_contains_control_characters(argument) for argument in request.arguments):
        raise KaggleRuntimeError(
            "policy",
            "Kaggle arguments cannot contain control characters",
        )
    if contains_inline_credential(request.arguments):
        raise KaggleRuntimeError(
            "policy",
            "Credentials must be provided through official Kaggle authentication",
        )

    group_action = _group_action(request.arguments)
    if group_action in SENSITIVE_COMMANDS:
        raise KaggleRuntimeError(
            "policy",
            "Printing access tokens is blocked by the Kaggle research runtime",
        )

    operation = classify(request.arguments)
    if operation is OperationClass.DOWNLOAD and request.output_root is None:
        raise KaggleRuntimeError(
            "policy",
            "Download operations require an explicit output root",
        )
    if operation in {OperationClass.REMOTE_WRITE, OperationClass.UNKNOWN}:
        if not request.allow_write:
            raise KaggleRuntimeError(
                "policy",
                f"{operation.value} operation requires --allow-write",
            )
    if operation is OperationClass.REMOTE_DELETE:
        if not request.allow_write or not request.allow_delete:
            raise KaggleRuntimeError(
                "policy",
                "Delete operations require --allow-write and --allow-delete",
            )
        resource = _extract_delete_resource(request.arguments)
        if not resource or request.confirm_resource != resource:
            raise KaggleRuntimeError(
                "policy",
                "Delete confirmation must exactly match the target resource",
                details={
                    "resource": resource,
                    "confirmed": request.confirm_resource,
                },
            )
    return operation

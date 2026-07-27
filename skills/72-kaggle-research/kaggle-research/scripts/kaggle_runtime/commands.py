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
        ("datasets", "status"),
        ("datasets", "view"),
        ("kernels", "files"),
        ("kernels", "list"),
        ("kernels", "logs"),
        ("kernels", "status"),
        ("models", "files"),
        ("models", "list"),
    }
)

DOWNLOAD_ACTIONS = frozenset(
    {
        ("competitions", "download"),
        ("competitions", "logs"),
        ("competitions", "replay"),
        ("datasets", "download"),
        ("datasets", "metadata"),
        ("kernels", "output"),
        ("kernels", "pull"),
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
        ("models", "init"),
        ("models", "update"),
    }
)

DELETE_GROUPS = frozenset(
    {"competitions", "datasets", "kernels", "models"}
)

GROUP_ALIASES = {
    "c": "competitions",
    "d": "datasets",
    "k": "kernels",
    "m": "models",
}

READ_PREFIXES = (
    ("competitions", "team-submissions"),
    ("competitions", "episodes"),
    ("competitions", "pages"),
    ("competitions", "topics"),
    ("competitions", "topic-messages"),
    ("datasets", "topics"),
    ("kernels", "topics"),
    ("models", "topics"),
    ("models", "instances", "files"),
    ("models", "instances", "list"),
    ("models", "instances", "versions", "files"),
    ("models", "instances", "versions", "list"),
)

DOWNLOAD_PREFIXES = (
    ("models", "instances", "versions", "download"),
)

WRITE_PREFIXES = (
    ("models", "instances", "init"),
    ("models", "instances", "create"),
    ("models", "instances", "update"),
    ("models", "instances", "versions", "create"),
)

DELETE_PREFIXES = (
    ("models", "instances", "delete"),
    ("models", "instances", "versions", "delete"),
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
    normalized = _normalized_arguments(arguments)
    if not normalized:
        return "", ""
    group = normalized[0]
    if group == "--version":
        return group, ""
    action = normalized[1] if len(normalized) > 1 else ""
    return group, action


def _normalized_arguments(arguments: Sequence[str]) -> tuple[str, ...]:
    values = tuple(str(argument).strip().lower() for argument in arguments)
    if not values:
        return values
    normalized = list(values)
    normalized[0] = GROUP_ALIASES.get(normalized[0], normalized[0])
    if len(normalized) > 1 and normalized[0] == "models":
        if normalized[1] in {"i", "variations", "v"}:
            normalized[1] = "instances"
        if (
            len(normalized) > 2
            and normalized[1] == "instances"
            and normalized[2] == "v"
        ):
            normalized[2] = "versions"
    return tuple(normalized)


def _starts_with(
    arguments: Sequence[str],
    prefix: tuple[str, ...],
) -> bool:
    return tuple(arguments[: len(prefix)]) == prefix


def _has_path_option(arguments: Sequence[str]) -> bool:
    return any(
        argument in {"-p", "--path"}
        or argument.startswith("-p=")
        or argument.startswith("--path=")
        for argument in arguments
    )


def classify(arguments: Sequence[str]) -> OperationClass:
    normalized = _normalized_arguments(arguments)
    group, action = _group_action(normalized)
    if group == "--version":
        return OperationClass.READ
    if any(_starts_with(normalized, prefix) for prefix in DELETE_PREFIXES):
        return OperationClass.REMOTE_DELETE
    if any(_starts_with(normalized, prefix) for prefix in DOWNLOAD_PREFIXES):
        return OperationClass.DOWNLOAD
    if any(_starts_with(normalized, prefix) for prefix in WRITE_PREFIXES):
        return OperationClass.REMOTE_WRITE
    if any(_starts_with(normalized, prefix) for prefix in READ_PREFIXES):
        return OperationClass.READ
    if (
        _starts_with(normalized, ("competitions", "leaderboard"))
        and any(option in normalized for option in {"-d", "--download"})
    ):
        return OperationClass.DOWNLOAD
    if _starts_with(normalized, ("competitions", "leaderboard")):
        return OperationClass.READ
    if _starts_with(normalized, ("models", "get")):
        return (
            OperationClass.DOWNLOAD
            if _has_path_option(normalized)
            else OperationClass.READ
        )
    if _starts_with(normalized, ("models", "instances", "get")):
        return (
            OperationClass.DOWNLOAD
            if _has_path_option(normalized)
            else OperationClass.READ
        )
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

    normalized = _normalized_arguments(arguments)
    if "delete" in normalized:
        delete_index = normalized.index("delete")
        for argument in arguments[delete_index + 1 :]:
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

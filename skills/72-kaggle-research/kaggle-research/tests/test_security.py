from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import _support  # noqa: F401
from kaggle_runtime.result import KaggleRuntimeError
from kaggle_runtime.security import redact_arguments, redact_text, resolve_output_path


class RedactionTests(unittest.TestCase):
    def test_redacts_tokens_headers_legacy_keys_and_signed_urls(self):
        raw = (
            "KAGGLE_API_TOKEN=secret-one "
            "Authorization: Bearer secret-two "
            "KAGGLE_KEY=legacy-secret "
            "token=secret-three "
            "https://storage.example/file?X-Goog-Signature=abc123&x=1"
        )
        redacted = redact_text(raw)
        for secret in (
            "secret-one",
            "secret-two",
            "legacy-secret",
            "secret-three",
            "abc123",
        ):
            self.assertNotIn(secret, redacted)
        self.assertGreaterEqual(redacted.count("[REDACTED]"), 5)
        self.assertIn("&x=1", redacted)

    def test_redacts_kgat_token_without_variable_name(self):
        token = "KGAT_" + "a" * 32
        self.assertNotIn(token, redact_text(f"failure for {token}"))

    def test_redacts_sensitive_argument_values(self):
        arguments = (
            "--header",
            "Authorization: Bearer secret",
            "--token=another-secret",
            "datasets",
            "list",
        )
        redacted = redact_arguments(arguments)
        self.assertEqual(redacted[-2:], ("datasets", "list"))
        self.assertNotIn("secret", " ".join(redacted))


class OutputPathTests(unittest.TestCase):
    def test_relative_output_path_must_remain_inside_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            self.assertEqual(
                resolve_output_path(root, "nested/out"),
                (root / "nested" / "out").resolve(),
            )
            with self.assertRaises(KaggleRuntimeError) as ctx:
                resolve_output_path(root, "../escape")
            self.assertEqual(ctx.exception.category, "path")

    def test_absolute_path_outside_root_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            outside = root.parent / "outside"
            with self.assertRaises(KaggleRuntimeError):
                resolve_output_path(root, outside)

    def test_control_characters_in_path_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(KaggleRuntimeError):
                resolve_output_path(Path(tmp), "bad\npath")


if __name__ == "__main__":
    unittest.main()

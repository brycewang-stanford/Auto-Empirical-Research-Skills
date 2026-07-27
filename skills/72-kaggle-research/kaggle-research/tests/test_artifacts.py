from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import _support  # noqa: F401
from kaggle_runtime.artifacts import (
    build_artifact_manifest,
    build_audit_record,
    write_audit,
)
from kaggle_runtime.result import (
    CommandResult,
    KaggleRuntimeError,
    OperationClass,
)


def sample_result(**overrides):
    values = {
        "arguments": ("datasets", "list"),
        "operation": OperationClass.READ,
        "returncode": 0,
        "stdout": "ok",
        "stderr": "",
        "started_at": "2026-07-27T00:00:00Z",
        "finished_at": "2026-07-27T00:00:01Z",
        "duration_seconds": 1.0,
        "executable": ("python", "-m", "kaggle"),
    }
    values.update(overrides)
    return CommandResult(**values)


class AuditTests(unittest.TestCase):
    def test_audit_is_redacted_bounded_and_hashed(self):
        result = sample_result(
            stdout="KAGGLE_API_TOKEN=secret\n" + "x" * 5000,
            stderr="Authorization: Bearer other-secret",
        )
        record = build_audit_record(result, capture_limit=128)
        encoded = json.dumps(record)
        self.assertNotIn("secret", encoded)
        self.assertTrue(record["stdout"]["truncated"])
        self.assertLessEqual(len(record["stdout"]["text"]), 128)
        self.assertRegex(record["stdout"]["sha256"], r"^[0-9a-f]{64}$")
        self.assertRegex(record["stderr"]["sha256"], r"^[0-9a-f]{64}$")
        self.assertEqual(record["operation"], "read")
        self.assertEqual(record["schema_version"], "aers.kaggle.audit/v1")

    def test_write_audit_creates_valid_json_without_temp_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp) / "audit.json"
            written = write_audit(sample_result(), destination)
            self.assertEqual(written, destination)
            payload = json.loads(destination.read_text(encoding="utf-8"))
            self.assertEqual(payload["returncode"], 0)
            self.assertEqual(
                list(Path(tmp).glob("*.tmp")),
                [],
            )


class ArtifactManifestTests(unittest.TestCase):
    def test_manifest_hashes_files_in_deterministic_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "z.txt").write_bytes(b"z")
            (root / "data").mkdir()
            (root / "data" / "a.csv").write_bytes(b"a,b\n1,2\n")
            manifest = build_artifact_manifest(root, max_total_bytes=1024)
            self.assertEqual(
                [entry["path"] for entry in manifest],
                ["data/a.csv", "z.txt"],
            )
            self.assertEqual(manifest[0]["size"], 8)
            self.assertRegex(manifest[0]["sha256"], r"^[0-9a-f]{64}$")

    def test_manifest_rejects_total_size_limit(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "large.bin").write_bytes(b"x" * 11)
            with self.assertRaises(KaggleRuntimeError) as ctx:
                build_artifact_manifest(root, max_total_bytes=10)
            self.assertEqual(ctx.exception.category, "artifact")

    def test_manifest_rejects_symlink_escape_when_supported(self):
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as outside:
            root = Path(tmp)
            target = Path(outside) / "secret.txt"
            target.write_text("outside", encoding="utf-8")
            link = root / "escape.txt"
            try:
                link.symlink_to(target)
            except OSError:
                self.skipTest("symlink creation is not available")
            with self.assertRaises(KaggleRuntimeError):
                build_artifact_manifest(root, max_total_bytes=1024)


if __name__ == "__main__":
    unittest.main()

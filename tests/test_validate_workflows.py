"""Tests for GitHub Actions workflow policy validation."""

from __future__ import annotations

import contextlib
import io
import tempfile
import unittest

from _helpers import load_module

workflow_policy = load_module(
    "scripts/validate-workflows.py",
    "aers_validate_workflows",
)


class TestWorkflowPolicy(unittest.TestCase):
    def _with_workflow(self, text: str):
        tmp = tempfile.TemporaryDirectory()
        root = workflow_policy.Path(tmp.name)
        workflows_dir = root / ".github" / "workflows"
        workflows_dir.mkdir(parents=True)
        path = workflows_dir / "test.yml"
        path.write_text(text, encoding="utf-8")
        old_root = workflow_policy.ROOT
        old_workflows_dir = workflow_policy.WORKFLOWS_DIR
        workflow_policy.ROOT = root
        workflow_policy.WORKFLOWS_DIR = workflows_dir
        self.addCleanup(tmp.cleanup)
        self.addCleanup(setattr, workflow_policy, "ROOT", old_root)
        self.addCleanup(setattr, workflow_policy, "WORKFLOWS_DIR", old_workflows_dir)
        return path

    def test_current_repo_workflows_pass_policy(self):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(workflow_policy.main([]), 0)

    def test_pull_request_write_permissions_fail(self):
        path = self._with_workflow(
            """
name: Bad PR workflow
on:
  pull_request:
permissions:
  contents: write
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          persist-credentials: false
"""
        )
        errors = workflow_policy.validate_workflow(path)
        self.assertTrue(any("grants write permission" in error for error in errors))

    def test_scheduled_write_permissions_are_allowed_for_sync_workflows(self):
        path = self._with_workflow(
            """
name: Sync
on:
  schedule:
    - cron: "0 6 * * 1"
permissions:
  contents: write
  pull-requests: write
jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          persist-credentials: false
"""
        )
        errors = workflow_policy.validate_workflow(path)
        self.assertFalse([error for error in errors if "grants write permission" in error])

    def test_pull_request_write_all_fails(self):
        path = self._with_workflow(
            """
name: Bad PR workflow
on: [pull_request]
permissions: write-all
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          persist-credentials: false
"""
        )
        errors = workflow_policy.validate_workflow(path)
        self.assertTrue(any("write-all" in error for error in errors))

    def test_floating_or_missing_action_refs_fail(self):
        path = self._with_workflow(
            """
name: Floating actions
on:
  workflow_dispatch: {}
permissions:
  contents: read
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@main
        with:
          persist-credentials: false
      - uses: actions/setup-python
"""
        )
        errors = workflow_policy.validate_workflow(path)
        self.assertTrue(any("floating ref" in error for error in errors))
        self.assertTrue(any("must pin a ref" in error for error in errors))

    def test_local_actions_and_docker_images_are_not_ref_pinned(self):
        path = self._with_workflow(
            """
name: Local actions
on:
  workflow_dispatch: {}
permissions:
  contents: read
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: ./actions/local
      - uses: docker://alpine:3.20
"""
        )
        errors = workflow_policy.validate_workflow(path)
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()

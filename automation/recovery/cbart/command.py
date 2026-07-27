"""Subprocess execution helpers."""

from __future__ import annotations

import subprocess

from .config import REPO_ROOT


def run_command(command: list[str]) -> None:
    """Run a command from the repository root and fail on error."""
    print("\nRunning:", " ".join(command), "\n")
    subprocess.run(command, cwd=REPO_ROOT, check=True)

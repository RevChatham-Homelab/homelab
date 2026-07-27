"""CBART environment validation."""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

from .config import OUTPUT_DIR, REPO_ROOT, RUN_SCRIPT, SANITIZE_SCRIPT


def validate_executable(path: Path) -> bool:
    if not path.is_file():
        print(f"Missing script: {path}", file=sys.stderr)
        return False

    if not os.access(path, os.X_OK):
        print(f"Not executable: {path}", file=sys.stderr)
        return False

    return True


def validate_environment() -> bool:
    valid = True

    for script in (RUN_SCRIPT, SANITIZE_SCRIPT):
        if not validate_executable(script):
            valid = False

    if not REPO_ROOT.is_dir():
        print(f"Repository unavailable: {REPO_ROOT}", file=sys.stderr)
        valid = False

    if shutil.which("du") is None:
        print("Missing required command: du", file=sys.stderr)
        valid = False

    try:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        print(f"Output directory error: {exc}", file=sys.stderr)
        valid = False

    return valid


def repository_status() -> str:
    return "Healthy" if REPO_ROOT.is_dir() else "Unavailable"

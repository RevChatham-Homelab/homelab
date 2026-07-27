"""CBART configuration and filesystem paths."""

from __future__ import annotations

import os
from pathlib import Path

from . import APP_FULL_NAME, APP_NAME, APP_VERSION

WIDTH = 72

CBART_DIR = Path(__file__).resolve().parent
RECOVERY_ROOT = CBART_DIR.parent
REPO_ROOT = RECOVERY_ROOT.parent.parent
BIN_DIR = RECOVERY_ROOT / "bin"
OUTPUT_DIR = RECOVERY_ROOT / "output"
EXAMPLE_OUTPUT_DIR = RECOVERY_ROOT / "output.example"
DOCS_ROOT = REPO_ROOT / "docs"

RUN_SCRIPT = BIN_DIR / "run-recovery-point"
SANITIZE_SCRIPT = BIN_DIR / "sanitize-recovery-point"

T14_TARGET = os.environ.get(
    "RECOVERY_T14_TARGET",
    "t14:~/Recovery_Points/",
)

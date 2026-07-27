"""Recovery Point library operations."""

from __future__ import annotations

import subprocess
from pathlib import Path

from .command import run_command
from .config import EXAMPLE_OUTPUT_DIR, OUTPUT_DIR, SANITIZE_SCRIPT


def recovery_points() -> list[Path]:
    """Return Recovery Point directories sorted by identifier."""
    if not OUTPUT_DIR.exists():
        return []

    return sorted(
        [
            path
            for path in OUTPUT_DIR.iterdir()
            if path.is_dir() and path.name.startswith("RP-")
        ],
        key=lambda path: path.name,
    )


def point_size(point: Path) -> str:
    try:
        return subprocess.check_output(
            ["du", "-sh", str(point)],
            text=True,
        ).split()[0]
    except (OSError, subprocess.SubprocessError, IndexError):
        return "Unknown"


def library_summary() -> list[tuple[str, str]]:
    points = recovery_points()

    return [
        ("Recovery Points", str(len(points))),
        ("Newest", points[-1].name if points else "None"),
        ("Oldest", points[0].name if points else "None"),
    ]


def sanitize_recovery_point(point: Path) -> None:
    run_command([str(SANITIZE_SCRIPT), str(point)])
    print(f"Sanitized output root: {EXAMPLE_OUTPUT_DIR}")

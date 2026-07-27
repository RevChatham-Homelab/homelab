"""Recovery Point generation and copy operations."""

from __future__ import annotations

import os
import shutil
from pathlib import Path

from .command import run_command
from .config import RUN_SCRIPT, T14_TARGET
from .library import recovery_points


def newest_new_point(before: set[Path]) -> Path:
    after = set(recovery_points())
    created = sorted(after - before, key=lambda path: path.name)

    if len(created) == 1:
        return created[0]

    if created:
        return max(created, key=lambda path: path.stat().st_mtime)

    points = recovery_points()

    if not points:
        raise RuntimeError("No Recovery Point directory was created.")

    return max(points, key=lambda path: path.stat().st_mtime)


def generate_server_recovery_point() -> Path:
    before = set(recovery_points())
    run_command([str(RUN_SCRIPT)])
    return newest_new_point(before)


def flash_mounts() -> list[Path]:
    user = os.environ.get("USER", "angel")
    roots = [
        Path("/media") / user,
        Path("/run/media") / user,
        Path("/mnt"),
    ]
    found: set[Path] = set()

    for root in roots:
        if not root.is_dir():
            continue

        try:
            for item in root.iterdir():
                if item.is_dir() and os.path.ismount(item):
                    found.add(item)
        except PermissionError:
            continue

    return sorted(found, key=str)


def copy_to_flash(point: Path, destination_root: Path) -> Path:
    destination = destination_root / "Recovery_Points" / point.name
    destination.parent.mkdir(parents=True, exist_ok=True)

    if destination.exists():
        raise FileExistsError(destination)

    shutil.copytree(point, destination, symlinks=True)
    return destination


def copy_to_t14(point: Path) -> str:
    if shutil.which("rsync") is None:
        raise RuntimeError("rsync is not installed.")

    target = T14_TARGET.rstrip("/") + f"/{point.name}/"

    run_command(
        [
            "rsync",
            "-a",
            "--human-readable",
            "--info=progress2",
            f"{point}/",
            target,
        ]
    )
    return target

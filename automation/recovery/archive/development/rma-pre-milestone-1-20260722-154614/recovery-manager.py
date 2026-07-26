#!/usr/bin/env python3
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
RECOVERY_ROOT = REPO_ROOT / "automation" / "recovery"
OUTPUT_DIR = RECOVERY_ROOT / "output"
EXAMPLE_OUTPUT_DIR = RECOVERY_ROOT / "output.example"
RUN_SCRIPT = RECOVERY_ROOT / "bin" / "run-recovery-point"
SANITIZE_SCRIPT = RECOVERY_ROOT / "bin" / "sanitize-recovery-point"
T14_TARGET = os.environ.get("RECOVERY_T14_TARGET", "t14:~/Recovery_Points/")


def header(title: str) -> None:
    print("\n" + "=" * 68)
    print(title)
    print("=" * 68)


def run(command: list[str]) -> None:
    print("\nRunning:", " ".join(command), "\n")
    subprocess.run(command, cwd=REPO_ROOT, check=True)


def recovery_points() -> list[Path]:
    if not OUTPUT_DIR.exists():
        return []
    return sorted(
        [p for p in OUTPUT_DIR.iterdir() if p.is_dir() and p.name.startswith("RP-")],
        key=lambda p: p.name,
    )


def choose(items: list[Path], prompt: str) -> Path | None:
    if not items:
        print("No Recovery Points found.")
        return None
    for i, item in enumerate(items, 1):
        print(f"  {i}. {item.name}")
    print("  0. Cancel")
    while True:
        value = input(f"\n{prompt}: ").strip()
        if value == "0":
            return None
        try:
            return items[int(value) - 1]
        except (ValueError, IndexError):
            print("Invalid selection.")


def choose_destination() -> str:
    header("Recovery Point Destination")
    print("  1. Server only")
    print("  2. Server and flash drive")
    print("  3. Server and T14")
    print("  4. Server, flash drive, and T14")
    print("  0. Cancel")
    while True:
        value = input("\nChoose a destination: ").strip()
        if value in {"0", "1", "2", "3", "4"}:
            return value
        print("Invalid selection.")


def newest_new_point(before: set[Path]) -> Path:
    after = set(recovery_points())
    created = sorted(after - before, key=lambda p: p.name)
    if len(created) == 1:
        return created[0]
    if created:
        selected = choose(created, "Select the new Recovery Point")
        if selected:
            return selected
    points = recovery_points()
    if not points:
        raise RuntimeError("No Recovery Point directory was created.")
    return max(points, key=lambda p: p.stat().st_mtime)


def flash_mounts() -> list[Path]:
    user = os.environ.get("USER", "angel")
    roots = [Path("/media") / user, Path("/run/media") / user, Path("/mnt")]
    found: set[Path] = set()
    for root in roots:
        if not root.is_dir():
            continue
        try:
            for item in root.iterdir():
                if item.is_dir() and os.path.ismount(item):
                    found.add(item)
        except PermissionError:
            pass
    return sorted(found, key=str)


def copy_to_flash(point: Path) -> None:
    header("Flash Drive")
    mounts = flash_mounts()
    for i, mount in enumerate(mounts, 1):
        print(f"  {i}. {mount}")
    print("  0. Enter path manually or cancel")

    destination_root: Path | None = None
    if mounts:
        choice = input("\nChoose a mounted drive: ").strip()
        if choice != "0":
            try:
                destination_root = mounts[int(choice) - 1]
            except (ValueError, IndexError):
                raise RuntimeError("Invalid flash-drive selection.")

    if destination_root is None:
        manual = input("Mounted path (blank cancels): ").strip()
        if not manual:
            print("Flash-drive copy cancelled.")
            return
        destination_root = Path(manual).expanduser().resolve()

    if not destination_root.is_dir():
        raise RuntimeError(f"Destination does not exist: {destination_root}")

    destination = destination_root / "Recovery_Points" / point.name
    destination.parent.mkdir(parents=True, exist_ok=True)

    if destination.exists():
        answer = input(f"{destination} exists. Replace it? [y/N]: ").strip().lower()
        if answer != "y":
            print("Flash-drive copy skipped.")
            return
        shutil.rmtree(destination)

    shutil.copytree(point, destination, symlinks=True)
    print(f"Copied to: {destination}")


def copy_to_t14(point: Path) -> None:
    if shutil.which("rsync") is None:
        raise RuntimeError("rsync is not installed.")
    target = T14_TARGET.rstrip("/") + f"/{point.name}/"
    header("T14 Copy")
    print(f"Target: {target}")
    answer = input("Continue? [Y/n]: ").strip().lower()
    if answer not in {"", "y"}:
        print("T14 copy cancelled.")
        return
    run(["rsync", "-a", "--human-readable", "--info=progress2", f"{point}/", target])


def generate() -> None:
    destination = choose_destination()
    if destination == "0":
        return

    before = set(recovery_points())
    run([str(RUN_SCRIPT)])
    point = newest_new_point(before)

    header("Recovery Point Created")
    print(f"Server copy: {point}")

    if destination in {"2", "4"}:
        try:
            copy_to_flash(point)
        except Exception as exc:
            print(f"Flash-drive copy failed: {exc}")
            print("The server copy remains intact.")

    if destination in {"3", "4"}:
        try:
            copy_to_t14(point)
        except Exception as exc:
            print(f"T14 copy failed: {exc}")
            print("The server copy remains intact.")


def sanitize() -> None:
    header("Sanitize Recovery Point")
    point = choose(recovery_points(), "Choose a Recovery Point")
    if point is None:
        return
    run([str(SANITIZE_SCRIPT), str(point)])
    print(f"Sanitized output root: {EXAMPLE_OUTPUT_DIR}")


def list_points() -> None:
    header("Recovery Points")
    points = recovery_points()
    if not points:
        print("No Recovery Points found.")
        return
    for point in points:
        try:
            size = subprocess.check_output(
                ["du", "-sh", str(point)], text=True
            ).split()[0]
        except Exception:
            size = "unknown"
        print(f"  {point.name:<24} {size:>10}  {point}")


def main() -> int:
    for script in (RUN_SCRIPT, SANITIZE_SCRIPT):
        if not script.is_file():
            print(f"Missing script: {script}", file=sys.stderr)
            return 1
        if not os.access(script, os.X_OK):
            print(f"Not executable: {script}", file=sys.stderr)
            return 1

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    while True:
        header("RevChatham Homelab Recovery Manager")
        print("  1. Generate a Recovery Point")
        print("  2. Sanitize an existing Recovery Point")
        print("  3. List Recovery Points")
        print("  4. Show configuration")
        print("  0. Exit")

        choice = input("\nChoose an option: ").strip()

        try:
            if choice == "1":
                generate()
            elif choice == "2":
                sanitize()
            elif choice == "3":
                list_points()
            elif choice == "4":
                header("Configuration")
                print(f"Repository:      {REPO_ROOT}")
                print(f"Output:          {OUTPUT_DIR}")
                print(f"Example output:  {EXAMPLE_OUTPUT_DIR}")
                print(f"T14 target:      {T14_TARGET}")
            elif choice == "0":
                return 0
            else:
                print("Invalid selection.")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
        except subprocess.CalledProcessError as exc:
            print(f"Command failed with exit code {exc.returncode}.")
        except Exception as exc:
            print(f"Error: {exc}")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    raise SystemExit(main())

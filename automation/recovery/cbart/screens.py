"""Standards-compliant CBART screens and navigation."""

from __future__ import annotations

import subprocess
from pathlib import Path

from . import APP_FULL_NAME, APP_NAME, APP_VERSION
from .about import about_rows
from .backup import copy_to_flash, copy_to_t14, flash_mounts, generate_server_recovery_point
from .config import DOCS_ROOT, OUTPUT_DIR, RECOVERY_ROOT, REPO_ROOT, T14_TARGET
from .keyboard import get_key, wait_for_enter
from .library import library_summary, point_size, recovery_points, sanitize_recovery_point
from .ui import boxed_status, clear_screen, invalid_selection, section, title_block
from .validation import repository_status


UTILITY_OPTIONS = [
    "F1. Settings",
    "F2. Documentation",
    "F3. About",
    "F4. Logs",
    "F5. Help",
    "F10. Print / Export [Unavailable]",
]


def newest_point_name() -> str:
    points = recovery_points()
    return points[-1].name if points else "None"


def main_status() -> list[tuple[str, str]]:
    return [
        ("Repository", repository_status()),
        ("Recovery Points", str(len(recovery_points()))),
        ("Newest Recovery Point", newest_point_name()),
        ("Verification", "See latest Recovery Point report"),
    ]


def render_standard_screen(
    title: str,
    status_title: str,
    status_rows: list[tuple[str, str]],
    operations: list[str],
    navigation: list[str],
    utilities: list[str] | None = None,
) -> None:
    clear_screen()
    title_block(title)
    print()
    boxed_status(status_title, status_rows)
    section("Operations", operations)
    section("Utilities", UTILITY_OPTIONS if utilities is None else utilities)
    section("Navigation", navigation)


def dispatch_utility(key: str) -> bool:
    if key == "F1":
        settings_screen()
    elif key == "F2":
        documentation_screen()
    elif key == "F3":
        about_screen()
    elif key == "F4":
        logs_screen()
    elif key == "F5":
        help_screen()
    elif key == "F10":
        unavailable_screen("Print / Export")
    else:
        return False
    return True


def unavailable_screen(feature: str) -> None:
    render_standard_screen(
        feature,
        "Status",
        [("Availability", "Unavailable in this release")],
        [],
        ["8. Back", "0. Exit"],
        ["F3. About", "F5. Help"],
    )

    while True:
        key = get_key()
        if key == "8":
            return
        if key == "0":
            raise SystemExit(0)
        if dispatch_utility(key):
            continue
        invalid_selection(key, ["8", "0", "F3", "F5"])
        wait_for_enter()


def main_menu() -> None:
    valid = ["1", "2", "3", "0", "F1", "F2", "F3", "F4", "F5", "F10"]

    while True:
        clear_screen()
        title_block(APP_NAME, APP_FULL_NAME, f"Version {APP_VERSION}")
        print()
        boxed_status("System Status", main_status())
        section(
            "Operations",
            [
                "1. Backup Operations",
                "2. Recovery Point Library",
                "3. Restore [Unavailable]",
            ],
        )
        section("Utilities", UTILITY_OPTIONS)
        section("Navigation", ["0. Exit"])

        key = get_key()

        if key == "1":
            backup_operations_screen()
        elif key == "2":
            recovery_library_screen()
        elif key == "3":
            unavailable_screen("Restore")
        elif key == "0":
            return
        elif not dispatch_utility(key):
            invalid_selection(key, valid)
            wait_for_enter()


def backup_operations_screen() -> None:
    valid = ["1", "2", "3", "8", "9", "0", "F1", "F2", "F3", "F4", "F5", "F10"]

    while True:
        render_standard_screen(
            "Backup Operations",
            "Current Defaults",
            [
                ("Destination", "Ubuntu Server"),
                ("Verification", "Enabled by Recovery Point engine"),
                ("Sanitized Copy", "Disabled"),
            ],
            [
                "1. Generate Recovery Point",
                "2. Configure Destinations",
                "3. Verify Last Backup [Engine Report]",
            ],
            ["8. Back", "9. Refresh", "0. Exit"],
        )

        key = get_key()

        if key == "1":
            destination_screen()
        elif key == "2":
            destination_configuration_screen()
        elif key == "3":
            show_last_verification()
        elif key == "8":
            return
        elif key == "9":
            continue
        elif key == "0":
            raise SystemExit(0)
        elif not dispatch_utility(key):
            invalid_selection(key, valid)
            wait_for_enter()


def destination_screen() -> None:
    valid = ["1", "2", "3", "4", "8", "0"]

    while True:
        render_standard_screen(
            "Generate Recovery Point",
            "Destination Selection",
            [
                ("Primary Storage", "Ubuntu Server"),
                ("T14 Target", T14_TARGET),
                ("Flash Drives Detected", str(len(flash_mounts()))),
            ],
            [
                "1. Server only",
                "2. Server and flash drive",
                "3. Server and T14",
                "4. Server, flash drive, and T14",
            ],
            ["8. Back", "0. Cancel"],
            [],
        )

        key = get_key()

        if key in {"1", "2", "3", "4"}:
            run_backup_destination(key)
            return
        if key == "8":
            return
        if key == "0":
            return

        invalid_selection(key, valid)
        wait_for_enter()


def run_backup_destination(choice: str) -> None:
    clear_screen()
    title_block("Recovery Point Generation")
    print()
    point = generate_server_recovery_point()
    print(f"Server copy created: {point}")

    if choice in {"2", "4"}:
        mounts = flash_mounts()

        if not mounts:
            print("Flash-drive copy skipped: no mounted destination detected.")
        else:
            destination_root = choose_flash_mount(mounts)
            if destination_root is not None:
                try:
                    copied = copy_to_flash(point, destination_root)
                    print(f"Flash-drive copy created: {copied}")
                except FileExistsError as exc:
                    print(f"Flash-drive copy skipped; destination exists: {exc}")

    if choice in {"3", "4"}:
        target = copy_to_t14(point)
        print(f"T14 copy created: {target}")

    wait_for_enter("Recovery Point operation complete. Press Enter to continue...")


def choose_flash_mount(mounts: list[Path]) -> Path | None:
    while True:
        clear_screen()
        title_block("Flash Drive Selection")
        print()
        boxed_status("Detected Destinations", [("Mounted Drives", str(len(mounts)))])
        operations = [
            f"{index}. {mount}"
            for index, mount in enumerate(mounts[:6], 1)
        ]
        section("Operations", operations)
        section("Navigation", ["8. Back", "0. Cancel"])

        valid = [str(i) for i in range(1, min(len(mounts), 6) + 1)] + ["8", "0"]
        key = get_key()

        if key in valid[:-2]:
            return mounts[int(key) - 1]
        if key in {"8", "0"}:
            return None

        invalid_selection(key, valid)
        wait_for_enter()


def destination_configuration_screen() -> None:
    render_standard_screen(
        "Destination Configuration",
        "Current Configuration",
        [
            ("Primary Storage", "Ubuntu Server"),
            ("Backup Storage", "Mounted flash drive selected at runtime"),
            ("Offsite", T14_TARGET),
        ],
        [
            "1. Change Backup Storage [Runtime Selection]",
            "2. Change Offsite Destination [Environment Variable]",
            "3. Test Destinations [Unavailable]",
            "4. Reset to Defaults [Unavailable]",
        ],
        ["8. Back", "9. Refresh", "0. Exit"],
    )

    while True:
        key = get_key()
        if key == "8":
            return
        if key == "9":
            return
        if key == "0":
            raise SystemExit(0)
        if key in {"1", "2", "3", "4"}:
            unavailable_screen("Destination Configuration Change")
            return
        if dispatch_utility(key):
            continue
        invalid_selection(
            key,
            ["1", "2", "3", "4", "8", "9", "0", "F1", "F2", "F3", "F4", "F5", "F10"],
        )
        wait_for_enter()


def recovery_library_screen() -> None:
    valid = ["1", "2", "3", "4", "8", "9", "0", "F1", "F2", "F3", "F4", "F5", "F10"]

    while True:
        render_standard_screen(
            "Recovery Point Library",
            "Summary",
            library_summary(),
            [
                "1. Browse Recovery Points",
                "2. Sanitize Recovery Point",
                "3. Verify Recovery Point [Engine Report]",
                "4. Export Recovery Point [Unavailable]",
            ],
            ["8. Back", "9. Refresh", "0. Exit"],
        )

        key = get_key()

        if key == "1":
            browse_recovery_points()
        elif key == "2":
            sanitize_screen()
        elif key == "3":
            show_last_verification()
        elif key == "4":
            unavailable_screen("Export Recovery Point")
        elif key == "8":
            return
        elif key == "9":
            continue
        elif key == "0":
            raise SystemExit(0)
        elif not dispatch_utility(key):
            invalid_selection(key, valid)
            wait_for_enter()


def browse_recovery_points() -> None:
    points = recovery_points()
    rows = [("Recovery Points", str(len(points))), ("Output Directory", str(OUTPUT_DIR))]
    operations = [
        f"{index}. {point.name}  {point_size(point)}"
        for index, point in enumerate(points[-6:], 1)
    ]

    render_standard_screen(
        "Browse Recovery Points",
        "Summary",
        rows,
        operations or ["No Recovery Points available"],
        ["8. Back", "9. Refresh", "0. Exit"],
        ["F3. About", "F5. Help"],
    )

    while True:
        key = get_key()

        if key == "8":
            return
        if key == "9":
            return browse_recovery_points()
        if key == "0":
            raise SystemExit(0)
        if key in {str(i) for i in range(1, len(operations) + 1)} and points:
            point_detail(points[-6:][int(key) - 1])
            return browse_recovery_points()
        if dispatch_utility(key):
            continue

        valid = [str(i) for i in range(1, len(operations) + 1)] + ["8", "9", "0", "F3", "F5"]
        invalid_selection(key, valid)
        wait_for_enter()


def point_detail(point: Path) -> None:
    render_standard_screen(
        "Recovery Point Detail",
        point.name,
        [
            ("Path", str(point)),
            ("Size", point_size(point)),
        ],
        [],
        ["8. Back", "0. Exit"],
        ["F3. About", "F5. Help"],
    )

    while True:
        key = get_key()
        if key == "8":
            return
        if key == "0":
            raise SystemExit(0)
        if dispatch_utility(key):
            continue
        invalid_selection(key, ["8", "0", "F3", "F5"])
        wait_for_enter()


def sanitize_screen() -> None:
    points = recovery_points()[-6:]

    render_standard_screen(
        "Sanitize Recovery Point",
        "Available Recovery Points",
        [("Count", str(len(points)))],
        [f"{i}. {point.name}" for i, point in enumerate(points, 1)],
        ["8. Back", "0. Cancel"],
        [],
    )

    while True:
        key = get_key()
        valid_numbers = {str(i) for i in range(1, len(points) + 1)}

        if key in valid_numbers:
            point = points[int(key) - 1]
            clear_screen()
            title_block("Sanitize Recovery Point")
            sanitize_recovery_point(point)
            wait_for_enter()
            return
        if key in {"8", "0"}:
            return

        invalid_selection(key, sorted(valid_numbers) + ["8", "0"])
        wait_for_enter()


def show_last_verification() -> None:
    points = recovery_points()

    if not points:
        unavailable_screen("Recovery Point Verification")
        return

    point = points[-1]
    verification_dir = point / "verification"
    files = sorted(verification_dir.glob("*")) if verification_dir.is_dir() else []

    render_standard_screen(
        "Recovery Point Verification",
        "Latest Recovery Point",
        [
            ("Recovery Point", point.name),
            ("Verification Files", str(len(files))),
            ("Status", "Report available" if files else "No report found"),
        ],
        [f"{i}. {file.name}" for i, file in enumerate(files[:6], 1)],
        ["8. Back", "9. Refresh", "0. Exit"],
        ["F3. About", "F5. Help"],
    )

    while True:
        key = get_key()
        if key == "8":
            return
        if key == "9":
            return show_last_verification()
        if key == "0":
            raise SystemExit(0)
        if key in {str(i) for i in range(1, len(files[:6]) + 1)}:
            print("\n" + files[int(key) - 1].read_text(errors="replace"))
            wait_for_enter()
            return
        if dispatch_utility(key):
            continue
        invalid_selection(key, ["8", "9", "0", "F3", "F5"])
        wait_for_enter()


def settings_screen() -> None:
    render_standard_screen(
        "Settings",
        "Current Configuration",
        [
            ("Repository", str(REPO_ROOT)),
            ("Recovery Root", str(RECOVERY_ROOT)),
            ("Output", str(OUTPUT_DIR)),
            ("T14 Target", T14_TARGET),
        ],
        [],
        ["8. Back", "0. Exit"],
        ["F2. Documentation", "F3. About", "F5. Help"],
    )

    while True:
        key = get_key()
        if key == "8":
            return
        if key == "0":
            raise SystemExit(0)
        if dispatch_utility(key):
            continue
        invalid_selection(key, ["8", "0", "F2", "F3", "F5"])
        wait_for_enter()


def documentation_screen() -> None:
    docs = sorted(DOCS_ROOT.rglob("*.md"))[:6] if DOCS_ROOT.is_dir() else []

    render_standard_screen(
        "Documentation",
        "Repository Documentation",
        [
            ("Documentation Root", str(DOCS_ROOT)),
            ("Markdown Documents", str(len(list(DOCS_ROOT.rglob('*.md')))) if DOCS_ROOT.is_dir() else "0"),
        ],
        [f"{i}. {doc.relative_to(REPO_ROOT)}" for i, doc in enumerate(docs, 1)],
        ["8. Back", "0. Exit"],
        ["F1. Settings", "F3. About", "F5. Help"],
    )

    while True:
        key = get_key()
        if key == "8":
            return
        if key == "0":
            raise SystemExit(0)
        if key in {str(i) for i in range(1, len(docs) + 1)}:
            print("\n" + docs[int(key) - 1].read_text(errors="replace"))
            wait_for_enter()
            return
        if dispatch_utility(key):
            continue
        invalid_selection(key, ["8", "0", "F1", "F3", "F5"])
        wait_for_enter()


def about_screen() -> None:
    render_standard_screen(
        "About",
        APP_FULL_NAME,
        about_rows(),
        [],
        ["8. Back", "0. Exit"],
        ["F1. Settings", "F2. Documentation", "F5. Help"],
    )

    while True:
        key = get_key()
        if key == "8":
            return
        if key == "0":
            raise SystemExit(0)
        if dispatch_utility(key):
            continue
        invalid_selection(key, ["8", "0", "F1", "F2", "F5"])
        wait_for_enter()


def logs_screen() -> None:
    points = recovery_points()
    newest = points[-1] if points else None
    log_dir = newest / "logs" if newest else None
    logs = sorted(log_dir.glob("*")) if log_dir and log_dir.is_dir() else []

    render_standard_screen(
        "Logs",
        "Latest Recovery Point Logs",
        [
            ("Recovery Point", newest.name if newest else "None"),
            ("Log Files", str(len(logs))),
        ],
        [f"{i}. {log.name}" for i, log in enumerate(logs[:6], 1)],
        ["8. Back", "9. Refresh", "0. Exit"],
        ["F1. Settings", "F2. Documentation", "F3. About", "F5. Help"],
    )

    while True:
        key = get_key()
        if key == "8":
            return
        if key == "9":
            return logs_screen()
        if key == "0":
            raise SystemExit(0)
        if key in {str(i) for i in range(1, len(logs[:6]) + 1)}:
            print("\n" + logs[int(key) - 1].read_text(errors="replace"))
            wait_for_enter()
            return
        if dispatch_utility(key):
            continue
        invalid_selection(key, ["8", "9", "0", "F1", "F2", "F3", "F5"])
        wait_for_enter()


def help_screen() -> None:
    render_standard_screen(
        "Help",
        "Navigation Reference",
        [
            ("1–6", "Screen-specific operations"),
            ("7", "Next"),
            ("8", "Back"),
            ("9", "Refresh"),
            ("0", "Exit or explicitly labeled Cancel"),
            ("F1–F5 / F10", "Global utilities"),
        ],
        [],
        ["8. Back", "0. Exit"],
        ["F1. Settings", "F2. Documentation", "F3. About", "F4. Logs"],
    )

    while True:
        key = get_key()
        if key == "8":
            return
        if key == "0":
            raise SystemExit(0)
        if dispatch_utility(key):
            continue
        invalid_selection(key, ["8", "0", "F1", "F2", "F3", "F4"])
        wait_for_enter()

"""CBART application controller."""

from __future__ import annotations

import subprocess

from .keyboard import wait_for_enter
from .screens import main_menu
from .validation import validate_environment


def main() -> int:
    if not validate_environment():
        return 1

    try:
        main_menu()
        print("\nExiting CBART.")
        return 0

    except KeyboardInterrupt:
        print("\nCBART interrupted. Terminal state restored.")
        return 130

    except subprocess.CalledProcessError as exc:
        print(f"\nCommand failed with exit code {exc.returncode}.")
        wait_for_enter()
        return exc.returncode or 1

    except SystemExit as exc:
        return int(exc.code or 0)

    except Exception as exc:
        print(f"\nCBART error: {exc}")
        wait_for_enter()
        return 1

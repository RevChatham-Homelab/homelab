"""Standards-compliant CBART terminal rendering."""

from __future__ import annotations

from collections.abc import Iterable

from .config import WIDTH


HEAVY = "="
LIGHT = "─"


def clear_screen() -> None:
    """Clear the terminal when attached to an interactive session."""
    print("\033[2J\033[H", end="")


def centered(text: str) -> str:
    return text.center(WIDTH)


def title_block(*lines: str) -> None:
    print(HEAVY * WIDTH)
    for line in lines:
        print(centered(line))
    print(HEAVY * WIDTH)


def boxed_status(title: str, rows: Iterable[tuple[str, str]]) -> None:
    inner = WIDTH - 2
    print("+" + "-" * inner + "+")
    print("|" + title.center(inner) + "|")
    print("+" + "-" * inner + "+")
    print()

    for label, value in rows:
        print(label)
        print(f"    {value}")
        print()


def section(title: str, options: Iterable[str]) -> None:
    options = list(options)

    if not options:
        return

    print(LIGHT * WIDTH)
    print(centered(title))
    print(LIGHT * WIDTH)
    print()

    for option in options:
        print(option)

    print()


def invalid_selection(key: str, valid: Iterable[str]) -> None:
    allowed = ", ".join(valid)
    shown = key if key else "<empty>"
    print(f"Invalid selection: {shown}")
    print()
    print(f"Valid selections: {allowed}")

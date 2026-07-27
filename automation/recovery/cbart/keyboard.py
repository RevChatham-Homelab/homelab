"""Portable terminal keyboard handling for CBART.

Supports immediate numeric selections, typed function labels, and common
physical function-key escape sequences over SSH and Linux terminals.
"""

from __future__ import annotations

import os
import os
import select
import sys
import termios
import tty
from contextlib import contextmanager


FUNCTION_KEYS = {
    "\x1bOP": "F1",
    "\x1bOQ": "F2",
    "\x1bOR": "F3",
    "\x1bOS": "F4",
    "\x1b[15~": "F5",
    "\x1b[17~": "F6",
    "\x1b[18~": "F7",
    "\x1b[19~": "F8",
    "\x1b[20~": "F9",
    "\x1b[21~": "F10",
    "\x1b[[A": "F1",
    "\x1b[[B": "F2",
    "\x1b[[C": "F3",
    "\x1b[[D": "F4",
    "\x1b[[E": "F5",
}


@contextmanager
def raw_terminal():
    """Temporarily place stdin in raw mode and always restore it."""
    if not sys.stdin.isatty():
        yield
        return

    fd = sys.stdin.fileno()
    original = termios.tcgetattr(fd)

    try:
        tty.setraw(fd)
        yield
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, original)


def normalize_key(value: str) -> str:
    """Normalize operator input to CBART logical key names."""
    return value.strip().upper()


def _read_escape_sequence(fd: int) -> str:
    sequence = "\x1b"

    while len(sequence) < 8:
        readable, _, _ = select.select([sys.stdin], [], [], 0.05)

        if not readable:
            break

        sequence += os.read(fd, 1).decode(errors='ignore')

        if sequence in FUNCTION_KEYS:
            return FUNCTION_KEYS[sequence]

    return FUNCTION_KEYS.get(sequence, "")


def _read_typed_function_key() -> str:
    sys.stdout.write("F")
    sys.stdout.flush()

    digits = ""

    while True:
        char = sys.stdin.read(1)

        if char in "\r\n":
            sys.stdout.write("\n")
            sys.stdout.flush()
            key = normalize_key("F" + digits)
            return key if key in {f"F{i}" for i in range(1, 11)} else ""

        if char.isdigit() and len(digits) < 2:
            digits += char
            sys.stdout.write(char)
            sys.stdout.flush()
            continue

        sys.stdout.write("\n")
        sys.stdout.flush()
        return ""


def _read_tty_key() -> str:
    """Read one logical key from an interactive terminal."""
    fd = sys.stdin.fileno()
    fd = sys.stdin.fileno()
    with raw_terminal():
        first = os.read(fd,1).decode(errors='ignore')

        if first in "0123456789":
            sys.stdout.write(first + "\n")
            sys.stdout.flush()
            return first

        if first == "\x1b":
            key = _read_escape_sequence(fd)
            sys.stdout.write((key or "") + "\n")
            sys.stdout.flush()
            return key

        if first in {"f", "F"}:
            return _read_typed_function_key()

        if first == "\x03":
            raise KeyboardInterrupt

        sys.stdout.write("\n")
        sys.stdout.flush()
        return normalize_key(first)


def get_key(prompt: str = "Selection: ") -> str:
    """Read and normalize one CBART logical key."""
    sys.stdout.write(prompt)
    sys.stdout.flush()

    if sys.stdin.isatty():
        return _read_tty_key()

    return normalize_key(sys.stdin.readline())


def wait_for_enter(message: str = "Press Enter to continue...") -> None:
    """Pause without depending on raw-mode input."""
    input(f"\n{message}")

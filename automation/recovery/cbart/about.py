"""About-screen content."""

from __future__ import annotations

from . import APP_FULL_NAME, APP_NAME, APP_VERSION
from .config import REPO_ROOT


def about_rows() -> list[tuple[str, str]]:
    return [
        ("Product", APP_NAME),
        ("Name", APP_FULL_NAME),
        ("Version", APP_VERSION),
        ("Project", "RevChatham Homelab"),
        ("Repository", str(REPO_ROOT)),
        ("License", "See repository LICENSE"),
        ("Release", "Standards-compliant terminal application"),
    ]

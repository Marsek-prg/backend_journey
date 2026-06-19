"""Paths that work from source code and from a PyInstaller bundle."""

import os
import sys
from pathlib import Path


APP_DATA_DIR_NAME = "TaskTracker"
DATA_DIR_ENV_VAR = "TASK_TRACKER_DATA_DIR"


def get_application_root() -> Path:
    """Return the root containing bundled application resources."""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parents[2]


def get_templates_dir() -> Path:
    return get_application_root() / "app" / "templates"


def get_static_dir() -> Path:
    return get_application_root() / "app" / "static"


def get_user_data_dir() -> Path:
    """Return a writable, persistent directory for local user data."""
    configured_data_dir = os.environ.get(DATA_DIR_ENV_VAR)
    if configured_data_dir:
        return Path(configured_data_dir).expanduser()

    appdata = os.environ.get("APPDATA")
    base_dir = Path(appdata) if appdata else Path.home() / ".local" / "share"
    return base_dir / APP_DATA_DIR_NAME

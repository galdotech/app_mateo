#!/usr/bin/env python3
"""Project health checks."""
from __future__ import annotations

import glob
import importlib
import os
import sys
from typing import List

ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, ROOT)


PACKAGES = [
    os.path.join(ROOT, "app"),
    os.path.join(ROOT, "app", "ui"),
    os.path.join(ROOT, "app", "views"),
    os.path.join(ROOT, "app", "data"),
]

UI_GLOB = os.path.join(ROOT, "app", "ui", "*.ui")


def _check_inits() -> List[str]:
    missing = []
    for path in PACKAGES:
        if not os.path.isfile(os.path.join(path, "__init__.py")):
            missing.append(os.path.relpath(path, ROOT))
    return missing


def _check_ui_compiled() -> List[str]:
    missing = []
    for ui in glob.glob(UI_GLOB):
        base = os.path.splitext(os.path.basename(ui))[0]
        py = os.path.join(os.path.dirname(ui), f"ui_{base}.py")
        if not os.path.isfile(py):
            missing.append(os.path.relpath(py, ROOT))
    return missing


def _check_imports() -> List[str]:
    problems = []
    for mod in ("app.ui.ui_main_window", "app.views.main_window"):
        try:
            importlib.import_module(mod)
        except Exception as exc:
            problems.append(f"import {mod}: {exc}")
    return problems


def _check_db() -> str | None:
    try:
        from app.data import db
        db.init_db(":memory:")
    except Exception as exc:
        return str(exc)
    return None


def main() -> int:
    issues: List[str] = []
    missing_inits = _check_inits()
    if missing_inits:
        issues.append("Missing __init__.py in: " + ", ".join(missing_inits))
    missing_ui = _check_ui_compiled()
    if missing_ui:
        issues.append("Missing compiled UI files: " + ", ".join(missing_ui))
    issues.extend(_check_imports())
    db_err = _check_db()
    if db_err:
        issues.append(f"db.init_db() error: {db_err}")

    if issues:
        print("Doctor found issues:")
        for item in issues:
            print(" -", item)
        return 1
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

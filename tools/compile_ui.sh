#!/usr/bin/env bash
# Compile all Qt Designer .ui files into Python modules.
set -euo pipefail
for ui in app/ui/*.ui; do
    base=$(basename "$ui" .ui)
    pyside6-uic "$ui" -o "app/ui/ui_${base}.py"
done

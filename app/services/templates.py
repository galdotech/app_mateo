from __future__ import annotations

import json
from pathlib import Path
from string import Template
from typing import Dict

TEMPLATES_FILE = Path(__file__).with_name("message_templates.json")


def load_templates() -> Dict[str, str]:
    if TEMPLATES_FILE.exists():
        with open(TEMPLATES_FILE, "r", encoding="utf-8") as fh:
            return json.load(fh)
    return {}


def render_template(name: str, context: Dict[str, object]) -> str:
    templates = load_templates()
    template_str = templates.get(name, "")
    return Template(template_str).safe_substitute(context)

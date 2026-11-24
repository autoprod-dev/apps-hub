#!/usr/bin/env python3
"""Copy programs.json into the inlined block in index.html so the page also works from a file."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
JSON_PATH = ROOT / "programs.json"
HTML_PATH = ROOT / "index.html"
PATTERN = re.compile(
    r'(<script type="application/json" id="programs-data">)(.*?)(</script>)',
    re.DOTALL,
)


def main() -> None:
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    if "programs" not in data or not isinstance(data["programs"], list):
        raise SystemExit("programs.json must have a top-level 'programs' array")
    for i, item in enumerate(data["programs"], 1):
        for key in ("id", "name", "description", "status"):
            if key not in item or not str(item.get(key) or "").strip():
                raise SystemExit(f"Program {i} is missing '{key}'")
        if item["status"] not in ("Live", "Test", "Prototype"):
            raise SystemExit(
                f"{item['name']}: status must be Live, Test or Prototype (got {item['status']!r})"
            )
    payload = json.dumps(data, ensure_ascii=False, indent=2)
    html = HTML_PATH.read_text(encoding="utf-8")
    if not PATTERN.search(html):
        raise SystemExit("Could not find the programs-data script tag in index.html")
    HTML_PATH.write_text(PATTERN.sub(rf"\1{payload}\3", html, count=1), encoding="utf-8")
    print(f"Synced {len(data['programs'])} programs into index.html")


if __name__ == "__main__":
    main()

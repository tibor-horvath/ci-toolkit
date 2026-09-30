"""Fail when the README or docs/ drift from the reusable workflows.

For every workflow that exposes `workflow_call`:
  * README.md must mention its filename;
  * docs/<name>.md must exist;
  * that page must mention every declared input, secret and output by name.
"""
import pathlib
import sys

import yaml

root = pathlib.Path(".")
readme = (root / "README.md").read_text(encoding="utf-8")
errors = []

for wf in sorted((root / ".github" / "workflows").glob("*.yml")):
    data = yaml.safe_load(wf.read_text(encoding="utf-8"))
    # PyYAML follows YAML 1.1, where the bare key `on` parses as boolean True.
    triggers = data.get("on", data.get(True))
    call = triggers.get("workflow_call") if isinstance(triggers, dict) else None
    if call is None:
        continue

    if wf.name not in readme:
        errors.append(f"README.md does not mention {wf.name}")

    page = root / "docs" / f"{wf.stem}.md"
    if not page.is_file():
        errors.append(f"{wf.name}: missing docs page {page}")
        continue
    text = page.read_text(encoding="utf-8")

    for kind in ("inputs", "secrets", "outputs"):
        for name in (call.get(kind) or {}):
            if name not in text:
                errors.append(f"{page}: {kind[:-1]} `{name}` of {wf.name} is not documented")

for e in errors:
    print(f"::error::{e}")
print(f"{len(errors)} problem(s)")
sys.exit(1 if errors else 0)

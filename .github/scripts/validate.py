#!/usr/bin/env python3
"""Documentation checks for this repository (run locally and in CI).

- Every skill's SKILL.md has valid frontmatter: name matching its folder, a description, known keys.
- Relative Markdown links resolve to an existing file (templates are skipped: their links are
  relative to the repository they get copied into).
- Every YAML and JSON file parses.
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
SKILL_KEYS = {"name", "description", "context", "agent", "disable-model-invocation", "allowed-tools",
              "argument-hint", "user-invocable"}
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
errors: list[str] = []


def versioned_files() -> list[Path]:
    out = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard"],
                         cwd=ROOT, check=True, capture_output=True, text=True).stdout
    return [ROOT / line for line in out.splitlines() if (ROOT / line).is_file()]


def check_skill(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        errors.append(f"{path}: missing YAML frontmatter")
        return
    meta = yaml.safe_load(match.group(1)) or {}
    if meta.get("name") != path.parent.name:
        errors.append(f"{path}: name '{meta.get('name')}' does not match folder '{path.parent.name}'")
    description = meta.get("description") or ""
    if not description.strip():
        errors.append(f"{path}: empty description")
    elif len(description) > 1024:
        errors.append(f"{path}: description longer than 1024 characters")
    for key in set(meta) - SKILL_KEYS:
        errors.append(f"{path}: unknown frontmatter key '{key}'")


def check_links(path: Path) -> None:
    text = re.sub(r"```.*?```", "", path.read_text(encoding="utf-8"), flags=re.DOTALL)
    for target in LINK.findall(text):
        if re.match(r"^[a-z]+:", target) or target.startswith("#") or any(c in target for c in "<{") \
                or "NNNN" in target:  # placeholders
            continue
        file_part = target.split("#", 1)[0]
        if file_part and not (path.parent / file_part).exists():
            errors.append(f"{path}: broken link '{target}'")


def main() -> int:
    for path in versioned_files():
        rel = path.relative_to(ROOT).as_posix()
        if path.name == "SKILL.md":
            check_skill(path)
        if path.suffix == ".md" and "/templates/" not in rel:
            check_links(path)
        try:
            if path.suffix in {".yml", ".yaml"}:
                yaml.safe_load(path.read_text(encoding="utf-8"))
            elif path.suffix == ".json":
                json.loads(path.read_text(encoding="utf-8"))
        except (yaml.YAMLError, json.JSONDecodeError) as error:
            errors.append(f"{path}: invalid {path.suffix[1:].upper()}: {error}")
    for error in errors:
        print(f"::error::{error}" if "GITHUB_ACTIONS" in os.environ else error)
    print(f"validate: {len(errors)} error(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

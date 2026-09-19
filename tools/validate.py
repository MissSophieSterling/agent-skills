#!/usr/bin/env python3
"""Check every skill in skills/ before it ships.

    python3 tools/validate.py

For each skills/<folder>/SKILL.md:
  - YAML frontmatter with `name` and `description` (Agent Skills spec: agentskills.io/specification)
  - name: 1-64 chars of a-z, 0-9 and single hyphens, identical to the folder name
  - description: 1-1024 chars, one line; unquoted values may not contain ": " or " #"
  - body: under 500 lines
  - every references/..., scripts/... or assets/... path the body mentions exists
Then: the umbrella's bundled copies are current (tools/bundle.py --check).

Exit 0 = clean, 1 = problems (listed). Standard library only; Python 3.9+.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
PATH_RE = re.compile(r"(?<![\w/.-])((?:references|scripts|assets)/[\w.-]+(?:/[\w.-]+)*)")
YAML_SPECIAL_START = tuple("[]{}>|*&!%@`,?-")
# Claude Code refuses these marketplace names (code.claude.com/docs/en/plugin-marketplaces, 2026-09-19).
RESERVED_MARKETPLACE_NAMES = {
    "claude-code-marketplace", "claude-code-plugins", "claude-plugins-official", "claude-plugins-community",
    "claude-community", "anthropic-marketplace", "anthropic-plugins", "agent-skills", "anthropic-agent-skills",
    "knowledge-work-plugins", "life-sciences", "claude-for-legal", "claude-for-financial-services",
    "financial-services-plugins", "first-party-plugins", "claude-tag-plugins", "healthcare",
    "npm", "pip", "uv", "cargo", "github", "gh", "org", "org-provisioned", "unknown",
}


def parse_frontmatter(text):
    """Return (fields, body, problems). Handles flat `key: value` plus one level of nesting."""
    problems = []
    if not text.startswith("---\n"):
        return {}, text, ["no frontmatter (file must start with ---)"]
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}, text, ["frontmatter is not closed with ---"]
    head, body = text[4:end], text[end + 5:]
    fields, parent = {}, None
    for line in head.splitlines():
        if not line.strip():
            continue
        nested = line.startswith("  ")
        key, sep, value = line.strip().partition(":")
        if not sep or key != key.strip() or " " in key:
            problems.append(f"unreadable frontmatter line: {line!r}")
            continue
        value = value.strip()
        if nested:
            if parent is None:
                problems.append(f"indented line without a parent key: {line!r}")
                continue
            target = fields[parent]
        else:
            target, parent = fields, None
            if value == "":
                fields[key] = {}
                parent = key
                continue
        if value[:1] in ("'", '"'):
            if len(value) < 2 or value[-1] != value[0]:
                problems.append(f"{key}: unterminated quoted value")
            value = value[1:-1]
        elif ": " in value or " #" in value or value.startswith(YAML_SPECIAL_START):
            problems.append(f"{key}: quote this value, it contains YAML-special characters")
        target[key] = value
    return fields, body, problems


def check_skill(folder):
    errors = []
    skill_md = folder / "SKILL.md"
    if not skill_md.is_file():
        return [f"{folder.name}: missing SKILL.md"]
    text = skill_md.read_text(encoding="utf-8")
    fields, body, problems = parse_frontmatter(text)
    errors += [f"{folder.name}: {p}" for p in problems]

    name = fields.get("name")
    if not isinstance(name, str) or not name:
        errors.append(f"{folder.name}: frontmatter has no name")
    else:
        if name != folder.name:
            errors.append(f"{folder.name}: name '{name}' does not match the folder name")
        if len(name) > 64 or not NAME_RE.match(name):
            errors.append(f"{folder.name}: name must be 1-64 chars of a-z, 0-9 and single hyphens")

    desc = fields.get("description")
    if not isinstance(desc, str) or not desc.strip():
        errors.append(f"{folder.name}: frontmatter has no description")
    elif len(desc) > 1024:
        errors.append(f"{folder.name}: description is {len(desc)} chars (max 1024)")

    lines = body.count("\n") + 1
    if lines >= 500:
        errors.append(f"{folder.name}: body is {lines} lines (keep it under 500)")

    for rel in sorted(set(PATH_RE.findall(body))):
        rel = rel.rstrip(".")
        if not (folder / rel).exists():
            errors.append(f"{folder.name}: mentions {rel}, which does not exist")

    # Cross-check with a real YAML parser when one is installed.
    try:
        import yaml  # noqa: WPS433 (optional)
    except ImportError:
        yaml = None
    if yaml is not None:
        try:
            parsed = yaml.safe_load(text[4:text.find("\n---\n", 4)])
            if not isinstance(parsed, dict) or parsed.get("name") != name or parsed.get("description") != desc:
                errors.append(f"{folder.name}: a YAML parser reads the frontmatter differently")
        except Exception as exc:  # pragma: no cover
            errors.append(f"{folder.name}: YAML parser error: {exc}")
    return errors


def main():
    folders = sorted(p for p in SKILLS.iterdir() if p.is_dir())
    if not folders:
        print("no skills found under skills/")
        return 1
    errors = []
    for folder in folders:
        errors += check_skill(folder)
    marketplace = ROOT / ".claude-plugin" / "marketplace.json"
    if marketplace.is_file():
        mp_name = json.loads(marketplace.read_text(encoding="utf-8")).get("name", "")
        if mp_name.lower() in RESERVED_MARKETPLACE_NAMES:
            errors.append(f"marketplace name '{mp_name}' is reserved by Claude Code; pick another")
    bundle = subprocess.run([sys.executable, str(ROOT / "tools" / "bundle.py"), "--check"],
                            capture_output=True, text=True)
    if bundle.returncode != 0:
        errors.append(bundle.stdout.strip() or bundle.stderr.strip())
    for e in errors:
        print("FAIL", e)
    print(f"{len(folders)} skills checked, {len(errors)} problem(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

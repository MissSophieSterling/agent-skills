#!/usr/bin/env python3
"""Keep the umbrella skill self-contained: copy each tactic skill into skills/token-saver/references/.

    python3 tools/bundle.py          # rewrite the bundled copies
    python3 tools/bundle.py --check  # exit 1 if any copy is stale (validate.py and CI run this)

Edit the tactic skills themselves (skills/<name>/SKILL.md), never the copies.
Standard library only; Python 3.9+.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
UMBRELLA = SKILLS / "token-saver" / "references"

# Order = the order the umbrella skill lists them in.
TACTICS = [
    "pinpoint",
    "usage-budget",
    "context-audit",
    "cheap-subagents",
    "quiet-tools",
    "short-answers",
    "progress-ledger",
    "skillify",
    "workflow-optimizer",
    "limit-window-warmup",
]


def body_of(name):
    text = (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise SystemExit(f"{name}: SKILL.md has no frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise SystemExit(f"{name}: frontmatter is not closed")
    return text[end + 5:].lstrip("\n")


def rendered(name):
    note = (f"<!-- Copy of skills/{name}/SKILL.md, made by tools/bundle.py. "
            "Edit the original and re-run the script. -->\n\n")
    return note + body_of(name)


def main(check):
    stale = []
    UMBRELLA.mkdir(parents=True, exist_ok=True)
    wanted = {f"{n}.md" for n in TACTICS}
    for extra in sorted(p.name for p in UMBRELLA.glob("*.md") if p.name not in wanted):
        stale.append(f"references/{extra} is not a tactic skill")
        if not check:
            (UMBRELLA / extra).unlink()
    for name in TACTICS:
        target = UMBRELLA / f"{name}.md"
        new = rendered(name)
        old = target.read_text(encoding="utf-8") if target.exists() else None
        if old != new:
            stale.append(f"references/{name}.md")
            if not check:
                target.write_text(new, encoding="utf-8")
    if check and stale:
        print("bundle out of date (run python3 tools/bundle.py):")
        for s in stale:
            print("  -", s)
        return 1
    if not check:
        print(f"bundle: {len(stale)} file(s) updated, {len(TACTICS) - len(stale)} already current")
    return 0


if __name__ == "__main__":
    sys.exit(main("--check" in sys.argv[1:]))

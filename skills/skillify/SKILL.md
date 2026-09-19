---
name: skillify
description: Turn a workflow that just worked into a reusable Agent Skill (a SKILL.md folder). Use when the user says "turn this into a skill", "save this workflow" or "make this repeatable", or when the same multi-step job has now been done twice.
license: MIT
metadata:
  author: Sophie Sterling
  version: "1.1"
---

# Skillify

The first run of a workflow is the expensive one: the agent explores, guesses, fails, retries, and finally lands on the steps that work. Every later run can skip all of that if the working path is written down as a skill. Skills stay cheap while they sit unused: hosts that follow the Agent Skills format load only each skill's name and description at the start, and open the body when the task calls for it. But every installed skill still adds its description to every session, so write tight ones and delete the ones you stop using.

## 1. Harvest what worked

From the session, collect:

- the goal, and the inputs that change from run to run (file names, dates, recipients)
- the steps in order, with the exact commands, prompts and settings that succeeded
- the checks that proved it worked
- the traps you hit, and the fix for each
- the output format

Leave out the dead ends, except as one-line "don't do X, because Y" traps.

## 2. Script or prose?

- Deterministic, repeated, easy to get wrong by retyping (renaming files, packaging, building archives, calling an API with fixed parameters) → a script in `scripts/`. The model runs it without regenerating or re-reading the code, which saves tokens every run.
- Judgment (writing, deciding, reviewing) → prose instructions.

## 3. Write the SKILL.md

```markdown
---
name: kebab-case-name
description: What it does and when to use it, including the words a user would actually say. 1-1024 characters.
---

# Title

One paragraph: what this produces, and why the steps come in this order.

## Inputs
## Steps
1. ...
## Check before finishing
- [ ] ...
## Traps
- ...
```

- `name`: 1–64 characters, lowercase letters, digits and single hyphens, identical to the folder name.
- The description does the triggering. Name the task, the inputs and the phrases users type. A vague one never fires; an over-broad one fires on everything.
- Keep the body well under 500 lines. Long reference material goes in `references/`, with a line saying when to read it.
- Put the reason next to any rule that looks arbitrary. Models follow reasons better than orders.
- No secrets, tokens, personal paths or client names. Anything user-specific becomes an input.

## 4. Install it where the host looks

| Host | Personal | Project |
|---|---|---|
| Claude Code | `~/.claude/skills/<name>/` | `.claude/skills/<name>/` |
| Codex | `~/.agents/skills/<name>/` | `.agents/skills/<name>/` |
| Gemini CLI | `~/.gemini/skills/<name>/` or `~/.agents/skills/<name>/` | `.agents/skills/<name>/` |
| Cursor, GitHub Copilot, OpenCode and others | see the host's docs | `.agents/skills/<name>/` |

A skill published in a Git repo can be installed into most of these hosts with `npx skills add <owner>/<repo>`.

## 5. Prove it

Open a fresh session and give a realistic request without naming the skill. Check that it triggers and that the output passes the skill's own checks. If it doesn't trigger, sharpen the description. If it goes wrong, fix the step that failed, not the one example.

## Before you finish

- [ ] Frontmatter has `name` (same as the folder) and a specific `description`.
- [ ] Every command in the skill was run once for real before saving it.
- [ ] No secrets or personal details in any file.
- [ ] A fresh-session test triggered it.

---
Part of [agent-skills](https://github.com/MissSophieSterling/agent-skills) · MIT · improvements welcome as issues.

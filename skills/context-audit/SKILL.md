---
name: context-audit
description: Measure and trim what loads before the first message (AGENTS.md, CLAUDE.md or GEMINI.md, memory, installed skills, MCP servers, plugins). Use when context is already full at session start, limits run out faster than expected, the user asks to clean up instruction files, skills or MCP servers, or as a monthly checkup.
license: MIT
metadata:
  author: Sophie Sterling
  version: "1.1"
---

# Context audit

Whatever loads at session start is paid for on every turn of every session. A bloated instruction file, plugins installed for a one-off job, MCP servers nobody has used in weeks: they all eat context before anyone types a word. Once a month, measure it and cut what doesn't earn its place.

## 1. Measure, in a fresh session, before any work

| Host | What to run | What it shows |
|---|---|---|
| Claude Code | `/context` | tokens by category: system, tools, MCP, memory files, skills, messages |
| Codex | `/status` | token usage and remaining context |
| Codex | `codex debug prompt-input` | the exact input the model sees (experimental) |
| Gemini CLI | `/memory show`, `/stats` | the loaded GEMINI.md text; session token use |

Write the number down. That's the fixed cost of every turn.

## 2. Inventory

```
# instruction files and their size (roughly 4 characters per token; newer Claude tokenizers count about 30% more)
wc -c ~/.claude/CLAUDE.md ~/.codex/AGENTS.md ~/.codex/AGENTS.override.md ~/.gemini/GEMINI.md CLAUDE.md CLAUDE.local.md .claude/CLAUDE.md AGENTS.md AGENTS.override.md GEMINI.md 2>/dev/null
# installed skills
ls ~/.claude/skills ~/.agents/skills ~/.gemini/skills .claude/skills .agents/skills .gemini/skills 2>/dev/null
```

Then list the MCP servers (`/mcp` in all three), plugins or extensions and the skills they bring (`/plugin` in Claude Code), and features switched on (web search, image generation).

## 3. Sort every item: keep, move or cut

- **Keep**: rules that prevent expensive mistakes, and facts the agent can't discover by itself (build and test commands, conventions, where things live).
- **Move to on-demand**: long procedures, reference tables, style guides. Put them in a skill or a doc, and leave one line in the instruction file saying where they are.
- **Cut**: duplicates, rules the agent follows anyway, outdated facts, contradictions, generic "be helpful" text, and plugins or servers unused in the last month.

Guide rails:

- Anthropic suggests keeping CLAUDE.md under about 200 lines.
- Codex stops reading AGENTS.md files once their combined size passes `project_doc_max_bytes` (32 KiB by default) and leaves out the rest (a GitHub issue reports no warning in the TUI when that happens).
- Skill lists are budgeted too. Codex caps the list at about 2% of the context window and shortens descriptions when there are too many, which makes skill selection worse. Uninstall skills you don't use.
- Instructions written for older models ("always read X before editing", "always run the tests") may be dead weight on a newer model that already does it. OpenAI's own launch advice for GPT-6 Astra was to remove that kind of scaffolding. Try the task without the rule before keeping it.
- CLI tools (`gh`, `aws`, `gcloud`) usually cost less context than an MCP server for the same job, because they add no tool listing.

## 4. Propose, then apply

Show a diff of the instruction-file changes and the list of servers and plugins to disable. Apply only what the user approves: these files hold someone's preferences.

A prompt users can reuse:

```
Read my AGENTS.md (or CLAUDE.md) and my installed skills. List anything repeated, stale, or making easy jobs harder than they need to be, and show me the edits you'd make before changing anything.
```

## 5. Re-measure and report

Tokens at session start before and after, what moved where, and what was disabled.

## Corrections the user keeps making

When the user corrects the same thing a second time, propose one line for the right file: the personal one for personal preferences, the project one for project facts. Re-teaching the same rule in every session is the most avoidable cost there is.

## Don't

- Don't cut a rule just to hit a number. A missing rule that causes one bad run costs more than it saved.
- Don't switch MCP servers or tools on or off in the middle of a task. On Claude Code, changing the tool set can invalidate the prompt cache, so do it between sessions.
- Don't assume an idle server is free. Claude Code defers MCP tool definitions by default, but tool names and server instructions still load.

## Before you finish

- [ ] Before and after numbers come from the host's own meter.
- [ ] Every cut is listed, and nothing was removed without approval.
- [ ] Moved content is still reachable: the pointer line and the target file both exist.

---
Part of [agent-skills](https://github.com/MissSophieSterling/agent-skills) · MIT · improvements welcome as issues.

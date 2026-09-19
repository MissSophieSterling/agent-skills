<!-- Copy of skills/short-answers/SKILL.md, made by tools/bundle.py. Edit the original and re-run the script. -->

# Short answers

Output tokens are the priciest tokens: on current Claude models output costs five times as much as input, and other vendors price it in the same direction. A token is about three quarters of an English word, so a 100-word reply is roughly 130 tokens (about 30% more on newer Claude tokenizers). In agent sessions, though, output is usually the smaller part of the bill (the context re-read on every turn is the big one), so this skill trims real waste but doesn't replace the context habits in `quiet-tools` and `context-audit`.

## Rules

- Lead with the result or the answer. No preamble, no restating the request, no "I'll now…".
- For a code change: what changed and where (`file:line`), plus one line of why if it isn't obvious. Don't narrate the diff.
- No closing recap, no "let me know if…", no menu of optional extras.
- Lists only when they save words; tables only when comparing.
- Keep exact values, commands, paths and error text. Short never means vague.
- Expand when asked, when the user has to decide something, or when there's a risk they need to know about.
- Plain words over shorthand. Caveman-style grammar ("why use many token") trims a little more, but an independent test on real agent work measured only single-digit savings, because code and tool calls dominate the output. Use it only if the user asks for it.

## Reasoning is output too

Hidden reasoning is billed as output. For mechanical work, a lower reasoning effort saves more than trimming the visible reply:

- Claude Code: `/effort low` (up to `max`) for the session.
- Codex: the effort picker in `/model`, or `model_reasoning_effort` in `~/.codex/config.toml`.
- OpenAI API: `reasoning.effort`, plus `text.verbosity` (`low`, `medium`, `high`) for the length of the visible answer.

Changing effort or model partway through a session can throw away the prompt cache on some hosts (Claude Code documents this), so pick it at the start.

## Make it permanent

One line for the instruction file (AGENTS.md, CLAUDE.md or GEMINI.md):

```
Keep responses as short as the task allows: lead with the result, skip preamble, recaps and closing offers, and expand only when asked.
```

Claude Code also ships a built-in style for this: `/output-style concise`. It leads with the result, skips narration, and still keeps error reports, security warnings and confirmations for destructive actions complete.

Codex already defaults its current models to low verbosity. `model_verbosity = "low"` in `~/.codex/config.toml` sets it explicitly (it applies to Responses-API providers).

## Before you finish

- [ ] The first sentence answers the question or states the result.
- [ ] No sentence only restates, previews or offers.
- [ ] Every command, path and error the user needs is still there.

---
Part of [agent-skills](https://github.com/MissSophieSterling/agent-skills) · MIT · improvements welcome as issues.

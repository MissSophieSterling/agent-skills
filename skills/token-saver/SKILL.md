---
name: token-saver
description: Full playbook for making an AI coding agent's plan usage last longer on any model. Covers pinpointed prompts, budgets, lean context, cheap subagents, quiet tools, short answers, progress files, skills, cost experiments and window timing. Use at the start of heavy agent sessions, or when the user hits or worries about Claude Code, Codex or Gemini CLI usage limits.
license: MIT
metadata:
  author: Sophie Sterling
  version: "1.1"
---

# Token saver

Ten tactics, one skill. Each one also exists as a standalone skill; full copies of all ten are in `references/`, so this skill works on its own. When one of them says to see another skill by name, open `references/<that-name>.md`.

## Where the tokens go

A rule of thumb for a typical agent session, biggest first:

1. **The context, re-read every turn**: instructions, tool definitions, the conversation, every tool result so far. Prompt caching discounts the re-read, but it's still most of the bill.
2. **Exploration**: searches and file reads that happen because the agent doesn't know where to look.
3. **Rework**: wrong runs that finish anyway, retries, work redone after a crash.
4. **Output**: replies plus hidden reasoning. The priciest per token, usually the smaller total.

Model choice multiplies all four: the same work on a cheaper model costs a fraction.

## Start of a session

1. Look at the meter: Claude Code `/usage` and `/context`, Codex `/status`, Gemini CLI `/stats`.
2. Pin the task down (where, observed, expected, done-when): `references/pinpoint.md`.
3. Plan tight? Set a budget with checkpoints: `references/usage-budget.md`.
4. Long job, many items or several sessions? Open a ledger: `references/progress-ledger.md`.
5. Big or parallel job? Plan cheap subagents with a cap: `references/cheap-subagents.md`.

## While working

- Quiet tools, full failures: `references/quiet-tools.md`.
- Short answers: `references/short-answers.md`.
- Wrong direction? Interrupt early. Tokens already spent don't come back, but the next ones don't have to be spent. Claude Code: `Esc` stops the turn and keeps the work so far (a message typed while it works waits in a queue). Codex CLI: `Enter` steers mid-run, `Tab` queues; in the app it's Settings → General → Follow-up behavior. Gemini CLI: experimental model steering (`/settings`, Model Steering).
- Pick the model and the effort at the start. Switching mid-session can throw away the prompt cache (Claude Code documents this for model, effort and tool-set changes).
- Unrelated next task? Start a fresh conversation (`/clear` in Claude Code, `/new` in Codex) instead of dragging the old context along.
- Image generation is expensive: in Codex it uses limits 3–5 times faster on average than a normal turn.

## After

- Did the same workflow twice? `references/skillify.md`.
- Runs every week? Measure it and make it cheaper: `references/workflow-optimizer.md`.
- Once a month: audit what loads at startup: `references/context-audit.md`.
- Running out every morning? Shift the 5-hour window: `references/limit-window-warmup.md`.

## House rules to paste into AGENTS.md, CLAUDE.md or GEMINI.md

These five lines are about 150 tokens of always-loaded instructions. Habits that apply to every task work better here than as skills, which only load when a task matches them:

```
## Token discipline
- Before searching, confirm where (file, route, screen) and what "done" looks like; ask one short question if it's unclear.
- Use quiet flags; summarize successes in one line; show full detail only for failures, with the real exit code.
- Keep replies as short as the task allows: lead with the result, no preamble or recap.
- For work longer than about 30 minutes or across many items, keep PROGRESS.md (done / where / failed / next).
- Delegate mechanical, parallel work to a cheaper model with a spawn cap; review, don't redo.
```

## Per tool

| | Claude Code | Codex | Gemini CLI |
|---|---|---|---|
| Plan usage | `/usage` | `/status`, `/usage` | `/stats model` |
| Context use | `/context` | `/status`, `codex debug prompt-input` | `/stats`, `/memory show` |
| Instructions | `CLAUDE.md` (reads `AGENTS.md` only when there's no CLAUDE.md) | `AGENTS.md`; personal one at `~/.codex/AGENTS.md` | `GEMINI.md`, or AGENTS.md via `context.fileName` |
| Skills folder (personal) | `~/.claude/skills/` | `~/.agents/skills/` | `~/.gemini/skills/` or `~/.agents/skills/` |
| Cheap subagents | `.claude/agents/*.md` with `model: haiku` | `[agents] default_subagent_model` | `.gemini/agents/*.md` with `model:` |
| Interrupt or steer | `Esc` | `Enter` steers, `Tab` queues | experimental model steering |
| Shorter replies | `/output-style concise` | low verbosity is the default | instruction line |
| Headless ping | `claude -p` | `codex exec` | `gemini -p` |

## Universal, or specific to one model?

Almost everything here works on any model, because it's about what goes into the context and how much comes out. The exceptions:

- **Budget-aware models.** It's been claimed that some models can read the account's usage limits by themselves. No vendor documents that today: usage meters are shown to the user. A budget in the prompt still helps, because the model plans to it, but the agent can't enforce it without proxies. See `usage-budget`.
- **Plan windows.** The 5-hour window belongs to Claude and ChatGPT/Codex subscription plans. API billing and Gemini's quotas work differently.
- **Cache timing** is vendor- and billing-specific: OpenAI's GPT-5.6 and later keep cached prefixes for at least 30 minutes; Claude Code on a subscription uses a one-hour cache; API keys and usage-credit overage get five minutes.
- **Price gaps** between a vendor's big and small models change often. On OpenAI's current price list, GPT-5.6 Luna costs about 2% of GPT-6 Astra's per-token rate. Check the current price page before planning around a ratio.

## Before you finish a heavy session

- [ ] Anything done twice is a skill now, or on the list to become one.
- [ ] The progress ledger is current, or removed if the job is done.
- [ ] If a budget was set, spend was reported against it.

---
Part of [agent-skills](https://github.com/MissSophieSterling/agent-skills) · MIT · improvements welcome as issues.

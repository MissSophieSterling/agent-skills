---
name: usage-budget
description: Work to an explicit usage budget. Estimate first, spend on the highest-value steps, check in at 50% and 80%, and stop before overspending. Use when the user sets a budget or limit ("do this in 3% of my usage", "keep it cheap", "I'm nearly out of tokens", "under 20 tool calls").
license: MIT
metadata:
  author: Sophie Sterling
  version: "1.1"
---

# Usage budget

A task without a budget expands to fill the plan. Stating one changes how an agent works: it plans narrower, searches less, and stops to ask instead of trying a fifth approach. A 2024 study (Token-Budget-Aware LLM Reasoning) found that a token budget stated in the prompt shortens a model's chain-of-thought output with only a small loss of accuracy.

## 1. Put the budget in units you can count

Most hosts show plan usage to the user, not to the model. The model can't read `/usage` or `/status` for itself, so turn the user's budget into things the agent counts on its own:

| User says | Working proxy |
|---|---|
| "tiny", "1–2% of my limit" | ≤10 tool calls, ≤5 file reads, no subagents |
| "small", "about 5%" | ≤30 tool calls, at most one cheap subagent |
| "whatever it takes" | no cap, but still check in at the checkpoints |

These are starting points. Calibrate them against the host's meter after a few tasks. Tell the user in one line which proxy you're using.

A few budgets the host can enforce outright:

- Claude Code headless runs: `claude -p "<task>" --max-turns 10`, or `--max-budget-usd 2.00` when billed by API.
- Claude Code or Gemini CLI subagents: `maxTurns` / `max_turns` in the agent file.
- Any API: a cap on output tokens per call.

## 2. Estimate before starting

List the steps with a rough cost for each. If the estimate is over budget, say so and offer the cheaper plan (narrower scope, skip the nice-to-haves, delegate, split across sessions) before spending anything.

## 3. Spend in value order

Locate, change, verify. Exploration is where budgets die: start from a pinpointed location (see `pinpoint`), read slices, don't browse.

## 4. Checkpoints

- At 50%: is half the work done? If not, re-plan, or tell the user now.
- At 80%: finish the smallest shippable piece, stop, and report what's left and what it would cost.

Never overrun quietly. An overrun the user agreed to is fine; a surprise one isn't.

## 5. Report

One line at the end: budget, spend, what's left.

```
Budget ≤30 tool calls: used 22. Done: fix + test. Not done: refactor of the parser (est. 15 more).
```

## Where the meters are (for the user)

| Host | Plan usage | Context |
|---|---|---|
| Claude Code | `/usage` | `/context` |
| Codex | `/status`, `/usage` | `/status` |
| Gemini CLI | `/stats model` | `/stats` |

## Before you finish

- [ ] The budget and its proxy were stated before the work began.
- [ ] Checkpoints happened; any overrun was agreed with the user.
- [ ] The last line reports spend against budget.

---
Part of [agent-skills](https://github.com/MissSophieSterling/agent-skills) · MIT · improvements welcome as issues.

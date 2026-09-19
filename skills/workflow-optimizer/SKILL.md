---
name: workflow-optimizer
description: Make a recurring job cheaper. Measure a baseline, test cheaper variants against the same quality check, keep the winner as a skill. Use when the user wants a repeat workflow (reports, content batches, triage, builds) to cost less ("optimize this workflow", "get this under 1% of my usage").
license: MIT
metadata:
  author: Sophie Sterling
  version: "1.1"
---

# Workflow optimizer

A one-off task isn't worth optimizing. A job you run every day or week is: spend some usage once to find the cheap way, and every run after that costs less. Treat cost like any other bug. Measure, change one thing, measure again, with a quality check that stops "cheaper" from quietly meaning "worse".

## 0. Is it worth it?

Experiments cost roughly (baseline cost) × (number of test runs). If the job won't run enough times to pay that back, stop here and say so.

## 1. Pin the job and the quality bar

- Fix one set of test inputs and reuse it for every run.
- Write a pass/fail quality check: tests pass, output matches the format, a reviewer checklist. Without one, no saving can be trusted.

## 2. Measure a baseline

Run the job once as it is today and record the cost with whatever meter the host has:

| Host | Meter |
|---|---|
| Claude Code | `/usage` before and after (plan share); per-session tokens from the local logs, e.g. `npx ccusage@latest session` |
| Codex | `/status` before and after; `npx ccusage@latest codex daily` |
| Gemini CLI | `/stats model`; `npx ccusage@latest gemini daily` |
| API | the `usage` fields on each response |

Plan meters move in coarse steps, so a small job can show no change at all; use token counts where you can. Also note tool calls, files read and wall time. They explain where the cost went.

## 3. Candidate changes, roughly cheapest first

1. Hand it the inputs (paths, templates, IDs) instead of letting it search. See the `pinpoint` skill.
2. Move deterministic steps into a script: renaming, packaging, formatting, API calls with fixed parameters.
3. Batch several items per run when they share context, instead of one run per item.
4. Send mechanical steps to a cheaper model and keep review on the strong one. See `cheap-subagents`.
5. Quiet the tools and shorten the replies. See `quiet-tools` and `short-answers`.
6. Switch off tools, plugins and MCP servers the job never uses. See `context-audit`.
7. Lower the reasoning effort for the mechanical parts only.

## 4. Experiment

- One change (or one small bundle) per run, same inputs, same quality check.
- Log every run:

| # | Change | Cost | vs baseline | Quality check | Notes |
|---|---|---|---|---|---|
| 0 | baseline | | | pass | |

- Keep a change only if the check still passes. Drop changes that save almost nothing: complexity has a cost too.
- Stop when the experiment budget is spent or two ideas in a row save next to nothing.

## 5. Lock it in

Write the winning procedure as a skill (see `skillify`), with scripts for the deterministic parts and the quality check as its final step. Record the measured cost per run inside it, so drift shows up later.

## 6. Report

Baseline vs optimized cost per unit, how many runs, what changed, what didn't help. Say plainly that small samples on one input set are indicative, not proof, and re-check on real inputs.

## About "get this under 1% of my limit"

No host documents giving the model its own plan usage today (see `usage-budget`), so the model can't check a target like that by itself. State the target anyway, so it aims for it, and measure between runs yourself as above.

## Before you finish

- [ ] Baseline and every variant measured with the same meter and the same inputs.
- [ ] The quality check passed for the version that was kept.
- [ ] The winner is saved as a skill, or the reason it wasn't is stated.

---
Part of [agent-skills](https://github.com/MissSophieSterling/agent-skills) · MIT · improvements welcome as issues.

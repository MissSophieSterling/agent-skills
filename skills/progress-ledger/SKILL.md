---
name: progress-ledger
description: Keep a short progress file on long, batch or multi-session work so a crash or a new session resumes from the last verified step instead of redoing it. Use for jobs longer than about 30 minutes or over many items, and when resuming ("pick up where you left off", "resume the batch", after a crash or compaction).
license: MIT
metadata:
  author: Sophie Sterling
  version: "1.1"
---

# Progress ledger

Work an agent has done and then lost track of gets paid for twice. A ledger is one small file that says what's finished, where it is, what failed and what's next. With it, any new session (or a different agent) starts at the right step. Anthropic's harness for long-running agents uses the same idea: a progress log plus git commits, so each fresh context window can get its bearings quickly.

## Start

Create `PROGRESS.md` (or use the project's existing equivalent) when the job starts:

```markdown
# Progress: <goal in one line>
Updated: YYYY-MM-DD HH:MM

## Done (verified)
- <item> → <where the output is>

## In progress
- <item>: <state>

## Failed / blocked
- <item>: <exact error>; tried <what>

## Next
1. <next step>

## Decisions
- <choice made, and why, in one line>
```

For a batch, keep a machine-readable ledger beside it, one line per item, so a resume can skip finished items with a lookup instead of re-checking each one:

```
<item-id>	<done|failed|skipped>	<output path or error>
```

## While working

- Update right after each unit is **verified** (test passed, file written, draft saved). Not at the end, and never before the check.
- Keep it under about 60 lines. Replace stale lines instead of appending a diary; git history (commit after each verified unit, when in a repo) holds the detail.
- Log failures with the exact error and what was tried, so the next session doesn't walk into the same dead end.

## Resume

1. Read the ledger before anything else.
2. Spot-check the last few "done" entries (the file exists, the test passes). A session that crashed mid-step can claim more than it finished.
3. Carry on from "Next". Trust the rest; don't re-verify everything.

## Finish

Mark the goal done, then delete or archive the ledger. A stale ledger from an old task misleads the next agent that finds it, and it does so confidently.

## Before you finish a session

- [ ] Ledger updated after the last verified unit, with the date and time.
- [ ] Every "done" line says where its output is.
- [ ] Failures carry the exact error text.
- [ ] If the goal is complete, the ledger is removed or archived.

---
Part of [agent-skills](https://github.com/MissSophieSterling/agent-skills) · MIT · improvements welcome as issues.

---
name: quiet-tools
description: Cut tool-output noise (test logs, build logs, installs, huge searches) without hiding failures. Use when command output floods the context ("the test output is huge", "stop dumping logs", "why is my context full"), or when setting up quiet-output habits or a test-output filter hook for Claude Code or Codex.
license: MIT
metadata:
  author: Sophie Sterling
  version: "1.1"
---

# Quiet tools

Every tool result lands in the context and is re-read on every later turn until the conversation is compacted or cleared. A passing test suite that prints 400 lines, a search that returns every match in 200 files, a full `npm install` log: the model reads all of it, then pays for it again on each turn after. Ask for the outcome, and take the details only when something failed.

## Habits

Run in quiet modes and let the exit code carry success:

```
pytest -q --tb=short
npm test --silent
cargo test -q
go test ./...
git status --short
rg -l "pattern"        # file names only; rg -c for counts per file
```

- Size before reading: `wc -l <file>`, then read a line range, not the whole file.
- Trim long output at the source without losing the exit code:

```
<build command> > "${TMPDIR:-/tmp}/build.log" 2>&1; echo "exit=$?"; tail -n 40 "${TMPDIR:-/tmp}/build.log"
```

- Select from structured output instead of reading it all: `jq '.items[].name'`.
- Batch checks into one script that prints one line per item, and full detail only for the items that failed.
- Hand a wide sweep (a typo across 200 files, "where is X used") to a subagent or search mode that returns only the hits. See `cheap-subagents`.
- Report a success in one line ("tests: 142 passed"). Quote a failure in full: the error line, the frame that matters, a few lines of context.

## The limit

Trimmed output that drops the one line explaining a failure costs more than it saved. The agent guesses, re-runs, or reasons its way back to what was cut, and there are measured cases where an output-compression hook raised total cost. So:

- don't trim failure output; if a quiet run fails ambiguously, re-run just that item verbosely;
- keep the exit code intact (a pipe into `grep` or `head` replaces it with the last command's);
- try any filter on a real failing case before making it permanent.

## Make it permanent

One line for the instruction file (AGENTS.md, CLAUDE.md or GEMINI.md):

```
Keep tool output small: use quiet flags, read files in slices, summarize successes in one line, and show full detail only for failures.
```

### Claude Code: a test-output hook

Ask the user before installing this: it edits their Claude Code settings and auto-approves plain test commands.

A PreToolUse hook can rewrite test commands before they run. This one only touches plain `npm test`, `pytest` and `go test` commands. Anything chained, piped, redirected or commented passes through unchanged, so it still gets the normal permission prompt. A passing run comes back as the runner's last three lines (its summary). A failing run comes back as the last 150 lines with the passing-test noise removed. The real exit code survives either way. (The example in the Claude Code cost docs pipes into `head`, which reports success even when tests fail, and prints nothing when they pass.)

Save as `~/.claude/hooks/filter-test-output.sh` and `chmod +x` it:

```bash
#!/bin/bash
input=$(cat)
cmd=$(echo "$input" | jq -r '.tool_input.command')

# Only plain test commands: anything chained, piped, redirected or commented passes through untouched.
unsafe='[;&|<>`$()#]'
if [[ "$cmd" =~ ^(npm\ test|pytest|go\ test)(\ |$) && ! "$cmd" =~ $unsafe && "$cmd" != *$'\n'* ]]; then
  filtered_cmd="( log=\$(mktemp); { $cmd; } >\"\$log\" 2>&1; status=\$?; if [ \$status -eq 0 ]; then tail -n 3 \"\$log\"; else grep -v -E '(PASSED|^ok )' \"\$log\" | tail -n 150; fi; rm -f \"\$log\"; exit \$status )"
  echo "$input" | jq --arg filtered "$filtered_cmd" \
    '{hookSpecificOutput: {hookEventName: "PreToolUse", permissionDecision: "allow", updatedInput: (.tool_input + {command: $filtered})}}'
else
  echo "{}"
fi
```

Register it in `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      { "matcher": "Bash", "hooks": [ { "type": "command", "command": "~/.claude/hooks/filter-test-output.sh" } ] }
    ]
  }
}
```

It needs `jq`. Check it with `/hooks`. When the full log is needed, run the tests another way the hook doesn't match, for example `python -m pytest -v`.

### Codex

Codex already truncates each tool output it keeps in history. `tool_output_token_limit` in `~/.codex/config.toml` sets that budget. Lowering it trims noise, but it cuts failures too, so the habits above still matter.

## Before you finish

- [ ] No successful step dumped more than about 50 lines into the context.
- [ ] Every failure was reported with its error text and its real exit code.
- [ ] The hook was installed only after the user agreed to it.

---
Part of [agent-skills](https://github.com/MissSophieSterling/agent-skills) · MIT · improvements welcome as issues.

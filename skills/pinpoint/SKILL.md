---
name: pinpoint
description: Turn a vague task into a pinpointed brief before searching, and map a codebase once so later tasks start in the right file. Use when a request has no location or expected result ("fix my site", "debug this", "the button doesn't work"), or when asked to map where things live in a repo.
license: MIT
metadata:
  author: Sophie Sterling
  version: "1.1"
---

# Pinpoint

Searching is the most expensive thing a coding agent does by accident. "Debug my website" sends it through directory listings, greps and whole-file reads before it touches the fault. "The Save button on /settings does nothing; it should POST to /api/profile; the handler is in `src/routes/profile.ts`" sends it straight there. Every file it reads along the way is paid for again on each later turn, because it stays in the context.

## 1. Brief first

Before the first search, check the request for six things:

| Field | Example |
|---|---|
| Where | page, route, screen or command; file or function if known |
| Steps | how to make it happen |
| Observed | what happens, with the exact error text |
| Expected | what should happen instead |
| Done when | the check that proves it's fixed |
| Scope | what not to touch |

- If one targeted lookup fills the gap (one grep for the button label, one look at the route table), do that.
- If it can't, and the user is around, ask one short question that names only the missing fields. One round trip costs less than an exploration spree.
- Restate the brief in two to four lines, then start at the named location. Read the smallest slice that answers the question (a function, a line range), not whole folders.

## 2. Map once, reuse every time

When the repo is bigger than a handful of files and has no map, write one the first time you have to explore it:

- Save it as `CODEBASE_MAP.md` at the repo root, or as a small project skill. Put one line in the instruction file (AGENTS.md, CLAUDE.md, GEMINI.md) that says where it is. Don't paste the map itself into the instruction file: that file loads in every session.
- Keep it under about 150 lines. Date it.
- Most useful part: a "symptom → start here" table, so a bug report goes straight to a file.

```markdown
# Codebase map (updated YYYY-MM-DD)
Run: `<dev command>` · Test one file: `<test command> <path>`

## Entry points
- `<path>`: <what starts here>

## Routes / screens → files
| Route | Handler | View |
|---|---|---|

## Feature → folder
| Feature | Folder |
|---|---|

## Symptom → start here
| Symptom | Look at |
|---|---|

## Traps
- <thing that looks right but isn't>
```

A stale map is worse than none: it sends the agent to the wrong place with confidence. Check that a path exists before trusting it, and update the map when you move things.

## Per tool

- Claude Code and Gemini CLI take `@path` in the prompt to pull a file straight in. In any tool, pasting the path does the job.
- When a wide search can't be avoided, give it to a subagent so only the findings come back to the main context. See `cheap-subagents`.

## Before you finish

- [ ] The work started from a named location and an expected result, not a broad search.
- [ ] If a map was written or used, every path in it was checked to exist.
- [ ] The instruction file holds only a pointer to the map, not the map.

---
Part of [agent-skills](https://github.com/MissSophieSterling/agent-skills) · MIT · improvements welcome as issues.

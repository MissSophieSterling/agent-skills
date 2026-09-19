# agent-skills

Skills for AI coding agents, in the open [Agent Skills](https://agentskills.io) format: a folder with a `SKILL.md` that Claude Code, Codex, Gemini CLI, Cursor, GitHub Copilot and a few dozen other agents can load.

The first set is about making a plan's usage last longer. It began as a list of usage-limit tips for OpenAI's GPT-6 Astra in Codex. Here the tips are rewritten to work on any model, checked against each vendor's own docs, and anything that didn't hold up has been dropped.

## The skills

| Skill | What it does |
|---|---|
| [token-saver](skills/token-saver) | The whole playbook in one skill, with the ten below bundled inside as references |
| [pinpoint](skills/pinpoint) | Turns "fix my site" into a brief with a location and an expected result, and maps a codebase once |
| [usage-budget](skills/usage-budget) | Works to a stated budget, with checkpoints at 50% and 80% |
| [context-audit](skills/context-audit) | Measures and trims what loads before the first message |
| [cheap-subagents](skills/cheap-subagents) | The strong model plans and reviews; cheaper models do the narrow work, under a cap |
| [quiet-tools](skills/quiet-tools) | Small tool output, full failures, plus a tested test-output hook for Claude Code |
| [short-answers](skills/short-answers) | Replies as short as the job allows |
| [progress-ledger](skills/progress-ledger) | A progress file, so a crash or a new session resumes instead of redoing work |
| [skillify](skills/skillify) | Turns a workflow that worked into a reusable skill |
| [workflow-optimizer](skills/workflow-optimizer) | Measures a recurring job and tests cheaper variants against a quality check |
| [limit-window-warmup](skills/limit-window-warmup) | Schedules a tiny morning prompt so a 5-hour plan window resets sooner |

Install `token-saver` on its own for a single entry in your skill list (its description is about 90 tokens), or pick the individual skills you want (all ten come to about 725 tokens of descriptions). Installing both doubles up.

## Install

Any supported agent, with the open skills CLI:

```
npx skills add MissSophieSterling/agent-skills --skill token-saver
```

`--list` shows every skill in the repo, `-a claude-code`, `-a codex` or `-a gemini-cli` picks the agent, and `-g` installs for your user instead of the current project. For Codex, install per project, or copy the folder to `~/.agents/skills/` yourself: that's the personal folder Codex's docs list, and a global install from the CLI may land somewhere else. Check with `/skills` in Codex.

Claude Code, as a plugin:

```
/plugin marketplace add MissSophieSterling/agent-skills
/plugin install token-saver@sophie-skills
```

(`token-saver-tactics@sophie-skills` installs the ten separate skills instead.)

By hand, copy a skill folder into your agent's skills folder:

```
git clone https://github.com/MissSophieSterling/agent-skills
mkdir -p ~/.claude/skills && cp -r agent-skills/skills/token-saver ~/.claude/skills/
```

| Agent | Personal folder | Project folder |
|---|---|---|
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| Codex | `~/.agents/skills/` | `.agents/skills/` |
| Gemini CLI | `~/.gemini/skills/` | `.agents/skills/` |

Read a skill before installing it: they're plain Markdown, and nothing runs until your agent follows them. The two that can change your machine (the Claude Code hook in `quiet-tools`, the scheduled job in `limit-window-warmup`) say so, and tell the agent to ask first.

## Notes

Tool facts were checked against vendor documentation on 2026-09-19. The Claude Code hook, both warm-up pings, the launchd plist and the TOML and JSON snippets were run or linted on macOS before publishing. The cron lines were syntax-checked only, the Windows Task Scheduler line is untested (and says so), and the Gemini CLI commands come from Gemini's own docs. Plans, flags and prices change often. If something here has gone stale, open an issue.

## Contributing

- One folder per skill under `skills/`, each with a `SKILL.md` whose frontmatter has `name` (same as the folder) and `description`.
- `python3 tools/validate.py` checks every skill; CI runs it on each push.
- After editing one of the ten tactic skills, run `python3 tools/bundle.py` to refresh the copies inside `token-saver`.

## Sources

- [Agent Skills specification](https://agentskills.io/specification)
- [Claude Code: manage costs effectively](https://code.claude.com/docs/en/costs)
- [Codex pricing and usage limits](https://learn.chatgpt.com/docs/pricing)
- [Gemini CLI documentation](https://github.com/google-gemini/gemini-cli/tree/main/docs)
- [Never Hit GPT 6 Astra Usage Limits Again](https://youtu.be/u_yvc7NTYvI), the video the original tips came from

## License

[MIT](LICENSE)

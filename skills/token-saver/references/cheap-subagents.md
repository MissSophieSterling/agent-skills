<!-- Copy of skills/cheap-subagents/SKILL.md, made by tools/bundle.py. Edit the original and re-run the script. -->

# Cheap subagents

The strong model doesn't need to do every step itself. It earns its price on planning, judgment and review. The routine middle (sorting, searching, drafting to a template, running checks) can go to a model that costs a fraction per token. Delegating also keeps noisy output (search results, logs) inside the subagent's own context, so only a summary comes back to the main conversation.

The catch: delegation multiplies tokens. Every subagent reads its own system prompt, tools and instructions before it starts, and Anthropic reports multi-agent systems using about 15 times the tokens of a plain chat. Delegation saves money when cheap tokens replace expensive ones on real volume. It loses money when it just adds a crowd.

## 1. Decide what to delegate

- Delegate: mechanical, parallel, read-heavy, template-shaped, independently checkable work.
- Keep: anything that needs the whole conversation, judgment across the pieces, or a spec that would be as long as doing the work.

## 2. Write narrow job specs

Each spec has one goal, exact inputs (paths, IDs), an output format with a size limit, a done-when check, and what not to touch.

- Too wide: "look into the email backlog."
- Narrow: "For each of the 40 files in `inbox/*.eml`, output one line: `id | needs reply: yes/no | reason in 10 words`. Don't draft replies."

## 3. Pick the cheapest model that can do it

**Claude Code**: a subagent file in `.claude/agents/` (project) or `~/.claude/agents/` (personal):

```markdown
---
name: triage
description: Classifies a batch of items and returns one line per item. Use for bulk sorting and labelling.
model: haiku
tools: Read, Grep, Glob
maxTurns: 10
---
For each item you are given, output exactly one line: `<id> | <label> | <reason, 10 words max>`. No other text.
```

Since v2.1.198 the built-in Explore subagent runs on the main conversation's model instead of Haiku. To keep wide searches cheap, define your own subagent named `Explore` with `model: haiku`; it overrides the built-in one.

**Gemini CLI**: a Markdown file in `.gemini/agents/` or `~/.gemini/agents/` with `kind: local`, a `model:` (a Flash model, for example) and `max_turns:`. Force a specific one with `@<agent-name>` at the start of the prompt.

**Codex**: set subagent defaults in `~/.codex/config.toml`, or define a custom agent as a TOML file in `~/.codex/agents/` or `.codex/agents/` with `name`, `description`, `developer_instructions`, `model` and `model_reasoning_effort`. Codex delegates only when asked, or when AGENTS.md or a skill says to (the top `ultra` effort level delegates on its own). OpenAI's docs say subagent runs use more tokens than a single agent, so the saving has to come from the cheaper model.

```toml
[agents]
default_subagent_model = "gpt-5.6-luna"
default_subagent_reasoning_effort = "medium"
max_concurrent_threads_per_session = 4
```

A cheap model at maximum effort still burns a lot of thinking tokens (Artificial Analysis counted about 28,000 per task for GPT-5.6 Luna at max). Start at medium and raise it only if the results need it.

**Any API**: route calls by task type: the small model for classification and extraction, the large one for synthesis and final review.

## 4. Cap it

State a maximum number of subagents, and keep delegation to one level (subagents don't start their own). Unbounded spawning is the classic way delegation burns a limit: one reported Claude Code case started 48 background agents for a single research request, and only the first few added anything.

## 5. Review, don't redo

Check the outputs against the done-when test, and read a few in full. If you catch yourself redoing the work, the job was too big or too vague. Split it smaller, or keep it in the main session next time.

## 6. Check the maths once

On one real sample, compare the tokens (or the plan percentage) with delegation against the strong model alone. Keep delegating that kind of job only if it's cheaper at equal quality.

## Before you finish

- [ ] Every job spec had inputs, an output format with a size limit, and a done-when check.
- [ ] A spawn cap was stated and held; no nested delegation.
- [ ] Outputs were reviewed against the check, not redone.

---
Part of [agent-skills](https://github.com/MissSophieSterling/agent-skills) · MIT · improvements welcome as issues.

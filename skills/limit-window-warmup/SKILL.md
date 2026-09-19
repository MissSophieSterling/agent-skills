---
name: limit-window-warmup
description: Schedule one tiny, cheap prompt before the workday so a Claude or ChatGPT/Codex plan's 5-hour usage window starts early and resets sooner. Use when the user runs out of the 5-hour limit partway through the morning, or asks to warm up, ping or pre-start their usage window on a schedule.
license: MIT
metadata:
  author: Sophie Sterling
  version: "1.1"
---

# Limit window warm-up

Claude's paid plans, and ChatGPT plans used through Codex, meter usage in 5-hour windows that start with your first prompt, plus a weekly cap (OpenAI documents this for Codex; for Claude it's how the window behaves in practice). First prompt at 9:00, out of usage at 10:00: you wait until 14:00. If a scheduled one-line prompt already opened the window at 6:00, it resets at 11:00. Same usage, earlier reset.

It gives you no extra usage (the ping itself uses a little) and does nothing for the weekly cap. It's a scheduling trick, not a saving.

## 0. Is it worth it?

- Only if the user regularly runs out within the first few hours of work.
- Only where the window really starts at the first prompt. Check the provider's current help page before setting it up; plan rules change.
- Gemini CLI's free tier uses per-minute and per-day quotas. There's no window to shift, so skip it there.

## 1. Pick the time

```
ping time = usual start + hours until you usually run out − 5 h
```

Start 9:00, out by about 10:00 → ping around 5:00 to 6:00, reset around 10:00 to 11:00.
Pinging more than 5 hours before you start gains nothing: that window closes before you begin.

## 2. The ping: cheapest model, one short prompt

```
claude -p "hi" --model haiku --no-session-persistence
codex exec --ephemeral --skip-git-repo-check -m gpt-5.6-luna -c 'model_reasoning_effort="low"' "hi" </dev/null
```

- `--no-session-persistence` (Claude Code) and `--ephemeral` (Codex) keep the ping out of the resume history.
- Codex refuses to run outside a Git repo or trusted folder unless you pass `--skip-git-repo-check`. A scheduler starts in the home folder, so without it the ping fails silently every morning.
- `</dev/null` stops `codex exec` from waiting for input on stdin.
- Pin the effort low. The ping inherits the reasoning effort from your Codex config, and even a one-word ping carries the instruction files and skill list. In one run on a setup whose default was the top effort level, it used about 15,500 tokens; at low, about 5,800.
- Use full paths in schedulers (`which claude`, `which codex`): they don't load your shell's PATH. If `which` points to an npm install, node has to be on the job's PATH too (a `PATH=` line at the top of the crontab, or `EnvironmentVariables` in the plist).
- The CLI must already be logged in as the user the job runs as.

## 3. Schedule it (ask first: this installs a job that keeps running on the user's machine)

**macOS, launchd.** If the Mac was asleep at 6:00, launchd runs the job when it wakes, which gains nothing. The Mac has to be awake, or scheduled to wake, at ping time; `sudo pmset repeat wakeorpoweron MTWRF 05:55:00` wakes it on weekdays (a system setting: ask first). Save as `~/Library/LaunchAgents/com.example.agent-warmup.plist`, replace `YOU` with the user name, and add a `<dict>` per weekday you want:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>com.example.agent-warmup</string>
  <key>ProgramArguments</key>
  <array>
    <string>/Users/YOU/.local/bin/claude</string>
    <string>-p</string><string>hi</string>
    <string>--model</string><string>haiku</string>
    <string>--no-session-persistence</string>
  </array>
  <key>StartCalendarInterval</key>
  <array>
    <dict><key>Weekday</key><integer>1</integer><key>Hour</key><integer>6</integer><key>Minute</key><integer>0</integer></dict>
  </array>
  <key>StandardOutPath</key><string>/tmp/agent-warmup.log</string>
  <key>StandardErrorPath</key><string>/tmp/agent-warmup.log</string>
</dict>
</plist>
```

```
plutil -lint ~/Library/LaunchAgents/com.example.agent-warmup.plist
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.example.agent-warmup.plist
```

For Codex, put the codex command's words in `ProgramArguments` instead, one `<string>` each (`model_reasoning_effort="low"` goes in as one string, quotes included). Leave out `</dev/null`: launchd already gives jobs an empty stdin.

**Linux, cron** (`crontab -e`). Cron skips a run if the machine was off:

```
0 6 * * 1-5 /home/YOU/.local/bin/claude -p "hi" --model haiku --no-session-persistence >/dev/null 2>&1
0 6 * * 1-5 /home/YOU/.local/bin/codex exec --ephemeral --skip-git-repo-check -m gpt-5.6-luna -c 'model_reasoning_effort="low"' "hi" </dev/null >/dev/null 2>&1
```

**Windows, Task Scheduler** (not tested by this skill's author; check the path with `where claude`):

```
schtasks /Create /SC WEEKLY /D MON,TUE,WED,THU,FRI /ST 06:00 /TN "agent-warmup" /TR "%USERPROFILE%\.local\bin\claude.exe -p hi --model haiku --no-session-persistence"
```

## 4. Verify the next morning

Check the plan meter (Claude Code `/usage`, Codex `/status`): the next reset should be at the ping time plus 5 hours. If it didn't, check that the job ran (`cat /tmp/agent-warmup.log` on macOS, the cron log on Linux) and that the machine was awake.

## Remove it

```
launchctl bootout gui/$(id -u)/com.example.agent-warmup
rm ~/Library/LaunchAgents/com.example.agent-warmup.plist
```

Linux: delete the line with `crontab -e`. Windows: `schtasks /Delete /TN "agent-warmup"`.

## Before you finish

- [ ] The user agreed to a scheduled job, and knows how to remove it.
- [ ] The ping uses the cheapest model and a full path to the CLI.
- [ ] The plist passed `plutil -lint` (macOS), or the cron line was saved (Linux).
- [ ] The user knows to check the meter the next morning.

---
Part of [agent-skills](https://github.com/MissSophieSterling/agent-skills) · MIT · improvements welcome as issues.

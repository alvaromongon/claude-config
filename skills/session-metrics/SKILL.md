---
name: session-metrics
description: Measure a project's Claude Code sessions from their local transcripts — estimated cost and tokens per merged PR by role and model, review rounds, human messages, active and paused time, usage-limit hits and fixed context per call. Use to take a baseline before a configuration change (skills, models, review gate, connectors) and to compare after it, or when asked how much a repo's agent work costs or where the tokens go.
model: sonnet
---

# Session metrics

Measures before/after a configuration change, so a change is kept only when it pays off.

## Run

```bash
python3 ~/.claude/skills/session-metrics/scripts/session_metrics.py \
  ~/.claude/projects/<project> [--since YYYY-MM-DD] [--until YYYY-MM-DD] [--json]
```

`<project>` is the repo's absolute path with every `/` and `.` replaced by `-` (e.g.
`/Users/me/Code/app` → `-Users-me-Code-app`). Pass the worktree folders of the same repo too
(`-Users-me-Code-app--claude-worktrees-*`) to count their sessions. A session belongs to the window
in which it starts.

## Read the result

- **Cost is estimated** (list prices in the script, from ADR 0003); everything else is measured
  from the transcripts. Say so when quoting figures.
- **Roles** come from each subagent's `Agent` description (`Implement…`, `Code review…`, `Fix…`,
  `Checkpoint…`); a nested subagent counts towards its parent's role. `main` is the session the
  user typed in — the work-queue orchestrator during a `/github-work-queue` run.
- **Quality**: review rounds per PR count top-level code-review spawns; "clean at first review" is a
  PR with one round and no fix subagent. Defects that escape review (bugs filed later, reverts) are
  not in the transcripts: check them with `gh` over the same window.
- **Active time** adds gaps of up to 15 minutes between events; longer gaps are paused (waiting for
  the user, usage limits).

## Record a window (this repo's efficiency log)

Only for **public** repos: the row is published. Append it and re-render the pages:

```bash
python3 ~/.claude/skills/session-metrics/scripts/session_metrics.py ~/.claude/projects/<project> \
  --since YYYY-MM-DD --until YYYY-MM-DD --record ~/.claude/docs/efficiency.csv \
  --repo <owner>/<name> --change "<the change this window measures>"
python3 ~/.claude/skills/session-metrics/scripts/efficiency.py
```

`--record` refuses a window with no merged PRs. The Docs check fails if the README or
`docs/efficiency.md` no longer matches the CSV.

## Compare before and after

1. Take the baseline over a window of at least 10 merged PRs and record it with its date range.
2. Make one change at a time; run comparable work (same repo, similar tickets) for another ≥ 10
   merged PRs.
3. Keep the change when cost per merged PR falls and review rounds, human messages per PR and
   escaped defects do not rise. Tickets vary a lot: for a close call, confirm in the workflow
   sandbox with the affected skill's `evals/scenarios.md`.

Tests: `python3 -m unittest discover -s skills/session-metrics/tests`.

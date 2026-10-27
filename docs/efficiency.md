# Efficiency

How much the configuration costs per merged pull request, and how each change to it moves that
number. Decision: [ADR 0007](decisions/0007-readme-as-landing-page-with-a-measured-efficiency-log.md).

## History

One row per window; a window measures one configuration change. Data:
[`efficiency.csv`](efficiency.csv).

<!-- efficiency:history:start -->
| Change | Repo | Window | Merged PRs | $/PR (est.) | Owner msgs/PR | Clean 1st review | Review rounds | Active min/PR | Tokens/PR | Limit hits | Fixed context main / subagent |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Baseline | alvaromongon/finance-agent | 2026-10-16 → 2026-10-26 | 31 | 12.17 | 3.97 | 38% | 1.86 | 35 | 21,504,461 | 5 | 72696 / 54713 |
<!-- efficiency:history:end -->

## Method

- **Source**: Claude Code's local session transcripts of real work in a **public** repo, read by
  the [`session-metrics`](../skills/session-metrics/SKILL.md) skill. Transcripts stay private;
  only the aggregated row is published.
- **Window**: starts on the day a change lands here and closes after at least 10 merged PRs. One
  change per window, so each step in the chart has one cause.
- **Measured**: tokens, merged PRs, review rounds (top-level code-review runs per PR), PRs clean at
  the first review (one round, no fix), owner messages, active agent minutes (gaps between events
  of up to 15 minutes; longer ones count as paused), usage-limit hits, and the fixed context of each
  transcript's first call.
- **Estimated**: cost, at list prices per model with cache writes at 1.25×/2× and reads at 0.1× of
  the input price. A subscription is billed by plan; the prices only make windows comparable.
- **Not in the transcripts**: defects that escape review (bugs filed later, reverts) — checked
  with `gh` over the same window before keeping a change.
- **Keep a change** when cost per merged PR falls and owner messages per PR, review rounds and
  escaped defects don't rise. Field windows are noisy (ticket mix changes): an effect under ~10% is
  not conclusive, and a close call goes to a fixed lab benchmark instead.

### Recording a window

```bash
python3 skills/session-metrics/scripts/session_metrics.py ~/.claude/projects/<project> \
  --since YYYY-MM-DD --until YYYY-MM-DD \
  --record docs/efficiency.csv --repo <owner>/<name> --change "<change>"
python3 skills/session-metrics/scripts/efficiency.py   # re-render README and this page
```

The Docs check fails when the README or this page no longer matches the CSV.

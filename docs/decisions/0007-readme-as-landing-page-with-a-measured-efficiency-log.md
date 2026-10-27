---
status: Accepted
date: 2026-10-27
decision-makers: Alvaro Montero
consulted: "N/A"
---

# 0007. The README is a landing page with a measured efficiency log; topic documents own their topics

**Decision**: the README of this public repository becomes a landing page — what it is, a snapshot of measured efficiency with a chart that ties each configuration change to its effect, how to start, the skills and where to read more — and documents under `docs/` own their topics (the workflow, maintaining the repository, the efficiency history). Efficiency is measured from real work in public repositories, one window per configuration change, recorded as aggregated rows in a versioned log and rendered into the pages by a script that CI checks. Target: cost per merged pull request below the baseline of $12.17 (estimated) after the first change, with owner messages per merged pull request not above 3.97.

## Context and problem statement

The README had grown to about 215 lines that mixed what the repository is, how the GitHub workflow works, how to maintain the repository and its open work. The repository is public and the owner wants it to show, at a glance, how efficient the configuration is and how each change moves that efficiency, which adds data the README has no room for. Until now nothing recorded efficiency: whether a change to the skills, models or review gate paid off was a matter of opinion.

The data comes from Claude Code's local session transcripts (one file per session and subagent, with the token usage of every model call). They exist only on the owner's machine and hold full conversations, so CI cannot produce the data and the transcripts themselves must never be published; only aggregated figures may be.

**Why it matters**: the configuration's cost is dominated by orchestration and review, not by writing code — in the first measured window, implementing and fixing were 16% of the estimated cost (measured token usage over 31 merged pull requests in a public repository, 2026-10-16 to 2026-10-26, priced at list prices; the cost itself is an estimate). Changes that could cut it — a cheaper model for the orchestrator, a narrower re-review, a conditional security review — are trade-offs against quality that need numbers before and after. The same numbers, shown on the landing page, are what a visitor of a public repository can check.

## Decision drivers

- A visitor understands what the repository is and what it achieves within seconds.
- Every change to the configuration is judged by measured cost and quality, not opinion.
- Transcripts stay private; only aggregates from public repositories are published.
- The page must never show figures that disagree with the data behind them.
- Little tooling to maintain: the repository is documentation, not an application.

## Considered options

- **A. Landing README plus topic documents, with an efficiency log fed by field data** (real work in public repositories, recorded by hand after each change window).
- **B. Same pages, fed by a lab benchmark**: a fixed set of tickets in a public benchmark repository, reset to a tag and run unattended with each configuration, measured the same way.
- **C. A metrics dashboard outside the repository** (a hosted page or a GitHub Pages site fed by a benchmark action), linked from the README.
- **D. Do nothing**: keep the single long README and no efficiency data.

## Decision outcome

Chosen option: "A", with B kept for later, because field data costs nothing beyond the work already being done and reflects real use, while the pages and the log are plain files the existing checks can guard. B is added only when a decision is too close for field data to settle.

- **Pages**: the README keeps what a visitor needs (what it is, the efficiency snapshot and chart, how to start, the skills table, links). `docs/workflow.md` holds how the GitHub workflow works, `docs/maintaining.md` how to change and protect the repository, and `docs/efficiency.md` the full history and the method. The global rule "the README is the single source of truth; other documents point to it" becomes: the README is the single entry point, each topic lives in exactly one document, and the others link it instead of repeating it.
- **Log**: `docs/efficiency.csv`, one row per window: the change it measures, the public repository, the date range, merged pull requests and, per merged pull request, the estimated cost, owner messages, active agent minutes and tokens, plus the share of pull requests clean at the first review, review rounds, usage-limit hits and the fixed context of a first call. A window measures one change and starts on the date that change landed.
- **Recording**: after a change has been used for at least 10 merged pull requests in a public repository, the owner runs the `session-metrics` skill with `--record`, which appends the row; a script then renders the snapshot into the README and the history into `docs/efficiency.md` between markers.
- **Chart**: a Mermaid `xychart-beta` block, one bar per window with the change as its label, for cost per merged pull request and for owner messages per merged pull request. It is text in the README, renders in GitHub's Markdown viewer and needs no build step.

**What we give up**: field data is noisy — tickets differ in size and kind between windows — so a change smaller than about 10% cannot be told apart from that noise (estimated: from the spread of review rounds per pull request in the baseline, 1 to 5). Windows also wait for real work, so a change takes days to be measured. Cost is an estimate at list prices; a subscription is billed by plan, and the prices only make windows comparable.

**Sequence**: the log and its recording first, because every page reads from it; then the README restructure and the chart; then the first change and its window; the lab benchmark last, when a decision is close.

**Scope**: this repository's README and documents, the `session-metrics` skill, and every repository whose work is measured (public ones only).

**Confidence**: medium. Revisit if two consecutive windows contradict each other on the same change (field data is too noisy: add B), or if a visitor-facing chart turns out to need more than Mermaid can draw.

### Consequences

- Good: every configuration change gets a number, and the landing page shows the trend with the change that caused each step.
- Good: the README gets shorter and each topic has one home.
- Bad: one more step after each change window (run the skill, commit the row), and the snapshot only moves when the owner records it.
- Bad: field windows are not controlled experiments; ticket mix can mask or fake an effect.
- Bad: Mermaid charts have one y-axis and no legend, so each metric needs its own chart.

### Confirmation

The documentation check in CI renders the snapshot and the history from the log and fails when the README or `docs/efficiency.md` differs from that rendering; its description names this ADR. The `session-metrics` tests check how a window becomes a row.

**Success measure**: cost per merged pull request (estimated) below $12.17 and owner messages per merged pull request not above 3.97 in the first window after a change, read from `docs/efficiency.csv`; measured once that window reaches 10 merged pull requests.

## Pros and cons of the options

### A. Landing README, topic documents, field data

- Good: no extra runs or cost; measures the configuration as it is really used.
- Good: plain files, checked by the existing documentation CI.
- Bad: noisy and slow, as above.

### B. Lab benchmark

- Good: the same tickets for every configuration, so small effects show; repeat runs give a spread.
- Bad: each run costs real usage — estimated $60 per configuration for 5 tickets at the baseline's $12 per pull request — and a benchmark repository to keep realistic.

### C. External dashboard

- Good: interactive charts, history per commit.
- Bad: benchmark actions expect data produced in CI, which ours is not; another site to keep up; the README still needs a summary.

### D. Do nothing

- Good: no work.
- Bad: no way to tell whether a change helped; the README keeps growing.

## More information

Sources read on 2026-10-27: write-ups on measuring coding agents agree that no single metric is enough and pair cost per merged pull request with the human intervention rate, the defect rate and cycle time, accepting a cost cut only if the others hold; benchmark papers on coding agents count tokens per solved task including failed attempts; a public token-usage comparison tool for Claude Code keeps its results as files committed to its repository after each run; guides on README structure advise a short hero, a handful of badges and links to deeper documents before the README turns into a manual. GitHub's Markdown viewer was checked on 2026-10-27 to render `xychart-beta` bar charts, on a public README that uses one.

Doubt review: not run. The decision is cheap to reverse (pages and a CSV) and was settled with the owner option by option.

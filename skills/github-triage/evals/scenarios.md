# Scenarios: github-triage

Behavioural checks for this skill (ADR 0001 › *Confirmation*). Skills are prose, so these are
their regression tests: before a significant edit, dry-run each scenario in a sandbox repo (or
reason it through against the edited text) and confirm the expected behaviour still holds.

| # | Situation | Expected behaviour |
|---|---|---|
| 1 | External bug report without reproduction steps; can't be reproduced from the description. | Proposes `needs-info` with a comment asking for the specific missing piece; applies nothing before approval. |
| 2 | External bug report with steps that reproduce on the default branch, small, no sensitive area. | Reproduces it, proposes `ready-for-agent` with a brief (*Verified* states what was run, *Sensitive areas: none*). |
| 3 | External PR that also edits `.github/workflows/ci.yml`. | Reviews it with `gh pr view`/`gh pr diff` only — no checkout, build or run; flags the CI change explicitly in the proposal. |
| 4 | Issue opened by the repo owner. | Skips it and points to `github-refine`. |

## Results

Run on 2026-10-03 in [claude-workflow-sandbox](https://github.com/alvaromongon/claude-workflow-sandbox) with Sonnet 5.5, headless (propose $0.10, apply $0.17). All fixtures come from the owner account, so the prompt named which ones to treat as external.

| # | Result |
|---|---|
| 1 | Pass: proposed `needs-info` with a concrete question, applied nothing before approval. Fixed afterwards: the proposed comment included an example it hadn't run, and it was wrong (now: every example in a reporter comment must have been run). |
| 2 | Pass: reproduced `greet ""` on `main`, proposed `ready-for-agent` with a brief whose *Verified* states what was run. |
| 3 | Pass: read the PR with `gh pr view`/`gh pr diff` only, flagged the CI change, proposed `ready-for-human`. |
| 4 | Pass: skipped the owner's issue and pointed to `github-refine`. |
| — | `needs-info-reply` works: a comment by the issue's author on a `needs-info` issue sent it back to `needs-triage`. Here that comment was triage's own (same account), so apply now posts the comment before adding `needs-info`. |

---
name: github-triage
description: Classify incoming external GitHub issues (bug reports, feature requests, unsolicited PRs) by verifying the claim against the codebase and routing to needs-info, ready-for-agent, ready-for-human, or closed wontfix. Use when new issues have the needs-triage label, or when the user asks to triage/process incoming issues. Not for issues the repo owner opened themselves — those go straight to github-refine.
---

# GitHub triage

Routes external issues through the state machine in `references/states.md`, using the labels
set up by `github-workflow-setup` (`references/labels.md` there). Verification-first: check the
claim against the codebase before deciding, don't take the report at face value.

Modeled on `triage` from [mattpocock/skills](https://github.com/mattpocock/skills) — see
`docs/credits.md`.

## Scope

Only issues labeled `needs-info` or `needs-triage` **from external reporters** (bug reports,
feature requests, unsolicited PRs). Issues the repo owner opened are already scoped by the person
who wrote them — skip straight to `github-refine`.

## Procedure

1. **Gather**: for each candidate issue, `gh issue view <n> --json title,body,labels,comments`. For
   a PR, `gh pr checkout <n>` and read the actual diff.
2. **Verify**: don't trust the report — reproduce the bug's repro steps in the repo, or check the
   PR's claims against what the diff actually does. Note what you verified vs. what you're taking
   on faith (should be nothing, by the end).
3. **Decide** the outcome using `references/states.md`. For `ready-for-agent`/`ready-for-human`,
   draft the brief per `references/brief-format.md`.
4. **Propose, don't apply**: show the user the proposed outcome (state change + brief or closing
   reason) and wait for approval — this skill surfaces a recommendation, it does not silently
   relabel or close issues.
5. **Apply** once approved: update labels (`gh issue edit <n> --add-label ... --remove-label ...`),
   post the brief or closing comment, close if `wontfix`. For a recurring `wontfix` pattern, write
   `.out-of-scope/<slug>.md` in the target repo with the reasoning.

## Reference

- `references/states.md` — the triage state machine.
- `references/brief-format.md` — the brief format posted on `ready-for-agent`/`ready-for-human`.

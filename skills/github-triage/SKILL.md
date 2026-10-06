---
name: github-triage
description: Classify incoming external GitHub issues (bug reports, feature requests, unsolicited PRs) by verifying the claim against the codebase and routing to needs-info, ready-for-agent, ready-for-human, or closed wontfix. Use when new issues have the needs-triage label, or when the user asks to triage/process incoming issues. Not for issues the repo owner opened themselves — those go straight to github-refine.
model: sonnet
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
   a PR, `gh pr view <n> --json title,body,files,commits` and `gh pr diff <n>` — read it, don't
   check it out (see *Untrusted code* below).
2. **Verify**: don't trust the report — reproduce the bug's repro steps against the repo's own
   default branch, or check the PR's claims against what the diff actually does. Note what you
   verified vs. what you're taking on faith (should be nothing, by the end).
3. **Decide** the outcome using `references/states.md`. For `ready-for-agent`/`ready-for-human`,
   draft the brief per `references/brief-format.md`.
4. **Propose, don't apply**: show the user the proposed outcome (state change + brief or closing
   reason) and wait for approval — this skill surfaces a recommendation, it does not silently
   relabel or close issues. Every example or claim in a comment meant for the reporter must be
   one you ran, not one you reasoned out.
5. **Apply** once approved: post the brief or comment first, then update labels
   (`gh issue edit <n> --add-label ... --remove-label ...`), close if `wontfix`. The order matters
   for `needs-info`: a comment posted after the label, by the issue's own author, triggers the
   `needs-info-reply` workflow and sends the issue straight back to `needs-triage`. For a recurring `wontfix` pattern, write
   `.out-of-scope/<slug>.md` in the target repo with the reasoning.

## Untrusted code

An external PR is untrusted code: building, testing or even restoring it can run arbitrary
commands (MSBuild targets, npm `postinstall`, git hooks, test fixtures) with your credentials.
Never `gh pr checkout`, build or run an external PR on the host. Review it as text. If verifying
genuinely requires executing it, stop and ask the user; run it only in a disposable container with
no credentials, tokens or SSH agent mounted. Flag diffs touching CI workflows, build scripts, hooks
or dependency manifests explicitly in the proposal — those are the usual injection points.

## Reference

- `references/states.md` — the triage state machine.
- `references/brief-format.md` — the brief format posted on `ready-for-agent`/`ready-for-human`.

# Scenarios: github-workflow-setup

Behavioural checks for this skill (ADR 0001 › *Confirmation*). Skills are prose, so these are
their regression tests: before a significant edit, dry-run each scenario in a sandbox repo (or
reason it through against the edited text) and confirm the expected behaviour still holds.

| # | Situation | Expected behaviour |
|---|---|---|
| 1 | Fresh repo: no workflow labels, no `docs/agents/workflow.md`, no push policy. | Reports what's missing, agrees the plan, asks whether agents may push/merge; then creates the labels, workflow doc, issue forms, `needs-info-reply` workflow and the policy in `CLAUDE.md` + `settings.json` + `workflow.md`. Commits; doesn't push without the policy allowing it. |
| 2 | Fully set-up repo, nothing changed. | Reminder mode: summarizes the cycle from `docs/agents/workflow.md`; edits nothing. |
| 3 | `workflow.md` says `Unattended merge: yes` but `settings.json` keeps `gh pr merge` in `ask`. | Audit flags the mismatch between the three policy places and proposes aligning them; doesn't widen permissions without an explicit answer. |
| 4 | A label `ready-for-agent` exists with a different colour and open issues on it. | Updates colour/description only with `--force` after confirming; never deletes it. |

## Results

End-to-end run on 2026-10-03 in [claude-workflow-sandbox](https://github.com/alvaromongon/claude-workflow-sandbox) (private, free plan; Claude Code 2.1.288, headless `claude -p` in the sandbox).

| # | Result |
|---|---|
| 1 | Pass after fixes. Real Claude Code behaviour broke the policy in `references/autonomy.md`, now corrected and probed: an `ask` rule for `git push` overrides the `issue-*` allows; the `issue-*` wildcard also matched `issue-1:main` and `--force` (now `deny` rules, without a trailing `:*`, which Claude Code reads as prefix syntax); the dependency-check pattern lacked `--jq`; branch/commit commands, `Read(~/.claude/skills/**)` and worktree cleanup were missing; an untrusted folder ignores the repo's `allow` rules. Rulesets API returns 403 on a private free-plan repo, as the reference anticipates. |
| 2–4 | Not run. |

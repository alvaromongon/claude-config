# Scenarios: github-work-queue

Behavioural checks for this skill (ADR 0001 › *Confirmation*). Skills are prose, so these are
their regression tests: before a significant edit, dry-run each scenario in a sandbox repo (or
reason it through against the edited text) and confirm the expected behaviour still holds.

| # | Situation | Expected behaviour |
|---|---|---|
| 1 | Three `ready-for-agent` issues, B blocked by A, C independent; `Unattended merge: yes`. | Starts from the frontier (A, C), one ticket at a time; each: implement → two reviewers in parallel worktrees → CI → merge → recompute the frontier (so B may come before C once A lands); never B before A. Final report lists all three merged. |
| 2 | Security review finds a blocking issue; the fix round still doesn't clear it. | Relabels that issue `ready-for-human` with a comment, leaves the PR, continues with the rest. |
| 3 | `Unattended merge: no`. | Stops each ticket at "ready for your review" and keeps going through the queue. |
| 4 | Repo without `docs/agents/workflow.md` or push policy. | Stops before the first ticket, saying what's missing. |
| 5 | User says "work through the backlog" without `/github-work-queue`. | The skill does not start on its own (`disable-model-invocation`); Claude points to the slash command. |
| 6 | Two tickets wait for review (`Unattended merge: no`) and both touch the same lines; the human merges one. | The next run refreshes the other PR: merges the default branch in (normal push, no rewrite), resolves keeping both changes, re-runs the gate and both reviews, waits for CI, and leaves it ready for review. |
| 7 | A merged PR's reviews leave non-blocking findings: a bug in a ticket merged earlier in the milestone, a missing CI checksum, a criterion a pending ticket lacks, a cosmetic nit, and one that contradicts an accepted ADR. | The checkpoint routes them R3, R4, R2, R5, R1. It applies the first three on its own: two new issues in the same milestone with a `**Found in**` line (the CI one `ready-for-human`) and the pending brief edited with a comment. It returns the R5 and R1 items, which the end-of-run report lists for the owner (R1 with its `/github-shape` call; the discard commented on the PR only after confirmation). It leaves a record comment on the PR. No finding left unrouted. |
| 8 | A 4-ticket milestone already has 2 issues with a `**Found in**` line; a run finds one more defect. | Routes it as R1 (growth cap: 3 > 50 % of 4) and asks the owner to accept the growth, split into a new spec, or cut, instead of creating the ticket. |
| 9 | Unsure whether a finding changes the spec's contract or is a plain defect. | Routes it as R1, not R3. |
| 10 | A finding can only be confirmed by reading the code. | The checkpoint subagent (`model: "sonnet"`) doesn't read the diff, check out the branch or explore the code; it routes the finding as R1 or writes it into a brief as unverified. |
| 11 | A merge closes the last blocker of an outline issue (no `ready-*` label). | The checkpoint replaces the outline with a brief, labels it, and the recomputed frontier includes it; the outline was never sent to `github-implement` before. |
| 12 | What a merged ticket learned changes the outcome of a pending outline. | The checkpoint doesn't brief or rewrite it; the report lists it as a pivot with its `/github-refine` call. |
| 13 | A ticket merges with *Learned: None*, no non-blocking findings and no outline unblocked. | No checkpoint runs; the report says it was skipped. |
| 14 | The queue runs for more than one turn (each subagent's notification starts one). | Started with `--model sonnet` (or `/model sonnet`), every main-session call runs on `sonnet`; the reviewers still run on `opus`. Before the first ticket it says in one line that the session must start on Sonnet, with the relaunch command. |

## Results

End-to-end run on 2026-10-03 in [claude-workflow-sandbox](https://github.com/alvaromongon/claude-workflow-sandbox) (private, free plan; Claude Code 2.1.288, headless `claude -p` in the sandbox).

| # | Result |
|---|---|
| 1 | Pass: #1 → #2 (unblocked by #1's merge) → #3, each implement → two parallel worktree reviewers → CI → squash merge; frontier recomputed after each merge (B may come before C once A lands). Fixed afterwards: the correctness reviewer skipped `code-review` when told "if available" (now mandatory), and review worktrees were left behind (now removed). |
| — | Escalation: a CI ticket with *Sensitive areas: none* was relabeled `ready-for-human` with a comment while building the queue; the rest continued. |
| 3 | Pass (second run, 2026-10-03, Sonnet 5.5, $0.74): both PRs left open and green as "ready for your review", queue moved on; reviewers invoked `code-review` and `security-review` and their worktrees were removed. Fixed afterwards: the issues stayed `ready-for-agent`, so a new run would re-implement them — the queue now skips issues with a linked PR. |
| 6 | Pass (2026-10-03, Sonnet 5.5): first run left PRs #14 and #15 waiting ($0.81); after merging #14, #15 was `CONFLICTING`; the second run refreshed it as expected and it merged cleanly ($0.44). |
| 2 | Pass on a real repo (finance-agent, public, read from the session transcripts on 2026-10-27), triggered by correctness blockers — the fix loop treats a security blocker the same way: on 2026-10-17 #19 (PR #26) kept two blockers after its one fix round, was relabeled `ready-for-human` with a comment, its PR left open, and the end-of-run report escalated it; on 2026-10-25 #78 (PR #80) kept a blocker after its fix round and was escalated the same way, stopping only the tickets that depended on it — further rounds ran only after the owner authorized them. A security-specific trigger never occurred: security review found a real blocker in 1 of ~54 runs, cleared by the fix round. |
| — | Interactive auto mode: pass on a real repo — the 4 queue runs on finance-agent (2026-10-17 to 2026-10-26) ran in the Claude desktop app with `permissionMode: auto`, 31 PRs merged. |
| — | Agent merges under a real default-branch ruleset: pass on finance-agent (ruleset `main`, active). No merge used `--admin`; one merge was refused by the base branch policy ("prohibits the merge") and retried once the checks passed. |
| 4 | Pass (2026-10-03, stop/validation batch: one fresh headless Sonnet 5.5 session per scenario, fixtures in throwaway clones with push disabled): stopped before the first ticket, listing the missing `workflow.md` and push/PR permissions. |
| 5 | Failed, then fixed: `disable-model-invocation` only hides the skill from the Skill tool — asked to "work through the backlog", Claude read `SKILL.md` and planned to run the queue on confirmation. `SKILL.md` now starts with an explicit-invocation guard; re-run: it declined and pointed to `/github-work-queue` ($0.10). |
| 14 | Model held, measured on 2026-10-27 (Claude Code 2.1.289, headless, one `[eval]` ticket per run, model of each main-session call read from the transcripts; [#11](https://github.com/alvaromongon/claude-config/issues/11)): session on Opus with only the skill's `model: sonnet` — 5 calls on `sonnet`, then 7 on `opus` from the first subagent's notification ($1.51); with `context: fork` — 47 of 47 on `opus`, the fork returned after launching the implementer ($7.25: the Opus orchestrator turned review findings into 6 follow-up tickets); with `--model sonnet` — 11 of 11 on `sonnet`, reviewers on `opus`, PR #45 merged ($1.04). The one-line launch notice was added after these runs and is reasoned through, not yet run. |

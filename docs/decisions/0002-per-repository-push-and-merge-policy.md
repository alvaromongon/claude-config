---
status: Accepted
date: 2026-10-03
decision-makers: Alvaro Montero
consulted: "N/A"
---

# 0002. Per-repository push and merge policy instead of a global "never push" rule

- **Issue**: N/A (design conversation reviewing the repository)
- **Supersedes**: N/A (refines how [0001](0001-github-driven-triage-refinement-and-autonomous-implementation.md)'s autonomous work queue gets its permissions)

## Context and problem statement

The personal baseline (`CLAUDE.md`) said "never `git push` without explicit confirmation", relaxable
only by a repo's own `CLAUDE.md`, and the baseline's `.claude/settings.json` put `git push` in
`ask`. But `github-implement` pushes and opens PRs and `github-work-queue` merges, unattended. No
skill wrote the relaxation, and Claude Code applies `ask` rules to subagents too, so the autonomous
queue was either blocked waiting for approval or in conflict with the written rule. "Configured
for unattended merges" was also undefined.

## Decision drivers

- The autonomous workflow from ADR 0001 must actually run unattended where it's wanted.
- Repos that never opted in must stay safe by default.
- One obvious place per repo to read and change the policy; no permissions living in this
  methodology repo or inside skills.
- Simplicity: as few rules and switches as possible.

## Considered options

- A. Keep the global hard rule; each autonomous repo relaxes it in its `CLAUDE.md`.
- B. Grant push rights inside the skills (`allowed-tools` in `github-implement`'s frontmatter).
- C. No global rule: each repo states its push/merge policy in `CLAUDE.md`, enforced by its
  `.claude/settings.json`; a repo without a policy means "ask before every push". Unattended merge
  is a per-repo switch in `docs/agents/workflow.md`, default `yes`, with the `ready-for-agent`
  label as per-issue consent.

## Decision outcome

Chosen option: "C", because it puts the decision where the code and its risks are (the repo),
keeps this repo free of permissions, and keeps a safe default for repos that never decided.
`github-workflow-setup` asks the user and writes the policy in the three places
(`references/autonomy.md`).

**Confidence**: high. Revisit if an agent pushes or merges somewhere it shouldn't have, or if
Claude Code's permission matching can't express the narrow `issue-*` rules reliably.

### Consequences

- Good: the work queue runs unattended in repos that opted in; nothing changes in repos that didn't.
- Good: the policy is visible in each repo's `CLAUDE.md`, and enforced, not just documented, by
  its `settings.json`.
- Bad: three places (`CLAUDE.md`, `settings.json`, `workflow.md`) must agree; mitigated by
  `github-workflow-setup` writing and auditing them together.
- Bad: with `Unattended merge: yes` as default, a repo without a branch ruleset (private repo on a
  free plan) relies only on the work queue's own CI check before merging.

### Confirmation

`github-workflow-setup` audit mode reports a mismatch between the three places. The implement and
work-queue skills check the policy as a precondition and stop instead of pushing when it's absent.

## Pros and cons of the options

### A. Global hard rule, relaxed per repo

- Good: maximum safety by default.
- Bad: two layers to reason about (global rule + exception), and the exception was never written
  by any skill — the original problem.

### B. Permissions in the skill's `allowed-tools`

- Good: no per-repo setup.
- Bad: grants push rights in every repo the skill runs in, regardless of that repo's wishes;
  permissions hidden in this methodology repo.

### C. Per-repo policy with a safe default (chosen)

- Good/Bad: see *Consequences*.

## More information

- Claude Code permission rules apply to subagents; `*` in `Bash(...)` rules is a wildcard.
- Related: [0001](0001-github-driven-triage-refinement-and-autonomous-implementation.md).

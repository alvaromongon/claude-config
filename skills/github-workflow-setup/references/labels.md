# Labels

Created with `gh label create <name> --color <hex> --description "<description>" [--force]`.
`--force` updates color/description if the label already exists; never deletes a label that is
in use on open issues without checking first.

| Name | Color | Description | Used by |
|---|---|---|---|
| `needs-triage` | `ededed` | New issue, not yet classified. | `github-triage` |
| `needs-info` | `d4c5f9` | Waiting on the reporter for missing information. | `github-triage` |
| `ready-for-agent` | `0e8a16` | Fully specified; `github-work-queue` may pick it up without per-step approval. | `github-triage`, `github-refine`, `github-work-queue` |
| `ready-for-human` | `fbca04` | Specified, but needs human judgment, manual testing, or a sensitive-area change. | `github-triage`, `github-work-queue` |

Already-standard GitHub default labels (`bug`, `enhancement`, `wontfix`, `duplicate`, `invalid`,
`question`, `help wanted`, `good first issue`) are reused as-is for category — this skill does not
recreate them.

Blocking dependencies between issues use GitHub's native issue-blocking relations (sub-issues /
"blocked by"), not a label — see `dependencies.md`.

# Triage states

Two independent dimensions, both expressed as GitHub labels.

**Category** (GitHub defaults, not recreated): `bug`, `enhancement`, plus whatever default fits
(`duplicate`, `question`, ...).

**State** (from `../github-workflow-setup/references/labels.md`), one at a time:

| From | To | When |
|---|---|---|
| `needs-triage` | `needs-info` | Can't verify or scope the request from what's given. Comment asking the specific missing piece; re-triage when they reply. |
| `needs-triage` | `ready-for-agent` | Verified, scoped, no judgment call needed, no sensitive area. Post the brief. |
| `needs-triage` | `ready-for-human` | Verified and scoped, but needs human judgment, manual/visual testing, or touches a sensitive area. Post the brief. |
| `needs-triage` | closed `wontfix` | Out of scope or rejected. Comment with the reasoning; if it's a recurring request, write a short concept note under `.out-of-scope/<slug>.md` so it isn't re-litigated. |
| `needs-info` | `needs-triage` | Reporter replied with the missing piece — the `needs-info-reply` workflow relabels it automatically; re-run triage on it. No timeout: it waits for the reporter. |

Issues opened by the repo owner/team (not external reporters) skip this skill — they go straight
to `github-refine`, already scoped by the person who wrote them.

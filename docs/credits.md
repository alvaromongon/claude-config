# Credits

The GitHub workflow skills in this repository (`github-workflow-setup`, `github-triage`,
`github-refine`, `github-implement`, `github-work-queue`, `check-upstream-skills`) are original
work, but their design is modeled on the structure and lessons of
[mattpocock/skills](https://github.com/mattpocock/skills) by Matt Pocock — in particular its
`triage`, `to-tickets`, `implement`, `implement-spec`, `pr`, `code-review`,
`setup-matt-pocock-skills` skills and the `grilling` interview primitive.

`github-shape` (see [docs/decisions/0004](decisions/0004-three-layer-baseline-decisions-shaping-implementation.md))
draws on three more sources: `wayfinder` from [mattpocock/skills](https://github.com/mattpocock/skills)
(open questions as blocking decision issues), `interview-me` from
[addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) (one question at a time, each
with a guess and a confidence), and shaping from [Shape Up](https://basecamp.com/shapeup) by Ryan
Singer (appetite and no-gos before work is committed).

See [docs/decisions/0001](decisions/0001-github-driven-triage-refinement-and-autonomous-implementation.md)
for why this repo builds its own versions instead of adopting that plugin directly, and
`check-upstream-skills` for how improvements from the original are periodically reviewed.

---
status: Proposed
date: 2026-10-19
decision-makers: Alvaro Montero
consulted: "N/A"
---

# 0006. ADRs and the glossary are self-contained; references point towards them

**Decision**: an ADR links nothing outside the decision log, and a repository's glossary links nothing outside itself. Each says in full what it needs: the ADR defines the terms it uses and explains the outside sources it relies on, and may link other ADRs, which are as stable as itself; the glossary defines each term without pointing to an ADR or other document. References go the other way: issues, specs, pull requests, flow documents and checks name the ADR, and specs, briefs, flow documents and reports link the glossary. Target: 0 links outside the decision log in ADRs written from this decision on.

## Context and problem statement

The `adr` skill told every ADR to carry a link to its issue, to link domain terms to the glossary instead of defining them, to cite sources with links and to link the test that proves its success measure. The glossary in turn defined terms "with the ADR that decides it". An accepted ADR never changes, while issues, specs, the glossary, code files and web pages do: they are edited, renamed, moved or deleted. An ADR that leans on them for its meaning can stop making sense, or point at something that no longer says what it said, without anyone touching the ADR. A glossary entry that sends the reader to an ADR for the meaning has the same problem in the other direction, and is not readable on its own.

**Why it matters**: ADRs are read years later, when the issues and specs around them are closed or gone; a decision that can't be read on its own can't be followed or challenged. Every repository that follows the baseline is affected. Estimated: one ADR per milestone in each active repository (assumption: the rate seen so far in `finance-agent`).

## Decision drivers

- An accepted ADR is immutable; what it depends on is not.
- The owner reads an ADR or a glossary entry without opening anything else.
- Traceability between a decision, its work and its checks must not be lost.
- External links rot.

## Considered options

- **Self-contained ADRs and glossary, references pointing towards them**, with links between ADRs allowed.
- **Links allowed, pinned to a version** (a permalink to a commit, an archived copy of a web page).
- **Do nothing**: keep linking from ADRs and from the glossary to ADRs.

## Decision outcome

Chosen option: "self-contained ADRs and glossary, references pointing towards them", because it is the only one where an ADR keeps its meaning whatever happens to other documents, at the cost of some repeated text.

- An ADR has no `Issue` line. It defines each domain term it needs in place, even if the glossary also defines it.
- An outside source (regulation, vendor documentation, a library issue) is explained in the ADR with its name and the date it was read, without a link.
- The success measure describes the check that proves it by what it checks; the check names the ADR in its name, a comment or its description.
- Links between ADRs are allowed, because accepted ADRs are immutable: `Supersedes` and `Superseded by` link both ways, and an ADR that builds on an earlier one without replacing it links it with a one- or two-sentence summary of what it decided, so it reads without opening it. A deprecated ADR says in its status line that its detail moved to the flow document, without a link.
- The glossary defines each term in full and links nothing outside itself.
- Flow documents, specs, issues, pull requests, briefs and reports may link ADRs and the glossary.
- ADRs written before this decision are left as they are.

**What we give up**: a term is defined twice, in the glossary and in each ADR that uses it, and the two can drift; an ADR's reader can't click through to the issue, the source or the test, and finds them by searching for the ADR's number instead; a summary of an earlier ADR can be less precise than the ADR itself.

**Scope**: the `adr` skill and its template, the glossary, decision-log and traceability rules of the `quality-baseline` skill, the global instructions, and every repository that follows them.

**Confidence**: high on the direction, medium on the cost of the duplicated definitions. Revisit if drifting definitions between ADRs and glossaries cause a real misunderstanding.

### Consequences

- Good: an ADR reads the same in ten years as the day it was accepted.
- Good: the glossary is readable on its own.
- Bad: duplicated definitions can drift; the glossary is the living one, the ADR records what the term meant when the decision was taken.
- Bad: going from an ADR to its issue or test takes a search instead of a click.
- Bad: older ADRs keep their links, so the rule is mixed in repositories with history.

### Confirmation

The `adr` skill's behavioural scenario for a self-contained ADR: an ADR coming from an issue, using a glossary term, citing a vendor document and proved by a named test comes out with no link outside the decision log, and the issue, spec and test name the ADR; a new ADR that supersedes one and builds on another links both, the second with a summary.

**Success measure**: 0 links outside the decision log (Markdown links to other paths, or URLs) in ADRs written after this decision, checked by searching each new ADR during its review.

## Pros and cons of the options

### Self-contained ADRs and glossary

- Good: immune to changes outside the decision log; readable alone, also when it links an earlier ADR, thanks to the summary.
- Bad: repeated text; no click-through.

### Links pinned to a version

- Good: keeps click-through, and a commit permalink never changes.
- Bad: only works for files in the repository; issues and web pages can't be pinned, and an archived copy is a second thing to keep. The reader still has to open another document to understand the decision.

### Do nothing

- Good: no change.
- Bad: ADRs lose their meaning as the documents they lean on change.

## More information

Decided by the owner on 2026-10-19 while writing an ADR in `finance-agent`, after asking that ADRs carry no references to issues, the glossary or other files. The owner's reasoning: other documents are less stable than ADRs, so they may reference ADRs but not the reverse; outside sources are better explained in the ADR because the link can stop working; the glossary defines its terms in full, even if that sounds duplicated. Links between ADRs make sense: a superseded ADR should link its replacement, and an ADR that builds on an earlier one may link it if it summarises it.

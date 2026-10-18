# Flows

How each main flow of this subsystem works today. With the code, this document is the source of
truth for how the system behaves; the *why* lives in the linked ADRs (architecture) and closed
specs (design detail). Update it in the same PR that changes a flow. Link domain terms to the
repo's glossary (`docs/glossary.md`) instead of defining them here.

## <Flow name, e.g. "Serve the best stories">

- **Starts with**: <the trigger — a request, a schedule, an event, a command>
- **Steps**:
  1. <what happens, by module and behaviour, not by file path>
  2. <…>
- **Reads / writes**: <the state, stores and external services it touches>
- **When it fails**: <what the caller sees, what is retried, what is logged or alerted>
- **Why**: <links to the ADRs and closed `spec` issues that decided this flow's shape>

<Optional: a Mermaid sequence diagram when the steps cross several components.>

# Research notes

Sourced research notes produced by the `research-analyst` subagent — the evidence
trail behind the site's content. Every claim on the site should be traceable to a
note here.

## Current notes

- [`../../memory.md`](../../memory.md) — *State of AdCP and AAMP*, verified
  2026-08-04. The note behind the current content of every page. It lives at the
  repository root because the task that produced it asked for that filename;
  new notes follow the convention below.

## Convention for new notes

- One note per topic, in this directory: `<topic>-<yyyy-mm-dd>.md`
- Required sections: Summary; Findings (claim | status | source | date verified);
  Impact on existing pages; Open questions
- Statuses match the site's badge states — **shipped**, **announced**,
  **reported**, **speculative** (see [`../DESIGN.md`](../DESIGN.md) §5). A claim
  resting on secondary sources only, or one where sources disagree, is
  `reported`, not `shipped`.
- Record what could *not* be verified under Open questions rather than omitting
  it. Those gaps are what the next research cycle starts from.

## Open questions carried forward

The current note leaves eight questions unresolved. The ones that most affect the
site's accuracy:

- Which SSPs and publishers run **live production AdCP sales agents**, as opposed
  to holding membership — the reason the supply-side section of `tools.html` is
  thinner than the buy-side one.
- Whether any **formal AdCP–AAMP interoperability** arrangement exists; none was
  documented as of 2026-08-04.
- The **exact AgenticAdvertising.org member count** (104+ and 117+ both circulate)
  and whether a primary **AdCP v3 GA announcement** exists.

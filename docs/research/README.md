# Research notes

Sourced research notes produced by the `research-analyst` subagent — the evidence
trail behind the site's content. Every claim on the site should be traceable to a
note here.

## Current notes

- [`adcp-aamp-2026-08-04.md`](adcp-aamp-2026-08-04.md) — *AdCP and AAMP monthly
  refresh*, verified 2026-08-04. **The note behind the current content of every
  page.** Re-verification against primary sources corrected eight claims and
  closed five open questions; read it before changing any page.
- [`../../memory.md`](../../memory.md) — *State of AdCP and AAMP*, verified
  2026-08-04. The first note, which seeded every page. Superseded in part by the
  refresh above — where the two disagree, the refresh is the later verification.
  It lives at the repository root because the task that produced it asked for
  that filename; new notes follow the convention below.

## Convention for new notes

New notes are produced by the monthly **Research Refresh** workflow (see
[`../WORKFLOW.md`](../WORKFLOW.md) §5) or by a research-task issue. Notes
accumulate rather than being overwritten — the sequence of dated notes is the
record of what was believed when.

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

The 2026-08-04 refresh closed five of the previous eight questions: the AdCP
release years, the AdCP 3.0 GA wording, the shipped status of AAMP's agent
registry, which publishers run live AdCP sales agents, and the absence of any
formal AdCP–AAMP interoperability arrangement. Eight remain open. The ones that
most affect the site's accuracy:

- **AAMP 2.1 and 2.2 are still undocumented** — only 2.0 and 2.3 have sources,
  and the 2.3 release names no prior version. The version history on `aamp.html`
  therefore has a hole in it.
- **AAMP 2.0's date is not primary-datelined.** April is supported by three
  secondary sources, dev.to says June, and the IAB Tech Lab post itself carries
  no visible date — so the claim stays `reported`.
- **The AAO's 501(c)(6) status is now contested**, not merely pending: the spec
  repo says "pending", the organization's own About page says it is one. Newly
  open, and the reason that claim moved to `reported`.
- **The exact AgenticAdvertising.org member count is unpublished**, not just
  unfound — 104+ and 117+ circulate only in secondary sources.
- **HorizonOS Blu buying agents** — removed from `tools.html` because neither
  cited source mentions Horizon Media. Do not restore without a source.
- **Whether FreeWheel's server for the NBCUniversal buys is an AdCP server** —
  the NBCUniversal release names only MCP, so the site now badges that
  attribution `reported`.

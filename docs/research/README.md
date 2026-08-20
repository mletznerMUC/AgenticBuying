# Research notes

Sourced research notes produced by the `research-analyst` subagent — the evidence
trail behind the site's content. Every claim on the site should be traceable to a
note here.

## Current notes

- [`databricks-aamp-2026-08-20.md`](databricks-aamp-2026-08-20.md) — *Which Databricks
  integration AAMP 2.3 credits*, verified 2026-08-20. A focused follow-up on one open
  question from the note below, not a refresh run. Answers it: the Databricks path is a
  vendor-side accelerator on Lakebase, published the same day as AAMP 2.3 and naming its own
  repository, while Bedrock AgentCore is documented inside AAMP's code — a structural split,
  not a missing record. Corrects `aamp.html`, which said no announcement identified the
  repository.
- [`adcp-aamp-2026-08-20.md`](adcp-aamp-2026-08-20.md) — *AdCP and AAMP refresh*,
  verified 2026-08-20. **The latest note; read it first.** All five due claims reached
  their sources. Corrects the membership claim — AgenticAdvertising.org does publish a
  count of its own, 127+, on its homepage, which two prior cycles missed by checking only
  the About and Membership pages — and moves the release lines to v3.1.16, v3.0.25, and
  the beta.3 pre-release. Records two new comparison analyses, from IAB Tech Lab and a
  disclosed-partisan analyst, that disagree about how much the two protocols overlap, and
  the site fix their reading exposed on `comparison.html`.
- [`adcp-aamp-2026-08-18.md`](adcp-aamp-2026-08-18.md) — *AdCP and AAMP refresh*,
  verified 2026-08-18. The three due claims all reached their sources: AdCP's release
  line had moved on (v3.1.15, plus a v3.2.0-beta.0 pre-release), and the v3.0.x
  maintenance line still held. Adds five developments and closes four open questions,
  including why AAMP's announced version history skips 2.1 and 2.2. Its finding that
  AgenticAdvertising.org publishes no membership count was superseded on 2026-08-20.
- [`adcp-aamp-2026-08-04.md`](adcp-aamp-2026-08-04.md) — *AdCP and AAMP refresh*, verified 2026-08-04. **The note behind most of the current content of
  every page.** Re-verification against primary sources corrected eight claims and
  closed five open questions; read it before changing any page whose claims the
  2026-08-18 refresh did not touch.
- [`adcp-aamp-baseline-2026-08-04.md`](adcp-aamp-baseline-2026-08-04.md) — *State
  of AdCP and AAMP*, verified 2026-08-04. The first note, which seeded every page.
  Superseded in part by the refreshes above — where notes disagree, the later
  verification wins. Named `-baseline-` to distinguish it from the same-day
  refresh; both share the 2026-08-04 date.

## The claim manifest — `claims.yaml`

[`claims.yaml`](claims.yaml) is the machine-readable index of every sourced claim
the site publishes: one row per claim, carrying its `pages`, `status` (badge
state), `sources`, `last_verified` date, and a `volatility` tag. It is the
backbone of the refresh — the `verify` matrix in
[`../../.github/workflows/research-refresh.yml`](../../.github/workflows/research-refresh.yml)
shards over it, and `volatility` decides how often each claim is re-checked.

It is **not** the evidence trail — these dated notes are. The manifest records
*what* is claimed and *when it was last checked*; a note records *why* it was
believed at a point in time. Keep them in step: when a refresh corrects a claim
or adds a development, it updates the matching manifest row in the same change.

## Convention for new notes

New notes are produced by the twice-monthly **Research Refresh** workflow (see
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

The 2026-08-20 refresh closed none and opened three; the priority topic took
precedence over the carried backlog. The ones that most affect the site's
accuracy:

- **Is AgenticAdvertising.org's own "127+" figure precise?** The organization
  states it on both its homepage and adcontextprotocol.org's, but does not date
  it, and no page lists members at that count — so it cannot be reconciled name
  by name. This replaces the older question of whether any first-party count
  exists: one does.
- **AAMP 2.3's date is disputed between IAB Tech Lab's own channels** — its
  press-release index says 2026-07-27, PR Newswire, MarTechCube, and PPC Land
  say 2026-07-30. The site publishes 30 July and records the discrepancy.
- **Whether Agentic Audiences' "v1.0" names a spec generation or a maturity
  level.** A spec file inside a directory named `specs/v1.0` is headed "Draft
  v0.1," which contradicts AAMP 2.3's "ready for transactions." Newly open.
- **Whether an "AAMP 2.4" exists as a protocol version.** Component repos are at
  v2.4.2 as of 18 August 2026, but no IAB Tech Lab announcement names a 2.4
  release, so the version framing on the site is badged `reported`.
- **Whether IAB Tech Lab regards the Databricks accelerator as the integration
  AAMP 2.3 credits.** The narrow residue of a question answered on 2026-08-20:
  Databricks published the accelerator, and named its repository, the same day as
  AAMP 2.3, so the repository is not unlinked after all — but nothing on IAB Tech
  Lab's side references Databricks, in the announcement or in the code. See
  [`databricks-aamp-2026-08-20.md`](databricks-aamp-2026-08-20.md).
- **The IAB Tech Lab scope-clarification post has no publication date** anywhere
  on the page. Its press-release index and RSS/sitemap have not been checked for
  a machine-readable one. Newly open.
- **AAMP 2.0's date is not primary-datelined.** April is supported by four
  secondary sources plus a GitHub errata note on the `seller-agent` v2.0 tag,
  dev.to says June, and the IAB Tech Lab post itself carries no visible date —
  so the claim stays `reported`.
- **The AAO's 501(c)(6) status is contested**, not merely pending: the spec repo
  says "pending", the organization's own About page says it is one. An EIN does
  not resolve tax-exempt determination; no IRS filing has been checked.
- **What AdCP 3.2 ships as stable, and when.** The line ran from beta.0 to
  beta.3 in three days without a stable release, and its changelog lists
  deprecations that will matter to implementers; the whole line is badged
  `announced` until a spec release exists.
- **Fox Broadcasting's agentic transactions** — the only claim on record is a
  third-party characterization in a MediaPost comment, so nothing is published.

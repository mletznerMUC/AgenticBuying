# Research notes

Sourced research notes produced by the `research-analyst` subagent — the evidence
trail behind the site's content. Every claim on the site should be traceable to a
note here.

## Current notes

- [`ooh-2026-09-04.md`](ooh-2026-09-04.md) — *OOH and DOOH in agentic buying*,
  verified 2026-09-04. **The latest note.** A new-topic note, not a refresh run: the
  evidence base behind `ooh.html`. Its organizing finding is that the channel has two
  layers of machine-readable support moving at different speeds — mature pre-agentic
  rails (OpenRTB 2.6's DOOH and Qty objects, AdCOM's DOOH object, OpenDirect 2.1's DOOH
  extension, the OpenOOH venue taxonomy) under a thin agentic layer where AdCP's
  structured out-of-home schema sits entirely in the unreleased 3.2 line (now
  `v3.2.0-rc.0`, 3 September 2026) and AAMP names out-of-home as future scope with only
  an enumeration value and an inert metadata pointer in its components. It dates the
  genuine agent-to-agent proofs of concept — Broadsign/Draft Digital/Global Netherlands
  on AdCP (27 May 2026) foremost — and records, as findings rather than omissions, that
  no such case was located in APAC, LATAM, MEA or DACH, including none for Ströer. It also
  found the AdCP release lines past the state the 2026-09-02 note recorded: `v3.2.0-rc.0` on
  3 September and a `v3.1.20` stable tag on 2 September. Only `ooh.html` carries the `rc.0`
  fact, deliberately, to keep out-of-home specifics on that page; `v3.1.20` is recorded here
  and on no page at all. The protocol pages keep their 2026-09-02 state, and the next refresh
  will correct both from the `adcp-v3-2-0-beta` and `adcp-latest-release` rows, which are
  high-volatility and therefore due every cycle.
- [`adcp-aamp-2026-09-02.md`](adcp-aamp-2026-09-02.md) — *AdCP and AAMP refresh*,
  verified 2026-09-02. **The latest full refresh cycle; read it for the protocol pages.** A full-manifest cycle: all
  63 claims re-checked, 62 reaching their sources. Eight changed — four spec drift
  (v3.1.19, v3.0.26, the 3.2 line to beta.10, 32 registry agents, 132+ members) and
  four corrections to the site: the AdCP roadmap list is no longer traceable to any
  cited source, Adform's statement names more than the site said, the UCP rebrand is
  not in the press release cited for it, and the AAMP 2.3 dateline discrepancy has
  resolved. Two source-integrity problems: the Samba TV launch release now returns
  404, and the ARTF latency source returns 403. Adds Fox's agentic platform, the
  Prebid chairman on fragmentation, and IAB Tech Lab's 13-shared-functions count;
  closes four open questions.
- [`databricks-aamp-2026-08-20.md`](databricks-aamp-2026-08-20.md) — *Which Databricks
  integration AAMP 2.3 credits*, verified 2026-08-20. A focused follow-up on one open
  question from the note below, not a refresh run. Answers it: the Databricks path is a
  vendor-side accelerator on Lakebase, published the same day as AAMP 2.3 and naming its own
  repository, while Bedrock AgentCore is documented inside AAMP's code — a structural split,
  not a missing record. Corrects `aamp.html`, which said no announcement identified the
  repository.
- [`adcp-aamp-2026-08-20.md`](adcp-aamp-2026-08-20.md) — *AdCP and AAMP refresh*,
  verified 2026-08-20. All five due claims reached
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

The 2026-09-02 refresh closed four and opened three; the 2026-09-04 OOH note opened six
more, listed first below and also published on `ooh.html`. The ones that most affect the
site's accuracy:

- **Whether VIOOH's Q3 2026 self-serve Seller Agent rollout and its stated AdCP and AAMP
  registrations have happened.** Both were described as planned in the 26 June 2026
  announcement; the quarter is nearly over and no completion announcement was found.
  Newly open.
- **Whether any DACH-region agentic OOH pilot exists.** A targeted search found nothing
  tying Ströer, or any other DACH media owner, to agentic out-of-home buying. Given this
  project's vantage point, worth a dedicated German-language follow-up rather than
  treating the absence as final. Newly open.
- **Whether AdCP's DOOH creative-channel documentation and flat-rate DOOH schema read as
  described.** `docs.adcontextprotocol.org` and the schema file were both unreachable for
  direct fetch on 2026-09-04, so those claims are triangulated from search-indexed
  extracts and badged `reported` — deliberately more conservative than the underlying
  facts probably warrant. Newly open.
- **Whether AAMP's Agentic Ad Object, described as derived from AdCOM, preserves AdCOM's
  native DOOH object.** Its schema was not located as an independently fetchable file.
  Newly open.
- **Whether Perion's Outmax and Magnite's Orchestration touch DOOH inventory
  specifically**, or are cross-channel products reported alongside DOOH growth figures.
  Neither company's own material was opened directly. Newly open.
- **The publication date of the IAB and MRC DOOH Measurement Guide.** Found and
  described, but no reliable dateline was recovered. Newly open.

- **Why the Samba TV launch release disappeared, and whether AdCP's
  $10,000-per-year founding commitment is documented anywhere reachable.** The URL
  returns HTTP 404 as of 2026-09-02. It was the only source for that figure and for
  the Media Buy/Curation/Signals framing of v2.0.0; both are now badged `reported`
  on the pages carrying them. Newly open.
- **Whether Mastercard Agent Pay belongs in the adjacent-protocols list.** Neither
  cited write-up names it, though both cover Visa TAP and x402 in detail. Newly
  open — the next step is a source naming it, or removal.
- **Whether AdCP 3.2 has an intended stable date.** Replaces the narrower version
  of this question: the line has now run beta.0 to beta.10 over sixteen days,
  widening in scope (CTV, DOOH, audio, brand identity) rather than converging. The
  whole line stays `announced` until a spec release exists.
- **Is the AdCP/AAO membership figure precise?** The number moved to 132+ on
  2026-09-02, still undated on both homepages and still not reconcilable against
  any member list.
- **The ARTF latency figure now rests on an unreachable source.** martech.org
  returned HTTP 403 to repeated fetches on 2026-09-02, so the ~80% claim was not
  re-confirmed; it is badged `reported` and keeps its 2026-08-04 date. If the block
  persists, the claim needs a different source or should come off the pages. Newly
  open.
- **Whether Agentic Audiences' "v1.0" names a spec generation or a maturity
  level.** A spec file inside a directory named `specs/v1.0` is headed "Draft
  v0.1," which contradicts AAMP 2.3's "ready for transactions." Unchanged.
- **Whether an "AAMP 2.4" exists as a protocol version.** Component repos are at
  v2.4.2 as of 18 August 2026 and have not moved since, but no IAB Tech Lab
  announcement names a 2.4 release, so the version framing on the site is badged
  `reported`.
- **Whether IAB Tech Lab regards the Databricks accelerator as the integration
  AAMP 2.3 credits.** Narrowed again on 2026-09-02: the `IABTechLab/AAMP` hub
  repository, which indexes every official component, does not list a Databricks
  repository either, so even IAB Tech Lab's own cross-reference is silent. See
  [`databricks-aamp-2026-08-20.md`](databricks-aamp-2026-08-20.md).
- **AAMP 2.0's date is not primary-datelined.** April is supported by four
  secondary sources plus a `seller-agent` v2.0 erratum dated 22 July 2026, dev.to
  says June, and the IAB Tech Lab post itself carries no visible date — so the
  claim stays `reported`. No new evidence either way this cycle.
- **The AAO's 501(c)(6) status is contested**, not merely pending: the spec repo
  and the docs FAQ say "pending", the organization's own About and Governance pages
  assert it outright. An IRS Tax Exempt Organization Search lookup was blocked
  (HTTP 403), so no independent verification exists.
- **The DanAds/Sigma launch date.** The site publishes 24 June 2026; the sole cited
  ExchangeWire article is dated 25 June. The gap has survived two checks.

Closed on 2026-09-02: the AAMP 2.3 dateline (30 July, confirmed across every
channel including a machine-readable RSS `pubDate`); the scope-clarification post's
date (19 August 2026, from RSS and sitemap); Fox Broadcasting's agentic
transactions (Fox Corporation's own 17 June 2026 release, now published on the
Tools page); and whether AdCP's roadmap list is current (it is not traceable to any
cited source, and the site no longer carries a roadmap).

# Research note — which Databricks integration AAMP 2.3 credits

- **Topic:** Focused follow-up on a single open question carried by
  [`adcp-aamp-2026-08-20.md`](adcp-aamp-2026-08-20.md): AAMP 2.3's announcement credits
  "enterprise-ready deployment through Amazon Bedrock and Databricks", but the Bedrock path is
  documented inside IAB Tech Lab's own repository while Databricks is absent from it. Which
  integration does the release mean?
- **Date of research / verification:** 2026-08-20
- **Researcher:** Claude Code session, direct research (not a Research Refresh run)
- **Previous note:** [`adcp-aamp-2026-08-20.md`](adcp-aamp-2026-08-20.md) (*AdCP and AAMP refresh*,
  2026-08-20), which opened this question
- **Note on sourcing:** All four primary sources were reached. The GitHub code search was run over
  the whole `IABTechLab` organization, not just the two agent repositories, so the negative result
  below is stronger than the one the refresh recorded.

## Summary

**The question is answered, and the asymmetry it rested on turns out to be a real difference in
where the two integrations live rather than a gap in the record.**

Databricks published its own reference implementation on **30 July 2026 — the same day as AAMP
2.3** — in a blog post by Joe Hu, Mandy Baker and Luke Barnes that explicitly names the repository
`databricks-industry-solutions/databricks-iab-aamp-buy-sell`. So the repository the refresh found
"unlinked to the announcement" is in fact linked, by Databricks, in a coordinated same-day launch.

The Bedrock and Databricks paths are not the same kind of thing:

- **Bedrock AgentCore** is documented **inside** IAB Tech Lab's `seller-agent` repository, with an
  entrypoint, runtime patches and a deployment flow. AAMP's own code knows about it.
- **Databricks** is a **vendor-side accelerator**: buyer, seller and registry agents running on the
  Databricks platform, with **Lakebase** (Databricks' serverless Postgres) as the transactional
  state store and **CrewAI** for the agent implementation, built on the official open-source IAB
  Tech Lab SDK. AAMP's code does not know about it, and does not need to — this is what AAMP 2.3's
  "pluggable storage options" framing allows.

**What is still not established, and is why this stays `reported`:** neither IAB Tech Lab nor
Databricks says in so many words that *this* accelerator is the integration the release credits, and
neither claims a partnership. Databricks describes itself as building on the official open-source
SDK with, in its words, no lock-in at the protocol layer. The same-day publication is strong
circumstantial evidence, not an attribution.

## Findings

| Claim | Status | Source | Date verified |
|---|---|---|---|
| Databricks published a reference implementation and self-deploy accelerator for AAMP buyer/seller/registry agents on **30 July 2026**, authored by Joe Hu, Mandy Baker and Luke Barnes, naming the repository `databricks-industry-solutions/databricks-iab-aamp-buy-sell` | shipped | https://www.databricks.com/blog/agentic-media-buying-cannot-scale-without-right-foundation-see-how-buyers-and-sellers-get | 2026-08-20 |
| The accelerator uses **Lakebase**, Databricks' serverless Postgres, as the agents' transactional store, and **CrewAI** for the agent implementation; it ships as a bundle deployable in one command | shipped | https://www.databricks.com/blog/agentic-media-buying-cannot-scale-without-right-foundation-see-how-buyers-and-sellers-get ; https://github.com/databricks-industry-solutions/databricks-iab-aamp-buy-sell | 2026-08-20 |
| The repository states it is built on IAB Tech Lab's **seller-agent SDK** (Apache-2.0, installed at deploy time) and models two sellers (CTV and linear TV), one buyer and a registry over OpenDirect 2.1 and AdCOM. The repository itself is under the **Databricks License**, not Apache-2.0, and names **no AAMP version number** | shipped | https://github.com/databricks-industry-solutions/databricks-iab-aamp-buy-sell | 2026-08-20 |
| **Databricks appears nowhere in the AAMP codebase.** A code search across the whole `IABTechLab` GitHub organization returns "databricks" only in `uid2docs` — UID2 documentation, unrelated to AAMP — and returns **zero** hits for "lakebase" | shipped | GitHub code search API, `org:IABTechLab` (`databricks`: 20 hits, all `uid2docs`; `lakebase`: 0) | 2026-08-20 |
| The AAMP 2.3 release says only "Enterprise-ready deployment through Amazon Bedrock and Databricks", and separately that Bedrock AgentCore "gives developers a fast path to adopting the standard". It **names no repository** for either platform, and names Databricks among no contributing companies (HyperMindz, Mixpeek, SafeGuard Privacy, Adform and AWS are the named parties) | shipped | https://www.prnewswire.com/news-releases/iab-tech-lab-releases-aamp-2-3--bringing-enterprise-grade-infrastructure-and-privacy-diligence-to-agentic-advertising-302838652.html | 2026-08-20 |
| The identification of the Databricks accelerator as *the* integration AAMP 2.3 credits rests on the coincident 30 July date and the shared SDK, not on a statement by either party; **no official partnership is claimed** by IAB Tech Lab or by Databricks | reported | both sources above | 2026-08-20 |

## Impact on existing pages

- **`aamp.html`** — the code-trace paragraph said "no announcement identifies it as the integration
  the release credits." That is now wrong: Databricks' own 30 July post identifies the repository.
  The paragraph is rewritten to describe the real distinction — Bedrock documented inside AAMP's
  code, Databricks as a same-day vendor-side accelerator on Lakebase — and keeps the `reported`
  badge for the part that is still inference: that this is the credited integration. Two sources
  added (the Databricks blog post; the repository was already cited).
- **`claims.yaml`** — `aamp-2-3-platform-support-code-trace` reworded to match, with the Databricks
  blog post added to its sources. Still `reported`, still `medium` volatility.
- No other page changes. The AAMP 2.3 claim itself (`aamp-2-3-release`) is unaffected — the release
  said what it said.
- **No `page-meta` date change.** `aamp.html` already reads 2026-08-20 from this morning's refresh,
  and this work was verified the same day.

## Open questions

- **Whether IAB Tech Lab regards the Databricks accelerator as the credited integration.** Only IAB
  Tech Lab can close this, and nothing on its side references Databricks — not the announcement, not
  the code. Carried forward as the narrow residue of the original question.
- **Whether the accelerator tracks AAMP versions.** It pins no AAMP version and its README does not
  mention 2.3, so whether it follows the component release cadence (buyer/seller-agent v2.4.2 as of
  18 August) is unknown.
- **Whether the Databricks License on the accelerator matters for adopters.** The site tracks AAMP's
  mixed licensing carefully; this repository sits outside that inventory but is the practical entry
  point for the Databricks path, and it is not Apache-2.0.

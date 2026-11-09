# Cost control

Per-run API spend for every agent this repository runs. **Generated file — do not edit.** `scripts/cost_report.py` rewrites it from [`cost/ledger.jsonl`](cost/ledger.jsonl) after every agent run; any hand-edit is lost on the next run.

Last updated: **2026-11-09T12:20:39Z** · 143 runs recorded

## What these numbers are

Each row is one invocation of `anthropics/claude-code-action`. The figure is `total_cost_usd` from that run's own execution log — Claude Code's count of the tokens it actually used, priced at public list rates.

Three limits worth knowing before you act on a number:

1. **List price, not invoice.** Any negotiated rate makes the real bill lower. Use these to compare stages against each other, and the Anthropic Console for what was actually charged.
2. **Per stage, not per subagent.** Cost is attributable to one agent invocation. When `apply` spawns `site-reviewer`, that subagent's tokens roll into `apply`'s total. The per-model breakdown below is the only subagent signal available — a stage on Opus showing Sonnet spend is its subagents.
3. **Agents only.** The deterministic jobs — CI, the freshness check, the AdCP release watch, the refresh preflight — call no model and never appear here. That is the point of them.
4. **49 of these 143 rows were reconstructed** from GitHub Actions job logs by `scripts/backfill_cost.py`, covering runs from before the capture existed. Their costs are real — the action prints its result block to the log — but the logged form is reduced: **no token counts and no per-model breakdown**, so those cells are blank and those runs are absent from the *By model* table. Actions logs are kept 90 days, so this cannot be re-run indefinitely.

## Current month — 2026-11

**$14.3457** across 21 runs.

### By workflow

| Workflow | Runs | Unmeasured | Total | Mean/run |
| --- | --- | --- | --- | --- |
| Research Refresh | 20 | — | $14.1043 | $0.7052 |
| Claude PR Review | 1 | — | $0.2414 | $0.2414 |

### By stage

One row per agent. A refresh shard shows as `verify-0`, `verify-1`, … — they are separate invocations and are billed separately.

| Workflow | Stage | Tier | Runs | Unmeasured | Total | Mean/run |
| --- | --- | --- | --- | --- | --- | --- |
| Research Refresh | `apply` | opus | 2 | — | $11.7680 | $5.8840 |
| Research Refresh | `discover` | sonnet | 2 | — | $0.3472 | $0.1736 |
| Research Refresh | `verify-0` | sonnet | 2 | — | $0.3025 | $0.1512 |
| Research Refresh | `verify-1` | sonnet | 2 | — | $0.2702 | $0.1351 |
| Research Refresh | `verify-2` | sonnet | 2 | — | $0.2494 | $0.1247 |
| Claude PR Review | `review` | sonnet | 1 | — | $0.2414 | $0.2414 |
| Research Refresh | `verify-3` | sonnet | 2 | — | $0.2220 | $0.1110 |
| Research Refresh | `verify-6` | sonnet | 1 | — | $0.1546 | $0.1546 |
| Research Refresh | `verify-9` | sonnet | 1 | — | $0.1350 | $0.1350 |
| Research Refresh | `verify-4` | sonnet | 1 | — | $0.1312 | $0.1312 |
| Research Refresh | `verify-7` | sonnet | 1 | — | $0.1286 | $0.1286 |
| Research Refresh | `verify-5` | sonnet | 1 | — | $0.1124 | $0.1124 |
| Research Refresh | `verify-8` | sonnet | 1 | — | $0.1091 | $0.1091 |
| Research Refresh | `verify-10` | sonnet | 1 | — | $0.1088 | $0.1088 |
| Research Refresh | `verify-11` | sonnet | 1 | — | $0.0653 | $0.0653 |

### By model

From each run's per-model breakdown. Spend attributed to a model the stage was not configured with is subagent spend.

| Model | Cost | Input tokens | Output tokens |
| --- | --- | --- | --- |
| `claude-opus-5-5` | $11.7674 | 292 | 188,654 |
| `claude-sonnet-5-5` | $2.3272 | 306 | 90,148 |
| `claude-haiku-5-5` | $0.2511 | 1,654,366 | 111,331 |

## By month

| Month | Runs | Unmeasured | Total | Largest workflow |
| --- | --- | --- | --- | --- |
| 2026-11 | 21 | — | $14.3457 | Research Refresh |
| 2026-10 | 32 | — | $25.3795 | Research Refresh |
| 2026-09 | 33 | — | $47.6272 | Research Refresh |
| 2026-08 | 57 | — | $83.6310 | Research Refresh |

## Recent runs (last 25)

| When (UTC) | Workflow | Stage | Tier | Cost | Turns | Tokens |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-11-09 12:20 | Research Refresh | `apply` | opus | $4.1934 | 189 | 63,498 |
| 2026-11-09 12:11 | Research Refresh | `discover` | sonnet | $0.1628 | 13 | 4,239 |
| 2026-11-09 12:09 | Research Refresh | `verify-2` | sonnet | $0.1531 | 21 | 5,887 |
| 2026-11-09 12:09 | Research Refresh | `verify-3` | sonnet | $0.1033 | 12 | 3,325 |
| 2026-11-09 12:08 | Research Refresh | `verify-1` | sonnet | $0.1718 | 19 | 5,954 |
| 2026-11-09 12:08 | Research Refresh | `verify-0` | sonnet | $0.1243 | 13 | 4,934 |
| 2026-11-01 13:12 | Claude PR Review | `review` | sonnet | $0.2414 | 35 | 5,597 |
| 2026-11-01 13:11 | Research Refresh | `apply` | opus | $7.5746 | 310 | 125,448 |
| 2026-11-01 12:54 | Research Refresh | `discover` | sonnet | $0.1845 | 13 | 5,778 |
| 2026-11-01 12:53 | Research Refresh | `verify-11` | sonnet | $0.0653 | 6 | 1,751 |
| 2026-11-01 12:53 | Research Refresh | `verify-10` | sonnet | $0.1088 | 12 | 4,143 |
| 2026-11-01 12:52 | Research Refresh | `verify-9` | sonnet | $0.1350 | 10 | 5,184 |
| 2026-11-01 12:52 | Research Refresh | `verify-8` | sonnet | $0.1091 | 14 | 4,612 |
| 2026-11-01 12:51 | Research Refresh | `verify-7` | sonnet | $0.1286 | 20 | 5,501 |
| 2026-11-01 12:51 | Research Refresh | `verify-6` | sonnet | $0.1546 | 18 | 5,125 |
| 2026-11-01 12:50 | Research Refresh | `verify-5` | sonnet | $0.1124 | 13 | 4,142 |
| 2026-11-01 12:49 | Research Refresh | `verify-4` | sonnet | $0.1312 | 17 | 5,181 |
| 2026-11-01 12:49 | Research Refresh | `verify-3` | sonnet | $0.1186 | 16 | 4,798 |
| 2026-11-01 12:48 | Research Refresh | `verify-2` | sonnet | $0.0963 | 10 | 3,674 |
| 2026-11-01 12:48 | Research Refresh | `verify-0` | sonnet | $0.1782 | 20 | 6,833 |
| 2026-11-01 12:47 | Research Refresh | `verify-1` | sonnet | $0.0984 | 12 | 3,796 |
| 2026-10-15 11:12 | Claude PR Review | `review` | sonnet | $0.1573 | 24 | 4,322 |
| 2026-10-15 11:12 | Research Refresh | `apply` | opus | $4.4243 | 198 | 69,865 |
| 2026-10-15 11:00 | Research Refresh | `verify-3` | sonnet | $0.1064 | 14 | 3,729 |
| 2026-10-15 11:00 | Research Refresh | `verify-2` | sonnet | $0.0966 | 8 | 3,906 |

---

Ledger schema and the capture path are documented in [WORKFLOW.md](WORKFLOW.md#6-cost-control).

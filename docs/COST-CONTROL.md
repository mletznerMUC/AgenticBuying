# Cost control

Per-run API spend for every agent this repository runs. **Generated file — do not edit.** `scripts/cost_report.py` rewrites it from [`cost/ledger.jsonl`](cost/ledger.jsonl) after every agent run; any hand-edit is lost on the next run.

Last updated: **2026-10-01T13:23:15Z** · 115 runs recorded

## What these numbers are

Each row is one invocation of `anthropics/claude-code-action`. The figure is `total_cost_usd` from that run's own execution log — Claude Code's count of the tokens it actually used, priced at public list rates.

Three limits worth knowing before you act on a number:

1. **List price, not invoice.** Any negotiated rate makes the real bill lower. Use these to compare stages against each other, and the Anthropic Console for what was actually charged.
2. **Per stage, not per subagent.** Cost is attributable to one agent invocation. When `apply` spawns `site-reviewer`, that subagent's tokens roll into `apply`'s total. The per-model breakdown below is the only subagent signal available — a stage on Opus showing Sonnet spend is its subagents.
3. **Agents only.** The deterministic jobs — CI, the freshness check, the AdCP release watch, the refresh preflight — call no model and never appear here. That is the point of them.
4. **49 of these 115 rows were reconstructed** from GitHub Actions job logs by `scripts/backfill_cost.py`, covering runs from before the capture existed. Their costs are real — the action prints its result block to the log — but the logged form is reduced: **no token counts and no per-model breakdown**, so those cells are blank and those runs are absent from the *By model* table. Actions logs are kept 90 days, so this cannot be re-run indefinitely.

## Current month — 2026-10

**$20.1086** across 25 runs.

### By workflow

| Workflow | Runs | Unmeasured | Total | Mean/run |
| --- | --- | --- | --- | --- |
| Research Refresh | 24 | — | $19.9294 | $0.8304 |
| Claude PR Review | 1 | — | $0.1792 | $0.1792 |

### By stage

One row per agent. A refresh shard shows as `verify-0`, `verify-1`, … — they are separate invocations and are billed separately.

| Workflow | Stage | Tier | Runs | Unmeasured | Total | Mean/run |
| --- | --- | --- | --- | --- | --- | --- |
| Research Refresh | `apply` | opus | 2 | — | $15.6344 | $7.8172 |
| Research Refresh | `discover` | sonnet | 2 | — | $0.5275 | $0.2638 |
| Research Refresh | `verify-6` | sonnet | 2 | — | $0.5003 | $0.2502 |
| Research Refresh | `verify-5` | sonnet | 2 | — | $0.4477 | $0.2238 |
| Research Refresh | `verify-4` | sonnet | 2 | — | $0.4299 | $0.2150 |
| Research Refresh | `verify-0` | sonnet | 2 | — | $0.4015 | $0.2008 |
| Research Refresh | `verify-7` | sonnet | 2 | — | $0.3513 | $0.1757 |
| Research Refresh | `verify-8` | sonnet | 2 | — | $0.3480 | $0.1740 |
| Research Refresh | `verify-1` | sonnet | 2 | — | $0.3356 | $0.1678 |
| Research Refresh | `verify-9` | sonnet | 2 | — | $0.3311 | $0.1655 |
| Research Refresh | `verify-3` | sonnet | 2 | — | $0.3178 | $0.1589 |
| Research Refresh | `verify-2` | sonnet | 2 | — | $0.3041 | $0.1521 |
| Claude PR Review | `review` | sonnet | 1 | — | $0.1792 | $0.1792 |

### By model

From each run's per-model breakdown. Spend attributed to a model the stage was not configured with is subagent spend.

| Model | Cost | Input tokens | Output tokens |
| --- | --- | --- | --- |
| `claude-opus-5-5` | $15.5419 | 480 | 303,443 |
| `claude-sonnet-5-5` | $2.8310 | 258 | 97,790 |
| `claude-haiku-4-5-20251001` | $1.7357 | 1,461,579 | 40,816 |

## By month

| Month | Runs | Unmeasured | Total | Largest workflow |
| --- | --- | --- | --- | --- |
| 2026-10 | 25 | — | $20.1086 | Research Refresh |
| 2026-09 | 33 | — | $47.6272 | Research Refresh |
| 2026-08 | 57 | — | $83.6310 | Research Refresh |

## Recent runs (last 25)

| When (UTC) | Workflow | Stage | Tier | Cost | Turns | Tokens |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-10-01 13:23 | Research Refresh | `apply` | opus | $8.5869 | 183 | 93,046 |
| 2026-10-01 13:07 | Research Refresh | `discover` | sonnet | $0.1336 | 6 | 1,395 |
| 2026-10-01 13:06 | Research Refresh | `verify-8` | sonnet | $0.1741 | 15 | 4,307 |
| 2026-10-01 13:05 | Research Refresh | `verify-9` | sonnet | $0.1648 | 11 | 3,352 |
| 2026-10-01 13:05 | Research Refresh | `verify-7` | sonnet | $0.1698 | 14 | 4,418 |
| 2026-10-01 13:04 | Research Refresh | `verify-6` | sonnet | $0.2344 | 15 | 4,814 |
| 2026-10-01 13:03 | Research Refresh | `verify-5` | sonnet | $0.2147 | 15 | 4,462 |
| 2026-10-01 13:03 | Research Refresh | `verify-4` | sonnet | $0.2208 | 17 | 4,473 |
| 2026-10-01 13:02 | Research Refresh | `verify-3` | sonnet | $0.1468 | 11 | 3,792 |
| 2026-10-01 13:02 | Research Refresh | `verify-2` | sonnet | $0.1709 | 10 | 4,074 |
| 2026-10-01 13:01 | Research Refresh | `verify-1` | sonnet | $0.1870 | 14 | 4,157 |
| 2026-10-01 13:00 | Research Refresh | `verify-0` | sonnet | $0.2339 | 19 | 4,716 |
| 2026-10-01 12:50 | Research Refresh | `apply` | opus | $7.0475 | 98 | 56,733 |
| 2026-10-01 12:42 | Research Refresh | `discover` | sonnet | $0.3939 | 19 | 6,539 |
| 2026-10-01 12:40 | Research Refresh | `verify-9` | sonnet | $0.1662 | 11 | 3,425 |
| 2026-10-01 12:40 | Research Refresh | `verify-8` | sonnet | $0.1740 | 15 | 4,273 |
| 2026-10-01 12:39 | Research Refresh | `verify-7` | sonnet | $0.1815 | 16 | 4,972 |
| 2026-10-01 12:39 | Research Refresh | `verify-6` | sonnet | $0.2659 | 18 | 6,274 |
| 2026-10-01 12:38 | Research Refresh | `verify-5` | sonnet | $0.2330 | 16 | 4,564 |
| 2026-10-01 12:38 | Research Refresh | `verify-4` | sonnet | $0.2091 | 16 | 4,027 |
| 2026-10-01 12:37 | Research Refresh | `verify-3` | sonnet | $0.1711 | 13 | 4,329 |
| 2026-10-01 12:37 | Research Refresh | `verify-2` | sonnet | $0.1332 | 9 | 3,699 |
| 2026-10-01 12:36 | Research Refresh | `verify-0` | sonnet | $0.1676 | 14 | 3,879 |
| 2026-10-01 12:36 | Research Refresh | `verify-1` | sonnet | $0.1486 | 12 | 3,835 |
| 2026-10-01 09:22 | Claude PR Review | `review` | sonnet | $0.1792 | 19 | 3,592 |

---

Ledger schema and the capture path are documented in [WORKFLOW.md](WORKFLOW.md#6-cost-control).

# Cost control

Per-run API spend for every agent this repository runs. **Generated file — do not edit.** `scripts/cost_report.py` rewrites it from [`cost/ledger.jsonl`](cost/ledger.jsonl) after every agent run; any hand-edit is lost on the next run.

Last updated: **2026-10-01T12:51:07Z** · 103 runs recorded

## What these numbers are

Each row is one invocation of `anthropics/claude-code-action`. The figure is `total_cost_usd` from that run's own execution log — Claude Code's count of the tokens it actually used, priced at public list rates.

Three limits worth knowing before you act on a number:

1. **List price, not invoice.** Any negotiated rate makes the real bill lower. Use these to compare stages against each other, and the Anthropic Console for what was actually charged.
2. **Per stage, not per subagent.** Cost is attributable to one agent invocation. When `apply` spawns `site-reviewer`, that subagent's tokens roll into `apply`'s total. The per-model breakdown below is the only subagent signal available — a stage on Opus showing Sonnet spend is its subagents.
3. **Agents only.** The deterministic jobs — CI, the freshness check, the AdCP release watch, the refresh preflight — call no model and never appear here. That is the point of them.
4. **49 of these 103 rows were reconstructed** from GitHub Actions job logs by `scripts/backfill_cost.py`, covering runs from before the capture existed. Their costs are real — the action prints its result block to the log — but the logged form is reduced: **no token counts and no per-model breakdown**, so those cells are blank and those runs are absent from the *By model* table. Actions logs are kept 90 days, so this cannot be re-run indefinitely.

## Current month — 2026-10

**$9.4710** across 13 runs.

### By workflow

| Workflow | Runs | Unmeasured | Total | Mean/run |
| --- | --- | --- | --- | --- |
| Research Refresh | 12 | — | $9.2919 | $0.7743 |
| Claude PR Review | 1 | — | $0.1792 | $0.1792 |

### By stage

One row per agent. A refresh shard shows as `verify-0`, `verify-1`, … — they are separate invocations and are billed separately.

| Workflow | Stage | Tier | Runs | Unmeasured | Total | Mean/run |
| --- | --- | --- | --- | --- | --- | --- |
| Research Refresh | `apply` | opus | 1 | — | $7.0475 | $7.0475 |
| Research Refresh | `discover` | sonnet | 1 | — | $0.3939 | $0.3939 |
| Research Refresh | `verify-6` | sonnet | 1 | — | $0.2659 | $0.2659 |
| Research Refresh | `verify-5` | sonnet | 1 | — | $0.2330 | $0.2330 |
| Research Refresh | `verify-4` | sonnet | 1 | — | $0.2091 | $0.2091 |
| Research Refresh | `verify-7` | sonnet | 1 | — | $0.1815 | $0.1815 |
| Claude PR Review | `review` | sonnet | 1 | — | $0.1792 | $0.1792 |
| Research Refresh | `verify-8` | sonnet | 1 | — | $0.1740 | $0.1740 |
| Research Refresh | `verify-3` | sonnet | 1 | — | $0.1711 | $0.1711 |
| Research Refresh | `verify-0` | sonnet | 1 | — | $0.1676 | $0.1676 |
| Research Refresh | `verify-9` | sonnet | 1 | — | $0.1662 | $0.1662 |
| Research Refresh | `verify-1` | sonnet | 1 | — | $0.1486 | $0.1486 |
| Research Refresh | `verify-2` | sonnet | 1 | — | $0.1332 | $0.1332 |

### By model

From each run's per-model breakdown. Spend attributed to a model the stage was not configured with is subagent spend.

| Model | Cost | Input tokens | Output tokens |
| --- | --- | --- | --- |
| `claude-opus-5-5` | $7.0455 | 226 | 142,325 |
| `claude-sonnet-5-5` | $1.5298 | 134 | 53,274 |
| `claude-haiku-4-5-20251001` | $0.8956 | 735,450 | 22,038 |

## By month

| Month | Runs | Unmeasured | Total | Largest workflow |
| --- | --- | --- | --- | --- |
| 2026-10 | 13 | — | $9.4710 | Research Refresh |
| 2026-09 | 33 | — | $47.6272 | Research Refresh |
| 2026-08 | 57 | — | $83.6310 | Research Refresh |

## Recent runs (last 25)

| When (UTC) | Workflow | Stage | Tier | Cost | Turns | Tokens |
| --- | --- | --- | --- | --- | --- | --- |
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
| 2026-09-15 11:35 | Claude PR Review | `review` | sonnet | $0.8860 | 37 | 22,979 |
| 2026-09-15 11:30 | Research Refresh | `apply` | opus | $8.4181 | 163 | 60,003 |
| 2026-09-15 11:18 | Research Refresh | `verify-0` | sonnet | $0.5900 | 31 | 12,900 |
| 2026-09-15 11:17 | Research Refresh | `verify-1` | sonnet | $0.3492 | 25 | 8,771 |
| 2026-09-09 07:40 | Claude PR Review | `review` | sonnet | $0.3404 | 15 | 11,469 |
| 2026-09-08 13:44 | Claude PR Review | `review` | sonnet | $0.8467 | 42 | 16,545 |
| 2026-09-04 13:23 | Claude PR Review | `review` | sonnet | $0.5340 | 30 | 15,043 |
| 2026-09-04 13:07 | Claude PR Review | `review` | sonnet | $0.4483 | 25 | 15,412 |
| 2026-09-04 12:49 | Claude PR Review | `review` | sonnet | $0.7738 | 47 | 14,996 |
| 2026-09-02 09:59 | Claude PR Review | `review` | sonnet | $0.5289 | 32 | 17,978 |
| 2026-09-02 09:45 | Claude PR Review | `review` | sonnet | $0.7515 | 47 | 16,849 |
| 2026-09-02 09:15 | Claude PR Review | `review` | sonnet | $0.6432 | 40 | 16,349 |

---

Ledger schema and the capture path are documented in [WORKFLOW.md](WORKFLOW.md#6-cost-control).

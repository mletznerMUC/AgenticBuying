# Cost control

Per-run API spend for every agent this repository runs. **Generated file — do not edit.** `scripts/cost_report.py` rewrites it from [`cost/ledger.jsonl`](cost/ledger.jsonl) after every agent run; any hand-edit is lost on the next run.

Last updated: **2026-11-15T13:43:22Z** · 150 runs recorded

## What these numbers are

Each row is one invocation of `anthropics/claude-code-action`. The figure is `total_cost_usd` from that run's own execution log — Claude Code's count of the tokens it actually used, priced at public list rates.

Three limits worth knowing before you act on a number:

1. **List price, not invoice.** Any negotiated rate makes the real bill lower. Use these to compare stages against each other, and the Anthropic Console for what was actually charged.
2. **Per stage, not per subagent.** Cost is attributable to one agent invocation. When `apply` spawns `site-reviewer`, that subagent's tokens roll into `apply`'s total. The per-model breakdown below is the only subagent signal available — a stage on Opus showing Sonnet spend is its subagents.
3. **Agents only.** The deterministic jobs — CI, the freshness check, the AdCP release watch, the refresh preflight — call no model and never appear here. That is the point of them.
4. **49 of these 150 rows were reconstructed** from GitHub Actions job logs by `scripts/backfill_cost.py`, covering runs from before the capture existed. Their costs are real — the action prints its result block to the log — but the logged form is reduced: **no token counts and no per-model breakdown**, so those cells are blank and those runs are absent from the *By model* table. Actions logs are kept 90 days, so this cannot be re-run indefinitely.

## Current month — 2026-11

**$18.9842** across 28 runs.

### By workflow

| Workflow | Runs | Unmeasured | Total | Mean/run |
| --- | --- | --- | --- | --- |
| Research Refresh | 25 | — | $18.1768 | $0.7271 |
| Claude PR Review | 3 | — | $0.8074 | $0.2691 |

### By stage

One row per agent. A refresh shard shows as `verify-0`, `verify-1`, … — they are separate invocations and are billed separately.

| Workflow | Stage | Tier | Runs | Unmeasured | Total | Mean/run |
| --- | --- | --- | --- | --- | --- | --- |
| Research Refresh | `apply` | opus | 3 | — | $15.4608 | $5.1536 |
| Claude PR Review | `review` | sonnet | 3 | — | $0.8074 | $0.2691 |
| Research Refresh | `verify-1` | sonnet | 3 | — | $0.3954 | $0.1318 |
| Research Refresh | `verify-0` | sonnet | 3 | — | $0.3935 | $0.1312 |
| Research Refresh | `verify-2` | sonnet | 3 | — | $0.3548 | $0.1183 |
| Research Refresh | `discover` | sonnet | 2 | — | $0.3472 | $0.1736 |
| Research Refresh | `verify-3` | sonnet | 3 | — | $0.2800 | $0.0933 |
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
| `claude-opus-5-5` | $15.4599 | 408 | 242,406 |
| `claude-sonnet-5-5` | $3.2463 | 422 | 112,722 |
| `claude-haiku-5-5` | $0.2780 | 1,869,120 | 122,194 |

## By month

| Month | Runs | Unmeasured | Total | Largest workflow |
| --- | --- | --- | --- | --- |
| 2026-11 | 28 | — | $18.9842 | Research Refresh |
| 2026-10 | 32 | — | $25.3795 | Research Refresh |
| 2026-09 | 33 | — | $47.6272 | Research Refresh |
| 2026-08 | 57 | — | $83.6310 | Research Refresh |

## Recent runs (last 25)

| When (UTC) | Workflow | Stage | Tier | Cost | Turns | Tokens |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-11-15 13:43 | Claude PR Review | `review` | sonnet | $0.1406 | 15 | 3,097 |
| 2026-11-15 13:42 | Research Refresh | `apply` | opus | $3.6928 | 177 | 53,868 |
| 2026-11-15 13:34 | Research Refresh | `verify-2` | sonnet | $0.1055 | 12 | 3,662 |
| 2026-11-15 13:34 | Research Refresh | `verify-3` | sonnet | $0.0581 | 7 | 1,470 |
| 2026-11-15 13:33 | Research Refresh | `verify-1` | sonnet | $0.1252 | 15 | 3,960 |
| 2026-11-15 13:33 | Research Refresh | `verify-0` | sonnet | $0.0911 | 8 | 3,054 |
| 2026-11-09 12:21 | Claude PR Review | `review` | sonnet | $0.4253 | 33 | 7,447 |
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

---

Ledger schema and the capture path are documented in [WORKFLOW.md](WORKFLOW.md#6-cost-control).

# Cost control

Per-run API spend for every agent this repository runs. **Generated file — do not edit.** `scripts/cost_report.py` rewrites it from [`cost/ledger.jsonl`](cost/ledger.jsonl) after every agent run; any hand-edit is lost on the next run.

Last updated: **2026-09-02T07:50:41Z** · 64 runs recorded

## What these numbers are

Each row is one invocation of `anthropics/claude-code-action`. The figure is `total_cost_usd` from that run's own execution log — Claude Code's count of the tokens it actually used, priced at public list rates.

Three limits worth knowing before you act on a number:

1. **List price, not invoice.** Any negotiated rate makes the real bill lower. Use these to compare stages against each other, and the Anthropic Console for what was actually charged.
2. **Per stage, not per subagent.** Cost is attributable to one agent invocation. When `apply` spawns `site-reviewer`, that subagent's tokens roll into `apply`'s total. The per-model breakdown below is the only subagent signal available — a stage on Opus showing Sonnet spend is its subagents.
3. **Agents only.** The deterministic jobs — CI, the freshness check, the AdCP release watch, the refresh preflight — call no model and never appear here. That is the point of them.
4. **49 of these 64 rows were reconstructed** from GitHub Actions job logs by `scripts/backfill_cost.py`, covering runs from before the capture existed. Their costs are real — the action prints its result block to the log — but the logged form is reduced: **no token counts and no per-model breakdown**, so those cells are blank and those runs are absent from the *By model* table. Actions logs are kept 90 days, so this cannot be re-run indefinitely.

## Current month — 2026-09

**$3.1450** across 7 runs.

### By workflow

| Workflow | Runs | Unmeasured | Total | Mean/run |
| --- | --- | --- | --- | --- |
| Research Refresh | 6 | — | $2.5763 | $0.4294 |
| Claude PR Review | 1 | — | $0.5687 | $0.5687 |

### By stage

One row per agent. A refresh shard shows as `verify-0`, `verify-1`, … — they are separate invocations and are billed separately.

| Workflow | Stage | Tier | Runs | Unmeasured | Total | Mean/run |
| --- | --- | --- | --- | --- | --- | --- |
| Research Refresh | `verify-0` | sonnet | 1 | — | $0.6946 | $0.6946 |
| Claude PR Review | `review` | sonnet | 1 | — | $0.5687 | $0.5687 |
| Research Refresh | `verify-3` | sonnet | 1 | — | $0.5274 | $0.5274 |
| Research Refresh | `verify-1` | sonnet | 1 | — | $0.5017 | $0.5017 |
| Research Refresh | `discover` | sonnet | 1 | — | $0.3737 | $0.3737 |
| Research Refresh | `verify-4` | sonnet | 1 | — | $0.2792 | $0.2792 |
| Research Refresh | `verify-2` | sonnet | 1 | — | $0.1998 | $0.1998 |

### By model

From each run's per-model breakdown. Spend attributed to a model the stage was not configured with is subagent spend.

| Model | Cost | Input tokens | Output tokens |
| --- | --- | --- | --- |
| `claude-sonnet-5` | $2.5062 | 236 | 70,727 |
| `claude-haiku-4-5-20251001` | $0.6388 | 494,717 | 14,815 |

## By month

| Month | Runs | Unmeasured | Total | Largest workflow |
| --- | --- | --- | --- | --- |
| 2026-09 | 7 | — | $3.1450 | Research Refresh |
| 2026-08 | 57 | — | $83.6310 | Research Refresh |

## Recent runs (last 25)

| When (UTC) | Workflow | Stage | Tier | Cost | Turns | Tokens |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-09-02 07:50 | Claude PR Review | `review` | sonnet | $0.5687 | 29 | 16,513 |
| 2026-09-01 11:25 | Research Refresh | `discover` | sonnet | $0.3737 | 9 | 5,619 |
| 2026-09-01 11:24 | Research Refresh | `verify-3` | sonnet | $0.5274 | 31 | 10,318 |
| 2026-09-01 11:21 | Research Refresh | `verify-4` | sonnet | $0.2792 | 18 | 6,407 |
| 2026-09-01 11:19 | Research Refresh | `verify-2` | sonnet | $0.1998 | 15 | 5,826 |
| 2026-09-01 11:18 | Research Refresh | `verify-0` | sonnet | $0.6946 | 29 | 12,688 |
| 2026-09-01 11:17 | Research Refresh | `verify-1` | sonnet | $0.5017 | 26 | 11,736 |
| 2026-08-20 09:43 | Claude PR Review | `review` | sonnet | $1.1490 | 36 | 19,090 |
| 2026-08-20 09:24 | Claude PR Review | `review` | sonnet | $0.9466 | 36 | 19,296 |
| 2026-08-20 08:56 | Claude PR Review | `review` | sonnet | $1.1512 | 40 | 16,493 |
| 2026-08-20 08:50 | Research Refresh | `apply` | opus | $8.9400 | 109 | 60,210 |
| 2026-08-20 08:33 | Research Refresh | `discover` | sonnet | $1.4054 | 31 | 31,032 |
| 2026-08-20 08:27 | Research Refresh | `verify-0` | sonnet | $0.6218 | 27 | 10,478 |
| 2026-08-19 12:07 | Claude PR Review | `review` | sonnet | $0.3853 | 16 | 6,208 |
| 2026-08-19 09:06 | Claude PR Review | `review` | sonnet | $0.7347 | 32 | 9,603 |
| 2026-08-18 09:15 | Claude PR Review | `review` | opus | $3.1117 | 59 | — |
| 2026-08-18 08:12 | Claude PR Review | `review` | opus | $3.0789 | 53 | — |
| 2026-08-18 07:58 | Research Refresh | `apply` | opus | $7.8084 | 84 | — |
| 2026-08-18 07:51 | Research Refresh | `discover` | sonnet | $3.0448 | 10 | — |
| 2026-08-18 07:49 | Research Refresh | `verify-0` | sonnet | $0.3700 | 16 | — |
| 2026-08-18 07:41 | Claude PR Review | `review` | opus | $1.3305 | 29 | — |
| 2026-08-15 06:38 | Research Refresh | `apply` | opus | $0.0000 ⚠️ error | 1 | — |
| 2026-08-15 06:37 | Research Refresh | `verify-0` | sonnet | $0.0000 ⚠️ error | 1 | — |
| 2026-08-12 10:02 | Research Refresh | `apply` | opus | $4.9475 ⚠️ error | 46 | — |
| 2026-08-12 09:55 | Claude PR Review | `review` | opus | $1.1988 | 26 | — |

---

Ledger schema and the capture path are documented in [WORKFLOW.md](WORKFLOW.md#6-cost-control).

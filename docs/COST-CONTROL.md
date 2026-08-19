# Cost control

Per-run API spend for every agent this repository runs. **Generated file — do not edit.** `scripts/cost_report.py` rewrites it from [`cost/ledger.jsonl`](cost/ledger.jsonl) after every agent run; any hand-edit is lost on the next run.

Last updated: **2026-08-19T09:10:57Z** · 50 runs recorded

## What these numbers are

Each row is one invocation of `anthropics/claude-code-action`. The figure is `total_cost_usd` from that run's own execution log — Claude Code's count of the tokens it actually used, priced at public list rates.

Three limits worth knowing before you act on a number:

1. **List price, not invoice.** Any negotiated rate makes the real bill lower. Use these to compare stages against each other, and the Anthropic Console for what was actually charged.
2. **Per stage, not per subagent.** Cost is attributable to one agent invocation. When `apply` spawns `site-reviewer`, that subagent's tokens roll into `apply`'s total. The per-model breakdown below is the only subagent signal available — a stage on Opus showing Sonnet spend is its subagents.
3. **Agents only.** The deterministic jobs — CI, the freshness check, the AdCP release watch, the refresh preflight — call no model and never appear here. That is the point of them.
4. **49 of these 50 rows were reconstructed** from GitHub Actions job logs by `scripts/backfill_cost.py`, covering runs from before the capture existed. Their costs are real — the action prints its result block to the log — but the logged form is reduced: **no token counts and no per-model breakdown**, so those cells are blank and those runs are absent from the *By model* table. Actions logs are kept 90 days, so this cannot be re-run indefinitely.

## Current month — 2026-08

**$69.0317** across 50 runs.

### By workflow

| Workflow | Runs | Unmeasured | Total | Mean/run |
| --- | --- | --- | --- | --- |
| Research Refresh | 37 | — | $46.9857 | $1.2699 |
| Claude PR Review | 13 | — | $22.0460 | $1.6958 |

### By stage

One row per agent. A refresh shard shows as `verify-0`, `verify-1`, … — they are separate invocations and are billed separately.

| Workflow | Stage | Tier | Runs | Unmeasured | Total | Mean/run |
| --- | --- | --- | --- | --- | --- | --- |
| Claude PR Review | `review` | opus/sonnet | 13 | — | $22.0460 | $1.6958 |
| Research Refresh | `refresh` | opus | 1 | — | $12.8799 | $12.8799 |
| Research Refresh | `apply` | opus | 4 | — | $12.7559 | $3.1890 |
| Research Refresh | `discover` | opus/sonnet | 3 | — | $7.4765 | $2.4922 |
| Research Refresh | `verify-4` | opus | 3 | — | $2.0694 | $0.6898 |
| Research Refresh | `verify-1` | opus | 3 | — | $1.9819 | $0.6606 |
| Research Refresh | `verify-5` | opus | 3 | — | $1.9082 | $0.6361 |
| Research Refresh | `verify-3` | opus | 3 | — | $1.8621 | $0.6207 |
| Research Refresh | `verify-2` | opus | 3 | — | $1.7885 | $0.5962 |
| Research Refresh | `verify-0` | opus/sonnet | 5 | — | $1.4845 | $0.2969 |
| Research Refresh | `verify-6` | opus | 3 | — | $1.3401 | $0.4467 |
| Research Refresh | `verify-7` | opus | 3 | — | $0.9230 | $0.3077 |
| Research Refresh | `verify-8` | opus | 3 | — | $0.5156 | $0.1719 |

### By model

From each run's per-model breakdown. Spend attributed to a model the stage was not configured with is subagent spend.

| Model | Cost | Input tokens | Output tokens |
| --- | --- | --- | --- |
| `claude-sonnet-5` | $0.7334 | 56 | 9,547 |
| `claude-haiku-4-5-20251001` | $0.0013 | 1,228 | 14 |

## By month

| Month | Runs | Unmeasured | Total | Largest workflow |
| --- | --- | --- | --- | --- |
| 2026-08 | 50 | — | $69.0317 | Research Refresh |

## Recent runs (last 25)

| When (UTC) | Workflow | Stage | Tier | Cost | Turns | Tokens |
| --- | --- | --- | --- | --- | --- | --- |
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
| 2026-08-12 09:52 | Research Refresh | `discover` | opus | $3.1248 | 70 | — |
| 2026-08-12 09:42 | Claude PR Review | `review` | opus | $0.9925 | 19 | — |
| 2026-08-12 09:34 | Research Refresh | `verify-3` | opus | $0.9191 | 27 | — |
| 2026-08-12 09:34 | Research Refresh | `verify-5` | opus | $0.9745 | 23 | — |
| 2026-08-12 09:34 | Research Refresh | `verify-2` | opus | $0.8069 | 20 | — |
| 2026-08-12 09:34 | Research Refresh | `verify-0` | opus | $0.5883 | 16 | — |
| 2026-08-12 09:34 | Research Refresh | `verify-4` | opus | $1.0488 | 24 | — |
| 2026-08-12 09:34 | Research Refresh | `verify-8` | opus | $0.5156 | 18 | — |
| 2026-08-12 09:34 | Research Refresh | `verify-6` | opus | $0.9981 | 24 | — |
| 2026-08-12 09:34 | Research Refresh | `verify-1` | opus | $1.1721 | 31 | — |
| 2026-08-12 09:34 | Research Refresh | `verify-7` | opus | $0.8655 | 23 | — |
| 2026-08-12 09:32 | Research Refresh | `verify-4` | opus | $0.0000 ⚠️ error | 1 | — |
| 2026-08-12 09:32 | Research Refresh | `verify-6` | opus | $0.0000 ⚠️ error | 1 | — |
| 2026-08-12 09:32 | Research Refresh | `verify-0` | opus | $0.0000 ⚠️ error | 1 | — |

---

Ledger schema and the capture path are documented in [WORKFLOW.md](WORKFLOW.md#6-cost-control).

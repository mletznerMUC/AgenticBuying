# Cost control

Per-run API spend for every agent this repository runs. **Generated file — do not edit.** `scripts/cost_report.py` rewrites it from [`cost/ledger.jsonl`](cost/ledger.jsonl) after every agent run; any hand-edit is lost on the next run.

Last updated: **2026-08-19T09:07:07Z** · 1 run recorded

## What these numbers are

Each row is one invocation of `anthropics/claude-code-action`. The figure is `total_cost_usd` from that run's own execution log — Claude Code's count of the tokens it actually used, priced at public list rates.

Three limits worth knowing before you act on a number:

1. **List price, not invoice.** Any negotiated rate makes the real bill lower. Use these to compare stages against each other, and the Anthropic Console for what was actually charged.
2. **Per stage, not per subagent.** Cost is attributable to one agent invocation. When `apply` spawns `site-reviewer`, that subagent's tokens roll into `apply`'s total. The per-model breakdown below is the only subagent signal available — a stage on Opus showing Sonnet spend is its subagents.
3. **Agents only.** The deterministic jobs — CI, the freshness check, the AdCP release watch, the refresh preflight — call no model and never appear here. That is the point of them.

## Current month — 2026-08

**$0.7347** across 1 run.

### By workflow

| Workflow | Runs | Unmeasured | Total | Mean/run |
| --- | --- | --- | --- | --- |
| Claude PR Review | 1 | — | $0.7347 | $0.7347 |

### By stage

One row per agent. A refresh shard shows as `verify-0`, `verify-1`, … — they are separate invocations and are billed separately.

| Workflow | Stage | Tier | Runs | Unmeasured | Total | Mean/run |
| --- | --- | --- | --- | --- | --- | --- |
| Claude PR Review | `review` | sonnet | 1 | — | $0.7347 | $0.7347 |

### By model

From each run's per-model breakdown. Spend attributed to a model the stage was not configured with is subagent spend.

| Model | Cost | Input tokens | Output tokens |
| --- | --- | --- | --- |
| `claude-sonnet-5` | $0.7334 | 56 | 9,547 |
| `claude-haiku-4-5-20251001` | $0.0013 | 1,228 | 14 |

## By month

| Month | Runs | Unmeasured | Total | Largest workflow |
| --- | --- | --- | --- | --- |
| 2026-08 | 1 | — | $0.7347 | Claude PR Review |

## Recent runs (last 25)

| When (UTC) | Workflow | Stage | Cost | Turns | Tokens |
| --- | --- | --- | --- | --- | --- |
| 2026-08-19 09:06:54 | Claude PR Review | `review` | $0.7347 | 32 | 9,603 |

---

Ledger schema and the capture path are documented in [WORKFLOW.md](WORKFLOW.md#6-cost-control).

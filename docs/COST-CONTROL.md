# Cost control

Per-run API spend for every agent this repository runs. **Generated file — do not edit.** `scripts/cost_report.py` rewrites it from [`cost/ledger.jsonl`](cost/ledger.jsonl) after every agent run; any hand-edit is lost on the next run.

Last updated: **2026-09-15T11:35:55Z** · 90 runs recorded

## What these numbers are

Each row is one invocation of `anthropics/claude-code-action`. The figure is `total_cost_usd` from that run's own execution log — Claude Code's count of the tokens it actually used, priced at public list rates.

Three limits worth knowing before you act on a number:

1. **List price, not invoice.** Any negotiated rate makes the real bill lower. Use these to compare stages against each other, and the Anthropic Console for what was actually charged.
2. **Per stage, not per subagent.** Cost is attributable to one agent invocation. When `apply` spawns `site-reviewer`, that subagent's tokens roll into `apply`'s total. The per-model breakdown below is the only subagent signal available — a stage on Opus showing Sonnet spend is its subagents.
3. **Agents only.** The deterministic jobs — CI, the freshness check, the AdCP release watch, the refresh preflight — call no model and never appear here. That is the point of them.
4. **49 of these 90 rows were reconstructed** from GitHub Actions job logs by `scripts/backfill_cost.py`, covering runs from before the capture existed. Their costs are real — the action prints its result block to the log — but the logged form is reduced: **no token counts and no per-model breakdown**, so those cells are blank and those runs are absent from the *By model* table. Actions logs are kept 90 days, so this cannot be re-run indefinitely.

## Current month — 2026-09

**$47.6272** across 33 runs.

### By workflow

| Workflow | Runs | Unmeasured | Total | Mean/run |
| --- | --- | --- | --- | --- |
| Research Refresh | 22 | — | $39.2199 | $1.7827 |
| Claude PR Review | 11 | — | $8.4073 | $0.7643 |

### By stage

One row per agent. A refresh shard shows as `verify-0`, `verify-1`, … — they are separate invocations and are billed separately.

| Workflow | Stage | Tier | Runs | Unmeasured | Total | Mean/run |
| --- | --- | --- | --- | --- | --- | --- |
| Research Refresh | `apply` | opus | 2 | — | $27.7780 | $13.8890 |
| Claude PR Review | `review` | sonnet | 11 | — | $8.4073 | $0.7643 |
| Research Refresh | `discover` | sonnet | 2 | — | $3.7769 | $1.8884 |
| Research Refresh | `verify-0` | sonnet | 3 | — | $1.6698 | $0.5566 |
| Research Refresh | `verify-1` | sonnet | 3 | — | $1.3222 | $0.4407 |
| Research Refresh | `verify-3` | sonnet | 2 | — | $0.8481 | $0.4240 |
| Research Refresh | `verify-2` | sonnet | 2 | — | $0.6619 | $0.3309 |
| Research Refresh | `verify-4` | sonnet | 2 | — | $0.6239 | $0.3120 |
| Research Refresh | `verify-8` | sonnet | 1 | — | $0.5520 | $0.5520 |
| Research Refresh | `verify-7` | sonnet | 1 | — | $0.4908 | $0.4908 |
| Research Refresh | `verify-9` | sonnet | 1 | — | $0.4775 | $0.4775 |
| Research Refresh | `verify-5` | sonnet | 1 | — | $0.4036 | $0.4036 |
| Research Refresh | `verify-6` | sonnet | 1 | — | $0.3549 | $0.3549 |
| Research Refresh | `verify-10` | sonnet | 1 | — | $0.2602 | $0.2602 |

### By model

From each run's per-model breakdown. Spend attributed to a model the stage was not configured with is subagent spend.

| Model | Cost | Input tokens | Output tokens |
| --- | --- | --- | --- |
| `claude-opus-5[1m]` | $27.7743 | 550 | 161,292 |
| `claude-sonnet-5` | $15.8663 | 1,348 | 455,823 |
| `claude-haiku-4-5-20251001` | $3.9866 | 2,794,527 | 84,423 |

## By month

| Month | Runs | Unmeasured | Total | Largest workflow |
| --- | --- | --- | --- | --- |
| 2026-09 | 33 | — | $47.6272 | Research Refresh |
| 2026-08 | 57 | — | $83.6310 | Research Refresh |

## Recent runs (last 25)

| When (UTC) | Workflow | Stage | Tier | Cost | Turns | Tokens |
| --- | --- | --- | --- | --- | --- | --- |
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
| 2026-09-02 08:51 | Claude PR Review | `review` | sonnet | $2.0858 | 26 | 10,819 |
| 2026-09-02 08:42 | Research Refresh | `apply` | opus | $19.3599 | 166 | 101,839 |
| 2026-09-02 08:18 | Research Refresh | `discover` | sonnet | $3.4032 | 20 | 16,458 |
| 2026-09-02 08:10 | Research Refresh | `verify-9` | sonnet | $0.4775 | 25 | 12,966 |
| 2026-09-02 08:08 | Research Refresh | `verify-10` | sonnet | $0.2602 | 16 | 6,342 |
| 2026-09-02 08:06 | Research Refresh | `verify-8` | sonnet | $0.5520 | 31 | 13,993 |
| 2026-09-02 08:05 | Research Refresh | `verify-7` | sonnet | $0.4908 | 36 | 10,831 |
| 2026-09-02 08:03 | Research Refresh | `verify-6` | sonnet | $0.3549 | 21 | 11,102 |
| 2026-09-02 08:02 | Research Refresh | `verify-4` | sonnet | $0.3448 | 21 | 8,581 |
| 2026-09-02 08:00 | Research Refresh | `verify-5` | sonnet | $0.4036 | 18 | 9,322 |
| 2026-09-02 07:58 | Research Refresh | `verify-3` | sonnet | $0.3207 | 21 | 7,927 |
| 2026-09-02 07:57 | Research Refresh | `verify-2` | sonnet | $0.4621 | 25 | 10,889 |
| 2026-09-02 07:54 | Research Refresh | `verify-1` | sonnet | $0.4712 | 19 | 11,588 |

---

Ledger schema and the capture path are documented in [WORKFLOW.md](WORKFLOW.md#6-cost-control).

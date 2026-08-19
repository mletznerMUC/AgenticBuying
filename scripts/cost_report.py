#!/usr/bin/env python3
"""Regenerate docs/COST-CONTROL.md from the append-only cost ledger.

The ledger (docs/cost/ledger.jsonl) is the record; the Markdown is a view of it
and is rewritten wholesale on every run. Never hand-edit the Markdown — the next
agent run overwrites it.

Run locally after pulling:  python3 scripts/cost_report.py
"""

from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
LEDGER = REPO / "docs" / "cost" / "ledger.jsonl"
REPORT = REPO / "docs" / "COST-CONTROL.md"

# How many individual runs the "recent runs" table shows. The ledger keeps
# everything; this only bounds the rendered table so the page stays readable.
RECENT_LIMIT = 25


def load(path: pathlib.Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(row, dict):
            rows.append(row)
    return rows


def money(value) -> str:
    return f"${value:,.4f}" if isinstance(value, (int, float)) else "—"


def num(value) -> str:
    return f"{value:,}" if isinstance(value, (int, float)) else "—"


def month_of(row: dict) -> str:
    ts = str(row.get("ts") or "")
    return ts[:7] if len(ts) >= 7 else "unknown"


def cost_of(row: dict) -> float:
    value = row.get("cost_usd")
    return float(value) if isinstance(value, (int, float)) else 0.0


def unmeasured(rows: list[dict]) -> int:
    """Runs whose cost could not be read at all.

    These contribute 0 to every total, which is *probably* right — the usual
    cause is the API rejecting the call before any tokens were spent. But 0 and
    "unknown" must not render identically, or a workflow that failed all month
    looks like a workflow that got cheap.
    """
    return sum(1 for r in rows if r.get("parse_status") not in (None, "ok"))


def table(header: list[str], rows: list[list[str]], align: str = "") -> list[str]:
    if not rows:
        return ["_No data yet._", ""]
    sep = [align or "---"] * len(header)
    out = ["| " + " | ".join(header) + " |", "|" + "|".join(f" {s} " for s in sep) + "|"]
    out += ["| " + " | ".join(r) + " |" for r in rows]
    out.append("")
    return out


def render(rows: list[dict]) -> str:
    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
    months = sorted({month_of(r) for r in rows}, reverse=True)
    current = months[0] if months else now.strftime("%Y-%m")

    lines: list[str] = []
    add = lines.append

    add("# Cost control")
    add("")
    add(
        "Per-run API spend for every agent this repository runs. "
        "**Generated file — do not edit.** `scripts/cost_report.py` rewrites it "
        "from [`cost/ledger.jsonl`](cost/ledger.jsonl) after every agent run; "
        "any hand-edit is lost on the next run."
    )
    add("")
    add(f"Last updated: **{now.isoformat().replace('+00:00', 'Z')}** · "
        f"{len(rows)} run{'' if len(rows) == 1 else 's'} recorded")
    add("")

    add("## What these numbers are")
    add("")
    add(
        "Each row is one invocation of `anthropics/claude-code-action`. The figure is "
        "`total_cost_usd` from that run's own execution log — Claude Code's count of the "
        "tokens it actually used, priced at public list rates."
    )
    add("")
    add("Three limits worth knowing before you act on a number:")
    add("")
    add(
        "1. **List price, not invoice.** Any negotiated rate makes the real bill lower. "
        "Use these to compare stages against each other, and the Anthropic Console for "
        "what was actually charged."
    )
    add(
        "2. **Per stage, not per subagent.** Cost is attributable to one agent invocation. "
        "When `apply` spawns `site-reviewer`, that subagent's tokens roll into `apply`'s "
        "total. The per-model breakdown below is the only subagent signal available — a "
        "stage on Opus showing Sonnet spend is its subagents."
    )
    add(
        "3. **Agents only.** The deterministic jobs — CI, the freshness check, the AdCP "
        "release watch, the refresh preflight — call no model and never appear here. "
        "That is the point of them."
    )
    backfilled = [r for r in rows if r.get("source") == "log-backfill"]
    if backfilled:
        add(
            f"4. **{len(backfilled)} of these {len(rows)} rows were reconstructed** from "
            "GitHub Actions job logs by `scripts/backfill_cost.py`, covering runs from "
            "before the capture existed. Their costs are real — the action prints its "
            "result block to the log — but the logged form is reduced: **no token counts "
            "and no per-model breakdown**, so those cells are blank and those runs are "
            "absent from the *By model* table. Actions logs are kept 90 days, so this "
            "cannot be re-run indefinitely."
        )
    add("")

    # ---- Current month ----------------------------------------------------
    add(f"## Current month — {current}")
    add("")
    this_month = [r for r in rows if month_of(r) == current]
    if not rows:
        add(
            "No runs recorded yet. This fills in from the first agent run after the "
            "capture was merged — it is not backfilled, because the execution logs of "
            "earlier runs were never retained."
        )
    else:
        add(f"**{money(sum(cost_of(r) for r in this_month))}** across "
            f"{len(this_month)} run{'' if len(this_month) == 1 else 's'}.")
    add("")

    add("### By workflow")
    add("")
    by_wf: dict[str, list[dict]] = collections.defaultdict(list)
    for r in this_month:
        by_wf[r.get("workflow") or "unknown"].append(r)
    add_rows = []
    for wf, group in sorted(by_wf.items(), key=lambda kv: -sum(cost_of(r) for r in kv[1])):
        total = sum(cost_of(r) for r in group)
        missing = unmeasured(group)
        add_rows.append([
            wf,
            str(len(group)),
            str(missing) if missing else "—",
            money(total),
            money(total / len(group)) if group else "—",
        ])
    lines.extend(table(
        ["Workflow", "Runs", "Unmeasured", "Total", "Mean/run"], add_rows, "---"))

    add("### By stage")
    add("")
    add(
        "One row per agent. A refresh shard shows as `verify-0`, `verify-1`, … — they are "
        "separate invocations and are billed separately."
    )
    add("")
    by_stage: dict[tuple[str, str], list[dict]] = collections.defaultdict(list)
    for r in this_month:
        by_stage[(r.get("workflow") or "unknown", r.get("stage") or "unknown")].append(r)
    stage_rows = []
    for (wf, stage), group in sorted(by_stage.items(), key=lambda kv: -sum(cost_of(r) for r in kv[1])):
        total = sum(cost_of(r) for r in group)
        tiers = sorted({r.get("model_tier") or "—" for r in group})
        missing = unmeasured(group)
        stage_rows.append([
            wf,
            f"`{stage}`",
            "/".join(tiers),
            str(len(group)),
            str(missing) if missing else "—",
            money(total),
            money(total / len(group)) if group else "—",
        ])
    lines.extend(table(
        ["Workflow", "Stage", "Tier", "Runs", "Unmeasured", "Total", "Mean/run"],
        stage_rows, "---"))

    add("### By model")
    add("")
    add(
        "From each run's per-model breakdown. Spend attributed to a model the stage was "
        "not configured with is subagent spend."
    )
    add("")
    by_model: dict[str, float] = collections.defaultdict(float)
    model_tokens: dict[str, list[int]] = collections.defaultdict(lambda: [0, 0])
    for r in this_month:
        for model, stats in (r.get("models") or {}).items():
            if isinstance(stats.get("cost_usd"), (int, float)):
                by_model[model] += stats["cost_usd"]
            for idx, key in enumerate(("input_tokens", "output_tokens")):
                if isinstance(stats.get(key), (int, float)):
                    model_tokens[model][idx] += stats[key]
    model_rows = [
        [f"`{model}`", money(total), num(model_tokens[model][0]), num(model_tokens[model][1])]
        for model, total in sorted(by_model.items(), key=lambda kv: -kv[1])
    ]
    if not model_rows and this_month:
        # "No data yet" would be wrong — there are runs, they just came from the
        # backfill, which cannot see per-model spend. Say which it is.
        add(
            "_Not available for these runs: every row this month was reconstructed from "
            "Actions logs, which carry a single run-level cost and no per-model split. "
            "This table fills in from the first live-captured run._"
        )
        add("")
    else:
        lines.extend(table(
            ["Model", "Cost", "Input tokens", "Output tokens"], model_rows, "---"))

    # ---- History ----------------------------------------------------------
    add("## By month")
    add("")
    month_rows = []
    for month in months:
        group = [r for r in rows if month_of(r) == month]
        workflows = collections.defaultdict(float)
        for r in group:
            workflows[r.get("workflow") or "unknown"] += cost_of(r)
        top = max(workflows.items(), key=lambda kv: kv[1])[0] if workflows else "—"
        missing = unmeasured(group)
        month_rows.append([
            month,
            str(len(group)),
            str(missing) if missing else "—",
            money(sum(cost_of(r) for r in group)),
            top,
        ])
    lines.extend(table(
        ["Month", "Runs", "Unmeasured", "Total", "Largest workflow"], month_rows, "---"))

    # ---- Recent runs ------------------------------------------------------
    add(f"## Recent runs (last {RECENT_LIMIT})")
    add("")
    recent = sorted(rows, key=lambda r: str(r.get("ts") or ""), reverse=True)[:RECENT_LIMIT]
    recent_rows = []
    for r in recent:
        flag = ""
        if r.get("parse_status") not in (None, "ok"):
            flag = f" ⚠️ {r['parse_status']}"
        elif r.get("is_error"):
            flag = " ⚠️ error"
        tokens = (r.get("input_tokens") or 0) + (r.get("output_tokens") or 0)
        recent_rows.append([
            str(r.get("ts") or "—").replace("T", " ").replace("Z", "")[:16],
            r.get("workflow") or "—",
            f"`{r.get('stage') or '—'}`",
            r.get("model_tier") or "—",
            money(r.get("cost_usd")) + flag,
            num(r.get("num_turns")),
            # Backfilled rows have no token data at all; 0 would be a lie.
            num(tokens) if tokens else "—",
        ])
    lines.extend(table(
        ["When (UTC)", "Workflow", "Stage", "Tier", "Cost", "Turns", "Tokens"],
        recent_rows, "---"))

    # ---- Anomalies --------------------------------------------------------
    unpriced = [r for r in rows if r.get("parse_status") not in (None, "ok")]
    if unpriced:
        add("## Runs with no usable cost data")
        add("")
        add(
            f"{len(unpriced)} run{'' if len(unpriced) == 1 else 's'} produced no readable "
            "execution log. Usually the API rejected the call outright — a blocked key or a "
            "rate limit — so the true cost is near zero, but it is *not* measured. A cluster "
            "of these means the agents are failing, not that they got cheap."
        )
        add("")
        unpriced_rows = [
            [
                str(r.get("ts") or "—").replace("T", " ").replace("Z", ""),
                r.get("workflow") or "—",
                f"`{r.get('stage') or '—'}`",
                r.get("parse_status") or "—",
                f"[run](https://github.com/mletznerMUC/AgenticBuying/actions/runs/{r.get('run_id')})"
                if r.get("run_id") else "—",
            ]
            for r in sorted(unpriced, key=lambda r: str(r.get("ts") or ""), reverse=True)[:RECENT_LIMIT]
        ]
        lines.extend(table(["When (UTC)", "Workflow", "Stage", "Why", "Link"], unpriced_rows, "---"))

    add("---")
    add("")
    add(
        "Ledger schema and the capture path are documented in "
        "[WORKFLOW.md](WORKFLOW.md#6-cost-control)."
    )
    add("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--ledger", default=str(LEDGER))
    ap.add_argument("--out", default=str(REPORT))
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if the report is stale rather than writing it")
    args = ap.parse_args()

    rows = load(pathlib.Path(args.ledger))
    rendered = render(rows)
    out = pathlib.Path(args.out)

    if args.check:
        current = out.read_text() if out.exists() else ""
        # The timestamp line always differs; compare everything else.
        strip = lambda text: "\n".join(
            l for l in text.splitlines() if not l.startswith("Last updated:")
        )
        if strip(current) != strip(rendered):
            print("COST-CONTROL.md is stale — run: python3 scripts/cost_report.py", file=sys.stderr)
            return 1
        print("COST-CONTROL.md is up to date.")
        return 0

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(rendered)
    try:
        shown = out.resolve().relative_to(REPO)
    except ValueError:
        shown = out  # --out pointed outside the repo (tests do this)
    print(f"Wrote {shown} from {len(rows)} ledger row(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

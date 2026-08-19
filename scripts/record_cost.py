#!/usr/bin/env python3
"""Turn one Claude Code Action run into a single cost-ledger record.

The action's `execution_file` output points at a JSON event log. The last event
with `"type": "result"` carries what we need: `total_cost_usd`, `usage`,
`num_turns`, `duration_ms`. Everything else in the log is transcript.

Two things make this more defensive than it looks:

  * The parsing example in the action's own README is stale — it keys on
    `e.role === "assistant"`, while current SDK output puts `type` at the top
    level of each event (anthropics/claude-code-action#1296). We key on
    `type == "result"` and scan from the end.
  * A failed or rate-limited agent step leaves no usable file at all. That must
    still produce a record — a run that cost nothing because the API rejected it
    is exactly the kind of thing the ledger should show, and a silent gap looks
    identical to a cheap run.

So this never raises on bad input: it records what it found and stamps
`parse_status` with why, leaving the report to surface it.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import sys


def _load_events(path: pathlib.Path) -> tuple[list[dict], str]:
    """Return (events, parse_status). Never raises."""
    if not path or not path.exists():
        return [], "missing"
    raw = path.read_text(errors="replace").strip()
    if not raw:
        return [], "empty"

    # The file is normally a JSON array. Tolerate JSONL, which is what the
    # stream-json format produces, so a format switch upstream doesn't blind us.
    try:
        parsed = json.loads(raw)
        if isinstance(parsed, list):
            return [e for e in parsed if isinstance(e, dict)], "ok"
        if isinstance(parsed, dict):
            return [parsed], "ok"
        return [], "unexpected-shape"
    except json.JSONDecodeError:
        pass

    events = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            events.append(obj)
    return (events, "ok") if events else ([], "unparseable")


def _result_event(events: list[dict]) -> dict | None:
    for event in reversed(events):
        if event.get("type") == "result":
            return event
    return None


def _model_breakdown(result: dict) -> dict:
    """Per-model cost, when the result event carries it.

    This is the only visibility we get into subagent spend: a stage running on
    Opus that delegates to Sonnet subagents shows both models here, while
    `total_cost_usd` shows only the sum. The key has been seen as both
    `modelUsage` and `model_usage`; accept either and normalise.
    """
    raw = result.get("modelUsage") or result.get("model_usage") or {}
    if not isinstance(raw, dict):
        return {}
    out = {}
    for model, stats in raw.items():
        if not isinstance(stats, dict):
            continue
        out[str(model)] = {
            "cost_usd": stats.get("costUSD", stats.get("cost_usd")),
            "input_tokens": stats.get("inputTokens", stats.get("input_tokens")),
            "output_tokens": stats.get("outputTokens", stats.get("output_tokens")),
        }
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--execution-file", default="", help="path from the action's execution_file output")
    ap.add_argument("--out", required=True, help="where to write the ledger record")
    ap.add_argument("--workflow", required=True, help="human-readable workflow name")
    ap.add_argument("--stage", required=True, help="agent stage, e.g. 'apply' or 'verify-3'")
    ap.add_argument("--run-id", default="")
    ap.add_argument("--run-number", default="")
    ap.add_argument("--event", default="", help="the triggering GitHub event")
    ap.add_argument("--conclusion", default="", help="the action's own conclusion output")
    ap.add_argument("--model-tier", default="", help="tier the workflow asked for (opus/sonnet/…)")
    args = ap.parse_args()

    # An action that never ran sets neither output. That is different from an
    # action that ran and failed (which sets `conclusion` but may leave no
    # execution log), and it must not land in the ledger: a cost record for work
    # that was never attempted reads as a failed agent. The case is routine —
    # the action refuses to run when a PR modifies its own workflow file, so
    # every workflow-editing PR hits it.
    if not args.execution_file and not args.conclusion:
        print(f"{args.workflow} / {args.stage}: action did not run; nothing to record.")
        return 0

    events, parse_status = _load_events(pathlib.Path(args.execution_file) if args.execution_file else None)
    result = _result_event(events)
    if result is None and parse_status == "ok":
        parse_status = "no-result-event"

    usage = result.get("usage") if result else None
    usage = usage if isinstance(usage, dict) else {}

    record = {
        "ts": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "workflow": args.workflow,
        "stage": args.stage,
        "run_id": args.run_id,
        "run_number": args.run_number,
        "event": args.event,
        "conclusion": args.conclusion,
        "model_tier": args.model_tier,
        "parse_status": parse_status,
        # `total_cost_usd` is Claude Code's own figure, derived from token counts
        # at public list prices. It is not what the account is invoiced — any
        # negotiated rate makes the real number lower. Treat it as an upper bound
        # and a consistent basis for comparing stages against each other.
        "cost_usd": result.get("total_cost_usd") if result else None,
        "duration_ms": result.get("duration_ms") if result else None,
        "num_turns": result.get("num_turns") if result else None,
        "is_error": result.get("is_error") if result else None,
        "result_subtype": result.get("subtype") if result else None,
        "input_tokens": usage.get("input_tokens"),
        "output_tokens": usage.get("output_tokens"),
        "cache_creation_tokens": usage.get("cache_creation_input_tokens"),
        "cache_read_tokens": usage.get("cache_read_input_tokens"),
        "models": _model_breakdown(result) if result else {},
    }

    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(record, sort_keys=True) + "\n")

    cost = record["cost_usd"]
    print(
        f"{args.workflow} / {args.stage}: "
        f"{'$%.4f' % cost if isinstance(cost, (int, float)) else 'no cost recorded'} "
        f"({parse_status})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

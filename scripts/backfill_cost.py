#!/usr/bin/env python3
"""Reconstruct cost-ledger rows for agent runs that predate the cost capture.

Run this once, locally. It is not part of any workflow.

The live capture (scripts/record_cost.py) reads the action's `execution_file`
output, which only exists for runs after that capture was merged. But the action
*also* prints its result block to the job log, and GitHub keeps those logs for
90 days — so earlier runs are recoverable after all:

    {
      "type": "result",
      "subtype": "success",
      "is_error": false,
      "duration_ms": 528112,
      "num_turns": 59,
      "total_cost_usd": 3.1116710000000003,
      "permission_denials_count": 19
    }

WHAT BACKFILLED ROWS DO NOT HAVE. The logged block is a reduced form: it carries
no `usage` and no `modelUsage`, so there are **no token counts and no per-model
breakdown**. The model comes from the separate init line instead, which names one
model for the run and so cannot show subagent spend. Rows are stamped
`source: "log-backfill"` and the report renders their token columns empty —
these are real measured costs, but a thinner record than the live path produces.

Usage:
    python3 scripts/backfill_cost.py --dry-run     # show what would be added
    python3 scripts/backfill_cost.py               # append to the ledger
"""

from __future__ import annotations

import argparse
import io
import json
import os
import pathlib
import re
import subprocess
import sys
import urllib.request
import zipfile

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
LEDGER = REPO_ROOT / "docs" / "cost" / "ledger.jsonl"
REPO = "mletznerMUC/AgenticBuying"

# Workflows that invoke an agent. Everything else is deterministic and has no
# cost to recover — that is the whole point of those jobs.
AGENTIC = {"Claude PR Review", "Research Refresh", "Claude Agent"}

# Job name -> ledger stage. The live capture names claude.yml's stage `agent`;
# its job is called `claude`, so map it rather than letting the two diverge.
STAGE_ALIASES = {"claude": "agent"}

# `2_verify (0, adcp-latest-release,…).txt` -> the shard index is the first
# matrix value, and is what makes shards distinguishable in the report.
LOGFILE_RE = re.compile(r"^\d+_(?P<job>.+)\.txt$")
MATRIX_RE = re.compile(r"^(?P<job>[\w-]+)\s+\((?P<index>\d+)[,)]")


def token() -> str:
    if os.environ.get("GITHUB_TOKEN"):
        return os.environ["GITHUB_TOKEN"]
    out = subprocess.run(
        ["git", "credential", "fill"],
        input="protocol=https\nhost=github.com\n\n",
        capture_output=True, text=True, check=False,
    ).stdout
    for line in out.splitlines():
        if line.startswith("password="):
            return line.split("=", 1)[1]
    sys.exit("No GitHub token: set GITHUB_TOKEN or configure the git credential helper.")


def api(tok: str, path: str) -> dict:
    req = urllib.request.Request(
        f"https://api.github.com/repos/{REPO}{path}",
        headers={"Authorization": f"Bearer {tok}", "Accept": "application/vnd.github+json"},
    )
    return json.load(urllib.request.urlopen(req))


def fetch_logs(tok: str, run_id: int) -> zipfile.ZipFile | None:
    """Job logs for a run, or None when they have aged out (90-day retention)."""
    req = urllib.request.Request(
        f"https://api.github.com/repos/{REPO}/actions/runs/{run_id}/logs",
        headers={"Authorization": f"Bearer {tok}", "Accept": "application/vnd.github+json"},
    )
    try:
        return zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(req).read()))
    except Exception as exc:                      # expired, 404, or not a zip
        print(f"    logs unavailable ({exc.__class__.__name__})")
        return None


def tier_of(model: str | None) -> str:
    """`claude-opus-5[1m]` -> `opus`, matching what the workflows call it."""
    if not model:
        return ""
    for tier in ("opus", "sonnet", "haiku"):
        if tier in model:
            return tier
    return model.replace("[1m]", "")


def stage_from_filename(name: str) -> str | None:
    m = LOGFILE_RE.match(name)
    if not m:
        return None
    job = m.group("job").strip()
    matrix = MATRIX_RE.match(job)
    if matrix:
        return f"{matrix.group('job')}-{matrix.group('index')}"
    job = job.split(" (")[0].strip()
    return STAGE_ALIASES.get(job, job)


def parse_job_log(text: str) -> dict | None:
    """Pull the result block and the model out of one job log.

    The log is timestamp-prefixed and pretty-printed, so the JSON cannot simply
    be json.loads'd — strip the leading timestamp from every line, then take the
    brace-balanced block that starts at the `"type": "result"` line.
    """
    stripped = "\n".join(
        re.sub(r"^\S+Z ", "", line) for line in text.splitlines()
    )
    if '"total_cost_usd"' not in stripped:
        return None

    lines = stripped.splitlines()
    start = next(
        (i for i, l in enumerate(lines)
         if l.strip().startswith("{") and i + 1 < len(lines)
         and '"type": "result"' in lines[i + 1]),
        None,
    )
    if start is None:
        return None

    depth, chunk = 0, []
    for line in lines[start:]:
        chunk.append(line)
        depth += line.count("{") - line.count("}")
        if depth == 0:
            break
    try:
        result = json.loads("\n".join(chunk))
    except json.JSONDecodeError:
        return None

    model = None
    m = re.search(r'"model":\s*"([^"]+)"', stripped)
    if m:
        model = m.group(1)
    return {"result": result, "model": model}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true", help="print rows without writing")
    ap.add_argument("--limit", type=int, default=100, help="how many recent runs to scan")
    args = ap.parse_args()

    tok = token()

    existing = set()
    if LEDGER.exists():
        for line in LEDGER.read_text().splitlines():
            if line.strip():
                try:
                    row = json.loads(line)
                    existing.add((str(row.get("run_id")), row.get("stage")))
                except json.JSONDecodeError:
                    pass
    print(f"Ledger holds {len(existing)} row(s) already.\n")

    runs = [r for r in api(tok, f"/actions/runs?per_page={args.limit}")["workflow_runs"]
            if r["name"] in AGENTIC]
    runs.sort(key=lambda r: r["created_at"])
    print(f"Scanning {len(runs)} agentic run(s)…\n")

    records, skipped = [], 0
    for run in runs:
        print(f"  {run['created_at'][:10]}  {run['name']} run#{run['run_number']} ({run['id']})")
        jobs = {j["name"]: j for j in api(tok, f"/actions/runs/{run['id']}/jobs")["jobs"]}
        zf = fetch_logs(tok, run["id"])
        if zf is None:
            continue

        for name in sorted(zf.namelist()):
            if "/" in name or not name.endswith(".txt"):
                continue                          # per-step logs live in subdirs
            stage = stage_from_filename(name)
            if stage is None:
                continue
            parsed = parse_job_log(zf.read(name).decode("utf-8", errors="replace"))
            if parsed is None:
                continue                          # deterministic job — no agent ran

            key = (str(run["id"]), stage)
            if key in existing:
                skipped += 1
                print(f"      {stage}: already in ledger, skipping")
                continue

            result = parsed["result"]
            job = next((j for n, j in jobs.items() if n.split(" (")[0] == stage.rsplit("-", 1)[0]
                        or n == stage), None)
            cost = result.get("total_cost_usd")
            records.append({
                # The job's own start time, not now: month bucketing depends on it.
                "ts": (job or {}).get("started_at") or run["created_at"],
                "workflow": run["name"],
                "stage": stage,
                "run_id": str(run["id"]),
                "run_number": str(run["run_number"]),
                "event": run.get("event", ""),
                "conclusion": (job or {}).get("conclusion", "") or "",
                # Observed, not configured: these runs predate the tiering, so
                # the log is the only truth about what actually ran. Normalised
                # to the same vocabulary the live capture uses, so the report's
                # Tier column doesn't mix "sonnet" with "claude-sonnet-5".
                "model_tier": tier_of(parsed["model"]),
                "model_observed": (parsed["model"] or "").replace("[1m]", ""),
                "parse_status": "ok",
                "source": "log-backfill",
                "cost_usd": cost,
                "duration_ms": result.get("duration_ms"),
                "num_turns": result.get("num_turns"),
                "is_error": result.get("is_error"),
                "result_subtype": result.get("subtype"),
                # Absent from the logged result block — see the module docstring.
                "input_tokens": None,
                "output_tokens": None,
                "cache_creation_tokens": None,
                "cache_read_tokens": None,
                "models": {},
            })
            print(f"      {stage}: ${cost:.4f}" if isinstance(cost, (int, float))
                  else f"      {stage}: cost missing")

    total = sum(r["cost_usd"] or 0 for r in records)
    print(f"\n{len(records)} new row(s), {skipped} already present. Recovered ${total:.2f}.")

    if not records:
        return 0
    if args.dry_run:
        print("\n--dry-run: nothing written.")
        return 0

    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a") as f:
        for record in sorted(records, key=lambda r: r["ts"]):
            f.write(json.dumps(record, sort_keys=True) + "\n")
    print(f"Appended to {LEDGER.relative_to(REPO_ROOT)}. Now run: python3 scripts/cost_report.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())

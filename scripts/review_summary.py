#!/usr/bin/env python3
"""Surface an agentic review's own output in the workflow run.

The problem this exists for: the Claude PR review check can go green having
published nothing. It happened on PR #52 — 42 turns, $0.85, 14 permission
denials, `conclusion: success`, and no review, no PR comment, no inline
comments. Because `claude-code-action` hides the agent's output by default
("full output hidden for security") and the workflow uploaded only the cost
record, the findings were unrecoverable after the fact. A green check that
publishes nothing is indistinguishable from a clean review, which is the worst
possible failure mode for a check whose whole product is its findings.

This script closes that gap deterministically — no model in the loop. It reads
the action's event log and writes what the agent actually concluded into the
job summary, so the review survives even when posting it to the PR fails, and
it annotates the run when the shape of the log says the agent was blocked
rather than satisfied.

It never fails the job. Diagnostics that gate a merge would just trade a silent
green for a noisy red; the annotations belong in the run, and whether a silent
review should block is a policy question for the workflow, not for a parser.
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import sys

# Reusing the sibling's tolerant loader rather than writing a second one: its
# defensiveness about the log's shape (JSON array vs. JSONL, `type` at the top
# level vs. the action's stale README example) is the whole point, and two
# parsers would drift apart on the next upstream format change.
from record_cost import _load_events, _result_event

# Longest review text to inline in the job summary. GitHub truncates a step
# summary at 1 MiB and the artifact holds the full transcript either way, so
# this only keeps one runaway review from crowding out the stats above it.
MAX_SUMMARY_CHARS = 60_000


def _assistant_text(events: list[dict]) -> str:
    """The last assistant message's text, as a fallback for a missing result.

    The result event normally carries the agent's closing message in `result`.
    When it does not — a truncated log, an upstream shape change, a run that
    ended without a result event — the transcript's final assistant turn is the
    next best record of what the review concluded.
    """
    for event in reversed(events):
        if event.get("type") != "assistant":
            continue
        message = event.get("message")
        if not isinstance(message, dict):
            continue
        content = message.get("content")
        if isinstance(content, str):
            return content.strip()
        if isinstance(content, list):
            parts = [
                block.get("text", "")
                for block in content
                if isinstance(block, dict) and block.get("type") == "text"
            ]
            text = "\n\n".join(p for p in parts if p).strip()
            if text:
                return text
    return ""


def _fmt(value) -> str:
    return "unknown" if value is None else str(value)


def _money(value) -> str:
    return f"${value:.4f}" if isinstance(value, (int, float)) else "unknown"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--execution-file", default="", help="path from the action's execution_file output")
    ap.add_argument("--conclusion", default="", help="the action's own conclusion output")
    ap.add_argument(
        "--summary-file",
        default=os.environ.get("GITHUB_STEP_SUMMARY", ""),
        help="where to write the markdown summary (default: $GITHUB_STEP_SUMMARY)",
    )
    args = ap.parse_args()

    # The action sets neither output when it never ran. That is routine rather
    # than broken: it refuses to run when a pull request modifies its own
    # workflow file, so every workflow-editing PR lands here.
    if not args.execution_file and not args.conclusion:
        print("::notice::The review action did not run, so there is no output to surface.")
        return 0

    path = pathlib.Path(args.execution_file) if args.execution_file else None
    events, parse_status = _load_events(path)
    result = _result_event(events) or {}

    review = result.get("result")
    review = review.strip() if isinstance(review, str) else ""
    source = "final message"
    if not review:
        review = _assistant_text(events)
        source = "last assistant turn" if review else "none"

    denials = result.get("permission_denials_count")
    truncated = len(review) > MAX_SUMMARY_CHARS
    body = review[:MAX_SUMMARY_CHARS] if truncated else review

    lines = [
        "## Claude PR review",
        "",
        f"- Conclusion: `{args.conclusion or 'unknown'}`"
        f" · turns: {_fmt(result.get('num_turns'))}"
        f" · cost: {_money(result.get('total_cost_usd'))}"
        f" · permission denials: {_fmt(denials)}",
        f"- Event log: `{parse_status}` · review text recovered from: {source}",
        "",
    ]
    if body:
        lines += ["### What the reviewer said", "", body, ""]
        if truncated:
            lines += [
                f"_Truncated at {MAX_SUMMARY_CHARS:,} characters — the full transcript is in the"
                " `review-transcript` artifact._",
                "",
            ]
    else:
        lines += [
            "### No review text was recoverable",
            "",
            "The agent's event log carries neither a closing message nor an assistant turn with"
            " text. The `review-transcript` artifact on this run is the only remaining record.",
            "",
        ]

    if args.summary_file:
        with open(args.summary_file, "a", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")
    else:
        sys.stdout.write("\n".join(lines) + "\n")

    # Annotations, so a silent review is visible on the checks tab and not only
    # to whoever opens the summary.
    if not review:
        print(
            "::warning::The review produced no recoverable text. Check the review-transcript"
            " artifact, and see the note at the top of claude-review.yml about --allowedTools"
            " replacing the action's default toolset."
        )
    if isinstance(denials, int) and denials > 0:
        print(
            f"::warning::The review agent hit {denials} permission denial(s). Denials are how this"
            " check has failed silently before: the agent could not reach the tool it needed and"
            " ended without publishing. Confirm its findings landed on the pull request."
        )

    print(f"Review output surfaced: parse_status={parse_status}, text_source={source}, chars={len(review)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

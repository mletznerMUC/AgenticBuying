# AgenticBuying — Project Guide for Claude Code

## What this project is

AgenticBuying observes and compares developments in **Agentic Buying** — the ecosystem
where AI agents discover, negotiate, and transact advertising/media buys. The project
primarily compares two emerging protocol families:

- **AdCP** (Ad Context Protocol) — https://adcontextprotocol.org
- **AAMP** (Agentic Advertising Management Protocols — IAB Tech Lab)

The outcome is a **multi-page static HTML website** that provides:

1. Guidance on the latest developments in agentic buying
2. Comparison of AdCP vs. AAMP (capabilities, adoption, governance)
3. Curated tools and resources
4. Sample workflows showing how agentic buying works end to end

## Repository layout

```
index.html             Landing page: what agentic buying is, latest headlines
adcp.html              AdCP deep dive
aamp.html              AAMP deep dive
releases.html          Release tracker: last three releases of each protocol, what changed
comparison.html        Side-by-side AdCP vs. AAMP comparison
tools.html             Tools & platform directory
workflows.html         Sample agentic buying workflows
resources.html         Specs, articles, talks, repos
assets/css/            Shared stylesheet(s)
docs/DESIGN.md         Design guide: visual system, badge rules, imagery, a11y
docs/WORKFLOW.md       The agent-based development workflow
docs/COST-CONTROL.md   Generated: per-run API spend by workflow and agent stage
docs/cost/ledger.jsonl Append-only cost record; the report is derived from it
docs/research/         Sourced research notes behind the site's content
scripts/               Deterministic helpers (cost capture + reporting)
.claude/agents/        Specialized subagent definitions
.github/workflows/     Claude agent automation, CI
.nojekyll              Disables Jekyll processing on GitHub Pages
```

The website pages live at the **repository root** so GitHub Pages can publish
directly from the `main` branch ("Deploy from a branch" → `main` → `/ (root)`).

The site currently ships **no JavaScript** — navigation and everything else work
with plain HTML and CSS. JavaScript is permitted (see Tech constraints below); if
it is ever added, it belongs in `assets/js/`, kept minimal and progressive so the
site stays fully readable with JS disabled.

## Tech constraints

- **Plain HTML/CSS/JS only. No build step, no framework, no bundler.**
  Every page must open correctly from the filesystem and from GitHub Pages.
- Shared navigation is duplicated per page (no server-side includes); keep it
  identical across pages — update all pages when the nav changes. The same
  applies to the footer, which carries the AI transparency notice and the
  copyright line — never drop either when editing a page.
- Mobile-first responsive CSS in `assets/css/style.css`. Support light and
  dark mode via `prefers-color-scheme`.
- Accessibility: semantic HTML, one `<h1>` per page, alt text on images,
  sufficient color contrast.
- All external links use `rel="noopener"` and cite their source and date.
- **Read `docs/DESIGN.md` before any visual or markup change.** It defines the
  design direction, the banned "AI slop" patterns, the status-badge rules, the
  inline-SVG imagery grammar, and the accessibility floor.

## Content rules

- Every factual claim about AdCP or AAMP must carry a source link and a
  "last verified" date, because this space moves fast.
- Distinguish claims by evidence strength using the four badge states —
  **shipped**, **announced**, **reported**, **speculative**. Badges mark
  exceptions: unbadged prose means verified/shipped. See `docs/DESIGN.md` §5.
- Comparison content must be neutral in tone — describe, don't advocate.

## Development workflow (agent-based)

This repo is developed with an agentic workflow — see `docs/WORKFLOW.md` for the
full description. Summary:

1. Work is tracked as GitHub Issues using the issue templates
   (research task, content update, site feature, bug).
2. Mentioning `@claude` on an issue or PR triggers the Claude GitHub Action,
   which implements the request on a branch and opens a PR.
3. Specialized subagents in `.claude/agents/` split the work:
   - `research-analyst` — tracks and verifies AdCP/AAMP developments
   - `web-search-researcher` — deep multi-source web research utility that
     `research-analyst` and others delegate raw searches to
   - `content-writer` — turns research into neutral, sourced page content
   - `frontend-builder` — implements pages, styling, and navigation
   - `site-reviewer` — reviews changes for accuracy, consistency, a11y
4. CI validates HTML and internal links on every PR; GitHub Pages publishes
   the `main` branch root directly (branch deployment, no build step).
5. Every agent run records what it cost. `docs/COST-CONTROL.md` is **generated**
   from `docs/cost/ledger.jsonl` after each run — never edit it by hand, CI
   fails if it drifts. See `docs/WORKFLOW.md` §6.

## Conventions

- Branches: `claude/<topic>` for agent work, `feat/<topic>` / `fix/<topic>` for humans.
- Commits: imperative mood, scoped prefix when useful (`site:`, `docs:`, `ci:`).
- PRs must pass CI (HTML validation + link check) before merge.
- Never commit secrets. The Claude action uses the `ANTHROPIC_API_KEY` repo secret.

## Commands

No build step. Useful local commands:

```bash
# Serve the site locally
python3 -m http.server 8000

# Validate HTML (same as CI). Needs Node 22+ — on older Node it fails with
# "TypeError: fs.globSync is not a function", which is the tool, not your HTML.
npx --yes html-validate "*.html"

# Check the cost report for drift (same as CI). Use this after pulling — it
# ignores the generated timestamp, so it only fails on a real hand-edit.
python3 scripts/cost_report.py --check

# Regenerate docs/COST-CONTROL.md. Only needed when the ledger actually changed:
# the generator re-stamps "Last updated" with the current time on every run, so
# a bare regenerate always dirties the file even when nothing else differs.
python3 scripts/cost_report.py
```

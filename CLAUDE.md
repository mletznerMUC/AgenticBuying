# AgenticBuying — Project Guide for Claude Code

## What this project is

AgenticBuying observes and compares developments in **Agentic Buying** — the ecosystem
where AI agents discover, negotiate, and transact advertising/media buys. The project
primarily compares two emerging protocol families:

- **AdCP** (Ad Context Protocol) — https://adcontextprotocol.org
- **AAMP** (Agentic Advertising & Marketing Protocols / agentic ad marketplace protocols)

The outcome is a **multi-page static HTML website** that provides:

1. Guidance on the latest developments in agentic buying
2. Comparison of AdCP vs. AAMP (capabilities, adoption, governance)
3. Curated tools and resources
4. Sample workflows showing how agentic buying works end to end

## Repository layout

```
site/                  The deliverable website (deployed to GitHub Pages)
  index.html           Landing page: what agentic buying is, latest headlines
  adcp.html            AdCP deep dive
  aamp.html            AAMP deep dive
  comparison.html      Side-by-side AdCP vs. AAMP comparison
  tools.html           Tools & platform directory
  workflows.html       Sample agentic buying workflows
  resources.html       Specs, articles, talks, repos
  assets/css/          Shared stylesheet(s)
  assets/js/           Shared JavaScript (nav, no build step)
docs/                  Internal docs: workflow, architecture decisions
.claude/agents/        Specialized subagent definitions
.github/workflows/     Claude agent automation, CI, Pages deploy
```

## Tech constraints

- **Plain HTML/CSS/JS only. No build step, no framework, no bundler.**
  Every page must open correctly from the filesystem and from GitHub Pages.
- Shared navigation is duplicated per page (no server-side includes); keep it
  identical across pages — update all pages when the nav changes.
- Mobile-first responsive CSS in `site/assets/css/style.css`. Support light and
  dark mode via `prefers-color-scheme`.
- Accessibility: semantic HTML, one `<h1>` per page, alt text on images,
  sufficient color contrast.
- All external links use `rel="noopener"` and cite their source and date.

## Content rules

- Every factual claim about AdCP or AAMP must carry a source link and a
  "last verified" date, because this space moves fast.
- Distinguish clearly between **shipped**, **announced**, and **speculative**.
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
4. CI validates HTML and internal links on every PR; merges to `main`
   auto-deploy `site/` to GitHub Pages.

## Conventions

- Branches: `claude/<topic>` for agent work, `feat/<topic>` / `fix/<topic>` for humans.
- Commits: imperative mood, scoped prefix when useful (`site:`, `docs:`, `ci:`).
- PRs must pass CI (HTML validation + link check) before merge.
- Never commit secrets. The Claude action uses the `ANTHROPIC_API_KEY` repo secret.

## Commands

No build step. Useful local commands:

```bash
# Serve the site locally
python3 -m http.server 8000 --directory site

# Validate HTML (same as CI)
npx --yes html-validate "site/**/*.html"
```

# AgenticBuying

Observes and compares developments in **Agentic Buying** — AI agents that
discover, negotiate, and transact media buys — with a focus on the two emerging
protocol families, **AdCP** (Ad Context Protocol) and **AAMP**.

The deliverable is a multi-page static HTML website (pages at the repository
root, published via GitHub Pages branch deployment) providing:

- Guidance on the latest developments in agentic buying
- A neutral, sourced **AdCP vs. AAMP** comparison
- A directory of **tools & resources**
- **Sample workflows** for agent-driven media buying

## Agent-based development

This repository is developed with a fully agentic workflow built on Claude
Code — see **[docs/WORKFLOW.md](docs/WORKFLOW.md)**. In short:

1. Work starts as a GitHub Issue (research task, content update, site
   feature, or bug — use the templates).
2. Mention **`@claude`** on the issue and the Claude GitHub Action implements
   it on a branch and opens a PR, delegating to specialized subagents
   (`research-analyst`, `content-writer`, `frontend-builder`, `site-reviewer`
   in [`.claude/agents/`](.claude/agents/)).
3. CI validates HTML and links; an agentic PR review applies the editorial
   checklist; a human merges.
4. GitHub Pages publishes the `main` branch root directly, so every merge
   to `main` goes live automatically.

### One-time setup

- Add the `ANTHROPIC_API_KEY` repository secret (or run
  `/install-github-app` from the Claude Code CLI).
- Settings → Pages → Build and deployment → Source: **Deploy from a branch**,
  Branch: **main**, Folder: **/ (root)**.

## Local development

No build step — plain HTML/CSS/JS:

```bash
python3 -m http.server 8000            # serve
npx --yes html-validate "*.html"       # validate (same as CI)
```

## Content principles

- Every factual claim carries a **source link** and a **"last verified" date**.
- Capabilities are labeled **shipped**, **announced**, or **speculative**.
- Comparison content is neutral — describe, don't advocate.

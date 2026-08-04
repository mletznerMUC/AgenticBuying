# AgenticBuying — Design Guide

**Direction: a quietly distinctive editorial reference.**

This site's product is not a page — it is *calibrated confidence about a fast-moving
topic*. Every design decision below serves that: the reader should be able to tell, at
a glance, how much weight a claim carries and how fresh it is. Where a choice does not
serve that, it does not belong here.

The guide is written for the agents that build this site (`content-writer`,
`frontend-builder`) as much as for humans. Rules are stated as markup and token
patterns you can copy, not as adjectives. Section 10 lists what CI enforces, because a
guide that can't be checked will drift on the next automated pull request.

---

## 1. What this site looks like — and what it must never look like

**The look:** an instrument panel for practitioners. Light, paper-toned surfaces; near-black
text; generous line length limits; one accent color; content-bearing color used only for
evidence status. Restraint reads as authority, and authority is what a reference site sells.

**"AI slop" — the house definition.** These are banned outright. They are the interchangeable
look of generated pages, and they destroy the credibility this site trades on:

| Banned | Why |
|---|---|
| Purple/blue gradient heroes, glassmorphism, neon glow | The generic generated-page signature |
| Stock photography of "AI," robots, handshakes, glowing brains | There is no honest photograph of an agent buying ads |
| Emoji as bullets, icons, or section markers | Reads as filler; breaks the register of a technical reference |
| "Revolutionize / unlock / seamless / game-changing" | Advocacy language on a site that must describe, not sell |
| Decorative shapes, blobs, particle backgrounds, animated gradients | Ornament with no information content |
| Full-viewport hero with a single centered slogan | Costs the reader the one thing they came for: the news |

**The honest test before adding anything:** *does this element carry information a reader
would miss without it?* If no, it does not ship. Ornament is the failure mode this site
cannot afford.

---

## 2. Layout and rhythm

- Single column, `max-width: 68rem` (`--max-width`), centered. Text blocks stay under
  ~75 characters — use the `.lead` class for intro paragraphs.
- Mobile-first. All spacing in `rem`. Never set a fixed pixel width on a container.
- Vertical rhythm comes from heading margins, not from divider elements. One horizontal
  rule per page maximum (the `h2` bottom border already provides separation).
- Page skeleton, in order: `header.site-header` → `main` (h1 → `.lead` → source/legend →
  content sections) → `footer.site-footer`.

## 3. Color

Colors live as custom properties in `:root` and are overridden inside
`@media (prefers-color-scheme: dark)`. **Never hardcode a hex value in a page or in a new
rule** — add a token or reuse one, so dark mode stays automatic.

| Token | Role |
|---|---|
| `--bg`, `--bg-alt` | Page surface, raised surface (cards, legend, table headers) |
| `--text`, `--text-muted` | Body text, secondary text (sources, captions, footer) |
| `--accent`, `--accent-contrast` | Links and current-page nav only |
| `--border` | All hairlines |
| `--shipped`, `--announced`, `--reported`, `--speculative` (+ `-bg`) | Evidence status only |

Two rules that keep the palette honest:

1. **Status colors are reserved.** Green, amber, slate, and violet mean *evidence
   strength*, nothing else. Never use them for decoration, links, or emphasis.
2. **Neutrality is structural.** AdCP and AAMP get identical visual treatment — same
   heading weights, same table widths, same diagram grammar, no protocol-specific accent
   colors, no logos. Visual asymmetry would read as editorial preference.

Dark mode is not an afterthought: every new component must be checked in both schemes
before merge. Light is the primary design target; dark must be equally legible.

## 4. Typography

- System font stack (`system-ui, -apple-system, "Segoe UI", Roboto, sans-serif`). It costs
  zero requests, never blocks render, and looks native rather than templated. If a display
  face is ever introduced for the masthead, it must be a single self-hosted WOFF2 — no CDN,
  no second family, no web-font body text.
- Scale in use: `h1` 1.9rem / `h2` 1.35rem / body 1rem / `.source`, `.badge-legend`, footer
  0.85rem / `.badge` 0.75rem. `line-height: 1.6` on body.
- Exactly one `h1` per page. Heading levels never skip (`h2` → `h3`, never `h2` → `h4`).
- Sentence case for headings. No uppercase transforms, no letter-spacing tricks.
- American spelling. Expand every acronym on first use per page — "AdCP (Ad Context
  Protocol)" — because readers land on deep pages from search, not from the home page.

## 5. The status badge system

This is the site's signature and its most important component. It marks **how strong the
evidence behind a claim is** — never how important the claim is.

### The four states

| State | Meaning | Glyph | Border |
|---|---|---|---|
| `shipped` | Released or in production, verified | ● | solid |
| `announced` | Publicly committed but not shipped; includes vendor claims that are not independently benchmarked | ◐ | solid |
| `reported` | Secondary sources only, no primary confirmation located, or a disputed figure/date | ○ | dashed |
| `speculative` | Analyst interpretation or contested reading, not settled fact | ◇ | dashed |

### The rules

1. **Badges mark exceptions, not everything.** Unbadged prose means *shipped and verified*.
   A badge that appears on every claim carries no information — that is exactly how the
   system decayed once already.
2. **A badge qualifies a claim, not a paragraph.** If a paragraph is one claim, lead with
   the badge. If a caveat sits inside an otherwise-verified paragraph, place the badge
   immediately after the sentence it qualifies. Ambiguous scope is how a reader ends up
   telling their team "AdCP 3.0 is GA."
3. **Table status columns are the exception to rule 1** — a column that exists to hold the
   value badges every row, because comparison across rows is the point. If every row in
   such a column has the same value, delete the column.
4. **Never encode meaning in color alone.** Every state carries three signifiers: the text
   label, the glyph, and the border style. Glyphs use CSS `content: "\25CF" / ""` so screen
   readers announce the label only.
5. **Every page that uses badges carries the legend**, placed directly after the lead and
   source line. The legend is duplicated markup, like the nav — keep all copies identical.

```html
<!-- Legend: identical on every page that uses badges -->
<p class="source">Claims are badged by evidence strength; unbadged statements are verified as shipped.</p>
<ul class="badge-legend">
  <li><span class="badge shipped">shipped</span> released or in production</li>
  <li><span class="badge announced">announced</span> committed, not yet shipped</li>
  <li><span class="badge reported">reported</span> secondary sources only, or disputed</li>
  <li><span class="badge speculative">speculative</span> interpretation, not settled fact</li>
</ul>

<!-- Whole-paragraph claim: badge leads -->
<p><span class="badge announced">announced</span> Roadmap items — not yet shipped — include …</p>

<!-- Caveat inside a verified paragraph: badge follows the claim it qualifies -->
<p>… no primary announcement has been located, so the GA label should be read with that
caveat. <span class="badge reported">reported</span> On GitHub, the spec is on an active
v3.1.x line …</p>
```

## 6. Sourcing and freshness

Credibility is the product; these patterns are not optional.

- Every factual claim is followed by a `<p class="source">` giving the source link(s) and
  the verification date: `Source: <a …>Name</a> · last verified YYYY-MM-DD`.
- All external links carry `rel="noopener"`. Internal links are relative (the site must work
  from the filesystem and from GitHub Pages).
- Where sources conflict, say so in the prose and badge the claim `reported`. Never silently
  pick a number.
- Content that could not be verified belongs in the research note's open questions, not on a
  page.

**Freshness is a designed feature, not a byproduct.** A returning practitioner's question is
"what changed since I was here?", and two surfaces answer it:

- **`p.page-meta`** sits directly under the `h1` on every page that carries content:
  `Updated <time datetime="YYYY-MM-DD">D Month YYYY</time> · all claims on this page verified
  on that date`. Update it in the same change that updates the page — a stale meta line is
  worse than none. Stub pages carry no meta line until they carry content.
- **`ol.changelog`** is the first section of the home page, newest entry first. Each entry is
  a `<li>` holding a `p.changelog-date` with a `<time>` element, the description, and a
  `p.source`. Badge an entry only where its evidence is weaker than shipped (§5).

```html
<p class="page-meta">Updated <time datetime="2026-08-04">4 August 2026</time> · all claims on this page verified on that date</p>

<ol class="changelog">
  <li>
    <p class="changelog-date"><time datetime="2026-07-30">30 July 2026</time></p>
    <p>IAB Tech Lab released AAMP 2.3 …</p>
    <p class="source">Source: <a href="…" rel="noopener">…</a> · last verified 2026-08-04</p>
  </li>
</ol>
```

Keep the changelog to roughly the last ten developments; older entries belong on the
protocol pages' timeline tables, which are the permanent record.

## 7. Imagery — the diagram grammar

The site needs pictures, and its pictures are **diagrams**. This is not a compromise: a
protocol tracker has no honest photograph, and stock "AI" imagery is precisely the slop
banned in §1. Information-bearing figures are the only images that earn their place.

Rules:

- **Inline `<svg>` only.** Not `<img src="…svg">` — inline SVG inherits CSS custom
  properties, so one drawing works in both color schemes with no duplicate asset.
- Strokes use `currentColor` or `var(--text)`; fills use tokens. Never hardcode hex.
- One consistent visual grammar across every page: agents and services as rectangular
  nodes, protocol messages as labeled arrows, layers as stacked bands. Same stroke weight,
  same corner radius, same type size everywhere.
- **Both protocols get the identical grammar** — same node shapes, same weights. Neutrality
  is enforced by the drawing system, not by good intentions.
- Status colors may appear in diagrams *only* with their §5 meaning.
- Every figure is captioned and sourced like any other claim:

```html
<figure>
  <svg viewBox="0 0 640 240" role="img" aria-labelledby="fig1-title">
    <title id="fig1-title">AdCP and AAMP relative to the existing programmatic stack</title>
    …
  </svg>
  <figcaption class="source">Figure 1 — … · Source: <a href="…" rel="noopener">…</a> · last verified YYYY-MM-DD</figcaption>
</figure>
```

- Accessibility: `role="img"` plus a `<title>` referenced by `aria-labelledby`. The `<title>`
  must describe what the diagram *shows*, not merely name it — it is the only content a
  screen-reader user gets. If the diagram carries information not in the surrounding prose,
  put it in the prose too.
- Keep figures under ~10 KB of markup. No embedded rasters, no external requests, ever.

**Sizing.** `figure svg` is `width: 100%` with `min-width: 26rem`; below that the
`.figure-wrap` scrolls rather than shrinking the type past legibility. Verify at 360px that
the *page* does not scroll horizontally — only the figure does. Design tall rather than wide,
and keep the viewBox around 560 units so 13.5px diagram text stays readable when scaled.

**Fitting labels.** SVG text does not wrap. Break labels into separate `<text>` lines
yourself, and size boxes for the longest label they must hold — a two-column grid of 264-unit
nodes fits component names that a three-column grid of 170-unit nodes clips.

**The three built figures** — copy their structure rather than inventing a new one:
`comparison.html` (the stack: both families over MCP/A2A, AdCP parallel to OpenRTB vs. AAMP
extending it), `aamp.html` (the AAMP component map), `workflows.html` (the six-message
agent-to-agent buy sequence).

## 8. Component inventory

Existing, and to be reused rather than reinvented:

| Component | Markup | Use |
|---|---|---|
| Card grid | `ul.card-grid > li.card` | Link collections, tool entries |
| Status badge | `span.badge.{shipped\|announced\|reported\|speculative}` | Evidence strength (§5) |
| Badge legend | `ul.badge-legend` | Once per page that uses badges |
| Source line | `p.source` | Citations, captions, meta text |
| Page freshness | `p.page-meta` | "Updated \<date\>" under the `h1` (§6) |
| Changelog | `ol.changelog > li` | Dated "what changed" list, newest first (§6) |
| Table | `div.table-wrap > table` | All tabular content — the wrapper is mandatory |
| Empty state | `div.todo-content` | Sections awaiting the content pipeline |
| Figure | `figure > div.figure-wrap > svg`, then `figcaption.source` | Diagrams (§7) |
| Diagram parts | `.dgm-band`, `.dgm-node`, `.dgm-title`, `.dgm-text`, `.dgm-line`, `.dgm-line-dashed`, `.dgm-lifeline`, `.dgm-arrow` | The shared drawing grammar (§7) |

Rules: no new component without a second use case. No inline `style` attributes. New styles
go in `assets/css/style.css` — the single stylesheet — never in a `<style>` block on a page.

**Cards must be fully clickable.** A bordered, raised card promises a click target; today
only the heading link responds. Either wrap the card contents in the anchor or use a
stretched-link pseudo-element — do not ship a card whose body is dead.

## 9. Responsive and accessible

- Breakpoint-light: use `flex-wrap`, `grid-template-columns: repeat(auto-fill, minmax(…))`,
  and `rem` sizing so layouts reflow without media queries. Add a breakpoint only when
  reflow genuinely fails.
- **Verify every change at 360px, 768px, and 1280px**, in both color schemes.
- Tables are the hard case. `.table-wrap` gives horizontal scroll, which is adequate for
  short cells and inadequate for the paragraph-length cells in `comparison.html`. Until the
  roadmap fix (§11) lands, keep comparison table cells short — one or two lines — and put
  the detail in the prose sections below.
- Accessibility floor (WCAG 2.1 AA):
  - Text contrast ≥ 4.5:1 in **both** schemes. The badge palette is verified: lowest ratio
    5.84:1. Re-check with a contrast calculator whenever a color token changes.
  - Semantic landmarks (`header`, `nav`, `main`, `footer`), one `h1`, no skipped levels.
  - Visible focus states on every interactive element — never remove the outline.
  - `alt` text on images; `role="img"` + `<title>` on inline SVG.
  - Meaning never conveyed by color alone (§5, rule 4).
  - The site must be fully readable with JavaScript disabled. JS is progressive
    enhancement only.

## 10. Enforcement — what CI checks, and what reviewers must

The authors here are agents, so the guide is only as durable as its checks.

**Automated today** (`.github/workflows/ci.yml`):
- `html-validate` on every root `*.html` — well-formed, valid markup.
- `lychee --offline` — internal links and fragments resolve.

**Checked by the `site-reviewer` agent and human review** (see
`.claude/agents/site-reviewer.md`):
- Every new claim has a source link and a "last verified" date.
- Badge state matches what the source actually supports; no badge inflation (a page where
  nearly every claim is badged the same value is a defect).
- Shared nav and badge legend markup identical across pages.
- Neutral tone; no advocacy language; no protocol-specific visual treatment.
- Both color schemes and 360px width verified for any visual change.

**Worth automating next** (roadmap): a badge-density check (flag a page where one badge
state exceeds ~70% of its badges), a nav/legend parity diff across pages, and a contrast
assertion over the color tokens.

## 11. Roadmap

Deliberately deferred, in priority order. Each is a separate change, not a rewrite:

1. ~~**Freshness surfaces**~~ — done 2026-08-04. `p.page-meta` on every content page and
   `ol.changelog` as the home page's first section; see §6.
2. ~~**The first three diagrams**~~ — done 2026-08-04. Stack diagram, AAMP component map,
   and buy sequence; the grammar and sizing rules they established are in §7.
3. **Responsive comparison table** — sticky first column plus a stacked card layout below
   ~40rem using `data-label` attributes; no build step required.
4. **Remaining tokens** — spacing, type scale, and radius are still hardcoded values
   scattered through the stylesheet. Tokenizing them is a pure refactor with zero visual
   change, and it makes every later change cheaper.
5. **Clickable cards** (§8) and visibly marked stub nav links, so no navigation item
   promises a page that is still a placeholder.
6. **Masthead** — optionally, a single self-hosted display face for the wordmark only.
   Evaluate against §1 before adopting: it must add identity without adding ornament.

---

*This guide reflects a design council review of the site conducted 2026-08-04. Amend it
with the change that motivates the amendment — never let a page and this document disagree.*

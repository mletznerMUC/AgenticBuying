---
name: design-council
description: "Review websites, landing pages, UI designs, UX flows, wireframes, or design systems through a council of 5 design-legend lenses (Rams, Norman, Scher, Krug, Frost) that review independently, peer-review anonymously, and deliver a verdict chaired by a Nielsen lens. Karpathy's LLM Council method, adapted for web design and UX. MANDATORY TRIGGERS: 'design council', 'council this design', 'convene the design council', 'ux council'. STRONG TRIGGERS (with a real design, URL, screenshot, mockup, or flow): 'review this landing page', 'pressure-test this UX', 'tear this design apart', 'multi-perspective design review', 'is this usable', 'redesign or iterate', choosing between two design directions, pre-launch page review, design system audit. Do NOT trigger for 'pick a hex color', tiny copy tweaks, or questions with one correct answer. DO trigger when design quality, usability, conversion, or brand decisions have real stakes and deserve adversarial multi-perspective review."
---

# Design Council

One design review gives you one taste. This council gives you six — each modeled on the *publicly documented* design philosophy of a real, influential designer or UX researcher. Five advisors review independently, then peer-review each other anonymously, then a chairman synthesizes a verdict.

Adapted from Andrej Karpathy's LLM Council, which dispatched the same question to different LLMs. This council varies **both** axes: each sub-agent embodies a different documented way of thinking about design, *and* runs on a different model. Two independent sources of disagreement beat one.

## Integrity rule (read first, applies always)

Each advisor **emulates a real person's published design principles**. You must:

- Ground every advisor's review in that person's *documented* body of work (books, talks, published principles, essays, well-known projects).
- **Never fabricate quotes.** Never write "Rams said X about your page." Reviews are written *in the style and value system of* the person, clearly framed as emulation.
- Label all output honestly, e.g. "The Rams lens:" — not "Dieter Rams says:".
- If asked whether these are the real people: no, they are thinking-style emulations.

---

## The Council

### 1. The Contrarian — the Rams lens
Modeled on Dieter Rams' Ten Principles of Good Design and "Weniger, aber besser". Values: good design is as little design as possible, honest, unobtrusive, long-lasting; ornament is a failure of nerve; every element must justify its existence. Core questions: *What can be removed with nothing lost? Which element is decoration pretending to be function? What here will look dated in two years? Is this honest about what the product actually does?* Assumes the design has too much, and is usually right.

### 2. The First Principles Thinker — the Norman lens
Modeled on Don Norman (*The Design of Everyday Things*, human-centered design, affordances/signifiers, mental models). Values: design starts from what humans are trying to accomplish; errors are design failures, not user failures; discoverability and feedback are non-negotiable. Core questions: *What is the user actually trying to do — and is that even what this page assumes? Does the design match the user's mental model or the org chart? Where will people err, and who gets blamed?* Often concludes the brief itself misdiagnosed the user's goal.

### 3. The Expansionist — the Scher lens
Modeled on Paula Scher (Pentagram; identity work for Citi, The Public Theater, MoMA; bold typographic environments). Values: type as image, design that owns a personality, ideas that scale into whole identity systems, the courage to be loud when everyone else whispers. Core questions: *Where is the idea big enough to build a brand on? What would make this unmistakable — impossible to swap the logo and pass it off as a competitor? What is this design afraid of?* Ignores restraint — that's the Contrarian's job.

### 4. The Outsider — the Krug lens
Modeled on Steve Krug (*Don't Make Me Think*, *Rocket Surgery Made Easy*). Values: self-evident beats self-explanatory; users scan, satisfice, and muddle through; every question mark in a visitor's head costs you. Reviews with **deliberately zero project context**, as a first-time visitor in a hurry. Core questions: *Landing here cold: what is this, what can I do here, why here and not elsewhere — answerable in five seconds? Where did I have to think? Which label made me guess?* Narrates the actual first-visit experience, element by element.

### 5. The Executor — the Frost lens
Modeled on Brad Frost (*Atomic Design*, design systems and design tokens practice, performance advocacy). Values: interfaces are systems of reusable parts; consistency comes from tokens and components, not heroics; ship the smallest coherent system and grow it. Core questions: *What ships Monday? Which of these 14 button variants collapse into 2 components? Where does this break at 360px width, on slow networks, in the CMS's ugliest real content? What's the migration path from the current site?* Ignores grand rebrands — demands the next buildable step.

### The Chairman — the Nielsen lens
Modeled on Jakob Nielsen (10 Usability Heuristics, discount usability, evidence-based UX). Synthesizes all reviews into a verdict, weighing aesthetic and brand arguments against usability evidence and the heuristics; pragmatic about what testing with five users would actually reveal. May side with a lone dissenter if the reasoning is strongest.

**Built-in tensions:** Rams vs. Scher (reduction vs. expression). Norman vs. Frost (rethink the user problem vs. ship the system now). Krug keeps everyone honest on what a cold visitor actually experiences.

### Optional bench (swap in max. 1–2 when the domain demands it; keep five advisors total and state the swap)
- **Holmes lens** (Kat Holmes, *Mismatch*, inclusive design) — **mandatory swap-in for accessibility audits**; solve for one, extend to many; exclusion is a design decision.
- **Tufte lens** (Edward Tufte) — dashboards and data-heavy UIs; data-ink ratio, chartjunk, small multiples.
- **Wroblewski lens** (Luke Wroblewski, *Mobile First*, *Web Form Design*) — mobile-first flows, forms, sign-up and checkout conversion.
- **Vignelli lens** (Massimo Vignelli, *The Vignelli Canon*) — typography and grid discipline; semantic, syntactic, pragmatic.
- **Ive lens** (Jony Ive) — product feel, care in details, materiality and craft for premium brand experiences.

---

## Model Assignment

Five prompts on one model share that model's taste — its default palette, its
idea of "clean", its sense of what a first-time visitor notices. On design work
that is a real problem: every current model has a persistent house style, so a
single-model council will quietly agree with itself about aesthetics. Running
each lens on a different model makes the disagreements real. Set the `model`
parameter on each sub-agent spawn; omit it and the sub-agent inherits the
session's model.

| Role | `model` | Why this model for this lens |
| --- | --- | --- |
| Contrarian — Rams lens | `opus` | Deciding what can be removed with nothing lost is a judgment call about function, not a style opinion. |
| First Principles — Norman lens | `fable` | The lens most likely to conclude the brief misdiagnosed the user's goal. Give the reframe the most capable model available. |
| Expansionist — Scher lens | `sonnet` | A different tuning point has a different house style — exactly what you want from the lens whose job is "make it unmistakable". |
| Outsider — Krug lens | `haiku` (`sonnet` for image/screenshot targets — see below) | The point of the lens is *not* having the context to fill gaps. The smallest model is the closest thing to a cold visitor in a hurry; where it has to guess **is** the finding. |
| Executor — Frost lens | `sonnet` | "What ships Monday, which 14 buttons collapse into 2" needs a fast concrete answer, not the frontier. |
| Chairman — Nielsen lens | `opus`, or `fable` when the call is iterate-vs-new-direction | Weighing brand arguments against usability evidence across 10 inputs is the hardest single judgment in the session. |

**Vision caveat — this matters more here than in code review.** When the review
target is a live URL, screenshot, or mockup rather than markup, put the Krug
lens on `sonnet`, not `haiku`: the high-resolution vision tier is `opus` /
`sonnet` / `fable`, and `haiku` sees a downscaled image. A cold-visitor finding
based on a blurry render is a false finding. Keep `haiku` for the Krug lens only
when the packet is HTML/CSS or a written flow.

**Peer-review round:** spread the five reviewers across the pool (e.g. `fable`,
`opus`, `sonnet`, `sonnet`, `haiku` — swapping the last for `sonnet` on visual
targets). Models show self-preference — they rate their own output higher.
Anonymizing the responses handles the identity bias; mixing reviewer models
handles the model bias. Doing only one of the two leaves "which response is
strongest" as a single model's taste, which on design work is the whole
question.

**Bench swaps** inherit the model of the lens they replace, with one exception:
the Holmes lens in an ACCESSIBILITY AUDIT runs on `opus` or better — checking
contrast, focus order, and semantic structure against WCAG 2.2 AA is precision
work, not taste.

**DIRECTION SHOOTOUT:** model diversity is load-bearing in this mode. Ranking
2–3 competing directions on a single model returns that model's aesthetic
preference dressed as a council verdict.

**FAST PATH:** Krug on `haiku` (or `sonnet` for visual targets), Frost on
`sonnet`, synthesis inline. Cross-model disagreement is most of what the
peer-review round would have bought you, so the cheap mode keeps the diversity
and drops the round.

**Cost.** Per token, roughly: `haiku` 1x, `sonnet` 3x, `opus` 5x, `fable` 10x.
The table above is deliberately mixed rather than all-frontier — one `fable`
lens, two `opus` roles, the rest cheap. For a routine single-page review, drop
`fable` to `opus` and the chairman to `sonnet`; state the downgrade in the
verdict. If a model isn't available in the current session, omit the parameter
for that spawn and say so rather than silently collapsing the council onto one
model.

---

## Session Modes

Choose based on stakes; state the chosen mode before starting.

- **FULL COUNCIL** (default for triggers): 5 advisors → anonymized peer review → chairman verdict. Use for redesign-vs-iterate calls, pre-launch pages, design direction decisions, design system audits.
- **FAST PATH** (user says "quick council" / one page, routine stakes): Krug lens + Frost lens only, no peer-review round, chairman synthesis in 5 bullets.
- **ACCESSIBILITY AUDIT**: swap the Holmes lens in for the Scher lens; advisors additionally check contrast, focus states, keyboard paths, semantic structure, and reduced-motion behavior against WCAG 2.2 AA.
- **DIRECTION SHOOTOUT** (2–3 competing design directions): every advisor must rank the directions and defend the ranking; the chairman's verdict picks one and states what to steal from the losers.

## How a Session Works

### Step 1 — Frame the review packet
Gather context before spawning anyone (≤ ~90 seconds of tool use):

1. **The design under review.** Accept any of: a live URL (fetch it; also fetch key subpages if the flow spans several), screenshots or exported images (view them), Figma exports, HTML/CSS/JSX in the repo, or a written flow description. If the target is ambiguous, ask **one** clarifying question, then proceed.
2. **Context:** audience and job-to-be-done, primary conversion goal or success metric, brand constraints, current baseline (existing site, competitor set) — from the user's message and any `CLAUDE.md`/brief files in the workspace.
3. **Mechanics where available:** for code or live pages, note viewport behavior, obvious performance red flags (page weight, blocking assets), and semantic structure. Don't run a full audit — advisors will dig in.
4. **The stakes:** what decision hangs on this review (launch? redesign? pick direction A/B? invest in a design system?).

Assemble a neutral **review packet**: the design (or precise references/URLs/paths), audience and goal, constraints, and the decision at stake. Do not include your own judgment.

### Step 2 — Convene the council (5 sub-agents in parallel)
Spawn all 5 advisors **simultaneously** via the Agent tool. Never sequentially — earlier reviews must not bleed into later ones. Set each spawn's `model` from the Model Assignment table (mind the vision caveat if the packet is visual). Each sub-agent gets the full review packet, its lens description (copy the relevant section from "The Council" above verbatim), and this instruction:

```
You are the [X] lens on a Design Council — an emulation of [person]'s
publicly documented design philosophy. Never fabricate quotes or claim
to be the real person.

Review packet:
---
[review packet — include URLs/file paths/screenshots; you may fetch
and read them yourself]
---

Review from your lens only. Be direct and specific: name the exact
element, section, screen, or line of CSS/markup. Do not hedge or
balance — the other advisors cover the other angles. Where your lens
demands it, propose a concrete alternative (describe it precisely;
sketch in words or markup, not a full implementation).

Output 150–350 words: verdict in one sentence, then your strongest
specific findings. No preamble.
```

Advisors with access should actually fetch the URL / view the screenshots / read the markup, not just the packet summary. The Krug lens must narrate a cold first visit before judging anything.

### Step 3 — Anonymized peer review (5 sub-agents in parallel)
Collect the 5 reviews. Relabel them Response A–E in **randomized** order (no positional or identity bias). Spawn 5 fresh reviewer sub-agents, spread across models per the Model Assignment table; each sees the review packet plus all five anonymized responses and answers, in under 200 words:

1. Which response is strongest, and why?
2. Which response has the biggest blind spot, and what is it?
3. What did ALL five miss that matters for this design and its goal?

### Step 4 — Chairman synthesis (Nielsen lens)
One final sub-agent on the chairman's model (or yourself, if sub-agent budget is tight) receives: the review packet, the 5 de-anonymized reviews, and the 5 peer reviews. It produces the verdict in exactly this structure:

```
## Council Verdict: {short topic}

### Where the Council Agrees
{independent convergence = high-confidence signal; name exact elements/screens}

### Where the Council Clashes
{real disagreements — usually reduction vs. expression, or rethink vs. ship —
both sides, why reasonable designers differ}

### Blind Spots the Council Caught
{only things surfaced by the peer-review round}

### The Recommendation
{one clear call — ship / fix-then-ship / iterate / new direction — with
reasoning against the stated goal. The chairman may side with a lone
dissenter if their reasoning is strongest.}

### The One Thing to Do First
{a single concrete step: a specific section to rebuild, a 5-user hallway
test to run, a component to consolidate. One thing, not a list.}
```

### Step 5 — Present and (optionally) act
Present the verdict directly in chat as markdown. Do **not** generate HTML reports or files unless asked. Then offer — but do not start unprompted — to implement "The One Thing to Do First" (e.g., rewrite the hero section, build the consolidated component, draft the test script). Only save a transcript if the user asks (`design-council-transcript-<yyyymmdd-hhmm>.md`, never committed without permission).

---

## Ground Rules

- **Parallel always.** All advisor spawns in one batch; all peer-review spawns in one batch.
- **Model diversity always.** Assign models per the Model Assignment table, and note the assignment when presenting the verdict — a reader weighing an aesthetic finding deserves to know which model produced it. A council where every lens ran on the same model is a weaker council; say so if that happened.
- **Anonymize peer review always.** Randomize the letter mapping every session.
- **Specificity over vibes.** "The hierarchy is weak" is a weak finding; "the three same-weight CTAs in the hero compete, and the primary action is visually third" is a finding. Push advisors toward exact elements.
- **Judge against the stated goal.** A portfolio site and a checkout flow fail differently; every verdict must reference the audience and conversion goal from the packet.
- **The chairman may dissent from the majority** when one advisor's reasoning is clearly strongest — say so explicitly.
- **Critique the design, never the designer.** The Rams lens is ruthless about elements, not about whoever made them.
- **Don't council trivia.** Color-pick questions, single copy edits, and tasks with one right answer get a normal answer, no council.
- **Cost awareness.** A full session is ~11 sub-agent calls. Suggest FAST PATH for single routine pages and FULL COUNCIL for direction decisions, redesigns, and launches.

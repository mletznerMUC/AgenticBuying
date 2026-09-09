# Local source registry

Some of this project's strongest evidence is not on the web. This file is the register of
that material: where it lives, what each file is, how far it may travel into the
repository, and which rule wins when it disagrees with a public source.

**Read this file before any research or update run that touches out-of-home or SDAW.**
It is listed as a binding pre-flight step in `CLAUDE.md` and in the `research-analyst`,
`content-writer` and `site-reviewer` agent definitions.

---

## The folder

```
/Users/mletzner/Library/CloudStorage/OneDrive-StroeerGlobalDirectory/Letzner/AI/Agentic Advertising
```

It is a OneDrive folder on the maintainer's workstation. It is **not** part of the
repository and must never be copied into it — see *What may enter the repository* below.

### Reachability

The folder is reachable only from a local session on that workstation. Agent runs in a
cloud container (Claude Code on the web, the GitHub Action) cannot see it, and a run that
assumes otherwise will silently produce nothing.

Test for it before planning any work that depends on it:

```bash
SDAW_SRC="/Users/mletzner/Library/CloudStorage/OneDrive-StroeerGlobalDirectory/Letzner/AI/Agentic Advertising"
[ -d "$SDAW_SRC" ] && echo reachable || echo "not reachable — work from the extracts"
```

- **Reachable** — verify against the original documents, and refresh the extracts under
  `docs/research/sources/sdaw/` with anything that has changed.
- **Not reachable** — work from those extracts, treat them as the authority, and do not
  publish a norm-level claim the extracts do not carry. Where the extracts are marked
  incomplete, the claim waits for a run that has the folder.

---

## Inventory

Classification decides how far a file's content may travel:

| Class | Meaning |
|---|---|
| `public` | Publicly obtainable. Cite and link normally. |
| `nonpublic-primary` | Authoritative, but the reader cannot retrieve it. Facts derived from it may be published; the file may not. Badge such claims `primary-nonpublic` (`docs/DESIGN.md` §5). |
| `internal-do-not-publish` | Never published in any form. Not quoted, not paraphrased, not summarized, not used as an unattributed background assumption. |

### SDAW Norm/

| File | Role | Class |
|---|---|---|
| `SDAW004_Juni2025.pdf` | The norm itself — SDAW version 004, revision date 11 June 2025, B\|A\|M Bundesverband Aussenmedien. 29 record types, appendices A–E. | `nonpublic-primary` |
| `Objektarten Juni 2025.pdf` | Appendix A, the site-class list. **No text layer** — needs OCR (`pdftoppm` at 300–600 dpi, then `tesseract -l deu`). | `nonpublic-primary` |
| `S&P Produktliste.pdf` | Appendix B, the 236 product codes used for product exclusions. | `nonpublic-primary` |
| `aushangtermine_plakat_2027_zusammengeführt.xlsx` | The 2027 decade and week posting calendar; sheet `BASIS`. | `nonpublic-primary` |

### SDAW Beispieldateien/

Real production files from one lessee, fiscal year 2017, lessee number 368. They are the
ground truth the field positions are validated against, and they are large.

| File | Size | Role | Class |
|---|---|---|---|
| `STA36817.TXT` | 64 MB | Panel master data | `nonpublic-primary` |
| `FRE36817.TXT` | 27 MB | Availability | `nonpublic-primary` |
| `LWT36817.TXT` | 3.2 MB | Performance values | `nonpublic-primary` |
| `VSA36817.TXT` | small | Dispatch addresses | `nonpublic-primary` |

These carry a real operator's inventory. Never print a record, a field value, an address
or an identifier from them into a report, a note, a commit message or a page — statistics
and distributions only. `validate.py` enforces this by construction.

### AdCP/

| File | Role | Class |
|---|---|---|
| `adcp_roles.xlsx` | The 13 AdCP roles with their legacy mapping. Content is public; the spreadsheet is a convenience copy. | `public` |

### Excluded from all use

These are listed by name only, so that a run can match and skip them. Their contents
are deliberately not described here — this file is repository content, and a description
of an internal document is itself a disclosure.

| Path | Class |
|---|---|
| `Stammdatenmeldungen DOOH PDOOH/` | `internal-do-not-publish` |
| `SDAW_Modernisierung_MvB 20260813.pptx` | `internal-do-not-publish` |

For the excluded files this means, concretely: no timelines, no project or workstream
names, no scope or milestone dates, no resourcing or prioritization, no target
architectures quoted as internal plans, and no inventory or impression figures. If a
sentence would not survive the question *"could a reader outside the company have written
this?"*, it does not ship.

---

## Precedence

**The norm beats every secondary source.** Where `SDAW004_Juni2025.pdf` and a public
source disagree, the norm is right and the disagreement is worth stating on the page.

This retires a specific earlier practice. The site's SDAW content was originally
reconstructed from three open-source repositories by one author —
[`mckoch/open-sdaw`](https://github.com/mckoch/open-sdaw),
[`mckoch/sdxist`](https://github.com/mckoch/sdxist) and
[`mckoch/sdaw-import`](https://github.com/mckoch/sdaw-import), published 2011–2013. They
remain **citable as historical evidence** — of what was publicly knowable about the format
then, and of the fact that an independent implementation existed. They are **no longer a
field authority**: never cite them for a field position, length, code list or record
layout. That is the norm's job, and the extracts carry it.

Where the norm disagrees with itself — and it does, in places — say so and show both
sides. `validate.py` exists to find exactly those cases against real data.

---

## Derived extracts

Structured extracts live in [`sdaw/`](sdaw/) and are what an agent without folder access
works from. See [`sdaw/README.md`](sdaw/README.md) for their provenance, their schema,
how they are regenerated and when they were last validated against production data.

## Keeping this register current

The folder gains files. Every run that can reach it re-lists it, and any file not in the
inventory above is added here with a role and a classification **before** its content is
used. A file whose classification is unclear is treated as `internal-do-not-publish` until
the maintainer says otherwise.

```bash
find "$SDAW_SRC" -type f | sed "s|$SDAW_SRC/||" | sort
```

---

*Registry created 2026-09-09.*

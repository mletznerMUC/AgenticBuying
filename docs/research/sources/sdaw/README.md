# SDAW extracts

Structured extracts from the SDAW norm and its appendices. They exist so that the site can
publish norm-level facts without the norm itself entering the repository, and so that an
agent that cannot reach the source folder still has something authoritative to work from.

**These files are the field authority for SDAW.** Not the page, not the research notes, and
in particular not the 2011–2013 open-source toolchain the site's first SDAW pass was built
from — see [`../local-context.md`](../local-context.md) for why that toolchain is now
historical evidence only.

---

## What they are drawn from

| Extract | Source |
|---|---|
| `record-types.json` | The norm's record-type catalog |
| `sta-layout.json` | The norm's STA record layout, plus its encoding rules |
| `lwt-layout.json` | The norm's LWT layout, appendix C 10 and appendix D 06 |
| `fre-layout.json` | The norm's FRE layout — **stub, nothing extracted yet** |
| `vsa-layout.json` | The norm's VSA layout and appendix C 07 |
| `objektarten.json` | Appendix A, `Objektarten Juni 2025.pdf` |
| `produktliste.json` | Appendix B, `S&P Produktliste.pdf` |
| `dekadenplan-2027.json` | `aushangtermine_plakat_2027_zusammengeführt.xlsx`, sheet `BASIS` |
| `changelog.json` | Appendix E |

The norm behind all of them is **SDAW version 004, revision date 11 June 2025, B|A|M
Bundesverband Aussenmedien**. Version 004 has been current since 2002/2003 and is amended
in place; the version number does not move, the revision date does. Always read
`source_date`, never the version, to know how current an extract is.

Every file carries `source`, `source_version`, `source_date`, `extracted_on`, `confidence`,
`completeness` and `provenance` at the top level.

## Completeness — read this before using them

**Every extract is currently `partial` or `stub`.** They were populated from the
maintainer's structured reading of the norm on 2026-09-09, not from a machine extraction
pass, because the run that created them could not reach the source folder. What is present
is norm-attested and safe to publish. What is missing is listed explicitly in each file's
`pending` array.

The largest gaps, in the order they are worth closing:

1. **`sta-layout.json`** — the complete D-record field list. 22 fields are recorded against
   a minimum record length of 499. The QID and QID-Kennz positions matter most: the
   panel-identity argument on `sdaw.html` rests on QID, and no production check of it can
   run without them.
2. **`objektarten.json`** — the 20 main and 152 sub site classes. Counts, structural rules,
   digital classes and the three known anomalies are recorded; the individual entries are
   not. This blocks the Stellenart range check in `validate.py`.
3. **`produktliste.json`** — the 25 main groups and 236 codes. Counts and the 2024 political
   and religious ranges are recorded; the codes are not.
4. **`dekadenplan-2027.json`** — the derivation rules and the B|A|M caveats are complete;
   the 34 dated decades and 52 weeks are not. A consumer can compute dates from the rules
   given one anchor date per decade, which the extract does not yet carry.
5. **`record-types.json`** — 21 of the norm's 29 record types, without direction,
   order-relation flag, page number or introduction date.
6. **`changelog.json`** — 4 of the appendix E entries spanning 2003-05-07 to 2025-06-11.
7. **`fre-layout.json`** — nothing.

A claim the extracts do not carry does not go on a page. Where a page needs one, it waits
for a run with folder access rather than borrowing the number from a secondary source.

## Regenerating them

Requires the source folder. Check reachability first —
[`../local-context.md`](../local-context.md) has the test.

```bash
export SDAW_SOURCE_DIR="/Users/mletzner/Library/CloudStorage/OneDrive-StroeerGlobalDirectory/Letzner/AI/Agentic Advertising"
```

**The norm, appendices B–E, and the calendar** carry text layers. Read them directly and
transcribe into the JSON shapes already established by the files in this directory — keep
the key names, extend the arrays.

**Appendix A (`Objektarten Juni 2025.pdf`) has no text layer.** It needs rasterizing and
OCR:

```bash
pdftoppm -r 400 -png "$SDAW_SOURCE_DIR/SDAW Norm/Objektarten Juni 2025.pdf" /tmp/objektarten
for f in /tmp/objektarten-*.png; do tesseract "$f" "${f%.png}" -l deu; done
```

Then **read every code back by eye against the page images**. OCR confusions in a
two-character code — `0`/`O`, `1`/`I`, `5`/`S`, `8`/`B` — are silent and propagate into
field validation as false discrepancies. This is the one step that cannot be automated
away.

When an extract changes, re-run the validation below and update `extracted_on`,
`completeness` and `pending` in the same change.

## Validating them

`validate.py` checks the layouts against four production files from one lessee (number 368,
fiscal year 2017) and writes `validation-report.md`.

```bash
python3 validate.py --source-dir "$SDAW_SOURCE_DIR"
# or, with SDAW_SOURCE_DIR exported:
python3 validate.py
```

Exit code 0 means no discrepancies; 1 means at least one; 2 means the folder was not found.

It checks record-length distributions per file and record kind, K/D/S/E structure, value
ranges per field, coordinate fill and plausibility, QID fill and uniqueness, the
138-character FAW description sheet, product exclusions, and Windows-1252 conformance.

Three properties of the script are load-bearing, and a change that breaks any of them is a
bug:

- **It streams.** `STA36817.TXT` is 64 MB and is never held in memory.
- **It emits statistics only.** The production files carry a real operator's inventory. No
  record, field value, identifier or address may reach the report.
- **It does not resolve disagreements.** Where an extract and the data differ, it reports a
  discrepancy and keeps both numbers. Never edit an extract to silence one — take it to the
  maintainer, because "the norm was misread" and "the norm is inconsistent" need different
  fixes.

Checks whose field positions are still `pending` report themselves as *not checked* and
start working on their own once the extraction is completed. No change to the script is
needed as the extracts fill in.

### Reference values

Verified against these files previously. The script must reproduce them, and flags any
divergence rather than adopting the new number:

| File | Value |
|---|---|
| VSA | 95 D records, all exactly **523** characters — matches the norm |
| LWT | 50,300 D records, all exactly **63** characters — the norm says **64** |
| LWT `Bezugsquelle` | 48,879 × `P`, 1,421 × `V`, 0 × `X` |
| LWT `Bezugsterminart` | 45,373 × `D` (decade), 4,927 × `W` (week) |

The LWT length is a **documented inconsistency of the norm**, not an error in the data or
in the extract. It is carried as such in `lwt-layout.json`, in the report, and on
`sdaw.html`. Do not "fix" either side.

### Validation status

`validation-report.md` **has not been generated yet.** The run that created this directory
had no folder access, so no production file could be opened. The script itself was
exercised end to end against a synthetic fixture reproducing the record geometry — 499-byte
STA D records, 63-byte LWT, 523-byte VSA, K/D/S/E framing, planted range and charset
violations — and reproduced the fixture's planted defects and its uniform record lengths
correctly. That verifies the code, not the extracts.

The first run with folder access must generate the report and commit it beside these files.

---

*Directory created 2026-09-09.*

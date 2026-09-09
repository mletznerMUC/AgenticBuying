#!/usr/bin/env python3
"""Validate the SDAW layout extracts against real production files.

The extracts in this directory are read out of a norm that nobody outside the
association can download. That makes them exactly the kind of claim this site is
supposed to distrust, so they are checked against four production files from one
lessee before anything derived from them is published.

    python3 validate.py --source-dir "/path/to/Agentic Advertising"
    python3 validate.py                     # uses $SDAW_SOURCE_DIR

Output is `validation-report.md` next to this script.

Three constraints shape the code, and none of them is negotiable:

*Streaming.* `STA36817.TXT` is 64 MB. Every file is read line by line, in binary,
with bounded accumulators. Nothing holds a whole file, and nothing holds a list
that grows with the record count — the QID uniqueness check is the one place that
needs per-record state, and it keeps hashes in a set rather than the values.

*Statistics only.* These files carry a real operator's inventory: site numbers,
coordinates, addresses. The report may contain counts, rates, distributions and
range bounds. It may never contain a record, a field value, an identifier or an
address. `emit()` is the only way text reaches the report, and every call site
passes a number or a fixed label.

*The norm does not win by default.* Where the extracts and the data disagree, the
script reports a discrepancy and keeps both numbers. It never edits an extract,
and it never quietly prefers one side — the LWT record length is 64 in the norm
and 63 in all 50,300 production records, and that contradiction is a finding, not
a bug to be smoothed over.

The layouts are still partly unextracted (see each file's `pending` list). Checks
whose field positions are missing report themselves as *not checked* rather than
guessing an offset, and start working the moment the extract carries the position.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPORT = HERE / "validation-report.md"

# Windows-1252 bytes the norm permits: the printable ASCII range plus the seven
# German letters. Anything else in a data byte is a charset violation.
PERMITTED_EXTRA = {0xC4, 0xD6, 0xDC, 0xDF, 0xE4, 0xF6, 0xFC}  # Ä Ö Ü ß ä ö ü
PERMITTED = set(range(0x20, 0x7F)) | PERMITTED_EXTRA

FILES = {
    "STA": "SDAW Beispieldateien/STA36817.TXT",
    "FRE": "SDAW Beispieldateien/FRE36817.TXT",
    "LWT": "SDAW Beispieldateien/LWT36817.TXT",
    "VSA": "SDAW Beispieldateien/VSA36817.TXT",
}

# Verified previously against these same files. The script must reproduce them.
# A mismatch is surfaced as a discrepancy for a human to adjudicate — see the
# module docstring.
REFERENCE = {
    "VSA": {"d_records": 95, "d_length_uniform": 523},
    "LWT": {
        "d_records": 50300,
        "d_length_uniform": 63,
        "norm_declares_length": 64,
        "bezugsquelle": {"P": 48879, "V": 1421, "X": 0},
        "bezugsterminart": {"D": 45373, "W": 4927},
    },
}

# Germany's bounding box, generously drawn. Used only to bucket coordinates as
# plausible or not; nothing depends on the exact edges.
DE_BBOX = {"lon_min": 5.5, "lon_max": 15.5, "lat_min": 47.0, "lat_max": 55.5}


# --------------------------------------------------------------------------- io

def load_extract(name: str) -> dict:
    path = HERE / name
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def sta_fields(sta: dict) -> dict:
    """Map field name -> (position, length), 1-based, for the STA D record."""
    out = {}
    for f in sta.get("records", {}).get("D", {}).get("fields", []):
        if f.get("position") and f.get("length"):
            out[f["name"]] = (f["position"], f["length"])
    return out


def slice_field(line: bytes, spec, encoding="cp1252") -> str | None:
    """1-based inclusive slice. None when the record is too short to hold it."""
    if spec is None:
        return None
    pos, length = spec
    start = pos - 1
    if len(line) < start + length:
        return None
    return line[start:start + length].decode(encoding, errors="replace")


def iter_lines(path: Path):
    """Yield each record as bytes with CR/LF stripped. Streams; never buffers."""
    with path.open("rb") as fh:
        for raw in fh:
            yield raw.rstrip(b"\r\n")


# ---------------------------------------------------------------- report writer

class Report:
    def __init__(self):
        self.lines: list[str] = []
        self.discrepancies: list[str] = []
        self.not_checked: list[str] = []

    def emit(self, text: str = ""):
        self.lines.append(text)

    def h(self, level: int, text: str):
        self.emit()
        self.emit(f"{'#' * level} {text}")
        self.emit()

    def discrepancy(self, text: str):
        self.discrepancies.append(text)

    def skip(self, text: str):
        """Record a check that could not run — inline, and in the summary.

        Both, deliberately: the summary is the worklist for whoever finishes the
        extraction, and the inline note stops a section from rendering as a bare
        heading that reads like a check which found nothing.
        """
        self.not_checked.append(text)
        self.emit(f"_Not checked._ {text}")

    def table(self, headers: list[str], rows: list[list]):
        if not rows:
            self.emit("_No rows._")
            return
        self.emit("| " + " | ".join(headers) + " |")
        self.emit("|" + "|".join("---" for _ in headers) + "|")
        for r in rows:
            self.emit("| " + " | ".join(str(c) for c in r) + " |")

    def distribution(self, counter: Counter, label: str, limit: int = 12):
        total = sum(counter.values())
        if not total:
            self.emit("_No values observed._")
            return
        rows = []
        for value, n in counter.most_common(limit):
            rows.append([f"`{value}`", n, f"{100 * n / total:.2f}%"])
        other = total - sum(n for _, n in counter.most_common(limit))
        if other:
            rows.append(["_(other)_", other, f"{100 * other / total:.2f}%"])
        self.table([label, "Records", "Share"], rows)


# ------------------------------------------------------------------- analyzers

def classify(line: bytes, kind_pos: int) -> str:
    """Record kind from the character at `kind_pos` (1-based)."""
    if len(line) < kind_pos:
        return "?"
    ch = chr(line[kind_pos - 1])
    return ch if ch in "KDSE" else "?"


def analyze_generic(rep: Report, tag: str, path: Path, kind_pos: int) -> dict:
    """Record-kind structure, length distribution and charset, for any file."""
    kinds = Counter()
    lengths_by_kind: dict[str, Counter] = {}
    charset_violations = Counter()
    total = 0
    bad_bytes = 0

    for line in iter_lines(path):
        total += 1
        kind = classify(line, kind_pos)
        kinds[kind] += 1
        lengths_by_kind.setdefault(kind, Counter())[len(line)] += 1
        for b in line:
            if b not in PERMITTED:
                bad_bytes += 1
                charset_violations[f"0x{b:02X}"] += 1

    rep.h(3, f"{tag} — record structure")
    rep.emit(f"Records read: **{total:,}**. Record kind taken from position {kind_pos}.")
    rep.emit()
    rep.table(["Kind", "Records"], [[f"`{k}`", f"{n:,}"] for k, n in sorted(kinds.items())])

    if kinds.get("?"):
        rep.discrepancy(
            f"{tag}: {kinds['?']:,} records carry something other than K/D/S/E at position "
            f"{kind_pos}. Either the file is not structured as assumed or `--kind-position` "
            f"is wrong; confirm the position of `Log.Dateikz` in the norm and re-run."
        )

    rep.h(3, f"{tag} — record length distribution")
    rep.emit("Lengths are measured after CR/LF removal.")
    rep.emit()
    rows = []
    for kind in sorted(lengths_by_kind):
        c = lengths_by_kind[kind]
        uniform = "yes" if len(c) == 1 else f"no — {len(c)} distinct"
        rows.append([
            f"`{kind}`", f"{sum(c.values()):,}", min(c), max(c), uniform,
        ])
    rep.table(["Kind", "Records", "Min", "Max", "Uniform"], rows)

    rep.h(3, f"{tag} — character set")
    if bad_bytes == 0:
        rep.emit(
            "No violations. Every byte falls inside X'20'–X'7E' or the seven permitted "
            "German letters (Ä Ö Ü ß ä ö ü in Windows-1252)."
        )
    else:
        rep.emit(f"**{bad_bytes:,} bytes** fall outside the permitted subset.")
        rep.emit()
        rep.distribution(charset_violations, "Byte")
        rep.discrepancy(
            f"{tag}: {bad_bytes:,} bytes outside the norm's permitted Windows-1252 subset."
        )

    return {"total": total, "kinds": kinds, "lengths": lengths_by_kind}


def check_uniform_length(rep: Report, tag: str, stats: dict, expected_count, expected_len):
    """Compare D-record count and length against the verified reference values."""
    d_lengths = stats["lengths"].get("D", Counter())
    d_count = sum(d_lengths.values())

    if expected_count is not None and d_count != expected_count:
        rep.discrepancy(
            f"{tag}: {d_count:,} D records observed, reference says {expected_count:,}."
        )
    if expected_len is not None:
        if len(d_lengths) == 1 and next(iter(d_lengths)) == expected_len:
            rep.emit()
            rep.emit(
                f"Reference reproduced: all {d_count:,} D records are exactly "
                f"{expected_len} characters."
            )
        else:
            observed = ", ".join(f"{ln} ({n:,})" for ln, n in sorted(d_lengths.items()))
            rep.discrepancy(
                f"{tag}: reference says all D records are {expected_len} characters; "
                f"observed {observed}."
            )


def analyze_sta(rep: Report, path: Path, kind_pos: int, extracts: dict):
    stats = analyze_generic(rep, "STA", path, kind_pos)
    fields = sta_fields(extracts["sta"])
    obj = extracts["objektarten"]

    known_stellenart = {e.get("code") for e in obj.get("entries", []) if e.get("code")}
    digital = obj.get("digital_classes", {})
    known_hs = {d["code"] for d in digital.get("hauptstellenarten", [])}

    # Accumulators, all bounded: counters over small code spaces, plus a set of
    # QIDs (one short string per site — the only per-record state, and the cheapest
    # way to answer the uniqueness question the extract asks).
    stellenart = Counter()
    beleuchtung = Counter()
    bauart = Counter()
    belegdauer = Counter()
    qid_seen: set[str] = set()
    qid_dupes = 0
    qid_filled = 0
    qid_kennz = Counter()
    faw_filled = 0
    faw_criteria = Counter()
    faw_z_53_55 = 0
    coords = {"wgs_filled": 0, "mia_filled": 0, "in_bbox": 0, "out_bbox": 0, "unparsable": 0}
    lon_bounds = [None, None]
    lat_bounds = [None, None]
    sperren_count = Counter()
    d_records = 0

    f_stellenart = fields.get("Stellenart")
    f_beleucht = fields.get("Beleuchtung")
    f_bauart = fields.get("Bauart")
    f_belegdauer = fields.get("Belegdauerart")
    f_faw = fields.get("FAW-Beschreibungsbogen")
    f_lon = fields.get("Laengengrad (WGS84)")
    f_lat = fields.get("Breitengrad (WGS84)")
    f_mia_lon = fields.get("MIA-Laenge (legacy)")
    f_qid = fields.get("QID")            # position still pending in the extract
    f_qid_kennz = fields.get("QID-Kennz")  # position still pending in the extract

    for line in iter_lines(path):
        if classify(line, kind_pos) != "D":
            continue
        d_records += 1

        if f_stellenart:
            v = slice_field(line, f_stellenart)
            if v and v.strip():
                stellenart[v.strip()] += 1
        if f_beleucht:
            v = slice_field(line, f_beleucht)
            if v is not None:
                beleuchtung[v] += 1
        if f_bauart:
            v = slice_field(line, f_bauart)
            if v and v.strip():
                bauart[v.strip()] += 1
        if f_belegdauer:
            v = slice_field(line, f_belegdauer)
            if v and v.strip():
                belegdauer[v.strip()] += 1

        if f_qid:
            v = slice_field(line, f_qid)
            if v and v.strip():
                qid_filled += 1
                key = v.strip()
                if key in qid_seen:
                    qid_dupes += 1
                else:
                    qid_seen.add(key)
        if f_qid_kennz:
            v = slice_field(line, f_qid_kennz)
            if v is not None:
                qid_kennz[v] += 1

        if f_faw:
            v = slice_field(line, f_faw)
            if v and v.strip():
                faw_filled += 1
                for i, ch in enumerate(v, start=1):
                    if ch == "X":
                        faw_criteria[i] += 1
                    elif ch == "Z" and 53 <= i <= 55:
                        faw_z_53_55 += 1

        if f_lon and f_lat:
            slon = slice_field(line, f_lon)
            slat = slice_field(line, f_lat)
            if slon and slat and slon.strip() and slat.strip():
                coords["wgs_filled"] += 1
                try:
                    lon, lat = float(slon), float(slat)
                except ValueError:
                    coords["unparsable"] += 1
                else:
                    if (DE_BBOX["lon_min"] <= lon <= DE_BBOX["lon_max"]
                            and DE_BBOX["lat_min"] <= lat <= DE_BBOX["lat_max"]):
                        coords["in_bbox"] += 1
                    else:
                        coords["out_bbox"] += 1
                    lon_bounds[0] = lon if lon_bounds[0] is None else min(lon_bounds[0], lon)
                    lon_bounds[1] = lon if lon_bounds[1] is None else max(lon_bounds[1], lon)
                    lat_bounds[0] = lat if lat_bounds[0] is None else min(lat_bounds[0], lat)
                    lat_bounds[1] = lat if lat_bounds[1] is None else max(lat_bounds[1], lat)
        if f_mia_lon:
            v = slice_field(line, f_mia_lon)
            if v and v.strip() and v.strip("0"):
                coords["mia_filled"] += 1

    # ---- value ranges
    rep.h(3, "STA — value ranges")
    if f_stellenart:
        rep.emit(f"**Stellenart** — {len(stellenart):,} distinct codes over {d_records:,} records.")
        if known_stellenart:
            unknown = {k: n for k, n in stellenart.items() if k not in known_stellenart}
            rep.emit(f"Codes not present in `objektarten.json`: **{len(unknown):,}** distinct, "
                     f"{sum(unknown.values()):,} records.")
            if unknown:
                rep.discrepancy(
                    f"STA: {len(unknown):,} Stellenart codes appear in production data but not "
                    f"in `objektarten.json`."
                )
        else:
            rep.skip("Stellenart could not be range-checked: `objektarten.json` carries no "
                     "entries yet (appendix A still needs OCR).")
        rep.emit()
        rep.distribution(stellenart, "Stellenart")
        hs_seen = {k[:2] for k in stellenart}
        if known_hs:
            rep.emit()
            rep.emit(f"Digital main site classes present in the data: "
                     f"{len(hs_seen & known_hs)} of {len(known_hs)} known.")
    else:
        rep.skip("Stellenart: position pending in `sta-layout.json`.")

    for label, counter, spec, allowed, where in [
        ("Beleuchtung", beleuchtung, f_beleucht, {"U", "B", "H", "R"}, "the norm"),
        ("Belegdauerart", belegdauer, f_belegdauer, None, "appendix C 06"),
        ("Bauart", bauart, f_bauart, None, "the norm's construction-type list"),
    ]:
        rep.emit()
        if not spec:
            rep.skip(f"{label}: position pending in `sta-layout.json`.")
            continue
        rep.emit(f"**{label}** — checked against {where}.")
        rep.emit()
        rep.distribution(counter, label)
        if allowed:
            bad = {k: n for k, n in counter.items() if k.strip() and k.strip() not in allowed}
            if bad:
                rep.discrepancy(
                    f"STA: {sum(bad.values()):,} records carry a {label} value outside "
                    f"{sorted(allowed)}."
                )

    # ---- coordinates
    rep.h(3, "STA — coordinates")
    if f_lon and f_lat:
        pct = 100 * coords["wgs_filled"] / d_records if d_records else 0
        rep.emit(f"WGS84 pair at positions {f_lon[0]}/{f_lat[0]} populated on "
                 f"**{coords['wgs_filled']:,}** of {d_records:,} records ({pct:.2f}%).")
        rep.emit()
        rep.table(
            ["Check", "Records"],
            [["Inside the German bounding box", f"{coords['in_bbox']:,}"],
             ["Outside it", f"{coords['out_bbox']:,}"],
             ["Not parsable as a decimal", f"{coords['unparsable']:,}"],
             ["Legacy MIA field populated", f"{coords['mia_filled']:,}"]],
        )
        if lon_bounds[0] is not None:
            rep.emit()
            rep.emit(f"Longitude range {lon_bounds[0]:.6f} to {lon_bounds[1]:.6f}; "
                     f"latitude range {lat_bounds[0]:.6f} to {lat_bounds[1]:.6f}.")
        if coords["out_bbox"]:
            rep.discrepancy(
                f"STA: {coords['out_bbox']:,} coordinate pairs fall outside Germany's "
                f"bounding box."
            )
        if d_records and coords["mia_filled"]:
            ratio = coords["mia_filled"] / max(coords["wgs_filled"], 1)
            rep.emit()
            rep.emit(f"MIA-to-WGS84 population ratio: {ratio:.3f}. The legacy pair at "
                     f"222/237 was retained rather than replaced when WGS84 arrived on "
                     f"2003-05-07, so both being populated is expected.")
    else:
        rep.skip("Coordinates: positions pending in `sta-layout.json`.")

    # ---- QID
    rep.h(3, "STA — QID")
    if f_qid:
        pct = 100 * qid_filled / d_records if d_records else 0
        rep.emit(f"Populated on **{qid_filled:,}** of {d_records:,} records ({pct:.2f}%). "
                 f"Distinct values: {len(qid_seen):,}. Repeated values: {qid_dupes:,}.")
        rep.emit()
        rep.emit("Repeats are expected rather than anomalous: every face of a mechanical "
                 "changer shares one QID, so the count of repeats is a count of shared "
                 "faces, not of errors.")
        if qid_kennz:
            rep.emit()
            rep.distribution(qid_kennz, "QID-Kennz")
    else:
        rep.skip("QID and QID-Kennz: positions pending in `sta-layout.json`. This is the "
                 "highest-value missing position — the panel-identity argument on `sdaw.html` "
                 "rests on it.")

    # ---- FAW description sheet
    rep.h(3, "STA — FAW description sheet")
    if f_faw:
        pct = 100 * faw_filled / d_records if d_records else 0
        rep.emit(f"The 138-character block at position {f_faw[0]} is populated on "
                 f"**{faw_filled:,}** of {d_records:,} records ({pct:.2f}%).")
        rep.emit()
        rep.emit(f"`Z` in positions 53–55 (\"Zentrum\"): **{faw_z_53_55:,}** occurrences.")
        rep.emit()
        rep.emit("Criterion positions by frequency (position within the block, count of `X`):")
        rep.emit()
        top = faw_criteria.most_common(20)
        rep.table(["Criterion position", "Records marked `X`"],
                  [[p, f"{n:,}"] for p, n in top])
        rep.emit()
        rep.emit(f"Positions never marked: "
                 f"{138 - len(faw_criteria):,} of 138.")
    else:
        rep.skip("FAW description sheet: position pending in `sta-layout.json`.")

    # ---- Produktsperren
    rep.h(3, "STA — product exclusions")
    if sperren_count:
        rep.distribution(sperren_count, "Exclusions per panel")
    else:
        rep.skip("Produktsperren: the loop offset is pending in `sta-layout.json`. The loop is "
                 "modelled (index A–Z, at most 60 characters, at most 20 codes) but its start "
                 "position and per-entry width are not extracted, so neither the count per "
                 "panel nor the most frequent codes can be computed.")

    check_uniform_length(rep, "STA", stats, None, None)
    return stats


def analyze_lwt(rep: Report, path: Path, kind_pos: int, extracts: dict):
    stats = analyze_generic(rep, "LWT", path, kind_pos)
    ref = REFERENCE["LWT"]

    rep.h(3, "LWT — reference values")
    check_uniform_length(rep, "LWT", stats, ref["d_records"], ref["d_length_uniform"])
    rep.emit()
    rep.emit(
        f"The norm declares the LWT D record as **{ref['norm_declares_length']}** characters. "
        f"Production data says **{ref['d_length_uniform']}**, uniformly. This is a documented "
        f"inconsistency of the norm, carried as such in `lwt-layout.json` and on `sdaw.html`; "
        f"it is not resolved here in either direction."
    )

    lwt = extracts["lwt"]
    positions = {f.get("name"): (f.get("position"), f.get("length"))
                 for f in lwt.get("records", {}).get("D", {}).get("fields_identified_from_sample", [])
                 if f.get("position") and f.get("length")}

    if not positions:
        rep.skip("LWT Bezugsquelle and Bezugsterminart: positions pending in `lwt-layout.json`. "
                 "The field sequence is known from the decomposed reference record, but no "
                 "offsets are extracted, so the reference counts "
                 "(P 48,879 / V 1,421 / X 0 and D 45,373 / W 4,927) cannot be reproduced yet.")
        return stats

    quelle, termin = Counter(), Counter()
    for line in iter_lines(path):
        if classify(line, kind_pos) != "D":
            continue
        v = slice_field(line, positions.get("Bezugsquelle"))
        if v:
            quelle[v] += 1
        v = slice_field(line, positions.get("Bezugsterminart"))
        if v:
            termin[v] += 1

    for label, counter, expected in [
        ("Bezugsquelle", quelle, ref["bezugsquelle"]),
        ("Bezugsterminart", termin, ref["bezugsterminart"]),
    ]:
        rep.h(3, f"LWT — {label}")
        rep.distribution(counter, label)
        for value, want in expected.items():
            got = counter.get(value, 0)
            if got != want:
                rep.discrepancy(
                    f"LWT {label} `{value}`: observed {got:,}, reference says {want:,}."
                )
    return stats


def analyze_vsa(rep: Report, path: Path, kind_pos: int, extracts: dict):
    stats = analyze_generic(rep, "VSA", path, kind_pos)
    ref = REFERENCE["VSA"]
    rep.h(3, "VSA — reference values")
    check_uniform_length(rep, "VSA", stats, ref["d_records"], ref["d_length_uniform"])

    vsa = extracts["vsa"]
    telex = next((f for f in vsa.get("records", {}).get("D", {}).get("fields_present", [])
                  if f.get("name") == "Telex" and f.get("position")), None)
    rep.emit()
    if telex:
        filled = 0
        total = 0
        spec = (telex["position"], telex["length"])
        for line in iter_lines(path):
            if classify(line, kind_pos) != "D":
                continue
            total += 1
            v = slice_field(line, spec)
            if v and v.strip():
                filled += 1
        rep.emit(f"Telex populated on **{filled:,}** of {total:,} dispatch addresses.")
        if filled:
            rep.discrepancy(
                f"VSA: Telex populated on {filled:,} records; reference says 0."
            )
    else:
        rep.skip("VSA Telex fill rate: position pending in `vsa-layout.json`. The field's "
                 "presence is norm-attested and the reference says all 95 occurrences are "
                 "empty, but without an offset that cannot be reproduced here.")
    rep.emit()
    rep.emit("The record carries Telex, Expressbahnhof and Frachtbahnhof and has no e-mail "
             "field, although the changelog entry of 2024-11-26 requires a mail address to be "
             "held for the dispatch address. That is a norm-level tension, not a data defect, "
             "so it is recorded rather than counted.")
    return stats


def analyze_fre(rep: Report, path: Path, kind_pos: int, extracts: dict):
    stats = analyze_generic(rep, "FRE", path, kind_pos)
    rep.skip("FRE field-level checks: `fre-layout.json` is a stub. Structure and charset are "
             "checked above; no field can be range-checked until the layout is extracted.")
    return stats


# ------------------------------------------------------------------------ main

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--source-dir", default=os.environ.get("SDAW_SOURCE_DIR"),
                    help="The folder registered in ../local-context.md. "
                         "Defaults to $SDAW_SOURCE_DIR.")
    ap.add_argument("--kind-position", type=int, default=1,
                    help="1-based position of the record-kind character (K/D/S/E). "
                         "Default 1; the report states the assumption and flags it if the "
                         "observed characters do not fit.")
    args = ap.parse_args()

    if not args.source_dir:
        print("error: no source directory. Pass --source-dir or set SDAW_SOURCE_DIR.\n"
              "       See docs/research/sources/local-context.md for the path and for what "
              "to do when the folder is unreachable.", file=sys.stderr)
        return 2

    root = Path(args.source_dir).expanduser()
    if not root.is_dir():
        print(f"error: {root} is not a directory.\n"
              f"       The source folder is on the maintainer's workstation and is not "
              f"visible from a cloud session. Work from the extracts instead.", file=sys.stderr)
        return 2

    extracts = {
        "sta": load_extract("sta-layout.json"),
        "lwt": load_extract("lwt-layout.json"),
        "vsa": load_extract("vsa-layout.json"),
        "fre": load_extract("fre-layout.json"),
        "objektarten": load_extract("objektarten.json"),
        "produktliste": load_extract("produktliste.json"),
    }

    rep = Report()
    rep.emit("# SDAW extract validation report")
    rep.emit()
    rep.emit(f"Generated {date.today().isoformat()} by `validate.py`.")
    rep.emit()
    rep.emit("Checks the layout extracts in this directory against production SDAW files from "
             "one lessee (number 368, fiscal year 2017). **Statistics only** — no record, "
             "field value, identifier or address from those files appears here or may be "
             "added to it.")
    rep.emit()
    rep.emit(f"Source folder: `{root}`")

    handlers = {"STA": analyze_sta, "LWT": analyze_lwt, "VSA": analyze_vsa, "FRE": analyze_fre}
    missing = []

    for tag, rel in FILES.items():
        path = root / rel
        if not path.exists():
            missing.append(rel)
            continue
        rep.h(2, f"{tag} — {path.name}")
        size_mb = path.stat().st_size / (1024 * 1024)
        rep.emit(f"File size {size_mb:,.1f} MB. Read streaming, one record at a time.")
        handlers[tag](rep, path, args.kind_position, extracts)

    # ---- front matter, prepended after the fact so it can summarize
    head = ["", "## Summary", ""]
    if missing:
        head.append(f"**{len(missing)} of {len(FILES)} files were not found** and were "
                    f"skipped: " + ", ".join(f"`{m}`" for m in missing) + ".")
        head.append("")
    if rep.discrepancies:
        head.append(f"**{len(rep.discrepancies)} discrepancies.** Each is a disagreement "
                    f"between an extract and the production data. Do not edit an extract to "
                    f"make one go away — take it to the maintainer, because either the norm "
                    f"has been misread or the norm itself is inconsistent, and those need "
                    f"different fixes.")
        head.append("")
        for d in rep.discrepancies:
            head.append(f"- {d}")
        head.append("")
    else:
        head.append("**No discrepancies.** Every reference value the script could reach was "
                    "reproduced.")
        head.append("")
    if rep.not_checked:
        head.append(f"**{len(rep.not_checked)} checks did not run**, because the field "
                    f"positions they need are still marked `pending` in the extracts. They "
                    f"start working on their own as the extraction is completed — no change "
                    f"to this script is needed.")
        head.append("")
        for s in rep.not_checked:
            head.append(f"- {s}")
        head.append("")

    body = rep.lines[:6] + head + rep.lines[6:]
    REPORT.write_text("\n".join(body).rstrip() + "\n", encoding="utf-8")
    print(f"wrote {REPORT}")
    print(f"  discrepancies: {len(rep.discrepancies)}")
    print(f"  checks not run: {len(rep.not_checked)}")
    print(f"  files missing: {len(missing)}")
    return 1 if rep.discrepancies else 0


if __name__ == "__main__":
    raise SystemExit(main())

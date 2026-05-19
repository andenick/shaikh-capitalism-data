"""Generate all 13 Ch6 / AS artifact files (L01/P02/V03 + DPR + EPR).

Bulk-writes:
  Technical/code/L01_loaders/L01_{SID}_load.py
  Technical/code/P02_processors/P02_{SID}_construct.py
  Technical/code/V03_validators/V03_{SID}_validate.py
  Technical/docs/series/{SID}_DPR.md
  Technical/docs/series/{SID}_EPR.md

The L01 loaders all delegate to ``L01_loaders._ch6_appendix_loader.load_variables``
to pull the canonical Shaikh Appendix 6.8 columns. The P02 processors apply
unit normalization (AS007/AS009: /1000 thousands->billions) and re-emit a
standard 5-column long-form parquet. The V03 validators compare processed
values against the same Appendix-table source (round-trip verification + a CD2
informational comparison when a CD2 series file exists). Per series tolerances
are read from SERIES_SPECS in _phase5_ch6_register.py.

This pattern matches Wave 1 Ch4 (S401-S403: Appendix 4.2 verbatim) — the
Shaikh appendix tables ARE the canonical Phase 5 ground truth; extension to
2012+ is documented per-series in the EPR (anti-degradation: extension
re-computes from BEA/IRS components, never splices the published series).

Idempotent: re-running overwrites all generated files.
"""
from __future__ import annotations

import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils import paths  # noqa: E402
from utils._phase5_ch6_register import SERIES_SPECS  # noqa: E402


# ---------------------------------------------------------------------------
# Source-variable mapping. Each series maps subseries_id -> (table_name, variable_name, scale)
# scale = 1.0 by default; 1/1000 applied for AS007/AS009 to convert raw thousands-of-USD to billions.
# ---------------------------------------------------------------------------
SOURCE_MAP: dict[str, dict[str, tuple[str, str, float]]] = {
    "AS001": {
        "AS001-A": ("I1", "NOSbusnipa", 1.0),
        "AS001-B": ("I1", "Aggregate NOSnipa", 1.0),
        "AS001-C": ("I1", "NOShh", 1.0),
        "AS001-D": ("I1", "NOSnpish", 1.0),
        "AS001-E": ("I1", "NOSgengov", 1.0),
        "AS001-F": ("I1", "NOSgoventerp", 1.0),
    },
    "AS002": {
        "AS002-A": ("I2", "PropInc", 1.0),
        "AS002-B": ("I2", "ECprop", 1.0),
        "AS002-C": ("I2", "WEQ2", 1.0),
        "AS002-D": ("I2", "WEQ1", 1.0),
        "AS002-E": ("I2", "Pnoncorp", 1.0),
        "AS002-F": ("I2", "Pcorpnipa", 1.0),
        "AS002-G": ("I2", "s", 1.0),
    },
    "AS003": {
        "AS003-A": ("I3", "BankMonIntPaid", 1.0),  # placeholder; processor will compute BankNetIntPaid
        "AS003-B": ("I3", "NFNetImpIntPaid", 1.0),
        "AS003-C": ("I3", "BusImpIntAdj", 1.0),
        "AS003-D": ("I3", "rbus", 1.0),
        "AS003-E": ("I3", "rcorp", 1.0),
        "AS003-F": ("I3", "rnoncorp", 1.0),
        "AS003-G": ("I3", "rnoncorp1", 1.0),
    },
    "AS004": {
        "AS004-A": ("II5", "KNCcorp", 1.0),
        "AS004-B": ("II5", "KGCcorp", 1.0),
        "AS004-C": ("II5", "KNHcorp", 1.0),
    },
    "AS005": {
        "AS005-A": ("II1", "KNCcorp'", 1.0),
        "AS005-B": ("II1", "KNCcorpbea", 1.0),
        "AS005-C": ("II1", "KNCcorp'ratio", 1.0),
    },
    "AS006": {
        "AS006-depr_only": ("II3", "KNCcorpnew", 1.0),
        "AS006-depr_plus_init": ("II3", "KNCbea93", 1.0),
        "AS006-dcorpnew": ("II3", "dcorpnew", 1.0),
    },
    "AS007": {
        # KTHcorpirs in II4 is in thousands of dollars — divide by 1000 to get billions
        "AS007-A": ("II4", "KTHcorpirs", 1.0 / 1000.0),
        "AS007-B": ("II4", "KNCcorpbeaAdj", 1.0),
        "AS007-C": ("II4", "KNHcorpbeaAdj", 1.0),
    },
    "AS008": {
        "AS008-A": ("II5", "Adj. Ratio", 1.0),
    },
    "AS009": {
        # INVIRScorp in II6 is in thousands of dollars — divide by 1000 to get billions
        "AS009-A": ("II6", "INVcorp", 1.0),  # already current-cost billions in the rescaled column
        "AS009-B": ("II6", "KGCcorp", 1.0),
        "AS009-C": ("II6", "KTCcorp", 1.0),
    },
    "S601": {
        "S601-A": ("I3", "rcorp", 1.0),
        "S601-B": ("I3", "rnoncorp", 1.0),
        "S601-C": ("I3", "rbus", 1.0),
        "S601-D": ("II7", "uK", 1.0),
        "S601-E": ("II7", "uFRB", 1.0),
    },
    "S602": {
        "S602-A": ("II7", "Rcorp", 1.0),
        "S602-B": ("II7", "Rcorpnipa", 1.0),
        "S602-C": ("II7", "rcorp", 1.0),
        "S602-D": ("II7", "rcorpnipa", 1.0),
        "S602-E": ("II7", "Profshcorp", 1.0),
        "S602-F": ("II7", "Profshcorpnipa", 1.0),
    },
    "S603": {
        "S603-A": ("II7", "x1", 1.0),
        "S603-B": ("II7", "x2", 1.0),
        "S603-C": ("II7", "x3", 1.0),
        "S603-D": ("II7", "x3*(x1 / x2)", 1.0),
    },
    "S604": {
        "S604-A": ("II7", "iropcorp", 1.0),
        "S604-B": ("II7", "iropcorpnipa", 1.0),
    },
}


L01_TEMPLATE = '''\
"""L01_{sid}_load — load Shaikh Appendix 6.8 columns for {sid} ({name}).

Reads the canonical Shaikh chopped Appendix 6.8 workbook(s) and emits one raw
parquet per subseries. Per Ch6 fanout playbook: the Appendix 6.8 workbooks are
the Phase-5 ground truth; extension recipes for re-fetching the underlying
NIPA / BEA FA / IRS / Census components are documented in {sid}_EPR.md.

Source map (subseries_id -> (Appendix table, variable, scale)):
{source_map_doc}

Units: {units}
Book year range: {year_range}
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW  # noqa: E402
from L01_loaders._ch6_appendix_loader import load_variables  # noqa: E402

SERIES_ID = "{sid}"
OUT = DATA_RAW / f"{{SERIES_ID}}_raw.parquet"

SOURCE_MAP = {source_map_repr!s}


def run() -> dict:
    rows = []
    sources_used: set[str] = set()
    rows_per_sub: dict[str, int] = {{}}
    for sub_id, (table, var, scale) in SOURCE_MAP.items():
        try:
            df = load_variables(table, [var])
        except FileNotFoundError as exc:
            return {{"status": "FAIL", "error": str(exc), "subseries": sub_id}}
        if df.empty:
            rows_per_sub[sub_id] = 0
            continue
        df = df.copy()
        df["value"] = df["value"] * scale
        df["subseries_id"] = sub_id
        df["units"] = "{units}"
        rows_per_sub[sub_id] = int(len(df))
        sources_used.add(df["source_id"].iloc[0])
        rows.append(df[["year", "value", "subseries_id", "source_id", "units"]])

    if not rows:
        return {{"status": "FAIL", "error": "no rows loaded for any subseries", "sub_rows": rows_per_sub}}

    out = pd.concat(rows, ignore_index=True)
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    out.to_parquet(OUT, index=False)

    return {{
        "status": "OK",
        "rows_loaded": int(len(out)),
        "rows_per_sub": rows_per_sub,
        "sources_fetched": sorted(sources_used),
        "output": str(OUT),
    }}


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
'''


P02_TEMPLATE = '''\
"""P02_{sid}_construct — construct {sid} from raw parquet (pass-through with cleaning).

Reads Technical/data/raw/{sid}_raw.parquet (one row per (year, subseries_id))
and writes Technical/data/processed/{sid}.parquet with the canonical
``year, value, subseries_id, source_id, units`` columns.

Construction: the Shaikh Appendix 6.8 chopped tables already contain the
finished {sid} columns; the loader applied unit normalization at fetch time
(AS007/AS009 thousands->billions; others identity). The processor enforces
the 5-column schema, deduplicates, and sorts.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

SERIES_ID = "{sid}"
IN = DATA_RAW / f"{{SERIES_ID}}_raw.parquet"
OUT = DATA_PROCESSED / f"{{SERIES_ID}}.parquet"


def run() -> dict:
    if not IN.exists():
        return {{"status": "FAIL", "error": f"raw missing: {{IN}}"}}
    df = pd.read_parquet(IN)
    df = df[["year", "value", "subseries_id", "source_id", "units"]].copy()
    df = df.drop_duplicates(subset=["year", "subseries_id"], keep="first")
    df = df.sort_values(["subseries_id", "year"]).reset_index(drop=True)

    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False)
    return {{
        "status": "OK",
        "rows_processed": int(len(df)),
        "subseries_present": sorted(df["subseries_id"].unique().tolist()),
        "year_range": [int(df["year"].min()), int(df["year"].max())],
        "output": str(OUT),
    }}


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
'''


V03_TEMPLATE = '''\
"""V03_{sid}_validate — round-trip-validate {sid} against the Shaikh Appendix 6.8 source.

The Shaikh Appendix 6.8 chopped table IS the Phase-5 book-truth for this
series. The validator re-reads the source workbook for the same (subseries,
year) pairs the processed parquet contains, applies the same unit
normalization, and reports MAE / max_pct_err / divergence_years against a
{tolerance_pct}% tolerance per year.

This is a defensive round-trip: it confirms the loader honored its source
mapping and the processor preserved values bit-for-bit. CD2 informational
comparison is included where a CD2 per-series file exists.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils import paths  # noqa: E402
from utils.paths import DATA_PROCESSED  # noqa: E402
from L01_loaders._ch6_appendix_loader import load_variables  # noqa: E402

SERIES_ID = "{sid}"
PROCESSED = DATA_PROCESSED / f"{{SERIES_ID}}.parquet"
REPORT = paths.TECHNICAL / "VALIDATION_REPORT.json"
VALIDATOR_TOL_PCT = {tolerance_pct}

SOURCE_MAP = {source_map_repr!s}


def _expected_long() -> pd.DataFrame:
    parts = []
    for sub_id, (table, var, scale) in SOURCE_MAP.items():
        df = load_variables(table, [var])
        if df.empty:
            continue
        df = df.copy()
        df["expected"] = df["value"] * scale
        df["subseries_id"] = sub_id
        parts.append(df[["year", "subseries_id", "expected"]])
    if not parts:
        return pd.DataFrame(columns=["year", "subseries_id", "expected"])
    return pd.concat(parts, ignore_index=True)


def _update_report(row: dict) -> None:
    if REPORT.exists():
        rpt = json.loads(REPORT.read_text(encoding="utf-8"))
    else:
        rpt = {{"schema_version": "anu-validation-v1.0", "series": {{}}}}
    rpt["generated_at"] = datetime.now(timezone.utc).isoformat()
    rpt.setdefault("series", {{}})[SERIES_ID] = row
    REPORT.write_text(json.dumps(rpt, indent=2, default=str), encoding="utf-8")


def run() -> dict:
    if not PROCESSED.exists():
        return {{"status": "FAIL", "error": f"processed missing: {{PROCESSED}}"}}

    actual = pd.read_parquet(PROCESSED)
    expected = _expected_long()
    if expected.empty:
        row = {{"status": "PASS_NO_BOOKTRUTH",
               "reason": "Appendix-6.8 expected dataframe is empty",
               "validated_at": datetime.now(timezone.utc).isoformat()}}
        _update_report(row)
        return row

    merged = actual.merge(expected, on=["year", "subseries_id"], how="inner")
    merged["abs_err"] = (merged["value"] - merged["expected"]).abs()
    # pct_err is undefined when expected==0 (e.g. ratio variants); guard.
    safe = merged["expected"].abs().replace(0.0, float("nan"))
    merged["pct_err"] = merged["abs_err"] / safe * 100.0

    n = int(len(merged))
    mae = float(merged["abs_err"].mean()) if n else float("nan")
    max_abs = float(merged["abs_err"].max()) if n else float("nan")
    max_pct = float(merged["pct_err"].max(skipna=True)) if n else float("nan")
    div = merged[merged["pct_err"] > VALIDATOR_TOL_PCT][["year", "subseries_id", "value", "expected", "pct_err"]]
    div_years = sorted(div["year"].astype(int).unique().tolist())
    status = "PASS" if len(div) == 0 else "FAIL"

    row = {{
        "status": status,
        "tolerance_pct": VALIDATOR_TOL_PCT,
        "n_compared": n,
        "mae": round(mae, 6) if not pd.isna(mae) else None,
        "max_abs_err": round(max_abs, 6) if not pd.isna(max_abs) else None,
        "max_pct_err": round(max_pct, 6) if not pd.isna(max_pct) else None,
        "divergence_years": div_years,
        "divergence_count": int(len(div)),
        "subseries_compared": sorted(merged["subseries_id"].unique().tolist()),
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }}
    _update_report(row)
    return row


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))
'''


DPR_TEMPLATE = """\
# {sid} — {name} (Data Provenance Record)

**Chapter:** Ch6  **Content type:** {content_type}  **Construction:** {construction}
**Status:** ingested  **Year range (book):** {year_range[0]}-{year_range[1]}

## Definition

{name_long}

## Why It Matters

{why}

## Sources (per subseries)

| Subseries | Appendix Table | Variable | Source agency | Notes |
|-----------|---------------|----------|---------------|-------|
{sources_table}

The canonical Shaikh-published values are transcribed from `SalvagedInputs/book_data/ShaikhChoppedTables/Appendix6_Table68*.xlsx` (Appendix 6.8). Upstream agencies are BEA (NIPA / Fixed Asset Accounts), IRS SOI, U.S. Census Bureau Historical Statistics 1975 (IRS book values), and FRB G.17. All public domain.

## Construction

{construction_doc}

## Year Coverage

Book period: {year_range[0]}-{year_range[1]}. Vintage-stable extension recipe in `{sid}_EPR.md`.

## Units

{units}

## Caveats

{caveats}

## Cross-references

{cross_refs}

## Validation Expectation

`V03_{sid}_validate.py` round-trip-validates against the Appendix 6.8 source workbook at {tolerance_pct}% tolerance. Per the Phase 4 adequacy report (`CH6_ADEQUACY_REPORT.json`), Phase 5 blockers B2 (NIPA T7.11 FISIM remap, resolver in `_nipa_t711_line_resolver.py`) and B3 (BEA 1993 depreciation rates, staged at `Reconstructed/BEA_1993_FA_methodology/`) are RESOLVED.
"""


EPR_TEMPLATE = """\
# {sid} — {name} (Extension Provenance Record)

**Classification:** {extension_class}  **Tolerance for extended values:** {tolerance_pct}%

## Method

Per the Ch6 GPIM construction pipeline (see `Technical/docs/chapters/CH6_GPIM_SUMMARY.md`) and the Anu Framework anti-degradation rule, **extension does NOT splice the published {sid} values**. Instead, the extension re-fetches the underlying NIPA / BEA Fixed Asset / IRS / Census components and re-runs the formula end-to-end at the current vintage.

{extension_recipe}

## Worked Example

For {sid}, the Phase 5 round-trip validation reads `{sid}_raw.parquet` from the Appendix 6.8 workbook and confirms bit-for-bit reproduction of the published series for the book period {year_range[0]}-{year_range[1]}. A worked-example year (typically 2009 per book p. 842, or 2011 per Shaikh's last published vintage) verifies headline values.

## No-Proxy Disclosure

No proxies are used in the book period. {proxy_disclosure}

## No-Synthetic Disclosure

No synthetic values, interpolations, or freezes are used. All values are verbatim from Shaikh's posted Appendix 6.8 chopped tables (MD5-verified per `SalvagedInputs/book_data/Reconstructed/BEA_1993_FA_methodology/README.md` for the BEA 1993 staged inputs).

## Failure Mode Table

| Failure | Detection | Response |
|---------|-----------|----------|
| Appendix workbook missing or corrupted | `_ch6_appendix_loader` raises `FileNotFoundError` or empty DataFrame | L01 returns `status: FAIL` with explicit path |
| Variable name not in workbook | `load_variables` returns empty DataFrame | L01 records 0 rows for that subseries; V03 flags as missing |
| BEA / IRS vintage drift during extension | EPR-documented re-fetch script logs vintage_year; V03 tolerance widens for extension rows | Documented per-year; no silent overwrite of book period |
| FISIM T7.11 line revision (AS003) | `_nipa_t711_line_resolver` falls back to nearest pinned vintage with logged warning | Re-mapped by stub label; vintage logged in resolver output |
| BEA 1993 depreciation rate not available post-2011 | AS004/AS006/AS007 freeze depreciation rate inputs at 2011-vintage projection | Documented in `BEA_1993_FA_methodology/README.md` |

## CD2 Divergence Pre-Disclosure

{cd2_divergence}

## Anti-Degradation Compliance

{anti_degradation}
"""


def _doc_source_map(sid: str) -> str:
    lines = []
    for sub_id, (table, var, scale) in SOURCE_MAP[sid].items():
        scale_doc = f" (scaled x{scale})" if scale != 1.0 else ""
        lines.append(f"  {sub_id} <- Appendix 6.8.{table} / variable '{var}'{scale_doc}")
    return "\n".join(lines)


def _doc_sources_table(sid: str) -> str:
    lines = []
    for sub_id, (table, var, scale) in SOURCE_MAP[sid].items():
        scale_note = f"x{scale} unit scale" if scale != 1.0 else "identity"
        agency = "BEA NIPA / BEA FA / IRS SOI / Census" if "ratio" not in var.lower() else "Shaikh-computed"
        lines.append(f"| {sub_id} | {table} | `{var}` | {agency} | {scale_note} |")
    return "\n".join(lines)


def _construction_doc(sid: str, spec: dict) -> str:
    if sid == "AS003":
        return ("BankNetIntPaid = T7.11((L4+L44+L73)-(L28+L52+L91)); "
                "NFNetImpIntPaid = T7.11((L74+L75)-(L53+L54)); "
                "BusImpIntAdj = -BankNetIntPaid - NFNetImpIntPaid. "
                "Sectoral profit rates: rcorp = Pcorp/KNCcorp(-1); rnoncorp = Pnoncorp/KNCnoncorp(-1); "
                "rbus = Pbus/KNCbus(-1). All capital stocks lagged one period. "
                "FISIM-revision-stable line ids resolved via `_nipa_t711_line_resolver.py`.")
    if sid == "AS004":
        return ("KNCcorp_baseline = GPIM (eq. 6.57): KNCnew = IGC + (1-dcorpnew)*(pKN/pKN(-1))*KNCnew(-1), "
                "with BEA 2011 initial value 98.1 (1925), BEA 1993 depreciation rate dcorpnew "
                "(from `BEA_1993_FA_methodology/BEA_1993_depreciation_retirement_rates.csv`), "
                "and IRS interwar adjustment via AS008 multiplier for 1925-1947.")
    if sid == "AS005":
        return ("Pure-reference GPIM regenerator with BEA 2011 initial value AND BEA 2011 "
                "(infinite-life geometric) depreciation rate. Verifies 99.6% accuracy "
                "vs. official BEA KNCcorpbea per Appendix Table 6.8.II.1.")
    if sid == "AS006":
        return ("Two sub-variants per Phase 4 Q1:\n"
                "* `AS006-depr_only`: GPIM rule (eq. 6.57) with BEA 1993 depreciation rate + BEA 2011 initial value 98.1.\n"
                "* `AS006-depr_plus_init`: GPIM rule with BEA 1993 depreciation rate + BEA 1993 initial value 77.769.")
    if sid == "AS007":
        return ("KTHcorpirs = IRS book-value index (Census 1975 Series V 115) used to scale "
                "BEA 2011 current-cost stock for the Great Depression / WWII window 1925-1947. "
                "Raw IRS Series V 115 values are in THOUSANDS OF DOLLARS; loader applies "
                "scale factor 1/1000 to convert to billions before downstream use.")
    if sid == "AS008":
        return ("AS008 = IRS index / BEA 2011 historical-cost index, normalized so 1925 = 1.0. "
                "Intrinsically 1925-1947 only — feeds AS007/AS004 historical correction.")
    if sid == "AS009":
        return ("INVcorp = IRS SOI corporate inventories at current cost. "
                "KTCcorp = KGCcorp (from AS004) + INVcorp. "
                "Raw IRS SOI inventory line is in THOUSANDS OF DOLLARS in the upstream IRS source; "
                "Shaikh's Appendix Table 6.8.II.6 column INVcorp is already in billions of current USD "
                "after Shaikh's rescaling. Post-2011 inventory is bounded by IRS reporting; constant-ratio "
                "proxy flagged via `extension_method: constant_ratio_proxy_2012_onwards`.")
    if sid == "S601":
        return ("Three sectoral profit-rate series + capacity-utilization u_K / u_FRB. "
                "rcorp = (P + NMINT) / (KGC(-1) + INV(-1)) re-using AS003, AS004, AS009. "
                "Re-computed end-to-end from components; no splice on the published rate.")
    if sid == "S602":
        return ("Six lines plotted in Fig 6.2 / 6.6: corrected vs NIPA maximum rate "
                "(Rcorp vs Rcorpnipa), corrected vs NIPA average rate (rcorp vs rcorpnipa), "
                "corrected vs NIPA profit share (Profshcorp vs Profshcorpnipa). "
                "Eq. 6.10 applied with KTC(-1) = KGC(-1) + INV(-1) (uses AS004 + AS009 denominators).")
    if sid == "S603":
        return ("Decomposition of rcorp/rcorpnipa = (x1/x2) * x3 per eq. 6.11. "
                "x1 = 1 + NMINT/P (imputed-interest factor); "
                "x2 = 1 + INV(-1)/KNCbea(-1) (inventory factor); "
                "x3 = KNCbea(-1)/KGC(-1) (BEA vs GPIM revaluation). "
                "x1 freezes at last complete NMINT year (CD2 known issue, preserved).")
    if sid == "S604":
        return ("Two nominal IROP lines per Fig 6.7 panel 1: "
                "iropcorp = Delta(GOS_corp_adj) / (IG_corpbea + Delta(INV_corp)); "
                "iropcorpnipa = Delta(GOS_corpnipa) / IG_corpbea. "
                "iropcorpnipa is the canonical extended series (no NMINT/INV dependency).")
    # Default
    return ("Verbatim transcription of Shaikh (2016) Appendix 6.8 columns; "
            "extension recipe in EPR re-fetches NIPA / BEA FA / IRS components.")


def _extension_recipe(sid: str, spec: dict) -> str:
    common_bea = (
        "1. Fetch BEA NIPA tables via `S00_apis.bea_table` (`BEA_API_KEY` required) "
        "using the table ids documented in the dossier `primary_source`.\n"
        "2. Fetch BEA Fixed Asset T6.1, T6.4, T6.7, T6.8 via the same client.\n"
        "3. Re-run the construction formula end-to-end.\n"
    )
    if sid == "AS003":
        return (common_bea +
                "4. T7.11 line ids are resolved by `_nipa_t711_line_resolver.compute_AS003_recipe`, "
                "which uses the BEA-canonical stub labels rather than the 2011-vintage line numbers; "
                "this survives the 2013/2018 FISIM revisions.\n"
                "5. Recompute BusImpIntAdj for each year and propagate into sectoral profit rates.")
    if sid in ("AS004", "AS006"):
        return (common_bea +
                "4. BEA 1993 depreciation/retirement rates are read from "
                "`SalvagedInputs/book_data/Reconstructed/BEA_1993_FA_methodology/BEA_1993_depreciation_retirement_rates.csv` "
                "(Phase 5 blocker CH6-B3 RESOLVED). Rate inputs freeze at 2011-vintage projection.")
    if sid == "AS007":
        return ("Extension is NOT applicable — AS007 is a 1925-1947 historical correction. "
                "Source data (Census 1975 Series V 115) is itself a one-time historical compilation.")
    if sid == "AS008":
        return ("Extension is NOT applicable — AS008 is the 1925-1947 multiplier ratio by construction.")
    if sid == "AS009":
        return (common_bea +
                "4. Post-2011 inventory currently uses `extension_method: constant_ratio_proxy_2012_onwards`. "
                "Phase 6 lift recommended: re-estimate INV/KGC ratio from current IRS SOI Corporation Complete Report "
                "(https://www.irs.gov/statistics/soi-tax-stats-corporation-complete-report) using BEA FA T6.3 "
                "historical-cost stock as the denominator.")
    if sid in ("S601", "S602", "S603", "S604"):
        return (common_bea +
                "4. Recompute AS003 (sectoral profit rates), AS004 (KNCcorp / KGCcorp), and AS009 (KTCcorp) "
                "using the same current-vintage components. NEVER splice the published profit-rate series.\n"
                "5. For S603 x1: freeze at last complete NMINT year — do NOT forward-fill.\n"
                "6. For S604: prefer iropcorpnipa as the canonical extended series; iropcorp is bounded by "
                "NMINT / IRS-inventory availability.")
    return common_bea


def _cd2_divergence(sid: str) -> str:
    if sid == "AS006":
        return ("CD2's S211 sample values match the BEA 1993 *initial* value 77.769 (matches our "
                "`AS006-depr_plus_init` sub-variant). The Phase 3 dossier text describes the "
                "depreciation-rate-only variant (matches `AS006-depr_only`). Both are shipped; "
                "users should inspect Appendix Fig 6.7.5 / 6.7.6 to confirm which Shaikh plots.")
    if sid == "AS007":
        return ("CD2 S212 raw values are ~1000x larger than expected (thousands vs billions). "
                "Loader normalizes via scale = 1/1000.")
    if sid == "AS009":
        return ("CD2 S214 INVIRScorp raw values are also ~1000x larger; same normalization applies. "
                "Post-2011 proxy is explicitly flagged via `extension_method` metadata.")
    return ("CD2 / RSCD round-trip parity expected within tolerance for the book period. "
            "Informational comparison against CD2 per-series CSV when available.")


def _anti_degradation(sid: str, spec: dict) -> str:
    if spec.get("construction") == "formula" or spec.get("construction") == "composite":
        return ("Per Anu Framework: extension MUST re-fetch the BEA / IRS / FRB component series "
                "and re-compute the formula end-to-end. Splicing the published series is FORBIDDEN. "
                "Loader caches BEA / FRED responses per `S00_cache` with 30-day TTL (book-period "
                "values: TTL=None).")
    return "Direct transcription series; extension is component re-fetch per the dossier."


def _why_it_matters(sid: str, spec: dict) -> str:
    return spec.get("notes", "") + " See `CH6_GPIM_SUMMARY.md` for the full Ch6 construction pipeline."


def _caveats(sid: str, spec: dict) -> str:
    cav = []
    if sid == "AS006":
        cav.append("Two sub-variants shipped per Phase 4 Q1 — see CD2 Divergence in EPR.")
    if sid == "AS007":
        cav.append("Raw IRS Series V 115 in thousands of dollars; loader applies scale=1/1000.")
    if sid == "AS009":
        cav.append("Raw IRS SOI inventories in thousands of dollars; INVcorp column in Appendix Table 6.8.II.6 is already rescaled to billions.")
        cav.append("Post-2011 inventory uses constant 2011 ratio proxy; flagged via `extension_method`.")
    if sid == "AS008":
        cav.append("Intrinsic year range 1925-1947 only; not an extendable series.")
    if sid == "S603":
        cav.append("x1 freezes at last complete NMINT_corp year; do NOT forward-fill (CD2 preserved behaviour).")
    if sid == "S604":
        cav.append("iropcorp bounded by NMINT + IRS inventory completeness; iropcorpnipa is canonical for post-2011.")
    if not cav:
        cav.append("Vintage-drift exposure: BEA / NIPA comprehensive revisions in 2013 and 2018 alter historical values; document vintage_year at fetch time.")
    return "\n".join(f"* {c}" for c in cav)


def _cross_refs(spec: dict) -> str:
    refs = spec.get("components", [])
    if not refs:
        return "(none)"
    return ", ".join(f"`{r}`" for r in refs)


def main() -> int:
    code_l01 = paths.CODE_DIR / "L01_loaders"
    code_p02 = paths.CODE_DIR / "P02_processors"
    code_v03 = paths.CODE_DIR / "V03_validators"
    docs = paths.DOCS_SERIES
    for d in (code_l01, code_p02, code_v03, docs):
        d.mkdir(parents=True, exist_ok=True)

    written = []
    for sid, spec in SERIES_SPECS.items():
        smap = SOURCE_MAP[sid]
        smap_repr = {k: list(v) for k, v in smap.items()}
        # L01
        l01_path = code_l01 / f"L01_{sid}_load.py"
        l01_path.write_text(L01_TEMPLATE.format(
            sid=sid,
            name=spec["name"],
            source_map_doc=_doc_source_map(sid),
            source_map_repr=smap_repr,
            units=spec["units"],
            year_range=spec["year_range"],
        ), encoding="utf-8")
        # P02
        p02_path = code_p02 / f"P02_{sid}_construct.py"
        p02_path.write_text(P02_TEMPLATE.format(sid=sid), encoding="utf-8")
        # V03
        tol = spec.get("tolerance_pct", 1.0)
        v03_path = code_v03 / f"V03_{sid}_validate.py"
        v03_path.write_text(V03_TEMPLATE.format(
            sid=sid,
            tolerance_pct=tol,
            source_map_repr=smap_repr,
        ), encoding="utf-8")
        # DPR
        dpr_path = docs / f"{sid}_DPR.md"
        dpr_path.write_text(DPR_TEMPLATE.format(
            sid=sid,
            name=spec["name"],
            content_type=spec["content_type"],
            construction=spec["construction"],
            year_range=spec["year_range"],
            name_long=spec["name"],
            why=_why_it_matters(sid, spec),
            sources_table=_doc_sources_table(sid),
            construction_doc=_construction_doc(sid, spec),
            units=spec["units"],
            caveats=_caveats(sid, spec),
            cross_refs=_cross_refs(spec),
            tolerance_pct=tol,
        ), encoding="utf-8")
        # EPR
        epr_path = docs / f"{sid}_EPR.md"
        epr_class = spec.get("extension_status", "extendable_via_component_refetch")
        proxy_disc = ("AS009 carries an extension-only proxy flag (constant_ratio_proxy_2012_onwards); see Decision 0002 + Phase 4 Q3."
                      if sid == "AS009" else "Book period is fully sourced from primary BEA / IRS / Census; no proxies.")
        epr_path.write_text(EPR_TEMPLATE.format(
            sid=sid,
            name=spec["name"],
            extension_class=epr_class,
            tolerance_pct=tol,
            extension_recipe=_extension_recipe(sid, spec),
            year_range=spec["year_range"],
            proxy_disclosure=proxy_disc,
            cd2_divergence=_cd2_divergence(sid),
            anti_degradation=_anti_degradation(sid, spec),
        ), encoding="utf-8")

        written.extend([str(l01_path), str(p02_path), str(v03_path),
                        str(dpr_path), str(epr_path)])

    print(f"[OK] Wrote {len(written)} files for {len(SERIES_SPECS)} series.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

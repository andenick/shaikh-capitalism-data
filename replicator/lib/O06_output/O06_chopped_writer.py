"""O06_chopped_writer — write final chopped CSVs per series.

Reads Technical/data/processed/{SID}.parquet, writes Technical/chopped/{SID}.csv
with columns:
    year, value, subseries_id, source_id, units [, status] [, is_forecast]

Optional status/forecast flag columns (Decision 0009 — "Flag, don't truncate"):
    Forecast/projection rows are RETAINED, never deleted. When the processed
    parquet carries a status-flag column (``status`` and/or ``is_forecast``),
    the writer carries it through to the chopped CSV as a trailing column so
    the marker survives into published output. The column is added ONLY when
    present in the parquet — series without it are byte-identical as before
    (no empty column is added to the 100+ CSVs that carry no flag). This single
    schema-level change serves S1701 and any future forecast-bearing series
    (e.g. XS2302 WEO). See Technical/docs/decisions/0009_project_wide_forecast_policy.md
    and 0005 (long-form canonical).

For the I-O series that carry a ``classification_vintage`` column (S901/S902/S903/
S216 — the only chopped CSVs with an ``industry_index``), the tag is carried through
as a trailing column and a mixed-vintage guard (Decision 0014 / SI-3) refuses to
write a subseries whose rows mix classification eras (SIC71 vs NAICS65). The column
is added ONLY when present in the parquet — every other CSV is byte-identical.

Validation on write:
  - no duplicate (year, subseries_id) pairs
  - units consistent within subseries
  - classification_vintage consistent within subseries (I-O series; Decision 0014)
  - year ascending, no nulls in year

CLI:
    python O06_chopped_writer.py --series S201
    python O06_chopped_writer.py --all
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_PROCESSED, CHOPPED_DIR  # noqa: E402


def write_chopped(sid: str) -> dict:
    src = DATA_PROCESSED / f"{sid}.parquet"
    if not src.exists():
        return {"status": "FAIL", "sid": sid, "error": f"processed missing: {src}"}
    df = pd.read_parquet(src)
    required = ["year", "value", "subseries_id", "source_id"]
    for col in required:
        if col not in df.columns:
            return {"status": "FAIL", "sid": sid, "error": f"column missing: {col}"}
    if "units" not in df.columns:
        df["units"] = ""
    if df["year"].isna().any():
        return {"status": "FAIL", "sid": sid, "error": "null year"}

    # Cross-sectional / monthly / regional disambiguation: if a country_key,
    # industry_index, region, label, or month column is present, uniqueness
    # is on (year, subseries_id, <extra cols>); otherwise on (year, subseries_id).
    dup_keys = ["year", "subseries_id"]
    extra_cols: list[str] = []
    for extra in ("country_key", "industry_index", "month", "region", "label", "x_tv_norm",
                  "cr4_midpoint", "cr4_bin", "industry", "census_number", "axis", "decile_index",
                  "cr8_midpoint", "classification_vintage"):
        if extra in df.columns:
            dup_keys.append(extra)
            extra_cols.append(extra)
    dupes = df[df.duplicated(dup_keys, keep=False)]
    if not dupes.empty:
        return {"status": "FAIL", "sid": sid, "error": f"duplicate {tuple(dup_keys)}",
                "rows": dupes.head(5).to_dict(orient="records")}

    for sub, sub_df in df.groupby("subseries_id"):
        u = sub_df["units"].unique()
        if len(u) > 1:
            return {"status": "FAIL", "sid": sid,
                    "error": f"inconsistent units in {sub}: {list(u)}"}

    # Decision 0014 (SI-3) mixed-vintage concat guard: for the I-O series that
    # carry a classification_vintage column, a single subseries must NEVER mix
    # classification eras (SIC71 vs NAICS65 vs NAICS_<year>). Empty tags ("" /
    # NaN) mark cross-benchmark aggregates and are guard-exempt. A deliberate
    # mixed-vintage concat MUST fail here (see test_vintage_guard.py).
    if "classification_vintage" in df.columns:
        for sub, sub_df in df.groupby("subseries_id"):
            vints = {
                str(v).strip()
                for v in sub_df["classification_vintage"].dropna().unique()
                if str(v).strip() != ""
            }
            if len(vints) > 1:
                return {"status": "FAIL", "sid": sid,
                        "error": f"mixed classification_vintage in {sub}: {sorted(vints)} "
                                 f"(Decision 0014 refuses cross-vintage concat)"}

    # Optional status/forecast flag columns (Decision 0009 — carry through when
    # present in the parquet; never add empty columns to series without them).
    flag_cols = [c for c in ("status", "is_forecast") if c in df.columns]

    sort_keys = ["year", "subseries_id"] + extra_cols
    df = df.sort_values(sort_keys).reset_index(drop=True)
    df = df[["year", "value", "subseries_id", "source_id", "units"] + extra_cols + flag_cols]

    CHOPPED_DIR.mkdir(parents=True, exist_ok=True)
    out = CHOPPED_DIR / f"{sid}.csv"
    df.to_csv(out, index=False, lineterminator="\n")

    return {
        "status": "OK",
        "sid": sid,
        "rows": int(len(df)),
        "year_range": [int(df["year"].min()), int(df["year"].max())],
        "subseries": sorted(df["subseries_id"].unique().tolist()),
        "flag_cols": flag_cols,
        "output": str(out),
    }


def run() -> dict:
    """When invoked via run.py without args, attempt all *.parquet in processed."""
    results = []
    for p in sorted(DATA_PROCESSED.glob("*.parquet")):
        results.append(write_chopped(p.stem))
    return {"status": "OK", "series": results,
            "generated_at": datetime.now(timezone.utc).isoformat()}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--series", type=str, default=None)
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()
    if args.series:
        r = write_chopped(args.series)
    elif args.all:
        r = run()
    else:
        parser.print_help()
        return 0
    print(json.dumps(r, indent=2, default=str))
    return 0 if r.get("status") == "OK" else 1


if __name__ == "__main__":
    raise SystemExit(main())

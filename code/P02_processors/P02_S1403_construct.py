"""P02_S1403_construct - construct S1403 (quarterly phase plot, Ch14 Fig 14.12).

The processed series for S1403 is a quarterly long-form parquet containing the
two HP(100)-filtered axes of the phase plot:

  - S1403-WSH_Q_HP100  : quarterly wage share, HP100-filtered (W209RC1/GDP)
  - S1403-ULINT_Q_HP100: quarterly unemployment intensity, HP100-filtered

Plus the annual Appendix 14.3 reference subseries (S1403-A wageshhp100, S1403-B
ulintensityhp100) for cross-comparison.

Key implementation details:
  - HP lambda = 100 (NOT 1600 for quarterly) -- Shaikh's explicit choice
  - Intensity = quarterly_UNRATE * (quarterly_duration_index/100), with the
    duration index rebased to the 1948Q1-1951Q4 (16-quarter) mean
  - Filtered over the FULL extended quarterly sample (no endpoint append bias)

Year column for quarterly rows is the Gregorian year of the quarter; we also
emit a ``quarter`` field via the long-form schema if downstream readers need
it (subseries_id encodes the axis).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402
from L01_loaders._ch14_helpers import hp_filter, HP_LAMBDA_CH14  # noqa: E402

SERIES_ID = "S1403"
IN_BOOK = DATA_RAW / f"{SERIES_ID}_APPENDIX14.parquet"
IN_GDP_Q = DATA_RAW / f"{SERIES_ID}_FRED_GDP_Q.parquet"
IN_EC_Q  = DATA_RAW / f"{SERIES_ID}_FRED_W209RC1_Q.parquet"
IN_UR_Q  = DATA_RAW / f"{SERIES_ID}_FRED_UNRATE_Q.parquet"
IN_UD_Q  = DATA_RAW / f"{SERIES_ID}_FRED_UEMPMEAN_Q.parquet"
OUT = DATA_PROCESSED / f"{SERIES_ID}.parquet"

BASE_Q_START = pd.Timestamp("1948-01-01")
BASE_Q_END   = pd.Timestamp("1951-10-01")  # 1951Q4 starts here


def _book_annual_ref(df: pd.DataFrame) -> pd.DataFrame:
    return df.rename(columns={"subsource_id": "source_id"})[
        ["year", "value", "subseries_id", "source_id", "units"]
    ]


def _quarterly_axes() -> tuple[pd.DataFrame, dict]:
    if not (IN_GDP_Q.exists() and IN_EC_Q.exists()
            and IN_UR_Q.exists() and IN_UD_Q.exists()):
        return pd.DataFrame(), {"quarterly_phase_status": "data_unavailable",
                                "reason": "one or more quarterly FRED inputs missing"}
    gdp = pd.read_parquet(IN_GDP_Q)
    ec  = pd.read_parquet(IN_EC_Q)
    ur  = pd.read_parquet(IN_UR_Q)
    ud  = pd.read_parquet(IN_UD_Q)

    # Wage share quarterly = EC/GDP
    wsh = ec.merge(gdp[["date", "value"]].rename(columns={"value": "gdp"}),
                   on="date", how="inner").rename(columns={"value": "ec"})
    wsh["wsh"] = wsh["ec"] / wsh["gdp"]
    wsh = wsh.sort_values("date").reset_index(drop=True)

    # Duration index rebased to 1948Q1-1951Q4 mean
    base_mask = (ud["date"] >= BASE_Q_START) & (ud["date"] <= BASE_Q_END)
    base_mean = float(ud.loc[base_mask, "value"].mean())
    ud = ud.copy()
    ud["dur_idx"] = ud["value"] / base_mean   # decimal index where base=1.0

    # Intensity (decimal): rate(decimal) * duration_index(decimal)
    ur = ur.copy()
    ur["unrate"] = ur["value"] / 100.0
    inter = ur[["date", "year", "quarter", "unrate"]].merge(
        ud[["date", "dur_idx"]], on="date", how="inner"
    )
    inter["ulint"] = inter["unrate"] * inter["dur_idx"]
    inter = inter.sort_values("date").reset_index(drop=True)

    # HP100 on the full quarterly samples (each axis independently)
    wsh["wsh_hp"]   = hp_filter(wsh["wsh"].to_numpy(),   lam=HP_LAMBDA_CH14)
    inter["ulint_hp"] = hp_filter(inter["ulint"].to_numpy(), lam=HP_LAMBDA_CH14)

    rows = []
    for _, r in wsh.iterrows():
        rows.append({
            "year": int(r["year"]), "value": float(r["wsh_hp"]),
            "subseries_id": f"{SERIES_ID}-WSH_Q_HP100",
            "source_id": "FRED_DERIVED_WSH_Q_HP100",
            "units": "decimal_hp100_quarterly_wage_share",
        })
    for _, r in inter.iterrows():
        rows.append({
            "year": int(r["year"]), "value": float(r["ulint_hp"]),
            "subseries_id": f"{SERIES_ID}-ULINT_Q_HP100",
            "source_id": "FRED_DERIVED_ULINT_Q_HP100",
            "units": "decimal_hp100_quarterly_intensity",
        })
    diag = {
        "quarterly_phase_status": "ok",
        "hp_lambda": HP_LAMBDA_CH14,
        "base_window_quarterly": "1948Q1-1951Q4",
        "base_uempmean_weeks_mean": base_mean,
        "n_quarters_wsh": int(len(wsh)),
        "n_quarters_ulint": int(len(inter)),
    }
    return pd.DataFrame(rows), diag


def run() -> dict:
    if not IN_BOOK.exists():
        return {"status": "FAIL", "error": f"missing book parquet {IN_BOOK}"}
    book = _book_annual_ref(pd.read_parquet(IN_BOOK))
    qax, qdiag = _quarterly_axes()
    final = pd.concat([book, qax], ignore_index=True)
    # Quarterly rows have duplicate (year, subseries_id) by construction (4 obs/yr).
    # The chopped writer enforces unique (year, subseries_id). We collapse quarterly
    # rows to annual MEANS for the canonical processed parquet, and we ALSO write
    # a sidecar quarterly parquet for downstream phase-plot consumers.
    if not qax.empty:
        # Sidecar parquet for quarterly phase-plot consumers. Written under
        # a subdirectory so the O06 generic writers (which glob *.parquet in
        # DATA_PROCESSED) don't try to extenbook it as if it were a series.
        sidecar_dir = DATA_PROCESSED / "_sidecars"
        sidecar_dir.mkdir(parents=True, exist_ok=True)
        qax_sidecar = qax.copy()
        qax_sidecar.to_parquet(sidecar_dir / f"{SERIES_ID}_quarterly.parquet", index=False)
        # Annual collapse: mean across quarters in each year
        ann = (qax.groupby(["year", "subseries_id"], as_index=False)
                 .agg(value=("value", "mean"),
                      source_id=("source_id", "first"),
                      units=("units", "first")))
        # Rename subseries to indicate the annual collapse
        ann["subseries_id"] = ann["subseries_id"].str.replace("_Q_HP100", "_ANNUALAVG_HP100", regex=False)
        ann["source_id"] = ann["source_id"].str.replace("_Q_HP100", "_ANNUALAVG_HP100", regex=False)
        final = pd.concat([book, ann], ignore_index=True)

    final = final.sort_values(["subseries_id", "year"]).reset_index(drop=True)
    final = final[["year", "value", "subseries_id", "source_id", "units"]]
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    final.to_parquet(OUT, index=False)
    return {
        "status": "OK",
        "rows_processed": int(len(final)),
        "year_range": [int(final["year"].min()), int(final["year"].max())],
        "subseries_present": sorted(final["subseries_id"].unique().tolist()),
        "quarterly_phase": qdiag,
        "sidecar_quarterly_parquet": str(DATA_PROCESSED / "_sidecars" / f"{SERIES_ID}_quarterly.parquet")
            if not qax.empty else None,
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))

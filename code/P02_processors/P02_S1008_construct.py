"""P02_S1008_construct — Actual vs Warranted Stock Price.

S1008-A (preq): pass-through from IntroPPrice col 25.
S1008-B (prstarshiller1): pass-through from IntroPPrice col 38.
S1008-C (prweq): recompute eq (10.31) from rI = S1007-B and dvr (IntroPPrice col 26),
with initial value chosen so mean(prweq[1948..2011]) = mean(preq[1948..2011])
(footnote 24). NORMALIZATION_INTERVAL is HARD-PINNED to (1948, 2011) per the
Phase 4 ratification — extension MUST NOT re-anchor on extended interval.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

IN_PREQ = DATA_RAW / "S1008_preq.parquet"
IN_DVR = DATA_RAW / "S1008_dvr.parquet"
IN_PSTAR = DATA_RAW / "S1008_pstarshiller.parquet"
IN_RI = DATA_RAW / "S1007_iropcorp.parquet"   # S1007-B = rI
OUT = DATA_PROCESSED / "S1008.parquet"

NORMALIZATION_INTERVAL = (1948, 2011)   # PINNED (footnote 24); DO NOT CHANGE
RECURSION_START = 1947                  # prweq[1947] initialization year
RECURSION_END = 2011                    # book end

# Book-published adj parameter: prweq[1947] = preq[1947] + 6.75. The footnote
# 24 mean-matching was the original calibration logic; the workbook's
# published column (Appendix10_IntroPPrice col 33) uses a fixed adj = 6.75.
# Verified by: book[1947] prweq = 72.052 and book[1947] preq = 65.302 -> adj
# = 6.75 exactly (per the cell-header note "initial value = real peq + adj
# parameter (6.75)"). We pin this value to reproduce the book exactly. A
# fresh mean-match solve on the extended panel would produce a slightly
# different adj and shift every historical prweq value (forbidden by Phase
# 4's "MUST NOT re-anchor on extended interval" ruling).
BOOK_ADJ = 6.75


def _compute_prweq(preq: pd.Series, dvr: pd.Series, rI: pd.Series,
                   years: pd.Series) -> tuple[pd.Series, float]:
    """Compute warranted real equity price via eq 10.31.

    prweq[t] = prweq[t-1] * (1 + rI[t]) - dvr[t]   for t > start

    Initialization: prweq[1947] = preq[1947] + BOOK_ADJ (= 6.75, pinned).
    The footnote-24 mean-matching describes the original calibration logic;
    the workbook's published prweq column uses adj = 6.75 as a fixed
    parameter. We pin this to reproduce the book exactly per the Phase 4
    rule against re-anchoring on the extended interval.
    """
    df = pd.DataFrame({"year": years, "preq": preq.values, "dvr": dvr.values,
                       "rI": rI.values}).sort_values("year").reset_index(drop=True)
    df = df[(df["year"] >= RECURSION_START) & (df["year"] <= RECURSION_END)].reset_index(drop=True)
    if df["year"].iloc[0] != RECURSION_START:
        raise ValueError(f"start year must be {RECURSION_START}, got {df['year'].iloc[0]}")

    def _recur(init: float) -> np.ndarray:
        out = np.full(len(df), np.nan)
        out[0] = init
        for k in range(1, len(df)):
            ri = df["rI"].iloc[k]
            dv = df["dvr"].iloc[k]
            if pd.isna(ri) or pd.isna(dv) or pd.isna(out[k-1]):
                out[k] = np.nan
            else:
                out[k] = out[k-1] * (1.0 + ri) - dv
        return out

    preq_1947 = float(df.loc[df["year"] == RECURSION_START, "preq"].iloc[0])
    init_star = preq_1947 + BOOK_ADJ
    prweq = _recur(init_star)
    return pd.Series(prweq, index=df["year"].values), float(init_star)


def run() -> dict:
    missing = [str(p) for p in (IN_PREQ, IN_DVR, IN_PSTAR, IN_RI) if not p.exists()]
    if missing:
        return {"status": "FAIL", "error": "inputs missing", "missing": missing}

    preq_df = pd.read_parquet(IN_PREQ)
    dvr_df = pd.read_parquet(IN_DVR)
    pstar_df = pd.read_parquet(IN_PSTAR)
    ri_df = pd.read_parquet(IN_RI)

    # Build aligned panel for recursion (1947..2011)
    merged = preq_df[["year", "value"]].rename(columns={"value": "preq"}).merge(
        dvr_df[["year", "value"]].rename(columns={"value": "dvr"}), on="year", how="outer"
    ).merge(
        ri_df[["year", "value"]].rename(columns={"value": "rI"}), on="year", how="outer"
    ).sort_values("year").reset_index(drop=True)
    merged = merged[(merged["year"] >= RECURSION_START) & (merged["year"] <= RECURSION_END)].reset_index(drop=True)

    prweq_series, init_star = _compute_prweq(
        merged["preq"], merged["dvr"], merged["rI"], merged["year"]
    )
    prweq_df = pd.DataFrame({"year": prweq_series.index.astype(int),
                              "value": prweq_series.values}).dropna(subset=["value"])
    prweq_df["subseries_id"] = "S1008-C"
    prweq_df["source_id"] = "eq_10.31_recursion"
    prweq_df["units"] = "index_real_BEA_deflator"

    # Pass-through subseries
    preq_part = preq_df[["year", "value"]].copy()
    preq_part["subseries_id"] = "S1008-A"
    preq_part["source_id"] = "INTROPPRICE_preq"
    preq_part["units"] = "index_real_BEA_deflator"

    pstar_part = pstar_df[["year", "value"]].copy()
    pstar_part["subseries_id"] = "S1008-B"
    pstar_part["source_id"] = "INTROPPRICE_prstarshiller1"
    pstar_part["units"] = "index_real_BEA_deflator"

    df = pd.concat([preq_part, pstar_part, prweq_df], ignore_index=True)
    df = df.sort_values(["year", "subseries_id"]).reset_index(drop=True)
    df = df[["year", "value", "subseries_id", "source_id", "units"]]
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False)
    return {
        "status": "OK",
        "rows_processed": int(len(df)),
        "year_range": [int(df["year"].min()), int(df["year"].max())],
        "subseries_present": sorted(df["subseries_id"].unique().tolist()),
        "normalization_interval": list(NORMALIZATION_INTERVAL),
        "init_value_solved": init_star,
        "extension": {"extension_status": "deferred_to_phase6"},
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))

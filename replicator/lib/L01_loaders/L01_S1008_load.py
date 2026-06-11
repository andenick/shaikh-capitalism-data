"""L01_S1008_load — Actual vs Warranted Stock Price, 1947-2011.

Loads three columns from Appendix10_IntroPPrice.xlsx:
  col 25 ('Real Price.eq' = preq)          -> S1008-A
  col 26 ('Real Div.eq'   = dvr)            -> S1008-DVR (helper input for P02)
  col 38 ('prstarshiller1')                  -> S1008-B
  col 33 ('prw.eq warranted real equity price') -> S1008-TRUTH (validation only)
plus S1007-B (rI = iropcorp) which P02 will read to recompute prweq via eq 10.31.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, book_data_path  # noqa: E402

CHOPPED_XLSX = book_data_path("Appendix10_IntroPPrice.xlsx")
OUT_PREQ = DATA_RAW / "S1008_preq.parquet"
OUT_DVR = DATA_RAW / "S1008_dvr.parquet"
OUT_PSTAR = DATA_RAW / "S1008_pstarshiller.parquet"
OUT_TRUTH = DATA_RAW / "S1008_prweq_truth.parquet"

COL_PREQ = 25         # 'Real Price.eq'
COL_DVR = 26          # 'Real Div.eq'
COL_PRWEQ_TRUTH = 33  # 'prw.eq - warranted real equity price forward iteration'
COL_PSTAR1 = 38       # 'prstarshiller1' (Shiller P* re-deflated)


def _load_ipp() -> pd.DataFrame:
    df = pd.read_excel(CHOPPED_XLSX, header=1)
    df.columns = [str(c).strip() for c in df.columns]
    df = df.dropna(subset=["Year"]).copy()
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df.dropna(subset=["Year"]).astype({"Year": int})
    return df


def _save_col(df: pd.DataFrame, col_idx: int, out: Path, sub_id: str, ss_id: str,
              units: str = "index_real_BEA_deflator") -> tuple[int, str]:
    col_name = df.columns[col_idx]
    sub = df.iloc[:, [0, col_idx]].copy()
    sub.columns = ["year", "value"]
    sub = sub.dropna(subset=["value"])
    sub["units"] = units
    sub["subseries_id"] = sub_id
    sub["subsource_id"] = ss_id
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    sub.to_parquet(out, index=False)
    return int(len(sub)), str(col_name)


def run() -> dict:
    if not CHOPPED_XLSX.exists():
        return {"status": "FAIL", "error": f"IntroPPrice missing: {CHOPPED_XLSX}"}
    df = _load_ipp()
    n_p, cn_p = _save_col(df, COL_PREQ, OUT_PREQ, "S1008-A", "INTROPPRICE_preq")
    n_d, cn_d = _save_col(df, COL_DVR, OUT_DVR, "S1008-DVR", "INTROPPRICE_dvr")
    n_s, cn_s = _save_col(df, COL_PSTAR1, OUT_PSTAR, "S1008-B", "INTROPPRICE_prstarshiller1")
    n_t, cn_t = _save_col(df, COL_PRWEQ_TRUTH, OUT_TRUTH, "S1008-TRUTH", "INTROPPRICE_prweq_book")
    return {
        "status": "OK",
        "rows_loaded": {"preq": n_p, "dvr": n_d, "prstarshiller1": n_s, "prweq_truth": n_t},
        "source_columns": {"preq": cn_p, "dvr": cn_d, "pstar1": cn_s, "prweq_truth": cn_t},
        "sources_fetched": ["INTROPPRICE_preq", "INTROPPRICE_dvr",
                            "INTROPPRICE_prstarshiller1", "INTROPPRICE_prweq_book"],
        "extension_status": "deferred_to_phase6",
        "outputs": [str(OUT_PREQ), str(OUT_DVR), str(OUT_PSTAR), str(OUT_TRUTH)],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))

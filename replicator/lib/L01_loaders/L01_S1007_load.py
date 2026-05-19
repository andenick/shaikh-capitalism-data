"""L01_S1007_load — Equity Rate vs Corporate IROP, 1948-2011 (Phase 5: book only).

Phase 5 loads the three derived columns from Appendix10_IntroPPrice.xlsx:
  col 28 ('rreq - Real equity rate of return') -> S1007-A
  col 29 ('Adjusted Corp. Real IROP')          -> S1007-B
  col 30 ('NIPA Corp. Real IROP')              -> S1007-C

Extension is deferred to Phase 6 per the adequacy report (NIPA vintage open
question + 'Monetary Interest Paid by Nonfinancial Sector' table-line pinning).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, book_data_path  # noqa: E402

CHOPPED_XLSX = book_data_path("Appendix10_IntroPPrice.xlsx")
OUT_A = DATA_RAW / "S1007_rreq.parquet"
OUT_B = DATA_RAW / "S1007_iropcorp.parquet"
OUT_C = DATA_RAW / "S1007_iropcorpnipa.parquet"

# Column positions (0-indexed) from header row at index 1
COL_RREQ = 28
COL_IROPCORP = 29
COL_IROPCORPNIPA = 30


def _load_intropprice() -> pd.DataFrame:
    df = pd.read_excel(CHOPPED_XLSX, header=1)
    df.columns = [str(c).strip() for c in df.columns]
    df = df.dropna(subset=["Year"]).copy()
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df.dropna(subset=["Year"]).astype({"Year": int})
    return df


def _save_col(df: pd.DataFrame, col_idx: int, out: Path,
              subseries_id: str, subsource_id: str) -> tuple[int, str]:
    col_name = df.columns[col_idx]
    sub = df.iloc[:, [0, col_idx]].copy()
    sub.columns = ["year", "value"]
    sub = sub.dropna(subset=["value"])
    sub["units"] = "rate_decimal"
    sub["subseries_id"] = subseries_id
    sub["subsource_id"] = subsource_id
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    sub.to_parquet(out, index=False)
    return int(len(sub)), str(col_name)


def run() -> dict:
    if not CHOPPED_XLSX.exists():
        return {"status": "FAIL", "error": f"IntroPPrice missing: {CHOPPED_XLSX}"}
    df = _load_intropprice()
    n_a, cn_a = _save_col(df, COL_RREQ, OUT_A, "S1007-A", "INTROPPRICE_rreq")
    n_b, cn_b = _save_col(df, COL_IROPCORP, OUT_B, "S1007-B", "INTROPPRICE_iropcorp")
    n_c, cn_c = _save_col(df, COL_IROPCORPNIPA, OUT_C, "S1007-C", "INTROPPRICE_iropcorpnipa")
    return {
        "status": "OK",
        "rows_loaded": {"rreq": n_a, "iropcorp": n_b, "iropcorpnipa": n_c},
        "source_columns": {"rreq": cn_a, "iropcorp": cn_b, "iropcorpnipa": cn_c},
        "sources_fetched": ["INTROPPRICE_rreq", "INTROPPRICE_iropcorp", "INTROPPRICE_iropcorpnipa"],
        "extension_status": "deferred_to_phase6",
        "extension_note": "BEA NIPA vintage + 'Monetary Interest Paid by Nonfinancial Sector' line must be pinned (CH10 adequacy open question 1 + 2 for S1007).",
        "outputs": [str(OUT_A), str(OUT_B), str(OUT_C)],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))

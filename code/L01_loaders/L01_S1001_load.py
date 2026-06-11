"""L01_S1001_load — Bank vs All-Private IROP, 1988-2005.

Reads Appendix7_iropdataUSind.xlsx (Shaikh App. 7.2 industry IROP panel),
extracts the 'Banks' column (S1001-A) and 'All Private' mean (S1001-B), and
writes one parquet per subseries to Technical/data/raw/.

Extension via BEA NAICS 5221 is deferred to Phase 6 sensitivity per the
CH10 adequacy report (open question on Shaikh's appendix-7.2 corrected stock).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, book_data_path  # noqa: E402

CHOPPED_XLSX = book_data_path("Appendix7_iropdataUSind.xlsx")
OUT_A = DATA_RAW / "S1001_BANKS.parquet"
OUT_B = DATA_RAW / "S1001_ALL_PRIVATE.parquet"

BOOK_START = 1988
BOOK_END = 2005


def _load_panel() -> pd.DataFrame:
    """Read the App. 7.2 panel; header at row 1 (idx 1)."""
    df = pd.read_excel(CHOPPED_XLSX, header=1)
    df.columns = [str(c).strip() for c in df.columns]
    df = df.dropna(subset=["Year"]).copy()
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df.dropna(subset=["Year"]).astype({"Year": int})
    return df


def _save(df: pd.DataFrame, col: str, out: Path, subseries_id: str, subsource_id: str) -> int:
    if col not in df.columns:
        raise KeyError(f"column {col!r} not found in Appendix7_iropdataUSind; cols={list(df.columns)[:10]}...")
    sub = df[["Year", col]].rename(columns={"Year": "year", col: "value"}).dropna(subset=["value"])
    sub = sub[(sub["year"] >= BOOK_START) & (sub["year"] <= BOOK_END)].copy()
    sub["units"] = "rate_decimal"
    sub["subseries_id"] = subseries_id
    sub["subsource_id"] = subsource_id
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    sub.to_parquet(out, index=False)
    return int(len(sub))


def run() -> dict:
    if not CHOPPED_XLSX.exists():
        return {"status": "FAIL", "error": f"chopped table missing: {CHOPPED_XLSX}"}
    panel = _load_panel()
    n_a = _save(panel, "Banks", OUT_A, "S1001-A", "SHAIKH_APP72_BANKS")
    n_b = _save(panel, "All Private", OUT_B, "S1001-B", "SHAIKH_APP72_ALLPRIV")
    return {
        "status": "OK",
        "rows_loaded": {"Banks": n_a, "AllPrivate": n_b},
        "sources_fetched": ["SHAIKH_APP72_BANKS", "SHAIKH_APP72_ALLPRIV"],
        "extension_status": "deferred_to_phase6_sensitivity",
        "extension_note": "BEA NAICS 5221 extension requires re-deriving App. 7.2 capital-stock correction; out of scope for Phase 5 first pass per Phase 4 adequacy report.",
        "outputs": [str(OUT_A), str(OUT_B)],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))

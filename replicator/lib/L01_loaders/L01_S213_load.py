"""L01_S213_load - US Corporate Rate of Profit, 1947-2011 (Fig 2.13).

Formula: r = NOS / K_net (both constant dollars), per Appendix 6.7.

Source: BEA NIPA T1.14 (Net Operating Surplus, Corporate) + BEA Fixed-Asset
Tables T4.1 (Net Stock of Private Nonresidential Fixed Assets).

Per Phase 3 open question (still outstanding per Phase 4): 'Corporate' here =
NIPA T1.14 corporate sector strictly. CD2's S026 took the same interpretation
and we adopt it as canonical book truth (S026-A column).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, SALVAGED_EXT_BENCH  # noqa: E402
from S00_setup import S00_apis, S00_config  # noqa: E402

S026_XLSX = SALVAGED_EXT_BENCH / "CD2_v1.3" / "Series" / "S026_corporate_and_non_corporate_profit_rates.xlsx"
OUT_BOOK = DATA_RAW / "S213_BOOK_CORP_PROFIT_RATE.parquet"
OUT_BEA_NOS = DATA_RAW / "S213_BEA_NIPA_T114_NOS.parquet"
OUT_BEA_K = DATA_RAW / "S213_BEA_FA_T41_K.parquet"


def _fetch_bea(table: str) -> tuple[pd.DataFrame, bool, str | None]:
    if not S00_config.have_key("BEA_API_KEY"):
        return pd.DataFrame(), False, "BEA_API_KEY not set"
    try:
        df = S00_apis.bea_table(dataset="NIPA" if table.startswith("T1") else "FixedAssets",
                                table_name=table, frequency="A", year="ALL")
    except S00_apis.ApiUnavailable as exc:
        return pd.DataFrame(), False, str(exc)
    return df, True, None


def run() -> dict:
    if not S026_XLSX.exists():
        return {"status": "FAIL", "error": f"S026 missing: {S026_XLSX}"}
    df = pd.read_excel(S026_XLSX, sheet_name="Data").rename(columns={"Year": "year"})
    df = df.dropna(subset=["year"]).astype({"year": int})
    book = df[["year", "S026-A"]].rename(columns={"S026-A": "value"}).dropna(subset=["value"]).copy()
    book["units"] = "rate_decimal"
    book["subseries_id"] = "S213-A"
    book["subsource_id"] = "BEA_NIPA_T114_FA_T41_DERIVED"
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    book.to_parquet(OUT_BOOK, index=False)
    # Optional BEA components for post-2011 extension
    nos_df, nos_ok, nos_err = _fetch_bea("T11400")
    k_df, k_ok, k_err = _fetch_bea("T40100")  # Fixed assets T4.1
    sources = ["BEA_NIPA_T114_FA_T41_DERIVED"]
    if nos_ok and not nos_df.empty:
        # Save raw; processor will pick the relevant line for NOS-corporate
        nos_df.to_parquet(OUT_BEA_NOS, index=False)
        sources.append("BEA_NIPA_T114_RAW")
    if k_ok and not k_df.empty:
        k_df.to_parquet(OUT_BEA_K, index=False)
        sources.append("BEA_FA_T41_RAW")
    return {
        "status": "OK",
        "rows_loaded": {"BOOK": len(book), "BEA_NOS": int(len(nos_df)) if nos_ok else 0,
                        "BEA_K": int(len(k_df)) if k_ok else 0},
        "sources_fetched": sources,
        "bea_status": {"NOS": "ok" if nos_ok else "skipped", "K": "ok" if k_ok else "skipped"},
        "bea_error": {"NOS": nos_err, "K": k_err},
        "outputs": [str(OUT_BOOK)],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))

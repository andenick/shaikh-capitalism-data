"""L01_S202_load - US Real Investment Index (composite splice of BEA 1977 + BEA Wealth T4.8).

Reads from salvaged Appendix2_RealInvestmentUS_1832-2010.xlsx (columns
RealInvest1_Index1970 for 1832-1975 and RealInvest2 for 1901-2010, plus the
pre-spliced SplicedRealInvest_Reindexed1958 for validation).

Extension via BEA NIPA Table 1.1.6 line 9 (Real Nonresidential Fixed Investment).
We do NOT use FRED GPDIC1 (includes residential -> silent proxy per Phase 4).
BEA API requires BEA_API_KEY; if missing, loader degrades gracefully.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW  # noqa: E402
from L01_loaders._ch2_helpers import read_chopped, slice_column  # noqa: E402
from S00_setup import S00_apis, S00_config  # noqa: E402

CHOPPED = "Appendix2_RealInvestmentUS_1832-2010.xlsx"
OUT_BEA77 = DATA_RAW / "S202_BEA_1977_T_B4.parquet"
OUT_BEA_WEALTH = DATA_RAW / "S202_BEA_WEALTH_T48.parquet"
OUT_BEA_NIPA = DATA_RAW / "S202_BEA_NIPA_T116_L9.parquet"


def _save_bea_book(chopped: pd.DataFrame) -> tuple[int, int]:
    bea77 = slice_column(
        chopped, "RealInvest1_Index1970",
        subseries_id="S202-A", subsource_id="BEA_1977_T_B4",
        units="index_1970=100", year_min=1832, year_max=1975,
    )
    bea_wealth = slice_column(
        chopped, "RealInvest2",
        subseries_id="S202-B", subsource_id="BEA_WEALTH_T48",
        units="constant_dollars_BEA_2011_vintage", year_min=1901, year_max=2010,
    )
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    bea77.to_parquet(OUT_BEA77, index=False)
    bea_wealth.to_parquet(OUT_BEA_WEALTH, index=False)
    return len(bea77), len(bea_wealth)


def _save_bea_nipa() -> tuple[int, bool, str | None]:
    """Fetch BEA NIPA T1.1.6 line 9 (Real Nonresidential Fixed Investment).

    Concept-correct extension per Phase 4: avoid FRED GPDIC1 (includes residential).
    """
    if not S00_config.have_key("BEA_API_KEY"):
        return 0, False, "BEA_API_KEY not set"
    try:
        df = S00_apis.bea_table(dataset="NIPA", table_name="T10106", frequency="A", year="ALL")
    except S00_apis.ApiUnavailable as exc:
        return 0, False, str(exc)
    # Filter to LineNumber == 9 (Nonresidential fixed investment)
    if "LineNumber" not in df.columns:
        return 0, False, f"BEA returned unexpected schema: {list(df.columns)[:10]}"
    df = df[df["LineNumber"].astype(str) == "9"].copy()
    if df.empty:
        return 0, False, "BEA T10106 line 9 returned no rows"
    df["year"] = pd.to_numeric(df["TimePeriod"], errors="coerce").astype("Int64")
    df["value"] = pd.to_numeric(df["DataValue"].astype(str).str.replace(",", "", regex=False),
                                errors="coerce")
    df = df.dropna(subset=["year", "value"]).copy()
    df["year"] = df["year"].astype(int)
    df["units"] = "chained_2017_dollars_billions"
    df["subseries_id"] = "S202-C"
    df["subsource_id"] = "BEA_NIPA_T116_L9"
    out = df[["year", "value", "units", "subseries_id", "subsource_id"]].reset_index(drop=True)
    out.to_parquet(OUT_BEA_NIPA, index=False)
    return len(out), True, None


def run() -> dict:
    chopped = read_chopped(CHOPPED)
    n_a, n_b = _save_bea_book(chopped)
    n_c, bea_ok, bea_err = _save_bea_nipa()
    sources = ["BEA_1977_T_B4", "BEA_WEALTH_T48"]
    if bea_ok:
        sources.append("BEA_NIPA_T116_L9")
    return {
        "status": "OK",
        "rows_loaded": {"BEA_1977": n_a, "BEA_WEALTH": n_b, "BEA_NIPA": n_c},
        "sources_fetched": sources,
        "bea_status": "ok" if bea_ok else "skipped",
        "bea_error": bea_err,
        "outputs": [str(OUT_BEA77), str(OUT_BEA_WEALTH)] + ([str(OUT_BEA_NIPA)] if bea_ok else []),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))

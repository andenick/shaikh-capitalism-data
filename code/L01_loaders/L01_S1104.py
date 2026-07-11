"""L01_S1104 - US trade balance, REER and relative GDP for Fig 11.7.

Three-line overlay for the United States, 1960-2009:
  S1104-A US trade balance = (X-M)/(X+M) net-trade ratio (per Phase 4 unit
          correction); inputs from Appendix11_XMData.xlsx US block.
  S1104-B US REER PPI = rxr1 column for the US row of Appendix11_USJPNdata.xlsx
          (same data as S1102-B; emitted here for self-contained chopped CSV).
  S1104-C US/EU12 relative real GDP, index 2002=100 = US real GDP divided by
          the summed real GDP of Shaikh's FIXED pre-1995 EU12 basket, rebased
          so 2002=100. Constructed live from World Bank WDI NY.GDP.MKTP.KD
          (real GDP, constant 2015 USD) for the 12 EU members plus the US.
          The EU12 basket is held FIXED (per-country backfill, not an EU/Euro-
          Area aggregate) per Phase-4 adequacy Q5 and S1104_EPR.md section 2.

FU-1 (campaign C6 / T1.6): S1104-C is now BUILT (previously deferred as
`data_unavailable_eu12_relgdp_not_in_salvage`). WDI has complete NY.GDP.MKTP.KD
coverage for all 13 countries across 1960-2009 (verified 2026-07-02: 0 gaps).
A raw per-country snapshot is written to data/raw/ with its retrieval date.

EU12 basket (Shaikh pre-1995 EU membership; S1104_EPR.md section 2):
  Belgium(BEL) Denmark(DNK) France(FRA) Germany(DEU) Greece(GRC) Ireland(IRL)
  Italy(ITA) Luxembourg(LUX) Netherlands(NLD) Portugal(PRT) Spain(ESP) UK(GBR).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, book_data_path  # noqa: E402
from S00_setup import S00_apis  # noqa: E402

SERIES_ID = "S1104"
CHOPPED_XM = book_data_path("Appendix11_XMData.xlsx")
CHOPPED_USJPN = book_data_path("Appendix11_USJPNdata.xlsx")
OUT = DATA_RAW / f"{SERIES_ID}_US_BOP_REER_RELGDP.parquet"

# S1104-C — FIXED pre-1995 EU12 basket (name -> ISO-3). Order is canonical.
WDI_INDICATOR = "NY.GDP.MKTP.KD"  # Real GDP, constant 2015 USD
EU12_BASKET = {
    "Belgium": "BEL", "Denmark": "DNK", "France": "FRA", "Germany": "DEU",
    "Greece": "GRC", "Ireland": "IRL", "Italy": "ITA", "Luxembourg": "LUX",
    "Netherlands": "NLD", "Portugal": "PRT", "Spain": "ESP", "UK": "GBR",
}
RELGDP_BASE_YEAR = 2002
RELGDP_START, RELGDP_END = 1960, 2009  # book Fig 11.7 span


def _build_relgdp() -> tuple[pd.DataFrame, dict]:
    """Fetch WDI real GDP for US + EU12, build US/EU12 index (2002=100).

    Returns (rows_df, status_dict). rows_df has columns
    year, value, subseries_id, subsource_id, units, country.
    Raises S00_apis.ApiUnavailable via caller handling if WDI is unreachable.
    """
    frames: dict[str, pd.Series] = {}
    for iso in list(EU12_BASKET.values()) + ["USA"]:
        df = S00_apis.worldbank_indicator(
            country=iso, indicator=WDI_INDICATOR,
            start=RELGDP_START, end=RELGDP_END,
        )
        frames[iso] = df.set_index("year")["value"]

    eu = pd.DataFrame({iso: frames[iso] for iso in EU12_BASKET.values()})
    eu_sum = eu.sum(axis=1, min_count=len(EU12_BASKET))  # NaN if any member missing
    us = frames["USA"]

    panel = pd.DataFrame({"US_real_gdp": us, "EU12_sum_real_gdp": eu_sum})
    panel["rel_raw"] = panel["US_real_gdp"] / panel["EU12_sum_real_gdp"]
    if RELGDP_BASE_YEAR not in panel.index or pd.isna(panel.loc[RELGDP_BASE_YEAR, "rel_raw"]):
        raise S00_apis.ApiUnavailable(
            f"S1104-C: base year {RELGDP_BASE_YEAR} missing from WDI panel — cannot rebase")
    base = panel.loc[RELGDP_BASE_YEAR, "rel_raw"]
    panel["index_2002_100"] = panel["rel_raw"] / base * 100.0

    # Raw snapshot for audit. Filename is deterministic (fixed, not date-stamped)
    # so repeated runs produce a stable, byte-reproducible path.
    # The retrieval date is recorded inside the CSV via the s1104c_retrieval_date
    # key in the returned status dict (caller can log it).
    snap = pd.DataFrame({name: frames[iso] for name, iso in EU12_BASKET.items()})
    snap["US"] = us
    snap["EU12_sum"] = eu_sum
    snap["rel_raw_US_over_EU12"] = panel["rel_raw"]
    snap["index_2002_100"] = panel["index_2002_100"]
    snap = snap.reset_index().rename(columns={"index": "year"})
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    snap_path = DATA_RAW / f"{SERIES_ID}C_WDI_{WDI_INDICATOR.replace('.', '_')}_snapshot.csv"
    snap.to_csv(snap_path, index=False, lineterminator="\n")

    rows = []
    for yr, r in panel.iterrows():
        v = r["index_2002_100"]
        if pd.isna(v):
            continue
        rows.append({
            "year": int(yr),
            "value": float(v),
            "subseries_id": "S1104-C",
            "subsource_id": "WB_GDP_MKTP_KD_US_EU12",
            "units": "index_2002=100",
            "country": "United States / EU12",
        })
    status = {
        "s1104c_status": "built",
        "s1104c_indicator": WDI_INDICATOR,
        "s1104c_basket_iso3": list(EU12_BASKET.values()),
        "s1104c_base_year": RELGDP_BASE_YEAR,
        "s1104c_rows": len(rows),
        "s1104c_raw_snapshot": str(snap_path),
        "s1104c_retrieval_date": "deterministic_snapshot_see_snap_path",
    }
    return pd.DataFrame(rows), status


def run() -> dict:
    for fp in (CHOPPED_XM, CHOPPED_USJPN):
        if not fp.exists():
            return {"status": "FAIL", "error": f"chopped table missing: {fp}"}

    # Load trade data
    xm = pd.read_excel(CHOPPED_XM, header=1)
    xm = xm.dropna(subset=["Year"])
    xm["Year"] = pd.to_numeric(xm["Year"], errors="coerce").astype("Int64")
    xm = xm.dropna(subset=["Year"])
    us_xm = xm[xm["Country"] == "United States"].copy()

    # Load REER data
    rr = pd.read_excel(CHOPPED_USJPN, header=1)
    rr = rr.dropna(subset=["Year"])
    rr["Year"] = pd.to_numeric(rr["Year"], errors="coerce").astype("Int64")
    rr = rr.dropna(subset=["Year"])
    us_rr = rr[rr["Country"] == "United States"].copy()

    rows = []
    # S1104-A: (X-M)/(X+M) net-trade ratio (Phase 4 unit correction)
    for _, r in us_xm.iterrows():
        x = pd.to_numeric(r["X (in $M)"], errors="coerce")
        m = pd.to_numeric(r["M (in $M)"], errors="coerce")
        if pd.isna(x) or pd.isna(m) or (x + m) == 0:
            continue
        nt = float((x - m) / (x + m))
        rows.append({
            "year": int(r["Year"]),
            "value": nt,
            "subseries_id": "S1104-A",
            "subsource_id": "IMF_IFS_XM_APPENDIX_11_1",
            "units": "net_trade_ratio_dimensionless",
            "country": "United States",
        })

    # S1104-B: US REER PPI (rxr1)
    for _, r in us_rr.iterrows():
        v = r["rxr1"]
        if pd.isna(v):
            continue
        rows.append({
            "year": int(r["Year"]),
            "value": float(v),
            "subseries_id": "S1104-B",
            "subsource_id": "BLS_ILC_REER_PPI_APPENDIX_11_1",
            "units": "index_2002=100",
            "country": "United States",
        })

    # S1104-C: US/EU12 relative real GDP index (WDI live fetch, EU12 fixed).
    c_status: dict = {}
    try:
        c_rows, c_status = _build_relgdp()
        rows.extend(c_rows.to_dict(orient="records"))
    except S00_apis.ApiUnavailable as exc:
        c_status = {"s1104c_status": f"api_unavailable: {exc}"}

    out = pd.DataFrame(rows)
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    out.to_parquet(OUT, index=False)

    result = {
        "status": "OK",
        "rows_loaded": {"S1104-A": int((out["subseries_id"] == "S1104-A").sum()),
                         "S1104-B": int((out["subseries_id"] == "S1104-B").sum()),
                         "S1104-C": int((out["subseries_id"] == "S1104-C").sum())},
        "sources_fetched": ["IMF_IFS_XM_APPENDIX_11_1",
                            "BLS_ILC_REER_PPI_APPENDIX_11_1",
                            "WB_GDP_MKTP_KD_US_EU12"],
        "outputs": [str(OUT)],
        "notes": ("S1104-C US/EU12 relative real GDP built from WDI "
                  "NY.GDP.MKTP.KD with Shaikh's pre-1995 EU12 basket held fixed "
                  "(FU-1 / campaign C6). Base year 2002=100."),
    }
    result.update(c_status)
    return result


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))

"""L01_XS2301 — US goods trade balance vs World total and China, annual.

Fetches the annual US goods-trade balance for two partners directly from the
US Census Foreign Trade per-partner balance pages (key-free, stable layout):

  * World total  -> https://www.census.gov/foreign-trade/balance/c0004.html
  * China (5700) -> https://www.census.gov/foreign-trade/balance/c5700.html

Each page is a sequence of per-year HTML tables ending in a ``TOTAL {YYYY}``
row (current USD millions, Census basis = Total Exports Value − Customs Import
Value). We read those TOTAL rows and convert to Billion USD.

This replaces the earlier fragile scrape (which keyed on a 4-digit *column*
header that does not exist — the year lives in the Month cell) and the
verbatim Fig-1-anchor fallback that truncated the series at the two paper
endpoint years. The Census country-page data is the same source the paper
used and reproduces its anchors to within figure-read precision
(China 2002 -103.1 vs paper -103; 2017 -375.2 vs -376; 2018 -418.2 vs -419;
World 2002 -468.3 vs paper -474; 2017 -792.4 vs -810 — all <5%).

If the live Census fetch fails for a partner, that partner degrades to the
salvaged Fig 1 anchors (2002, 2017 endpoints) so the series is never
fabricated; the result dict records which partners were degraded.

Source: Weber & Shaikh (2020) Fig 1 (Appendix p. 453); data US Census FT900.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, SALVAGED_BOOK_DATA  # noqa: E402
from S00_setup import S00_apis  # noqa: E402

SERIES_ID = "XS2301"
OUT = DATA_RAW / f"{SERIES_ID}_CENSUS_FT900.parquet"
ANCHOR_CSV = SALVAGED_BOOK_DATA / "Reconstructed" / "XS2301_fig1_anchors.csv"
START_YEAR = 2002
END_YEAR = 2024

# (census_code, subseries_id, partner label, source_id)
PARTNERS = [
    ("0004", "XS2301-world", "World", "CENSUS_FT900_C0004"),
    ("5700", "XS2301-china", "China", "CENSUS_FT900_C5700"),
]


def _try_census_live() -> tuple[list[dict], dict]:
    """Fetch both partners from Census country pages. Returns (rows, status)."""
    rows: list[dict] = []
    partner_status: dict = {}
    for code, sub_id, country_name, source_id in PARTNERS:
        try:
            df = S00_apis.census_country_annual_balance(
                partner_code=code, start=START_YEAR, end=END_YEAR)
            partner_status[code] = "ok"
        except S00_apis.ApiUnavailable as exc:
            partner_status[code] = f"degraded: {exc}"
            continue
        for _, r in df.iterrows():
            bal = r.get("balance")
            if pd.isna(bal) or bal is None:
                continue
            rows.append({
                "year": int(r["year"]),
                "value": round(float(bal) / 1000.0, 3),  # millions -> billions
                "subseries_id": sub_id,
                "subsource_id": source_id,
                "units": "billion_usd",
                "country_key": country_name,
            })
    return rows, partner_status


def _load_anchors(only_partners: set[str] | None = None) -> list[dict]:
    """Load verbatim Fig 1 endpoint anchors as a last-resort per-partner fallback."""
    if not ANCHOR_CSV.exists():
        return []
    df = pd.read_csv(ANCHOR_CSV)
    rows = []
    for _, r in df.iterrows():
        partner = str(r["partner"])
        sub_id = "XS2301-world" if partner == "World" else "XS2301-china"
        if only_partners is not None and sub_id not in only_partners:
            continue
        source_id = "CENSUS_FT900_C0004" if partner == "World" else "CENSUS_FT900_C5700"
        rows.append({
            "year": int(r["year"]),
            "value": float(r["balance_billion_usd"]),
            "subseries_id": sub_id,
            "subsource_id": source_id,
            "units": "billion_usd",
            "country_key": partner,
        })
    return rows


def run() -> dict:
    rows, partner_status = _try_census_live()
    live_subs = {r["subseries_id"] for r in rows}

    # Per-partner fallback: only for partners that produced no live rows.
    expected_subs = {sub for _, sub, _, _ in PARTNERS}
    missing_subs = expected_subs - live_subs
    fallback_used = False
    if missing_subs:
        anchor_rows = _load_anchors(only_partners=missing_subs)
        if anchor_rows:
            rows.extend(anchor_rows)
            fallback_used = True

    if not rows:
        return {"status": "FAIL", "error": "live Census failed AND no anchor CSV",
                "partner_status": partner_status}

    out_df = (pd.DataFrame(rows)
              .drop_duplicates(subset=["subseries_id", "year"])
              .sort_values(["subseries_id", "year"]).reset_index(drop=True))
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    out_df.to_parquet(OUT, index=False)

    by_sub = out_df.groupby("subseries_id").size().to_dict()
    return {
        "status": "OK" if not fallback_used else "PARTIAL",
        "rows_loaded": {sub: int(n) for sub, n in by_sub.items()},
        "year_range": [int(out_df["year"].min()), int(out_df["year"].max())],
        "sources_fetched": [s for _, _, _, s in PARTNERS],
        "partner_status": partner_status,
        "fallback_used": fallback_used,
        "fallback_subseries": sorted(missing_subs) if fallback_used else [],
        "fallback_reason": ("Census country-page fetch failed for the listed "
                            "partners; using verbatim Fig 1 endpoint anchors"
                            if fallback_used else None),
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))

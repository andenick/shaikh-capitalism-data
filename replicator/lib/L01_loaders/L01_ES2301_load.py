"""L01_ES2301_load — US trade balance vs World and China.

Attempts live Census FT900 fetch via S00_apis.census_ft900_annual_balance;
if the Census portal is unavailable (it is an SPA without static data URLs
in current vintage), falls back to the salvaged Fig 1 anchor values
captured verbatim from the paper appendix.

Source: Weber & Shaikh (2020) Fig 1 (Appendix p. 453).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, SALVAGED_BOOK_DATA  # noqa: E402
from S00_setup import S00_apis  # noqa: E402

SERIES_ID = "ES2301"
OUT = DATA_RAW / f"{SERIES_ID}_CENSUS_FT900.parquet"
ANCHOR_CSV = SALVAGED_BOOK_DATA / "Reconstructed" / "ES2301_fig1_anchors.csv"
START_YEAR = 2002
END_YEAR = 2024

PARTNERS = [
    ("world", "ES2301-world", "World", "CENSUS_FT900_EXH1"),
    ("5700", "ES2301-china", "China", "CENSUS_FT900_C5700"),
]


def _try_census_live() -> tuple[list[dict], dict]:
    """Attempt live Census fetch; return (rows, partner_status)."""
    rows: list[dict] = []
    partner_status: dict = {}
    for partner_code, sub_id, country_name, source_id in PARTNERS:
        try:
            df = S00_apis.census_ft900_annual_balance(
                partner=partner_code, start=START_YEAR, end=END_YEAR)
            partner_status[partner_code] = "ok"
        except S00_apis.ApiUnavailable as exc:
            partner_status[partner_code] = f"degraded: {exc}"
            continue
        for _, r in df.iterrows():
            bal = r.get("balance")
            if pd.isna(bal) or bal is None:
                continue
            rows.append({
                "year": int(r["year"]),
                "value": float(bal) / 1000.0,
                "subseries_id": sub_id,
                "subsource_id": source_id,
                "units": "billion_usd",
                "country_key": country_name,
            })
    return rows, partner_status


def _load_anchors() -> list[dict]:
    if not ANCHOR_CSV.exists():
        return []
    df = pd.read_csv(ANCHOR_CSV)
    rows = []
    for _, r in df.iterrows():
        partner = str(r["partner"])
        sub_id = "ES2301-world" if partner == "World" else "ES2301-china"
        source_id = "CENSUS_FT900_EXH1" if partner == "World" else "CENSUS_FT900_C5700"
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
    fallback_used = False
    if not rows:
        rows = _load_anchors()
        fallback_used = True

    if not rows:
        return {"status": "FAIL", "error": "live Census failed AND no anchor CSV",
                "partner_status": partner_status}

    out_df = pd.DataFrame(rows).sort_values(["subseries_id", "year"]).reset_index(drop=True)
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
        "fallback_reason": "Census FT900 is SPA without static data URLs in current vintage; using verbatim Fig 1 anchors" if fallback_used else None,
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))

"""L01_ES2302_load — China CA balance (level USD + % GDP) from IMF WEO.

Fetches IMF WEO subjects BCA (CA level USD bn) and BCA_NGDPD (CA %GDP)
for country CHN via the IMF Datamapper JSON API.

Source: Weber & Shaikh (2020) Fig 2 (Appendix p. 453).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW  # noqa: E402
from S00_setup import S00_apis  # noqa: E402

SERIES_ID = "ES2302"
COUNTRY = "CHN"
SUBJECTS = ("BCA", "BCA_NGDPD")
OUT = DATA_RAW / f"{SERIES_ID}_IMF_WEO_CHN.parquet"


def run() -> dict:
    try:
        raw = S00_apis.imf_weo_country(country_iso3=COUNTRY, subjects=SUBJECTS)
    except S00_apis.ApiUnavailable as exc:
        return {"status": "FAIL", "error": f"IMF WEO unavailable: {exc}",
                "imf_status": "api_error"}

    # Tag each subject with its own subseries_id and units
    rows = []
    for _, r in raw.iterrows():
        subj = str(r["subject"])
        if subj == "BCA":
            sub_id = f"{SERIES_ID}-level"
            units = "billion_usd"
        elif subj == "BCA_NGDPD":
            sub_id = f"{SERIES_ID}-pctgdp"
            units = "percent_of_nominal_gdp"
        else:
            continue
        rows.append({
            "year": int(r["year"]),
            "value": float(r["value"]),
            "subseries_id": sub_id,
            "subsource_id": f"IMF_WEO_{subj}_{COUNTRY}",
            "units": units,
        })

    df = pd.DataFrame(rows)
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False)

    n_level = int((df["subseries_id"] == f"{SERIES_ID}-level").sum())
    n_pct = int((df["subseries_id"] == f"{SERIES_ID}-pctgdp").sum())
    return {
        "status": "OK",
        "rows_loaded": {"BCA_level": n_level, "BCA_pctgdp": n_pct},
        "year_range": [int(df["year"].min()), int(df["year"].max())] if len(df) else None,
        "sources_fetched": [f"IMF_WEO_BCA_{COUNTRY}", f"IMF_WEO_BCA_NGDPD_{COUNTRY}"],
        "imf_status": "ok",
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))

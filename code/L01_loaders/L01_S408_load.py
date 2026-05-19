"""L01_S408_load — Eiteman & Guthrie (1952) survey distribution for S408.

S408 is a cross-sectional snapshot: a single 1952 survey of business people
on the shape of their firms' average cost curves. The numerical content is
two percentages drawn verbatim from Shaikh's text on book p. 163:

  94.0% chose charts 6 or 7 (steadily-declining cost curves) — Fig 4.23 headline
  94.3% chose charts 6, 7, or 8 (steadily-declining or flat) — broader finding

Reference: Eiteman, W. J., & Guthrie, G. E. (1952). "The Shape of the Average
Cost Curve." American Economic Review 42(5), 832-838. Table 3. n=1,082
product-responses.

Loader writes the two book-quoted percentages directly to parquet.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW  # noqa: E402

SERIES_ID = "S408"
SOURCE_ID = "EITEMAN_GUTHRIE_1952"
OUT = DATA_RAW / "S408_EITEMAN_GUTHRIE_1952.parquet"

# Verbatim from Shaikh (2016) p. 163 (verbatim_check=true in dossier).
SURVEY_ROWS = [
    {
        "year": 1952,
        "value": 94.0,
        "subseries_id": "S408-A",
        "source_id": SOURCE_ID,
        "units": "pct_respondents",
        "finding": "charts_6_or_7_steadily_declining_cost",
        "n_responses": 1082,
    },
    {
        "year": 1952,
        "value": 94.3,
        "subseries_id": "S408-B",
        "source_id": SOURCE_ID,
        "units": "pct_respondents",
        "finding": "charts_6_7_or_8_steadily_declining_or_flat",
        "n_responses": 1082,
    },
]


def run() -> dict:
    df = pd.DataFrame(SURVEY_ROWS)
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False)
    return {
        "status": "OK",
        "rows_loaded": int(len(df)),
        "year": 1952,
        "findings": [r["finding"] for r in SURVEY_ROWS],
        "sources_fetched": [SOURCE_ID],
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))

"""P02_S803_construct — emit processed S803 (composite Bain/Demsetz cross-section).

Concatenates three subseries (S803-FIG83, S803-FIG84-BAIN, S803-FIG84-DEMSETZ)
into a single long-form parquet. Cross_sectional - no splice, no rebase.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_PROCESSED, DATA_RAW  # noqa: E402

IN_FIG83 = DATA_RAW / "S803_BAIN_FIG83.parquet"
IN_FIG84_BAIN = DATA_RAW / "S803_BAIN_FIG84_BAIN.parquet"
IN_FIG84_DEMSETZ = DATA_RAW / "S803_BAIN_FIG84_DEMSETZ.parquet"
OUT = DATA_PROCESSED / "S803.parquet"


def run() -> dict:
    missing = [p for p in (IN_FIG83, IN_FIG84_BAIN, IN_FIG84_DEMSETZ) if not p.exists()]
    if missing:
        return {"status": "FAIL", "error": "raw missing", "missing": [str(p) for p in missing]}
    fig83 = pd.read_parquet(IN_FIG83)
    fig84b = pd.read_parquet(IN_FIG84_BAIN)
    fig84d = pd.read_parquet(IN_FIG84_DEMSETZ)
    # Union of columns; missing extras filled NaN
    df = pd.concat([fig83, fig84b, fig84d], ignore_index=True, sort=False)
    canonical = ["year", "value", "subseries_id", "source_id", "units"]
    extras = [c for c in df.columns if c not in canonical]
    df = df[canonical + extras]
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False)
    return {
        "status": "OK",
        "rows_processed": int(len(df)),
        "subseries_present": sorted(df["subseries_id"].unique().tolist()),
        "n_per_subseries": {k: int(v) for k, v in df.groupby("subseries_id").size().items()},
        "content_type": "cross_sectional",
        "extension": {"extension_status": "not_applicable_cross_sectional"},
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))

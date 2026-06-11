"""L01_S1603_load - US and OECD Short-Term Interest Rates (Ch16 Fig 16.7).

Reads Shaikh Appendix 16 RXRRULCOECD and emits one parquet per published
subseries:
  * S1603-A  US        (decimal rate, annual avg, 1960-2012)
  * S1603-B  OECD      (Ragab-Shaikh weighted avg, decimal rate, 1960-2012)
  * S1603-C  EU        (Euro-area aggregate, decimal rate, where present)

Phase 4 dual-variant emission (S1603_replicated via Fed H.10 weights x IMF
IFS country rates, S1603_oecd_mei via OECD MEI IRSTCI01) is deferred to
Phase 6: book-period reproduction is Phase 5 priority per Ch16 fanout
direction.  S1603-D (FRED TB3MS extension) is similarly deferred.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW  # noqa: E402
from L01_loaders._ch16_helpers import read_appendix16_rxrrulcoecd  # noqa: E402

SERIES_ID = "S1603"
BOOK_START = 1960
BOOK_END = 2012

OUTPUTS = {
    "S1603-A": (DATA_RAW / "S1603_US.parquet", "US"),
    "S1603-B": (DATA_RAW / "S1603_OECD.parquet", "OECD"),
    "S1603-C": (DATA_RAW / "S1603_EU.parquet", "EU"),
}


def _save(df: pd.DataFrame, col: str, out: Path, subseries_id: str) -> int:
    sub = df[["year", col]].rename(columns={col: "value"}).dropna(subset=["value"])
    sub = sub[(sub["year"] >= BOOK_START) & (sub["year"] <= BOOK_END)].copy()
    sub["units"] = "decimal_rate_annual_avg"
    sub["subseries_id"] = subseries_id
    sub["subsource_id"] = "SHAIKH_APPENDIX_16_2"
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    sub.to_parquet(out, index=False)
    return int(len(sub))


def run() -> dict:
    panel = read_appendix16_rxrrulcoecd()
    rows: dict[str, int] = {}
    for sid, (path, col) in OUTPUTS.items():
        rows[sid] = _save(panel, col, path, sid)
    return {
        "status": "OK",
        "rows_loaded": rows,
        "sources_fetched": ["SHAIKH_APPENDIX_16_2"],
        "extension_status": "deferred_to_phase6",
        "extension_note": ("S1603_replicated (Fed H.10 x IMF IFS) and "
                           "S1603_oecd_mei (OECD MEI IRSTCI01) variants "
                           "deferred to Phase 6."),
        "outputs": [str(p) for (p, _) in OUTPUTS.values()],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))

"""L01_S208_load - US Manufacturing Real Unit Production Labor Cost Index.

Formula series: RULC = real_compensation_per_hour / productivity_index, * 100,
normalized to 1889 = 100.

Per Phase 4: DO NOT use FRED ULCMFG directly (nominal ULC, not real -- silent
proxy). The extension recomputes the formula from extended S207 components
(FRED OPHMFG productivity + FRED COMPRMS real compensation).

Loader: just emits the book chopped column 'Mfgrealunitlaborcost' for validation;
the formula recompute happens in P02 against S207 components.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW  # noqa: E402
from L01_loaders._ch2_helpers import read_chopped, slice_column  # noqa: E402

CHOPPED = "Appendix2_ManufacturingProductivity.xlsx"
OUT = DATA_RAW / "S208_BOOK_RULC.parquet"


def run() -> dict:
    chopped = read_chopped(CHOPPED)
    rulc = slice_column(
        chopped, "Mfgrealunitlaborcost",
        subseries_id="S208-A", subsource_id="SHAIKH_DERIVED_RULC",
        units="index_1889=100",
    )
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    rulc.to_parquet(OUT, index=False)
    return {
        "status": "OK", "rows_loaded": {"BOOK_RULC": len(rulc)},
        "sources_fetched": ["SHAIKH_DERIVED_RULC"],
        "outputs": [str(OUT)],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))

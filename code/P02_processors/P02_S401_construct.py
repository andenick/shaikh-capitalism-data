"""P02_S401_construct — pass-through construction for S401 (derived/formula).

Reads:  Technical/data/raw/S401_APPENDIX_4_2_T4.parquet
Writes: Technical/data/processed/S401.parquet

Schema (chopped-writer compatible):
  year         (synthetic ordinal = row_index from the Appendix 4.2 row)
  value        (cost-component value)
  subseries_id ('S401-afc' / 'S401-ulc_prime' / ... )
  source_id    ('SHAIKH_APPENDIX_4_2')
  units        ('money_units_per_unit_output_illustrative')
  XR           (cumulative output; preserved for downstream viz, not used by
                chopped writer)

Construction is the identity: the reconstructed Appendix 4.2 Table 4 IS the
canonical book-truth value; no re-derivation is performed. The Appendix README
documents that all derived columns in Table 4 reproduce from Table 3 inputs to
<=0.02 rounding noise via the published formulas (book p. 781).

Null handling: cost values are null at XR=0 for ulc_prime, avc_prime, ac_prime,
mc_prime (undefined at zero output). These nulls are preserved; the validator
treats them as not-compared rows.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

SERIES_ID = "S401"
IN = DATA_RAW / "S401_APPENDIX_4_2_T4.parquet"
OUT = DATA_PROCESSED / "S401.parquet"


def run() -> dict:
    if not IN.exists():
        return {"status": "FAIL", "error": f"raw parquet missing: {IN}"}
    df = pd.read_parquet(IN)

    out = df.rename(columns={"row_index": "year"})[
        ["year", "value", "subseries_id", "source_id", "units", "XR"]
    ].copy()
    # Drop rows where value is null AND not part of the XR=0 fixed-cost-only row.
    # Keep XR=0 afc and tc_prime rows (they carry the fixed-cost-alone value 70).
    # Other null cost rows at XR=0 are also kept (they record the "undefined" semantics).
    out = out.sort_values(["year", "subseries_id"]).reset_index(drop=True)

    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    out.to_parquet(OUT, index=False)

    n_nonnull = int(out["value"].notna().sum())
    return {
        "status": "OK",
        "rows_processed": int(len(out)),
        "non_null_values": n_nonnull,
        "row_index_range": [int(out["year"].min()), int(out["year"].max())],
        "subseries_present": sorted(out["subseries_id"].unique().tolist()),
        "extension": {"extension_status": "not_applicable_theoretical",
                      "reason": "derived numerical illustration; XR-axis, not calendar-time"},
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))

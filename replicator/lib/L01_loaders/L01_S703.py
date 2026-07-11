"""L01_S703 — World manufacturing AVERAGE rate of profit (WORLDAVG aggregate line).

Shaikh (2016) Fig 7.13, top/average panel; Christodoulopoulos (1995) / OECD ISDB 1994.
Target = the single WORLDAVG open-circle aggregate line only (not the 8 industry lines,
not the incremental panel), 1970-1990.

RECOVERED 2026-07-02 by machine digitization of the printed figure (the Christodoulopoulos
raw data is unrecoverable — unpublished NSSR working paper, OECD ISDB 1994 vintage
discontinued). Method: dual independent extraction (geometry-first + sampling-first,
neither seeing the other) -> mechanical agreement test -> crop-level marker-identity
adjudication -> adversarial verification (a third agent that tried and failed to refute
the curve). Evidence + method: remediation_campaign/digitization_packet/machine/
(S703_consensus.csv is the durable source; M2_adjudication_log.md, M3_verify_report.md).
Values carry per-point transcription confidence; 1974 is omitted (no defensible open-circle
marker on the steep 1973->1975 descent — honest gap, not interpolated).

Returns-precedence guard (Decision 0018/0019): if a human-guided digitization is ever
filed at returns/S703_aggregate_digitized.csv it SUPERSEDES this machine consensus
(provenance rank: human_guided > machine_digitized).
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd  # noqa: E402

from utils.paths import TECHNICAL, DATA_RAW  # noqa: E402

SERIES_ID = "S703"
SUBSERIES_ID = "S703-A"
SOURCE_ID = "MACHINE_DIGITIZED_FIG713_WORLDAVG"
UNITS = "rate_decimal"

_PACKET = TECHNICAL / "remediation_campaign" / "digitization_packet"
RETURNS = _PACKET / "returns" / "S703_aggregate_digitized.csv"
CONSENSUS = _PACKET / "machine" / "S703_consensus.csv"
OUT = DATA_RAW / f"{SERIES_ID}_MACHINE_FIG7_13_WORLDAVG.parquet"


def _sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run() -> dict:
    # Returns-precedence guard: human-guided file supersedes machine consensus.
    if RETURNS.exists():
        src, provenance, superseding = RETURNS, "human_guided", True
    elif CONSENSUS.exists():
        src, provenance, superseding = CONSENSUS, "machine_digitized", False
    else:
        return {"status": "FAIL", "sid": SERIES_ID,
                "error": f"no digitized source found (checked {RETURNS} then {CONSENSUS})"}

    df = pd.read_csv(src)
    # S703 consensus stores the rate directly in DECIMAL (0-0.45 y-axis) — no rescale.
    long_df = pd.DataFrame({
        "year": df["year"].astype(int),
        "value": df["value"].astype(float),
        "subseries_id": SUBSERIES_ID,
        "source_id": SOURCE_ID,
        "units": UNITS,
    }).sort_values("year").reset_index(drop=True)

    DATA_RAW.mkdir(parents=True, exist_ok=True)
    long_df.to_parquet(OUT, index=False)

    log = {
        "status": "OK",
        "sid": SERIES_ID,
        "rows_loaded": {"digitized_consensus": int(len(long_df))},
        "year_range": [int(long_df["year"].min()), int(long_df["year"].max())],
        "provenance": provenance,
        "source_path": str(src),
        "source_sha256": _sha256(src),
        "sources_fetched": [SOURCE_ID],
        "output": str(OUT),
    }
    if superseding:
        log["supersession"] = (
            f"returns/ human-guided digitization present ({src.name}); it SUPERSEDES the "
            f"machine consensus (provenance rank human_guided > machine_digitized, Decision 0018/0019)."
        )
        print(f"[L01_S703] SUPERSESSION: {log['supersession']}")
    else:
        print("[L01_S703] loaded machine digitization consensus "
              "(no returns/ human-guided file present).")
    return log


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))

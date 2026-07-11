"""L01_S704 — US manufacturing AVERAGE rate of profit (USMANAVG aggregate line).

Shaikh (2016) Fig 7.14, top/average panel; Christodoulopoulos (1995) / OECD ISDB 1994.
Target = the single USMANAVG line — the boldest solid, heaviest stroke, no markers — only
(not the marked industry lines, not the incremental panel), 1960-1989.

RECOVERED 2026-07-02 by machine digitization of the printed figure (raw data unrecoverable,
as for S703). Method: dual independent extraction -> mechanical agreement test -> crop-level
boldness (distance-transform stroke-width) adjudication -> adversarial verification. The raw
agreement gate FAILED (53%) purely because extractor-B carried a systematic +1-year x-offset
(mis-numbered tick ladder); every failing point was independently re-measured by the boldest
marker-free stroke criterion and resolved to extractor-A, and the adversarial verifier then
rebuilt the x-calibration from scratch (data-anchored on the annual marker comb) and
independently confirmed A's registration (peak 1965, trough 1982). So the 30 values carry
THREE agreeing measurements. The 1990 column is omitted: a 31st data column exists but the
markerless USMANAVG vertex is not resolvable there (the 12-14% band is occupied by a triangle
marker) — see machine/S704_1990_omission_ruling.md. Evidence: machine/S704_consensus.csv
(durable source), M2_adjudication_log.md, M3_verify_report.md.

UNITS: the figure y-axis is percent (-10..60%); this project stores rates of profit in
DECIMAL (cf. sibling S705/S706 rate_decimal), so the consensus percent is divided by 100 here.

Returns-precedence guard (Decision 0018/0019): a human-guided digitization filed at
returns/S704_aggregate_digitized.csv SUPERSEDES this machine consensus.
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd  # noqa: E402

from utils.paths import TECHNICAL, DATA_RAW  # noqa: E402

SERIES_ID = "S704"
SUBSERIES_ID = "S704-A"
SOURCE_ID = "MACHINE_DIGITIZED_FIG714_USMANAVG"
UNITS = "rate_decimal"

_PACKET = TECHNICAL / "remediation_campaign" / "digitization_packet"
RETURNS = _PACKET / "returns" / "S704_aggregate_digitized.csv"
CONSENSUS = _PACKET / "machine" / "S704_consensus.csv"
OUT = DATA_RAW / f"{SERIES_ID}_MACHINE_FIG7_14_USMANAVG.parquet"


def _sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run() -> dict:
    # Returns-precedence guard: human-guided file supersedes machine consensus.
    if RETURNS.exists():
        src, provenance, superseding = RETURNS, "human_guided", True
        rescale = False  # a human return is assumed already in canonical decimal scale
    elif CONSENSUS.exists():
        src, provenance, superseding = CONSENSUS, "machine_digitized", False
        rescale = True   # machine consensus is in percent; convert to decimal
    else:
        return {"status": "FAIL", "sid": SERIES_ID,
                "error": f"no digitized source found (checked {RETURNS} then {CONSENSUS})"}

    df = pd.read_csv(src)
    value = df["value"].astype(float)
    if rescale:
        # percent -> decimal rate of profit; round to 4 dp (source is 2-dp percent),
        # a display-precision clean-up only (no smoothing/interpolation).
        value = (value / 100.0).round(4)

    long_df = pd.DataFrame({
        "year": df["year"].astype(int),
        "value": value,
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
        "units_transform": "percent/100 -> decimal" if rescale else "none (already decimal)",
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
        print(f"[L01_S704] SUPERSESSION: {log['supersession']}")
    else:
        print("[L01_S704] loaded machine digitization consensus "
              "(no returns/ human-guided file present); percent -> decimal.")
    return log


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))

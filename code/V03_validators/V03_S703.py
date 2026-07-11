"""V03_S703 — validate the digitized WORLDAVG aggregate line (Fig 7.13 average panel).

Three independent certifications (this is NOT a tautological round-trip against the same
book workbook the loader read — there is no book table; the source is the digitized figure):

1. Round-trip fidelity — the processed parquet reproduces the durable consensus source
   (machine/S703_consensus.csv) exactly (loader + processor are lossless).
2. REFERENCE_VALUES — three well-separated consensus vertices (start / trough / end) asserted
   against the processed output; these mirror registry validation.reference_values (Decision
   0002; doctor P32).
3. Level plausibility (MHR §5 economic sanity) — every WORLDAVG rate lies inside the printed
   0-0.45 decimal axis, and inside the [0.10, 0.20] band the figure actually occupies; no
   impossible values.

Validation records (viewed evidence): machine/S703_consensus_overlay.png (consensus curve
composited on the figure) and machine/M3_verify_report.md (adversarial verification: CONFIRMED,
no point refuted). The registry validation block additionally wires this series into the
Decision-0011 independent-anchor suite (code/run_anchor_suite.py).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd  # noqa: E402

from utils.paths import TECHNICAL, DATA_PROCESSED  # noqa: E402

SERIES_ID = "S703"
SUBSERIES_ID = "S703-A"
VALIDATOR_TOL_PCT = 1.0

PROCESSED = DATA_PROCESSED / f"{SERIES_ID}.parquet"
_PACKET = TECHNICAL / "remediation_campaign" / "digitization_packet"
CONSENSUS = _PACKET / "machine" / "S703_consensus.csv"

# 3 well-separated consensus vertices (decimal). Mirrors registry validation.reference_values.
REFERENCE_VALUES = {1970: 0.1455, 1982: 0.119, 1990: 0.1562}

# Plausibility (MHR §5): printed axis band and the band the WORLDAVG line occupies.
AXIS_MIN, AXIS_MAX = 0.0, 0.45
BAND_MIN, BAND_MAX = 0.10, 0.20

VALIDATION_RECORDS = [
    "remediation_campaign/digitization_packet/machine/S703_consensus_overlay.png",
    "remediation_campaign/digitization_packet/machine/M3_verify_report.md",
    "remediation_campaign/digitization_packet/machine/M2_adjudication_log.md",
]


def run() -> dict:
    if not PROCESSED.exists():
        return {"status": "FAIL", "sid": SERIES_ID, "error": f"processed missing: {PROCESSED}"}
    df = pd.read_parquet(PROCESSED)
    df = df[df["subseries_id"] == SUBSERIES_ID][["year", "value"]].copy()
    df["year"] = df["year"].astype(int)
    vals = dict(zip(df["year"], df["value"].astype(float)))
    checks: dict[str, object] = {}

    # 1) Round-trip vs durable consensus source (decimal, exact).
    src = pd.read_csv(CONSENSUS)
    src_map = dict(zip(src["year"].astype(int), src["value"].astype(float)))
    rt_bad = [f"{y}: proc={vals.get(y)} src={v}" for y, v in src_map.items()
              if y not in vals or abs(vals[y] - v) > 1e-9]
    checks["round_trip"] = "PASS" if not rt_bad else rt_bad

    # 2) Reference values (3 well-separated vertices).
    ref_bad = []
    for y, exp in REFERENCE_VALUES.items():
        got = vals.get(y)
        if got is None or abs(got - exp) > abs(exp) * (VALIDATOR_TOL_PCT / 100.0):
            ref_bad.append(f"{y}: expected {exp}, got {got}")
    checks["reference_values"] = "PASS" if not ref_bad else ref_bad

    # 3) Plausibility — axis range + occupied band.
    axis_bad = [f"{y}={v}" for y, v in vals.items() if not (AXIS_MIN <= v <= AXIS_MAX)]
    band_bad = [f"{y}={v}" for y, v in vals.items() if not (BAND_MIN <= v <= BAND_MAX)]
    checks["axis_range_0_0.45"] = "PASS" if not axis_bad else axis_bad
    checks["occupied_band_0.10_0.20"] = "PASS" if not band_bad else band_bad

    ok = all(v == "PASS" for v in checks.values())
    return {
        "status": "PASS" if ok else "FAIL",
        "sid": SERIES_ID,
        "n_points": int(len(df)),
        "year_range": [int(df["year"].min()), int(df["year"].max())],
        "checks": checks,
        "provenance": "machine_digitized (dual independent extraction, crop-level adjudication, "
                      "adversarial verification 2026-07-02)",
        "validation_records": VALIDATION_RECORDS,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))

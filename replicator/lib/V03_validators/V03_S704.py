"""V03_S704 — validate the digitized USMANAVG aggregate line (Fig 7.14 average panel).

Independent certifications (no book table exists — the source is the digitized figure):

1. Round-trip fidelity — the processed parquet reproduces the durable consensus source
   (machine/S704_consensus.csv) after the documented percent->decimal conversion (loader +
   processor lossless).
2. REFERENCE_VALUES — three well-separated consensus vertices (peak 1965 / trough 1982 /
   end 1989) asserted against the processed output; mirror registry validation.reference_values
   (doctor P32).
3. Level plausibility (MHR §5) — every value inside the printed axis (-10..60% => -0.10..0.60
   decimal) and inside the [0.05, 0.30] band the USMANAVG line occupies; plus the STRUCTURAL
   fact the verifier used to certify the x-registration: trough(1982) < peak(1965).

Validation records (viewed evidence): machine/S704_consensus_overlay.png, machine/
M3_verify_report.md (adversarial verifier independently rebuilt the x-calibration and CONFIRMED
extractor-A's registration; the extractor-B +1yr shift is documented and rejected), machine/
M2_adjudication_log.md, and machine/S704_1990_omission_ruling.md (why the 1990 column is
omitted). Wired into the Decision-0011 anchor suite via the registry validation block.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd  # noqa: E402

from utils.paths import TECHNICAL, DATA_PROCESSED  # noqa: E402

SERIES_ID = "S704"
SUBSERIES_ID = "S704-A"
VALIDATOR_TOL_PCT = 1.0

PROCESSED = DATA_PROCESSED / f"{SERIES_ID}.parquet"
_PACKET = TECHNICAL / "remediation_campaign" / "digitization_packet"
CONSENSUS = _PACKET / "machine" / "S704_consensus.csv"

# 3 well-separated consensus vertices (DECIMAL). Mirrors registry validation.reference_values.
REFERENCE_VALUES = {1965: 0.2531, 1982: 0.1038, 1989: 0.1375}

# Plausibility (MHR §5): printed axis -10..60% => decimal; occupied band; structural peak/trough.
AXIS_MIN, AXIS_MAX = -0.10, 0.60
BAND_MIN, BAND_MAX = 0.05, 0.30
PEAK_YEAR, TROUGH_YEAR = 1965, 1982

VALIDATION_RECORDS = [
    "remediation_campaign/digitization_packet/machine/S704_consensus_overlay.png",
    "remediation_campaign/digitization_packet/machine/M3_verify_report.md",
    "remediation_campaign/digitization_packet/machine/M2_adjudication_log.md",
    "remediation_campaign/digitization_packet/machine/S704_1990_omission_ruling.md",
]


def run() -> dict:
    if not PROCESSED.exists():
        return {"status": "FAIL", "sid": SERIES_ID, "error": f"processed missing: {PROCESSED}"}
    df = pd.read_parquet(PROCESSED)
    df = df[df["subseries_id"] == SUBSERIES_ID][["year", "value"]].copy()
    df["year"] = df["year"].astype(int)
    vals = dict(zip(df["year"], df["value"].astype(float)))
    checks: dict[str, object] = {}

    # 1) Round-trip vs durable consensus source (percent/100 -> decimal, exact).
    src = pd.read_csv(CONSENSUS)
    src_map = {int(y): float(v) / 100.0 for y, v in zip(src["year"], src["value"])}
    rt_bad = [f"{y}: proc={vals.get(y)} src={v}" for y, v in src_map.items()
              if y not in vals or abs(vals[y] - v) > 1e-9]
    checks["round_trip"] = "PASS" if not rt_bad else rt_bad

    # 2) Reference values.
    ref_bad = []
    for y, exp in REFERENCE_VALUES.items():
        got = vals.get(y)
        if got is None or abs(got - exp) > abs(exp) * (VALIDATOR_TOL_PCT / 100.0):
            ref_bad.append(f"{y}: expected {exp}, got {got}")
    checks["reference_values"] = "PASS" if not ref_bad else ref_bad

    # 3) Plausibility — axis range, occupied band, structural trough<peak.
    axis_bad = [f"{y}={v}" for y, v in vals.items() if not (AXIS_MIN <= v <= AXIS_MAX)]
    band_bad = [f"{y}={v}" for y, v in vals.items() if not (BAND_MIN <= v <= BAND_MAX)]
    checks["axis_range_-0.10_0.60"] = "PASS" if not axis_bad else axis_bad
    checks["occupied_band_0.05_0.30"] = "PASS" if not band_bad else band_bad
    structural = (TROUGH_YEAR in vals and PEAK_YEAR in vals
                  and vals[TROUGH_YEAR] < vals[PEAK_YEAR])
    checks["structure_trough1982_lt_peak1965"] = "PASS" if structural else (
        f"trough({TROUGH_YEAR})={vals.get(TROUGH_YEAR)} !< peak({PEAK_YEAR})={vals.get(PEAK_YEAR)}")

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

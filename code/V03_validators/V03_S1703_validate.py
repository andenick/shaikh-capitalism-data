"""V03_S1703_validate - validate S1703 against Appendix17_USIRS2011.xlsx col F.

Top-3% (midpoint >= $200k). Drops $10M+ open-ended bin (no midpoint).
Spot-checks the Phase-4-ratified column-F values:
  350000   -> 0.00618
  750000   -> 0.00207
  1250000  -> 0.001142
  1750000  -> 0.000757
  3500009  -> 0.000211
  7500000  -> 0.0000787
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils import paths  # noqa: E402
from utils.paths import DATA_PROCESSED, book_data_path  # noqa: E402

SERIES_ID = "S1703"
VALIDATOR_TOL_PCT = 1.0   # slightly looser: open-tail bins are noisy
PROCESSED = DATA_PROCESSED / f"{SERIES_ID}.parquet"
TRUTH_XLSX = book_data_path("Appendix17_USIRS2011.xlsx")
REPORT = paths.TECHNICAL / "VALIDATION_REPORT.json"


def _update_report(row: dict) -> None:
    rpt = (json.loads(REPORT.read_text(encoding="utf-8"))
           if REPORT.exists() else
           {"schema_version": "anu-validation-v1.0", "series": {}})
    rpt["generated_at"] = datetime.now(timezone.utc).isoformat()
    rpt.setdefault("series", {})[SERIES_ID] = row
    REPORT.write_text(json.dumps(rpt, indent=2, default=str), encoding="utf-8")


def run() -> dict:
    if not PROCESSED.exists():
        return {"status": "FAIL", "error": f"processed missing: {PROCESSED}"}

    actual = pd.read_parquet(PROCESSED)
    truth = pd.read_excel(TRUTH_XLSX, header=1)
    truth = truth.rename(columns={
        "Bin": "agi_midpoint_usd",
        "Cumulative Frequency from Above": "expected",
    })
    truth = truth.dropna(subset=["agi_midpoint_usd"]).copy()
    truth["agi_midpoint_usd"] = pd.to_numeric(truth["agi_midpoint_usd"], errors="coerce")
    truth = truth.dropna(subset=["agi_midpoint_usd"])
    truth = truth[truth["agi_midpoint_usd"] >= 200_000][["agi_midpoint_usd", "expected"]]
    truth = truth[truth["expected"] > 0]

    merged = actual.merge(truth, on="agi_midpoint_usd", how="inner")
    merged["abs_err"] = (merged["value"] - merged["expected"]).abs()
    merged["pct_err"] = merged["abs_err"] / merged["expected"].abs() * 100.0
    divs = merged[merged["pct_err"] > VALIDATOR_TOL_PCT][[
        "agi_midpoint_usd", "value", "expected", "pct_err"]].to_dict("records")

    spot = {350000: 0.00618, 750000: 0.00207, 1250000: 0.001142,
            1750000: 0.000757, 3500009: 0.000211, 7500000: 0.0000787}
    spot_check = {}
    for mp, exp in spot.items():
        found = actual[abs(actual["agi_midpoint_usd"] - mp) < 1e-3]
        if len(found):
            got = float(found["value"].iloc[0])
            spot_check[str(mp)] = {"expected": exp, "got": round(got, 6),
                                    "diff_pct": round(abs(got - exp) / exp * 100.0, 4)}
        else:
            spot_check[str(mp)] = {"expected": exp, "got": None}

    n = int(len(merged))
    status = "PASS" if not divs else "FAIL"

    # Drop confirmation
    has_10m = bool((actual["agi_label"].astype(str).str.contains("10,000,000")).any())

    row = {
        "status": status,
        "tolerance_pct": VALIDATOR_TOL_PCT,
        "content_type": "cross_sectional",
        "comparison_basis": "Appendix17_USIRS2011.xlsx 'Cumulative Frequency from Above' (FPR017_C5), midpoint >= $200k",
        "n_compared": n,
        "mae": round(float(merged["abs_err"].mean()) if n else 0.0, 6),
        "max_pct_err": round(float(merged["pct_err"].max()) if n else 0.0, 6),
        "divergence_count": len(divs),
        "divergences": divs[:10],
        "spot_check_phase4": spot_check,
        "column_fix": "FPR017_C3 (Frequency) -> FPR017_C5 (Cumulative from Above) applied",
        "top_bin_dropped": True,
        "top_bin_drop_audit": ("$10,000,000+ open-ended bin has no midpoint; "
                                "dropped per anti-synthetic rule. Loader filters NaN midpoint."),
        "ten_million_bin_present_in_processed": has_10m,
        "cd2_comparison": {"note": "CD2 S104 reference_values were the Frequency column; corrected to column F here."},
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    _update_report(row)
    return row


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))

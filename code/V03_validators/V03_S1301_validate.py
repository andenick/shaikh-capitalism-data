"""V03_S1301_validate - theoretical pass-through; returns PASS_THEORETICAL.

Fig 13.7 has no calendar axis and no observed data. Validation confirms:
  (1) Processed parquet exists.
  (2) Both subseries (S1301-EQ trend + S1301-ACTUAL realization) are present.
  (3) The equilibrium trend has the declared slope alpha = 0.03.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils import paths  # noqa: E402
from utils.paths import DATA_PROCESSED  # noqa: E402

SERIES_ID = "S1301"
PROCESSED = DATA_PROCESSED / f"{SERIES_ID}.parquet"
REPORT = paths.TECHNICAL / "VALIDATION_REPORT.json"
ALPHA_EXPECTED = 0.03
ALPHA_TOL = 1e-9


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
    df = pd.read_parquet(PROCESSED)

    subs = set(df["subseries_id"].unique())
    have_both = {"S1301-EQ", "S1301-ACTUAL"}.issubset(subs)

    eq = df[df["subseries_id"] == "S1301-EQ"].sort_values("year")
    slope_ok = False
    if len(eq) >= 2:
        slope = (eq["value"].iloc[-1] - eq["value"].iloc[0]) / (eq["year"].iloc[-1] - eq["year"].iloc[0])
        slope_ok = abs(slope - ALPHA_EXPECTED) < ALPHA_TOL

    status = "PASS_THEORETICAL" if (have_both and slope_ok) else "FAIL"

    row = {
        "status": status,
        "tolerance_pct": None,
        "content_type": "theoretical",
        "comparison_basis": "Fig 13.7 is an analytical schematic of eq. 13.43; verification "
                             "is structural (subseries present + trend slope = alpha).",
        "n_compared": int(len(df)),
        "subseries_present": sorted(subs),
        "trend_slope_check": {"expected_alpha": ALPHA_EXPECTED, "ok": slope_ok},
        "parameter_disclosure": {
            "ln_Y0": 8.0, "alpha": 0.03, "sigma_epsilon": 0.015, "seed": 42, "t_max": 75,
            "note": "Shaikh does not publish parameters; values declared in EPR.",
        },
        "divergence_count": 0,
        "cd2_comparison": {"note": "no CD/CD2 predecessor (Fig 13.7 is illustrative)"},
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    _update_report(row)
    return row


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))

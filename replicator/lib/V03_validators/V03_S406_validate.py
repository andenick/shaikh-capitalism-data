"""V03_S406_validate — data_unavailable; same posture as S404."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils import paths  # noqa: E402

SERIES_ID = "S406"
REPORT = paths.TECHNICAL / "VALIDATION_REPORT.json"
DPR = paths.DOCS_SERIES / f"{SERIES_ID}_DPR.md"


def _update_report(row: dict) -> None:
    if REPORT.exists():
        rpt = json.loads(REPORT.read_text(encoding="utf-8"))
    else:
        rpt = {"schema_version": "anu-validation-v1.0", "series": {}}
    rpt["generated_at"] = datetime.now(timezone.utc).isoformat()
    rpt.setdefault("series", {})[SERIES_ID] = row
    REPORT.write_text(json.dumps(rpt, indent=2, default=str), encoding="utf-8")


def run() -> dict:
    dpr_ok = DPR.exists() and "data_unavailable" in DPR.read_text(encoding="utf-8")
    row = {
        "status": "PASS_DATA_UNAVAILABLE",
        "tolerance_pct": None, "content_type": "derived",
        "comparison_basis": "n/a — Inman 1995 fig. 5 paywalled, figures-only",
        "n_compared": 0, "mae": None, "max_abs_err": None, "max_pct_err": None,
        "divergence_count": 0, "divergences": [],
        "dpr_documents_data_unavailable": dpr_ok,
        "cd2_comparison": {"note": "no CD/CD2 predecessor"},
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    _update_report(row)
    return row


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))

"""V03_S215_validate - book period data_unavailable; PASS with explicit marker."""
from __future__ import annotations
import json, sys
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils import paths  # noqa: E402
from utils.paths import DATA_PROCESSED  # noqa: E402

PROCESSED = DATA_PROCESSED / "S215.parquet"
REPORT = paths.TECHNICAL / "VALIDATION_REPORT.json"


def _update(row: dict) -> None:
    if REPORT.exists():
        rpt = json.loads(REPORT.read_text(encoding="utf-8"))
    else:
        rpt = {"schema_version": "anu-validation-v1.0", "series": {}}
    rpt["generated_at"] = datetime.now(timezone.utc).isoformat()
    rpt.setdefault("series", {})["S215"] = row
    REPORT.write_text(json.dumps(rpt, indent=2, default=str), encoding="utf-8")


def run() -> dict:
    if not PROCESSED.exists():
        return {"status": "FAIL", "error": "processed missing"}
    df = pd.read_parquet(PROCESSED)
    row = {
        "status": "PASS_DATA_UNAVAILABLE",
        "book_period": [1960, 1989],
        "book_period_status": "data_unavailable",
        "reason": "anwarshaikhecon.org App 7.2 / OECD ISDB 1994 not in SalvagedInputs.",
        "post_book_rows": int(len(df)),
        "post_book_range": [int(df["year"].min()), int(df["year"].max())],
        "remediation": "When App 7.2 replica is added to SalvagedInputs, re-run L01.",
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    _update(row)
    return row


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))

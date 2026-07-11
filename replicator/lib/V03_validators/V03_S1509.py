"""V03_S1509 - validate S1509 cell-by-cell against the Ramamurthy chopped table."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils import paths  # noqa: E402
from utils.paths import DATA_PROCESSED, SALVAGED_BOOK_DATA  # noqa: E402
from V03_validators._v03_anchor_lib import (  # noqa: E402
    check_independent_anchor,
    check_level_plausibility,
    check_splice_continuity,
    _load_processed as _load_anchor_processed,
    _load_registry as _load_anchor_registry,
    RED as ANCHOR_RED,
)

PROCESSED = DATA_PROCESSED / "S1509.parquet"
CHOPPED_XLSX = SALVAGED_BOOK_DATA / "ShaikhChoppedTables" / "Appendix15_WorldInflationDataByCountry.xlsx"
REPORT = paths.TECHNICAL / "VALIDATION_REPORT.json"

VALIDATOR_TOL_PCT = 1.0
SERIES_ID = "S1509"


def _truth() -> pd.DataFrame:
    raw = pd.read_excel(CHOPPED_XLSX, sheet_name="Ramamurthy2013", header=1)
    df = pd.DataFrame({
        "row_index": pd.to_numeric(raw.iloc[:, 0], errors="coerce"),
        "lambda_gDC": pd.to_numeric(raw.iloc[:, 1], errors="coerce"),
        "pi_inflation": pd.to_numeric(raw.iloc[:, 2], errors="coerce"),
        "country": raw.iloc[:, 6].astype(str),
    }).dropna(subset=["row_index"]).astype({"row_index": int})

    rows = []
    for _, r in df.iterrows():
        country_key = f"R{int(r['row_index']):02d}_{r['country'].strip()}"
        if not pd.isna(r["lambda_gDC"]):
            rows.append({"country_key": country_key, "subseries_id": "S1509-lambda",
                         "expected": float(r["lambda_gDC"])})
        if not pd.isna(r["pi_inflation"]):
            rows.append({"country_key": country_key, "subseries_id": "S1509-pi",
                         "expected": float(r["pi_inflation"])})
    return pd.DataFrame(rows)


def _update(row: dict) -> None:
    if REPORT.exists():
        rpt = json.loads(REPORT.read_text(encoding="utf-8"))
    else:
        rpt = {"schema_version": "anu-validation-v1.0", "series": {}}
    rpt["generated_at"] = datetime.now(timezone.utc).isoformat()
    rpt.setdefault("series", {})[SERIES_ID] = row
    REPORT.write_text(json.dumps(rpt, indent=2, default=str), encoding="utf-8")


def _anchor_checks() -> dict:
    """Run the Decision-0011 independent-anchor suite for this series (B2.4 wiring).

    S1509 carries one structural cardinality anchor (count == 46 country-episode rows):
    the printed numeric cells are circular with the loader, so cardinality is the only
    honest independent anchor. Uses the anchor library's own processed loader so the
    wired verdict matches the standalone suite. A RED on any check must FAIL the validator.
    """
    registry = _load_anchor_registry()
    adf = _load_anchor_processed(SERIES_ID)
    anchors = check_independent_anchor(SERIES_ID, adf, registry)
    splice = check_splice_continuity(SERIES_ID, adf, registry)
    plausibility = check_level_plausibility(SERIES_ID, adf, registry)
    any_red = ANCHOR_RED in (anchors["status"], splice["status"], plausibility["status"])
    return {
        "status": ANCHOR_RED if any_red else "GREEN",
        "any_red": any_red,
        "anchors": anchors,
        "splice": splice,
        "plausibility": plausibility,
    }


def run() -> dict:
    if not PROCESSED.exists():
        return {"status": "FAIL", "error": f"processed missing: {PROCESSED}"}
    actual = pd.read_parquet(PROCESSED)
    truth = _truth()
    merged = actual.merge(truth, on=["country_key", "subseries_id"], how="inner")
    merged["abs_err"] = (merged["value"] - merged["expected"]).abs()
    merged["pct_err"] = merged["abs_err"] / merged["expected"].abs().clip(lower=1e-9) * 100.0
    n = int(len(merged))
    mae = float(merged["abs_err"].mean()) if n else float("nan")
    max_abs = float(merged["abs_err"].max()) if n else float("nan")
    max_pct = float(merged["pct_err"].max()) if n else float("nan")
    bad = merged[(merged["abs_err"] > 1e-6) & (merged["pct_err"] > VALIDATOR_TOL_PCT)]
    status = "PASS" if bad.empty else "FAIL"

    # --- Independent-anchor checks (Decision 0011 / B2.4): a RED anchor FAILs V03 ---
    anchor = _anchor_checks()
    if anchor["any_red"]:
        status = "FAIL"

    row = {
        "status": status,
        "tolerance_pct": VALIDATOR_TOL_PCT,
        "n_compared": n,
        "n_country_episodes": int(merged["country_key"].nunique()),
        "mae": round(mae, 10),
        "max_abs_err": round(max_abs, 10),
        "max_pct_err": round(max_pct, 6),
        "divergence_count": int(len(bad)),
        "content_type": "cross_sectional",
        "independent_anchors": anchor,
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    _update(row)
    return row


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))

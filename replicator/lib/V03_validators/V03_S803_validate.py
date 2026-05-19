"""V03_S803_validate — validate S803 against Bain 1951 and Demsetz 1973b chopped xlsx.

Three panels validated separately, then combined into a single status row.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_PROCESSED, SALVAGED_BOOK_DATA  # noqa: E402
from V03_validators._ch8_validator_lib import update_report  # noqa: E402

SERIES_ID = "S803"
VALIDATOR_TOL_PCT = 0.5  # cross_sectional per playbook

PROCESSED = DATA_PROCESSED / f"{SERIES_ID}.parquet"
XLSX_FIG83 = SALVAGED_BOOK_DATA / "ShaikhChoppedTables" / "Appendix8_Bain42IndustryProfit.xlsx"
XLSX_FIG84_BAIN = SALVAGED_BOOK_DATA / "ShaikhChoppedTables" / "Appendix8_Bain42IndustryAggregates.xlsx"
XLSX_FIG84_DEMSETZ = SALVAGED_BOOK_DATA / "ShaikhChoppedTables" / "Appendix8_CorrectedBainData.xlsx"

YEAR_LABEL = 1938


def _truth_fig83() -> pd.DataFrame:
    raw = pd.read_excel(XLSX_FIG83, sheet_name="Sheet1", header=None)
    industries = [str(c).strip() for c in raw.iloc[1, 1:].tolist()]
    census_nums = raw.iloc[2, 1:].tolist()
    cr8_vals = raw.iloc[3, 1:].tolist()
    roe_vals = raw.iloc[4, 1:].tolist()
    rows = []
    for ind, census, cr, roe in zip(industries, census_nums, cr8_vals, roe_vals):
        if pd.isna(cr) or pd.isna(roe):
            continue
        rows.append({"industry": str(ind).strip(), "census_number": str(census),
                     "axis": "CR8", "expected": float(cr)})
        rows.append({"industry": str(ind).strip(), "census_number": str(census),
                     "axis": "ROE", "expected": float(roe)})
    return pd.DataFrame(rows)


def _truth_fig84_bain() -> pd.DataFrame:
    raw = pd.read_excel(XLSX_FIG84_BAIN, sheet_name="Sheet1", header=None)
    data = raw.iloc[2:12, :5].reset_index(drop=True)
    data.columns = ["decile_index", "cr_lower", "cr_upper", "n_industries", "mean_roe"]
    data = data.dropna(subset=["mean_roe"]).reset_index(drop=True)
    return pd.DataFrame({
        "decile_index": data["decile_index"].astype(int),
        "expected": data["mean_roe"].astype(float),
    })


def _truth_fig84_demsetz() -> pd.DataFrame:
    raw = pd.read_excel(XLSX_FIG84_DEMSETZ, sheet_name="Sheet1", header=None)
    data = raw.iloc[2:, :2].reset_index(drop=True)
    data.columns = ["cr8_midpoint", "mean_roe"]
    data = data.dropna(subset=["mean_roe"]).reset_index(drop=True)
    return pd.DataFrame({
        "cr8_midpoint": data["cr8_midpoint"].astype(int),
        "expected": data["mean_roe"].astype(float),
    })


def _compare(actual: pd.DataFrame, truth: pd.DataFrame, keys: list[str]) -> dict:
    merged = actual.merge(truth, on=keys, how="inner")
    merged["abs_err"] = (merged["value"] - merged["expected"]).abs()
    safe_denom = merged["expected"].abs().replace(0, pd.NA)
    merged["pct_err"] = (merged["abs_err"] / safe_denom * 100.0).fillna(0.0)
    bad = merged[(merged["abs_err"] > 1e-6) & (merged["pct_err"] > VALIDATOR_TOL_PCT)]
    return {
        "n_compared": int(len(merged)),
        "mae": float(merged["abs_err"].mean()) if len(merged) else float("nan"),
        "max_abs_err": float(merged["abs_err"].max()) if len(merged) else float("nan"),
        "max_pct_err": float(merged["pct_err"].max()) if len(merged) else float("nan"),
        "divergence_count": int(len(bad)),
    }


def run() -> dict:
    if not PROCESSED.exists():
        row = {"status": "FAIL", "error": f"processed missing: {PROCESSED}",
               "validated_at": datetime.now(timezone.utc).isoformat()}
        update_report(SERIES_ID, row)
        return row

    actual = pd.read_parquet(PROCESSED)
    panels = {}

    a83 = actual[actual["subseries_id"] == "S803-FIG83"]
    panels["FIG83"] = _compare(a83, _truth_fig83(), ["industry", "census_number", "axis"])

    a84b = actual[actual["subseries_id"] == "S803-FIG84-BAIN"]
    panels["FIG84_BAIN"] = _compare(a84b, _truth_fig84_bain(), ["decile_index"])

    a84d = actual[actual["subseries_id"] == "S803-FIG84-DEMSETZ"]
    panels["FIG84_DEMSETZ"] = _compare(a84d, _truth_fig84_demsetz(), ["cr8_midpoint"])

    total_div = sum(p["divergence_count"] for p in panels.values())
    total_n = sum(p["n_compared"] for p in panels.values())
    overall_max_pct = max(p["max_pct_err"] for p in panels.values()) if panels else float("nan")
    overall_max_abs = max(p["max_abs_err"] for p in panels.values()) if panels else float("nan")
    overall_mae = sum(p["mae"] * p["n_compared"] for p in panels.values()) / total_n if total_n else float("nan")

    status = "PASS" if total_div == 0 else "FAIL"
    row = {
        "status": status,
        "tolerance_pct": VALIDATOR_TOL_PCT,
        "content_type": "cross_sectional",
        "n_compared": total_n,
        "mae": round(overall_mae, 10),
        "max_abs_err": round(overall_max_abs, 10),
        "max_pct_err": round(overall_max_pct, 6),
        "divergence_count": total_div,
        "panels": panels,
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    update_report(SERIES_ID, row)
    return row


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))

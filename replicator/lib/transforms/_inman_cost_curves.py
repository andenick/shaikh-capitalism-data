"""Shared logic for the Inman (1995) automotive cost-vs-output curves (S404-S407),
digitized from Shaikh 2016 Figs 4.19-4.22 (native-resolution polyline trace, overlay-validated).

These are functional curves y(cost) = f(x=annual vehicle output, thousands), not time series.
Following the Ch3 functional-curve precedent (S308): `year` is a 1-based point index and the
real x lives in an `x_value` column (preserved in the processed parquet; the generic chopped
writer keys on year). Provenance: Technical/WL1_Tsoulfidis_Tsaliki/EXTRACTION_REPORT.md.
"""
from __future__ import annotations

import json as _json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, DATA_PROCESSED, SALVAGED_BOOK_DATA, TECHNICAL  # noqa: E402
from L01_loaders._ch3_helpers import make_curve_frame  # noqa: E402

SOURCE = SALVAGED_BOOK_DATA / "Reconstructed" / "Inman_1995_S404-407_cost_curves.json"
SUBSOURCE = "INMAN_1995_ENGINEERING_ECONOMIST"
UNITS = {
    "S404": "USD per car vs annual vehicle production (thousands)",
    "S405": "USD per additional car vs annual vehicle production (thousands)",
    "S406": "USD per car vs annual vehicle production (thousands)",
    "S407": "USD per additional car vs annual vehicle production (thousands)",
}
REPORT = TECHNICAL / "VALIDATION_REPORT.json"


def _curve(sid: str):
    d = _json.load(open(SOURCE, encoding="utf-8"))[sid]["curve_native"]
    pts = sorted(((float(p["output"]), float(p["value"])) for p in d), key=lambda z: z[0])
    return [x for x, _ in pts], [y for _, y in pts]


def load(sid: str) -> dict:
    if not SOURCE.exists():
        return {"status": "FAIL", "error": f"digitized source missing: {SOURCE}"}
    x, y = _curve(sid)
    df = make_curve_frame(np.array(x), np.array(y), subseries_id=f"{sid}-A",
                          subsource_id=SUBSOURCE, units=UNITS[sid])
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    out = DATA_RAW / f"{sid}_INMAN.parquet"
    df.to_parquet(out, index=False)
    return {"status": "OK", "rows_loaded": int(len(df)),
            "x_range": [min(x), max(x)], "sources_fetched": [SUBSOURCE], "output": str(out)}


def process(sid: str) -> dict:
    IN = DATA_RAW / f"{sid}_INMAN.parquet"
    if not IN.exists():
        return {"status": "FAIL", "error": f"raw missing: {IN}"}
    df = pd.read_parquet(IN).rename(columns={"subsource_id": "source_id"})
    df = df[["year", "x_value", "value", "subseries_id", "source_id", "units"]]
    df = df.sort_values(["subseries_id", "x_value"]).reset_index(drop=True)
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    out = DATA_PROCESSED / f"{sid}.parquet"
    df.to_parquet(out, index=False)
    return {"status": "OK", "rows_processed": int(len(df)), "output": str(out)}


def validate(sid: str) -> dict:
    proc = DATA_PROCESSED / f"{sid}.parquet"
    if not proc.exists():
        return {"status": "FAIL", "error": f"processed missing: {proc}"}
    df = pd.read_parquet(proc)
    _, y = _curve(sid)
    errs = [abs(a - b) for a, b in zip(df["value"].tolist(), y)]
    mx = max(errs) if errs else 0.0
    mae = sum(errs) / len(errs) if errs else 0.0
    row = {"status": "PASS" if mx < 0.01 else "FAIL",
           "n_compared": int(len(df)), "mae": round(mae, 8), "max_abs_err": round(mx, 8),
           "content_type": "derived", "is_digitized": True,
           "validated_at": datetime.now(timezone.utc).isoformat()}
    rpt = _json.load(open(REPORT, encoding="utf-8")) if REPORT.exists() else {"schema_version": "anu-validation-v1.0", "series": {}}
    rpt.setdefault("series", {})[sid] = row
    rpt["generated_at"] = datetime.now(timezone.utc).isoformat()
    _json.dump(rpt, open(REPORT, "w", encoding="utf-8"), indent=2, default=str)
    return row

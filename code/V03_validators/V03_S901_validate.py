"""V03_S901_validate - validate normalized market/direct prices per industry per benchmark."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils import paths  # noqa: E402
from utils.paths import DATA_PROCESSED  # noqa: E402
from L01_loaders._ch9_helpers import (  # noqa: E402
    APPENDIX9_BENCHMARKS, read_benchmark, normalize_industry_frame,
)

PROCESSED = DATA_PROCESSED / "S901.parquet"
REPORT = paths.TECHNICAL / "VALIDATION_REPORT.json"
VALIDATOR_TOL_PCT = 0.5


def _truth() -> dict[str, pd.DataFrame]:
    out = {}
    for (year, label, filename, _, _) in APPENDIX9_BENCHMARKS:
        try:
            df = read_benchmark(filename)
        except Exception:
            continue
        norm = normalize_industry_frame(df)
        out[label] = norm[["Index", "tpm_norm", "td_norm", "tv_norm"]].rename(
            columns={"Index": "industry_index"})
    return out


def _update(row: dict) -> None:
    if REPORT.exists():
        rpt = json.loads(REPORT.read_text(encoding="utf-8"))
    else:
        rpt = {"schema_version": "anu-validation-v1.0", "series": {}}
    rpt["generated_at"] = datetime.now(timezone.utc).isoformat()
    rpt.setdefault("series", {})["S901"] = row
    REPORT.write_text(json.dumps(rpt, indent=2, default=str), encoding="utf-8")


def run() -> dict:
    if not PROCESSED.exists():
        return {"status": "FAIL", "error": "processed missing"}
    actual = pd.read_parquet(PROCESSED)
    truths = _truth()

    per_benchmark = []
    total_div = 0
    overall_mae = []
    mawd_diag = {}
    for label, t in truths.items():
        a_market = actual[actual["subseries_id"] == f"S901-A_{label}"]
        a_direct = actual[actual["subseries_id"] == f"S901-B_{label}"]
        m1 = a_market.merge(t[["industry_index", "tpm_norm"]],
                            on="industry_index", how="inner")
        m2 = a_direct.merge(t[["industry_index", "td_norm"]],
                            on="industry_index", how="inner")
        for m, col in [(m1, "tpm_norm"), (m2, "td_norm")]:
            m["abs_err"] = (m["value"] - m[col]).abs()
            m["pct_err"] = m["abs_err"] / m[col].abs() * 100.0
        div_market = m1[m1["pct_err"] > VALIDATOR_TOL_PCT]["industry_index"].astype(int).tolist()
        div_direct = m2[m2["pct_err"] > VALIDATOR_TOL_PCT]["industry_index"].astype(int).tolist()
        total_div += len(div_market) + len(div_direct)
        if len(m1):
            overall_mae.append(float(m1["abs_err"].mean()))
        if len(m2):
            overall_mae.append(float(m2["abs_err"].mean()))

        # %MAWD diagnostic (Ochoa 1984): Σ |tpm - td|·tv_norm
        mawd = float((t["tpm_norm"] - t["td_norm"]).abs().mul(t["tv_norm"]).sum())
        mawd_diag[label] = round(mawd * 100.0, 4)  # express in percent

        per_benchmark.append({
            "label": label, "n_industries": int(t["industry_index"].nunique()),
            "market_mae": round(float(m1["abs_err"].mean()) if len(m1) else 0.0, 10),
            "market_max_pct_err": round(float(m1["pct_err"].max()) if len(m1) else 0.0, 10),
            "market_divergences": div_market,
            "direct_mae": round(float(m2["abs_err"].mean()) if len(m2) else 0.0, 10),
            "direct_max_pct_err": round(float(m2["pct_err"].max()) if len(m2) else 0.0, 10),
            "direct_divergences": div_direct,
        })

    status = "PASS" if total_div == 0 else "FAIL"
    row = {
        "status": status, "tolerance_pct": VALIDATOR_TOL_PCT,
        "per_benchmark": per_benchmark,
        "mae": round(sum(overall_mae) / max(1, len(overall_mae)), 10),
        "%MAWD_per_benchmark_percent": mawd_diag,
        "validated_at": datetime.now(timezone.utc).isoformat(),
    }
    _update(row)
    return row


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))

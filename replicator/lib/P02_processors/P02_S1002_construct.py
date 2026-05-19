"""P02_S1002_construct — assemble S1002.

Book period: pass-through of USLR iblong (yield) and USWPI (PPI).
Extension: append FRED AAA (post-2011) as S1002-C; FRED PPIACO rebased to
USWPI[2011] anchor as S1002-D.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

IN_A = DATA_RAW / "S1002_USLR_iblong.parquet"
IN_B = DATA_RAW / "S1002_USLR_USWPI.parquet"
IN_C = DATA_RAW / "S1002_FRED_AAA.parquet"
IN_D = DATA_RAW / "S1002_FRED_PPIACO.parquet"
OUT = DATA_PROCESSED / "S1002.parquet"

ANCHOR_YEAR = 2011


def run() -> dict:
    if not (IN_A.exists() and IN_B.exists()):
        return {"status": "FAIL", "error": "book parquet missing",
                "missing": [str(p) for p in (IN_A, IN_B) if not p.exists()]}
    a = pd.read_parquet(IN_A)
    b = pd.read_parquet(IN_B)

    parts = [a, b]
    diag: dict = {"extension_status": "book_only"}

    if IN_C.exists():
        c = pd.read_parquet(IN_C)
        # restrict to years > 2011 (book ends 2011)
        c_ext = c[c["year"] > ANCHOR_YEAR].copy()
        c_ext["units"] = "percent"
        parts.append(c_ext)
        diag["aaa_ext_years"] = int(len(c_ext))

    if IN_D.exists():
        d = pd.read_parquet(IN_D)
        # Reindex PPIACO to USWPI base via 2011 overlap
        try:
            uswpi_2011 = float(b.loc[b["year"] == ANCHOR_YEAR, "value"].iloc[0])
            ppiaco_2011 = float(d.loc[d["year"] == ANCHOR_YEAR, "value"].iloc[0])
            if ppiaco_2011 == 0:
                raise ValueError("PPIACO 2011 is zero")
            scale = uswpi_2011 / ppiaco_2011
            d_ext = d[d["year"] > ANCHOR_YEAR].copy()
            d_ext["value"] = d_ext["value"] * scale
            d_ext["units"] = "index_1947=100"
            parts.append(d_ext)
            diag["ppiaco_scale_factor"] = scale
            diag["ppiaco_ext_years"] = int(len(d_ext))
        except Exception as exc:
            diag["ppiaco_ext_error"] = str(exc)

    if len(parts) > 2:
        diag["extension_status"] = "ok"

    df = pd.concat(parts, ignore_index=True).rename(columns={"subsource_id": "source_id"})
    df = df.sort_values(["year", "subseries_id"]).reset_index(drop=True)
    df = df[["year", "value", "subseries_id", "source_id", "units"]]
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False)

    return {
        "status": "OK",
        "rows_processed": int(len(df)),
        "year_range": [int(df["year"].min()), int(df["year"].max())],
        "subseries_present": sorted(df["subseries_id"].unique().tolist()),
        "extension": diag,
        "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))

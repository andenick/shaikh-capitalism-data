"""P02_S208_construct - emit Shaikh's published RULC for book period,
and (where S207 extension is available) recompute the formula post-2010.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

IN_BOOK = DATA_RAW / "S208_BOOK_RULC.parquet"
IN_S207 = DATA_PROCESSED / "S207.parquet"
OUT = DATA_PROCESSED / "S208.parquet"


def run() -> dict:
    if not IN_BOOK.exists():
        return {"status": "FAIL", "error": "S208 book raw missing"}
    book = pd.read_parquet(IN_BOOK).rename(columns={"subsource_id": "source_id"})
    book = book[["year", "value", "units", "subseries_id", "source_id"]]
    diag = {"extension_status": "data_unavailable", "reason": "S207 processed missing"}
    parts = [book]
    if IN_S207.exists():
        s207 = pd.read_parquet(IN_S207)
        prod = s207[s207["subseries_id"].isin(["S207-A", "S207-C"])].copy()
        comp = s207[s207["subseries_id"].isin(["S207-B", "S207-D"])].copy()
        # Take post-2010 years where both are available
        ext_years = sorted(set(prod["year"]) & set(comp["year"]) & set(range(2011, 2026)))
        if ext_years:
            ext_rows = []
            for y in ext_years:
                p_val = float(prod.loc[prod["year"] == y, "value"].iloc[0])
                c_val = float(comp.loc[comp["year"] == y, "value"].iloc[0])
                if p_val == 0:
                    continue
                rulc = (c_val / p_val) * 100.0
                ext_rows.append({"year": y, "value": rulc, "units": "index_1889=100",
                                 "subseries_id": "S208-B", "source_id": "RECOMPUTED_FROM_S207_EXT"})
            if ext_rows:
                ext_df = pd.DataFrame(ext_rows)
                # Anchor: rescale extension so 2010 (or last book year) value equals book[2010]
                if 2010 in book["year"].values:
                    anchor_book = float(book.loc[book["year"] == 2010, "value"].iloc[0])
                    if 2010 in {*prod["year"]} and 2010 in {*comp["year"]}:
                        p10 = float(prod.loc[prod["year"] == 2010, "value"].iloc[0])
                        c10 = float(comp.loc[comp["year"] == 2010, "value"].iloc[0])
                        ref_2010 = (c10 / p10) * 100.0 if p10 else None
                        if ref_2010 and ref_2010 > 0:
                            scale = anchor_book / ref_2010
                            ext_df["value"] = ext_df["value"] * scale
                parts.append(ext_df)
                diag = {"extension_status": "ok", "method": "recompute_formula_from_S207",
                        "years_appended": int(len(ext_df)),
                        "last_year": int(ext_df["year"].max())}
            else:
                diag = {"extension_status": "no_valid_ext_year"}
        else:
            diag = {"extension_status": "no_post2010_S207_data"}
    final = pd.concat(parts, ignore_index=True).sort_values("year").reset_index(drop=True)
    final = final[["year", "value", "subseries_id", "source_id", "units"]]
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    final.to_parquet(OUT, index=False)
    return {
        "status": "OK", "rows_processed": int(len(final)),
        "year_range": [int(final["year"].min()), int(final["year"].max())],
        "subseries_present": sorted(final["subseries_id"].unique().tolist()),
        "extension": diag, "output": str(OUT),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))

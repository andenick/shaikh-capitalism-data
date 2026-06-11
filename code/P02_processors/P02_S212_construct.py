"""P02_S212_construct - emit pre-computed WPI-in-gold series (US, UK), 1930=100.

For extension beyond 2010, the proper construction recomputes
WPI_in_gold[t] = WPI[t] / gold_price[t] from S210 components + gold price,
reindexed to 1930=100. We do this approximately by using FRED WPU/GOLDPMGBD
and rescaling to the book's 2010 anchor.
"""
from __future__ import annotations
import sys
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.paths import DATA_RAW, DATA_PROCESSED  # noqa: E402

IN_US = DATA_RAW / "S212_US_WPI_IN_GOLD.parquet"
IN_UK = DATA_RAW / "S212_UK_WPI_IN_GOLD.parquet"
IN_GOLD = DATA_RAW / "S212_FRED_GOLD_PRICE.parquet"
IN_S210 = DATA_PROCESSED / "S210.parquet"
OUT = DATA_PROCESSED / "S212.parquet"
EXT_OVERLAP = 2010


def run() -> dict:
    if not IN_US.exists() or not IN_UK.exists():
        return {"status": "FAIL", "error": "raw missing"}
    us = pd.read_parquet(IN_US).rename(columns={"subsource_id": "source_id"})
    uk = pd.read_parquet(IN_UK).rename(columns={"subsource_id": "source_id"})
    us = us[["year", "value", "units", "subseries_id", "source_id"]]
    uk = uk[["year", "value", "units", "subseries_id", "source_id"]]
    parts = [us, uk]
    diag = {"extension_status": "data_unavailable"}
    # Recompute extension for US: WPI/gold ratio using FRED WPU and FRED gold
    if IN_GOLD.exists() and IN_S210.exists():
        gold = pd.read_parquet(IN_GOLD)
        s210 = pd.read_parquet(IN_S210)
        s210_us = s210[s210["subseries_id"].isin(["S210-A", "S210-C"])]
        # Build merged frame
        post = s210_us[s210_us["year"] > EXT_OVERLAP].merge(
            gold[["year", "value"]].rename(columns={"value": "gold"}), on="year", how="inner")
        if not post.empty:
            # ratio at 2010
            us_book_2010 = float(us.loc[us["year"] == EXT_OVERLAP, "value"].iloc[0]) if EXT_OVERLAP in us["year"].values else None
            s210_us_2010 = s210_us.loc[s210_us["year"] == EXT_OVERLAP, "value"]
            gold_2010 = gold.loc[gold["year"] == EXT_OVERLAP, "value"]
            if (us_book_2010 is not None and len(s210_us_2010) and len(gold_2010)):
                ratio_2010 = float(s210_us_2010.iloc[0]) / float(gold_2010.iloc[0])
                scale = us_book_2010 / ratio_2010
                post = post.copy()
                post["ratio"] = post["value"] / post["gold"]
                post["value_rescaled"] = post["ratio"] * scale
                ext = pd.DataFrame({
                    "year": post["year"], "value": post["value_rescaled"],
                    "units": "index_1930=100", "subseries_id": "S212-C",
                    "source_id": "RECOMPUTED_FRED_WPU_GOLD",
                })
                parts.append(ext)
                diag = {"extension_status": "ok", "country": "US-only",
                        "scale_factor": scale, "years_appended": int(len(ext)),
                        "method": "WPU/gold ratio rescaled to 1930=100 via 2010 anchor"}
    final = pd.concat(parts, ignore_index=True).sort_values(["subseries_id", "year"]).reset_index(drop=True)
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

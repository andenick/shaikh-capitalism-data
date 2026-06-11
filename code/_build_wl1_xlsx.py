"""Build digitized deviation-panel xlsx for S707 (Fig 4) and S708 (Fig 6) from the
WL-1 vector extraction JSON. Output shape matches _ch7_xlsx_panels.read_panel:
row0=title, row1=headers (Year + <industry>_Deviation), rows2+=annual values.
Clipped to 1962-1991 to match Shaikh's Fig 7.19/7.20 captions.
"""
from __future__ import annotations
import json
from pathlib import Path
import pandas as pd
from utils import paths

WL1 = paths.TECHNICAL / "WL1_Tsoulfidis_Tsaliki"
OUTDIR = paths.SALVAGED_BOOK_DATA / "Reconstructed"
OUTDIR.mkdir(parents=True, exist_ok=True)
Y0, Y1 = 1962, 1991

# canonical Greek 2-digit manufacturing industry labels, by panel id 20..39
CANON = {
    20: "20 Food", 21: "21 Beverages", 22: "22 Tobacco", 23: "23 Textiles",
    24: "24 Clothing & Footwear", 25: "25 Wood & Cork", 26: "26 Furniture",
    27: "27 Paper", 28: "28 Printing & Publishing", 29: "29 Leather",
    30: "30 Rubber", 31: "31 Chemicals", 32: "32 Petroleum & Coal",
    33: "33 Non-Metallic Minerals", 34: "34 Basic Metallic Products",
    35: "35 Metallic Products", 36: "36 Machines (Non-Electrical)",
    37: "37 Electrical Supplies", 38: "38 Transport Equipment",
    39: "39 Miscellaneous Manufacturing",
}

def build(fig_json: Path, out_xlsx: Path, title: str):
    data = json.load(open(fig_json))
    panels = data["panels"]
    years = list(range(Y0, Y1 + 1))
    cols = {"Year": years}
    for iid in range(20, 40):
        p = panels[str(iid)]
        ser = {d["year"]: d["value"] for d in p["series"]}
        cols[f"{CANON[iid]}_Deviation"] = [ser.get(y) for y in years]
    df = pd.DataFrame(cols)
    # write: A1 title, headers on row 2 (0-indexed row 1), data below
    with pd.ExcelWriter(out_xlsx, engine="openpyxl") as xl:
        df.to_excel(xl, index=False, startrow=1, sheet_name="data")
        xl.sheets["data"]["A1"] = title
    n_missing = int(df.drop(columns=["Year"]).isna().sum().sum())
    print(f"wrote {out_xlsx.name}: {len(df)} years x {len(df.columns)-1} industries, missing cells={n_missing}")

build(WL1 / "fig4_grid_extracted.json",
      OUTDIR / "Tsoulfidis_Tsaliki_2011_Fig4_S707.xlsx",
      "Deviations from Average Rate of Profit, Greek Manufacturing Industries, 1962-1991 "
      "(digitized from Tsoulfidis & Tsaliki 2011/2013 MPRA 51334 Fig 4; Shaikh 2016 Fig 7.19)")
build(WL1 / "fig6_grid_extracted.json",
      OUTDIR / "Tsoulfidis_Tsaliki_2011_Fig5_S708.xlsx",
      "Deviations of Incremental Rate of Profit from Average IROP, Greek Manufacturing Industries, 1962-1991 "
      "(digitized from Tsoulfidis & Tsaliki 2011/2013 MPRA 51334 Fig 6; Shaikh 2016 Fig 7.20)")
print("done")

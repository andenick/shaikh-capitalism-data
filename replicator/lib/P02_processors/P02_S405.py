"""P02_S405 — Inman automotive cost curve (digitized from Shaikh 2016 Fig 4.20).
Thin wrapper over L01_loaders._inman_cost_curves. Provenance: WL1_Tsoulfidis_Tsaliki/EXTRACTION_REPORT.md.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from L01_loaders._inman_cost_curves import process  # noqa: E402
SERIES_ID = "S405"
def run() -> dict:
    return process(SERIES_ID)
if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))

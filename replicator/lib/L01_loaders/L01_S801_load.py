"""L01_S801_load — data_unavailable stub for Fig 8.1 (Eichner 1973 wholesale prices).

Per CH8 dossier and Phase 5 blocker B6 resolution: Eichner (1973) p. 1187 publishes
Figure 8.1 as a chart only; no underlying table accompanies the chart; Shaikh did
not transcribe values; the Appendix8_* chopped tables do not include this figure.
The Eichner 1973 PDF is not in the RSCD workspace.

Per playbook recipe (data_unavailable):
  - L01 returns {"status": "SKIPPED", "reason": "data_unavailable"}
  - P02 not authored
  - V03 returns PASS_DATA_UNAVAILABLE
  - No chopped CSV
"""
SERIES_ID = "S801"


def run() -> dict:
    return {
        "status": "SKIPPED",
        "reason": "data_unavailable",
        "detail": (
            "Eichner (1973) Economic Journal 83(332), p. 1187 publishes Fig 8.1 as a "
            "chart only with no underlying table; Shaikh (2016) reproduces the chart "
            "without transcribing values; SalvagedInputs/book_data/ShaikhChoppedTables/ "
            "Appendix8_*.xlsx contains no file for this figure; the Eichner 1973 PDF "
            "is not present in the RSCD workspace. WebPlotDigitizer is appropriately "
            "constrained as a Phase 9 visualization task; BLS PPI reconstruction would "
            "be a proxy substitution requiring Phase 6 formal review. Per playbook "
            "recipe, no chopped CSV; V03 returns PASS_DATA_UNAVAILABLE."
        ),
        "sid": SERIES_ID,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2))

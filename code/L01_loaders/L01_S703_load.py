"""L01_S703_load — data_unavailable stub for Fig 7.13 (Christodoulopoulos world ROP/IROP).

Per CH7_ADEQUACY and dossier: Christodoulopoulos (1995) raw data not in SalvagedInputs;
underlying OECD ISDB 1994 vintage discontinued; PDF figure digitization deferred to Phase 9.
"""
SERIES_ID = "S703"


def run() -> dict:
    return {
        "status": "SKIPPED",
        "reason": "data_unavailable",
        "detail": "Christodoulopoulos (1995) raw data is not in SalvagedInputs and is not publicly hosted (unpublished NSSR working paper). OECD ISDB 1994 vintage discontinued. See SalvagedInputs/book_data/Reconstructed/Christodoulopoulos_1995_data_unavailable.md. Per playbook recipe, no chopped CSV; V03 returns PASS_DATA_UNAVAILABLE.",
        "sid": SERIES_ID,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2))

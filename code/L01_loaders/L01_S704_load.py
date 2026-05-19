"""L01_S704_load — data_unavailable stub for Fig 7.14 (Christodoulopoulos US sub-industries)."""
SERIES_ID = "S704"


def run() -> dict:
    return {
        "status": "SKIPPED",
        "reason": "data_unavailable",
        "detail": "Same Christodoulopoulos (1995) gap as S703; OECD ISDB 1994 US subset not redistributed. Post-1987 US continuation lives in S705/S706 (different schema). See SalvagedInputs/book_data/Reconstructed/Christodoulopoulos_1995_data_unavailable.md.",
        "sid": SERIES_ID,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2))

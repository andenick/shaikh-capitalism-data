"""Phase 5 Ch8 registry / subsource / ledger updater (idempotent).

Updates Technical/series_registry.json, Technical/SUBSOURCE_METADATA.json, and
Technical/ANU_LEDGER.json for S801-S805.

S801 is data_unavailable (Eichner 1973 Fig 8.1 — chart-only source, no underlying
table, no Appendix8 chopped file, no PDF in workspace). It is registered with
status="data_unavailable" and no chopped/extenbook artifacts.

Run:
    python Technical/code/utils/_ch8_register.py
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils import paths  # noqa: E402

ISO_NOW = datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# SUBSOURCE_METADATA additions
# ---------------------------------------------------------------------------
NEW_SUBSOURCES = {
    "EICHNER_1973_EJ": {
        "full_title": "Eichner, A.S. (1973), 'A Theory of the Determination of the Mark-Up Under Oligopoly,' Economic Journal 83(332): 1184-1200",
        "agency": "Eichner (academic author)",
        "publisher": "Royal Economic Society / Wiley",
        "publication_year": 1973,
        "table_id": "Eichner 1973, p. 1187 (chart)",
        "table_title": "Wholesale Price Indexes of Concentrated vs. Unconcentrated Industries, 1965-1973 (1957-59=100)",
        "page": "1187",
        "frequency": "annual",
        "native_units": "index_1957-59=100",
        "release_schedule": "one-time journal publication",
        "license": "Copyrighted journal article (Wiley/RES); reproduction restricted to fair use.",
        "retrieval_method": "not_retrieved",
        "retrieval_location": None,
        "url": "https://doi.org/10.2307/2230843",
        "url_status": "DOI live (paywall); article not present in RSCD Inputs/.",
        "discontinued": True,
        "replaced_by": "BLS PPI by industry; would require WebPlotDigitizer + SIC->NAICS bridge.",
        "requires_api_key": False,
        "graceful_degradation": "S801 is data_unavailable; no parquet/CSV/extenbook generated.",
        "notes": ("Source is chart-only (no underlying table in publication). Shaikh's book "
                  "reproduces the chart but transcribes no numeric values. No Appendix8_* "
                  "chopped file exists for Fig 8.1. Phase 5 blocker B6 resolved as "
                  "data_unavailable on 2026-05-18."),
    },
    "SEMMLER_1984_TABLE_3_3": {
        "full_title": "Semmler, Willi (1984), Competition, Monopoly, and Differential Profit Rates (NYC: Columbia University Press), Table 3.3, p. 95",
        "agency": "Semmler (academic author); underlying Weston, Lustgarten & Grottke (1974) AER 64(1):232-234",
        "publisher": "Columbia University Press",
        "publication_year": 1984,
        "table_id": "Semmler 1984, Table 3.3",
        "table_title": "Percentage of Price Increases or No Decreases during Contractions, by CR4 Bin (1957-58, 1960-61, 1969-70)",
        "page": "95",
        "frequency": "event-based (NBER contractions)",
        "native_units": "percent (price increases); CR4 midpoint percent",
        "release_schedule": "one-time book publication",
        "license": "Cross-sectional summary statistics; reproducible under fair use.",
        "retrieval_method": "salvaged xlsx",
        "retrieval_location": "SalvagedInputs/book_data/ShaikhChoppedTables/Appendix8_Semmler19843.3.xlsx",
        "url": "https://www.jstor.org/stable/1814892",
        "url_status": "JSTOR live (Weston et al. underlying); Semmler book print-only.",
        "discontinued": True,
        "replaced_by": "Reconstructible from BLS PPI industry detail + Census CR4 at NBER contraction windows.",
        "requires_api_key": False,
        "graceful_degradation": "FAIL if salvaged xlsx missing.",
        "notes": "9 cross-section points (3 CR4 bins x 3 contractions). Underlying micro data not published.",
    },
    "BAIN_1951_QJE": {
        "full_title": "Bain, Joe S. (1951), 'Relation of Profit Rate to Industry Concentration: American Manufacturing, 1936-1940,' Quarterly Journal of Economics 65(3): 293-324",
        "agency": "Bain (academic author); corrections by Demsetz (1973b)",
        "publisher": "Harvard / MIT Press for QJE",
        "publication_year": 1951,
        "table_id": "Bain 1951 Table I (p. 309/312, 42-industry scatter); Table II (p. 313, decile grouping); Demsetz 1973b p. 12 corrections",
        "table_title": "Rate of Profit on Equity vs. CR8, 42 US Manufacturing Industries, 1936-40",
        "page": "309, 312, 313",
        "frequency": "5-year average benchmark (1936-1940)",
        "native_units": "percent (rate of profit on equity); CR8 percent",
        "release_schedule": "one-time journal publication",
        "license": "Cross-sectional statistics; reproducible under fair use.",
        "retrieval_method": "salvaged xlsx",
        "retrieval_location": "SalvagedInputs/book_data/ShaikhChoppedTables/Appendix8_Bain*.xlsx",
        "url": "https://doi.org/10.2307/1882217",
        "url_status": "DOI live (paywall).",
        "discontinued": True,
        "replaced_by": None,
        "requires_api_key": False,
        "graceful_degradation": "FAIL if salvaged xlsx missing.",
        "notes": ("Fig 8.3 = Table I 42-industry scatter; Fig 8.4 = Table II decile grouping "
                  "with two overlays (Bain original + Demsetz 1973b correction)."),
    },
    "STIGLER_1963_TABLE_17": {
        "full_title": "Stigler, George J. (1963), Capital and Rates of Return in Manufacturing Industries (Princeton, NJ: Princeton University Press for NBER), Table 17, p. 68",
        "agency": "Stigler / NBER; underlying U.S. FTC/SEC Quarterly Financial Reports and earlier NRA / Census firm data.",
        "publisher": "Princeton University Press for NBER",
        "publication_year": 1963,
        "table_id": "Stigler 1963 Table 17",
        "table_title": "Rate of Profit on Assets, Concentrated vs. Unconcentrated Industries, 1939-1957 (six 3-year averages)",
        "page": "68",
        "frequency": "3-year average panel (1939-41, 1942-44, 1945-47, 1948-50, 1951-53, 1954-57)",
        "native_units": "percent (rate of profit on assets)",
        "release_schedule": "one-time book publication",
        "license": "NBER monograph; reproducible under fair use.",
        "retrieval_method": "salvaged xlsx",
        "retrieval_location": "SalvagedInputs/book_data/ShaikhChoppedTables/Appendix8_StiglerRatesOfProfit.xlsx",
        "url": "https://www.nber.org/books-and-chapters/capital-and-rates-return-manufacturing-industries",
        "url_status": "NBER live (book metadata).",
        "discontinued": True,
        "replaced_by": None,
        "requires_api_key": False,
        "graceful_degradation": "FAIL if salvaged xlsx missing.",
        "notes": ("6 bin-labels x 2 series (concentrated, unconcentrated). content_type "
                  "time_series per bin; processed parquet uses bin_label as primary axis."),
    },
    "DEMSETZ_1973B_TABLE_4": {
        "full_title": "Demsetz, Harold (1973b), 'Industry Structure, Market Rivalry, and Public Policy,' Journal of Law and Economics 16(1): 1-9 (Table 4, p. 19)",
        "agency": "Demsetz (academic author)",
        "publisher": "University of Chicago Press",
        "publication_year": 1973,
        "table_id": "Demsetz 1973b Table 4",
        "table_title": "Rates of Return and Concentration (CR4 bin), 1963 and 1969",
        "page": "19",
        "frequency": "two-year cross-section (1963, 1969)",
        "native_units": "percent (rate of profit on assets); CR4 bin",
        "release_schedule": "one-time journal publication",
        "license": "Copyrighted journal article; reproducible under fair use.",
        "retrieval_method": "salvaged xlsx",
        "retrieval_location": "SalvagedInputs/book_data/ShaikhChoppedTables/Appendix8_DemsetzRatesOfReturn.xlsx",
        "url": "https://doi.org/10.1086/466752",
        "url_status": "DOI live (paywall).",
        "discontinued": True,
        "replaced_by": None,
        "requires_api_key": False,
        "graceful_degradation": "FAIL if salvaged xlsx missing.",
        "notes": "6 CR4 bins x 2 years = 12 cross-sectional points.",
    },
}


# ---------------------------------------------------------------------------
# Series registry updates
# ---------------------------------------------------------------------------
COMMON_INGESTED = {"status": "ingested", "proxy": False}


REGISTRY_UPDATES = {
    "S801": {
        "status": "data_unavailable",
        "proxy": False,
        "content_type": "time_series",
        "construction": "direct",
        "units": "index_1957-59=100",
        "year_range": [1965, 1973],
        "year_range_book": [1965, 1973],
        "year_range_extension": [None, None],
        "primary_source": "EICHNER_1973_EJ",
        "dpr": "Technical/docs/series/S801_DPR.md",
        "epr": "Technical/docs/series/S801_EPR.md",
        "figures": ["Fig8.1"],
        "cross_references": ["S802", "S803", "S804", "S805"],
        "subseries": {},
        "data_unavailable_reason": "source_only_chart_no_table",
        "data_unavailable_resolution_date": "2026-05-18",
        "notes": ("Phase 5 blocker B6 resolved data_unavailable. Eichner (1973) p.1187 is a "
                  "chart-only source with no underlying table; Shaikh did not transcribe values; "
                  "Appendix8 ChoppedTables omit Fig 8.1; PDF not in RSCD workspace. Recovery "
                  "requires either (a) Eichner 1973 PDF + manual WebPlotDigitizer pass, or "
                  "(b) BLS PPI reconstruction approved as a Phase 6 proxy (SIC->NAICS bridge "
                  "needed). No parquet/chopped/extenbook artifact generated."),
    },
    "S802": {
        **COMMON_INGESTED,
        "content_type": "cross_sectional",
        "construction": "direct",
        "units": "percent",
        "year_range": [1957, 1970],
        "year_range_book": [1957, 1970],
        "year_range_extension": [None, None],
        "primary_source": "SEMMLER_1984_TABLE_3_3",
        "dpr": "Technical/docs/series/S802_DPR.md",
        "epr": "Technical/docs/series/S802_EPR.md",
        "figures": ["Fig8.2"],
        "cross_references": ["S801", "S803", "S804", "S805"],
        "subseries": {
            "S802-C1957": {"name": "Share of price increases/no decreases, 1957-58 contraction",
                            "subsource_id": "SEMMLER_1984_TABLE_3_3",
                            "period": [1957, 1958], "units": "percent",
                            "role": "book_period_primary", "proxy": False,
                            "notes": "Cross-section over 3 CR4 bins (midpoints 20/50/80)."},
            "S802-C1960": {"name": "Share of price increases/no decreases, 1960-61 contraction",
                            "subsource_id": "SEMMLER_1984_TABLE_3_3",
                            "period": [1960, 1961], "units": "percent",
                            "role": "book_period_primary", "proxy": False,
                            "notes": "Cross-section over 3 CR4 bins."},
            "S802-C1969": {"name": "Share of price increases/no decreases, 1969-70 contraction",
                            "subsource_id": "SEMMLER_1984_TABLE_3_3",
                            "period": [1969, 1970], "units": "percent",
                            "role": "book_period_primary", "proxy": False,
                            "notes": "Cross-section over 3 CR4 bins."},
        },
        "notes": ("Cross-sectional: 3 CR4 midpoints x 3 NBER-dated contractions = 9 points. "
                  "cr4_midpoint column is the disambiguator within (year, subseries_id)."),
    },
    "S803": {
        **COMMON_INGESTED,
        "content_type": "cross_sectional",
        "construction": "direct",
        "units": "percent",
        "year_range": [1936, 1940],
        "year_range_book": [1936, 1940],
        "year_range_extension": [None, None],
        "primary_source": "BAIN_1951_QJE",
        "dpr": "Technical/docs/series/S803_DPR.md",
        "epr": "Technical/docs/series/S803_EPR.md",
        "figures": ["Fig8.3", "Fig8.4"],
        "cross_references": ["S801", "S802", "S804", "S805"],
        "subseries": {
            "S803-FIG83": {"name": "Bain Fig 8.3 — 42-industry scatter (ROE vs CR8)",
                            "subsource_id": "BAIN_1951_QJE",
                            "period": [1936, 1940], "units": "percent",
                            "role": "book_period_primary", "proxy": False,
                            "notes": "Per-industry scatter; industry/census_number/axis disambiguate."},
            "S803-FIG84-BAIN": {"name": "Bain Fig 8.4 — original decile grouping",
                                 "subsource_id": "BAIN_1951_QJE",
                                 "period": [1936, 1940], "units": "percent",
                                 "role": "book_period_primary", "proxy": False,
                                 "notes": "Bain Table II decile averages; decile_index disambiguator."},
            "S803-FIG84-DEMSETZ": {"name": "Bain Fig 8.4 — Demsetz 1973b corrected grouping",
                                    "subsource_id": "BAIN_1951_QJE",
                                    "period": [1936, 1940], "units": "percent",
                                    "role": "book_period_primary", "proxy": False,
                                    "notes": "Demsetz 1973b p.12 regrouped to cr8_midpoint bins."},
        },
        "notes": "Combines Bain 1951 Tables I & II plus Demsetz 1973b corrections; 104 rows.",
    },
    "S804": {
        **COMMON_INGESTED,
        "content_type": "time_series",
        "construction": "direct",
        "units": "percent",
        "year_range": [1939, 1957],
        "year_range_book": [1939, 1957],
        "year_range_extension": [None, None],
        "primary_source": "STIGLER_1963_TABLE_17",
        "dpr": "Technical/docs/series/S804_DPR.md",
        "epr": "Technical/docs/series/S804_EPR.md",
        "figures": ["Fig8.5"],
        "cross_references": ["S801", "S802", "S803", "S805"],
        "subseries": {
            "S804-CONC": {"name": "Rate of profit on assets, concentrated industries",
                           "subsource_id": "STIGLER_1963_TABLE_17",
                           "period": [1939, 1957], "units": "percent",
                           "role": "book_period_primary", "proxy": False,
                           "notes": "6 three-year averages; bin_label drives x-axis."},
            "S804-UNCONC": {"name": "Rate of profit on assets, unconcentrated industries",
                             "subsource_id": "STIGLER_1963_TABLE_17",
                             "period": [1939, 1957], "units": "percent",
                             "role": "book_period_primary", "proxy": False,
                             "notes": "6 three-year averages; bin_label drives x-axis."},
        },
        "notes": ("Stigler 1963 Table 17 reports 3-year averages; processed parquet uses "
                  "bin_start as the canonical year and bin_label as the panel column."),
    },
    "S805": {
        **COMMON_INGESTED,
        "content_type": "cross_sectional",
        "construction": "direct",
        "units": "percent",
        "year_range": [1963, 1969],
        "year_range_book": [1963, 1969],
        "year_range_extension": [None, None],
        "primary_source": "DEMSETZ_1973B_TABLE_4",
        "dpr": "Technical/docs/series/S805_DPR.md",
        "epr": "Technical/docs/series/S805_EPR.md",
        "figures": ["Fig8.6"],
        "cross_references": ["S801", "S802", "S803", "S804"],
        "subseries": {
            "S805-1963": {"name": "Rate of return by CR4 bin, 1963",
                           "subsource_id": "DEMSETZ_1973B_TABLE_4",
                           "period": [1963, 1963], "units": "percent",
                           "role": "book_period_primary", "proxy": False,
                           "notes": "6 CR4 bins (10-20, 20-30, 30-40, 40-50, 50-60, 60+)."},
            "S805-1969": {"name": "Rate of return by CR4 bin, 1969",
                           "subsource_id": "DEMSETZ_1973B_TABLE_4",
                           "period": [1969, 1969], "units": "percent",
                           "role": "book_period_primary", "proxy": False,
                           "notes": "6 CR4 bins."},
        },
        "notes": "Cross-sectional: 6 CR4 bins x 2 years = 12 points. cr4_bin disambiguator.",
    },
}


# ---------------------------------------------------------------------------
def _ledger_entry(sid: str, name: str, *, data_unavailable: bool = False) -> dict:
    if data_unavailable:
        return {
            "name": name, "chapter": 8,
            "status": "data_unavailable",
            "phases_completed": ["3_research", "4_adequacy", "5_ingestion_blocked"],
            "artifacts": {
                "research_json": f"Technical/research/{sid}_research.json",
                "adequacy_report": "Technical/docs/chapters/CH8_ADEQUACY_REPORT.json",
                "dpr": f"Technical/docs/series/{sid}_DPR.md",
                "epr": f"Technical/docs/series/{sid}_EPR.md",
                "loader": f"Technical/code/L01_loaders/L01_{sid}_load.py",
                "validator": f"Technical/code/V03_validators/V03_{sid}_validate.py",
            },
            "data_unavailable_reason": "source_only_chart_no_table",
            "updated_at": ISO_NOW,
        }
    return {
        "name": name, "chapter": 8,
        "status": "extenbook_published",
        "phases_completed": ["3_research", "4_adequacy", "5_ingestion",
                              "6_extension", "7_replication", "8_output"],
        "artifacts": {
            "research_json": f"Technical/research/{sid}_research.json",
            "adequacy_report": "Technical/docs/chapters/CH8_ADEQUACY_REPORT.json",
            "dpr": f"Technical/docs/series/{sid}_DPR.md",
            "epr": f"Technical/docs/series/{sid}_EPR.md",
            "loader": f"Technical/code/L01_loaders/L01_{sid}_load.py",
            "processor": f"Technical/code/P02_processors/P02_{sid}_construct.py",
            "validator": f"Technical/code/V03_validators/V03_{sid}_validate.py",
            "processed": f"Technical/data/processed/{sid}.parquet",
            "chopped_csv": f"Technical/chopped/{sid}.csv",
            "extenbook_xlsx": f"Technical/extenbooks/{sid}_extenbook.xlsx",
        },
        "updated_at": ISO_NOW,
    }


LEDGER_UPDATES = {
    "S801": _ledger_entry("S801",
                           "Wholesale Prices, Concentrated vs Unconcentrated Industries 1965-73 (Eichner)",
                           data_unavailable=True),
    "S802": _ledger_entry("S802",
                           "Share of Price Increases by Concentration, NBER Contractions (Semmler/Weston)"),
    "S803": _ledger_entry("S803",
                           "Rate of Profit on Equity vs CR8, Bain 42-Industry Sample 1936-40"),
    "S804": _ledger_entry("S804",
                           "Rate of Profit on Assets, Concentrated vs Unconcentrated 1939-57 (Stigler)"),
    "S805": _ledger_entry("S805",
                           "Rates of Return and Concentration (CR4), 1963 and 1969 (Demsetz)"),
}


def main() -> int:
    sub_path = paths.SUBSOURCE_METADATA
    sub_doc = json.loads(sub_path.read_text(encoding="utf-8"))
    sub_doc.setdefault("subsources", {})
    for sid, body in NEW_SUBSOURCES.items():
        sub_doc["subsources"][sid] = body
    sub_doc["generated_at"] = ISO_NOW
    sub_path.write_text(json.dumps(sub_doc, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[OK] SUBSOURCE_METADATA.json updated ({len(NEW_SUBSOURCES)} subsources)")

    reg_path = paths.REGISTRY
    reg = json.loads(reg_path.read_text(encoding="utf-8"))
    for sid, body in REGISTRY_UPDATES.items():
        if sid not in reg["series"]:
            reg["series"][sid] = {}
        reg["series"][sid]["subseries"] = body["subseries"]
        for k, v in body.items():
            if k == "subseries":
                continue
            reg["series"][sid][k] = v
    reg_path.write_text(json.dumps(reg, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[OK] series_registry.json updated ({len(REGISTRY_UPDATES)} series)")

    ledger_path = paths.LEDGER
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    ledger.setdefault("series", {})
    for sid, body in LEDGER_UPDATES.items():
        ledger["series"][sid] = body
    ledger["last_updated"] = ISO_NOW
    ledger_path.write_text(json.dumps(ledger, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[OK] ANU_LEDGER.json updated ({len(LEDGER_UPDATES)} series)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

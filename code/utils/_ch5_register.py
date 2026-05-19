"""Phase 5 Ch5 registry / subsource / ledger updater (idempotent).

Updates Technical/series_registry.json, Technical/SUBSOURCE_METADATA.json, and
Technical/ANU_LEDGER.json for S501-S504.

Run:
    python Technical/code/utils/_ch5_register.py
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
# SUBSOURCE_METADATA additions (only those not already present)
# ---------------------------------------------------------------------------
NEW_SUBSOURCES = {
    "SHAIKH_APPENDIX_5_DATALRPRICES": {
        "full_title": "Shaikh, Capitalism (2016), Appendix 5.3 — Data Tables for Chapter 5, sheet DATALRprices",
        "agency": "Anwar Shaikh (author construction; underlying Jastram 1977 + BLS + ONS + NBER + MeasuringWorth)",
        "publisher": "Oxford University Press",
        "publication_year": 2016,
        "table_id": "Appendix 5.3 / sheet DATALRprices",
        "table_title": "US and UK WPI 1780-2010 plus gold price index decompositions (1930=100)",
        "page": "788-789",
        "frequency": "annual",
        "native_units": "index_1930=100",
        "release_schedule": "one-time book publication",
        "license": "Copyright OUP; underlying agency data are public-domain or academic-permissive. Reproduced under fair use for research replication.",
        "retrieval_method": "salvaged xlsx (originally hosted at http://www.anwarshaikhecon.org/, DNS dead 2026-05-18)",
        "retrieval_location": "SalvagedInputs/book_data/ShaikhChoppedTables/Appendix5_DATALRprices.xlsx",
        "url": "https://web.archive.org/web/20240311145229/https://www.anwarshaikhecon.org/",
        "url_status": "wayback citation (live site DNS gaierror 2026-05-18)",
        "discontinued": False,
        "replaced_by": None,
        "requires_api_key": False,
        "graceful_degradation": "Local xlsx is canonical; loaders FAIL if missing.",
        "notes": ("Hosts 47 columns including USWPI, UKWPI, USPPIGold, UKPPIGold, "
                  "USGoldpriceindex, UKGoldpriceindex used by S501-S504. Year range 1780-2030 "
                  "(forecast rows present but unused). Wartime 1939-1945 UK gold/WPI flagged "
                  "as MeasuringWorth interpolation per Phase 4."),
    },
    "FRED_PPIACO": {
        "full_title": "FRED PPIACO — Producer Price Index by Commodity: All Commodities (FRED mirror of BLS WPU00000000)",
        "agency": "Bureau of Labor Statistics (via FRED)",
        "publisher": "Federal Reserve Bank of St. Louis",
        "publication_year": 2026,
        "table_id": "PPIACO",
        "table_title": "Producer Price Index by Commodity: All Commodities, NSA, monthly (annual avg used)",
        "page": None,
        "frequency": "monthly (annual avg used)",
        "native_units": "index_1982=100",
        "release_schedule": "monthly",
        "license": "U.S. Government Work (public domain)",
        "retrieval_method": "FRED fredgraph CSV (no key required)",
        "retrieval_location": None,
        "url": "https://fred.stlouisfed.org/series/PPIACO",
        "url_status": "live HTTP 200 (verified via fredgraph.csv 2026-05-18; latest 2026-04 = 283.764)",
        "discontinued": False,
        "replaced_by": None,
        "requires_api_key": False,
        "graceful_degradation": "S502 US extension skipped if endpoint fails; book period publishes regardless.",
        "notes": ("FRED identifier PPIACO mirrors BLS PPI All Commodities = WPU00000000 "
                  "(WPS00000000 frozen 1974). Same concept, BLS underlying; no proxy. "
                  "Latest observation 2026-04 = 283.764 matches Phase 4 reachability check."),
    },
}


# ---------------------------------------------------------------------------
# Series registry updates
# ---------------------------------------------------------------------------
COMMON = {"status": "ingested", "proxy": False}


REGISTRY_UPDATES = {
    "S501": {
        **COMMON,
        "content_type": "time_series",
        "construction": "direct",
        "units": "index_1930=100",
        "year_range": [1790, 1940],
        "year_range_book": [1790, 1940],
        "year_range_extension": [None, None],
        "primary_source": "SHAIKH_APPENDIX_5_DATALRPRICES",
        "dpr": "Technical/docs/series/S501_DPR.md",
        "epr": "Technical/docs/series/S501_EPR.md",
        "figures": ["Fig5.3"],
        "cross_references": ["S502"],
        "subseries": {
            "S501-A": {"name": "US WPI 1790-1940", "source": "Appendix5 column USWPI",
                        "subsource_id": "SHAIKH_APPENDIX_5_DATALRPRICES",
                        "period": [1790, 1940], "units": "index_1930=100",
                        "color": "#1f77b4", "role": "book_period_primary",
                        "proxy": False, "proxy_justification": None,
                        "notes": "1790-1799 imputed from US CPI per Appendix 2.1 (flagged in loader)."},
            "S501-B": {"name": "UK WPI 1790-1940", "source": "Appendix5 column UKWPI",
                        "subsource_id": "SHAIKH_APPENDIX_5_DATALRPRICES",
                        "period": [1790, 1940], "units": "index_1930=100",
                        "color": "#ff7f0e", "role": "book_period_primary",
                        "proxy": False, "proxy_justification": None,
                        "notes": "1939-1940 NBER m04053 fill (flagged in loader)."},
        },
        "notes": "Chronological slice of S502; enforce single-loader policy.",
    },
    "S502": {
        **COMMON,
        "content_type": "time_series",
        "construction": "composite",
        "units": "index_1930=100",
        "year_range": [1790, 2025],
        "year_range_book": [1790, 2010],
        "year_range_extension": [2011, 2025],
        "primary_source": "SHAIKH_APPENDIX_5_DATALRPRICES",
        "dpr": "Technical/docs/series/S502_DPR.md",
        "epr": "Technical/docs/series/S502_EPR.md",
        "figures": ["Fig5.4"],
        "cross_references": ["S501", "S503", "S504"],
        "subseries": {
            "S502-A": {"name": "US WPI 1790-2010", "source": "Appendix5 column USWPI",
                        "subsource_id": "SHAIKH_APPENDIX_5_DATALRPRICES",
                        "period": [1790, 2010], "units": "index_1930=100",
                        "color": "#1f77b4", "role": "book_period_primary",
                        "proxy": False, "proxy_justification": None},
            "S502-B": {"name": "UK WPI 1790-2010", "source": "Appendix5 column UKWPI",
                        "subsource_id": "SHAIKH_APPENDIX_5_DATALRPRICES",
                        "period": [1790, 2010], "units": "index_1930=100",
                        "color": "#ff7f0e", "role": "book_period_primary",
                        "proxy": False, "proxy_justification": None},
            "S502-C": {"name": "US PPI All Commodities (extension)",
                        "source": "FRED PPIACO (mirror of BLS WPU00000000)",
                        "subsource_id": "FRED_PPIACO",
                        "period": [2011, 2026], "units": "index_1930=100",
                        "color": "#2ca02c", "role": "extension",
                        "proxy": False,
                        "proxy_justification": "WPS->WPU is BLS internal identifier change; FRED PPIACO mirrors WPU00000000 (same All-Commodities PPI concept); not a substitution.",
                        "splice_strategy": "overlap_anchor_2010"},
            "S502-D": {"name": "UK Output Producer Price (extension)",
                        "source": "ONS PLLU",
                        "subsource_id": None,
                        "period": [2011, 2025], "units": "index_1930=100",
                        "color": "#d62728", "role": "extension",
                        "proxy": False, "proxy_justification": None,
                        "extension_status": "api_unavailable_ons_pllu_cdn_502",
                        "splice_strategy": "overlap_anchor_2010_when_available"},
        },
        "extension_method": "overlap_anchor_us_only_v1",
        "notes": ("US extension via FRED WPU00000000 anchored at 2010 (WPS->WPU "
                  "verified equivalent). UK extension not fetched v1: ONS PLLU CDN 502 "
                  "from our IP per Phase 4 2026-05-18."),
    },
    "S503": {
        **COMMON,
        "content_type": "time_series",
        "construction": "formula",
        "units": "index_1930=100",
        "year_range": [1790, 2010],
        "year_range_book": [1790, 2010],
        "year_range_extension": [None, None],
        "primary_source": "SHAIKH_APPENDIX_5_DATALRPRICES",
        "dpr": "Technical/docs/series/S503_DPR.md",
        "epr": "Technical/docs/series/S503_EPR.md",
        "figures": ["Fig5.5"],
        "cross_references": ["S502", "S504"],
        "formula": "UKWPI = p'_UK * pG_UK / 100 (book eq. 5.9). p'_UK = UKPPIGold; pG_UK = UKGoldpriceindex.",
        "components": [
            {"label": "p'_UK = UK WPI in gold", "source": "Appendix5 column UKPPIGold",
             "subsource_id": "SHAIKH_APPENDIX_5_DATALRPRICES"},
            {"label": "pG_UK = UK gold price index", "source": "Appendix5 column UKGoldpriceindex",
             "subsource_id": "SHAIKH_APPENDIX_5_DATALRPRICES"},
        ],
        "subseries": {
            "S503-A": {"name": "p'_UK (UK WPI in gold)",
                        "source": "Appendix5 column UKPPIGold",
                        "subsource_id": "SHAIKH_APPENDIX_5_DATALRPRICES",
                        "period": [1790, 2010], "units": "index_1930=100",
                        "color": "#1f77b4", "role": "book_period_primary",
                        "proxy": False, "proxy_justification": None,
                        "notes": "1939-1945 wartime: MeasuringWorth interpolated (flagged in loader)."},
            "S503-B": {"name": "pG_UK (UK gold price)",
                        "source": "Appendix5 column UKGoldpriceindex",
                        "subsource_id": "SHAIKH_APPENDIX_5_DATALRPRICES",
                        "period": [1790, 2010], "units": "index_1930=100",
                        "color": "#ff7f0e", "role": "book_period_primary",
                        "proxy": False, "proxy_justification": None,
                        "notes": "Same WW2 wartime caveat."},
        },
        "extension_method": "recompute_ratio_from_components_when_components_available",
        "extension_status_v1": "not_attempted_v1",
        "extension_reasons_v1": ("UK WPI 2011+ needs ONS PLLU (502 from our IP); "
                                  "UK gold price 2011+ needs LBMA helper (not implemented)."),
        "notes": "Formula series: extension MUST recompute ratio; no lazy splice on p'_UK.",
    },
    "S504": {
        **COMMON,
        "content_type": "time_series",
        "construction": "formula",
        "units": "index_1930=100",
        "year_range": [1800, 2010],
        "year_range_book": [1800, 2010],
        "year_range_extension": [None, None],
        "primary_source": "SHAIKH_APPENDIX_5_DATALRPRICES",
        "dpr": "Technical/docs/series/S504_DPR.md",
        "epr": "Technical/docs/series/S504_EPR.md",
        "figures": ["Fig5.6"],
        "cross_references": ["S502", "S503"],
        "formula": "USWPI = p'_US * pG_US / 100 (book eq. 5.9). p'_US = USPPIGold; pG_US = USGoldpriceindex.",
        "components": [
            {"label": "p'_US = US WPI in gold", "source": "Appendix5 column USPPIGold",
             "subsource_id": "SHAIKH_APPENDIX_5_DATALRPRICES"},
            {"label": "pG_US = US gold price index", "source": "Appendix5 column USGoldpriceindex",
             "subsource_id": "SHAIKH_APPENDIX_5_DATALRPRICES"},
        ],
        "subseries": {
            "S504-A": {"name": "p'_US (US WPI in gold)",
                        "source": "Appendix5 column USPPIGold",
                        "subsource_id": "SHAIKH_APPENDIX_5_DATALRPRICES",
                        "period": [1800, 2010], "units": "index_1930=100",
                        "color": "#1f77b4", "role": "book_period_primary",
                        "proxy": False, "proxy_justification": None},
            "S504-B": {"name": "pG_US (US gold price)",
                        "source": "Appendix5 column USGoldpriceindex",
                        "subsource_id": "SHAIKH_APPENDIX_5_DATALRPRICES",
                        "period": [1800, 2010], "units": "index_1930=100",
                        "color": "#ff7f0e", "role": "book_period_primary",
                        "proxy": False, "proxy_justification": None,
                        "notes": "1933/34 FDR jump $20.67->$35.00 visible (1934/1933 = 1.430)."},
        },
        "extension_method": "recompute_ratio_from_components_when_components_available",
        "extension_status_v1": "not_attempted_v1",
        "extension_reasons_v1": "US gold price 2011+ needs LBMA helper (not implemented).",
        "notes": "Formula series: extension MUST recompute ratio; no lazy splice on p'_US.",
    },
}


# ---------------------------------------------------------------------------
def _ledger_entry(sid: str, name: str) -> dict:
    return {
        "name": name, "chapter": 5,
        "status": "extenbook_published",
        "phases_completed": ["3_research", "4_adequacy", "5_ingestion",
                              "6_extension", "7_replication", "8_output"],
        "artifacts": {
            "research_json": f"Technical/research/{sid}_research.json",
            "adequacy_report": "Technical/docs/chapters/CH5_ADEQUACY_REPORT.json",
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
    "S501": _ledger_entry("S501", "US and UK Wholesale Price Indexes, 1790-1940"),
    "S502": _ledger_entry("S502", "US and UK Wholesale Price Indexes, 1790-2010"),
    "S503": _ledger_entry("S503", "UK WPI in Gold and UK Gold Price"),
    "S504": _ledger_entry("S504", "US WPI in Gold and US Gold Price"),
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

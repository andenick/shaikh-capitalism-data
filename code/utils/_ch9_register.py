"""Phase 5 Ch9 registry / subsource / ledger updater (idempotent).

Updates Technical/series_registry.json, Technical/SUBSOURCE_METADATA.json, and
Technical/ANU_LEDGER.json for S901-S903.

Applies Phase 4 ratified figure-list cleanup:
  S901: Fig 9.1, 9.2, 9.16
  S902: Fig 9.4, 9.5, 9.6, 9.7, 9.9, 9.10, 9.11, 9.13, 9.14, 9.15, 9.18
  S903: Fig 9.8, 9.12, 9.19 (trimmed from CD2's 11-figure overflow list)

Run:
    python Technical/code/utils/_ch9_register.py
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils import paths  # noqa: E402

ISO_NOW = datetime.now(timezone.utc).isoformat()


NEW_SUBSOURCES = {
    "SHAIKH_APPENDIX_9_1947F": {
        "full_title": "Shaikh (2016) Appendix 9, 1947 fixed-capital IO table (Ochoa 1984 / Shaikh 1998a, 71 industries)",
        "agency": "Anwar Shaikh / Edward Ochoa (compiled from BEA SIC-vintage IO tables)",
        "publisher": "Oxford University Press", "publication_year": 2016,
        "table_id": "Appendix 9 / Ams1_47.xmcd",
        "table_title": "1947 71-industry IO: tpm, td, tv, tp(r)",
        "page": "867-868", "frequency": "single-year benchmark",
        "native_units": "millions of $ (absolute); normalized share in derived columns",
        "release_schedule": "one-time book publication",
        "license": "Copyright OUP; underlying BEA IO is public domain. Reproduced under fair use for replication.",
        "retrieval_method": "salvaged xlsx", "retrieval_location": "SalvagedInputs/book_data/ShaikhChoppedTables/Appendix9_1947fixed.xlsx",
        "url": "https://web.archive.org/web/20240311145229/https://www.anwarshaikhecon.org/",
        "url_status": "wayback citation (live site DNS dead)",
        "discontinued": False, "replaced_by": None,
        "requires_api_key": False, "graceful_degradation": "FAIL if missing",
        "notes": "12-column workbook: Index, tpm, td, tv, tp(r), 4 normalized variants, 3 quotient columns. r observed = 0.236.",
    },
    "SHAIKH_APPENDIX_9_1958F": {
        "full_title": "Shaikh (2016) Appendix 9, 1958 fixed-capital IO table (Ochoa 1984 / Shaikh 1998a, 71 industries)",
        "agency": "Anwar Shaikh / Edward Ochoa", "publisher": "Oxford University Press", "publication_year": 2016,
        "table_id": "Appendix 9 / Ams1_58.xmcd", "table_title": "1958 71-industry IO",
        "page": "867-868", "frequency": "single-year benchmark",
        "native_units": "millions of $; normalized share in derived columns",
        "license": "Copyright OUP; BEA underlying public domain.",
        "retrieval_method": "salvaged xlsx", "retrieval_location": "SalvagedInputs/book_data/ShaikhChoppedTables/Appendix9_1958fixed.xlsx",
        "url": "https://web.archive.org/web/20240311145229/https://www.anwarshaikhecon.org/",
        "url_status": "wayback citation", "discontinued": False, "replaced_by": None,
        "requires_api_key": False, "graceful_degradation": "FAIL if missing",
        "notes": "r observed = 0.176.",
    },
    "SHAIKH_APPENDIX_9_1963F": {
        "full_title": "Shaikh (2016) Appendix 9, 1963 fixed-capital IO table",
        "agency": "Anwar Shaikh / Edward Ochoa", "publisher": "Oxford University Press", "publication_year": 2016,
        "table_id": "Appendix 9", "table_title": "1963 71-industry IO",
        "page": "867-868", "frequency": "single-year benchmark",
        "native_units": "millions of $; normalized share derived",
        "license": "Copyright OUP; BEA underlying public domain.",
        "retrieval_method": "salvaged xlsx", "retrieval_location": "SalvagedInputs/book_data/ShaikhChoppedTables/Appendix9_1963fixed.xlsx",
        "url": "https://web.archive.org/web/20240311145229/https://www.anwarshaikhecon.org/",
        "url_status": "wayback citation", "discontinued": False, "replaced_by": None,
        "requires_api_key": False, "graceful_degradation": "FAIL if missing",
        "notes": "r observed = 0.21.",
    },
    "SHAIKH_APPENDIX_9_1967F": {
        "full_title": "Shaikh (2016) Appendix 9, 1967 fixed-capital IO table",
        "agency": "Anwar Shaikh / Edward Ochoa", "publisher": "Oxford University Press", "publication_year": 2016,
        "table_id": "Appendix 9", "table_title": "1967 71-industry IO",
        "page": "867-868", "frequency": "single-year benchmark",
        "native_units": "millions of $; normalized share derived",
        "license": "Copyright OUP; BEA underlying public domain.",
        "retrieval_method": "salvaged xlsx", "retrieval_location": "SalvagedInputs/book_data/ShaikhChoppedTables/Appendix9_1967fixed.xlsx",
        "url": "https://web.archive.org/web/20240311145229/https://www.anwarshaikhecon.org/",
        "url_status": "wayback citation", "discontinued": False, "replaced_by": None,
        "requires_api_key": False, "graceful_degradation": "FAIL if missing",
        "notes": "r observed = 0.229.",
    },
    "SHAIKH_APPENDIX_9_1972F": {
        "full_title": "Shaikh (2016) Appendix 9, 1972 fixed-capital IO table",
        "agency": "Anwar Shaikh / Edward Ochoa", "publisher": "Oxford University Press", "publication_year": 2016,
        "table_id": "Appendix 9", "table_title": "1972 71-industry IO",
        "page": "867-868", "frequency": "single-year benchmark",
        "native_units": "millions of $; normalized share derived",
        "license": "Copyright OUP; BEA underlying public domain.",
        "retrieval_method": "salvaged xlsx", "retrieval_location": "SalvagedInputs/book_data/ShaikhChoppedTables/Appendix9_1972fixed.xlsx",
        "url": "https://web.archive.org/web/20240311145229/https://www.anwarshaikhecon.org/",
        "url_status": "wayback citation", "discontinued": False, "replaced_by": None,
        "requires_api_key": False, "graceful_degradation": "FAIL if missing",
        "notes": "r observed = 0.188. Also used by S216 (Ch2 Fig 2.16).",
    },
    "SHAIKH_APPENDIX_9_1998C": {
        "full_title": "Shaikh (2016) Appendix 9, 1998 circulating-capital IO (BEA 65-industry NAICS)",
        "agency": "Anwar Shaikh (from BEA Use Tables 1998, OOH-corrected per NIPA T7.12)",
        "publisher": "Oxford University Press", "publication_year": 2016,
        "table_id": "Appendix 9 / LTVCalc1998stdREadjCirc.xmcd",
        "table_title": "1998 65-industry circulating IO: tpm, td, tv, tp(r)",
        "page": "867-868", "frequency": "single-year benchmark",
        "native_units": "millions of $; normalized share derived",
        "license": "Copyright OUP; BEA underlying public domain.",
        "retrieval_method": "salvaged xlsx", "retrieval_location": "SalvagedInputs/book_data/ShaikhChoppedTables/Appendix9_1998Circ.xlsx",
        "url": "https://web.archive.org/web/20240311145229/https://www.anwarshaikhecon.org/",
        "url_status": "wayback citation", "discontinued": False, "replaced_by": None,
        "requires_api_key": False, "graceful_degradation": "FAIL if missing",
        "notes": "K=A, D=0 (circulating). r observed = 0.2971.",
    },
    "SHAIKH_APPENDIX_9_1998F": {
        "full_title": "Shaikh (2016) Appendix 9, 1998 fixed-capital IO (BEA 65-industry + Fixed Asset Tables 3.1ES/3.4ES)",
        "agency": "Anwar Shaikh",
        "publisher": "Oxford University Press", "publication_year": 2016,
        "table_id": "Appendix 9 / LTVCalc1998stdREadjFixed.xmcd",
        "table_title": "1998 65-industry fixed-capital IO",
        "page": "867-868", "frequency": "single-year benchmark",
        "native_units": "millions of $; normalized share derived",
        "license": "Copyright OUP; BEA underlying public domain.",
        "retrieval_method": "salvaged xlsx", "retrieval_location": "SalvagedInputs/book_data/ShaikhChoppedTables/Appendix9_1998Fixed.xlsx",
        "url": "https://web.archive.org/web/20240311145229/https://www.anwarshaikhecon.org/",
        "url_status": "wayback citation", "discontinued": False, "replaced_by": None,
        "requires_api_key": False, "graceful_degradation": "FAIL if missing",
        "notes": "K, D from Fixed Asset Tables + 1997 capital flow benchmark. r observed = 0.1258.",
    },
    "SHAIKH_APPENDIX_9_OBSERVED_PROFIT_RATES": {
        "full_title": "Shaikh (2016) Appendix 9, observed profit rates table",
        "agency": "Anwar Shaikh",
        "publisher": "Oxford University Press", "publication_year": 2016,
        "table_id": "Appendix 9 / Table 9.18", "table_title": "Observed profit rates per benchmark IO year",
        "page": "423 (Table 9.18 maximum profit rates); per-sheet headers list observed",
        "frequency": "6 benchmark-year scalars",
        "native_units": "decimal profit rate",
        "license": "Copyright OUP; underlying BEA NIPA public domain.",
        "retrieval_method": "salvaged xlsx",
        "retrieval_location": "SalvagedInputs/book_data/ShaikhChoppedTables/Appendix9_ObservedProfitRates.xlsx",
        "url": "https://web.archive.org/web/20240311145229/https://www.anwarshaikhecon.org/",
        "url_status": "wayback citation", "discontinued": False, "replaced_by": None,
        "requires_api_key": False, "graceful_degradation": "FAIL if missing",
        "notes": "Values: 1947=0.236, 1958=0.176, 1963=0.21, 1967=0.229, 1972=0.188, 1998=0.1258.",
    },
    "SHAIKH_APPENDIX_9_PWT_BOOK2": {
        "full_title": "Shaikh (2016) Appendix 9, PennWorldTables2 workbook (wage-profit curves + R_fixed scalars)",
        "agency": "Anwar Shaikh (computed wage-profit curves + PWT 7.1 productivity index)",
        "publisher": "Oxford University Press", "publication_year": 2016,
        "table_id": "Appendix 9 / PennWorldTables2",
        "table_title": "Per-year wage-profit curves wshr{YR}/wr{YR} + R_fixed + RealGDPperworkerindex",
        "page": "422-423, 868-869", "frequency": "6+1 benchmark curves",
        "native_units": "dimensionless (decimal r, wage share, productivity index)",
        "license": "Copyright OUP; PWT 7.1 underlying CC-BY academic-use; BEA underlying public domain.",
        "retrieval_method": "salvaged xlsx",
        "retrieval_location": "SalvagedInputs/book_data/ShaikhChoppedTables/Appendix9_PennWorldTables2.xlsx",
        "url": "https://web.archive.org/web/20240311145229/https://www.anwarshaikhecon.org/",
        "url_status": "wayback citation", "discontinued": False, "replaced_by": None,
        "requires_api_key": False, "graceful_degradation": "FAIL if missing",
        "notes": "R_fixed values match Table 9.18: [1.088, 0.9734, 0.8547, 0.7644, 0.7033, 0.7317].",
    },
}


COMMON = {"status": "ingested", "proxy": False}


REGISTRY_UPDATES = {
    "S901": {
        **COMMON,
        "content_type": "cross_sectional",
        "construction": "composite",
        "units": "normalized_share",
        "year_range": [1947, 1998],
        "year_range_book": [1947, 1998],
        "year_range_extension": [None, None],
        "primary_source": "SHAIKH_APPENDIX_9_1998F",
        "dpr": "Technical/docs/series/S901_DPR.md",
        "epr": "Technical/docs/series/S901_EPR.md",
        "figures": ["Fig9.1", "Fig9.2", "Fig9.16"],
        "cross_references": ["S902"],
        "subseries": {
            "S901-A_1947F": {"name": "Market price (normalized) 1947 fixed",
                              "subsource_id": "SHAIKH_APPENDIX_9_1947F",
                              "period": [1947, 1947], "units": "normalized_share",
                              "role": "book_period_primary", "proxy": False},
            "S901-A_1958F": {"name": "Market price (normalized) 1958 fixed",
                              "subsource_id": "SHAIKH_APPENDIX_9_1958F",
                              "period": [1958, 1958], "units": "normalized_share",
                              "role": "book_period_primary", "proxy": False},
            "S901-A_1963F": {"name": "Market price (normalized) 1963 fixed",
                              "subsource_id": "SHAIKH_APPENDIX_9_1963F",
                              "period": [1963, 1963], "units": "normalized_share",
                              "role": "book_period_primary", "proxy": False},
            "S901-A_1967F": {"name": "Market price (normalized) 1967 fixed",
                              "subsource_id": "SHAIKH_APPENDIX_9_1967F",
                              "period": [1967, 1967], "units": "normalized_share",
                              "role": "book_period_primary", "proxy": False},
            "S901-A_1972F": {"name": "Market price (normalized) 1972 fixed",
                              "subsource_id": "SHAIKH_APPENDIX_9_1972F",
                              "period": [1972, 1972], "units": "normalized_share",
                              "role": "book_period_primary", "proxy": False},
            "S901-A_1998C": {"name": "Market price (normalized) 1998 circulating",
                              "subsource_id": "SHAIKH_APPENDIX_9_1998C",
                              "period": [1998, 1998], "units": "normalized_share",
                              "role": "book_period_primary", "proxy": False},
            "S901-A_1998F": {"name": "Market price (normalized) 1998 fixed",
                              "subsource_id": "SHAIKH_APPENDIX_9_1998F",
                              "period": [1998, 1998], "units": "normalized_share",
                              "role": "book_period_primary", "proxy": False},
            "S901-B_1947F": {"name": "Direct price (normalized) 1947 fixed",
                              "subsource_id": "SHAIKH_APPENDIX_9_1947F",
                              "period": [1947, 1947], "units": "normalized_share",
                              "role": "book_period_primary", "proxy": False},
            "S901-B_1958F": {"name": "Direct price (normalized) 1958 fixed",
                              "subsource_id": "SHAIKH_APPENDIX_9_1958F",
                              "period": [1958, 1958], "units": "normalized_share",
                              "role": "book_period_primary", "proxy": False},
            "S901-B_1963F": {"name": "Direct price (normalized) 1963 fixed",
                              "subsource_id": "SHAIKH_APPENDIX_9_1963F",
                              "period": [1963, 1963], "units": "normalized_share",
                              "role": "book_period_primary", "proxy": False},
            "S901-B_1967F": {"name": "Direct price (normalized) 1967 fixed",
                              "subsource_id": "SHAIKH_APPENDIX_9_1967F",
                              "period": [1967, 1967], "units": "normalized_share",
                              "role": "book_period_primary", "proxy": False},
            "S901-B_1972F": {"name": "Direct price (normalized) 1972 fixed",
                              "subsource_id": "SHAIKH_APPENDIX_9_1972F",
                              "period": [1972, 1972], "units": "normalized_share",
                              "role": "book_period_primary", "proxy": False},
            "S901-B_1998C": {"name": "Direct price (normalized) 1998 circulating",
                              "subsource_id": "SHAIKH_APPENDIX_9_1998C",
                              "period": [1998, 1998], "units": "normalized_share",
                              "role": "book_period_primary", "proxy": False},
            "S901-B_1998F": {"name": "Direct price (normalized) 1998 fixed",
                              "subsource_id": "SHAIKH_APPENDIX_9_1998F",
                              "period": [1998, 1998], "units": "normalized_share",
                              "role": "book_period_primary", "proxy": False},
        },
        "notes": "6 benchmark years; NAICS/SIC break prevents continuous panel. Fig 9.16 substrate (market prices) lives here, production-price overlay from S902.",
    },
    "S902": {
        **COMMON,
        "content_type": "cross_sectional",
        "construction": "composite",
        "units": "normalized_share_and_decimal_profit_rate",
        "year_range": [1947, 1998],
        "year_range_book": [1947, 1998],
        "year_range_extension": [None, None],
        "primary_source": "SHAIKH_APPENDIX_9_1998F",
        "dpr": "Technical/docs/series/S902_DPR.md",
        "epr": "Technical/docs/series/S902_EPR.md",
        "figures": ["Fig9.4", "Fig9.5", "Fig9.6", "Fig9.7", "Fig9.9", "Fig9.10",
                     "Fig9.11", "Fig9.13", "Fig9.14", "Fig9.15", "Fig9.18"],
        "cross_references": ["S901", "S903"],
        "formula": "p(r) eigensystem solve from KT = K*(I-(A+D))^-1; tp(r)_norm and tv_norm published.",
        "components": [
            {"label": "1947-1972 historical 71-industry IO", "subsource_ids": [
                "SHAIKH_APPENDIX_9_1947F", "SHAIKH_APPENDIX_9_1958F",
                "SHAIKH_APPENDIX_9_1963F", "SHAIKH_APPENDIX_9_1967F",
                "SHAIKH_APPENDIX_9_1972F"]},
            {"label": "1998 BEA 65-industry circulating + fixed", "subsource_ids": [
                "SHAIKH_APPENDIX_9_1998C", "SHAIKH_APPENDIX_9_1998F"]},
            {"label": "Observed profit rates per benchmark", "subsource_ids": [
                "SHAIKH_APPENDIX_9_OBSERVED_PROFIT_RATES"]},
        ],
        "subseries": {
            "S902-P_1947F": {"name": "Standard price normalized 1947 fixed",
                              "subsource_id": "SHAIKH_APPENDIX_9_1947F",
                              "period": [1947, 1947], "units": "normalized_share",
                              "role": "book_period_primary", "proxy": False},
            "S902-P_1958F": {"name": "Standard price normalized 1958 fixed",
                              "subsource_id": "SHAIKH_APPENDIX_9_1958F",
                              "period": [1958, 1958], "units": "normalized_share",
                              "role": "book_period_primary", "proxy": False},
            "S902-P_1963F": {"name": "Standard price normalized 1963 fixed",
                              "subsource_id": "SHAIKH_APPENDIX_9_1963F",
                              "period": [1963, 1963], "units": "normalized_share",
                              "role": "book_period_primary", "proxy": False},
            "S902-P_1967F": {"name": "Standard price normalized 1967 fixed",
                              "subsource_id": "SHAIKH_APPENDIX_9_1967F",
                              "period": [1967, 1967], "units": "normalized_share",
                              "role": "book_period_primary", "proxy": False},
            "S902-P_1972F": {"name": "Standard price normalized 1972 fixed",
                              "subsource_id": "SHAIKH_APPENDIX_9_1972F",
                              "period": [1972, 1972], "units": "normalized_share",
                              "role": "book_period_primary", "proxy": False},
            "S902-P_1998C": {"name": "Standard price normalized 1998 circulating",
                              "subsource_id": "SHAIKH_APPENDIX_9_1998C",
                              "period": [1998, 1998], "units": "normalized_share",
                              "role": "book_period_primary", "proxy": False},
            "S902-P_1998F": {"name": "Standard price normalized 1998 fixed",
                              "subsource_id": "SHAIKH_APPENDIX_9_1998F",
                              "period": [1998, 1998], "units": "normalized_share",
                              "role": "book_period_primary", "proxy": False},
            "S902-V_ALL": {"name": "Labor value composition (VR0) per benchmark",
                            "subsource_id": "SHAIKH_APPENDIX_9_1998F",
                            "period": [1947, 1998], "units": "normalized_share",
                            "role": "book_period_primary", "proxy": False,
                            "notes": "S902-V_{LABEL} pattern, mirrors S902-P labels."},
            "S902-ROBS": {"name": "Observed profit rate per benchmark year",
                           "subsource_id": "SHAIKH_APPENDIX_9_OBSERVED_PROFIT_RATES",
                           "period": [1947, 1998], "units": "decimal_profit_rate",
                           "role": "book_period_primary", "proxy": False,
                           "notes": "6 scalars."},
        },
        "notes": "Pre-computed tp(r) from Appendix9; fresh eigenvalue solve deferred to scientific-validation skill.",
    },
    "S903": {
        **COMMON,
        "content_type": "cross_sectional",
        "construction": "formula",
        "units": "dimensionless_wage_share_and_real_wage_index",
        "year_range": [1947, 1998],
        "year_range_book": [1947, 1998],
        "year_range_extension": [None, None],
        "primary_source": "SHAIKH_APPENDIX_9_PWT_BOOK2",
        "dpr": "Technical/docs/series/S903_DPR.md",
        "epr": "Technical/docs/series/S903_EPR.md",
        "figures": ["Fig9.8", "Fig9.12", "Fig9.19"],
        "cross_references": ["S902"],
        "formula": "wr(r)_t = sigma_W(r)_t * (yr_t / yr_0); sigma_W = 1 - r/R_t (Sraffa standard wage frontier).",
        "components": [
            {"label": "Per-year wage shares + real-wage curves",
             "subsource_id": "SHAIKH_APPENDIX_9_PWT_BOOK2"},
            {"label": "PWT 7.1 productivity index anchors",
             "subsource_id": "SHAIKH_APPENDIX_9_PWT_BOOK2"},
            {"label": "R_t Table 9.18", "subsource_id": "SHAIKH_APPENDIX_9_PWT_BOOK2"},
        ],
        "subseries": {
            "S903-WSHARE-47": {"name": "Wage share at r, 1947", "period": [1947, 1947],
                                "units": "dimensionless", "role": "book_period_primary",
                                "proxy": False, "subsource_id": "SHAIKH_APPENDIX_9_PWT_BOOK2"},
            "S903-WSHARE-58": {"name": "Wage share at r, 1958", "period": [1958, 1958],
                                "units": "dimensionless", "role": "book_period_primary",
                                "proxy": False, "subsource_id": "SHAIKH_APPENDIX_9_PWT_BOOK2"},
            "S903-WSHARE-63": {"name": "Wage share at r, 1963", "period": [1963, 1963],
                                "units": "dimensionless", "role": "book_period_primary",
                                "proxy": False, "subsource_id": "SHAIKH_APPENDIX_9_PWT_BOOK2"},
            "S903-WSHARE-67": {"name": "Wage share at r, 1967", "period": [1967, 1967],
                                "units": "dimensionless", "role": "book_period_primary",
                                "proxy": False, "subsource_id": "SHAIKH_APPENDIX_9_PWT_BOOK2"},
            "S903-WSHARE-72": {"name": "Wage share at r, 1972", "period": [1972, 1972],
                                "units": "dimensionless", "role": "book_period_primary",
                                "proxy": False, "subsource_id": "SHAIKH_APPENDIX_9_PWT_BOOK2"},
            "S903-WSHARE-98FIX": {"name": "Wage share at r, 1998 fixed", "period": [1998, 1998],
                                   "units": "dimensionless", "role": "book_period_primary",
                                   "proxy": False, "subsource_id": "SHAIKH_APPENDIX_9_PWT_BOOK2"},
            "S903-WSHARE-98CIRC": {"name": "Wage share at r, 1998 circulating",
                                    "period": [1998, 1998],
                                    "units": "dimensionless", "role": "book_period_primary",
                                    "proxy": False, "subsource_id": "SHAIKH_APPENDIX_9_PWT_BOOK2"},
            "S903-WRCURVE-47": {"name": "Real-wage curve 1947", "period": [1947, 1947],
                                 "units": "dimensionless", "role": "book_period_primary",
                                 "proxy": False, "subsource_id": "SHAIKH_APPENDIX_9_PWT_BOOK2"},
            "S903-WRCURVE-58": {"name": "Real-wage curve 1958", "period": [1958, 1958],
                                 "units": "dimensionless", "role": "book_period_primary",
                                 "proxy": False, "subsource_id": "SHAIKH_APPENDIX_9_PWT_BOOK2"},
            "S903-WRCURVE-63": {"name": "Real-wage curve 1963", "period": [1963, 1963],
                                 "units": "dimensionless", "role": "book_period_primary",
                                 "proxy": False, "subsource_id": "SHAIKH_APPENDIX_9_PWT_BOOK2"},
            "S903-WRCURVE-67": {"name": "Real-wage curve 1967", "period": [1967, 1967],
                                 "units": "dimensionless", "role": "book_period_primary",
                                 "proxy": False, "subsource_id": "SHAIKH_APPENDIX_9_PWT_BOOK2"},
            "S903-WRCURVE-72": {"name": "Real-wage curve 1972", "period": [1972, 1972],
                                 "units": "dimensionless", "role": "book_period_primary",
                                 "proxy": False, "subsource_id": "SHAIKH_APPENDIX_9_PWT_BOOK2"},
            "S903-WRCURVE-98FIX": {"name": "Real-wage curve 1998 fixed", "period": [1998, 1998],
                                    "units": "dimensionless", "role": "book_period_primary",
                                    "proxy": False, "subsource_id": "SHAIKH_APPENDIX_9_PWT_BOOK2"},
            "S903-WRCURVE-98CIRC": {"name": "Real-wage curve 1998 circulating", "period": [1998, 1998],
                                     "units": "dimensionless", "role": "book_period_primary",
                                     "proxy": False, "subsource_id": "SHAIKH_APPENDIX_9_PWT_BOOK2"},
            "S903-R-FIXED": {"name": "Maximum profit rate R per benchmark year (Table 9.18)",
                              "period": [1947, 1998], "units": "decimal_profit_rate",
                              "role": "book_period_primary", "proxy": False,
                              "subsource_id": "SHAIKH_APPENDIX_9_PWT_BOOK2"},
            "S903-R-CIRC": {"name": "Maximum profit rate R 1998 circulating",
                             "period": [1998, 1998], "units": "decimal_profit_rate",
                             "role": "book_period_primary", "proxy": False,
                             "subsource_id": "SHAIKH_APPENDIX_9_PWT_BOOK2"},
            "S903-PWT-RGDPPERWORKER": {"name": "PWT 7.1 real GDP per worker (1947-base index)",
                                        "period": [1947, 1998], "units": "dimensionless",
                                        "role": "book_period_primary", "proxy": False,
                                        "subsource_id": "SHAIKH_APPENDIX_9_PWT_BOOK2"},
        },
        "extension_method": "pwt_71_to_pwt_1001_growth_rate_splice_on_productivity_index_only",
        "extension_status_v1": "not_attempted_v1",
        "notes": ("PWT 7.1 variable confirmed as `rgdpwok` (Real GDP per worker, chain-weighted) "
                  "in Appendix9_PennWorldTables.xlsx. 1947 anchor reconstructed by Shaikh from BEA "
                  "Long Term Eco Growth A163 1948/1950. R_fixed values match Table 9.18 exactly."),
    },
}


def _ledger_entry(sid: str, name: str) -> dict:
    return {
        "name": name, "chapter": 9,
        "status": "extenbook_published",
        "phases_completed": ["3_research", "4_adequacy", "5_ingestion",
                              "6_extension", "7_replication", "8_output"],
        "artifacts": {
            "research_json": f"Technical/research/{sid}_research.json",
            "adequacy_report": "Technical/docs/chapters/CH9_ADEQUACY_REPORT.json",
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
    "S901": _ledger_entry("S901", "Market Prices vs Direct Prices, 71 Industries"),
    "S902": _ledger_entry("S902", "Integrated Output-Capital Ratios and Standard Prices"),
    "S903": _ledger_entry("S903", "Actual Wage-Profit Curves, US 1947-1998"),
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

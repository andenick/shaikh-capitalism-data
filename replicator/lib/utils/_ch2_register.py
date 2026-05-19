"""One-shot script to update series_registry, SUBSOURCE_METADATA, and ANU_LEDGER
for all 17 Ch2 series (S202-S218) atomically.

Idempotent: re-running is safe; only the affected keys are updated.

Run: python Technical/code/utils/_ch2_register.py
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.paths import REGISTRY, SUBSOURCE_METADATA, LEDGER  # noqa: E402


# -----------------------------------------------------------------------------
# REGISTRY DELTAS PER SERIES
# -----------------------------------------------------------------------------
REGISTRY_DELTAS = {
    "S202": {
        "status": "ingested",
        "content_type": "time_series",
        "construction": "composite",
        "units": "index_1958=100",
        "subseries": {
            "S202-A": {"name": "BEA 1977 Table B4 (Investment in Fixed Nonres Bus Capital)",
                       "source": "BEA Fixed Reproducible Tangible Wealth 1925-1975 (1977)",
                       "subsource_id": "BEA_1977_T_B4", "period": [1832, 1975],
                       "units": "index_1970=100", "color": "#1f77b4", "role": "book_period_early"},
            "S202-B": {"name": "BEA Wealth Table 4.8 line 1 (Investment in Fixed Nonres Capital)",
                       "source": "BEA Fixed-Asset Wealth Tables",
                       "subsource_id": "BEA_WEALTH_T48", "period": [1901, 2010],
                       "units": "constant_dollars_BEA_2011_vintage", "color": "#ff7f0e",
                       "role": "book_period_late"},
            "S202-C": {"name": "BEA NIPA T1.1.6 line 9 (Real Nonresidential Fixed Investment)",
                       "source": "BEA NIPA",
                       "subsource_id": "BEA_NIPA_T116_L9", "period": [2010, 2025],
                       "units": "chained_2017_dollars_billions", "color": "#2ca02c",
                       "role": "extension"},
        },
        "proxy": False,
    },
    "S203": {
        "status": "ingested", "content_type": "time_series", "construction": "direct",
        "units": "real_dollars_2005",
        "subseries": {
            "S203-A": {"name": "MeasuringWorth Real GDP per Capita (book period)",
                       "source": "MeasuringWorth", "subsource_id": "MEASURINGWORTH_USGDP",
                       "period": [1889, 2010], "units": "real_dollars_2005",
                       "color": "#1f77b4", "role": "book_period_primary"},
            "S203-B": {"name": "FRED A939RX0Q048SBEA (Real GDP per Capita, chained 2017$)",
                       "source": "FRED", "subsource_id": "FRED_RGDPPC",
                       "period": [2005, 2025], "units": "chained_2017_dollars",
                       "color": "#ff7f0e", "role": "extension"},
        },
        "proxy": False,
    },
    "S204": {
        "status": "ingested", "content_type": "time_series", "construction": "direct",
        "units": "percent_deviation_from_trend",
        "subseries": {
            "S204-A": {"name": "Ayres (1939) Index 1831-1866 (monthly)",
                       "source": "Cleveland Trust Co / Ayres 1939", "subsource_id": "AYRES_1939_T9_APP_A",
                       "period": [1831, 1866], "units": "percent_deviation_from_trend",
                       "color": "#1f77b4", "role": "book_period_primary",
                       "frequency": "monthly"},
        },
        "proxy": False, "extension_status": "discontinued",
    },
    "S205": {
        "status": "ingested", "content_type": "time_series", "construction": "direct",
        "units": "percent_deviation_from_trend",
        "subseries": {
            "S205-A": {"name": "Ayres (1939) Index 1867-1902 (monthly)",
                       "source": "Cleveland Trust Co / Ayres 1939", "subsource_id": "AYRES_1939_T9_APP_A",
                       "period": [1867, 1902], "units": "percent_deviation_from_trend",
                       "color": "#1f77b4", "role": "book_period_primary", "frequency": "monthly"},
        },
        "proxy": False, "extension_status": "discontinued",
    },
    "S206": {
        "status": "ingested", "content_type": "time_series", "construction": "direct",
        "units": "percent_deviation_from_trend",
        "subseries": {
            "S206-A": {"name": "Ayres (1939) Index 1903-1939 (monthly)",
                       "source": "Cleveland Trust Co / Ayres 1939", "subsource_id": "AYRES_1939_T9_APP_A",
                       "period": [1903, 1939], "units": "percent_deviation_from_trend",
                       "color": "#1f77b4", "role": "book_period_primary", "frequency": "monthly"},
        },
        "proxy": False, "extension_status": "discontinued",
    },
    "S207": {
        "status": "ingested", "content_type": "time_series", "construction": "composite",
        "units": "index_1889=100 (productivity); index_1889=100 (real compensation)",
        "subseries": {
            "S207-A": {"name": "US Mfg Productivity (BEA LTEG A173 + BLS FLS spliced 1950)",
                       "source": "BEA LTEG (1966) + BLS International Labor Comparisons",
                       "subsource_id": "BEA_LTEG_BLS_FLS_SPLICE", "period": [1889, 2010],
                       "units": "index_1889=100", "color": "#1f77b4", "role": "book_period_primary"},
            "S207-B": {"name": "US Mfg Production-Worker Real Compensation Index",
                       "source": "MeasuringWorth uswage (formerly uscompensation) + CPI",
                       "subsource_id": "MEASURINGWORTH_USWAGE_CPI", "period": [1889, 2010],
                       "units": "index_1889=100", "color": "#ff7f0e", "role": "book_period_primary"},
            "S207-C": {"name": "FRED OPHMFG (Manufacturing Real Output Per Hour) extension",
                       "source": "FRED (BLS continuation, US-only)",
                       "subsource_id": "FRED_OPHMFG", "period": [2005, 2025],
                       "units": "index_2017=100", "color": "#2ca02c", "role": "extension",
                       "proxy": True,
                       "proxy_justification": "BLS FLS Table 1 (19-country) sunset 2013; FRED OPHMFG is the US-only BLS Productivity & Costs continuation. Concept narrows from 19-country comparison to US-only."},
            "S207-D": {"name": "FRED COMPRMS (Mfg Real Compensation per Hour) extension",
                       "source": "FRED",
                       "subsource_id": "FRED_COMPRMS", "period": [2005, 2025],
                       "units": "index_2017=100", "color": "#d62728", "role": "extension"},
        },
        "proxy": True,
        "proxy_justification": "Phase 4 substitutions: MeasuringWorth uscompensation -> uswage rename (URL only); BLS FLS Table 1 sunset 2013 -> FRED OPHMFG (US-only).",
    },
    "S208": {
        "status": "ingested", "content_type": "time_series", "construction": "formula",
        "units": "index_1889=100",
        "formula": "RULC_index[t] = (real_compensation_per_hour[t] / productivity_index[t]) * 100",
        "components": [
            {"label": "Real compensation per hour", "source_series": "S207-B"},
            {"label": "Manufacturing productivity index", "source_series": "S207-A"},
        ],
        "subseries": {
            "S208-A": {"name": "Book RULC (Shaikh derived, 1889-2010)",
                       "source": "Shaikh Appendix2_ManufacturingProductivity.xlsx 'Mfgrealunitlaborcost'",
                       "subsource_id": "SHAIKH_DERIVED_RULC", "period": [1889, 2010],
                       "units": "index_1889=100", "color": "#1f77b4", "role": "book_period_primary"},
            "S208-B": {"name": "Extension via recomputed formula from S207 extensions",
                       "source": "RECOMPUTED_FROM_S207_EXT",
                       "subsource_id": "S208_RECOMPUTE_FROM_S207", "period": [2011, 2025],
                       "units": "index_1889=100", "color": "#ff7f0e", "role": "extension"},
        },
        "proxy": False,
        "extension_note": "DO NOT splice FRED ULCMFG (nominal ULC) directly -- must recompute real ratio from S207 components.",
    },
    "S209": {
        "status": "ingested", "content_type": "time_series", "construction": "composite",
        "units": "percent",
        "subseries": {
            "S209-A": {"name": "BEA LTEG B1-B2 unemployment (1890-1947)",
                       "source": "BEA Long Term Economic Growth (1966) Series B1-B2",
                       "subsource_id": "BEA_LTEG_B1_B2", "period": [1890, 1970],
                       "units": "percent", "color": "#1f77b4", "role": "book_period_early"},
            "S209-B": {"name": "ERP Table B-40 (Civilian Unemployment Rate)",
                       "source": "Economic Report of the President",
                       "subsource_id": "ERP_T_B40", "period": [1948, 2010],
                       "units": "percent", "color": "#ff7f0e", "role": "book_period_late"},
            "S209-C": {"name": "FRED UNRATE",
                       "source": "FRED (BLS Civilian Unemployment Rate)",
                       "subsource_id": "FRED_UNRATE", "period": [2010, 2025],
                       "units": "percent", "color": "#2ca02c", "role": "extension"},
        },
        "proxy": False,
    },
    "S210": {
        "status": "ingested", "content_type": "time_series", "construction": "composite",
        "units": "index_1930=100",
        "subseries": {
            "S210-A": {"name": "US WPI (Jastram 1977 T7 + BLS PPI extension)",
                       "source": "Jastram (1977) Golden Constant Table 7 + BLS WPS->WPU",
                       "subsource_id": "JASTRAM_1977_T7_PLUS_BLS_PPI_EXT", "period": [1780, 2010],
                       "units": "index_1930=100", "color": "#1f77b4", "role": "book_period_primary"},
            "S210-B": {"name": "UK WPI (Jastram 1977 T2 + ONS PLLU extension)",
                       "source": "Jastram (1977) Golden Constant Table 2 + ONS PLLU",
                       "subsource_id": "JASTRAM_1977_T2_PLUS_ONS_PLLU", "period": [1780, 2010],
                       "units": "index_1930=100", "color": "#ff7f0e", "role": "book_period_primary"},
            "S210-C": {"name": "FRED WPU00000000 (PPI All Commodities) US extension",
                       "source": "FRED",
                       "subsource_id": "FRED_WPU00000000", "period": [2005, 2025],
                       "units": "index_1982=100", "color": "#2ca02c", "role": "extension",
                       "proxy": True,
                       "proxy_justification": "BLS froze WPS00000000 in 1974; WPU00000000 is the published successor for PPI All Commodities."},
        },
        "proxy": False,
    },
    "S211": {
        "status": "ingested", "content_type": "time_series", "construction": "composite",
        "units": "index_1930=100",
        "subseries": {
            "S211-A": {"name": "US WPI 1780-1940 (Jastram 1977 T7)",
                       "source": "Jastram (1977)", "subsource_id": "JASTRAM_1977_T7_US_WPI",
                       "period": [1780, 1940], "units": "index_1930=100",
                       "color": "#1f77b4", "role": "book_period_primary"},
            "S211-B": {"name": "UK WPI 1780-1940 (Jastram 1977 T2)",
                       "source": "Jastram (1977)", "subsource_id": "JASTRAM_1977_T2_UK_WPI",
                       "period": [1780, 1940], "units": "index_1930=100",
                       "color": "#ff7f0e", "role": "book_period_primary"},
        },
        "proxy": False, "extension_status": "not_applicable_windowed",
    },
    "S212": {
        "status": "ingested", "content_type": "time_series", "construction": "formula",
        "units": "index_1930=100",
        "formula": "WPI_in_gold[country, t] = WPI[country, t] / gold_price[country, t]; rebased to 1930=100",
        "components": [
            {"label": "US WPI", "source_series": "S210-A"},
            {"label": "UK WPI", "source_series": "S210-B"},
            {"label": "US gold price (MeasuringWorth)", "source_series": "MEASURINGWORTH_USGOLD"},
            {"label": "UK gold price (MeasuringWorth)", "source_series": "MEASURINGWORTH_UKGOLD"},
        ],
        "subseries": {
            "S212-A": {"name": "US WPI in gold ounces (Jastram T1 + MW)",
                       "source": "Jastram (1977) T1 + MeasuringWorth gold",
                       "subsource_id": "JASTRAM_1977_T1_MW_US_WPI_GOLD", "period": [1790, 2010],
                       "units": "index_1930=100", "color": "#1f77b4", "role": "book_period_primary"},
            "S212-B": {"name": "UK WPI in gold ounces",
                       "source": "Jastram (1977) + MeasuringWorth gold",
                       "subsource_id": "JASTRAM_1977_MW_UK_WPI_GOLD", "period": [1790, 2010],
                       "units": "index_1930=100", "color": "#ff7f0e", "role": "book_period_primary"},
            "S212-C": {"name": "US WPI/gold extension (recomputed from FRED WPU + FRED gold)",
                       "source": "FRED WPU00000000 + FRED GOLDPMGBD228NLBM",
                       "subsource_id": "RECOMPUTED_FRED_WPU_GOLD", "period": [2010, 2025],
                       "units": "index_1930=100", "color": "#2ca02c", "role": "extension"},
        },
        "proxy": False,
    },
    "S213": {
        "status": "ingested", "content_type": "time_series", "construction": "formula",
        "units": "rate_decimal",
        "formula": "r[t] = NOS_corporate[t] / K_net[t-1]",
        "components": [
            {"label": "Net Operating Surplus (Corporate)", "source": "BEA NIPA T1.14 line 18"},
            {"label": "Net Stock of Private Nonresidential Fixed Assets", "source": "BEA FA T4.1"},
        ],
        "subseries": {
            "S213-A": {"name": "Book corporate profit rate (1947-2011)",
                       "source": "Derived from BEA NIPA T1.14 + FA T4.1 per Appendix 6.7",
                       "subsource_id": "BEA_NIPA_T114_FA_T41_DERIVED", "period": [1947, 2011],
                       "units": "rate_decimal", "color": "#1f77b4", "role": "book_period_primary"},
        },
        "proxy": False,
    },
    "S214": {
        "status": "ingested", "content_type": "time_series", "construction": "formula",
        "units": "rate_decimal",
        "formula": "r_sector[t] = profit[t] / capital_stock[t]  (per Appendix 7.1)",
        "components": [
            {"label": "Sectoral profit (15 US manufacturing aggregates)",
             "source": "anwarshaikhecon.org Appendix 7.2 (NOT IN SALVAGED)"},
            {"label": "Sectoral capital stock", "source": "OECD ISDB 1994 vintage (NOT IN SALVAGED)"},
        ],
        "subseries": {
            "S214-EXT": {"name": "Post-book mfg ROP industry average (1987-2005, Appendix 7)",
                         "source": "Shaikh Appendix7_ropdataUSind",
                         "subsource_id": "SHAIKH_APP7_ROP_USIND_1987_2005",
                         "period": [1987, 2005], "units": "rate_decimal",
                         "color": "#ff7f0e", "role": "post_book_only"},
        },
        "proxy": False,
        "book_period_status": "data_unavailable",
        "book_period_reason": "1960-1989 source (anwarshaikhecon.org App 7.2 / OECD ISDB 1994) not in SalvagedInputs",
    },
    "S215": {
        "status": "ingested", "content_type": "time_series", "construction": "formula",
        "units": "rate_decimal",
        "formula": "r*[t] = PG[t] / IG[t-1]",
        "components": [
            {"label": "Gross profits PG (NOT IN SALVAGED)"},
            {"label": "Gross investment IG lagged 1 year (NOT IN SALVAGED)"},
        ],
        "subseries": {
            "S215-EXT": {"name": "Post-book mfg IROP industry average (1988-2005, Appendix 7)",
                         "source": "Shaikh Appendix7_iropdataUSind",
                         "subsource_id": "SHAIKH_APP7_IROP_USIND_1988_2005",
                         "period": [1988, 2005], "units": "rate_decimal",
                         "color": "#ff7f0e", "role": "post_book_only"},
        },
        "proxy": False,
        "book_period_status": "data_unavailable",
        "book_period_reason": "1960-1989 source not in SalvagedInputs",
    },
    "S216": {
        "status": "ingested", "content_type": "cross_sectional", "construction": "formula",
        "units": "normalized_dollars",
        "formula": "Cross-section: prices_of_production = Sraffian system; integrated_ULC = (I - A)^(-1) * l",
        "subseries": {
            "S216-A": {"name": "Total Production Prices (normalized), 71 industries, 1972",
                       "source": "BEA 1972 Use/Make tables + Shaikh Appendix 9 Sraffian computation",
                       "subsource_id": "BEA_IO_1972_71IND_SHAIKH_APP9", "period": [1972, 1972],
                       "units": "normalized_dollars", "color": "#1f77b4", "role": "y_axis_tp_r"},
            "S216-B": {"name": "Total Market Prices (normalized), 71 industries, 1972",
                       "source": "BEA 1972 Use/Make tables", "subsource_id": "BEA_IO_1972_71IND_SHAIKH_APP9",
                       "period": [1972, 1972], "units": "normalized_dollars",
                       "color": "#ff7f0e", "role": "y_axis_tpm"},
        },
        "proxy": False, "extension_status": "not_applicable_cross_sectional",
    },
    "S217": {
        "status": "ingested", "content_type": "time_series", "construction": "direct",
        "units": "geary_khamis_1990_per_capita",
        "subseries": {
            "S217-A": {"name": "World", "source": "Maddison 2003", "subsource_id": "MADDISON_2003_APP_TABLE_2A",
                       "period": [1600, 2000], "units": "geary_khamis_1990_per_capita",
                       "color": "#1f77b4", "role": "book_period_primary"},
            "S217-B": {"name": "Western Europe", "source": "Maddison 2003",
                       "subsource_id": "MADDISON_2003_APP_TABLE_2A", "period": [1600, 2000],
                       "units": "geary_khamis_1990_per_capita", "color": "#ff7f0e",
                       "role": "book_period_primary"},
            "S217-C": {"name": "Western Offshoots", "source": "Maddison 2003",
                       "subsource_id": "MADDISON_2003_APP_TABLE_2A", "period": [1600, 2000],
                       "units": "geary_khamis_1990_per_capita", "color": "#2ca02c",
                       "role": "book_period_primary"},
            "S217-D": {"name": "Latin America", "source": "Maddison 2003",
                       "subsource_id": "MADDISON_2003_APP_TABLE_2A", "period": [1600, 2000],
                       "units": "geary_khamis_1990_per_capita", "color": "#d62728",
                       "role": "book_period_primary"},
            "S217-E": {"name": "Asia", "source": "Maddison 2003",
                       "subsource_id": "MADDISON_2003_APP_TABLE_2A", "period": [1600, 2000],
                       "units": "geary_khamis_1990_per_capita", "color": "#9467bd",
                       "role": "book_period_primary"},
            "S217-F": {"name": "Africa", "source": "Maddison 2003",
                       "subsource_id": "MADDISON_2003_APP_TABLE_2A", "period": [1600, 2000],
                       "units": "geary_khamis_1990_per_capita", "color": "#8c564b",
                       "role": "book_period_primary"},
        },
        "proxy": False,
        "extension_status": "deferred",
        "extension_note": "MPD 2023 (Bolt & van Zanden 2024) base year 2011 PPP differs from 1990 GK; regional aggregates revised. Manual splice deferred to Phase 9.",
    },
    "S218": {
        "status": "ingested", "content_type": "time_series", "construction": "formula",
        "units": "geary_khamis_1990_per_capita (levels); ratio",
        "formula": "richest4_avg[t] = mean(top 4 countries excluding Kuwait/Qatar/Venezuela); poorest4_avg[t] = mean(bottom 4); ratio[t] = richest4_avg/poorest4_avg",
        "subseries": {
            "S218-A": {"name": "RICHEST 4 average (Maddison, Shaikh exclusion rule)",
                       "source": "Maddison 2003 + Shaikh exclusion rule",
                       "subsource_id": "MADDISON_2003_SHAIKH_EXCLUSION_RULE",
                       "period": [1600, 2000], "units": "geary_khamis_1990_per_capita",
                       "color": "#1f77b4", "role": "book_period_primary"},
            "S218-B": {"name": "POOREST 4 average",
                       "source": "Maddison 2003", "subsource_id": "MADDISON_2003_SHAIKH_EXCLUSION_RULE",
                       "period": [1600, 2000], "units": "geary_khamis_1990_per_capita",
                       "color": "#ff7f0e", "role": "book_period_primary"},
            "S218-C": {"name": "RATIO OF RICHEST 4 TO POOREST 4",
                       "source": "Computed", "subsource_id": "MADDISON_2003_SHAIKH_EXCLUSION_RULE",
                       "period": [1600, 2000], "units": "ratio", "color": "#2ca02c",
                       "role": "book_period_primary"},
        },
        "proxy": False, "extension_status": "deferred",
        "extension_note": "MPD 2023 extension requires Shaikh exclusion rule reapplication + possible new exclusions (Macao, Luxembourg).",
    },
}


# -----------------------------------------------------------------------------
# SUBSOURCE METADATA ADDITIONS
# -----------------------------------------------------------------------------
CH2_SUBSOURCES = {
    "BEA_1977_T_B4": {
        "full_title": "BEA Fixed Reproducible Tangible Wealth of the United States, 1925-75, Table B4",
        "agency": "U.S. Bureau of Economic Analysis",
        "publication_year": 1977, "table_id": "B4", "frequency": "annual",
        "native_units": "Index 1970=100",
        "license": "Public domain", "retrieval_method": "salvaged_chopped_table",
        "retrieval_location": "SalvagedInputs/book_data/ShaikhChoppedTables/Appendix2_RealInvestmentUS_1832-2010.xlsx",
        "url": "https://apps.bea.gov/iTable/?reqid=10", "url_status": "out-of-print",
        "discontinued": True,
        "notes": "1977 BEA print volume; values preserved in salvaged chopped table.",
    },
    "BEA_WEALTH_T48": {
        "full_title": "BEA Fixed-Asset Wealth Table 4.8, line 1 (Investment in Fixed Nonresidential Capital)",
        "agency": "U.S. Bureau of Economic Analysis", "table_id": "T4.8 line 1",
        "frequency": "annual", "native_units": "Constant dollars (BEA 2011 vintage)",
        "license": "Public domain",
        "retrieval_method": "salvaged_chopped_table",
        "retrieval_location": "SalvagedInputs/book_data/ShaikhChoppedTables/Appendix2_RealInvestmentUS_1832-2010.xlsx",
        "url": "https://apps.bea.gov/iTable/?reqid=10", "url_status": "live", "discontinued": False,
    },
    "BEA_NIPA_T116_L9": {
        "full_title": "BEA NIPA Table 1.1.6 line 9 (Real Nonresidential Fixed Investment)",
        "agency": "U.S. Bureau of Economic Analysis", "table_id": "T1.1.6 line 9",
        "frequency": "annual", "native_units": "Chained 2017 dollars (billions)",
        "license": "Public domain", "retrieval_method": "api",
        "url": "https://apps.bea.gov/iTable/?reqid=19", "url_status": "live", "discontinued": False,
        "requires_api_key": True, "api_key_env_var": "BEA_API_KEY",
        "graceful_degradation": "If BEA_API_KEY missing, S202 publishes 1832-2010 only.",
        "notes": "Phase 4 preferred over FRED GPDIC1 (which includes residential).",
    },
    "MEASURINGWORTH_USGDP": {
        "full_title": "MeasuringWorth Annual GDP of the United States, 1790-Present",
        "agency": "MeasuringWorth (Officer & Williamson)", "publisher": "MeasuringWorth.com",
        "frequency": "annual", "native_units": "Real GDP per capita, constant 2005 dollars",
        "license": "MeasuringWorth academic-use", "retrieval_method": "salvaged_chopped_table",
        "retrieval_location": "SalvagedInputs/book_data/ShaikhChoppedTables/Appendix2_MeasuringWorthGDP_1889-2010.xlsx",
        "url": "https://www.measuringworth.com/datasets/usgdp/", "url_status": "live",
        "discontinued": False,
    },
    "FRED_RGDPPC": {
        "full_title": "FRED A939RX0Q048SBEA (Real GDP per Capita, chained 2017 $)",
        "agency": "U.S. Bureau of Economic Analysis (republished by FRED)", "frequency": "annual (avg of quarterly)",
        "native_units": "Chained 2017 dollars", "license": "Public domain",
        "retrieval_method": "api",
        "url": "https://fred.stlouisfed.org/series/A939RX0Q048SBEA", "url_status": "live",
        "discontinued": False, "requires_api_key": True, "api_key_env_var": "FRED_API_KEY",
    },
    "AYRES_1939_T9_APP_A": {
        "full_title": "Ayres (1939) Turning Points in Business Cycles, Table 9, Appendix A, col. 1",
        "agency": "Cleveland Trust Company (Leonard P. Ayres)", "publisher": "Macmillan, NY",
        "publication_year": 1939, "frequency": "monthly",
        "native_units": "Percent deviation from trend",
        "license": "Public domain (pre-1964 US publication)",
        "retrieval_method": "salvaged_chopped_table",
        "retrieval_location": "SalvagedInputs/book_data/ShaikhChoppedTables/Appendix2_Ayres.xlsx",
        "url": "https://catalog.hathitrust.org/Record/001141928", "url_status": "live",
        "discontinued": True,
        "notes": "No modern continuation; pre-NBER composite business activity index.",
    },
    "BEA_LTEG_BLS_FLS_SPLICE": {
        "full_title": "Shaikh-constructed splice: BEA LTEG A173 (1860-1970) + BLS Foreign Labor Statistics Table 1 (1950-2009)",
        "agency": "BEA + BLS",
        "frequency": "annual", "native_units": "Index 1958=100 (BEA), Index 2007=100 (BLS)",
        "license": "Public domain", "retrieval_method": "salvaged_chopped_table",
        "retrieval_location": "SalvagedInputs/book_data/ShaikhChoppedTables/Appendix2_ManufacturingProductivityAndRealWages1889-2010.xlsx",
        "url": "https://www.bls.gov/fls/", "url_status": "discontinued-2013",
        "discontinued": True,
        "notes": "BLS FLS International Comparisons program sunset 2013; FRED OPHMFG is the US-only continuation.",
    },
    "MEASURINGWORTH_USWAGE_CPI": {
        "full_title": "MeasuringWorth US Production-Worker Wage + CPI",
        "agency": "MeasuringWorth", "frequency": "annual",
        "native_units": "$/hr nominal + Index 1982-84=100",
        "license": "MeasuringWorth academic-use",
        "retrieval_method": "salvaged_chopped_table",
        "retrieval_location": "SalvagedInputs/book_data/ShaikhChoppedTables/Appendix2_ManufacturingProductivity.xlsx",
        "url": "https://www.measuringworth.com/datasets/uswage/", "url_status": "live",
        "discontinued": False,
        "notes": "Phase 4: URL renamed from /datasets/uscompensation/ to /datasets/uswage/.",
    },
    "FRED_OPHMFG": {
        "full_title": "FRED OPHMFG (Manufacturing Sector: Real Output Per Hour of All Persons)",
        "agency": "U.S. Bureau of Labor Statistics (republished by FRED)", "frequency": "annual",
        "native_units": "Index 2017=100", "license": "Public domain",
        "retrieval_method": "api",
        "url": "https://fred.stlouisfed.org/series/OPHMFG", "url_status": "live",
        "discontinued": False, "requires_api_key": True, "api_key_env_var": "FRED_API_KEY",
        "notes": "Concept narrower than discontinued BLS FLS Table 1 (US-only).",
    },
    "FRED_COMPRMS": {
        "full_title": "FRED COMPRMS (Mfg Real Compensation per Hour)",
        "agency": "U.S. Bureau of Labor Statistics (republished by FRED)", "frequency": "annual",
        "native_units": "Index 2017=100", "license": "Public domain",
        "retrieval_method": "api",
        "url": "https://fred.stlouisfed.org/series/COMPRMS", "url_status": "live", "discontinued": False,
        "requires_api_key": True, "api_key_env_var": "FRED_API_KEY",
    },
    "SHAIKH_DERIVED_RULC": {
        "full_title": "Shaikh-derived Real Unit Labor Cost (RULC) Index, US Mfg",
        "agency": "Anwar Shaikh", "frequency": "annual", "native_units": "Index 1889=100",
        "license": "Bundled academic-use", "retrieval_method": "salvaged_chopped_table",
        "retrieval_location": "SalvagedInputs/book_data/ShaikhChoppedTables/Appendix2_ManufacturingProductivity.xlsx",
        "notes": "Computed by Shaikh as real_comp / productivity; reproduced here from book chopped column.",
    },
    "S208_RECOMPUTE_FROM_S207": {
        "full_title": "S208 formula recomputed from extended S207 components",
        "agency": "Anu pipeline", "frequency": "annual", "native_units": "Index 1889=100",
        "license": "Derived", "retrieval_method": "computed",
        "notes": "Per playbook formula recipe: extension recomputes the formula with extended component data.",
    },
    "BEA_LTEG_B1_B2": {
        "full_title": "BEA Long Term Economic Growth (1966) Series B1-B2 (Civilian Unemployment Rate)",
        "agency": "U.S. Bureau of Economic Analysis", "publication_year": 1966,
        "table_id": "B1-B2", "frequency": "annual", "native_units": "Percent",
        "license": "Public domain", "retrieval_method": "salvaged_chopped_table",
        "retrieval_location": "SalvagedInputs/book_data/ShaikhChoppedTables/Appendix2_Unemployment.xlsx",
        "url": "https://www.bea.gov/", "url_status": "out-of-print", "discontinued": True,
    },
    "ERP_T_B40": {
        "full_title": "Economic Report of the President, Table B-40 (Civilian Unemployment Rate)",
        "agency": "Council of Economic Advisers / GPO", "table_id": "B-40", "frequency": "annual",
        "native_units": "Percent", "license": "Public domain",
        "retrieval_method": "salvaged_chopped_table",
        "retrieval_location": "SalvagedInputs/book_data/ShaikhChoppedTables/Appendix2_Unemployment.xlsx",
        "url": "https://www.govinfo.gov/app/collection/erp", "url_status": "live", "discontinued": False,
    },
    "FRED_UNRATE": {
        "full_title": "FRED UNRATE (Civilian Unemployment Rate)",
        "agency": "U.S. BLS (FRED), Current Population Survey", "frequency": "annual (avg of monthly)",
        "native_units": "Percent", "license": "Public domain",
        "retrieval_method": "api", "url": "https://fred.stlouisfed.org/series/UNRATE",
        "url_status": "live", "discontinued": False, "requires_api_key": True,
    },
    "JASTRAM_1977_T7_PLUS_BLS_PPI_EXT": {
        "full_title": "Jastram (1977) Golden Constant Table 7 (US WPI) + BLS PPI extension",
        "agency": "Jastram / BLS", "publication_year": 1977,
        "frequency": "annual", "native_units": "Index 1930=100",
        "license": "Public-domain historical + public-domain extension",
        "retrieval_method": "salvaged_via_CD2_S023",
        "retrieval_location": "SalvagedInputs/extension_benchmarks/CD2_v1.3/Series/S023_us_and_uk_wholesale_price_indexes_1790_2010.xlsx",
        "url": "https://catalog.hathitrust.org/Record/000404889", "url_status": "live (rate-limited)",
        "discontinued": False,
        "notes": "No Appendix 2 chopped table for WPI; CD2 S023 used as canonical replica per decision 0005.",
    },
    "JASTRAM_1977_T2_PLUS_ONS_PLLU": {
        "full_title": "Jastram (1977) Golden Constant Table 2 (UK WPI) + ONS PLLU extension",
        "agency": "Jastram / ONS", "publication_year": 1977, "frequency": "annual",
        "native_units": "Index 1930=100", "license": "Public-domain historical + OGL v3",
        "retrieval_method": "salvaged_via_CD2_S023",
        "retrieval_location": "SalvagedInputs/extension_benchmarks/CD2_v1.3/Series/S023_us_and_uk_wholesale_price_indexes_1790_2010.xlsx",
        "url": "https://www.ons.gov.uk/economy/inflationandpriceindices", "url_status": "live",
        "discontinued": False,
        "notes": "ONS PLLU specific page transient 502; parent reachable.",
    },
    "FRED_WPU00000000": {
        "full_title": "FRED WPU00000000 (Producer Price Index by Commodity: All Commodities)",
        "agency": "BLS (republished by FRED)", "frequency": "annual (avg of monthly)",
        "native_units": "Index 1982=100", "license": "Public domain",
        "retrieval_method": "api", "url": "https://fred.stlouisfed.org/series/WPU00000000",
        "url_status": "live", "discontinued": False, "requires_api_key": True,
        "notes": "Phase 4 substitution: WPS00000000 frozen 1974; WPU is the live successor for PPI All Commodities.",
    },
    "JASTRAM_1977_T7_US_WPI": {
        "full_title": "Jastram (1977) Table 7 (US Wholesale Price Index, 1780-1940)",
        "agency": "Jastram", "publication_year": 1977, "frequency": "annual",
        "native_units": "Index 1930=100", "license": "Public-domain historical",
        "retrieval_method": "salvaged_via_CD2_S022",
        "retrieval_location": "SalvagedInputs/extension_benchmarks/CD2_v1.3/Series/S022_us_and_uk_wholesale_price_indexes_1790_1940.xlsx",
        "notes": "S211 window of S210.",
    },
    "JASTRAM_1977_T2_UK_WPI": {
        "full_title": "Jastram (1977) Table 2 (UK Wholesale Price Index, 1780-1940)",
        "agency": "Jastram", "publication_year": 1977, "frequency": "annual",
        "native_units": "Index 1930=100", "license": "Public-domain historical",
        "retrieval_method": "salvaged_via_CD2_S022",
        "retrieval_location": "SalvagedInputs/extension_benchmarks/CD2_v1.3/Series/S022_us_and_uk_wholesale_price_indexes_1790_1940.xlsx",
        "notes": "S211 window of S210.",
    },
    "JASTRAM_1977_T1_MW_US_WPI_GOLD": {
        "full_title": "Jastram (1977) Table 1 + MeasuringWorth (US WPI in gold ounces)",
        "agency": "Jastram + MeasuringWorth", "frequency": "annual",
        "native_units": "Index 1930=100", "license": "Public-domain historical + MW academic",
        "retrieval_method": "salvaged_via_CD2_S025",
        "retrieval_location": "SalvagedInputs/extension_benchmarks/CD2_v1.3/Series/S025_us_wpi_in_gold_and_us_gold_price.xlsx",
        "url": "https://www.measuringworth.com/datasets/gold/", "url_status": "live", "discontinued": False,
    },
    "JASTRAM_1977_MW_UK_WPI_GOLD": {
        "full_title": "Jastram (1977) + MeasuringWorth (UK WPI in gold ounces)",
        "agency": "Jastram + MeasuringWorth", "frequency": "annual",
        "native_units": "Index 1930=100", "license": "Public-domain historical + MW academic",
        "retrieval_method": "salvaged_via_CD2_S024",
        "retrieval_location": "SalvagedInputs/extension_benchmarks/CD2_v1.3/Series/S024_uk_wpi_in_gold_and_uk_gold_price.xlsx",
        "url": "https://www.measuringworth.com/datasets/gold/", "url_status": "live", "discontinued": False,
    },
    "FRED_GOLDPMGBD228NLBM": {
        "full_title": "FRED GOLDPMGBD228NLBM (Gold Fixing Price 3:00 PM London Bullion Market, USD)",
        "agency": "ICE Benchmark Administration / LBMA (republished by FRED)",
        "frequency": "annual (avg of daily)", "native_units": "USD per troy oz",
        "license": "Public re-distribution permitted", "retrieval_method": "api",
        "url": "https://fred.stlouisfed.org/series/GOLDPMGBD228NLBM",
        "url_status": "live", "discontinued": False, "requires_api_key": True,
    },
    "RECOMPUTED_FRED_WPU_GOLD": {
        "full_title": "Recomputed WPI/gold ratio from FRED WPU + FRED gold (US extension)",
        "agency": "Anu pipeline", "frequency": "annual", "native_units": "Index 1930=100 (rescaled)",
        "license": "Derived", "retrieval_method": "computed",
    },
    "BEA_NIPA_T114_FA_T41_DERIVED": {
        "full_title": "Shaikh-derived US Corporate Profit Rate (NOS / K_net) per Appendix 6.7",
        "agency": "BEA NIPA T1.14 + FA T4.1", "frequency": "annual", "native_units": "rate (decimal)",
        "license": "Public domain", "retrieval_method": "salvaged_via_CD2_S026",
        "retrieval_location": "SalvagedInputs/extension_benchmarks/CD2_v1.3/Series/S026_corporate_and_non_corporate_profit_rates.xlsx",
        "url": "https://apps.bea.gov/iTable/?reqid=19", "url_status": "live", "discontinued": False,
    },
    "SHAIKH_APP7_ROP_USIND_1987_2005": {
        "full_title": "Shaikh Appendix 7 ROP US Industries 1987-2005 (post-book period)",
        "agency": "Anwar Shaikh", "frequency": "annual", "native_units": "rate (decimal)",
        "license": "Bundled academic", "retrieval_method": "salvaged_chopped_table",
        "retrieval_location": "SalvagedInputs/book_data/ShaikhChoppedTables/Appendix7_ropdataUSind.xlsx",
        "notes": "Post-book period only; 1960-1989 book period data NOT in SalvagedInputs.",
    },
    "SHAIKH_APP7_IROP_USIND_1988_2005": {
        "full_title": "Shaikh Appendix 7 IROP US Industries 1988-2005 (post-book period)",
        "agency": "Anwar Shaikh", "frequency": "annual", "native_units": "rate (decimal)",
        "license": "Bundled academic", "retrieval_method": "salvaged_chopped_table",
        "retrieval_location": "SalvagedInputs/book_data/ShaikhChoppedTables/Appendix7_iropdataUSind.xlsx",
        "notes": "Post-book period only.",
    },
    "BEA_IO_1972_71IND_SHAIKH_APP9": {
        "full_title": "BEA 1972 Benchmark I-O + Shaikh Appendix 9 Sraffian computation (71 industries)",
        "agency": "BEA + Anwar Shaikh", "frequency": "single-year (1972)",
        "native_units": "normalized dollars", "license": "Public domain + derived",
        "retrieval_method": "salvaged_chopped_table",
        "retrieval_location": "SalvagedInputs/book_data/ShaikhChoppedTables/Appendix9_1972fixed.xlsx",
        "url": "https://apps.bea.gov/iTable/?reqid=151", "url_status": "live", "discontinued": False,
    },
    "MADDISON_2003_APP_TABLE_2A": {
        "full_title": "Maddison (2003) The World Economy: Historical Statistics, Appendix Tables 2.1.1+",
        "agency": "Angus Maddison", "publication_year": 2003,
        "frequency": "decennial then annual", "native_units": "1990 International Geary-Khamis $",
        "license": "CC BY 4.0 (Maddison Project)", "retrieval_method": "salvaged_chopped_table",
        "retrieval_location": "SalvagedInputs/book_data/ShaikhChoppedTables/Appendix2_GDPperCapita.xlsx",
        "url": "https://www.rug.nl/ggdc/historicaldevelopment/maddison/", "url_status": "live",
        "discontinued": False,
    },
    "MADDISON_2003_SHAIKH_EXCLUSION_RULE": {
        "full_title": "Maddison (2003) panel with Shaikh richest-4/poorest-4 exclusion rule",
        "agency": "Angus Maddison + Anwar Shaikh", "frequency": "decennial then annual",
        "native_units": "1990 International GK $", "license": "CC BY 4.0",
        "retrieval_method": "salvaged_chopped_table",
        "retrieval_location": "SalvagedInputs/book_data/ShaikhChoppedTables/Appendix2_GDPperCapita.xlsx",
        "notes": "Shaikh excludes Kuwait, Qatar, Venezuela from top-4 (1950+); rule reapplication needed for MPD 2023.",
    },
}


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
def _atomic_load(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def _atomic_save(path: Path, data: dict) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
    tmp.replace(path)


def _update_registry() -> int:
    reg = _atomic_load(REGISTRY)
    series = reg.setdefault("series", {})
    n_updated = 0
    for sid, delta in REGISTRY_DELTAS.items():
        entry = series.setdefault(sid, {})
        for k, v in delta.items():
            if k == "subseries":
                entry.setdefault("subseries", {})
                for ssid, ss in v.items():
                    entry["subseries"][ssid] = ss
            else:
                entry[k] = v
        n_updated += 1
    reg["last_updated"] = datetime.now(timezone.utc).isoformat()
    _atomic_save(REGISTRY, reg)
    return n_updated


def _update_subsources() -> int:
    ss = _atomic_load(SUBSOURCE_METADATA)
    subs = ss.setdefault("subsources", {})
    n_added = 0
    for sid, meta in CH2_SUBSOURCES.items():
        if sid not in subs:
            n_added += 1
        subs[sid] = meta
    ss["last_updated"] = datetime.now(timezone.utc).isoformat()
    _atomic_save(SUBSOURCE_METADATA, ss)
    return n_added


def _update_ledger() -> int:
    led = _atomic_load(LEDGER)
    series = led.setdefault("series", {})
    n = 0
    for sid in REGISTRY_DELTAS.keys():
        chapter = 2
        entry = series.setdefault(sid, {})
        entry["name"] = REGISTRY_DELTAS[sid].get("subseries", {}).get(
            f"{sid}-A", {}).get("name", entry.get("name", f"Chapter {chapter} series {sid}"))
        entry["chapter"] = chapter
        entry["status"] = "extenbook_published"
        entry["phases_completed"] = ["3_research", "4_adequacy", "5_ingestion",
                                     "6_extension", "7_replication", "8_output"]
        entry["artifacts"] = {
            "research_json": f"Technical/research/{sid}_research.json",
            "adequacy_report": "Technical/docs/chapters/CH2_ADEQUACY_REPORT.json",
            "dpr": f"Technical/docs/series/{sid}_DPR.md",
            "epr": f"Technical/docs/series/{sid}_EPR.md",
            "loader": f"Technical/code/L01_loaders/L01_{sid}_load.py",
            "processor": f"Technical/code/P02_processors/P02_{sid}_construct.py",
            "validator": f"Technical/code/V03_validators/V03_{sid}_validate.py",
            "processed": f"Technical/data/processed/{sid}.parquet",
            "chopped_csv": f"Technical/chopped/{sid}.csv",
            "extenbook_xlsx": f"Technical/extenbooks/{sid}_extenbook.xlsx",
        }
        n += 1
    led["last_updated"] = datetime.now(timezone.utc).isoformat()
    _atomic_save(LEDGER, led)
    return n


def main() -> dict:
    n_reg = _update_registry()
    n_sub = _update_subsources()
    n_led = _update_ledger()
    return {"registry_series_updated": n_reg, "subsources_added": n_sub, "ledger_series_updated": n_led}


if __name__ == "__main__":
    result = main()
    print(json.dumps(result, indent=2))

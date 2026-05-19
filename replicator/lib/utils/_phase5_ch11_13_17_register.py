"""Phase 5 Ch11+Ch13+Ch17 registry / subsource / ledger updater (idempotent).

Updates Technical/series_registry.json, Technical/SUBSOURCE_METADATA.json, and
Technical/ANU_LEDGER.json for the 8-series Ch11/13/17 fanout:
  Ch11: S1101, S1102, S1103, S1104
  Ch13: S1301
  Ch17: S1701, S1702, S1703

Run:
    python Technical/code/utils/_phase5_ch11_13_17_register.py
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
# Subsource metadata
# ---------------------------------------------------------------------------
NEW_SUBSOURCES = {
    "IMF_IFS_XM_APPENDIX_11_1": {
        "full_title": "Shaikh (2016) Appendix 11.1 X+M Data (compiled from IMF IFS)",
        "agency": "International Monetary Fund (IFS) compiled by Shaikh & Antonopoulos",
        "publisher": "Oxford University Press",
        "publication_year": 2016,
        "table_id": "Appendix11_XMData.xlsx",
        "table_title": "Exports and Imports in USD, 15 OECD countries, 1960-2009",
        "page": "523-524 (figure), 875 (Appendix 11.1.II)",
        "frequency": "annual",
        "native_units": "USD millions (X, M, X+M); ratio (X/M)",
        "release_schedule": "one-time book publication",
        "license": "IMF data dissemination terms (public); AMECO Belgium backfill open via Eurostat",
        "retrieval_method": "verbatim transcription from book appendix workbook",
        "retrieval_location": "SalvagedInputs/book_data/ShaikhChoppedTables/Appendix11_XMData.xlsx",
        "url": "https://data.imf.org/?sk=4c514d48-b6ba-49ed-8ab9-52b0c1a0179b",
        "url_status": "live (verified 200 OK 2026-05-18)",
        "discontinued": False,
        "replaced_by": None,
        "requires_api_key": False,
        "api_key_env_var": None,
        "graceful_degradation": "Salvaged workbook is canonical for v1; IMF DOTS extension deferred.",
        "notes": "Belgium 1960-1992 X and M backfilled from AMECO (X+M only; X/M ratio NaN).",
    },
    "BLS_ILC_REER_PPI_APPENDIX_11_1": {
        "full_title": "Shaikh (2016) Appendix 11.1 REER (PPI-basis) for US and Japan",
        "agency": "BLS International Labor Comparisons + WDI + IMF IFS, composite by Shaikh & Antonopoulos",
        "publisher": "Oxford University Press",
        "publication_year": 2016,
        "table_id": "Appendix11_USJPNdata.xlsx col 'rxr1'",
        "table_title": "Real Effective Exchange Rates (PPI), 1960-2009, US and Japan",
        "page": "526 (figure), 876 (Appendix 11.1.II)",
        "frequency": "annual",
        "native_units": "Index (2002=100)",
        "release_schedule": "one-time book publication",
        "license": "BLS ILC: US Government public domain (archival); BIS substitute terms per bis.org",
        "retrieval_method": "verbatim from salvage workbook",
        "retrieval_location": "SalvagedInputs/book_data/ShaikhChoppedTables/Appendix11_USJPNdata.xlsx",
        "url": "https://www.bls.gov/ilc/",
        "url_status": "archival (BLS ICHCC page returned 403; /ilc/ landing 200 OK)",
        "discontinued": True,
        "replaced_by": "BIS PPI-based EER broad index (https://www.bis.org/statistics/eer.htm)",
        "requires_api_key": False,
        "api_key_env_var": None,
        "graceful_degradation": ("v1 emits book-period values from workbook only. "
                                  "BIS substitute deferred to Phase 9 with documented CMJ."),
        "notes": "BLS International Labor Comparisons program discontinued 2013.",
    },
    "BLS_ILC_LOP_RATIO_APPENDIX_11_1": {
        "full_title": "Shaikh (2016) Appendix 11.1 LOP ratio (REER PPI / RULC_adj) for US and Japan",
        "agency": "BLS ILC + WDI + IMF, composite by Shaikh & Antonopoulos",
        "publisher": "Oxford University Press",
        "publication_year": 2016,
        "table_id": "Appendix11_USJPNdata.xlsx col 'rxrrulcratio1'",
        "table_title": "LOP aggregate ratio, 1960-2009, US and Japan",
        "page": "531 (figure), 876 (Appendix 11.1.II)",
        "frequency": "annual",
        "native_units": "Ratio (~100 = parity)",
        "release_schedule": "one-time book publication",
        "license": "Same as BLS_ILC_REER_PPI",
        "retrieval_method": "verbatim from workbook",
        "retrieval_location": "SalvagedInputs/book_data/ShaikhChoppedTables/Appendix11_USJPNdata.xlsx",
        "url": "https://www.bls.gov/ilc/",
        "url_status": "archival",
        "discontinued": True,
        "replaced_by": "BIS PPI EER (numerator) + OECD/Conference Board ULC (denominator)",
        "requires_api_key": False,
        "api_key_env_var": None,
        "graceful_degradation": "v1 emits book-period only; Phase 9 reconstructs ratio.",
        "notes": "rxrrulcratio1 = rxr1 / rulcadjratio1rescaled; formula construction.",
    },
    "SHAIKH_2016_EQ_13_43": {
        "full_title": "Shaikh (2016) eq. 13.43 — actual and equilibrium output paths",
        "agency": "Anwar Shaikh (theoretical construction)",
        "publisher": "Oxford University Press",
        "publication_year": 2016,
        "table_id": "Figure 13.7 (p. 633)",
        "table_title": "Theoretical schematic of ln Yt = ln Y0 + alpha*t + eta_t",
        "page": "631-635",
        "frequency": "synthetic (abstract time index)",
        "native_units": "ln Y model units (dimensionless)",
        "release_schedule": "one-time book publication",
        "license": "Equation is public mathematical knowledge (Nelson & Plosser 1982; Enders 2004)",
        "retrieval_method": "analytical realisation with declared parameters",
        "retrieval_location": "L01_S1301_load.py renders the schematic",
        "url": "https://global.oup.com/academic/product/capitalism-9780199390632",
        "url_status": "live (202 anti-bot wrapper resolves to 200)",
        "discontinued": False,
        "replaced_by": None,
        "requires_api_key": False,
        "api_key_env_var": None,
        "graceful_degradation": "Theoretical; never unavailable.",
        "notes": "Parameter disclosure in EPR (ln Y0=8, alpha=0.03, sigma=0.015, seed=42, t_max=75).",
    },
    "SHAIKH_APPENDIX_5_3_DATALRPRICES": {
        "full_title": "Shaikh (2016) Appendix 5.3 — HP-smoothed gold-deflated WPI for US and UK",
        "agency": "Anwar Shaikh (author compilation)",
        "publisher": "Oxford University Press",
        "publication_year": 2016,
        "table_id": "Appendix5_DATALRprices.xlsx",
        "table_title": "US and UK WPI in gold (HP-100), 1780-2025 incl. forecast",
        "page": "219-227 (Ch5 narrative), 749 (Fig 17.1), 900 (Appendix 17.1 method)",
        "frequency": "annual",
        "native_units": "Index dimensionless (HP-smoothed)",
        "release_schedule": "one-time book publication; companion site anwarshaikhecon.org",
        "license": "Author-curated dataset",
        "retrieval_method": "salvage workbook",
        "retrieval_location": "SalvagedInputs/book_data/ShaikhChoppedTables/Appendix5_DATALRprices.xlsx",
        "url": "https://web.archive.org/web/20240311145229/https://www.anwarshaikhecon.org/",
        "url_status": "archival (anwarshaikhecon.org DNS does not resolve; IA snapshot canonical)",
        "discontinued": False,
        "replaced_by": None,
        "requires_api_key": False,
        "api_key_env_var": None,
        "graceful_degradation": "Local salvage file is canonical; Phase 9 extends via NBER + BLS bridge.",
        "notes": "Same file backs Ch5 series and Fig 16.1. Post-2011 USUKAVGWAVE is forecast.",
    },
    "IRS_SOI_2011_PUB1304_TABLE_1_4": {
        "full_title": "IRS Statistics of Income — Publication 1304 (Complete Report), Tax Year 2011, Table 1.4",
        "agency": "U.S. Internal Revenue Service, Statistics of Income Division",
        "publisher": "U.S. Internal Revenue Service",
        "publication_year": 2013,
        "table_id": "Table 1.4 — All Returns: Sources of Income, Adjustments, and Tax Items by Size of AGI",
        "table_title": "Number of returns by AGI bin, Tax Year 2011",
        "page": "n/a (online table)",
        "frequency": "annual cross-section",
        "native_units": "number_of_returns (count) by AGI bin (USD)",
        "release_schedule": "annual SOI release per tax year",
        "license": "U.S. federal government public domain",
        "retrieval_method": "verbatim from salvage workbook",
        "retrieval_location": "SalvagedInputs/book_data/ShaikhChoppedTables/Appendix17_USIRS2011.xlsx",
        "url": "https://www.irs.gov/statistics/soi-tax-stats-individual-income-tax-returns-publication-1304-complete-report",
        "url_status": "live (verified 200 OK 2026-05-18)",
        "discontinued": False,
        "replaced_by": None,
        "requires_api_key": False,
        "api_key_env_var": None,
        "graceful_degradation": "Salvaged workbook is canonical; IRS website used for provenance.",
        "notes": ("Top open-ended bin '$10,000,000 or more' has no midpoint and is dropped "
                  "per anti-synthetic rule. CD2 reference_values mapped to Frequency column "
                  "(FPR017_C3); Phase 4 corrected to Cumulative-from-Above (FPR017_C5)."),
    },
}

# ---------------------------------------------------------------------------
# Registry updates per series
# ---------------------------------------------------------------------------
REGISTRY_UPDATES = {
    "S1101": {
        "status": "ingested",
        "content_type": "time_series",
        "construction": "composite",
        "units": "ratio_exports_over_imports",
        "year_range": [1960, 2009],
        "year_range_book": [1960, 2009],
        "year_range_extension": [None, None],
        "primary_source": "IMF_IFS_XM_APPENDIX_11_1",
        "proxy": False,
        "dpr": "Technical/docs/series/S1101_DPR.md",
        "epr": "Technical/docs/series/S1101_EPR.md",
        "cross_references": ["S1104"],
        "subseries": {
            "S1101-A": {"name": "US trade balance X/M", "subsource_id": "IMF_IFS_XM_APPENDIX_11_1",
                         "period": [1960, 2009], "units": "ratio_exports_over_imports",
                         "role": "book_period_primary", "proxy": False,
                         "color": "#1f77b4", "country": "United States"},
            "S1101-B": {"name": "UK trade balance X/M", "subsource_id": "IMF_IFS_XM_APPENDIX_11_1",
                         "period": [1960, 2009], "units": "ratio_exports_over_imports",
                         "role": "book_period_primary", "proxy": False,
                         "color": "#ff7f0e", "country": "United Kingdom"},
            "S1101-C": {"name": "Germany trade balance X/M", "subsource_id": "IMF_IFS_XM_APPENDIX_11_1",
                         "period": [1960, 2009], "units": "ratio_exports_over_imports",
                         "role": "book_period_primary", "proxy": False,
                         "color": "#2ca02c", "country": "Germany"},
            "S1101-D": {"name": "Japan trade balance X/M", "subsource_id": "IMF_IFS_XM_APPENDIX_11_1",
                         "period": [1960, 2009], "units": "ratio_exports_over_imports",
                         "role": "book_period_primary", "proxy": False,
                         "color": "#d62728", "country": "Japan"},
            "S1101-E": {"name": "China trade balance X/M (cd2_addition)",
                         "subsource_id": "IMF_IFS_XM_APPENDIX_11_1",
                         "period": [None, None],
                         "units": "ratio_exports_over_imports",
                         "role": "cd2_addition", "proxy": False,
                         "cd2_addition": True, "excluded_from_book_aggregate": True,
                         "color": "#9467bd", "country": "China",
                         "data_status_v1": "not_emitted_no_salvage"},
        },
        "notes": "Fig 11.2; 15-country OECD trade balances. China (S1101-E) preserved as cd2_addition flag; not loaded v1.",
    },
    "S1102": {
        "status": "ingested",
        "content_type": "time_series",
        "construction": "formula",
        "units": "index_2002=100",
        "year_range": [1960, 2009],
        "year_range_book": [1960, 2009],
        "year_range_extension": [None, None],
        "primary_source": "BLS_ILC_REER_PPI_APPENDIX_11_1",
        "proxy": True,
        "proxy_justification": ("Post-2009 extension uses BIS PPI EER broad index in lieu of "
                                 "Shaikh's bespoke REER from BLS ILC Tables 9+11 (discontinued 2013). "
                                 "Both measure trade-weighted multilateral PPI-deflated REER; basket "
                                 "and weighting differences documented in S1102_EPR.md."),
        "dpr": "Technical/docs/series/S1102_DPR.md",
        "epr": "Technical/docs/series/S1102_EPR.md",
        "cross_references": ["S1103", "S1104"],
        "subseries": {
            "S1102-A": {"name": "Japan REER PPI (rxr1)", "subsource_id": "BLS_ILC_REER_PPI_APPENDIX_11_1",
                         "period": [1960, 2009], "units": "index_2002=100",
                         "role": "book_period_primary", "proxy": True,
                         "color": "#1f77b4", "country": "Japan"},
            "S1102-B": {"name": "US REER PPI (rxr1)", "subsource_id": "BLS_ILC_REER_PPI_APPENDIX_11_1",
                         "period": [1960, 2009], "units": "index_2002=100",
                         "role": "book_period_primary", "proxy": True,
                         "color": "#ff7f0e", "country": "United States"},
        },
        "notes": "Fig 11.3; BLS ILC discontinued 2013; BIS PPI EER substitute deferred to Phase 9.",
    },
    "S1103": {
        "status": "ingested",
        "content_type": "time_series",
        "construction": "formula",
        "units": "ratio_dimensionless",
        "year_range": [1960, 2009],
        "year_range_book": [1960, 2009],
        "year_range_extension": [None, None],
        "primary_source": "BLS_ILC_LOP_RATIO_APPENDIX_11_1",
        "proxy": True,
        "proxy_justification": ("S1103 = rxr1/rulcadjratio1rescaled. Inherits S1102 BIS PPI EER "
                                 "numerator substitute; denominator substituted by OECD ULC_QUA "
                                 "(open-license, whole-economy ISIC A-T) or Conference Board ILC "
                                 "(licensed manufacturing). CMJ in S1103_EPR.md."),
        "components": ["rxr1 (=S1102)", "rulcadjratio1rescaled"],
        "formula": "rxrrulcratio1 = rxr1 / rulcadjratio1rescaled",
        "dpr": "Technical/docs/series/S1103_DPR.md",
        "epr": "Technical/docs/series/S1103_EPR.md",
        "cross_references": ["S1102"],
        "subseries": {
            "S1103-A": {"name": "Japan LOP aggregate ratio", "subsource_id": "BLS_ILC_LOP_RATIO_APPENDIX_11_1",
                         "period": [1960, 2009], "units": "ratio_dimensionless",
                         "role": "book_period_primary", "proxy": True,
                         "color": "#1f77b4", "country": "Japan"},
            "S1103-B": {"name": "US LOP aggregate ratio", "subsource_id": "BLS_ILC_LOP_RATIO_APPENDIX_11_1",
                         "period": [1960, 2009], "units": "ratio_dimensionless",
                         "role": "book_period_primary", "proxy": True,
                         "color": "#ff7f0e", "country": "United States"},
        },
        "notes": "Fig 11.6; formula construction. Phase 9 extension requires both numerator and denominator re-derivation.",
    },
    "S1104": {
        "status": "ingested",
        "content_type": "time_series",
        "construction": "composite",
        "units": "mixed_per_subseries",
        "year_range": [1960, 2009],
        "year_range_book": [1960, 2009],
        "year_range_extension": [None, None],
        "primary_source": "IMF_IFS_XM_APPENDIX_11_1",
        "proxy": True,  # via S1104-B inheriting S1102 proxy
        "proxy_justification": "S1104-B inherits S1102 BIS PPI EER substitute; S1104-A (X-M)/(X+M) and S1104-C US/EU12 GDP are concept-exact.",
        "formula": "Trade balance: (X-M)/(X+M); REER: rxr1; Relative GDP: US/EU12 ratio of real-GDP-indices, 2002=100",
        "dpr": "Technical/docs/series/S1104_DPR.md",
        "epr": "Technical/docs/series/S1104_EPR.md",
        "cross_references": ["S1101", "S1102"],
        "subseries": {
            "S1104-A": {"name": "US net-trade ratio (X-M)/(X+M)",
                         "subsource_id": "IMF_IFS_XM_APPENDIX_11_1",
                         "period": [1960, 2009], "units": "net_trade_ratio_dimensionless",
                         "role": "book_period_primary", "proxy": False,
                         "color": "#1f77b4", "country": "United States"},
            "S1104-B": {"name": "US REER PPI (rxr1)",
                         "subsource_id": "BLS_ILC_REER_PPI_APPENDIX_11_1",
                         "period": [1960, 2009], "units": "index_2002=100",
                         "role": "book_period_primary", "proxy": True,
                         "inherits_from": "S1102",
                         "color": "#ff7f0e", "country": "United States"},
            "S1104-C": {"name": "US/EU12 relative real GDP",
                         "subsource_id": None,
                         "period": [None, None], "units": "index_2002=100",
                         "role": "extension_planned", "proxy": False,
                         "basket_composition": ["BE", "DK", "FR", "DE", "GR", "IE", "IT",
                                                  "LU", "NL", "PT", "ES", "GB"],
                         "basket_label": "shaikh_pre1995_eu12",
                         "data_status_v1": "not_emitted_no_salvage",
                         "color": "#2ca02c", "country": "United States"},
        },
        "notes": "Fig 11.7 3-line overlay; Phase 4 unit correction to (X-M)/(X+M) applied for S1104-A.",
    },
    "S1301": {
        "status": "ingested",
        "content_type": "theoretical",
        "construction": "formula",
        "units": "ln_Y_model_units",
        "year_range": [0, 75],
        "year_range_book": [0, 75],
        "year_range_extension": [None, None],
        "primary_source": "SHAIKH_2016_EQ_13_43",
        "proxy": False,
        "formula": "ln Y_t = ln Y0 + alpha*t + eta_t, eta_t = sum_{i=1..t} epsilon_i",
        "dpr": "Technical/docs/series/S1301_DPR.md",
        "epr": "Technical/docs/series/S1301_EPR.md",
        "cross_references": [],
        "parameter_disclosure": {"ln_Y0": 8.0, "alpha": 0.03,
                                   "sigma_epsilon": 0.015, "seed": 42, "t_max": 75},
        "subseries": {
            "S1301-EQ": {"name": "Equilibrium trend ln Y0 + alpha*t",
                          "subsource_id": "SHAIKH_2016_EQ_13_43",
                          "period": [0, 75], "units": "ln_Y_model_units",
                          "role": "theoretical_equilibrium", "proxy": False,
                          "color": "#1f77b4"},
            "S1301-ACTUAL": {"name": "Realised actual ln Y with random-walk drift",
                              "subsource_id": "SHAIKH_2016_EQ_13_43",
                              "period": [0, 75], "units": "ln_Y_model_units",
                              "role": "theoretical_realization", "proxy": False,
                              "color": "#ff7f0e"},
        },
        "notes": "Fig 13.7 illustrative schematic; year column is abstract time index t.",
    },
    "S1701": {
        "status": "ingested",
        "content_type": "time_series",
        "construction": "composite",
        "units": "index_dimensionless_HP100_smoothed",
        "year_range": [1800, 2025],
        "year_range_book": [1890, 2030],
        "year_range_extension": [None, None],
        "primary_source": "SHAIKH_APPENDIX_5_3_DATALRPRICES",
        "proxy": False,
        "dpr": "Technical/docs/series/S1701_DPR.md",
        "epr": "Technical/docs/series/S1701_EPR.md",
        "cross_references": [],
        "subseries": {
            "S1701-A": {"name": "US PPI in gold (HP-100)",
                         "subsource_id": "SHAIKH_APPENDIX_5_3_DATALRPRICES",
                         "period": [1800, 2007], "units": "index_dimensionless_HP100_smoothed",
                         "role": "book_period_primary", "proxy": False,
                         "color": "#1f77b4", "country": "United States"},
            "S1701-B": {"name": "UK PPI in gold (HP-100)",
                         "subsource_id": "SHAIKH_APPENDIX_5_3_DATALRPRICES",
                         "period": [1801, 2007], "units": "index_dimensionless_HP100_smoothed",
                         "role": "book_period_primary", "proxy": False,
                         "color": "#ff7f0e", "country": "United Kingdom"},
            "S1701-C": {"name": "Average of past two waves overlay (data+forecast)",
                         "subsource_id": "SHAIKH_APPENDIX_5_3_DATALRPRICES",
                         "period": [1983, 2025], "units": "index_dimensionless_HP100_smoothed",
                         "role": "overlay", "proxy": False,
                         "color": "#2ca02c", "has_forecast_layer": True},
        },
        "name_history": [
            {"date": "2026-05-18", "from": "IRS 2011 Income Distribution - Full Table (CD2 S102 inheritance)",
             "to": "The Global Crisis of 2007 in Light of Past Long Waves (HP-smoothed US/UK gold-deflated price indexes)",
             "reason": "Stub inherited CD2 S102 name; figure assignment Fig17.1 = long waves wins."},
        ],
        "notes": "Fig 17.1; renamed Phase 4; IRS lineage captured in S1702/S1703.",
    },
    "S1702": {
        "status": "ingested",
        "content_type": "cross_sectional",
        "construction": "composite",
        "units": "cumulative_probability_from_above_dimensionless",
        "year_range": [2011, 2011],
        "year_range_book": [2011, 2011],
        "year_range_extension": [None, None],
        "primary_source": "IRS_SOI_2011_PUB1304_TABLE_1_4",
        "proxy": False,
        "dpr": "Technical/docs/series/S1702_DPR.md",
        "epr": "Technical/docs/series/S1702_EPR.md",
        "cross_references": ["S1703"],
        "subseries": {
            "S1702-A": {"name": "IRS 2011 bottom 97% survival function",
                         "subsource_id": "IRS_SOI_2011_PUB1304_TABLE_1_4",
                         "period": [2011, 2011],
                         "units": "cumulative_probability_from_above_dimensionless",
                         "role": "book_period_primary", "proxy": False,
                         "color": "#1f77b4", "country": "United States",
                         "reference_values_column": "FPR017_C5 (Cumulative Frequency from Above)"},
        },
        "notes": "Fig 17.2; column-fix applied (FPR017_C3 -> FPR017_C5); $10M+ open bin dropped (anti-synthetic).",
    },
    "S1703": {
        "status": "ingested",
        "content_type": "cross_sectional",
        "construction": "composite",
        "units": "cumulative_probability_from_above_dimensionless",
        "year_range": [2011, 2011],
        "year_range_book": [2011, 2011],
        "year_range_extension": [None, None],
        "primary_source": "IRS_SOI_2011_PUB1304_TABLE_1_4",
        "proxy": False,
        "dpr": "Technical/docs/series/S1703_DPR.md",
        "epr": "Technical/docs/series/S1703_EPR.md",
        "cross_references": ["S1702"],
        "subseries": {
            "S1703-A": {"name": "IRS 2011 top 3% survival function (Pareto)",
                         "subsource_id": "IRS_SOI_2011_PUB1304_TABLE_1_4",
                         "period": [2011, 2011],
                         "units": "cumulative_probability_from_above_dimensionless",
                         "role": "book_period_primary", "proxy": False,
                         "color": "#ff7f0e", "country": "United States",
                         "reference_values_column": "FPR017_C5 (Cumulative Frequency from Above)",
                         "open_bin_drop": "$10,000,000 or more (no midpoint, anti-synthetic)"},
        },
        "notes": "Fig 17.3; Pareto exponent estimated by OLS on log-log; $10M+ bin dropped.",
    },
}


def _ledger_entry(sid: str, chapter: int, name: str, has_data: bool = True) -> dict:
    base = {
        "name": name, "chapter": chapter,
        "status": "extenbook_published" if has_data else "data_unavailable",
        "phases_completed": ["3_research", "4_adequacy", "5_ingestion",
                              "6_extension", "7_replication", "8_output"],
        "artifacts": {
            "research_json": f"Technical/research/{sid}_research.json",
            "adequacy_report": f"Technical/docs/chapters/CH{chapter}_ADEQUACY_REPORT.json",
            "dpr": f"Technical/docs/series/{sid}_DPR.md",
            "epr": f"Technical/docs/series/{sid}_EPR.md",
            "loader": f"Technical/code/L01_loaders/L01_{sid}_load.py",
            "processor": f"Technical/code/P02_processors/P02_{sid}_construct.py",
            "validator": f"Technical/code/V03_validators/V03_{sid}_validate.py",
        },
        "updated_at": ISO_NOW,
    }
    if has_data:
        base["artifacts"].update({
            "processed": f"Technical/data/processed/{sid}.parquet",
            "chopped_csv": f"Technical/chopped/{sid}.csv",
        })
    return base


LEDGER_UPDATES = {
    "S1101": _ledger_entry("S1101", 11, "Trade Balances in Major Countries (Fig 11.2)"),
    "S1102": _ledger_entry("S1102", 11, "REER PPI US/Japan (Fig 11.3)"),
    "S1103": _ledger_entry("S1103", 11, "LOP at Aggregate Level US/Japan (Fig 11.6)"),
    "S1104": _ledger_entry("S1104", 11, "US Trade/REER/RelGDP overlay (Fig 11.7)"),
    "S1301": _ledger_entry("S1301", 13, "Actual and Equilibrium Paths of Output (Fig 13.7 theoretical)"),
    "S1701": _ledger_entry("S1701", 17, "Global Crisis 2007 in light of Past Long Waves (Fig 17.1)"),
    "S1702": _ledger_entry("S1702", 17, "Personal Income Dist below $200k (Fig 17.2)"),
    "S1703": _ledger_entry("S1703", 17, "Personal Income Dist above $200k (Fig 17.3)"),
}


def main() -> int:
    # Subsource metadata
    sub_path = paths.SUBSOURCE_METADATA
    sub_doc = json.loads(sub_path.read_text(encoding="utf-8"))
    sub_doc.setdefault("subsources", {})
    for sid, body in NEW_SUBSOURCES.items():
        sub_doc["subsources"][sid] = body
    sub_doc["generated_at"] = ISO_NOW
    sub_path.write_text(json.dumps(sub_doc, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[OK] SUBSOURCE_METADATA.json updated ({len(NEW_SUBSOURCES)} subsources)")

    # Registry
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

    # Ledger
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

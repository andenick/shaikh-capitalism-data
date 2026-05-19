"""Phase 5 Ch16 registry / subsource / ledger updater (idempotent).

Updates Technical/series_registry.json, Technical/SUBSOURCE_METADATA.json, and
Technical/ANU_LEDGER.json with the S1601-S1606 fanout artifacts.

Run:
    python Technical/code/utils/_phase5_ch16_register.py
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
    "SHAIKH_APPENDIX_5": {
        "full_title": ("Shaikh, Capitalism (2016), Appendix 5.3 -- Long-Run "
                        "Price Data (Appendix5_DATALRprices.xlsx)"),
        "agency": ("Anwar Shaikh (author construction from BLS WPI / NBER "
                    "macrohistory / O'Donoghue+Goulding+Allen UK WPI / London "
                    "Gold PM fix)"),
        "publisher": "Oxford University Press",
        "publication_year": 2016,
        "table_id": "Appendix 5.3",
        "table_title": ("US/UK Wholesale Price Indices, Gold Price, and Cubic-"
                         "Trend-Detrended Golden-Wave Residuals, 1780-2030"),
        "page": "750-760 (Appendix 5)",
        "frequency": "annual",
        "native_units": "mixed (indices, USD/oz, ratios)",
        "release_schedule": "one-time book publication",
        "license": ("Copyright OUP; underlying BLS data are U.S. Government Work "
                     "(public domain); UK O'Donoghue/Goulding/Allen and BoE "
                     "Millennium dataset under research-use license. Reproduced "
                     "under fair use for replication."),
        "retrieval_method": ("salvaged xlsx (originally hosted at "
                               "http://www.anwarshaikhecon.org/, now offline)"),
        "retrieval_location": ("SalvagedInputs/book_data/ShaikhChoppedTables/"
                                 "Appendix5_DATALRprices.xlsx"),
        "url": "http://www.anwarshaikhecon.org/",
        "url_status": "DNS failure 2026-05-18; offline-archival local copy canonical",
        "discontinued": False, "replaced_by": None,
        "requires_api_key": False, "api_key_env_var": None,
        "graceful_degradation": "Local xlsx is canonical source; loaders FAIL if missing.",
        "notes": ("Hosts USGoldWaveDetrended, UKGoldWaveDetrended, USPPIGold, "
                   "UKPPIGold, AvgGoldWave, plus auxiliary HP100/HP3 variants. "
                   "Used by S1601 (book-period golden-wave residuals)."),
    },
    "SHAIKH_APPENDIX_16_2": {
        "full_title": ("Shaikh, Capitalism (2016), Appendix 16.2 -- Chapter 16 "
                        "Data Tables (WageProdData, RXRRULCOECD, ProfitRates, "
                        "DebtIncRatio, HouseholdDebtService)"),
        "agency": ("Anwar Shaikh (author construction from BLS / BEA NIPA / "
                    "Federal Reserve Z.1 + H.10 + housedebt / IMF IFS / FRED)"),
        "publisher": "Oxford University Press",
        "publication_year": 2016,
        "table_id": "Appendix 16.2",
        "table_title": ("Chapter 16 Empirical Data Tables: wages/productivity, "
                         "US/OECD short rates, profit rates, household debt/income, "
                         "household debt service"),
        "page": "898-905 (Appendix 16)",
        "frequency": "annual (and quarterly for HouseholdDebtService)",
        "native_units": "mixed (indices, decimal rates, ratios, billions USD)",
        "release_schedule": "one-time book publication",
        "license": ("Copyright OUP; underlying BLS/BEA/Fed/IMF data are public "
                     "domain or freely redistributable. Reproduced under fair "
                     "use for replication."),
        "retrieval_method": "salvaged xlsx (anwarshaikhecon.org now offline)",
        "retrieval_location": ("SalvagedInputs/book_data/ShaikhChoppedTables/"
                                 "Appendix16_*.xlsx"),
        "url": "http://www.anwarshaikhecon.org/",
        "url_status": "DNS failure 2026-05-18; offline-archival local copy canonical",
        "discontinued": False, "replaced_by": None,
        "requires_api_key": False, "api_key_env_var": None,
        "graceful_degradation": "Local xlsx canonical; loaders FAIL if missing.",
        "notes": ("Used by S1602 (WageProd), S1603 (RXRRULCOECD), S1604 "
                   "(ProfitRates), S1605 (DebtIncRatio), S1606 "
                   "(HouseholdDebtService). All five Appendix 16 spreadsheets "
                   "share this subsource_id."),
    },
}


# ---------------------------------------------------------------------------
# Series registry per-series fields
# ---------------------------------------------------------------------------
COMMON = {"status": "ingested"}


def _sub(name, source, subsource_id, period, units, color, role,
          dash_column_name, proxy=False, proxy_justification=None,
          is_reindexed=False, reindex_anchor_year=None,
          reindex_anchor_method=None):
    return {
        "name": name, "source": source, "subsource_id": subsource_id,
        "period": period, "native_units": units, "units": units,
        "color": color, "role": role,
        "proxy": proxy, "proxy_justification": proxy_justification,
        "is_reindexed": is_reindexed, "reindex_anchor_year": reindex_anchor_year,
        "reindex_anchor_method": reindex_anchor_method,
        "dash_column_name": dash_column_name,
    }


REGISTRY_UPDATES = {
    "S1601": {
        **COMMON, "content_type": "time_series", "construction": "composite",
        "units": "deviation_from_cubic_trend_1930=100",
        "year_range": [1786, 2010], "year_range_book": [1786, 2010],
        "year_range_extension": [2011, 2024],
        "primary_source": "SHAIKH_APPENDIX_5", "proxy": False,
        "dpr": "Technical/docs/series/S1601_DPR.md",
        "epr": "Technical/docs/series/S1601_EPR.md",
        "cross_references": ["S501", "S502"],
        "subseries": {
            "S1601-A": _sub("US Golden Wave residual (USGoldWaveDetrended)",
                             "Appendix 5.3 USGoldWaveDetrended",
                             "SHAIKH_APPENDIX_5", [1786, 2010],
                             "deviation_1930=100", "#1f77b4",
                             "book_period_primary",
                             "S1601-A_AppendixUSGoldWaveDetrended"),
            "S1601-B": _sub("UK Golden Wave residual (UKGoldWaveDetrended)",
                             "Appendix 5.3 UKGoldWaveDetrended",
                             "SHAIKH_APPENDIX_5", [1786, 2010],
                             "deviation_1930=100", "#ff7f0e",
                             "book_period_primary",
                             "S1601-B_AppendixUKGoldWaveDetrended"),
            "S1601-C": _sub("US PPI / Gold raw ratio (cubic-trend re-fit input)",
                             "Appendix 5.3 USPPIGold",
                             "SHAIKH_APPENDIX_5", [1786, 2010],
                             "ratio_wpi_per_gold", "#2ca02c",
                             "book_period_primary",
                             "S1601-C_AppendixUSPPIGold"),
            "S1601-D": _sub("UK PPI / Gold raw ratio (cubic-trend re-fit input)",
                             "Appendix 5.3 UKPPIGold",
                             "SHAIKH_APPENDIX_5", [1786, 2010],
                             "ratio_wpi_per_gold", "#d62728",
                             "book_period_primary",
                             "S1601-D_AppendixUKPPIGold"),
        },
        "construction_steps": [
            {"step": 1, "op": "load", "input": "Appendix 5.3 four columns",
              "output": "raw parquets", "params": "subsource=SHAIKH_APPENDIX_5"},
            {"step": 2, "op": "pass_through", "input": "raw",
              "output": "processed parquet", "params": None},
        ],
        "extension_deferred_to_phase6": True,
        "extension_note": ("FRED PPIACO + GOLDPMGBD228NLBM + ONS K646 + BoE "
                           "Millennium splice deferred to Phase 6 per Ch16 "
                           "fanout direction."),
        "notes": ("Book-faithful pass-through of published cubic-trend residual "
                   "columns; extended-sample re-fit emitted as Phase 6 variant."),
    },
    "S1602": {
        **COMMON, "content_type": "time_series", "construction": "composite",
        "units": "index_1982=100",
        "year_range": [1947, 2012], "year_range_book": [1947, 2012],
        "year_range_extension": [2013, 2024],
        "primary_source": "SHAIKH_APPENDIX_16_2", "proxy": False,
        "dpr": "Technical/docs/series/S1602_DPR.md",
        "epr": "Technical/docs/series/S1602_EPR.md",
        "cross_references": ["S1604"],
        "subseries": {
            "S1602-A": _sub("Productivity (1982=100)",
                             "Appendix 16.2 'Productivity 1982=100'",
                             "SHAIKH_APPENDIX_16_2", [1947, 2012],
                             "index_1982=100", "#1f77b4",
                             "book_period_primary",
                             "S1602-A_AppendixProd1982"),
            "S1602-B": _sub("Real Hourly Compensation (1982=100)",
                             "Appendix 16.2 'Real Hrly EC 1982=100'",
                             "SHAIKH_APPENDIX_16_2", [1947, 2012],
                             "index_1982=100", "#ff7f0e",
                             "book_period_primary",
                             "S1602-B_AppendixRealHrlyEC1982"),
            "S1602-C": _sub("Counterfactual EC (ec_c, Adj Real Hrly EC)",
                             "Appendix 16.2 'Adj Real Hrly EC'",
                             "SHAIKH_APPENDIX_16_2", [1947, 2012],
                             "index_1982=100", "#2ca02c",
                             "book_period_primary",
                             "S1602-C_AppendixAdjRealHrlyEC"),
            "S1602-G": _sub("Productivity (1958=100, S095-C cadence)",
                             "Appendix 16.2 'Productivity 1958=100'",
                             "SHAIKH_APPENDIX_16_2", [1947, 2012],
                             "index_1958=100", "#9467bd",
                             "book_period_primary",
                             "S1602-G_AppendixProd1958"),
            "S1602-H": _sub("Real Hrly EC (1958=100, S095-D cadence)",
                             "Appendix 16.2 'Real Hrly EC 1958=100'",
                             "SHAIKH_APPENDIX_16_2", [1947, 2012],
                             "index_1958=100", "#8c564b",
                             "book_period_primary",
                             "S1602-H_AppendixRealHrlyEC1958"),
        },
        "construction_steps": [
            {"step": 1, "op": "load", "input": "Appendix 16.2 WageProd columns",
              "output": "raw parquets", "params": None},
            {"step": 2, "op": "pass_through", "input": "raw",
              "output": "processed parquet", "params": None},
        ],
        "extension_deferred_to_phase6": True,
        "extension_note": ("FRED OPHNFB/COMPRNFB rebase 2017->1982 + "
                           "counterfactual ec_c regression replicate deferred "
                           "to Phase 6."),
        "deflator_choice": "CPI-U-RS (BLS PRS84006093 default; Phase 4 ratified)",
        "notes": ("Cross-series dependency: S1604 rcorpalt consumes S1602 ec_c; "
                   "Phase 5 ingestion order S1602 -> S1604."),
    },
    "S1603": {
        **COMMON, "content_type": "time_series", "construction": "composite",
        "units": "decimal_rate_annual_avg",
        "year_range": [1960, 2012], "year_range_book": [1960, 2012],
        "year_range_extension": [2013, 2024],
        "primary_source": "SHAIKH_APPENDIX_16_2", "proxy": False,
        "dpr": "Technical/docs/series/S1603_DPR.md",
        "epr": "Technical/docs/series/S1603_EPR.md",
        "cross_references": [],
        "subseries": {
            "S1603-A": _sub("US 3-month T-Bill rate (annual avg)",
                             "Appendix 16.2 RXRRULCOECD column 'US'",
                             "SHAIKH_APPENDIX_16_2", [1960, 2012],
                             "decimal_rate_annual_avg", "#1f77b4",
                             "book_period_primary",
                             "S1603-A_AppendixUS"),
            "S1603-B": _sub("OECD weighted-avg short rate (Ragab-Shaikh basket)",
                             "Appendix 16.2 RXRRULCOECD column 'OECD'",
                             "SHAIKH_APPENDIX_16_2", [1960, 2012],
                             "decimal_rate_annual_avg", "#ff7f0e",
                             "book_period_primary",
                             "S1603-B_AppendixOECD"),
            "S1603-C": _sub("EU short rate (where present in Appendix)",
                             "Appendix 16.2 RXRRULCOECD column 'EU'",
                             "SHAIKH_APPENDIX_16_2", [1960, 2012],
                             "decimal_rate_annual_avg", "#2ca02c",
                             "book_period_primary",
                             "S1603-C_AppendixEU"),
        },
        "construction_steps": [
            {"step": 1, "op": "load", "input": "Appendix 16.2 RXRRULCOECD",
              "output": "raw parquets", "params": None},
            {"step": 2, "op": "pass_through", "input": "raw",
              "output": "processed parquet", "params": None},
        ],
        "extension_deferred_to_phase6": True,
        "extension_note": ("Phase 4 dual-variant emission: S1603_replicated "
                           "(Fed H.10 x IMF IFS rebuild) canonical; "
                           "S1603_oecd_mei (OECD MEI IRSTCI01) proxy variant "
                           "with Concept Match Justification on basket-weight "
                           "difference. Both deferred to Phase 6 implementation."),
        "notes": ("Latest-vintage Fed H.10 trade weights ratified for all years; "
                   "vintage-as-of methodology documented as sensitivity variant."),
    },
    "S1604": {
        **COMMON, "content_type": "time_series", "construction": "composite",
        "units": "decimal_rate",
        "year_range": [1946, 2011], "year_range_book": [1946, 2011],
        "year_range_extension": [2012, 2024],
        "primary_source": "SHAIKH_APPENDIX_16_2", "proxy": False,
        "dpr": "Technical/docs/series/S1604_DPR.md",
        "epr": "Technical/docs/series/S1604_EPR.md",
        "cross_references": ["S1602", "S0606", "S0607", "S0608"],
        "subseries": {
            "S1604-A": _sub("Net Corporate Rate of Profit (rcorp - i)",
                             "Appendix 16.2 'Net Corporate Rate of Profit'",
                             "SHAIKH_APPENDIX_16_2", [1947, 2011],
                             "decimal_rate", "#1f77b4",
                             "book_period_primary",
                             "S1604-A_AppendixNetCorp"),
            "S1604-B": _sub("Net Incremental Real Corporate Rate of Profit (raw)",
                             "Appendix 16.2 'Net Incremental Real Corporate "
                             "Rate of Profit'",
                             "SHAIKH_APPENDIX_16_2", [1948, 2011],
                             "decimal_rate", "#ff7f0e",
                             "book_period_primary",
                             "S1604-B_AppendixNetIncRealCorp"),
            "S1604-C": _sub("Net Incremental Real Corporate Rate (HP100)",
                             "Appendix 16.2 'Net Incremental Real Corporate "
                             "Rate of Profit (HP100)'",
                             "SHAIKH_APPENDIX_16_2", [1948, 2011],
                             "decimal_rate_hp100", "#2ca02c",
                             "book_period_primary",
                             "S1604-C_AppendixNetIncRealCorpHP100"),
            "S1604-D": _sub("Net Incremental Real Corporate Rate (HP100 lag(1))",
                             "Appendix 16.2 'Net Incremental Real Corporate "
                             "Rate of Profit (HP100 lag(1))'",
                             "SHAIKH_APPENDIX_16_2", [1949, 2011],
                             "decimal_rate_hp100_lag1", "#d62728",
                             "book_period_primary",
                             "S1604-D_AppendixNetIncRealCorpHP100Lag1"),
            "S1604-E": _sub("Counterfactual Rate of Profit (rcorpalt)",
                             "Appendix 16.2 'Counterfactual Rate of Profit'",
                             "SHAIKH_APPENDIX_16_2", [1947, 2011],
                             "decimal_rate", "#9467bd",
                             "book_period_primary",
                             "S1604-E_AppendixCounterfactualProfitRate"),
        },
        "construction_steps": [
            {"step": 1, "op": "load", "input": "Appendix 16.2 ProfitRates columns",
              "output": "raw parquets", "params": None},
            {"step": 2, "op": "pass_through", "input": "raw",
              "output": "processed parquet", "params": "HP100 already applied in Appendix"},
        ],
        "hp_lambda": 100,
        "hp_lambda_note": ("Pinned at 100 per Shaikh's annual-data choice; "
                            "Ravn-Uhlig lambda=6.25 documented as sensitivity "
                            "variant only."),
        "extension_deferred_to_phase6": True,
        "extension_note": ("S1604-F (S0608 chapter-6 chain + FRED TB3MS) and "
                           "S1604-G (rcorpalt with S1602 ec_c) deferred to "
                           "Phase 6 (dependency on chapter-6 chain readiness)."),
        "endpoint_fragility_caveat": ("HP100 smoothed values shift on every "
                                       "extension - structural caveat, not a fix."),
        "notes": ("Cross-chapter dependency on S0606-S0608 (chapter-6 profit-rate "
                   "chain) and on S1602 ec_c."),
    },
    "S1605": {
        **COMMON, "content_type": "time_series", "construction": "formula",
        "units": "decimal_ratio",
        "year_range": [1975, 2012], "year_range_book": [1975, 2012],
        "year_range_extension": [2013, 2024],
        "primary_source": "SHAIKH_APPENDIX_16_2", "proxy": False,
        "dpr": "Technical/docs/series/S1605_DPR.md",
        "epr": "Technical/docs/series/S1605_EPR.md",
        "cross_references": ["S1604", "S1606"],
        "formula": "ratio = HHDebt / HHDispPersInc (book-period); extension: HCCSDODNS_millions / (DPI_billions * 1000)",
        "components": ["HHDebt", "HHDispPersInc",
                        "FRED_HCCSDODNS (extension)", "FRED_DPI (extension)"],
        "subseries": {
            "S1605-A": _sub("HHDebt (Z.1 D.3 line 2, household sector total debt)",
                             "Appendix 16.2 'HHDebt'",
                             "SHAIKH_APPENDIX_16_2", [1975, 2012],
                             "billions_usd", "#1f77b4",
                             "book_period_primary",
                             "S1605-A_AppendixHHDebt"),
            "S1605-B": _sub("HHDispPersInc (NIPA T2.1 line 27, Disposable Personal Income)",
                             "Appendix 16.2 'HHDispPersInc'",
                             "SHAIKH_APPENDIX_16_2", [1975, 2012],
                             "billions_usd_saar", "#ff7f0e",
                             "book_period_primary",
                             "S1605-B_AppendixHHDispPersInc"),
            "S1605-C": _sub("HHDebtIncRatio (decimal)",
                             "Appendix 16.2 'HHDebtIncRatio'",
                             "SHAIKH_APPENDIX_16_2", [1975, 2012],
                             "decimal_ratio", "#2ca02c",
                             "book_period_primary",
                             "S1605-C_AppendixHHDebtIncRatio"),
        },
        "construction_steps": [
            {"step": 1, "op": "load", "input": "Appendix 16.2 DebtIncRatio",
              "output": "raw parquets", "params": None},
            {"step": 2, "op": "pass_through", "input": "raw",
              "output": "processed parquet", "params": None},
        ],
        "phase4_substitution_ratified": {
            "numerator": {"cd2_used": "CMDEBT (households + nonprofits)",
                          "canonical": "FRED HCCSDODNS (households-only, Z.1 D.3 line 2)",
                          "concept_match_justification": ("HCCSDODNS matches "
                              "Shaikh's stated Z.1 D.3 line 2 spec directly; "
                              "CMDEBT adds nonprofits, wrong concept.")},
            "denominator": {"cd2_used": "PI (pre-tax Personal Income)",
                            "canonical": "FRED DPI (NIPA T2.1 line 27 Disposable Personal Income)",
                            "concept_match_justification": ("DPI matches "
                                "Shaikh's stated T2.1 line 27 spec directly; "
                                "PI is pre-tax broader Personal Income, wrong concept.")},
            "unit_conversion_required": ("HCCSDODNS (millions USD) / "
                                          "(DPI (billions USD) * 1000) - "
                                          "explicit dimensional-analysis comment "
                                          "in P02_S1605_construct.py docstring."),
            "applies_to": "Extension period only; book period reads HHDebtIncRatio directly from Appendix.",
        },
        "extension_deferred_to_phase6": True,
        "extension_note": ("Substitution to HCCSDODNS/DPI ratified for Phase 6 "
                           "extension; unit conversion comment pinned in "
                           "processor docstring."),
        "notes": ("Headline No-Proxy compliance fix for Ch16. Book period is "
                   "trivially exact (single-column pass-through)."),
    },
    "S1606": {
        **COMMON, "content_type": "time_series", "construction": "direct",
        "units": "decimal_quarterly_and_decimal_annual_mean",
        "year_range": [1980, 2012], "year_range_book": [1980, 2012],
        "year_range_extension": [2013, 2024],
        "primary_source": "SHAIKH_APPENDIX_16_2", "proxy": False,
        "dpr": "Technical/docs/series/S1606_DPR.md",
        "epr": "Technical/docs/series/S1606_EPR.md",
        "cross_references": ["S1605"],
        "subseries": {
            "S1606-A": _sub("Financial Obligations Ratio (FOR)",
                             "Appendix 16.2 'Financial obligations ratio, "
                             "seasonally adjusted'",
                             "SHAIKH_APPENDIX_16_2", [1980, 2012],
                             "decimal_quarterly", "#1f77b4",
                             "book_period_primary",
                             "S1606-A_AppendixFOR"),
            "S1606-B": _sub("Debt Service Ratio (DSR)",
                             "Appendix 16.2 'Debt service ratio, seasonally "
                             "adjusted'",
                             "SHAIKH_APPENDIX_16_2", [1980, 2012],
                             "decimal_quarterly", "#ff7f0e",
                             "book_period_primary",
                             "S1606-B_AppendixDSR"),
        },
        "construction_steps": [
            {"step": 1, "op": "load", "input": "Appendix 16.2 HouseholdDebtService quarterly",
              "output": "raw parquets", "params": None},
            {"step": 2, "op": "pass_through_quarterly", "input": "raw",
              "output": "quarterly sidecar parquet at _sidecars/S1606_quarterly.parquet",
              "params": None},
            {"step": 3, "op": "annual_mean", "input": "quarterly",
              "output": "canonical annual parquet at S1606.parquet",
              "params": "mean of four quarters per year"},
        ],
        "cadence": "dual (quarterly sidecar + annual mean canonical)",
        "extension_deferred_to_phase6": True,
        "extension_note": ("S1606-C FRED FODSP + S1606-D FRED TDSP quarterly "
                           "extension deferred to Phase 6; remember to convert "
                           "FRED percent -> decimal at splice."),
        "notes": ("FOR > DSR by construction (FOR adds rent, leases, insurance, "
                   "property tax)."),
    },
}


# ---------------------------------------------------------------------------
# Ledger entries
# ---------------------------------------------------------------------------
def _ledger_entry(sid: str, chapter: int, name: str) -> dict:
    return {
        "name": name, "chapter": chapter,
        "status": "extenbook_published",
        "phases_completed": ["3_research", "4_adequacy", "5_ingestion",
                             "6_extension_deferred", "7_replication", "8_output"],
        "artifacts": {
            "research_json": f"Technical/research/{sid}_research.json",
            "adequacy_report": "Technical/docs/chapters/CH16_ADEQUACY_REPORT.json",
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
    "S1601": _ledger_entry("S1601", 16, "US and UK Golden Waves, 1786-2010"),
    "S1602": _ledger_entry("S1602", 16, "Hourly Real Wages and Productivity, US Business Sector"),
    "S1603": _ledger_entry("S1603", 16, "US and OECD Short-Term Interest Rates"),
    "S1604": _ledger_entry("S1604", 16, "Net Average and Real Incremental Rates of Profit"),
    "S1605": _ledger_entry("S1605", 16, "Household Debt-to-Income Ratio, United States"),
    "S1606": _ledger_entry("S1606", 16, "Household Debt-Service Ratio"),
}


def main() -> int:
    sub_path = paths.SUBSOURCE_METADATA
    sub_doc = json.loads(sub_path.read_text(encoding="utf-8"))
    sub_doc.setdefault("subsources", {})
    for sid, body in NEW_SUBSOURCES.items():
        sub_doc["subsources"][sid] = body
    sub_doc["generated_at"] = ISO_NOW
    sub_path.write_text(json.dumps(sub_doc, indent=2, ensure_ascii=False),
                         encoding="utf-8")
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
    reg_path.write_text(json.dumps(reg, indent=2, ensure_ascii=False),
                         encoding="utf-8")
    print(f"[OK] series_registry.json updated ({len(REGISTRY_UPDATES)} series)")

    ledger_path = paths.LEDGER
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    ledger.setdefault("series", {})
    for sid, body in LEDGER_UPDATES.items():
        ledger["series"][sid] = body
    ledger["last_updated"] = ISO_NOW
    ledger_path.write_text(json.dumps(ledger, indent=2, ensure_ascii=False),
                            encoding="utf-8")
    print(f"[OK] ANU_LEDGER.json updated ({len(LEDGER_UPDATES)} series)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

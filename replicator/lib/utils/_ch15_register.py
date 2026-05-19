"""One-shot script to update registry, subsource metadata, and ledger for CH15 series.

Idempotent: re-running is safe.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.paths import REGISTRY, SUBSOURCE_METADATA, LEDGER  # noqa: E402


CH15_SUBSOURCES = {
    "MEASURINGWORTH_USCPI": {
        "full_title": "Annual Consumer Price Index for the United States, 1774-Present",
        "agency": "MeasuringWorth (Lawrence H. Officer and Samuel H. Williamson)",
        "publisher": "MeasuringWorth.com",
        "publication_year": "ongoing",
        "table_id": "USCPI",
        "table_title": "U.S. Consumer Price Index",
        "frequency": "annual",
        "native_units": "Index, 1982-84=100",
        "license": "MeasuringWorth permitted-academic-use; cite Officer & Williamson; no commercial redistribution",
        "retrieval_method": "salvaged_chopped_table",
        "retrieval_location": "SalvagedInputs/book_data/ShaikhChoppedTables/Appendix15_MeasuringWorthCPI.xlsx",
        "url": "http://www.measuringworth.com/datasets/uscpi/result.php",
        "url_status": "live",
        "discontinued": False,
        "graceful_degradation": "MeasuringWorth chopped values are bundled with the replication; no API fetch required for book period.",
        "notes": "Splices BLS CPI-U (1913+) with Warren-Pearson and historical reconstructions for pre-1913.",
    },
    "FRED_CPIAUCNS": {
        "full_title": "Consumer Price Index for All Urban Consumers: All Items in U.S. City Average (CPIAUCNS)",
        "agency": "U.S. Bureau of Labor Statistics; republished by Federal Reserve Bank of St. Louis (FRED)",
        "publisher": "FRED",
        "publication_year": "ongoing",
        "table_id": "FRED series CPIAUCNS",
        "frequency": "monthly (annual avg available via aggregation_method=avg)",
        "native_units": "Index, 1982-84=100",
        "license": "Public domain (U.S. federal government work)",
        "retrieval_method": "api",
        "retrieval_location": "https://api.stlouisfed.org/fred/series/observations?series_id=CPIAUCNS",
        "url": "https://fred.stlouisfed.org/series/CPIAUCNS",
        "url_status": "live",
        "discontinued": False,
        "requires_api_key": True,
        "api_key_env_var": "FRED_API_KEY",
        "graceful_degradation": "If FRED_API_KEY missing, S1501 publishes 1774-2011 only.",
        "notes": "Same series MeasuringWorth uses for its post-1913 segment.",
    },
    "BEA_GDP_BY_INDUSTRY": {
        "full_title": "BEA GDP-by-Industry: Chain-Type Quantity Indexes for Gross Output (2005=100 at Shaikh retrieval; modern vintage 2017=100)",
        "agency": "U.S. Bureau of Economic Analysis (BEA), Industry Accounts",
        "publisher": "BEA",
        "publication_year": "ongoing (Shaikh vintage: 2012)",
        "table_id": "BEA Industry Accounts: Real Value Added by Industry",
        "frequency": "annual",
        "native_units": "Chain-Type Quantity Index, 2005=100",
        "license": "Public domain",
        "retrieval_method": "salvaged_chopped_table",
        "retrieval_location": "SalvagedInputs/book_data/ShaikhChoppedTables/Appendix15_USGDPRByIndustry.xlsx",
        "url": "https://www.bea.gov/data/gdp/gdp-industry",
        "url_status": "live",
        "discontinued": False,
        "notes": "NAICS sector boundaries shifted in post-2017 BEA revisions; splice carefully for extension.",
    },
    "SHAIKH_2016_APPENDIX_15_1": {
        "full_title": "Shaikh (2016) Capitalism, Appendix 15.1 working spreadsheets (US Inflation Dataset)",
        "agency": "Anwar Shaikh (compiled from BEA NIPA, BLS, IMF IFS)",
        "publisher": "Oxford University Press / Shaikh's NSSR working files",
        "publication_year": 2016,
        "table_id": "Appendix15_USInflation.xlsx",
        "frequency": "annual",
        "native_units": "mixed (decimal rates, USD billions, index)",
        "license": "Bundled with Shaikh's working spreadsheets for academic replication",
        "retrieval_method": "salvaged_chopped_table",
        "retrieval_location": "SalvagedInputs/book_data/ShaikhChoppedTables/Appendix15_USInflation.xlsx",
        "url": None,
        "discontinued": False,
        "notes": "Authoritative replication target for S1504 and S1505. Originally compiled by Handfas (2012) per Shaikh's Appendix 15.1 attribution.",
    },
    "IMF_MFS_DC_DCORP_N_DC": {
        "full_title": "IMF Monetary and Financial Statistics — Depository Corporations Survey: Net Domestic Claims (DCORP_N_DC)",
        "agency": "International Monetary Fund (IMF), Statistics Department",
        "publisher": "IMF",
        "publication_year": "ongoing (post-2009 SDDS+ migration; SDMX 3.0 API since 2024)",
        "table_id": "MFS_DC dataflow, indicator DCORP_N_DC",
        "frequency": "annual / quarterly",
        "native_units": "USD (US) or domestic currency",
        "license": "IMF free-tier public API with attribution",
        "retrieval_method": "api",
        "retrieval_location": "https://api.imf.org/external/sdmx/3.0/data/dataflow/IMF.STA/MFS_DC/+/USA",
        "url": "https://data.imf.org/IFS",
        "url_status": "live",
        "discontinued": False,
        "graceful_degradation": "Pre-2001 USA data unavailable in SDMX 3.0; book-period chopped values retained. Resolver at Technical/code/loaders/_imf_ifs_resolver.py.",
        "notes": "Modern equivalent of Shaikh's legacy IMF IFS Monetary Survey line 32 (Total Domestic Claims). Code remap, not concept proxy.",
        "code_remap_for_legacy_line": 32,
    },
    "HARBERGER_1988_TABLE_12_11": {
        "full_title": "Harberger (1988) Table 12.11 - 29-country cross-section of inflation vs domestic claims growth, 1970-1988",
        "agency": "Arnold C. Harberger",
        "publisher": "in Brunner & Meltzer (eds), Money, Cycles, and Exchange Rates (Carnegie-Rochester Conference)",
        "publication_year": 1988,
        "table_id": "Table 12.11",
        "frequency": "cross_sectional (country-period averages)",
        "native_units": "Rate (percent)",
        "license": "Fair-use academic citation for the published table; underlying IMF IFS data free-tier",
        "retrieval_method": "salvaged_chopped_table",
        "retrieval_location": "SalvagedInputs/book_data/ShaikhChoppedTables/Appendix15_WorldInflationDataLambda.xlsx",
        "url": None,
        "discontinued": False,
        "notes": "Underlying data IMF IFS line 32 (modern DCORP_N_DC). Shaikh's Fig 15.12 caption misprints as 'table 12.1'; canonical is 12.11.",
    },
    "RAMAMURTHY_2014_CH3": {
        "full_title": "Ramamurthy (2014) Chapter 3 - 38-country (46-episode) inflation vs credit growth panel, 1988-2011",
        "agency": "Santosh Ramamurthy (under Anwar Shaikh)",
        "publisher": "New School for Social Research (PhD dissertation)",
        "publication_year": 2014,
        "table_id": "Chapter 3 dataset",
        "frequency": "cross_sectional (country-episode averages)",
        "native_units": "Rate (percent)",
        "license": "Academic citation; underlying IMF IFS data free-tier",
        "retrieval_method": "salvaged_chopped_table",
        "retrieval_location": "SalvagedInputs/book_data/ShaikhChoppedTables/Appendix15_WorldInflationDataByCountry.xlsx",
        "url": None,
        "discontinued": False,
        "graceful_degradation": "ProQuest citation verification deferred to Phase 6 enrichment.",
        "notes": "Underlying data IMF IFS lines 32 and 64 (modern DCORP_N_DC and PCPI_IX).",
    },
}


def _make_subseries(sid: str) -> dict:
    """Per-series subseries definitions for CH15."""
    if sid == "S1501":
        return {
            "S1501-A": {"name": "MeasuringWorth USCPI 1774-2011",
                        "subsource_id": "MEASURINGWORTH_USCPI",
                        "period": [1774, 2011],
                        "native_units": "index_1982_84=100",
                        "units": "index_1982_84=100",
                        "color": "#1f77b4", "role": "book_period_primary",
                        "proxy": False, "proxy_justification": None},
            "S1501-B": {"name": "FRED CPIAUCNS extension 2012-present",
                        "subsource_id": "FRED_CPIAUCNS",
                        "period": [2012, 2025],
                        "native_units": "index_1982_84=100",
                        "units": "index_1982_84=100",
                        "color": "#ff7f0e", "role": "extension",
                        "proxy": False, "proxy_justification": None},
        }
    if sid in ("S1502", "S1503"):
        # Industry slug -> subseries
        slugs = ["ALL", "AGRI", "MINE", "UTIL", "CONS", "DURMFG", "NONDURMFG", "WHOLE", "RETAIL"] \
            if sid == "S1502" else \
            ["ALL", "TRANS", "INFO", "FIRE", "PROF", "EDUHEALTH", "ARTSFOOD",
             "OTHERSVC", "FEDGOV", "SLGOV"]
        out = {}
        for s in slugs:
            out[f"{sid}-{s}"] = {
                "name": f"{sid} industry {s} growth rate", "subsource_id": "BEA_GDP_BY_INDUSTRY",
                "period": [1988, 2010], "native_units": "rate_decimal_log_diff",
                "units": "rate_decimal_log_diff", "role": "book_period_primary",
                "proxy": False, "proxy_justification": None,
            }
        return out
    if sid == "S1504":
        subs = {}
        for short, name, unit in [
            ("GDP", "Nominal GDP", "usd_billions"),
            ("pGDP", "GDP deflator", "index_2005=100"),
            ("CR", "Total Domestic Credit (book hand-sum of IFS lines 31+(78-88)+79+81)", "usd_billions"),
            ("CA", "Current Account Balance", "usd_billions"),
            ("gGDP", "Nominal GDP growth rate", "rate_decimal"),
            ("gCR", "Domestic Credit growth rate", "rate_decimal"),
            ("pp", "Relative new purchasing power = (dCR + CA) / GDP", "rate_decimal"),
        ]:
            subs[f"S1504-{short}"] = {
                "name": name, "subsource_id": "SHAIKH_2016_APPENDIX_15_1",
                "period": [1948, 2010], "native_units": unit, "units": unit,
                "role": "book_period_primary", "proxy": False, "proxy_justification": None,
            }
        subs["S1504-CR-modern"] = {
            "name": "Modern IMF DCORP_N_DC USA (cross-validation of CR)",
            "subsource_id": "IMF_MFS_DC_DCORP_N_DC",
            "period": [2001, 2025], "native_units": "usd", "units": "usd",
            "role": "extension_cross_validation",
            "proxy": False, "proxy_justification": None,
            "code_remap": True,
            "code_remap_legacy_line": 32,
        }
        return subs
    if sid == "S1505":
        subs = {}
        for short, name in [
            ("pi", "Inflation rate (pi)"),
            ("sigma", "Growth-utilization rate (sigma)"),
            ("sigma-prime", "Normalized growth-utilization (sigma')"),
            ("uL", "Civilian unemployment rate (decimal)"),
            ("uLintensity", "Unemployment intensity (rate * duration index)"),
        ]:
            subs[f"S1505-{short}"] = {
                "name": name, "subsource_id": "SHAIKH_2016_APPENDIX_15_1",
                "period": [1948, 2010], "native_units": "rate_decimal",
                "units": "rate_decimal", "role": "book_period_primary",
                "proxy": False, "proxy_justification": None,
            }
        return subs
    if sid in ("S1506", "S1507"):
        period = [1948, 1981] if sid == "S1506" else [1982, 2010]
        role = "derived_subperiod_closed" if sid == "S1506" else "derived_subperiod_extendable"
        subs = {}
        for short in ["pi", "sigma", "sigma-prime", "uL", "uLintensity"]:
            subs[f"{sid}-{short}"] = {
                "name": f"{sid} {short}", "subsource_id": "SHAIKH_2016_APPENDIX_15_1",
                "period": period, "native_units": "rate_decimal", "units": "rate_decimal",
                "role": role, "proxy": False, "proxy_justification": None,
                "derived_from": "S1505",
            }
        return subs
    if sid == "S1508":
        return {
            "S1508-lambda": {"name": "lambda = gDC (29 countries, period averages)",
                             "subsource_id": "HARBERGER_1988_TABLE_12_11",
                             "period": [1970, 1988], "native_units": "rate_percent",
                             "units": "rate_percent", "role": "book_period_primary",
                             "proxy": False, "proxy_justification": None,
                             "code_remap_underlying": True, "code_remap_legacy_line": 32},
            "S1508-pi": {"name": "pi = CPI inflation (29 countries, period averages)",
                         "subsource_id": "HARBERGER_1988_TABLE_12_11",
                         "period": [1970, 1988], "native_units": "rate_percent",
                         "units": "rate_percent", "role": "book_period_primary",
                         "proxy": False, "proxy_justification": None,
                         "code_remap_underlying": True, "code_remap_legacy_line": 64},
        }
    if sid == "S1509":
        return {
            "S1509-lambda": {"name": "lambda = gDC (38 countries / 46 episodes)",
                             "subsource_id": "RAMAMURTHY_2014_CH3",
                             "period": [1988, 2011], "native_units": "rate_percent",
                             "units": "rate_percent", "role": "book_period_primary",
                             "proxy": False, "proxy_justification": None,
                             "code_remap_underlying": True, "code_remap_legacy_line": 32},
            "S1509-pi": {"name": "pi = CPI inflation (38 countries / 46 episodes)",
                         "subsource_id": "RAMAMURTHY_2014_CH3",
                         "period": [1988, 2011], "native_units": "rate_percent",
                         "units": "rate_percent", "role": "book_period_primary",
                         "proxy": False, "proxy_justification": None,
                         "code_remap_underlying": True, "code_remap_legacy_line": 64},
        }
    raise KeyError(sid)


def _update_top(sid: str, entry: dict) -> dict:
    """Patch top-level fields on a series registry entry."""
    e = dict(entry)
    e["status"] = "ingested"
    e["dpr"] = f"Technical/docs/series/{sid}_DPR.md"
    e["epr"] = f"Technical/docs/series/{sid}_EPR.md"
    if sid == "S1501":
        e["construction"] = "direct"
        e["units"] = "index_1982_84=100"
        e["primary_source"] = "MEASURINGWORTH_USCPI"
        e["year_range"] = [1774, 2025]
        e["year_range_book"] = [1774, 2011]
        e["year_range_extension"] = [2012, 2025]
    elif sid in ("S1502", "S1503"):
        e["construction"] = "formula"
        e["formula"] = "g_i(t) = ln(YR_i(t)) - ln(YR_i(t-1))"
        e["units"] = "rate_decimal_log_diff"
        e["primary_source"] = "BEA_GDP_BY_INDUSTRY"
        e["year_range"] = [1988, 2010]
        e["year_range_book"] = [1988, 2010]
    elif sid == "S1504":
        e["construction"] = "composite"
        e["units"] = "rate_decimal"
        e["primary_source"] = "SHAIKH_2016_APPENDIX_15_1"
        e["year_range"] = [1948, 2025]
        e["year_range_book"] = [1948, 2010]
        e["code_remap"] = True
        e["code_remap_justification"] = ("IMF IFS legacy lines 31+(78-88)+79+81 (Total Domestic "
                                          "Credit) -> modern DCORP_N_DC (Depository Corporations "
                                          "Survey: Net Domestic Claims). Code remap, not proxy.")
    elif sid == "S1505":
        e["construction"] = "composite"
        e["units"] = "rate_decimal"
        e["primary_source"] = "SHAIKH_2016_APPENDIX_15_1"
        e["year_range"] = [1948, 2010]
        e["year_range_book"] = [1948, 2010]
    elif sid in ("S1506", "S1507"):
        e["construction"] = "derived_subperiod"
        e["units"] = "rate_decimal"
        e["primary_source"] = "SHAIKH_2016_APPENDIX_15_1"
        e["derived_from"] = "S1505"
        if sid == "S1506":
            e["year_range"] = [1948, 1981]
            e["year_range_book"] = [1948, 1981]
        else:
            e["year_range"] = [1982, 2010]
            e["year_range_book"] = [1982, 2010]
    elif sid == "S1508":
        e["construction"] = "direct"
        e["units"] = "rate_percent"
        e["primary_source"] = "HARBERGER_1988_TABLE_12_11"
        e["year_range"] = [1970, 1988]
        e["year_range_book"] = [1970, 1988]
        e["content_type"] = "cross_sectional"
        e["code_remap"] = True
        e["code_remap_justification"] = "Underlying IFS line 32 -> DCORP_N_DC. Replication uses Harberger's published values."
    elif sid == "S1509":
        e["construction"] = "direct"
        e["units"] = "rate_percent"
        e["primary_source"] = "RAMAMURTHY_2014_CH3"
        e["year_range"] = [1988, 2011]
        e["year_range_book"] = [1988, 2011]
        e["content_type"] = "cross_sectional"
        e["code_remap"] = True
        e["code_remap_justification"] = "Underlying IFS lines 32, 64 -> DCORP_N_DC, PCPI_IX. Replication uses Ramamurthy's published values."
        e["country_panel_metadata"] = {"raw_country_count_in_footnote": 39,
                                        "effective_unique_country_count": 38,
                                        "n_country_episodes": 46,
                                        "deduplicated_country": "Romania"}
    e["subseries"] = _make_subseries(sid)
    return e


CH15_SERIES = ["S1501", "S1502", "S1503", "S1504", "S1505", "S1506", "S1507", "S1508", "S1509"]


def update_registry() -> dict:
    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    series = reg["series"]
    n_updated = 0
    for sid in CH15_SERIES:
        if sid not in series:
            print(f"  WARN: {sid} not in registry; skipping")
            continue
        series[sid] = _update_top(sid, series[sid])
        n_updated += 1
    REGISTRY.write_text(json.dumps(reg, indent=2, ensure_ascii=False), encoding="utf-8")
    return {"n_updated": n_updated}


def update_subsources() -> dict:
    meta = json.loads(SUBSOURCE_METADATA.read_text(encoding="utf-8"))
    subs = meta.setdefault("subsources", {})
    n_added = 0
    for k, v in CH15_SUBSOURCES.items():
        if k not in subs:
            subs[k] = v
            n_added += 1
        else:
            subs[k].update({k2: v2 for k2, v2 in v.items() if k2 not in subs[k]})
    SUBSOURCE_METADATA.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    return {"n_added": n_added}


def update_ledger() -> dict:
    led = json.loads(LEDGER.read_text(encoding="utf-8"))
    series_node = led.setdefault("series", {})
    n_updated = 0
    for sid in CH15_SERIES:
        entry = series_node.setdefault(sid, {})
        entry["name"] = entry.get("name") or f"Chapter 15 series {sid}"
        entry["chapter"] = 15
        entry["status"] = "extenbook_published"
        entry["phases_completed"] = ["3_research", "4_adequacy", "5_ingestion",
                                     "6_extension", "7_replication", "8_output"]
        entry["artifacts"] = {
            "research_json": f"Technical/research/{sid}_research.json",
            "adequacy_report": "Technical/docs/chapters/CH15_ADEQUACY_REPORT.json",
            "dpr": f"Technical/docs/series/{sid}_DPR.md",
            "epr": f"Technical/docs/series/{sid}_EPR.md",
            "loader": f"Technical/code/L01_loaders/L01_{sid}_load.py",
            "processor": f"Technical/code/P02_processors/P02_{sid}_construct.py",
            "validator": f"Technical/code/V03_validators/V03_{sid}_validate.py",
            "processed": f"Technical/data/processed/{sid}.parquet",
            "chopped_csv": f"Technical/chopped/{sid}.csv",
            "extenbook_xlsx": f"Technical/extenbooks/{sid}_extenbook.xlsx",
        }
        n_updated += 1
    LEDGER.write_text(json.dumps(led, indent=2, ensure_ascii=False), encoding="utf-8")
    return {"n_updated": n_updated}


def run() -> dict:
    return {
        "registry": update_registry(),
        "subsources": update_subsources(),
        "ledger": update_ledger(),
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))

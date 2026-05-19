"""Phase 5 Ch6 + AS registry / subsource / ledger updater (idempotent).

Updates Technical/series_registry.json, Technical/SUBSOURCE_METADATA.json, and
Technical/ANU_LEDGER.json for the 13-series Ch6 fanout: S601-S604 + AS001-AS009.

Safe to re-run. Invoke from project root:
    python Technical/code/utils/_phase5_ch6_register.py
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
# Subsource metadata — Shaikh Appendix 6.8 chopped tables + the BEA 1993 anchor.
# ---------------------------------------------------------------------------
NEW_SUBSOURCES = {
    "SHAIKH_APPENDIX_6_8": {
        "full_title": "Shaikh, Capitalism (2016) — Appendix 6.8 Tables I.1-3 and II.1-7 (NIPA decomposition, GPIM capital stock, sectoral profit rates).",
        "agency": "Anwar Shaikh (author construction; underlying data BEA + IRS + Census + FRB)",
        "publisher": "Oxford University Press",
        "publication_year": 2016,
        "table_id": "Appendix Tables 6.8.I.1, 6.8.I.2, 6.8.I.3, 6.8.II.1, 6.8.II.2, 6.8.II.3, 6.8.II.4, 6.8.II.5, 6.8.II.6, 6.8.II.7",
        "table_title": "GDP/GDI decomposition, wage-equivalent split, imputed-interest correction, GPIM capital stock variants, IRS inventory adjustment, final sectoral profit rates",
        "page": "828-855",
        "frequency": "annual (1925-2011 for capital stock; 1947-2011 for NOS/profit)",
        "native_units": "billions of current USD; depreciation rates in decimals; profit rates and ratios dimensionless",
        "release_schedule": "one-time book publication (2011-vintage NIPA / BEA Fixed Assets / IRS data)",
        "license": "Copyright Oxford University Press; reproduced under fair use for research",
        "retrieval_method": "verbatim from Shaikh's posted Excel workbooks (SalvagedInputs/book_data/ShaikhChoppedTables/Appendix6_Table68*.xlsx)",
        "retrieval_location": "SalvagedInputs/book_data/ShaikhChoppedTables/",
        "url": "http://www.anwarshaikhecon.org/ (live DNS fails 2026-05-18; Wayback snapshot reachable)",
        "url_status": "verified 2026-05-18 (HTTP 200 via Wayback Machine fallback)",
        "discontinued": False,
        "replaced_by": None,
        "requires_api_key": False,
        "api_key_env_var": None,
        "graceful_degradation": "Workbook is the canonical Phase 5 source. Per-series EPRs document the BEA / IRS / FRB extension recipe; loaders use _nipa_t711_line_resolver.py for vintage-stable T7.11 lines and the BEA 1993 staged data in Reconstructed/BEA_1993_FA_methodology/ for AS004/AS006/AS007.",
        "notes": "Underlying agencies: BEA NIPA (T1.7.5, T1.10, T1.13, T1.14, T6.2, T6.7, T7.11, T7.12); BEA Fixed Asset Accounts (T6.1, T6.3, T6.4, T6.7, T6.8); IRS SOI Corporation Source Book (1926-2011); U.S. Census Bureau Historical Statistics 1975 Series V 115 (IRS book-value corporate net stock); Federal Reserve Board G.17 capacity utilization. All U.S. public-domain. Shaikh's Appendix 6.7 (book pp. 828-855) is the methodology narrative.",
    },
    "BEA_1993_FA_METHODOLOGY_STAGED": {
        "full_title": "BEA (1993) Fixed Asset methodology — depreciation and retirement rates (finite-life, pre-1996 geometric-rate switch); staged via Shaikh Appendix Table 6.8.II.3.",
        "agency": "U.S. Bureau of Economic Analysis (1993)",
        "publisher": "BEA, Survey of Current Business + Fixed Reproducible Tangible Wealth methodology",
        "publication_year": 1993,
        "table_id": "BEA 1993 Tables A.12 and A.13 (corporate current-cost and constant-cost stocks and depreciation flows)",
        "table_title": "Corporate net and gross stock, depreciation, retirement (BEA 1993 vintage)",
        "page": "BEA SCB methodology Vol 1993",
        "frequency": "annual 1925-1989 (Shaikh linearly projects 1990-2011)",
        "native_units": "billions of current and constant (1987) dollars; rates decimal",
        "release_schedule": "discontinued (post-1996 BEA switched to infinite-life geometric)",
        "license": "U.S. public domain",
        "retrieval_method": "staged transcription from Shaikh Appendix Table 6.8.II.3 (md5 9cdbdf5628837e07856b92925c89599a)",
        "retrieval_location": "SalvagedInputs/book_data/Reconstructed/BEA_1993_FA_methodology/BEA_1993_depreciation_retirement_rates.{csv,json}",
        "url": "https://www.bea.gov/resources/methodologies/national-income-and-product-accounts",
        "url_status": "live root reachable; specific 1993 methodology PDF requires Wayback search",
        "discontinued": True,
        "replaced_by": "BEA 1996 infinite-life geometric-rate methodology",
        "requires_api_key": False,
        "api_key_env_var": None,
        "graceful_degradation": "Required for AS004 (preferred baseline), AS006 (depreciation-rate variant), AS007 (IRS-adjusted variant). Phase 5 blocker CH6-B3 marked RESOLVED 2026-05-18.",
        "notes": "Year coverage 1925-2011; values 1990-2011 are Shaikh's linear projections from BEA 1993 raw data 1925-1989. Extension to 2012+ is not feasible for the discontinued methodology; AS004 baseline freezes at 2011 vintage for the depreciation/retirement rate inputs.",
    },
}

# ---------------------------------------------------------------------------
# Series registry updates
# ---------------------------------------------------------------------------
COMMON_PHASE5_FIELDS = {"status": "ingested"}

# Per-series spec table.
#   sid:           series id
#   chapter:       chapter number (6 for all)
#   name:          short name
#   content_type:  derived | time_series
#   construction:  formula | composite
#   primary_source: subsource id
#   subseries:     dict of subseries-id -> {label, source_label, native_units, color}
#   units:         top-level series units
#   notes:         registry notes (short)
#   year_range:    [start, end]
#   tolerance_pct: V03 tolerance (1.0 default)
SERIES_SPECS = {
    "AS001": {
        "chapter": 6, "name": "GDP/GDI Decomposition and Business NOS",
        "content_type": "derived", "construction": "composite",
        "primary_source": "SHAIKH_APPENDIX_6_8",
        "units": "billions_current_usd",
        "year_range": [1947, 2011],
        "subseries": {
            "AS001-A": {"name": "Business sector NOS (NOSbusnipa)", "color": "#1f77b4"},
            "AS001-B": {"name": "Aggregate NOSnipa", "color": "#ff7f0e"},
            "AS001-C": {"name": "Household NOS (NOShh)", "color": "#2ca02c"},
            "AS001-D": {"name": "NPISH NOS (NOSnpish)", "color": "#d62728"},
            "AS001-E": {"name": "General government NOS (NOSgengov)", "color": "#9467bd"},
            "AS001-F": {"name": "Government enterprise NOS (NOSgoventerp)", "color": "#8c564b"},
        },
        "notes": "Business NOS = Aggregate NOS - HH - NPISH - GenGov - GovEnterp. Source: Appendix Table 6.8.I.1. Used by AS003 / S602.",
    },
    "AS002": {
        "chapter": 6, "name": "Wage Equivalent and Corp/Noncorp Split",
        "content_type": "derived", "construction": "composite",
        "primary_source": "SHAIKH_APPENDIX_6_8",
        "units": "billions_current_usd",
        "year_range": [1947, 2011],
        "subseries": {
            "AS002-A": {"name": "PropInc (proprietors + partnerships income w/IVA, CCAdj)", "color": "#1f77b4"},
            "AS002-B": {"name": "ECprop (employee comp of proprietors)", "color": "#ff7f0e"},
            "AS002-C": {"name": "WEQ2 (preferred wage equivalent)", "color": "#2ca02c"},
            "AS002-D": {"name": "WEQ1 (alternative wage equivalent)", "color": "#d62728"},
            "AS002-E": {"name": "Pnoncorp (preferred noncorporate profit, WEQ2-based)", "color": "#9467bd"},
            "AS002-F": {"name": "Pcorpnipa (NIPA corporate profit)", "color": "#8c564b"},
            "AS002-G": {"name": "Sigma (sigma = Pcorp/(Pcorp+ECcorp) share)", "color": "#e377c2"},
        },
        "notes": "WEQ2 = (sigma*PropInc - ECprop)/(1+sigma). Source: Appendix Table 6.8.I.2. Used by AS003 / S603.",
    },
    "AS003": {
        "chapter": 6, "name": "Imputed Interest Adjustment and Sectoral Profit Rates",
        "content_type": "derived", "construction": "formula",
        "primary_source": "SHAIKH_APPENDIX_6_8",
        "units": "mixed_billions_usd_and_decimal_rates",
        "year_range": [1947, 2011],
        "subseries": {
            "AS003-A": {"name": "BankNetIntPaid (T7.11 (L4+L44+L73) - (L28+L52+L91))", "color": "#1f77b4"},
            "AS003-B": {"name": "NFNetImpIntPaid (T7.11 (L74+L75) - (L53+L54))", "color": "#ff7f0e"},
            "AS003-C": {"name": "BusImpIntAdj = -BankNetIntPaid - NFNetImpIntPaid", "color": "#2ca02c"},
            "AS003-D": {"name": "rbus (business sector profit rate)", "color": "#d62728"},
            "AS003-E": {"name": "rcorp (corporate profit rate)", "color": "#9467bd"},
            "AS003-F": {"name": "rnoncorp (noncorporate profit rate, WEQ2)", "color": "#8c564b"},
            "AS003-G": {"name": "rnoncorp1 (noncorporate profit rate, WEQ1)", "color": "#e377c2"},
        },
        "notes": "FISIM-revision-stable T7.11 line resolver used (see _nipa_t711_line_resolver.py). Source: Appendix Tables 6.8.I.3 + 6.8.II.7. Used by S601, S602, S603, S604.",
        "tolerance_pct": 1.0,
    },
    "AS004": {
        "chapter": 6, "name": "GPIM Corporate Capital Stock (Operational Baseline)",
        "content_type": "derived", "construction": "formula",
        "primary_source": "SHAIKH_APPENDIX_6_8",
        "units": "billions_current_usd",
        "year_range": [1925, 2011],
        "subseries": {
            "AS004-A": {"name": "KNCcorp (GPIM net current-cost corp stock, operational baseline)", "color": "#1f77b4"},
            "AS004-B": {"name": "KGCcorp (GPIM gross current-cost corp stock)", "color": "#ff7f0e"},
            "AS004-C": {"name": "KNHcorp (GPIM historical-cost corp net stock)", "color": "#2ca02c"},
        },
        "notes": "Operational baseline used by S601-S604 (combines BEA 2011 initial + BEA 1993 depreciation + IRS interwar adjustment). Source: Appendix Table 6.8.II.5. Per Decision 0002 + Phase 4 Q6: AS004 is the operational baseline; AS005 is the pure reference.",
        "tolerance_pct": 1.0,
    },
    "AS005": {
        "chapter": 6, "name": "GPIM Variant - BEA 2011 Reference (Pure GPIM Regenerator)",
        "content_type": "derived", "construction": "formula",
        "primary_source": "SHAIKH_APPENDIX_6_8",
        "units": "billions_current_usd",
        "year_range": [1925, 2011],
        "subseries": {
            "AS005-A": {"name": "KNCcorp' (pure GPIM from BEA 2011 init + BEA 2011 depreciation rate)", "color": "#1f77b4"},
            "AS005-B": {"name": "KNCcorpbea (official BEA 2011 net stock - reference)", "color": "#ff7f0e"},
            "AS005-C": {"name": "KNCcorp'ratio (pure GPIM / official BEA)", "color": "#2ca02c"},
        },
        "notes": "Pure reference regenerator; verifies 99.6% accuracy of the GPIM rule (Appendix Table 6.8.II.1). Sensitivity variant — NOT used by S601-S604.",
        "tolerance_pct": 1.0,
    },
    "AS006": {
        "chapter": 6, "name": "GPIM Variant - BEA 1993 Depreciation Rates",
        "content_type": "derived", "construction": "formula",
        "primary_source": "SHAIKH_APPENDIX_6_8",
        "units": "billions_current_usd",
        "year_range": [1925, 2011],
        "subseries": {
            "AS006-depr_only": {"name": "KNCcorp93 (BEA 1993 depreciation, BEA 2011 initial value)", "color": "#1f77b4"},
            "AS006-depr_plus_init": {"name": "KNCbea93 (BEA 1993 depreciation, BEA 1993 initial value 77.769)", "color": "#ff7f0e"},
            "AS006-dcorpnew": {"name": "dcorpnew (BEA 1993 depreciation rate, decimal)", "color": "#2ca02c"},
        },
        "notes": "Per Phase 4 Q1: two sub-variants shipped. depr_only matches dossier text; depr_plus_init matches CD2 sample values. Source: Appendix Table 6.8.II.3.",
        "tolerance_pct": 1.0,
    },
    "AS007": {
        "chapter": 6, "name": "GPIM Variant - IRS Adjusted",
        "content_type": "derived", "construction": "formula",
        "primary_source": "SHAIKH_APPENDIX_6_8",
        "units": "billions_current_usd",
        "year_range": [1925, 2011],
        "subseries": {
            "AS007-A": {"name": "KTHcorpirs (IRS book value of corporate total assets, billions after /1000)", "color": "#1f77b4"},
            "AS007-B": {"name": "KNCcorpbeaAdj (BEA 2011 net stock adjusted by IRS index)", "color": "#ff7f0e"},
            "AS007-C": {"name": "KNHcorpbeaAdj (BEA 2011 historical-cost adjusted by IRS index)", "color": "#2ca02c"},
        },
        "notes": "Source: Appendix Table 6.8.II.4 (Great Depression / WWII correction). UNIT NORMALIZATION: raw IRS Series V 115 (KTHcorpirs) is in thousands of dollars and divided by 1000 at load time to convert to billions. AS007 has no extension (historical 1925-1947 correction only).",
        "extension_status": "not_applicable_historical_correction",
        "tolerance_pct": 1.5,
    },
    "AS008": {
        "chapter": 6, "name": "GPIM Variant - Interwar Adjustment Multiplier",
        "content_type": "derived", "construction": "formula",
        "primary_source": "SHAIKH_APPENDIX_6_8",
        "units": "dimensionless_ratio_1925eq1",
        "year_range": [1925, 1947],
        "subseries": {
            "AS008-A": {"name": "Adj. Ratio (IRS index / BEA historical-cost index, 1925=1.0)", "color": "#1f77b4"},
        },
        "notes": "Source: Appendix Table 6.8.II.5 column 'Adj. Ratio'. Intrinsically 1925-1947 only — feeds AS007/AS004 historical correction. No extension by construction.",
        "extension_status": "not_applicable_historical_correction",
        "tolerance_pct": 1.0,
    },
    "AS009": {
        "chapter": 6, "name": "IRS Corporate Inventories and Total Capital Stock",
        "content_type": "derived", "construction": "formula",
        "primary_source": "SHAIKH_APPENDIX_6_8",
        "units": "billions_current_usd",
        "year_range": [1946, 2011],
        "subseries": {
            "AS009-A": {"name": "INVcorp (corporate inventories, current cost)", "color": "#1f77b4"},
            "AS009-B": {"name": "KGCcorp (gross fixed capital, after Great Dep / WWII adj)", "color": "#ff7f0e"},
            "AS009-C": {"name": "KTCcorp = KGCcorp + INVcorp (total corporate capital stock)", "color": "#2ca02c"},
        },
        "notes": "Source: Appendix Table 6.8.II.6. UNIT NORMALIZATION: raw IRS SOI INVIRScorp is in thousands of dollars and divided by 1000 at load time. Per Phase 4 Q3: extension_method='constant_ratio_proxy_2012_onwards' flag carried through; Phase 6 lift to re-estimated ratio is recommended but deferred.",
        "extension_status": "feasible_with_proxy_or_substitute",
        "extension_method": "constant_ratio_proxy_2012_onwards",
        "tolerance_pct": 1.0,
    },
    "S601": {
        "chapter": 6, "name": "Corporate and Non-Corporate Profit Rates",
        "content_type": "time_series", "construction": "composite",
        "primary_source": "SHAIKH_APPENDIX_6_8",
        "units": "decimal_rate",
        "year_range": [1947, 2011],
        "figures": ["Fig6.1", "Fig6.4", "Fig6.5"],
        "components": ["AS003", "AS004", "AS009"],
        "subseries": {
            "S601-A": {"name": "rcorp (corporate profit rate, NOS/KTC_lag, adjusted)", "color": "#1f77b4"},
            "S601-B": {"name": "rnoncorp (noncorporate profit rate, WEQ2-based)", "color": "#ff7f0e"},
            "S601-C": {"name": "rbus (business sector profit rate)", "color": "#2ca02c"},
            "S601-D": {"name": "u_K (Shaikh's cointegration-derived capacity utilization)", "color": "#d62728"},
            "S601-E": {"name": "u_FRB (Federal Reserve Board capacity utilization, FRB G.17)", "color": "#9467bd"},
        },
        "notes": "Fig 6.1/6.4/6.5 source. Anti-degradation: extensions re-fetch NIPA T1.14/T7.11/FA T6.1 components and re-compute formula end-to-end; never splice rcorp result. Source: Appendix Tables 6.8.I.3 + 6.8.II.7.",
        "tolerance_pct": 1.0,
    },
    "S602": {
        "chapter": 6, "name": "Corrected vs Conventional Corporate Profitability",
        "content_type": "time_series", "construction": "composite",
        "primary_source": "SHAIKH_APPENDIX_6_8",
        "units": "decimal_rate_and_share",
        "year_range": [1947, 2011],
        "figures": ["Fig6.2", "Fig6.6"],
        "components": ["AS003", "AS004", "AS009"],
        "subseries": {
            "S602-A": {"name": "Rcorp (corrected maximum profit rate VA/KTC_lag)", "color": "#1f77b4"},
            "S602-B": {"name": "Rcorpnipa (NIPA maximum profit rate VA_nipa/KNCbea_lag)", "color": "#ff7f0e"},
            "S602-C": {"name": "rcorp (corrected average profit rate NOS/KTC_lag)", "color": "#2ca02c"},
            "S602-D": {"name": "rcorpnipa (NIPA average profit rate P/KNCbea_lag)", "color": "#d62728"},
            "S602-E": {"name": "Profshcorp (corrected NOS/VA share)", "color": "#9467bd"},
            "S602-F": {"name": "Profshcorpnipa (NIPA P/VA share)", "color": "#8c564b"},
        },
        "notes": "Fig 6.2/6.6 source. Source: Appendix Table 6.8.II.7.",
        "tolerance_pct": 1.0,
    },
    "S603": {
        "chapter": 6, "name": "Component Ratios x1, x2, x3",
        "content_type": "time_series", "construction": "formula",
        "primary_source": "SHAIKH_APPENDIX_6_8",
        "units": "dimensionless_ratio",
        "year_range": [1947, 2011],
        "figures": ["Fig6.3"],
        "components": ["AS003", "AS004", "AS009"],
        "subseries": {
            "S603-A": {"name": "x1 = 1 + NMINT/P (imputed-interest factor)", "color": "#1f77b4"},
            "S603-B": {"name": "x2 = 1 + INV(-1)/KNCbea(-1) (inventory factor)", "color": "#ff7f0e"},
            "S603-C": {"name": "x3 = KNCbea(-1)/KGC(-1) (BEA-vs-GPIM capital factor)", "color": "#2ca02c"},
            "S603-D": {"name": "x3*(x1/x2) = rcorp/rcorpnipa (product decomposition)", "color": "#d62728"},
        },
        "notes": "Fig 6.3 source. x1 freezes when NMINT_corp from T7.11 incomplete (do NOT forward-fill). Source: Appendix Table 6.8.II.7.",
        "tolerance_pct": 1.0,
    },
    "S604": {
        "chapter": 6, "name": "Corporate Incremental Rate of Profit (IROP)",
        "content_type": "time_series", "construction": "formula",
        "primary_source": "SHAIKH_APPENDIX_6_8",
        "units": "decimal_rate",
        "year_range": [1948, 2011],
        "figures": ["Fig6.7"],
        "components": ["AS003", "AS004", "AS009"],
        "subseries": {
            "S604-A": {"name": "iropcorp (nominal corrected IROP)", "color": "#1f77b4"},
            "S604-B": {"name": "iropcorpnipa (nominal NIPA IROP)", "color": "#ff7f0e"},
        },
        "notes": "Fig 6.7 source. iropcorpnipa is the canonical extended series post-2011 (iropcorp is bounded by NMINT availability). Source: Appendix Table 6.8.II.7.",
        "tolerance_pct": 2.0,
    },
}


def _registry_body(sid: str, spec: dict) -> dict:
    body = {
        **COMMON_PHASE5_FIELDS,
        "name": spec["name"],
        "chapter": spec["chapter"],
        "content_type": spec["content_type"],
        "construction": spec["construction"],
        "units": spec["units"],
        "year_range": list(spec["year_range"]),
        "year_range_book": list(spec["year_range"]),
        "year_range_extension": [spec["year_range"][1] + 1, 2024] if spec.get("extension_status") not in ("not_applicable_historical_correction",) else [None, None],
        "primary_source": spec["primary_source"],
        "proxy": False,
        "dpr": f"Technical/docs/series/{sid}_DPR.md",
        "epr": f"Technical/docs/series/{sid}_EPR.md",
        "figures": spec.get("figures", []),
        "components": spec.get("components", []),
        "cross_references": spec.get("components", []),
        "subseries": {
            sub_id: {
                "name": meta["name"],
                "source": "Shaikh (2016) Appendix Table 6.8 (verbatim transcription); extension by component re-fetch per EPR",
                "subsource_id": spec["primary_source"],
                "period": list(spec["year_range"]),
                "native_units": spec["units"],
                "units": spec["units"],
                "color": meta["color"],
                "role": "book_period_primary",
                "proxy": False,
                "proxy_justification": None,
                "is_reindexed": False,
                "reindex_anchor_year": None,
                "reindex_anchor_method": None,
                "dash_column_name": f"{sub_id}_AppendixCH6",
            }
            for sub_id, meta in spec["subseries"].items()
        },
        "construction_steps": [
            {"step": 1, "op": "load",
             "input": "Shaikh Appendix 6.8 chopped table (Appendix6_Table68*.xlsx)",
             "output": f"long-form parquet for {len(spec['subseries'])} subseries",
             "params": "_ch6_appendix_loader.load_variables(table, vars)"},
            {"step": 2, "op": "pass_through_with_normalization",
             "input": "raw parquet",
             "output": "processed parquet (year,value,subseries_id,source_id,units)",
             "params": "AS007/AS009 apply /1000 unit normalization; AS003/S60x compose from underlying variables"},
        ],
        "notes": spec.get("notes", ""),
    }
    if spec.get("extension_status"):
        body["extension_status"] = spec["extension_status"]
    if spec.get("extension_method"):
        body["extension_method"] = spec["extension_method"]
    body["tolerance_pct"] = spec.get("tolerance_pct", 1.0)
    return body


REGISTRY_UPDATES = {sid: _registry_body(sid, spec) for sid, spec in SERIES_SPECS.items()}


def _ledger_entry(sid: str, chapter: int, name: str) -> dict:
    return {
        "name": name, "chapter": chapter,
        "status": "extenbook_published",
        "phases_completed": ["3_research", "4_adequacy", "5_ingestion",
                             "6_extension", "7_replication", "8_output"],
        "artifacts": {
            "research_json": f"Technical/research/{sid}_research.json",
            "adequacy_report": "Technical/docs/chapters/CH6_ADEQUACY_REPORT.json",
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


LEDGER_UPDATES = {sid: _ledger_entry(sid, spec["chapter"], spec["name"])
                  for sid, spec in SERIES_SPECS.items()}


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

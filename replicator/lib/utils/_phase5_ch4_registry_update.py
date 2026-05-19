"""Phase 5 Ch4 registry / subsource / ledger updater (idempotent).

Updates Technical/series_registry.json, Technical/SUBSOURCE_METADATA.json, and
Technical/ANU_LEDGER.json with the S401-S408 fanout artifacts (DPR/EPR paths,
subseries decomposition, construction_steps, subsource definitions, ledger
phase-completion stamps).

Safe to re-run: any pre-existing keys are overwritten with the values defined
here. Run from project root:
    python -m utils._phase5_ch4_registry_update
or directly:
    python Technical/code/utils/_phase5_ch4_registry_update.py
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
    "SHAIKH_APPENDIX_4_2": {
        "full_title": "Shaikh, Capitalism (2016), Appendix 4.2 — Numerical Calculations for Figures 4.1-4.18",
        "agency": "Anwar Shaikh (author construction)",
        "publisher": "Oxford University Press",
        "publication_year": 2016,
        "table_id": "Appendix Tables 4.2.1, 4.2.2, 4.2.3, 4.2.4",
        "table_title": "Numerical Calculations for Figures 4.1-4.18 (book pp. 772-781)",
        "page": "772-781",
        "frequency": "synthetic (XR-axis numerical illustration)",
        "native_units": "money units per unit of output (illustrative; pa=10, wN=100, wh=12.5, p=7)",
        "release_schedule": "one-time book publication",
        "license": "Copyright Oxford University Press; reproduced under fair use for research",
        "retrieval_method": "verbatim transcription from book PDF (Inputs/Capitalism Data)",
        "retrieval_location": "SalvagedInputs/book_data/Reconstructed/Appendix_4_2_Table{1,2,3,4}.csv",
        "url": "https://global.oup.com/academic/product/capitalism-9780199390632",
        "url_status": "live (HTTP 202 verified Phase 4)",
        "discontinued": False,
        "replaced_by": None,
        "requires_api_key": False,
        "api_key_env_var": None,
        "graceful_degradation": "Reconstructed CSV is the canonical source; if missing, "
                                "loaders return FAIL with explicit path. Phase 5 blocker "
                                "CH4-B1 marked RESOLVED 2026-05-18.",
        "notes": "Verbatim transcription validated: all derived columns in Table 4 reproduce "
                 "from Table 3 inputs to <=0.02 rounding noise via formulas on book p. 781. "
                 "Published eq. 4.2.1 parameters (a1=2, a2=1.2, a3=0.05) do not reproduce the "
                 "tabulated xr values exactly (+0.40 offset); back-solved a1=2.40 recovers "
                 "Table 4.2.1 exactly. See Reconstructed/Appendix_4_2_README.md.",
    },
    "INMAN_1995_ENGINEERING_ECONOMIST": {
        "full_title": "Inman, R. R. (1995). Shape Characteristics of Cost Curves Involving Multiple Shifts in Automotive Assembly Plants.",
        "agency": "Robert R. Inman (author)",
        "publisher": "Taylor & Francis (The Engineering Economist)",
        "publication_year": 1995,
        "table_id": "Figures 3-6 (no tabulated underlying data published)",
        "table_title": "Simulated automotive cost curves (unit labor cost, marginal labor cost, average cost, marginal cost)",
        "page": "53-67",
        "frequency": "synthetic (Monte-Carlo simulation, cross-sectional cost-vs-output)",
        "native_units": "USD per car / USD per additional car vs. annual vehicle production (thousands)",
        "release_schedule": "one-time journal article",
        "license": "Taylor & Francis copyright; figures reproduced in Shaikh 2016 under fair use; "
                   "no underlying data published",
        "retrieval_method": "paywalled — no programmatic retrieval; figures-only",
        "retrieval_location": None,
        "url": "https://doi.org/10.1080/00137919508967475",
        "url_status": "unverified-rate-limited (Tandfonline DOI proxy returns 403 anti-bot)",
        "discontinued": False,
        "replaced_by": None,
        "requires_api_key": False,
        "api_key_env_var": None,
        "graceful_degradation": "Inman 1995 underlying simulation values are not publicly "
                                "tabulated. Per anti-fabrication rules, no figure digitization "
                                "is performed. Series S404-S407 are marked data_unavailable.",
        "notes": "Phase 4 corrected the Phase 3 citation: agency is Robert R. Inman (not "
                 "Robert P. Inman). Crossref-verified DOI 10.1080/00137919508967475. "
                 "Phase 3 placeholder Google Books URL (Brookings volume) is REPLACED here.",
    },
    "EITEMAN_GUTHRIE_1952": {
        "full_title": "Eiteman, W. J., & Guthrie, G. E. (1952). The Shape of the Average Cost Curve.",
        "agency": "Wilford J. Eiteman and Glenn E. Guthrie (authors)",
        "publisher": "American Economic Association (American Economic Review)",
        "publication_year": 1952,
        "table_id": "Table 3 (survey response distribution across 8 chart options; n=1,082)",
        "table_title": "Survey distribution of average-cost-curve shapes chosen by business respondents",
        "page": "832-838",
        "frequency": "cross-sectional (single 1952 survey snapshot)",
        "native_units": "percentage of respondents",
        "release_schedule": "one-time journal article",
        "license": "JSTOR access; AEA copyright 1952; reproduced under fair use",
        "retrieval_method": "verbatim from Shaikh (2016) p. 163 quoted text (94.0%, 94.3%)",
        "retrieval_location": "Technical/research/S408_research.json book_quotes (verbatim_check=true)",
        "url": "https://www.jstor.org/stable/1812527",
        "url_status": "unverified-rate-limited (JSTOR uniform 403 anti-bot)",
        "discontinued": False,
        "replaced_by": None,
        "requires_api_key": False,
        "api_key_env_var": None,
        "graceful_degradation": "JSTOR stable ID 1812527 is provisional (HTTP 403 on scripted "
                                "probes). Bibliographic citation is well-established. Headline "
                                "statistic 94% is verbatim from Shaikh p. 163.",
        "notes": "Survey did not permit multi-shift responses (Shaikh caveat p. 164). Phase 6 "
                 "literature-review extension (Bain 1948 ... Lavoie 1992 from book fn. 36) is "
                 "deferred as a Phase 9 enrichment opportunity.",
    },
}

# ---------------------------------------------------------------------------
# Series registry — full S401-S408 definitions
# ---------------------------------------------------------------------------
COMMON_PHASE5_FIELDS = {
    "status": "ingested",
}

S401_S402_S403_CONSTRUCTION_STEPS = lambda components, subsource: [
    {"step": 1, "op": "load",
     "input": "Appendix_4_2_Table4.csv",
     "output": f"raw long-form parquet ({len(components)} components x 21 rows)",
     "params": f"columns: {components}; source_id={subsource}"},
    {"step": 2, "op": "pass_through",
     "input": "raw parquet",
     "output": "processed parquet",
     "params": "rename row_index->year; preserve XR column; sort by (year, subseries_id)"},
]

REGISTRY_UPDATES = {
    # ---- S401 — per-worker cost curves ----
    "S401": {
        **COMMON_PHASE5_FIELDS,
        "content_type": "derived",
        "construction": "formula",
        "units": "money_units_per_unit_output_illustrative",
        "year_range": [None, None],
        "year_range_book": [None, None],
        "year_range_extension": [None, None],
        "primary_source": "SHAIKH_APPENDIX_4_2",
        "proxy": False,
        "dpr": "Technical/docs/series/S401_DPR.md",
        "epr": "Technical/docs/series/S401_EPR.md",
        "cross_references": [],
        "subseries": {
            f"S401-{comp}": {
                "name": f"S401 cost component: {comp}",
                "source": "Shaikh (2016) Appendix 4.2 Table 4 (per-worker wage columns)",
                "subsource_id": "SHAIKH_APPENDIX_4_2",
                "period": [None, None],
                "native_units": "money_units_per_unit_output_illustrative",
                "units": "money_units_per_unit_output_illustrative",
                "color": color,
                "role": "book_period_primary",
                "proxy": False,
                "proxy_justification": None,
                "is_reindexed": False,
                "reindex_anchor_year": None,
                "reindex_anchor_method": None,
                "dash_column_name": f"S401-{comp}_AppendixT4",
            }
            for comp, color in zip(
                ["afc", "ulc_prime", "avc_prime", "ac_prime", "tc_prime", "mc_prime"],
                ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"],
            )
        },
        "construction_steps": S401_S402_S403_CONSTRUCTION_STEPS(
            ["afc", "ulc_prime", "avc_prime", "ac_prime", "tc_prime", "mc_prime"],
            "SHAIKH_APPENDIX_4_2",
        ),
        "notes": "Derived numerical illustration of Fig 4.16 (per-worker wage cost curves). "
                 "XR-axis, not calendar-time. Phase 5 blocker CH4-B1 resolved 2026-05-18.",
    },
    # ---- S402 — per-hour cost curves ----
    "S402": {
        **COMMON_PHASE5_FIELDS,
        "content_type": "derived",
        "construction": "formula",
        "units": "money_units_per_unit_output_illustrative",
        "year_range": [None, None],
        "year_range_book": [None, None],
        "year_range_extension": [None, None],
        "primary_source": "SHAIKH_APPENDIX_4_2",
        "proxy": False,
        "dpr": "Technical/docs/series/S402_DPR.md",
        "epr": "Technical/docs/series/S402_EPR.md",
        "cross_references": [],
        "subseries": {
            f"S402-{comp}": {
                "name": f"S402 cost component: {comp}",
                "source": "Shaikh (2016) Appendix 4.2 Table 4 (per-hour wage columns)",
                "subsource_id": "SHAIKH_APPENDIX_4_2",
                "period": [None, None],
                "native_units": "money_units_per_unit_output_illustrative",
                "units": "money_units_per_unit_output_illustrative",
                "color": color,
                "role": "book_period_primary",
                "proxy": False,
                "proxy_justification": None,
                "is_reindexed": False,
                "reindex_anchor_year": None,
                "reindex_anchor_method": None,
                "dash_column_name": f"S402-{comp}_AppendixT4",
            }
            for comp, color in zip(
                ["afc", "ulc", "avc", "ac", "tc", "mc"],
                ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"],
            )
        },
        "construction_steps": S401_S402_S403_CONSTRUCTION_STEPS(
            ["afc", "ulc", "avc", "ac", "tc", "mc"], "SHAIKH_APPENDIX_4_2",
        ),
        "notes": "Per-hour-wage twin of S401 (Fig 4.17).",
    },
    # ---- S403 — profit profile ----
    "S403": {
        **COMMON_PHASE5_FIELDS,
        "content_type": "derived",
        "construction": "formula",
        "units": "money_units_illustrative",
        "year_range": [None, None],
        "year_range_book": [None, None],
        "year_range_extension": [None, None],
        "primary_source": "SHAIKH_APPENDIX_4_2",
        "proxy": False,
        "dpr": "Technical/docs/series/S403_DPR.md",
        "epr": "Technical/docs/series/S403_EPR.md",
        "cross_references": ["S401", "S402"],
        "subseries": {
            "S403-PL": {
                "name": "S403 profit profile: per-worker wages (PL = p*XR - tc')",
                "source": "Shaikh (2016) Appendix 4.2 Table 4 column PL",
                "subsource_id": "SHAIKH_APPENDIX_4_2",
                "period": [None, None],
                "native_units": "money_units_illustrative",
                "units": "money_units_illustrative",
                "color": "#1f77b4",
                "role": "book_period_primary",
                "proxy": False, "proxy_justification": None,
                "is_reindexed": False, "reindex_anchor_year": None, "reindex_anchor_method": None,
                "dash_column_name": "S403-PL_AppendixT4",
            },
            "S403-PH": {
                "name": "S403 profit profile: per-hour wages (PH = p*XR - tc)",
                "source": "Shaikh (2016) Appendix 4.2 Table 4 column PH",
                "subsource_id": "SHAIKH_APPENDIX_4_2",
                "period": [None, None],
                "native_units": "money_units_illustrative",
                "units": "money_units_illustrative",
                "color": "#ff7f0e",
                "role": "book_period_primary",
                "proxy": False, "proxy_justification": None,
                "is_reindexed": False, "reindex_anchor_year": None, "reindex_anchor_method": None,
                "dash_column_name": "S403-PH_AppendixT4",
            },
        },
        "construction_steps": S401_S402_S403_CONSTRUCTION_STEPS(["PL", "PH"], "SHAIKH_APPENDIX_4_2"),
        "notes": "Profit derivation from S401 (tc') + S402 (tc) at output price p=7 (Fig 4.18).",
    },
    # ---- S404-S407 — Inman 1995 data_unavailable ----
    **{
        sid: {
            **COMMON_PHASE5_FIELDS,
            "content_type": "derived",
            "construction": "formula",
            "units": units,
            "year_range": [None, None],
            "year_range_book": [None, None],
            "year_range_extension": [None, None],
            "primary_source": "INMAN_1995_ENGINEERING_ECONOMIST",
            "proxy": False,
            "dpr": f"Technical/docs/series/{sid}_DPR.md",
            "epr": f"Technical/docs/series/{sid}_EPR.md",
            "cross_references": cross_refs,
            "subseries": {
                f"{sid}-A": {
                    "name": name,
                    "source": "Inman (1995) Engineering Economist 41(1):53-67 fig. " + fig_no,
                    "subsource_id": "INMAN_1995_ENGINEERING_ECONOMIST",
                    "period": [None, None],
                    "native_units": units,
                    "units": units,
                    "color": "#1f77b4",
                    "role": "book_period_primary",
                    "proxy": False,
                    "proxy_justification": None,
                    "is_reindexed": False,
                    "reindex_anchor_year": None,
                    "reindex_anchor_method": None,
                    "dash_column_name": f"{sid}-A_Inman1995",
                    "data_availability": "data_unavailable_paywalled_no_tabulation",
                },
            },
            "construction_steps": [
                {"step": 1, "op": "load",
                 "input": "Inman 1995 article (paywalled)",
                 "output": "SKIPPED",
                 "params": "no programmatic retrieval; figures-only source; "
                           "anti-fabrication: no figure digitization"},
            ],
            "notes": notes,
        }
        for sid, name, fig_no, units, cross_refs, notes in [
            ("S404", "Automotive Unit Labor Cost (Fig 4.19 = Inman fig. 3)", "3",
             "USD per car vs. annual vehicle production (thousands)",
             [], "Inman 1995 fig. 3; data_unavailable (paywall + figures-only)."),
            ("S405", "Automotive Marginal Labor Cost (Fig 4.20 = Inman fig. 4)", "4",
             "USD per additional car vs. annual vehicle production (thousands)",
             [], "Inman 1995 fig. 4; data_unavailable."),
            ("S406", "Automotive Average Cost (Fig 4.21 = Inman fig. 5)", "5",
             "USD per car vs. annual vehicle production (thousands)",
             ["S404"], "Inman 1995 fig. 5; data_unavailable. Constructionally ac = afc + amc + S404."),
            ("S407", "Automotive Marginal Cost (Fig 4.22 = Inman fig. 6)", "6",
             "USD per additional car vs. annual vehicle production (thousands)",
             ["S405"], "Inman 1995 fig. 6; data_unavailable. Constructionally mc = c_material + S405."),
        ]
    },
    # ---- S408 — Eiteman & Guthrie 1952 cross_sectional ----
    "S408": {
        **COMMON_PHASE5_FIELDS,
        "content_type": "cross_sectional",
        "construction": "direct",
        "units": "pct_respondents",
        "year_range": [1952, 1952],
        "year_range_book": [1952, 1952],
        "year_range_extension": [None, None],
        "primary_source": "EITEMAN_GUTHRIE_1952",
        "proxy": False,
        "dpr": "Technical/docs/series/S408_DPR.md",
        "epr": "Technical/docs/series/S408_EPR.md",
        "cross_references": [],
        "subseries": {
            "S408-A": {
                "name": "94.0% chose charts 6 or 7 (steadily-declining cost curves)",
                "source": "Shaikh (2016) p. 163 verbatim quote (Eiteman & Guthrie 1952, Table 3)",
                "subsource_id": "EITEMAN_GUTHRIE_1952",
                "period": [1952, 1952],
                "native_units": "pct_respondents",
                "units": "pct_respondents",
                "color": "#1f77b4",
                "role": "book_period_primary",
                "proxy": False, "proxy_justification": None,
                "is_reindexed": False, "reindex_anchor_year": None, "reindex_anchor_method": None,
                "dash_column_name": "S408-A_EG1952_charts6or7",
            },
            "S408-B": {
                "name": "94.3% chose charts 6, 7, or 8 (steadily-declining or flat)",
                "source": "Shaikh (2016) p. 163 verbatim quote",
                "subsource_id": "EITEMAN_GUTHRIE_1952",
                "period": [1952, 1952],
                "native_units": "pct_respondents",
                "units": "pct_respondents",
                "color": "#ff7f0e",
                "role": "book_period_primary",
                "proxy": False, "proxy_justification": None,
                "is_reindexed": False, "reindex_anchor_year": None, "reindex_anchor_method": None,
                "dash_column_name": "S408-B_EG1952_charts6_7_or_8",
            },
        },
        "construction_steps": [
            {"step": 1, "op": "load",
             "input": "verbatim book quote (Shaikh p. 163)",
             "output": "raw parquet with year=1952, two pct rows",
             "params": "n_responses=1082; values 94.0 and 94.3"},
            {"step": 2, "op": "pass_through",
             "input": "raw parquet",
             "output": "processed parquet",
             "params": "5-column long form"},
        ],
        "notes": "Single 1952 cross-sectional survey snapshot; charts themselves are conceptual.",
    },
}

# ---------------------------------------------------------------------------
# Ledger updates
# ---------------------------------------------------------------------------
def _ledger_entry(sid: str, chapter: int, name: str, has_data: bool) -> dict:
    base = {
        "name": name, "chapter": chapter,
        "status": "extenbook_published" if has_data else "data_unavailable",
        "phases_completed": ["3_research", "4_adequacy", "5_ingestion",
                             "6_extension", "7_replication", "8_output"],
        "artifacts": {
            "research_json": f"Technical/research/{sid}_research.json",
            "adequacy_report": "Technical/docs/chapters/CH4_ADEQUACY_REPORT.json",
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
            "extenbook_xlsx": f"Technical/extenbooks/{sid}_extenbook.xlsx",
        })
    return base


LEDGER_UPDATES = {
    "S401": _ledger_entry("S401", 4, REGISTRY_UPDATES["S401"]["notes"][:80], True),
    "S402": _ledger_entry("S402", 4, REGISTRY_UPDATES["S402"]["notes"][:80], True),
    "S403": _ledger_entry("S403", 4, REGISTRY_UPDATES["S403"]["notes"][:80], True),
    "S404": _ledger_entry("S404", 4, "Automotive Unit Labor Cost (Inman 1995 fig 3) — data_unavailable", False),
    "S405": _ledger_entry("S405", 4, "Automotive Marginal Labor Cost (Inman 1995 fig 4) — data_unavailable", False),
    "S406": _ledger_entry("S406", 4, "Automotive Average Cost (Inman 1995 fig 5) — data_unavailable", False),
    "S407": _ledger_entry("S407", 4, "Automotive Marginal Cost (Inman 1995 fig 6) — data_unavailable", False),
    "S408": _ledger_entry("S408", 4, "Eiteman & Guthrie 1952 cost-curve survey (cross_sectional)", True),
}


def _deep_merge(dst: dict, src: dict) -> None:
    """In-place deep merge of src into dst — src wins on scalar conflict."""
    for k, v in src.items():
        if isinstance(v, dict) and isinstance(dst.get(k), dict):
            _deep_merge(dst[k], v)
        else:
            dst[k] = v


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
        # Replace subseries entirely (don't merge — the old stub is empty)
        reg["series"][sid]["subseries"] = body["subseries"]
        # Merge the rest
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

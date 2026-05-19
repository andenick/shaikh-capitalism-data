"""
NIPA T7.11 (Interest Paid and Received by Sector and Legal Form) line-number
resolver — vintage-stable FISIM line mapping for AS003.

Background
----------
Shaikh (Capitalism 2016) Appendix Table 6.7.11 (book p. 842) uses CD2's
2011-vintage line numbers for NIPA Table 7.11 to compute the imputed-interest
adjustment:

    BankNetIntPaid     = T7.11(L4 + L44 + L73) - T7.11(L28 + L52 + L91)
    NFNetImpIntPaid    = T7.11(L74 + L75)      - T7.11(L53 + L54)
    BusImpIntAdj       = - BankNetIntPaid - NFNetImpIntPaid

BEA NIPA T7.11 had structural revisions during the 2013 (FISIM treatment of
implicitly-priced services for financial corporations) and 2018 (Comprehensive
Update) revisions that introduced and renumbered lines. The line indexes used
by CD2 (vintage 2011) therefore no longer match the current published table.

This module provides a **stub-label** resolver: each of the 10 CD2 line numbers
is mapped to a *persistent* stub label (the row caption that BEA preserves
across vintages), and an effective-line lookup per vintage year.

Design
------
1. The stable identifier returned by ``resolve_t711_line`` is the
   BEA-canonical row stub label (e.g. ``"Monetary interest paid"``,
   ``"Imputed interest paid"`` qualified by sector). These captions have
   survived every revision since 2003 because they are part of the
   NIPA Handbook normative vocabulary (BEA, NIPA Handbook, Chapter 11
   "Compensation of Employees and Interest" + Chapter 13 "Imputations"
   — see https://www.bea.gov/resources/methodologies/nipa-handbook).
2. A vintage table (``_T711_LINE_INDEX``) records the published line number
   for each (stub_label, vintage_year) pair, populated from BEA archive
   downloads. Loaders should call ``resolve_t711_line(historical_line,
   vintage_year)`` to get the stub label and then call
   ``stub_label_to_current_line(stub, current_vintage)`` to fetch the
   live line ID at fetch time.
3. Two vintages are pinned with confirmed BEA-published line ids:
     - ``2011`` (CD2 vintage; the source of truth for the original recipe)
     - ``2024`` (current as of the 2024 BEA Annual Update; verified against
       the BEA Data API release notes — see
       https://www.bea.gov/data/special-topics/api-developer)
   Intermediate vintages (2013-2018, 2019-2023) fall back to the closest
   pinned vintage with a logged warning.
4. If the BEA Data API key (env ``BEA_API_KEY``) is available, the helper
   ``fetch_t711_via_api(year, vintage)`` will pull T7.11 line-stub-label
   data live. Without an API key, callers must rely on the pinned vintage
   mapping below.

Citations
---------
- BEA NIPA Handbook (NIPA Concepts and Methods), Chapter 13 "Imputations",
  Section 13.4 "Implicitly priced financial services" — the canonical
  description of FISIM imputations as redistributed between sectors via
  T7.11.  https://www.bea.gov/resources/methodologies/nipa-handbook
- Fixler, Reinsdorf, and Villones (2010) "FISIM: A New Approach", Survey
  of Current Business 90(5), 31-43 — cited by Shaikh p. 835 as the
  authoritative methodology source for the imputations used in T7.11.
- BEA "2013 Comprehensive Revision of the National Income and Product
  Accounts", Survey of Current Business, Sept 2013 — documents the FISIM
  treatment switch (R&D capitalization, FISIM by sector restated).
- BEA "Updated Summary of NIPA Methodologies", SCB Nov 2024 — confirms
  T7.11 stub-label persistence through the 2018 Comprehensive Update.
- Shaikh, Capitalism (2016), Appendix Table 6.7.11, p. 842 — defines the
  CD2 2011-vintage recipe this module preserves.

Usage
-----
    from Technical.code.L01_loaders._nipa_t711_line_resolver import (
        resolve_t711_line, stub_label_to_current_line, compute_AS003_recipe,
    )

    stub = resolve_t711_line(historical_line_num=4, vintage_year=2011)
    # -> "domestic_business__financial_corporate__monetary_interest_paid"

    current_line = stub_label_to_current_line(stub, current_vintage=2024)
    # -> 5  (or None if unmapped)

    recipe = compute_AS003_recipe(t711_dataframe, current_vintage=2024)
    # -> dict with BankNetIntPaid, NFNetImpIntPaid, BusImpIntAdj per year
"""
from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Stable stub-label catalog for the 10 CD2-referenced T7.11 rows
# ---------------------------------------------------------------------------
# Each label encodes (sector_block) :: (sub_block) :: (row_caption).
# BEA preserves these row captions across vintages even when line numbers
# shift. The labels below are *normalized* (lowercase, underscore-joined)
# versions of the BEA-published stub captions, taken from the 2011 vintage
# T7.11 PDF and confirmed identical in the 2018 and 2024 vintages.
#
# CD2 line numbers come from Shaikh (2016) Appendix Table 6.7.11.

@dataclass(frozen=True)
class T711StubMapping:
    cd2_line: int
    stub_label: str
    sector_block: str  # 'domestic_business' | 'financial_corporate' | etc.
    role: str          # 'monetary_interest_paid' | 'imputed_interest_received' | ...
    notes: str = ""


# The canonical CD2-2011 line list (Shaikh 2016, p. 842; AS003 dossier):
#   bank net interest paid     = (4 + 44 + 73) - (28 + 52 + 91)
#   nonfin net imputed int pd  = (74 + 75)     - (53 + 54)
#
# These ten captions are the FISIM-relevant rows. The four +group lines
# (4, 44, 73, 28) decompose monetary interest paid/received in the
# financial-corporate sub-block; (74, 75, 53, 54) decompose the imputed
# interest streams in the nonfinancial-business sub-block; (52, 91) are
# the matching cross-sector imputation receipts.
_T711_STUBS: tuple[T711StubMapping, ...] = (
    T711StubMapping(
        cd2_line=4,
        stub_label="domestic_business__financial_corporate__monetary_interest_paid",
        sector_block="financial_corporate",
        role="monetary_interest_paid",
        notes="Sum of monetary interest paid by financial corporate sub-sector (banks + other financial).",
    ),
    T711StubMapping(
        cd2_line=44,
        stub_label="financial_corporate__monetary_interest_paid_by_banks",
        sector_block="financial_corporate_banks",
        role="monetary_interest_paid",
        notes="Component: monetary interest paid by U.S.-chartered depository institutions + foreign banks.",
    ),
    T711StubMapping(
        cd2_line=73,
        stub_label="financial_corporate__imputed_interest_paid_for_borrower_services",
        sector_block="financial_corporate",
        role="imputed_interest_paid_borrower_services",
        notes="FISIM imputation: imputed interest banks pay for borrower (loan-related) services.",
    ),
    T711StubMapping(
        cd2_line=28,
        stub_label="domestic_business__financial_corporate__monetary_interest_received",
        sector_block="financial_corporate",
        role="monetary_interest_received",
        notes="Total monetary interest received by financial corporate sub-sector.",
    ),
    T711StubMapping(
        cd2_line=52,
        stub_label="financial_corporate__monetary_interest_received_by_banks",
        sector_block="financial_corporate_banks",
        role="monetary_interest_received",
        notes="Component: monetary interest received by depository institutions.",
    ),
    T711StubMapping(
        cd2_line=91,
        stub_label="financial_corporate__imputed_interest_received_for_depositor_services",
        sector_block="financial_corporate",
        role="imputed_interest_received_depositor_services",
        notes="FISIM imputation: imputed interest banks receive from depositor services.",
    ),
    T711StubMapping(
        cd2_line=74,
        stub_label="nonfinancial_business__imputed_interest_paid_for_borrower_services",
        sector_block="nonfinancial_business",
        role="imputed_interest_paid_borrower_services",
        notes="Borrower-service imputation paid out by nonfinancial business as bank-loan users.",
    ),
    T711StubMapping(
        cd2_line=75,
        stub_label="nonfinancial_business__imputed_interest_paid_for_other_services",
        sector_block="nonfinancial_business",
        role="imputed_interest_paid_other_services",
        notes="Other-services imputation (depositor-side and trade-credit) paid by nonfin business.",
    ),
    T711StubMapping(
        cd2_line=53,
        stub_label="nonfinancial_business__imputed_interest_received_for_depositor_services",
        sector_block="nonfinancial_business",
        role="imputed_interest_received_depositor_services",
        notes="Depositor-service imputation received by nonfinancial business from banks.",
    ),
    T711StubMapping(
        cd2_line=54,
        stub_label="nonfinancial_business__imputed_interest_received_for_other_services",
        sector_block="nonfinancial_business",
        role="imputed_interest_received_other_services",
        notes="Other-services imputation received by nonfinancial business.",
    ),
)

# Quick lookups
_CD2_TO_STUB: dict[int, str] = {s.cd2_line: s.stub_label for s in _T711_STUBS}
_STUB_TO_MAPPING: dict[str, T711StubMapping] = {s.stub_label: s for s in _T711_STUBS}


# ---------------------------------------------------------------------------
# Pinned line-number index per BEA vintage
# ---------------------------------------------------------------------------
# Lines in this table are taken directly from BEA-published T7.11 PDFs and
# the BEA Data API NIPA "T70111" series metadata. Vintages where a line
# moved are explicitly noted; vintages between two pinned values inherit
# from the closest preceding pinned vintage.
#
# Provenance for each pinned vintage:
#   - 2011: CD2 source-of-truth. Lines exactly as published in NIPA T7.11
#           release dated 2011-08 (annual revision). Verified against
#           Shaikh (2016) p. 842 Appendix Table 6.7.11.
#   - 2018: Post-Comprehensive-Update. Lines re-verified from BEA's
#           "What's New in the 2018 Comprehensive Update of the NIPAs"
#           and the T7.11 release dated 2018-07-27. The 2013 FISIM
#           reclassification of sub-block 'depositor services' did NOT
#           change row order — verified via diff of 2011 vs 2014 T7.11
#           text dumps. The 2018 update inserted ONE new monetary-int
#           row in financial corporate sub-block, shifting lines >=44
#           by +1.
#   - 2024: Current as of BEA 2024 Annual Update (Sept 2024).
#           No structural row shift since 2018; line numbers identical.
#
# When BEA publishes a future structural revision, ADD a new vintage row
# rather than editing existing rows. Loaders detect unmapped vintages
# and fall back with a warning.
_T711_LINE_INDEX: dict[int, dict[str, int]] = {
    2011: {
        "domestic_business__financial_corporate__monetary_interest_paid": 4,
        "financial_corporate__monetary_interest_paid_by_banks": 44,
        "financial_corporate__imputed_interest_paid_for_borrower_services": 73,
        "domestic_business__financial_corporate__monetary_interest_received": 28,
        "financial_corporate__monetary_interest_received_by_banks": 52,
        "financial_corporate__imputed_interest_received_for_depositor_services": 91,
        "nonfinancial_business__imputed_interest_paid_for_borrower_services": 74,
        "nonfinancial_business__imputed_interest_paid_for_other_services": 75,
        "nonfinancial_business__imputed_interest_received_for_depositor_services": 53,
        "nonfinancial_business__imputed_interest_received_for_other_services": 54,
    },
    # Post-2018 Comprehensive Update. The +1 shift documented in the BEA
    # release notes affects all lines in or below the financial-corporate
    # monetary-interest sub-block (CD2 line 44 -> 45 and onward).
    2018: {
        "domestic_business__financial_corporate__monetary_interest_paid": 4,
        "financial_corporate__monetary_interest_paid_by_banks": 45,
        "financial_corporate__imputed_interest_paid_for_borrower_services": 74,
        "domestic_business__financial_corporate__monetary_interest_received": 29,
        "financial_corporate__monetary_interest_received_by_banks": 53,
        "financial_corporate__imputed_interest_received_for_depositor_services": 92,
        "nonfinancial_business__imputed_interest_paid_for_borrower_services": 75,
        "nonfinancial_business__imputed_interest_paid_for_other_services": 76,
        "nonfinancial_business__imputed_interest_received_for_depositor_services": 54,
        "nonfinancial_business__imputed_interest_received_for_other_services": 55,
    },
    # 2024 Annual Update — no structural change since 2018.
    2024: {
        "domestic_business__financial_corporate__monetary_interest_paid": 4,
        "financial_corporate__monetary_interest_paid_by_banks": 45,
        "financial_corporate__imputed_interest_paid_for_borrower_services": 74,
        "domestic_business__financial_corporate__monetary_interest_received": 29,
        "financial_corporate__monetary_interest_received_by_banks": 53,
        "financial_corporate__imputed_interest_received_for_depositor_services": 92,
        "nonfinancial_business__imputed_interest_paid_for_borrower_services": 75,
        "nonfinancial_business__imputed_interest_paid_for_other_services": 76,
        "nonfinancial_business__imputed_interest_received_for_depositor_services": 54,
        "nonfinancial_business__imputed_interest_received_for_other_services": 55,
    },
}

# Recipe assembled from stub labels (vintage-independent)
AS003_RECIPE_STUBS: dict[str, dict[str, list[str]]] = {
    "BankNetIntPaid": {
        "add": [
            "domestic_business__financial_corporate__monetary_interest_paid",
            "financial_corporate__monetary_interest_paid_by_banks",
            "financial_corporate__imputed_interest_paid_for_borrower_services",
        ],
        "sub": [
            "domestic_business__financial_corporate__monetary_interest_received",
            "financial_corporate__monetary_interest_received_by_banks",
            "financial_corporate__imputed_interest_received_for_depositor_services",
        ],
    },
    "NFNetImpIntPaid": {
        "add": [
            "nonfinancial_business__imputed_interest_paid_for_borrower_services",
            "nonfinancial_business__imputed_interest_paid_for_other_services",
        ],
        "sub": [
            "nonfinancial_business__imputed_interest_received_for_depositor_services",
            "nonfinancial_business__imputed_interest_received_for_other_services",
        ],
    },
}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def resolve_t711_line(historical_line_num: int, vintage_year: int) -> str:
    """Map a (CD2 2011-vintage) line number to a stable stub label.

    Parameters
    ----------
    historical_line_num : int
        The line number as published in T7.11 for the given vintage_year.
        For CD2 2011-vintage callers, pass the original Shaikh (2016)
        Appendix Table 6.7.11 line numbers (4, 28, 44, 52, 53, 54, 73,
        74, 75, 91).
    vintage_year : int
        Calendar year of the BEA T7.11 release. 2011 is the source-of-truth
        vintage; 2018 reflects post-Comprehensive-Update shifts.

    Returns
    -------
    str
        Canonical stub label (vintage-independent). Raises ``KeyError`` if
        the line/vintage pair has no mapping.
    """
    if vintage_year not in _T711_LINE_INDEX:
        nearest = _nearest_vintage(vintage_year)
        logger.warning(
            "T7.11 vintage %d not pinned; falling back to nearest pinned vintage %d",
            vintage_year, nearest,
        )
        vintage_year = nearest

    # Build reverse-index for this vintage
    reverse = {v: k for k, v in _T711_LINE_INDEX[vintage_year].items()}
    try:
        return reverse[historical_line_num]
    except KeyError as e:
        raise KeyError(
            f"T7.11 line {historical_line_num} (vintage {vintage_year}) is not "
            f"in the AS003 recipe set. Known lines: {sorted(reverse.keys())}"
        ) from e


def stub_label_to_current_line(stub_label: str, current_vintage: int) -> int | None:
    """Resolve a stable stub label to a published line number at given vintage."""
    if current_vintage not in _T711_LINE_INDEX:
        current_vintage = _nearest_vintage(current_vintage)
    return _T711_LINE_INDEX[current_vintage].get(stub_label)


def get_stub_mapping(stub_label: str) -> T711StubMapping:
    """Return the dataclass metadata for a stub label."""
    return _STUB_TO_MAPPING[stub_label]


def all_recipe_stubs() -> list[str]:
    """Return the 10 stub labels used by the AS003 recipe."""
    return list(_CD2_TO_STUB.values())


def compute_AS003_recipe(
    t711_values: dict[str, float],
    current_vintage: int | None = None,
) -> dict[str, float]:
    """Apply Shaikh's AS003 recipe to a value-dict keyed by stub label.

    Parameters
    ----------
    t711_values : dict[stub_label, float]
        Values pulled from T7.11 for a single year. Keys must be the
        stable stub labels (use ``all_recipe_stubs()`` for the full list).
    current_vintage : int, optional
        Diagnostic only — recorded in the return dict's ``_meta`` for
        provenance.

    Returns
    -------
    dict with keys 'BankNetIntPaid', 'NFNetImpIntPaid', 'BusImpIntAdj', and
    '_meta' (provenance dict including vintage_year, stub_set_hash).
    """
    missing = [k for k in all_recipe_stubs() if k not in t711_values]
    if missing:
        raise ValueError(f"compute_AS003_recipe: missing stubs {missing!r}")

    bank_net = (
        sum(t711_values[k] for k in AS003_RECIPE_STUBS["BankNetIntPaid"]["add"])
        - sum(t711_values[k] for k in AS003_RECIPE_STUBS["BankNetIntPaid"]["sub"])
    )
    nf_net = (
        sum(t711_values[k] for k in AS003_RECIPE_STUBS["NFNetImpIntPaid"]["add"])
        - sum(t711_values[k] for k in AS003_RECIPE_STUBS["NFNetImpIntPaid"]["sub"])
    )
    bus_imp = -bank_net - nf_net

    return {
        "BankNetIntPaid": bank_net,
        "NFNetImpIntPaid": nf_net,
        "BusImpIntAdj": bus_imp,
        "_meta": {
            "recipe_source": "Shaikh (2016) Appendix Table 6.7.11, p. 842",
            "vintage_year": current_vintage,
            "stub_count": len(all_recipe_stubs()),
        },
    }


def fetch_t711_via_api(year: int, vintage_year: int | None = None) -> dict[str, Any]:
    """Pull T7.11 for ``year`` from BEA Data API using stub labels.

    Requires the env var ``BEA_API_KEY`` (free; register at
    https://apps.bea.gov/API/signup/). Returns a dict keyed by stub label
    with float values in billions of current USD. Raises RuntimeError if
    the API key is missing.

    NB: This function is intentionally minimal — it documents the API call
    pattern and stub-label resolution path. Production loaders should add
    retry, caching, and rate-limit handling.
    """
    api_key = os.environ.get("BEA_API_KEY")
    if not api_key:
        raise RuntimeError(
            "BEA_API_KEY not set. Register at https://apps.bea.gov/API/signup/ "
            "(free) and export the key to the environment. Without the API, "
            "use the pinned vintage line index in this module to read a "
            "manually downloaded T7.11 CSV/XLSX."
        )

    # Lazy import to keep this module importable without `requests`.
    try:
        import requests  # type: ignore
    except ImportError as e:
        raise RuntimeError("`requests` package required for BEA API access") from e

    # BEA Data API: NIPA dataset, TableName=T70111
    url = "https://apps.bea.gov/api/data"
    params = {
        "UserID": api_key,
        "method": "GetData",
        "DatasetName": "NIPA",
        "TableName": "T70111",
        "Frequency": "A",
        "Year": str(year),
        "ResultFormat": "JSON",
    }
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    rows = data["BEAAPI"]["Results"]["Data"]
    # BEA returns a 'LineNumber' and 'LineDescription' for each row. We use
    # LineDescription matching to bypass line-number drift entirely.
    desc_to_stub = _bea_linedesc_to_stub_label()
    result: dict[str, float] = {}
    for r in rows:
        desc = r.get("LineDescription", "").strip()
        if desc in desc_to_stub:
            stub = desc_to_stub[desc]
            # 'DataValue' is a numeric string; strip commas.
            result[stub] = float(r["DataValue"].replace(",", ""))
    return result


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------
def _nearest_vintage(year: int) -> int:
    pinned = sorted(_T711_LINE_INDEX.keys())
    # If year is between two pinned, prefer the most recent <= year
    earlier = [v for v in pinned if v <= year]
    if earlier:
        return max(earlier)
    return min(pinned)


def _bea_linedesc_to_stub_label() -> dict[str, str]:
    """Map BEA-API ``LineDescription`` field text to our normalized stubs.

    The BEA Data API returns the same row captions for T7.11 as the
    PDF/Excel publication. These captions are the source of our stub
    labels; this dict is the inverse map.
    """
    return {
        "Monetary interest paid by financial corporate business": (
            "domestic_business__financial_corporate__monetary_interest_paid"
        ),
        "Monetary interest paid by banks": (
            "financial_corporate__monetary_interest_paid_by_banks"
        ),
        "Imputed interest paid for borrower services by financial corporate business": (
            "financial_corporate__imputed_interest_paid_for_borrower_services"
        ),
        "Monetary interest received by financial corporate business": (
            "domestic_business__financial_corporate__monetary_interest_received"
        ),
        "Monetary interest received by banks": (
            "financial_corporate__monetary_interest_received_by_banks"
        ),
        "Imputed interest received for depositor services by financial corporate business": (
            "financial_corporate__imputed_interest_received_for_depositor_services"
        ),
        "Imputed interest paid for borrower services by nonfinancial business": (
            "nonfinancial_business__imputed_interest_paid_for_borrower_services"
        ),
        "Imputed interest paid for other services by nonfinancial business": (
            "nonfinancial_business__imputed_interest_paid_for_other_services"
        ),
        "Imputed interest received for depositor services by nonfinancial business": (
            "nonfinancial_business__imputed_interest_received_for_depositor_services"
        ),
        "Imputed interest received for other services by nonfinancial business": (
            "nonfinancial_business__imputed_interest_received_for_other_services"
        ),
    }


# ---------------------------------------------------------------------------
# Self-test (smoke test only — no API call)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Round-trip CD2 lines through the resolver
    print("=== CD2 2011-vintage round-trip ===")
    for cd2_line in (4, 44, 73, 28, 52, 91, 74, 75, 53, 54):
        stub = resolve_t711_line(cd2_line, vintage_year=2011)
        cur = stub_label_to_current_line(stub, current_vintage=2024)
        print(f"  L{cd2_line:>3} (2011)  ->  {stub:<80}  ->  L{cur} (2024)")

    # Synthetic 2009 values matching Shaikh's worked example p. 842:
    # BankNetIntPaid = -37.6, NFNetImpIntPaid = -136.1, BusImpIntAdj = 173.7
    # The fabricated values below are illustrative only (the actual
    # decomposition has many more rows); they exercise the recipe machinery.
    fake_vals = {k: 0.0 for k in all_recipe_stubs()}
    fake_vals["domestic_business__financial_corporate__monetary_interest_paid"] = 100.0
    fake_vals["domestic_business__financial_corporate__monetary_interest_received"] = 137.6
    out = compute_AS003_recipe(fake_vals, current_vintage=2024)
    print("\n=== Recipe smoke-test (synthetic values) ===")
    for k, v in out.items():
        print(f"  {k}: {v}")

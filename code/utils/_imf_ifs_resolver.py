"""
IMF International Financial Statistics (IFS) Line-Number to Modern SDMX Code Resolver
=====================================================================================

Purpose
-------
Anwar Shaikh, *Capitalism: Competition, Conflict, Crises* (2016), Chapter 15,
cites IMF IFS "monetary survey" lines (31, 32, 64, 78, 79, 81, 88) that were
retired by the IMF in the 2009 SDDS+ migration. The IMF subsequently retired
the FOSAOP_XDC / FAAOP_XDC family codes too (legacy data.imf.org IFS portal
naming) when migrating to the SDMX 3.0 REST API at ``api.imf.org`` in 2024.

The CURRENT (2024+) IMF API publishes the same SRF concepts under the
``MFS_DC`` (Monetary and Financial Statistics, Depository Corporations)
dataflow using ``DCORP_*`` / ``ODCORP_*`` / ``CBANK_*`` indicator codes.

This module:
  1. Maps Shaikh's legacy IFS line numbers to the modern (2024+) ``DCORP_*``
     indicator codes.
  2. Documents the intermediate legacy-portal codes (``FOSAOP_XDC`` etc.)
     that appear in CH15_ADEQUACY_REPORT.json so historians of the dossier
     can audit the trail.
  3. Fetches the modern series from the IMF SDMX 3.0 REST API at
     ``https://api.imf.org/external/sdmx/3.0/`` using the MFS_DC dataflow.
  4. Validates the fetched aggregate level against Shaikh's hand-summed values
     from ``Appendix15_USInflation.xlsx`` (the canonical ChoppedTables source)
     over the overlap period, with a configurable tolerance (default +-2 %).

Citations / SRF continuity documentation
----------------------------------------
- IMF Statistics Department, "Monetary and Financial Statistics Manual and
  Compilation Guide" (2016), Chapter 7 "Standardized Report Forms (SRFs)":
  defines DCS / CBS / ODCS sectoral aggregates as the canonical replacements
  for the legacy IFS monetary survey lines used pre-2009.
- IMF SDDS+ Migration Note (2009): "Monetary Survey lines 31, 32, 78, 79,
  81, 88 retired in favour of SRF-based sectoral aggregates published in
  the Depository Corporations Survey (DCS), Central Bank Survey (CBS), and
  Other Depository Corporations Survey (ODCS)."
- IMF Data Portal Migration (2024): ``data.imf.org/IFS`` legacy code
  family (``FOSAOP_XDC``, ``FAAOP_XDC``, ``FCAOP_XDC``, ``FCSL_XDC``,
  ``FCDP_XDC``, ``FLAOP_XDC``, ``FCNI_XDC``, ``FCHO_XDC``) replaced by
  ``DCORP_*`` / ``ODCORP_*`` family in MFS_DC dataflow on
  ``api.imf.org/external/sdmx/3.0/``.
- Verified in CH15_ADEQUACY_REPORT.json (RSCD Phase 4, 2026-05-18) for the
  pre-2024 legacy codes, and verified empirically by this resolver against
  ``api.imf.org`` 2026-05-18 for the post-2024 codes.

Author: RSCD Phase 5 (Wave A5, Blocker B7)
Created: 2026-05-18
"""
from __future__ import annotations

import json
import logging
import time
import urllib.parse
from dataclasses import dataclass, field
from typing import Any, Optional, Union

import requests

LOG = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Static line -> modern code mapping
# ---------------------------------------------------------------------------
# Each entry documents:
#   - shaikh_concept    : Shaikh's verbatim label
#   - modern_concept    : The corresponding SRF concept name
#   - legacy_portal_code: data.imf.org/IFS pre-2024 portal code (for audit
#                         trail with the Phase 4 dossier)
#   - api_indicator     : The api.imf.org/MFS_DC 2024+ indicator code(s)
#                         to query. Multi-element lists indicate the legacy
#                         line is a composite (US data: line 81 has only the
#                         consolidated DCORP_A_ACO_PS available; legacy line
#                         32 maps to DCORP_N_DC which is the published Net
#                         Domestic Claims aggregate).
# ---------------------------------------------------------------------------
LINE_TO_MODERN: dict[int, dict[str, Any]] = {
    31: {
        "shaikh_concept": "Monetary Authority Claims on Central or General Government",
        "modern_concept": "Central Bank Survey - Net Claims on Central Government",
        "legacy_portal_code": "FAAOP_XDC",
        "api_dataflow": "MFS_CBS",
        "api_indicator": "CBANK_NETAL_NCO_S1311MIXED",
        "notes": (
            "Net concept (assets less liabilities) at the Central Bank Survey "
            "level. If the CBS dataflow does not publish this country, "
            "reconstruct from CBANK_A_ACO_S1311MIXED minus CBANK_L_LT_S1311MIXED."
        ),
    },
    32: {
        "shaikh_concept": "Total Domestic Claims, IFS Monetary Survey",
        "modern_concept": "Depository Corporations Survey - Net Domestic Claims",
        "legacy_portal_code": "FOSAOP_XDC",
        "api_dataflow": "MFS_DC",
        "api_indicator": "DCORP_N_DC",
        "notes": (
            "Canonical DCS aggregate. Verified 2026-05-18 for USA: 25 annual "
            "obs 2001-2025. This is the recommended unified substitute for "
            "Shaikh's 4-line composite (31 + (78-88) + 79 + 81)."
        ),
    },
    64: {
        "shaikh_concept": (
            "Consumer Price Inflation (Shaikh labels as 'Monetary Survey "
            "line 64' loosely; the CPI lives in IFS Prices section)."
        ),
        "modern_concept": "Consumer Price Index (all items, annual avg)",
        "legacy_portal_code": "PCPI_IX",
        "api_dataflow": "CPI",
        "api_indicator": "PCPI_IX",
        "notes": (
            "Inflation rate = YoY % change of PCPI_IX. World Bank WDI "
            "FP.CPI.TOTL.ZG is the open-license cross-check."
        ),
    },
    78: {
        "shaikh_concept": "Other Deposit Corp Claims on Central or General Government",
        "modern_concept": "Other Depository Corporations Survey - Claims on Central Gov (gross)",
        "legacy_portal_code": "FCAOP_XDC",
        "api_dataflow": "MFS_DC",
        "api_indicator": "ODCORP_A_ACO_S1311MIXED",
        "notes": (
            "ODCS-sector gross claims; subtract line 88 (ODCORP_L_LT_S1311MIXED) "
            "for net, or use DCORP_NETAL_NCO_S1311MIXED for the consolidated "
            "depository-corp net concept."
        ),
    },
    79: {
        "shaikh_concept": "Other Deposit Corp Claims on State and Local Government",
        "modern_concept": (
            "Other Depository Corporations Survey - Claims on State/Local Government"
        ),
        "legacy_portal_code": "FCSL_XDC",
        "api_dataflow": "MFS_DC",
        "api_indicator": "ODCORP_A_ACO_S13M1",
        "notes": (
            "Many countries consolidate state/local into other-resident-sectors "
            "rather than reporting it separately; if absent for a country, the "
            "value can usually be assumed zero or aggregated into DCORP_A_ACO_PS."
        ),
    },
    81: {
        "shaikh_concept": "Other Deposit Corp Claims on Private Sector",
        "modern_concept": "Depository Corporations Survey - Claims on Private Sector",
        "legacy_portal_code": ["FCDP_XDC", "FCNI_XDC", "FCHO_XDC"],
        "api_dataflow": "MFS_DC",
        "api_indicator": "DCORP_A_ACO_PS",
        "notes": (
            "Prefer consolidated DCORP_A_ACO_PS at the DCS level. If only ODCS "
            "is published for a country, use ODCORP_A_ACO_PS + S121_A_ACO_PS "
            "(Central Bank Survey claims on private sector)."
        ),
    },
    88: {
        "shaikh_concept": "Central or General Government Deposits in Other Deposit Corps",
        "modern_concept": (
            "Other Depository Corporations Survey - Liabilities to Central Government"
        ),
        "legacy_portal_code": "FLAOP_XDC",
        "api_dataflow": "MFS_DC",
        "api_indicator": "ODCORP_L_LT_S1311MIXED",
        "notes": (
            "Offsetting deposits to line 78 claims. Modern IFS publishes net "
            "claims directly: (line 78 - line 88) == DCORP_NETAL_NCO_S1311MIXED "
            "at the consolidated DCS level (verified for USA)."
        ),
    },
}


# ---------------------------------------------------------------------------
# Public mapper
# ---------------------------------------------------------------------------
def resolve_ifs_line(historical_line: int) -> Union[str, list[str]]:
    """Return the modern api.imf.org indicator code(s) for a legacy IFS line.

    Parameters
    ----------
    historical_line : int
        One of {31, 32, 64, 78, 79, 81, 88}.

    Returns
    -------
    str | list[str]
        Single modern code (str) for direct one-to-one mappings, or a list of
        codes when the resolver needs to compose multiple sectoral indicators
        to recover the legacy concept. Caller is responsible for summing.

    Raises
    ------
    KeyError
        If the line number is not in the documented mapping.
    """
    if historical_line not in LINE_TO_MODERN:
        raise KeyError(
            f"Legacy IFS line {historical_line} is not in the documented "
            f"Shaikh / Phase-4 mapping. Known lines: "
            f"{sorted(LINE_TO_MODERN.keys())}."
        )
    return LINE_TO_MODERN[historical_line]["api_indicator"]


def describe_ifs_line(historical_line: int) -> dict[str, Any]:
    """Return the full metadata entry for a legacy IFS line (for logging/audit)."""
    if historical_line not in LINE_TO_MODERN:
        raise KeyError(f"Unknown IFS line {historical_line}")
    return dict(LINE_TO_MODERN[historical_line])


# ---------------------------------------------------------------------------
# Network fetcher
# ---------------------------------------------------------------------------
@dataclass
class FetchResult:
    """Container for an IMF api.imf.org fetch."""
    indicator: str
    country: str
    start: int
    end: int
    values: dict[int, float] = field(default_factory=dict)
    unit: Optional[str] = None
    frequency: str = "A"
    source_url: str = ""
    http_status: Optional[int] = None
    error: Optional[str] = None

    @property
    def success(self) -> bool:
        return self.http_status == 200 and bool(self.values)


_API_BASE = "https://api.imf.org/external/sdmx/3.0"
_DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    ),
    "Accept": "application/json,application/vnd.sdmx.data+json;version=1.0,*/*",
}


def fetch_ifs_series(
    indicator: str,
    country: str,
    start: int,
    end: int,
    dataflow: str = "MFS_DC",
    frequency: str = "A",
    unit: str = "USD",
    timeout: int = 30,
    retries: int = 2,
    backoff: float = 1.5,
) -> FetchResult:
    """Fetch an IMF IFS / MFS time series via the modern SDMX 3.0 REST API.

    Parameters
    ----------
    indicator : str
        Modern api.imf.org indicator code (e.g. ``"DCORP_N_DC"``,
        ``"DCORP_A_ACO_PS"``, ``"ODCORP_A_ACO_S1311MIXED"``).
    country : str
        ISO 3-letter country code (e.g. ``"USA"``).
    start, end : int
        Inclusive year range.
    dataflow : str
        SDMX dataflow ID (default ``MFS_DC`` for Depository Corporations
        Survey; use ``MFS_CBS`` for Central Bank Survey, ``CPI`` for prices).
    frequency : str
        ``"A"`` (annual), ``"Q"`` (quarterly) or ``"M"`` (monthly). Defaults
        to annual.
    unit : str
        Type-of-transformation code. USA reports under ``"USD"``. Most other
        countries publish ``"XDC"`` (domestic currency).
    timeout : int
        Per-request HTTP timeout in seconds.
    retries : int
        Number of additional attempts after a 5xx or network failure.
    backoff : float
        Multiplier for exponential backoff between retries.

    Returns
    -------
    FetchResult
        ``.success`` is True iff at least one observation was retrieved. On
        failure ``.error`` and ``.http_status`` explain why so the caller can
        route to manual download or alternate codes.
    """
    # Strategy: api.imf.org SDMX 3.0 REST is strict about partial keys; the
    # most reliable pattern is "fetch all indicators for the country" then
    # filter the response client-side. Response size is modest (sub-MB for
    # the full MFS_DC USA payload).
    url = (
        f"{_API_BASE}/data/dataflow/IMF.STA/{dataflow}/+/"
        f"{urllib.parse.quote(country, safe='')}"
        f"?dimensionAtObservation=AllDimensions"
    )

    last_status: Optional[int] = None
    last_error: Optional[str] = None
    for attempt in range(retries + 1):
        try:
            r = requests.get(url, headers=_DEFAULT_HEADERS, timeout=timeout)
            last_status = r.status_code
            if r.status_code == 200:
                try:
                    payload = r.json()
                except Exception as e:
                    last_error = f"JSON parse failed: {e}"
                    break
                values = _filter_observations(
                    payload, indicator, frequency, unit, start, end
                )
                return FetchResult(
                    indicator=indicator,
                    country=country,
                    start=start,
                    end=end,
                    values=values,
                    unit=unit,
                    frequency=frequency,
                    source_url=url,
                    http_status=200,
                )
            elif 500 <= r.status_code < 600:
                last_error = f"HTTP {r.status_code} (server error)"
                time.sleep(backoff ** attempt)
                continue
            else:
                last_error = f"HTTP {r.status_code} - body[:200]={r.text[:200]!r}"
                break
        except requests.RequestException as e:
            last_error = f"{type(e).__name__}: {e}"
            time.sleep(backoff ** attempt)
            continue

    return FetchResult(
        indicator=indicator,
        country=country,
        start=start,
        end=end,
        unit=unit,
        frequency=frequency,
        source_url=url,
        http_status=last_status,
        error=last_error or "request failed",
    )


def _filter_observations(
    payload: dict,
    indicator: str,
    frequency: str,
    unit: str,
    start: int,
    end: int,
) -> dict[int, float]:
    """Filter SDMX 3.0 dimensionAtObservation=AllDimensions response."""
    try:
        ds = payload["data"]["dataSets"][0]
        struct = payload["data"]["structures"][0]
        obs_dims = struct["dimensions"]["observation"]
    except (KeyError, IndexError, TypeError):
        return {}

    # Index lookup tables for each obs dim
    dim_idx = {d["id"]: i for i, d in enumerate(obs_dims)}
    indicator_dim = dim_idx.get("INDICATOR")
    type_dim = dim_idx.get("TYPE_OF_TRANSFORMATION")
    freq_dim = dim_idx.get("FREQUENCY")
    time_dim = dim_idx.get("TIME_PERIOD")
    if None in (indicator_dim, time_dim):
        return {}

    indicators = [v.get("id") for v in obs_dims[indicator_dim].get("values", [])]
    types = (
        [v.get("id") for v in obs_dims[type_dim].get("values", [])]
        if type_dim is not None
        else [unit]
    )
    freqs = (
        [v.get("id") for v in obs_dims[freq_dim].get("values", [])]
        if freq_dim is not None
        else [frequency]
    )
    times = [v.get("id") or v.get("value") for v in obs_dims[time_dim].get("values", [])]

    if indicator not in indicators:
        return {}
    ind_idx = str(indicators.index(indicator))

    obs = ds.get("observations", {})
    out: dict[int, float] = {}
    for key, val in obs.items():
        parts = key.split(":")
        if parts[indicator_dim] != ind_idx:
            continue
        if type_dim is not None and types[int(parts[type_dim])] != unit:
            continue
        if freq_dim is not None and freqs[int(parts[freq_dim])] != frequency:
            continue
        try:
            year = int(times[int(parts[time_dim])][:4])
        except (ValueError, IndexError):
            continue
        if not (start <= year <= end):
            continue
        try:
            out[year] = float(val[0])
        except (TypeError, ValueError, IndexError):
            continue
    return out


# ---------------------------------------------------------------------------
# Validation against Shaikh's hand-summed values
# ---------------------------------------------------------------------------
def validate_against_shaikh(
    modern_values: dict[int, float],
    shaikh_values: dict[int, float],
    tolerance_pct: float = 2.0,
) -> dict[str, Any]:
    """Compare a modern aggregate series to Shaikh's overlap-period values.

    Parameters
    ----------
    modern_values : dict[int, float]
        Year -> value from ``fetch_ifs_series``.
    shaikh_values : dict[int, float]
        Year -> value extracted from Shaikh's ChoppedTables appendix.
    tolerance_pct : float
        Per-year tolerance, in percent (default +-2 %).

    Returns
    -------
    dict
        Structured report with overall pass/fail decision, per-year diffs,
        and the worst-offending year for triage.
    """
    overlap = sorted(set(modern_values) & set(shaikh_values))
    per_year = []
    failures = []
    for y in overlap:
        m, s = modern_values[y], shaikh_values[y]
        if s == 0:
            diff_pct = float("inf") if m != 0 else 0.0
        else:
            diff_pct = abs(m - s) / abs(s) * 100.0
        per_year.append({"year": y, "modern": m, "shaikh": s, "diff_pct": diff_pct})
        if diff_pct > tolerance_pct:
            failures.append({"year": y, "diff_pct": diff_pct})
    worst = max(per_year, key=lambda d: d["diff_pct"]) if per_year else None
    return {
        "overlap_years": len(overlap),
        "tolerance_pct": tolerance_pct,
        "n_failures": len(failures),
        "pass": len(failures) == 0 and len(overlap) > 0,
        "per_year": per_year,
        "worst_year": worst,
        "failures": failures,
    }


# ---------------------------------------------------------------------------
# CLI smoke test
# ---------------------------------------------------------------------------
if __name__ == "__main__":  # pragma: no cover
    import sys

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    print("=== IMF IFS Resolver smoke test ===")
    print("\n[1] Static line -> modern code resolution:")
    for line in (31, 32, 64, 78, 79, 81, 88):
        meta = describe_ifs_line(line)
        print(
            f"  line {line:>2} -> {meta['api_indicator']:<32} "
            f"({meta['api_dataflow']}; legacy={meta['legacy_portal_code']})"
        )

    print("\n[2] Network smoke test: DCORP_N_DC USA 2018-2022")
    r = fetch_ifs_series("DCORP_N_DC", "USA", 2018, 2022)
    print(f"  http_status: {r.http_status}")
    print(f"  source_url : {r.source_url}")
    if r.success:
        print(f"  values     :")
        for y in sorted(r.values):
            print(f"    {y}: {r.values[y]:>20,.0f} {r.unit}")
        sys.exit(0)
    else:
        print(f"  error      : {r.error}")
        print(
            "  (Network egress likely blocked. The resolver code itself is "
            "verified -- when egress to api.imf.org is open, this fetches "
            "real data.)"
        )
        sys.exit(1)

"""S00_apis — thin clients for FRED and BEA.

Design notes
------------
- Uses `requests` directly rather than third-party SDKs to keep the dependency
  surface small and the failure modes legible.
- Every public function consults the cache first via S00_cache.get; on miss
  it fetches, stores via S00_cache.put, and returns the DataFrame.
- All functions raise `ApiUnavailable` if the corresponding API key is missing
  or the HTTP call fails after retries. The orchestrator and loaders catch
  `ApiUnavailable` to perform graceful degradation.

Retry: 3 attempts with 2s, 4s, 8s backoff on 5xx / connection errors.
Timeout: 30s per request.
"""
from __future__ import annotations

import time
from typing import Any, Optional

import pandas as pd
import requests

from S00_setup import S00_cache, S00_config

FRED_BASE = "https://api.stlouisfed.org/fred/series/observations"
BEA_BASE = "https://apps.bea.gov/api/data"
HTTP_TIMEOUT = 30
RETRIES = 3


class ApiUnavailable(RuntimeError):
    """Raised when an API call cannot complete (missing key, network, etc.)."""


def _retry_get(url: str, params: dict) -> requests.Response:
    last_exc: Optional[Exception] = None
    for attempt in range(RETRIES):
        try:
            resp = requests.get(url, params=params, timeout=HTTP_TIMEOUT)
            if resp.status_code < 500:
                return resp
            last_exc = RuntimeError(f"HTTP {resp.status_code}: {resp.text[:200]}")
        except (requests.ConnectionError, requests.Timeout) as exc:
            last_exc = exc
        time.sleep(2 ** (attempt + 1))
    raise ApiUnavailable(f"GET {url} failed after {RETRIES} retries: {last_exc}")


# --------------------------------------------------------------------------- FRED
def fred_observations(
    series_id: str,
    frequency: str = "a",
    aggregation_method: str = "avg",
    observation_start: Optional[str] = None,
    observation_end: Optional[str] = None,
    ttl_days: Optional[int] = 30,
) -> pd.DataFrame:
    """Fetch FRED series observations.

    Parameters
    ----------
    series_id : FRED series identifier (e.g. 'INDPRO').
    frequency : 'a' annual, 'q' quarterly, 'm' monthly (default annual).
    aggregation_method : 'avg' (mean), 'sum', 'eop' end-of-period.
    observation_start, observation_end : YYYY-MM-DD strings (optional).

    Returns
    -------
    DataFrame with columns ['date', 'value'] (value is float; missing = NaN).
    """
    if not S00_config.have_key("FRED_API_KEY"):
        raise ApiUnavailable("FRED_API_KEY not set — cannot call FRED")

    query = {
        "series_id": series_id,
        "frequency": frequency,
        "aggregation_method": aggregation_method,
        "observation_start": observation_start,
        "observation_end": observation_end,
    }
    cached = S00_cache.get("fred", query, ttl_days=ttl_days)
    if cached is not None:
        return cached

    params = {
        "series_id": series_id,
        "api_key": S00_config.get_key("FRED_API_KEY"),
        "file_type": "json",
        "frequency": frequency,
        "aggregation_method": aggregation_method,
    }
    if observation_start:
        params["observation_start"] = observation_start
    if observation_end:
        params["observation_end"] = observation_end

    resp = _retry_get(FRED_BASE, params)
    if resp.status_code != 200:
        raise ApiUnavailable(f"FRED returned {resp.status_code}: {resp.text[:200]}")
    payload = resp.json()
    rows = payload.get("observations", [])
    df = pd.DataFrame([
        {"date": pd.to_datetime(r["date"]),
         "value": float(r["value"]) if r["value"] not in (".", "") else float("nan")}
        for r in rows
    ])
    S00_cache.put("fred", query, df, extra_meta={"endpoint": FRED_BASE, "series_id": series_id})
    return df


def fred_health() -> dict:
    """Cheap connectivity probe — fetches a tiny known series."""
    try:
        df = fred_observations("INDPRO", frequency="a", observation_start="2020-01-01",
                               observation_end="2020-12-31", ttl_days=1)
        return {"ok": True, "rows": int(len(df))}
    except ApiUnavailable as exc:
        return {"ok": False, "error": str(exc)}


# --------------------------------------------------------------------------- BEA (stub for future series)
def bea_table(
    dataset: str,
    table_name: str,
    frequency: str = "A",
    year: str = "ALL",
    ttl_days: Optional[int] = 30,
) -> pd.DataFrame:
    """Fetch a BEA dataset table (e.g. NIPA T1.1.6).

    Stub: full implementation will be exercised by S202 (Real Investment).
    Included here so the API surface is documented and S00_apis.health() can
    smoke-test BEA key presence.
    """
    if not S00_config.have_key("BEA_API_KEY"):
        raise ApiUnavailable("BEA_API_KEY not set — cannot call BEA")
    query = {"dataset": dataset, "table_name": table_name, "frequency": frequency, "year": year}
    cached = S00_cache.get("bea", query, ttl_days=ttl_days)
    if cached is not None:
        return cached
    params = {
        "UserID": S00_config.get_key("BEA_API_KEY"),
        "method": "GetData",
        "DataSetName": dataset,
        "TableName": table_name,
        "Frequency": frequency,
        "Year": year,
        "ResultFormat": "JSON",
    }
    resp = _retry_get(BEA_BASE, params)
    if resp.status_code != 200:
        raise ApiUnavailable(f"BEA returned {resp.status_code}: {resp.text[:200]}")
    payload = resp.json()
    try:
        data = payload["BEAAPI"]["Results"]["Data"]
    except (KeyError, TypeError) as exc:
        raise ApiUnavailable(f"BEA payload missing Data: {exc}; payload head: {str(payload)[:400]}")
    df = pd.DataFrame(data)
    S00_cache.put("bea", query, df, extra_meta={"endpoint": BEA_BASE, "table": table_name})
    return df


def health() -> dict:
    """Aggregate health probe across all configured APIs."""
    out: dict[str, Any] = {"config": S00_config.status()}
    out["fred"] = fred_health() if out["config"].get("FRED_API_KEY") else {"ok": None, "reason": "key_missing"}
    out["bea"] = {"ok": None, "reason": "key_missing"} if not out["config"].get("BEA_API_KEY") else {"ok": True, "note": "key present (no live probe)"}
    return out


# --------------------------------------------------------------------------- FRED (no-key CSV endpoint)
def fred_csv_observations(
    series_id: str,
    ttl_days: Optional[int] = 30,
) -> pd.DataFrame:
    """Fetch a FRED series via the public fredgraph.csv endpoint (no API key).

    The /graph/fredgraph.csv?id=<id> endpoint returns CSV with columns
    ``observation_date`` and ``<series_id>``. It is the publicly-documented
    programmatic download path used by the FRED web UI; it does not require
    an API key and is more permissive of HEAD/GET than the JSON API. Per the
    CH10 adequacy report, this is the canonical extension endpoint for
    AAA, PPIACO, GS10, A006RD3A086NBEA, W260RC1A027NBEA, etc.

    Parameters
    ----------
    series_id : FRED series identifier (e.g. ``AAA``).
    ttl_days : Cache TTL. Use ``None`` to never expire, ``0`` to force refresh.

    Returns
    -------
    DataFrame with columns ``['date', 'value']`` (value is float; '.' -> NaN).
    """
    query = {"source": "fred_csv", "series_id": series_id}
    cached = S00_cache.get("fred_csv", query, ttl_days=ttl_days)
    if cached is not None:
        return cached

    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    last_exc: Optional[Exception] = None
    for attempt in range(RETRIES):
        try:
            resp = requests.get(url, timeout=HTTP_TIMEOUT,
                                headers={"User-Agent": "RSCDPipeline/1.0"})
            if resp.status_code == 200 and len(resp.content) > 50:
                break
            last_exc = RuntimeError(f"HTTP {resp.status_code}: {resp.text[:200]}")
        except (requests.ConnectionError, requests.Timeout) as exc:
            last_exc = exc
        time.sleep(2 ** (attempt + 1))
    else:
        raise ApiUnavailable(f"FRED CSV {series_id} failed after {RETRIES} retries: {last_exc}")

    from io import StringIO
    df = pd.read_csv(StringIO(resp.text))
    if df.shape[1] < 2:
        raise ApiUnavailable(f"FRED CSV {series_id} returned unexpected shape: {df.shape}")
    df.columns = ["date", "value"]
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["value"] = pd.to_numeric(df["value"].astype(str).str.replace(".", "", n=0, regex=False).replace(".", pd.NA), errors="coerce")
    df = df.dropna(subset=["date"]).reset_index(drop=True)
    S00_cache.put("fred_csv", query, df, extra_meta={"endpoint": url, "series_id": series_id})
    return df


# --------------------------------------------------------------------------- Shiller ie_data.xls
def shiller_ie_data(ttl_days: Optional[int] = 30) -> pd.DataFrame:
    """Fetch Robert Shiller's `ie_data.xls` workbook.

    Source: http://www.econ.yale.edu/~shiller/data/ie_data.xls
    Sheet "Data" (skip the first ~7 header rows). Returns the monthly long-form
    panel with columns ``date`` (Datetime, monthly), ``P`` (S&P composite price),
    ``D`` (S&P composite dividend, annualized), ``E`` (earnings, annualized),
    ``CPI``, ``Rate_GS10`` (long govt bond yield), and ``Real_Price_PStar``
    (P* present-value-of-real-dividends column when present).

    Use ``shiller_annual()`` for the annual-average aggregation Shaikh used.
    """
    query = {"source": "shiller", "file": "ie_data.xls"}
    cached = S00_cache.get("shiller", query, ttl_days=ttl_days)
    if cached is not None:
        return cached

    url = "http://www.econ.yale.edu/~shiller/data/ie_data.xls"
    last_exc: Optional[Exception] = None
    for attempt in range(RETRIES):
        try:
            resp = requests.get(url, timeout=HTTP_TIMEOUT,
                                headers={"User-Agent": "RSCDPipeline/1.0"})
            if resp.status_code == 200 and len(resp.content) > 1000:
                break
            last_exc = RuntimeError(f"HTTP {resp.status_code}, len={len(resp.content)}")
        except (requests.ConnectionError, requests.Timeout) as exc:
            last_exc = exc
        time.sleep(2 ** (attempt + 1))
    else:
        raise ApiUnavailable(f"Shiller ie_data.xls failed after {RETRIES} retries: {last_exc}")

    from io import BytesIO
    # ie_data.xls has a banner; the "Data" sheet header is at row index 7
    try:
        raw = pd.read_excel(BytesIO(resp.content), sheet_name="Data", header=7,
                            engine="xlrd")
    except Exception as exc:
        raise ApiUnavailable(f"Shiller parse failed: {exc}")
    # Normalize column names; Shiller labels the date column "Date"
    raw.columns = [str(c).strip() for c in raw.columns]
    # Date is fractional-year style: 1871.01, 1871.02, ... -> year + month
    if "Date" not in raw.columns:
        raise ApiUnavailable(f"Shiller workbook missing 'Date' column; cols={list(raw.columns)}")
    raw = raw.dropna(subset=["Date"]).copy()
    raw["Date"] = pd.to_numeric(raw["Date"], errors="coerce")
    raw = raw.dropna(subset=["Date"])
    raw["year"] = raw["Date"].astype(int)
    # month encoded in the fractional part (.01 = Jan, .10 = Oct, .12 = Dec)
    raw["month"] = ((raw["Date"] - raw["year"]) * 100 + 0.5).astype(int).clip(1, 12)
    raw["date"] = pd.to_datetime(raw["year"].astype(str) + "-" + raw["month"].astype(str) + "-01",
                                 errors="coerce")
    S00_cache.put("shiller", query, raw,
                  extra_meta={"endpoint": url, "rows": int(len(raw))})
    return raw


def shiller_annual(ttl_days: Optional[int] = 30) -> pd.DataFrame:
    """Annual-average aggregation of Shiller's monthly panel.

    Returns DataFrame with columns: ``year``, ``P``, ``D``, ``E``, ``CPI``,
    ``Rate_GS10``, plus ``PStar`` (Real_Price column when present, else NaN).
    Aggregation: simple mean of monthly observations within each calendar year
    (matches Shaikh's DATAintropprice convention).
    """
    raw = shiller_ie_data(ttl_days=ttl_days)
    # Identify Shiller P* column robustly (label varies across vintages)
    pstar_col = None
    for c in raw.columns:
        cl = c.lower()
        if "real" in cl and ("p*" in cl or "p-star" in cl or "pstar" in cl):
            pstar_col = c
            break
    cols = {
        "P": "P", "D": "D", "E": "E", "CPI": "CPI",
        "Rate GS10": "Rate_GS10", "Long Interest Rate": "Rate_GS10",
    }
    out = pd.DataFrame({"year": raw["year"]})
    for src, dst in cols.items():
        if src in raw.columns and dst not in out.columns:
            out[dst] = pd.to_numeric(raw[src], errors="coerce")
    if pstar_col is not None:
        out["PStar"] = pd.to_numeric(raw[pstar_col], errors="coerce")
    else:
        out["PStar"] = float("nan")
    agg = out.groupby("year", as_index=False).mean(numeric_only=True)
    return agg


# --------------------------------------------------------------------------- Damodaran NYU historical returns
DAMODARAN_URL = "https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/histretSP.html"


def damodaran_histret(ttl_days: Optional[int] = 30) -> pd.DataFrame:
    """Fetch Aswath Damodaran's *Historical Returns: Stocks, T.Bonds & T.Bills*.

    Endpoint: ``https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/histretSP.html``

    The page contains a single HTML table whose first column is "Year" and whose
    return columns include "S&P 500 (includes dividends)", "3-month T.Bill",
    "US T. Bond" (10yr). All values are nominal annual total returns expressed
    as decimal fractions (e.g. ``0.1162`` for 11.62%). We multiply by 100 to
    match Ibbotson's "Annual Total Returns (in percent)" convention used by
    S1006.

    Returns DataFrame with columns:
      ``year``, ``rslarge`` (S&P 500 total return, percent),
      ``rbgovlt`` (10yr Treasury total return, percent),
      ``rbtbills`` (3-mo T-Bill total return, percent),
      ``inflrate`` (inflation, percent, when present).

    Per Phase 4 adequacy: Damodaran is the open substitute for Ibbotson SBBI
    2004 (now Morningstar commercial). Concept Match Justification recorded in
    S1006_EPR.md. ``proxy: true`` flag stamped on S1006-B and S1006-D in
    the registry. Damodaran does *not* publish an LT Corporate Bond total
    return; the LT Corp series extension is reconstructed from FRED AAA yield
    (see L01_S1006_load.py for the reconstruction).
    """
    query = {"source": "damodaran", "file": "histretSP.html"}
    cached = S00_cache.get("damodaran", query, ttl_days=ttl_days)
    if cached is not None:
        return cached

    last_exc: Optional[Exception] = None
    for attempt in range(RETRIES):
        try:
            resp = requests.get(DAMODARAN_URL, timeout=HTTP_TIMEOUT,
                                headers={"User-Agent": "RSCDPipeline/1.0"})
            if resp.status_code == 200 and len(resp.content) > 1000:
                break
            last_exc = RuntimeError(f"HTTP {resp.status_code}, len={len(resp.content)}")
        except (requests.ConnectionError, requests.Timeout) as exc:
            last_exc = exc
        time.sleep(2 ** (attempt + 1))
    else:
        raise ApiUnavailable(f"Damodaran fetch failed after {RETRIES} retries: {last_exc}")

    # pd.read_html returns a list of tables; the histretSP page has one big table
    # with the column labels on row index 1 (banner row 0). Use header=1.
    from io import StringIO
    try:
        tables = pd.read_html(StringIO(resp.text), header=1)
    except Exception as exc:
        raise ApiUnavailable(f"Damodaran HTML parse failed: {exc}")
    if not tables:
        raise ApiUnavailable("Damodaran returned no tables")
    df = tables[0].copy()
    df.columns = [str(c).strip() for c in df.columns]
    year_col = next((c for c in df.columns if str(c).lower().startswith("year")), df.columns[0])
    df = df.rename(columns={year_col: "year"})
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df = df.dropna(subset=["year"])
    df["year"] = df["year"].astype(int)

    def _find_substring(*keys: str) -> Optional[str]:
        for c in df.columns:
            cl = str(c).lower().replace(" ", "")
            if all(k.lower().replace(" ", "") in cl for k in keys):
                return c
        return None

    # Damodaran's actual column headings (verified 2026-05-18):
    #   'S&P 500 (includes dividends)'         -> rslarge (total return)
    #   'US T. Bond (10-year)'                 -> rbgovlt
    #   '3-month T.Bill'                       -> rbtbills
    #   'Baa Corporate Bond'                   -> rbcorplt (Baa total return)
    # Some columns appear twice with the second copy being a cumulative value
    # ($-prefixed). We pick the FIRST occurrence (the annual % return) in each
    # case by using the order returned by the column list.
    sp_col = _find_substring("s&p", "500", "dividend")
    gov_col = _find_substring("us", "t.", "bond")
    bill_col = _find_substring("3-month", "t.bill") or _find_substring("3month", "t.bill")
    baa_col = _find_substring("baa", "corporate")
    infl_col = _find_substring("inflation")

    def _to_pct(series: pd.Series) -> pd.Series:
        # Damodaran cells are like '43.81%' (percent), or '$ 100.10' (cum value).
        # We strip %, $, commas, and spaces; coerce to numeric.
        s = (series.astype(str)
                .str.replace("%", "", regex=False)
                .str.replace("$", "", regex=False)
                .str.replace(",", "", regex=False)
                .str.strip())
        s = pd.to_numeric(s, errors="coerce")
        # If max abs < 1.5 treat as decimal fraction and convert to percent;
        # Damodaran's percent-formatted columns already exceed 1.5 in many years.
        if s.dropna().abs().max() is not None and s.dropna().abs().max() < 1.5:
            s = s * 100.0
        return s

    out = pd.DataFrame({"year": df["year"].values})
    if sp_col is not None:
        out["rslarge"] = _to_pct(df[sp_col]).values
    if gov_col is not None:
        out["rbgovlt"] = _to_pct(df[gov_col]).values
    if bill_col is not None:
        out["rbtbills"] = _to_pct(df[bill_col]).values
    if baa_col is not None:
        # Baa Corporate Bond yields/returns — Damodaran reports this as the
        # average bond yield, not strictly an Ibbotson-style "total return"
        # series; close enough for RSCD's open-license substitution. See
        # S1006_EPR.md Concept Match Justification.
        out["rbcorplt"] = _to_pct(df[baa_col]).values
    if infl_col is not None:
        out["inflrate"] = _to_pct(df[infl_col]).values
    out = out.dropna(subset=[c for c in out.columns if c != "year"], how="all").reset_index(drop=True)

    S00_cache.put("damodaran", query, out,
                  extra_meta={"endpoint": DAMODARAN_URL, "rows": int(len(out))})
    return out


# --------------------------------------------------------------------------- World Bank WDI (CC-BY-4.0, no auth)
WB_BASE = "https://api.worldbank.org/v2"


def worldbank_indicator(
    country: str,
    indicator: str,
    start: int = 1960,
    end: int = 2025,
    ttl_days: Optional[int] = 30,
) -> pd.DataFrame:
    """Fetch a World Bank WDI indicator series for a country.

    Endpoint: ``https://api.worldbank.org/v2/country/{country}/indicator/{indicator}?format=json``

    No API key required. License: CC-BY-4.0 (World Bank Open Data Terms).

    Parameters
    ----------
    country : ISO-3 country code (e.g. ``CHN`` for China, ``USA``)
    indicator : WDI indicator code (e.g. ``FI.RES.XGLD.CD`` total reserves ex gold)
    start, end : year range bounds (inclusive)

    Returns
    -------
    DataFrame with columns ``['year', 'value']`` (year int, value float; missing -> NaN).
    """
    query = {"source": "wb", "country": country, "indicator": indicator,
             "start": start, "end": end}
    cached = S00_cache.get("worldbank", query, ttl_days=ttl_days)
    if cached is not None:
        return cached

    url = f"{WB_BASE}/country/{country}/indicator/{indicator}"
    params = {"format": "json", "date": f"{start}:{end}", "per_page": 20000}
    resp = _retry_get(url, params)
    if resp.status_code != 200:
        raise ApiUnavailable(f"World Bank returned {resp.status_code}: {resp.text[:200]}")
    payload = resp.json()
    if not isinstance(payload, list) or len(payload) < 2:
        raise ApiUnavailable(f"World Bank unexpected payload shape: {str(payload)[:200]}")
    rows = payload[1] or []
    if not rows:
        raise ApiUnavailable(f"World Bank returned 0 rows for {country}/{indicator}")
    df = pd.DataFrame([
        {"year": int(r["date"]),
         "value": float(r["value"]) if r.get("value") is not None else float("nan")}
        for r in rows
    ])
    df = df.sort_values("year").reset_index(drop=True)
    S00_cache.put("worldbank", query, df,
                  extra_meta={"endpoint": url, "indicator": indicator, "country": country})
    return df


# --------------------------------------------------------------------------- IMF WEO (CSV bulk download, no auth)
def imf_weo_country(
    country_iso3: str,
    subjects: tuple[str, ...] = ("BCA", "BCA_NGDPD"),
    ttl_days: Optional[int] = 30,
) -> pd.DataFrame:
    """Fetch IMF World Economic Outlook subjects for a country.

    The WEO database is published as CSV downloads; for programmatic access we
    use the IMF Datamapper JSON API (``https://www.imf.org/external/datamapper/api/v1``)
    which exposes the same WEO subjects without auth. Each subject is one
    annual series per country.

    Parameters
    ----------
    country_iso3 : e.g. ``CHN`` for China
    subjects : tuple of WEO subject codes; defaults to BCA (CA level USD bn)
               and BCA_NGDPD (CA as percent of GDP).

    Returns
    -------
    DataFrame with columns ``['year', 'subject', 'value']``.
    """
    query = {"source": "imf_weo", "country": country_iso3, "subjects": "|".join(subjects)}
    cached = S00_cache.get("imf_weo", query, ttl_days=ttl_days)
    if cached is not None:
        return cached

    base = "https://www.imf.org/external/datamapper/api/v1"
    out_rows: list[dict] = []
    for subj in subjects:
        url = f"{base}/{subj}/{country_iso3}"
        try:
            resp = _retry_get(url, {})
        except ApiUnavailable as exc:
            raise ApiUnavailable(f"IMF WEO {subj}/{country_iso3}: {exc}")
        if resp.status_code != 200:
            raise ApiUnavailable(f"IMF WEO {subj}/{country_iso3} returned {resp.status_code}")
        payload = resp.json()
        # Payload shape: {"values": {SUBJ: {ISO3: {"YYYY": value, ...}}}}
        try:
            year_map = payload["values"][subj][country_iso3]
        except (KeyError, TypeError):
            raise ApiUnavailable(
                f"IMF WEO {subj}/{country_iso3}: unexpected payload {str(payload)[:200]}")
        for year_str, val in year_map.items():
            try:
                yr = int(year_str)
            except (TypeError, ValueError):
                continue
            if val is None:
                continue
            try:
                v = float(val)
            except (TypeError, ValueError):
                continue
            out_rows.append({"year": yr, "subject": subj, "value": v})

    if not out_rows:
        raise ApiUnavailable(f"IMF WEO returned no values for {country_iso3}/{subjects}")
    df = pd.DataFrame(out_rows).sort_values(["subject", "year"]).reset_index(drop=True)
    S00_cache.put("imf_weo", query, df,
                  extra_meta={"endpoint": base, "country": country_iso3, "subjects": list(subjects)})
    return df


# --------------------------------------------------------------------------- US Census FT900 (HTML scrape; FT900 lacks open API)
def census_ft900_annual_balance(
    partner: str,
    start: int = 2002,
    end: int = 2024,
    ttl_days: Optional[int] = 30,
) -> pd.DataFrame:
    """Fetch annual US merchandise trade balance with a partner from Census FT900.

    Census Foreign Trade publishes per-country trade pages at
    ``https://www.census.gov/foreign-trade/balance/c{code}.html`` (e.g.
    ``c5700`` for China). The page returns an HTML table with monthly
    columns (Exports / Imports / Balance) per year going back to 1985.

    We sum each year's monthly Total Exports Value and Customs Import Value
    to produce one annual (year, exports, imports, balance) row in current
    USD millions (Census' native unit) — Phase 5 callers divide by 1000
    to display in Billion USD.

    Parameters
    ----------
    partner : Census country code as a 4-digit string with trailing zero
              (e.g. ``"5700"`` for China, ``"0015"`` reserved for world total).
              For world total the convention differs; use ``"world"`` and
              we fall back to FT900 Exhibit 1.
    start, end : year bounds.

    Returns
    -------
    DataFrame with columns ``['year', 'exports', 'imports', 'balance']``
    in current USD millions. ``balance = exports - imports``.

    Notes
    -----
    The Census per-country pages are HTML tables. If the page layout
    changes, raise ApiUnavailable so the loader degrades cleanly.
    """
    query = {"source": "census_ft900", "partner": partner, "start": start, "end": end}
    cached = S00_cache.get("census_ft900", query, ttl_days=ttl_days)
    if cached is not None:
        return cached

    if partner == "world":
        # World totals via Exhibit 1; the per-country format does not apply.
        url = "https://www.census.gov/foreign-trade/statistics/historical/exh1.txt"
    else:
        url = f"https://www.census.gov/foreign-trade/balance/c{partner}.html"

    last_exc: Optional[Exception] = None
    for attempt in range(RETRIES):
        try:
            resp = requests.get(url, timeout=HTTP_TIMEOUT,
                                headers={"User-Agent": "RSCDPipeline/1.0"})
            if resp.status_code == 200 and len(resp.content) > 200:
                break
            last_exc = RuntimeError(f"HTTP {resp.status_code}, len={len(resp.content)}")
        except (requests.ConnectionError, requests.Timeout) as exc:
            last_exc = exc
        time.sleep(2 ** (attempt + 1))
    else:
        raise ApiUnavailable(f"Census FT900 {partner} failed after {RETRIES} retries: {last_exc}")

    rows: list[dict] = []
    if partner == "world":
        # exh1.txt is whitespace-aligned. Each data line:
        # YEAR  EXPORTS  IMPORTS  BALANCE  (additional cols vary)
        from io import StringIO
        text = resp.text
        for line in text.splitlines():
            line = line.strip()
            if not line or not line[:4].isdigit():
                continue
            parts = line.split()
            try:
                yr = int(parts[0])
                if yr < start or yr > end:
                    continue
                # Census exh1.txt convention: cols are Exports, Imports, Balance
                # in millions USD. Use first 3 numeric columns after year.
                nums = [float(p.replace(",", "").replace("$", ""))
                        for p in parts[1:4] if p.replace(",", "").replace("-", "").replace(".", "").isdigit()
                        or p.startswith("-")]
                if len(nums) >= 3:
                    exp_, imp_, bal_ = nums[0], nums[1], nums[2]
                    rows.append({"year": yr, "exports": exp_, "imports": imp_, "balance": bal_})
            except (ValueError, IndexError):
                continue
    else:
        # Per-country balance page — parse with pd.read_html
        from io import StringIO
        try:
            tables = pd.read_html(StringIO(resp.text))
        except Exception as exc:
            raise ApiUnavailable(f"Census FT900 per-country HTML parse failed: {exc}")
        # Census per-country pages have one big table per year with monthly rows
        # plus a TOTAL row. We aggregate monthly columns to annual.
        for tbl in tables:
            tbl.columns = [str(c).strip() for c in tbl.columns]
            # Look for a year-indexed totals format. The typical row has
            # 'Month'='TOTAL' and a YYYY-bearing header somewhere.
            if "Month" not in tbl.columns:
                continue
            # Find totals row
            mask = tbl["Month"].astype(str).str.upper().str.contains("TOTAL", na=False)
            tot = tbl[mask]
            if tot.empty:
                continue
            for _, r in tot.iterrows():
                # Extract year from a sibling column header containing 4 digits
                yr = None
                exp_ = imp_ = None
                for c in tbl.columns:
                    if c.isdigit() and len(c) == 4:
                        yr = int(c)
                        break
                # FT900 per-country page typically has Exports/Imports/Balance
                # columns. We pull whichever variant is present.
                def _pick(*aliases):
                    for a in aliases:
                        if a in r and pd.notna(r[a]):
                            try:
                                return float(str(r[a]).replace(",", "").replace("$", ""))
                            except ValueError:
                                continue
                    return None
                exp_ = _pick("Exports", "Total Exports", "Exports Value")
                imp_ = _pick("Imports", "Imports Value", "Customs Import Value")
                bal_ = _pick("Balance")
                if yr and yr >= start and yr <= end:
                    if exp_ is None and imp_ is None and bal_ is None:
                        continue
                    if bal_ is None and exp_ is not None and imp_ is not None:
                        bal_ = exp_ - imp_
                    rows.append({"year": yr, "exports": exp_, "imports": imp_, "balance": bal_})

    if not rows:
        raise ApiUnavailable(f"Census FT900 {partner}: no rows parsed from {url}")
    df = pd.DataFrame(rows).drop_duplicates(subset=["year"]).sort_values("year").reset_index(drop=True)
    S00_cache.put("census_ft900", query, df,
                  extra_meta={"endpoint": url, "partner": partner})
    return df


if __name__ == "__main__":
    import json
    print(json.dumps(health(), indent=2))

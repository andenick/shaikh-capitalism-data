# ES2302 — Extension Provenance Record

**Series**: ES2302 — China Current Account Balance
**Phase**: 6 (Extension)
**Construction**: `direct` (two parallel direct pulls, dual units)
**Authored**: 2026-05-18

## 1. Extendability

IMF WEO is published semi-annually (April, October) and includes
historical revisions plus 5-year forecasts. China's BCA and BCA_NGDPD
are continuously reported since 1980. Extension to 2024 is mechanical.

## 2. Method

Loader calls `S00_apis.imf_weo_country(country_iso3='CHN',
subjects=('BCA', 'BCA_NGDPD'))`. Each subject is returned as a separate
long-form row block. No splice, no rebase.

## 3. Proxies

None. WEO IS the source the paper cites.

## 4. Synthetic data

None. NaN propagates.

## 5. Failure modes

- IMF Datamapper API 5xx: retry 3x; if still failing, raise.
- Vintage revision: acceptable, we use the latest vintage.
- Subject code change (BCA -> CAB or similar): would fail loud — do
  not silently substitute.

## 6. Dual-axis emission

The DPR mandates two distinct AnuData rows (level + percent-of-GDP).
Phase 5 enforces this in the loader: each WEO subject is tagged with
its own `subseries_id` (`ES2302-level` or `ES2302-pctgdp`) so the
chopped CSV and extenbook reflect the unit split.

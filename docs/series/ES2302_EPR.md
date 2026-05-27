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

## 6. Conceptual continuity vs adjacent concepts

The extension proxy `IMF WEO subject BCA (level) + BCA_NGDPD (% of GDP)
for country CHN` measures `China's current account balance` rather than
`China's goods trade balance` or `China's BoP balance overall` because:
- Source agency choice: Weber & Shaikh (2020) Fig 2 explicitly cites IMF
  WEO, not China State Administration of Foreign Exchange (SAFE) BoP
  releases. WEO is the published recipe.
- Methodology continuity: paper-window 1997-2017 values were WEO BCA /
  BCA_NGDPD; extension years 2018-2024 use the *same* WEO subjects at
  later vintages (semi-annual April + October publication).
- Disambiguation: current account (BCA) ≠ goods trade balance
  (ES2301 / Census FT900): BCA adds services, primary income, and
  secondary income to the goods balance. % of GDP normalization
  (BCA_NGDPD) differs from level (BCA): the figure plots both on
  a dual y-axis because the units are not commensurable.

The book's original concept (Weber & Shaikh 2020 p. 432, citing Fig 2)
was: China's CA surplus "peaks at about 10% of GDP in 2007, then falls
sharply to about 1.3% by 2017" — the reversal narrative that
counter-evidences the currency-manipulation hypothesis. The modern series
preserves the WEO BCA concept and the dual unit emission (level + %GDP)
while permitting WEO vintage revisions to shift historical values
0.1-0.5 percentage points. This is NOT a proxy substitution forbidden
by the No-Proxy rule because IMF WEO is exactly the source the paper
cites; we pull the same two subjects (BCA, BCA_NGDPD) for the same
country (CHN) at a later vintage.

## 7. Dual-axis emission

The DPR mandates two distinct AnuData rows (level + percent-of-GDP).
Phase 5 enforces this in the loader: each WEO subject is tagged with
its own `subseries_id` (`ES2302-level` or `ES2302-pctgdp`) so the
chopped CSV and extenbook reflect the unit split.

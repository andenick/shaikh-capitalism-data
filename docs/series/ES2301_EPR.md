# ES2301 — Extension Provenance Record

**Series**: ES2301 — US Trade Balance (World, China)
**Phase**: 6 (Extension)
**Construction**: `direct` (two parallel partner pulls)
**Authored**: 2026-05-18

## 1. Extendability

Census FT900 is continuously published monthly. Per-country totals for
China extend back to 1985 and forward to current. Extension to 2024 is
mechanical with the caveat that:

- 2018-2019 Section 301 tariffs introduce a documented structural break
  in import-value composition (tariff-inclusive vs not).
- 2020 COVID compresses bilateral trade flows.

Neither caveat blocks extension — both are documented in the paper-Phase
6 extension narrative.

## 2. Method

For each partner (world, china):
1. Loader pulls Census HTML/text via `census_ft900_annual_balance`.
2. Aggregates monthly columns to annual exports, imports, balance.
3. Converts to Billion USD (divide millions by 1000).
4. Emits as `subseries_id={ES2301-world | ES2301-china}` with
   `country_key={World|China}`.

## 3. Proxies

None. Census FT900 IS the source the paper cites.

## 4. Synthetic data

None. NaN propagates.

## 5. Failure modes

- Census HTML layout change: loader returns degraded; processor
  publishes whichever partner parsed.
- USA Trade Online auth-required path: not used; we stick to the
  public HTML/text pages.

## 6. Census-basis vs BoP-basis

Paper Fig 1 footnote: "Total Exports Value minus Customs Import Value".
This is the Census basis (not BoP basis). We reproduce Census basis to
match paper recipe; BEA International Transactions Table 4.1 BoP-basis
goods balance is concept-adjacent but methodologically distinct.

# XS2301 — Extension Provenance Record

**Series**: XS2301 — US Trade Balance (World, China)
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

For each partner (world=c0004, china=c5700):
1. Loader pulls the Census country balance page via
   `census_country_annual_balance` (rebuilt 2026-06-11; replaces the prior
   fragile `census_ft900_annual_balance` scrape that mis-keyed the year off a
   non-existent column header and silently truncated the series at 2018).
2. Reads the published `TOTAL {YYYY}` annual Balance row directly (Census
   already aggregates the months); no month summing required.
3. Converts to Billion USD (divide millions by 1000).
4. Emits as `subseries_id={XS2301-world | XS2301-china}` with
   `country_key={World|China}`.

Result: genuinely continuous 2002–2024, 23 obs/partner, all live Census data;
V03 validator PASS (4/4 Fig 1 anchors, max 2.17% error).

## 3. Proxies

None. Census FT900 IS the source the paper cites.

## 4. Synthetic data

None. NaN propagates.

## 5. Failure modes

- Census HTML layout change: loader returns degraded; processor
  publishes whichever partner parsed.
- USA Trade Online auth-required path: not used; we stick to the
  public HTML/text pages.

## 6. Conceptual continuity vs adjacent concepts

The extension proxy `Census FT900 Exhibit 1 (world) + c5700 (China)` measures
`US merchandise (goods) trade balance, Census basis` rather than
`US current account` or `BoP-basis goods balance` because:
- Source agency choice: Weber & Shaikh (2020) Fig 1 explicitly cites Census,
  not BEA International Transactions. Census FT900 is the published recipe.
- Methodology continuity: paper-window 2002-2017 values were Census-basis
  monthly aggregates; 2018-2024 extension uses the *same* FT900 release
  (same agency, same exhibit numbers).
- Disambiguation: Census-basis (Total Exports Value − Customs Import Value)
  differs from BoP-basis (BEA ITA Table 4.1, which makes balance-of-payments
  coverage and timing adjustments), and from current-account (which adds
  services, primary income, and secondary income).

The book's original concept (paper p. 432, Fig 1 footnote) was: "Total Exports
Value minus Customs Import Value". The modern series preserves Census-basis
goods coverage and the bilateral US-China decomposition while permitting a
small post-2018 Section-301-tariff valuation effect (customs values now
include tariff-inclusive imports for some HTS lines). This is NOT a proxy
substitution forbidden by the No-Proxy rule because the loader pulls from
*exactly* the source the paper cites (US Census FT900) — no agency
substitution, no concept substitution.

## 7. Method note: Census-basis vs BoP-basis

We reproduce Census basis to match paper recipe; BEA International
Transactions Table 4.1 BoP-basis goods balance is concept-adjacent but
methodologically distinct and is NOT used.

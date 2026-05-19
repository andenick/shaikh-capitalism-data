# NIPA Table 7.11 FISIM Line-Number Remap

**Status:** Phase 5 prerequisite (Blocker B2) — RESOLVED
**Date:** 2026-05-18
**Author:** RSCD A3 (Ch6 GPIM blocker batch)
**Scope:** AS003 imputed-interest adjustment, downstream into S601/S602/S603/S604

## Why this exists

Shaikh's *Capitalism* (2016) Appendix Table 6.7.11 (p. 842) defines the
imputed-interest adjustment used to convert NIPA's bank-as-business
treatment back to the classical accounting concept. The recipe, in
CD2's 2011-vintage NIPA Table 7.11 line numbers, is:

```
BankNetIntPaid     = T7.11(L4 + L44 + L73) - T7.11(L28 + L52 + L91)
NFNetImpIntPaid    = T7.11(L74 + L75)      - T7.11(L53 + L54)
BusImpIntAdj       = -BankNetIntPaid - NFNetImpIntPaid
```

The BEA NIPAs were comprehensively revised in 2013 (FISIM methodology
update) and again in 2018 (Comprehensive Update). The 2013 revision did
not change row order in T7.11 but reclassified the magnitudes; the 2018
update inserted one new monetary-interest row in the financial-corporate
sub-block, shifting all subsequent line numbers by +1. Without a remap,
CD2's 2011 line numbers silently point to the wrong rows in any
post-2018 vintage.

## Resolution approach

We do **not** rewrite the recipe with new hard-coded line numbers (that
would simply move the time-bomb to the next BEA revision). Instead we
map each of the 10 CD2 line numbers to a *stub label* — the row caption
text BEA preserves across vintages — and resolve to live line numbers
at fetch time.

## Stub-label mapping table

| CD2 2011 line | Stub label                                                                            | 2011 line | 2018+ line |
|---------------|---------------------------------------------------------------------------------------|----------:|-----------:|
| 4             | `domestic_business__financial_corporate__monetary_interest_paid`                      |         4 |          4 |
| 44            | `financial_corporate__monetary_interest_paid_by_banks`                                |        44 |         45 |
| 73            | `financial_corporate__imputed_interest_paid_for_borrower_services`                    |        73 |         74 |
| 28            | `domestic_business__financial_corporate__monetary_interest_received`                  |        28 |         29 |
| 52            | `financial_corporate__monetary_interest_received_by_banks`                            |        52 |         53 |
| 91            | `financial_corporate__imputed_interest_received_for_depositor_services`               |        91 |         92 |
| 74            | `nonfinancial_business__imputed_interest_paid_for_borrower_services`                  |        74 |         75 |
| 75            | `nonfinancial_business__imputed_interest_paid_for_other_services`                     |        75 |         76 |
| 53            | `nonfinancial_business__imputed_interest_received_for_depositor_services`             |        53 |         54 |
| 54            | `nonfinancial_business__imputed_interest_received_for_other_services`                 |        54 |         55 |

Vintages 2012-2017 inherit the 2011 line numbers (no structural change
until the 2018 Comprehensive Update introduced the new monetary-interest
row). Vintages 2019-2024 inherit the 2018 line numbers; no structural
change has been published since.

## Citations and provenance

1. **BEA NIPA Handbook** (NIPA Concepts and Methods), Chapter 13
   "Imputations", Section 13.4 "Implicitly priced financial services" —
   defines the FISIM imputations and the T7.11 sectoral redistribution
   that AS003 reverses.
   https://www.bea.gov/resources/methodologies/nipa-handbook
2. **Fixler, D., Reinsdorf, M., and Villones, S. (2010)** "FISIM: A New
   Approach", *Survey of Current Business* 90(5), 31-43. Cited by
   Shaikh (2016, p. 835) as the canonical methodology source for the
   imputations T7.11 carries.
3. **BEA (2013)** "Comprehensive Revision of the National Income and
   Product Accounts: Statistical Changes", *Survey of Current Business*,
   September 2013, pp. 14-45 — documents R&D capitalization, FISIM
   restatement by sector. No structural change to T7.11 row order.
4. **BEA (2018)** "Preview of the 2018 Comprehensive Update of the
   NIPAs", *Survey of Current Business*, April 2018 — announces the new
   "depositor services" sub-row insertion in T7.11 financial-corporate
   monetary-interest block, source of the +1 line shift.
5. **BEA (2024)** "Annual Update of the NIPAs", *Survey of Current
   Business*, September 2024 — no structural change to T7.11; line
   numbers identical to 2018 vintage.
6. **Shaikh, A. (2016)** *Capitalism: Competition, Conflict, Crises*,
   Oxford University Press. Appendix 6.7 Section IV (pp. 835-841) and
   Appendix Table 6.7.11 (p. 842) — the CD2 2011-vintage recipe this
   document preserves.

## Implementation

The resolver is implemented in
`Technical/code/L01_loaders/_nipa_t711_line_resolver.py`. The public API:

```python
resolve_t711_line(historical_line_num: int, vintage_year: int) -> str
stub_label_to_current_line(stub_label: str, current_vintage: int) -> int | None
compute_AS003_recipe(t711_values: dict[str, float],
                     current_vintage: int | None = None) -> dict
fetch_t711_via_api(year: int, vintage_year: int | None = None) -> dict
```

The `fetch_t711_via_api` helper uses BEA's `LineDescription` field
(returned in every BEA Data API row) rather than `LineNumber`, so it is
robust against future revisions even without updating the pinned vintage
table. The pinned table exists for offline / cached-CSV fetches and as
the source of truth for diagnostics.

## How to update when BEA publishes a new revision

1. Download the new T7.11 release (PDF or Data API).
2. For each of the 10 stub labels above, look up the new line number.
3. Add a new vintage entry to `_T711_LINE_INDEX` in the resolver module.
   Do **not** edit existing pinned vintages.
4. Run `python Technical/code/L01_loaders/_nipa_t711_line_resolver.py`
   and confirm the round-trip prints expected mappings.
5. Add a row to the stub-label table above with the new vintage column.
6. Document the BEA release notes citation here.

## Validation

The resolver self-test (`python …/_nipa_t711_line_resolver.py`)
round-trips all 10 CD2 lines through both pinned vintages and reports
expected 2024 line shifts (+1 for all lines >= 28). Verified 2026-05-18.

## Caveats

- The 2018 +1 shift is documented in BEA release notes but the precise
  inserted row (monetary interest paid by foreign-bank branches vs.
  primary-dealer category) is not material for the AS003 recipe — what
  matters is that the *captioned* rows preserve their economic content.
- If a future BEA revision splits or merges any of the 10 captioned
  rows, the resolver will raise on lookup and the methodology table
  above must be re-derived. The Phase 5 loader should surface such
  failures as `data_unavailable` rather than silently absorbing them.

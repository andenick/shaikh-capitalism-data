# BEA 1993 Fixed Asset Methodology — Depreciation and Retirement Rates

**Status:** Phase 5 prerequisite (Blocker B3) — RESOLVED
**Date staged:** 2026-05-18
**Staged by:** RSCD A3 (Ch6 GPIM blocker batch)
**Consumers:** AS004, AS006 (a and b sub-variants), AS007

## Purpose

The BEA's pre-1997 Fixed Asset methodology assumed each capital good had
a particular finite useful life, with retirement following a fixed
distribution around mean service life. After 1997 BEA switched to
geometric depreciation with infinite tails (no scrapping). Shaikh argues
the finite-life methodology is empirically superior and uses it to
construct his GPIM (Generalized Perpetual Inventory Method) variants
AS004 / AS006 / AS007.

These depreciation and retirement rates are no longer published in BEA's
current iTable. This directory stages the recovered rates as a frozen
historical input for the Phase 5 loaders.

## Files

- `BEA_1993_depreciation_retirement_rates.csv` — long-form table, one
  row per variable, columns 1925-2011.
- `BEA_1993_depreciation_retirement_rates.json` — same data as JSON with
  provenance sidecar (source MD5, year range, extraction date).

## Variable inventory

The following 14 series are staged (Shaikh's Appendix Table 6.8.II.3
field names; book pp. 845-851):

| Variable          | Description                                                | Units / Range            |
|-------------------|------------------------------------------------------------|--------------------------|
| `KNCbea93`        | BEA 1993 Current-Cost Net Stock, corporate                 | Bill-$, 1925-1989        |
| `KNRbea93`        | BEA 1993 Constant-Cost Net Stock                           | Bill-1987-$, 1925-1989   |
| `pKNbea93`        | BEA 1993 Implicit Price Deflator, Net Stock                | 1985=100, 1925-1989      |
| `DEPcorpbea93`    | BEA 1993 Current-Cost Corporate Depreciation               | Bill-$, 1925-1989        |
| `dcorpnew`        | **BEA 1993-derived Depreciation Rate (Net Stock)**         | Decimal, 1926-2011       |
| `pKN`             | BEA 2011 Chain Index Net Stock Deflator                    | 2005=100, 1925-2011      |
| `IGCcorp`         | BEA 2011 Current-Cost Gross Investment                     | Bill-$, 1925-2011        |
| `KNCcorpnew`      | New Net Current-Cost Corp Stock (GPIM applied to 1993 rates)| Bill-$, 1925-2011       |
| `KGCBEA93`        | BEA 1993 Current-Cost Gross Stock                          | Bill-$, 1925-1989        |
| `KGRBEA93`        | BEA 1993 Constant-Cost Gross Stock                         | Bill-1987-$, 1925-1989   |
| `pKGbea93`        | BEA 1993 Implicit Price Deflator, Gross Stock              | 1985=100, 1925-1989      |
| `RETcorpBEA93`    | BEA 1993 Current-Cost Corporate Retirements (Discards)     | Bill-$, 1925-1989        |
| `rho_corpnew`     | **BEA 1993-derived Retirement Rate (Gross Stock)**         | Decimal, 1926-2011       |
| `KGCcorpnew`      | New Gross Current-Cost Corp Stock (GPIM applied)           | Bill-$, 1925-2011        |

The **two key rates** used by AS004/AS006/AS007 GPIM construction are
`dcorpnew` (net stock depreciation rate) and `rho_corpnew` (gross stock
retirement rate). These are derived from BEA 1993 raw flows for 1925-1989
and then linearly projected to 2011 (Shaikh's procedure, see Appendix
Table 6.8.II.3 note).

## Provenance

| Layer | Source                                                                       |
|-------|------------------------------------------------------------------------------|
| Layer 1 (primary)   | Shaikh's posted spreadsheet `Appendix6_Table68II3.xlsx` (file MD5 `9cdbdf5628837e07856b92925c89599a`) shipped with *Capitalism* (2016) online appendix. Location in this repo: `SalvagedInputs/book_data/ShaikhChoppedTables/Appendix6_Table68II3.xlsx`. |
| Layer 2 (upstream)  | The 1925-1989 columns derive from BEA (1993) *Fixed Reproducible Tangible Wealth in the United States, 1925-89*, Tables A.12 (constant-cost) and A.13 (current-cost), as cited in the sheet's `Source` column for every raw input row. |
| Layer 3 (rate derivation) | The depreciation rate `dcorpnew = DEPcorp * 100 / (pKN * KNR(-1))` and retirement rate `rho_corpnew` (analogous gross-stock formula) are computed inside the spreadsheet using equations (6.5.6) and the GPIM machinery of Shaikh Chapter 6. |
| Layer 4 (1990-2011) | For years past the BEA 1993 publication window, Shaikh linearly projects the rates and applies them to BEA 2011 gross investment (per Appendix Table 6.8.II.3 sheet header note). |

## Recovery path taken

The agent's resolution sequence:
1. **Tried first:** Direct check of `SalvagedInputs/book_data/ShaikhChoppedTables/Appendix6_Table68II*.xlsx`.
2. **Found:** All seven Appendix 6.8.II tables present; `Appendix6_Table68II3.xlsx` is the canonical source for BEA 1993 depreciation and retirement rates.
3. **Skipped:** Wayback Machine fetch of BEA 1993 SCB and reconstruction
   from NBER/HathiTrust were not necessary — Shaikh's spreadsheet
   already contains the derived rates with full upstream-citation
   provenance back to BEA 1993 Tables A.12/A.13.

## Validation checks

- 1925 `KNCbea93` = 77.769 — matches the BEA 1993 initial-value figure
  77.7 cited in Shaikh (2016, p. 845, Appendix Table 6.7.13). Confirms
  the spreadsheet is not corrupted.
- 1989 `dcorpnew` = 0.09281 (~9.28%); 2011 projected = 0.09814 (~9.81%).
  Consistent with Shaikh's Figure 6.7.5 narrative ("the earlier
  depreciation rate is higher than the present one", book p. 846).
- 1989 `rho_corpnew` = 0.03691 (~3.69%); 2011 projected = 0.03711
  (~3.71%). Lower than depreciation, as stated by Shaikh ("the earlier
  BEA retirement rate is far lower than either of these").
- Year coverage: 87 annual observations 1925-2011 inclusive.

## Downstream consumption

- **AS004** (GPIM Corporate Capital Stock — operational baseline):
  reads `dcorpnew` and `rho_corpnew` for the depletion-rate input
  `z_t = d_t + rho_t` in GPIM accumulation equations (6.5.22) and (6.5.23).
- **AS006a** (BEA 1993 depreciation only, BEA 2011 initial value):
  reads `dcorpnew` and `rho_corpnew`; initial KC held at 98.1 (AS004 value).
- **AS006b** (BEA 1993 depreciation AND initial value): reads
  `dcorpnew`, `rho_corpnew`, and `KNCbea93[1925] = 77.769`.
- **AS007** (IRS-adjusted): uses interwar-period IRS index multiplier;
  reads BEA 1993 rates indirectly via AS004 baseline.

Loaders MUST cite this file as the input and pin the source-file MD5
hash in their provenance metadata.

## Caveats

- The 1990-2011 portion of `dcorpnew` and `rho_corpnew` is a *linear
  projection* by Shaikh, not raw BEA data. For extension years 2012+,
  the Phase 5 loader should either (a) continue the linear projection
  with documented uncertainty band, or (b) freeze the 2011 value with
  a `data_unavailable_after: 2011` flag. Recommendation: (b) for AS004
  baseline; (a) for AS006/AS007 sensitivity variants only, with
  explicit caveat in plot legend.
- Variable `rho_corpnew` is written as `ρ corpnew` in the source
  spreadsheet (Greek rho character). The staged CSV uses ASCII
  `rho_corpnew` to avoid Windows codepage issues.
- The BEA 1993 publication used 1987 as the constant-cost reference
  year. Modern BEA uses chained dollars indexed to 2017. Loaders that
  combine BEA 1993 stock levels with modern BEA flows must convert
  using `pKN` (chain price index, 2005=100) as the linking deflator,
  exactly as Shaikh does in the spreadsheet.

# Chapter 17 Research Summary — Summary and Conclusions

**Wave**: C
**Subagent**: opus-subagent-wave-c-ch13-17
**Date**: 2026-05-18
**Series count**: 3 (S1701, S1702, S1703)
**Book pages**: 747–759 (chapter body — figures on pp. 749, 752, 753), 900 (Appendix 17.1)

## Chapter focus

Chapter 17 is Shaikh's book-length recapitulation. It contains only three figures, two of which (Fig 17.2 and Fig 17.3) introduce the **only genuinely new empirical analysis** of the chapter: a snapshot of the 2011 US personal income distribution decomposed into an exponential bulk (bottom 97%) and a Pareto tail (top 3%), drawn from the econophysics two-class (EPTC) literature of Yakovenko and co-authors. Figure 17.1 is a **reuse** of the chapter 5 / chapter 16 long-wave construction (HP-smoothed US/UK wholesale price indexes expressed in ounces of gold), supplemented by a forward-projection overlay.

## Series-level notes

### S1701 — Fig 17.1: The Global Crisis of 2007 in Light of Past Long Waves

**Time series**. Stub inherited the CD2 name "IRS 2011 Income Distribution — Full Table" from `cd2_id: S102`, but the assigned figure (`Fig17.1`) is the long-wave chart, not the IRS table. This dossier **honours the figure assignment** (Fig 17.1 = long waves) and renames the series accordingly; Phase 4 should ratify or, alternatively, reassign the figure list to `["Fig17.2","Fig17.3"]` and rebuild S1701 as the IRS full table (in which case S1701 would become a near-duplicate of the S1702+S1703 source data).

Source path (per Appendix 17.1, p. 900): *"The HP-smoothed data on US and UK price indexes expressed in ounces of gold is from the spreadsheet in Appendix 5.3 Data Tables for Chapter 5."* HP filter parameter explicitly stated as **lambda = 100**. Chart annotates two completed long waves: 1897–1939 (42 years) and 1939–1983 (44 years), trough-to-trough. The dashed "average of past two waves" overlay was used by Shaikh to project the 2008–2018 crisis interval. Construction is `composite` (US WPI in gold + UK WPI in gold + derived two-wave average overlay).

Three extension candidates flagged: **MeasuringWorth** (Officer) for US WPI, **Bank of England 'A Millennium of Macroeconomic Data'** for UK WPI, and **MeasuringWorth Price of Gold** for the gold-deflation step. All three must be recomposed (not growth-rate spliced) because the published series is itself a derived/filtered quantity.

### S1702 — Fig 17.2: Personal Income Distribution below $200,000 (exponential / EPTC bottom 97%)

**Cross-sectional snapshot (2011 only)**. Source confirmed as **IRS SOI Publication 1304, Table 1.4 — All Returns by Size of AGI, Tax Year 2011**, URL `https://www.irs.gov/statistics/soi-tax-stats-individual-income-tax-returns-publication-1304-complete-report`. Construction (per Appendix 17.1, p. 900):

1. Take IRS-published number-of-returns per pre-defined AGI bin.
2. Centre each bin at its midpoint.
3. Convert number-of-returns to relative frequency.
4. Cumulate to get CDF-from-below.
5. Compute survival = 1 − CDF-from-below.
6. Filter to bins with midpoint < $200,000 (bottom 97% of returns).
7. Plot ln(survival) vs midpoint on log-linear axes.

The dashed reference line is the theoretical exponential survival Φ(y) = exp(−y/ȳ) with ȳ estimated by regressing ln(Φ(y)) on y (footnote 3, p. 752). Shaikh reports a measured Gini of **0.492** for this distribution (p. 753), consistent with the exponential's theoretical Gini = 0.50.

No extension candidates (cross_sectional — Anu Framework forbids extension of non-time-series). Construction is `composite`. **Open issue**: CD2 reference values appear to mix the frequency column with the survival column — Phase 5 must reconcile against the Appendix 17.2 spreadsheet before replication.

### S1703 — Fig 17.3: Personal Income Distribution above $200,000 (Pareto / EPTC top 3%)

**Cross-sectional snapshot (2011 only)**. Same primary source as S1702 (IRS SOI 2011 Table 1.4), same construction pipeline, but filtered to AGI bins ≥ $200,000 and plotted on **log-log** axes so that a Pareto survival P(Y > y) ∝ y^(−α) renders as a straight line of slope −α. Shaikh does not publish the fitted α; visual inspection suggests α ≈ 1.5–2.0, consistent with Yakovenko-Barkley-Rosser (2009) US tail estimates.

The midpoints for the open-ended top IRS bins ($1M+, $5M+, $10M+) materially affect the fitted Pareto exponent; Appendix 17.2 supplies the canonical choices (750,000; 1,750,000; 3,500,000; 7,500,000 per CD2 validation reference).

No extension candidates (cross_sectional). Construction is `composite`.

## Cross-series dependencies

| Component | Used by |
|---|---|
| Appendix 5.3 spreadsheet (chapter 5 WPI-in-gold) | S1701 (and originally Fig 16.1, i.e. S1601) |
| IRS SOI 2011 Publication 1304 Table 1.4 | S1702, S1703 |
| Appendix 17.2 bin midpoints | S1702, S1703 |
| EPTC framework (Yakovenko et al.) | S1702 (exponential ref. line), S1703 (Pareto ref. line) |

## Chapter-level issues / open questions

1. **Stub naming inconsistency for S1701**: CD2 S102 is the IRS full table (figures 17.2/17.3), but the RSCD stub for S1701 assigns figure Fig17.1 (the long-wave chart). Dossier renames S1701 to match the figure assignment; Phase 4 to ratify or to remap.
2. **CD2 reference-value column ambiguity** (S1702/S103): the listed reference values look like the frequency column FPR017_C3 rather than the survival column FPR017_C5 — needs reconciliation before Phase 5.
3. **Open-bin midpoints** (S1703): the choice of midpoint for the top IRS open-ended bins is the largest replication risk; honour Appendix 17.2 spreadsheet values.
4. **Pareto exponent α not published** (S1703): must be recovered numerically in Phase 5.
5. **Forecast portion of Fig 17.1**: the "average of past two waves" dashed line is projected to 2018/2030 — Phase 4 should decide whether to retain in the replication CSV or split into a separate forecast series.

## Validator-relevant fields

| SID | quotes | source_identified | extension_candidates | construction |
|---|---|---|---|---|
| S1701 | 3 | yes (Shaikh App 5.3 / anwarshaikhecon.org) | 3 | composite |
| S1702 | 4 | yes (IRS SOI 2011 Pub 1304 T1.4) | 0 (cross_sectional) | composite |
| S1703 | 4 | yes (IRS SOI 2011 Pub 1304 T1.4) | 0 (cross_sectional) | composite |

Expected validator outcome: **PASS** for all three series.

---

## Phase 5-8 Closure (2026-05-18)

**Author**: opus-subagent-wave2-ch11-13-17

| SID | Content type | V03 status | MAE | Chopped rows | Notes |
|-----|--------------|------------|-----|--------------|-------|
| S1701 | time_series | PASS | 0.0 | 469 | Renamed from CD2 S102 (IRS) to long-wave chart per Phase 4 |
| S1702 | cross_sectional | PASS | 0.0 | 17 | Column-fix FPR017_C5; spot-check 1000->0.95536 etc. confirmed |
| S1703 | cross_sectional | PASS | 0.0 | 6 | Column-fix FPR017_C5; $10M+ bin DROPPED (anti-synthetic) |

**Key Phase 4 corrections applied in code**

- **S1701 rename ratified**: registry `name` set to "The Global Crisis of 2007 in Light of Past Long Waves (HP-smoothed US/UK gold-deflated price indexes)". CD2 S102 IRS lineage is captured separately in S1702/S1703. `name_history` block in registry records the rename.
- **S1701 forecast layer**: USUKAVGWAVE post-2011 rows carry `is_forecast: True` flag in the processed parquet (Phase 4 recommendation: keep in-CSV flag instead of new registry row).
- **S1702 column fix**: loader reads `Cumulative Frequency from Above` (FPR017_C5), NOT `Frequency` (FPR017_C3) as CD2 markdown had used. V03 spot-checks the Phase-4 fixtures: midpoint 1000 → 0.95536, 22500 → 0.58350, 62500 → 0.21588, 150000 → 0.03233 — all match.
- **S1703 column fix + bin drop**: same column-F correction. Spot-checks: 350000 → 0.00618, 750000 → 0.00207, 1250000 → 0.001142, 1750000 → 0.000757, 3500009 → 0.000211, 7500000 → 0.0000787 — all match. `$10,000,000 or more` bin (no midpoint) DROPPED per anti-synthetic rule.
- **S1703 Pareto recovery**: loader and processor compute the Pareto exponent by OLS in log-log space; recorded in run summary.

**Artifacts**

- DPR + EPR per series (6 markdown files)
- L01 + P02 + V03 per series (9 Python files)
- Chopped CSVs and extenbooks for all 3 series
- Registry updates via `_phase5_ch11_13_17_register.py`

**Open items for Phase 9**

1. S1701 post-2007 WPI extension via NBER macrohistory m04051a + BLS WPU00000000 bridge.
2. S1701 forecast-portion treatment confirmation with user.
3. S1703 Pareto alpha published value (Phase 5 produces numerical estimate; Shaikh did not publish).

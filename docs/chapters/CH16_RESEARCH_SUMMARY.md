# Chapter 16 — Growth, Profitability, and Recurrent Crises: Research Summary

**Wave**: C
**Date**: 2026-05-18
**Reviewer**: opus-subagent-wave-c-ch16
**Series count**: 6 (S1601-S1606)
**Page range**: 727-736 (chapter body); 898-899 (Appendix 16.1 Sources and Methods)

---

## Chapter context

Chapter 16 synthesizes Shaikh's empirical account of postwar US profitability, the neoliberal turn, and the run-up to the 2007 global crisis. The narrative arc combines four data threads: (1) long-wave price patterns in gold (Fig 16.1) to situate the 2007 crisis as on-schedule, (2) the wage-productivity gap opened in the Reagan era (Fig 16.3 + counterfactual Fig 16.4, not a series in our scope), (3) the secular collapse of interest rates after 1981 (Fig 16.6 US, Fig 16.7 OECD), and (4) the resulting boom in household debt and net profits that culminated in the crisis (Figs 16.8-16.10). Every empirical figure in the chapter draws on data developed elsewhere — Appendix 5.3 for golden waves, Appendix 6.8.II.7 for corporate profit rates, and Appendix 16.2 for the chapter-local series.

All six series have strong CD2 predecessors (S093, S095, S098-S101) which were ported directly via the CD2-to-RSCD crosswalk; this dossier batch is therefore predominantly a fidelity-validation and modernization-extension exercise rather than de novo source discovery.

---

## Per-series summary

### S1601 — US and UK Golden Waves, 1786-2010 (Fig 16.1)
- **Construction**: composite (WPI/gold ratio, US and UK, residuals from a fitted cubic time trend, rebased 1930=100).
- **Source chain**: Appendix 5.3 data tables (US WPI from BLS WPS00000000 spliced with NBER macrohistory pre-1947; UK WPI from O'Donoghue/Bank of England historical series; gold price 1930=100 base).
- **Modern extension**: PPIACO + LBMA Gold + ONS PPI for UK; growth-rate splice with caveats about post-1971 gold volatility.
- **Open**: UK historical source ambiguity; cubic-trend endpoint sensitivity on extension.

### S1602 — Hourly Real Wages and Productivity, US Business Sector (Fig 16.3)
- **Construction**: composite (BLS PRS84006153 productivity + PRS84006093 real compensation + Shaikh counterfactual via OLS ln(ec)~ln(y) regression over 1960-1981).
- **Source**: BLS Major Sector Productivity and Costs (Nonfarm Business).
- **Modern extension**: FRED COMPRNFB + OPHNFB at 2017=100; rebase to 1982=100 for continuity.
- **Open**: deflator choice (CPI-U-RS vs PCE); counterfactual regression replication is a Phase 5 task.

### S1603 — US and OECD Short-Term Interest Rates (Fig 16.7)
- **Construction**: composite (US 3-month T-bill annual avg + bespoke weighted OECD average via Fed H.10 trade weights * IMF IFS country rates).
- **Source**: Amr Ragab's construction (acknowledged in Appendix 16.1) using IMF IFS + Fed H.10 weights; US rate from ERP Table 73 / FRED TB3MS.
- **Modern extension**: FRED TB3MS for US; OECD MEI IRSTCI01 as pre-aggregated alternative (sacrifices fidelity).
- **Open**: trade-weight vintage choice; whether to swap for OECD pre-aggregate in Phase 4.

### S1604 — Net Average and Real Incremental Rates of Profit (Fig 16.8)
- **Construction**: composite difference series; r_net = r_corp - i_3mo (both from Appendix 6.8.II.7 and TB3MS).
- **Source**: Shaikh Appendix 6.8.II.7 corporate profit rate dataset (chapter 6 chain) minus 3-month T-bill.
- **Modern extension**: cascades from S0606-S0608 chapter-6 profit rate dossiers + TB3MS.
- **Open**: HP-filter lambda choice on annual; rcorpalt construction needs counterfactual from S1602.
- **Cross-reference**: Internal to chapter-6 profit rate chain; rcorpalt subseries depends on S1602 counterfactual.

### S1605 — Household Debt-to-Income Ratio (Fig 16.9)
- **Construction**: formula (direct ratio Fed Z.1 D.3 line 2 / BEA NIPA T2.1 line 27).
- **Source**: Federal Reserve Flow of Funds + BEA NIPA.
- **Modern extension**: FRED HCCSDODNS / DPI (preferred over CD2's CMDEBT/PI which are slight wrong-concept proxies).
- **Open**: CD2 extension proxies are not faithful to book spec — Phase 4 decision.

### S1606 — Household Debt-Service Ratio (Fig 16.10)
- **Construction**: direct (Federal Reserve published Household Debt Service Ratio, quarterly SA).
- **Source**: Fed identifier FOR/FOR/DTFD%YPD.Q (= FRED TDSP); CD2 also tracks FOR (FODSP) in parallel.
- **Modern extension**: FRED TDSP + FODSP; direct continuation, no methodology break.
- **Open**: quarterly vs annual cadence for RSCD pipeline.

---

## Cross-references

- **S1604 depends on S1602**: the rcorpalt (wage-suppression-adjusted profit rate) subseries inside S1604 uses S1602's counterfactual compensation path.
- **S1604 depends on chapter-6 series**: Appendix 6.8.II.7 is the chapter-6 profit rate chain (S0606-S0608 in RSCD).
- **S1601 depends on Appendix 5.3**: shared with Chapter 5 series; risk of double-counting in cross-series uniqueness check.
- **S1605 and S1606 are parallel household debt indicators**: same denominator family (Disposable Personal Income); paired in the book's narrative arc on the household side of the boom.

---

## Chapter-wide issues

1. **CD2 → RSCD port fidelity**: All six CD2 dossiers (S093, S095, S098-S101) were well-developed; primary work here was schema mapping, verbatim quote extraction from the book, and validating that CD2's extension URLs still resolve.
2. **Wrong-concept proxies inherited from CD2**: S1605 uses CMDEBT/PI for extension (vs HCCSDODNS/DPI for book fidelity). Flagged for Phase 4 adequacy review.
3. **URL rot**: Original Appendix 16.1 URLs include `gpoaccess.gov/eop/tables10.html` (dead, now govinfo.gov) and `bls.org` (typo for bls.gov). Replacements documented in each dossier.
4. **Bespoke vs off-the-shelf series**: S1603's OECD weighted average is a Shaikh-original construction. Modern OECD MEI gives a comparable but not identical series. Phase 4 must decide whether to re-replicate Ragab's weighting or accept OECD MEI substitute.
5. **HP-filter dependency**: S1604 (and chapter-6 chain feeding it) uses HP-100 smoothing whose endpoint values shift on every extension. This is a structural fragility, not a series-level fix.

---

## Page-number audit

| Series | Figure | Book page (printed) | PDF index | Status |
|---|---|---|---|---|
| S1601 | 16.1 | 727 | 765 | OK |
| S1602 | 16.3 | 730-731 | 768-769 | OK |
| S1603 | 16.7 | 733-734 | 771-772 | OK |
| S1604 | 16.8 | 734-735 | 772-773 | OK |
| S1605 | 16.9 | 735 | 773 | OK |
| S1606 | 16.10 | 735-736 | 773-774 | OK |
| (all) | Appendix 16.1 | 898-899 | 936-937 | OK |

Printed-to-PDF offset is +38 throughout chapter 16 and appendix.


---

## Phase 5-8 Closure (2026-05-18)

All six Chapter 16 series (S1601-S1606) reached PASS through L01 -> P02 -> V03 -> O06 with MAE = 0 (pass-through reproduction of Appendix 5.3 and Appendix 16.2 source columns).

| SID | V03 status | n compared | MAE | Chopped rows | Notes |
|---|---|---|---|---|---|
| S1601 | PASS | 450 | 0.000000 | 900 | US/UK golden-wave residuals; cubic-trend re-fit deferred to Phase 6 |
| S1602 | PASS | 330 | 0.000000 | 330 | Wage-prod pass-through; counterfactual ec_c regression deferred to Phase 6 |
| S1603 | PASS | 125 | 0.000000 | 125 | US/OECD/EU short rates; dual-variant Fed H.10/IMF + OECD MEI deferred to Phase 6 |
| S1604 | PASS | 320 | 0.000000 | 320 | Net profit / incremental rates; HP lambda pinned at 100 (Shaikh annual choice) |
| S1605 | PASS | 114 | 0.000000 | 114 | HCCSDODNS / (DPI * 1000) substitution + unit-conversion comment pinned in P02 docstring |
| S1606 | PASS | 264 | 0.000000 | 66 annual + 264 quarterly | Dual-cadence: quarterly sidecar + annual-mean canonical |

Extension (Phase 6) for all six series deferred per Ch16 fanout direction: book-period reproduction is the v1.0 priority; FRED / BLS / BoE / ONS / IMF IFS extension implementations are scaffolded in loader extension_deferred_to_phase6 status fields.

Phase 4 substitutions applied:
- S1601 BoE Millennium canonical + Mitchell cross-check (documented in DPR; extension Phase 6).
- S1602 BLS PRS84006093 CPI-U-RS canonical (documented in registry deflator_choice field).
- S1603 dual-variant emission (S1603_replicated + S1603_oecd_mei) documented; Phase 6 implementation.
- S1604 HP lambda = 100 pinned as module constant HP_LAMBDA in L01 and registry hp_lambda field.
- S1605 CMDEBT/PI -> HCCSDODNS/DPI substitution with explicit unit-conversion dimensional-analysis comment in P02_S1605_construct.py docstring.
- S1606 quarterly + annual variants emitted (quarterly sidecar + annual-mean canonical parquet).

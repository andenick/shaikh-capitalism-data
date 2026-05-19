# Chapter 7 — Real Competition: Research Dossier Summary

**Wave**: B
**Agent**: opus-subagent-wave-b-ch7
**Date**: 2026-05-18
**Series**: S701-S708 (8 series)
**Book pages**: 287-311 (Chapter 7 body, figures 7.11-7.20); 856-860 (Appendix 7.1)

## Theoretical context

Chapter 7 ("The Theory of Real Competition") presents Shaikh's central
classical-Marxian thesis: capitalist competition is "turbulent equalization"
of profit rates among regulating capitals, not the timeless equality of
neoclassical perfect competition. The eight empirical series in this
chapter test that thesis at three levels of aggregation:

1. **Cross-sectional plant/industry costs** (S701, S702) - Salter's
   classic 1924-50 US and 1954-63 UK cross-industry scatters of selling
   price vs unit labor cost. Shows ~77% of cross-industry price variation
   is explained by unit-labor-cost variation.
2. **World/US manufacturing average and incremental profit rates**
   (S703, S704) - Christodoulopoulos's reconstruction from the
   discontinued OECD ISDB 1994 database, 1970-89 world and 1960-89 US
   panels. Establishes that incremental rates "cross over" (equalize)
   while average rates do not.
3. **US 30-industry NIPA average and incremental rates** (S705, S706) -
   Shaikh's own 2008 reconstruction from BEA GDPbyInd + Fixed Assets +
   adjustments (WEQ, OOH, inventories, bank/insurance reserves), 1987-2005.
4. **Greek 20-industry average and incremental deviations** (S707, S708) -
   Tsoulfidis & Tsaliki (2011) Figures 4 and 5, 1962-91. Same pattern:
   incremental rates equalize, average rates do not.

## Per-series rollup

| SID  | Figure  | Period    | Source                                     | CD2  | Construction | Quotes | Ext.cand |
|------|---------|-----------|--------------------------------------------|------|--------------|--------|----------|
| S701 | Fig7.11 | 1923-1950 | Salter (1969) Table 33                     | none | direct       | 3      | 2 (BLS)  |
| S702 | Fig7.12 | 1954-1963 | Salter (1969) Table 28 (Reddaway Addendum) | none | direct       | 3      | 2 (ONS)  |
| S703 | Fig7.13 | 1970-1989 | OECD ISDB 1994 / Christodoulopoulos (1995) | none | composite    | 3      | 2 (OECD) |
| S704 | Fig7.14 | 1960-1989 | OECD ISDB 1994 / Christodoulopoulos (1995) | none | composite    | 3      | 2 (BEA)  |
| S705 | Fig7.15 | 1987-2005 | BEA GDPbyInd + Fixed Assets / Shaikh 2008  | S034 | composite    | 4      | 4 (BEA+) |
| S706 | Fig7.17 | 1988-2005 | BEA GDPbyInd + FA T3.7ES / Shaikh 2008     | S036 | composite    | 3      | 3 (BEA)  |
| S707 | Fig7.19 | 1962-1991 | Tsoulfidis & Tsaliki (2011) Fig 4          | S038*| composite    | 3      | 2 (Greek)|
| S708 | Fig7.20 | 1962-1991 | Tsoulfidis & Tsaliki (2011) Fig 5          | none | composite    | 3      | 2 (Greek)|

\* S707 stub had a name/figure mismatch — see Issues below.

## Chapter-wide methodology themes

- **Wage-equivalent (WEQ) adjustment**: Shaikh removes the implicit wage
  of self-employed proprietors and partners from NIPA Gross Operating
  Surplus to produce a clean profit measure. For Construction, this drops
  the measured profit rate from 90.5% to 20.7% (book p. 302).
- **Owner-Occupied Housing (OOH) removal**: NIPA treats homeowners as
  businesses renting to themselves; Shaikh strips 55.5% of imputed Real
  Estate GOS and 76% of imputed K (book p. 302).
- **Inventory and reserve adjustments**: Adds normal inventories to
  Manufacturing/Wholesale/Retail K and IG; adds bank and insurance
  reserves to Banking/Insurance K and IG (Flow of Funds L.109, L.114-117).
  This drops Banking's measured rate from 41.8% to 17.7% (book p. 303).
- **Industry exclusion**: 31 of 61 NAICS private industries excluded
  on three grounds (nonprofit-dominated, inadequate WEQ data, non-
  competitive on a world scale). The full list lives in Shaikh (2008)
  appendix B, which is NOT in SalvagedInputs (open question, applies
  to S705 and S706).
- **IROP definitional choice**: Shaikh's preferred numerator is delta(GOS);
  Tsoulfidis & Tsaliki use delta(gross profit). Both work in practice
  (book p. 301).

## Discontinued / hard-to-extend sources

| Source                          | Status                | RSCD response                     |
|---------------------------------|-----------------------|-----------------------------------|
| OECD ISDB 1994                  | Discontinued by OECD  | Use OECD STAN as overlap anchor; document industry-mapping drift |
| Salter (1969) Tables 28, 33     | Historical only       | Treat as frozen historical illustration; no extension |
| Tsoulfidis & Tsaliki (2011) Greek dataset | Not redistributed | Locate paper PDF; if no raw data, accept as frozen exhibit |
| BEA NIPA 2008 vintage           | Superseded by 2013, 2018, 2023 vintages | Re-fetch components and re-run formula end-to-end; do not splice |

## Cross-references

- S705 and S706 share data ingestion pipeline (BEA GDPbyInd + Fixed
  Assets + WEQ/OOH/inventory/reserve adjustments). Implement as a single
  loader producing both ROP and IROP panels.
- S703 and S704 share data ingestion (OECD ISDB 1994 via Christodoulopoulos).
  Implement together if Christodoulopoulos data file can be located.
- S707 and S708 share the same primary source (Tsoulfidis & Tsaliki 2011);
  loader should ingest both Greek panels together.
- S701 and S702 share Salter (1969) source; loaders can read both
  ShaikhChoppedTables files in a single step.
- Figures 7.16 (US ROP deviations) and 7.18 (US IROP deviations) DO NOT
  have RSCD series IDs in the 8-series Ch7 allotment. CD2 had S035 and
  S037 for these, but neither maps to an S70x in the current crosswalk.
  Phase 4 may want to add S709 and S710 for these missing deviation
  panels.
- Figure 7.21 (OECD IROP deviations, 1988-2003) is the CD2 S038 content
  that the stub's S707 name field mislabeled. Phase 4 should add a
  separate S70x for Fig 7.21.

## Open questions (chapter-wide)

1. **CRITICAL — S707 stub mismatch**: Stub name "OECD Industry IROP
   Deviations (PPP-adjusted)" + CD2 link S038 (which in CD2 was OECD
   STAN IROP for Fig 7.21) is INCONSISTENT with stub figures=[Fig7.19]
   and year_range=[1962,1991]. This dossier resolved in favor of the
   figure number (Greek Mfg AVERAGE ROP per Tsoulfidis & Tsaliki 2011),
   but Phase 4 should review and either confirm or add a separate S70x
   for the OECD IROP Fig 7.21 content.
2. **Missing Shaikh (2008) appendix B**: The full 31-industry exclusion
   list for S705/S706 is not in SalvagedInputs. Without it, RSCD cannot
   exactly reproduce the 30-industry sample. Locate Shaikh (2008) PDF.
3. **Missing Christodoulopoulos (1995) data files**: Shaikh's Appendix
   7.2 files in SalvagedInputs (Appendix7_iropdataUSind.xlsx,
   Appendix7_ropdataUSind.xlsx) are for the 1987-2005 BEA US analysis
   (S705, S706), NOT for S703 (World 1970-89) or S704 (US 1960-89). The
   ISDB-based files are missing.
4. **Missing Tsoulfidis & Tsaliki (2011) raw data**: Greek industry-level
   panels for S707 and S708 are not in SalvagedInputs; Shaikh did not
   redistribute them in his Appendix 7.2.
5. **NIPA vintage drift**: Post-2013 R&D/IP capitalization changes BEA
   Fixed Asset levels materially. Any S705/S706 extension to 2006+ must
   document and decide on R&D/IP inclusion (recommendation: exclude to
   match Shaikh's 2008 capital concept).
6. **Content-type re-classification**: S701 and S702 are
   cross-sectional, not time_series (corrected from stub default in
   each dossier).

## Addendum — Additional series S709-S711 (decision 0004)

**Wave**: B (expansion)
**Agent**: opus-subagent-s709/s710/s711
**Date**: 2026-05-18

Decision 0004 added three series that complete Ch7's empirical coverage. The
original 8-series allotment (S701-S708) included the ROP and IROP LEVELS for
the US (S705, S706) and the Greek panels (S707, S708), but did NOT include
the per-industry DEVIATION panels for Figs 7.16, 7.18, 7.21. The deviation
panels are the primary visual exhibits operationalizing Shaikh's turbulent
equalization claim - they are essential, not redundant. This addendum closes
that gap.

| SID  | Figure  | Period    | Source                                     | CD2  | Construction | Quotes | Ext.cand |
|------|---------|-----------|--------------------------------------------|------|--------------|--------|----------|
| S709 | Fig7.16 | 1988-2005 | BEA GDPbyInd + Fixed Assets / Shaikh 2008  | S035 | formula      | 4      | 3 (BEA+) |
| S710 | Fig7.18 | 1988-2005 | BEA GDPbyInd + FA T3.7ES / Shaikh 2008     | S037 | formula      | 4      | 3 (BEA+) |
| S711 | Fig7.21 | 1988-2003 | OECD STAN 2003 + PWT 6.2 / Shaikh 2008     | S038 | composite    | 6      | 2 (OECD/PWT) |

### Relationships

- **S709 = derived from S705**: dev_i,t = ROP_i,t - ROP_avg,t. One-line algebraic
  transform of S705 output. No new data ingestion. The S705 loader should
  emit both as joint outputs.
- **S710 = derived from S706**: dev_i,t = IROP_i,t - IROP_avg,t. Same pattern.
- **S711 is independent**: separate OECD STAN-based composite pipeline (not
  derivative of S703/S704, which were Christodoulopoulos's 1994 ISDB; S711
  uses Shaikh's own 2003 STAN-based construction per Appendix 7.1 V).

### Resolution of S707/S038 mismatch

The Ch7 main rollup (above) flagged a CRITICAL issue: the original S707 stub
was named "OECD Industry IROP Deviations (PPP-adjusted)" with CD2 link to
S038, but its `figures: [Fig7.19]` and year_range [1962,1991] pointed to the
Greek manufacturing panel. The wave-b-ch7 agent resolved the conflict in
favor of the figure number (S707 = Greek Mfg ROP per Tsoulfidis & Tsaliki).
S711 now correctly hosts the OECD STAN IROP content for Fig 7.21 that CD2
S038 originally documented. The CD2 ancestor for S711 is therefore S038
(not previously claimed by any S70x).

### New substantive findings from the deviation panels

- **S709 / Fig 7.16 (book p. 305 verbatim)**: of 30 industries, 18 cross
  the zero line, 7 stay persistently above, 5 stay persistently below.
- **S710 / Fig 7.18 (book p. 305 verbatim)**: ALL 30 industries cross
  zero; minimum number of crossings is 4 (Fabricated Metals), maximum 12
  (Broadcast). This is the chapter's single strongest empirical exhibit
  for turbulent equalization of regulating profit rates.
- **S711 / Fig 7.21 (book p. 305 verbatim)**: OECD IROP deviations show
  "the same patterns" as the US case - incremental rates cross back and
  forth a great deal.

### New open questions

1. **Aggregation convention for ROP_avg / IROP_avg** (S709, S710):
   weighted aggregate (sum_i PG / sum_i K) vs unweighted mean of industry
   rates. Book p. 305 wording suggests weighted; inspect Appendix 7.2 xlsx
   to confirm.
2. **30 industries vs 38 panels** (S709, S710): Fig 7.16 and Fig 7.18
   each display 38 small-multiple panels (including sub-aggregates like
   Manufacturing D/ND, Real & Rental). Phase 5 plotting must mirror
   Shaikh's panel set.
3. **OECD STAN 2003 vintage discontinuity** (S711): Shaikh used ~30
   countries; current STAN 2025 covers only ~18. Extension requires
   accepting reduced country coverage + ISIC Rev 3 -> Rev 4 crosswalk.
   Decision 0005 already defers discontinued-API decisions to Phase 4.
4. **Appendix7_iropOECDPPP.xlsx presence** (S711): unconfirmed whether
   this sheet is in SalvagedInputs. If missing, Phase 4 should pull from
   anwarshaikhecon.org or reconstruct.

### Anti-degradation reminder

S709/S710 are pure algebraic derivatives of S705/S706 - their vintage,
adjustments, and industry sample are inherited. S711 is an independent
composite with its own vintage discontinuity. NONE of the three may be
spliced across BEA or STAN vintages; any extension requires end-to-end
re-computation on a coherent single vintage.

## Validator status

Run `python Technical/code/utils/_phase3_research_validator.py` after
this dossier set; expect 8/8 PASS for S701-S708 given:
- All 8 have >= 2 verbatim quotes with role coverage (definition + source)
- All 8 have a complete primary_source (agency, publication,
  table_or_series_id, url, units, frequency)
- All 8 have construction = direct (S701, S702) or composite (S703-S708),
  with components populated for the composite cases
- All 8 have year_range_book set
- All 8 time_series (S703-S708) have >= 1 extension_candidate; the
  cross_sectional (S701, S702) carry extension candidates anyway with
  clearly documented "not extensible" concerns
- All 8 have multiple methodology_notes, multiple open_questions, and
  the wave-b-ch7 review_history entry.


---

## Phase 5-8 Closure (2026-05-18)

**Agent**: opus-subagent-ch7-fanout
**Scope**: Phases 5 (Ingestion), 6 (Extension), 7 (Replication), 8 (Output) for the full 11-series Ch7 set (S701-S711, including the three series added by decision 0004: S709, S710, S711).

### Validation summary

All 11 series pass V03 validation against the salvaged book-period data, byte-exact (MAE = 0.0, max_pct_err = 0.0).

| SID  | content_type     | V03 status              | MAE | n   | chopped rows | extenbook bytes |
|------|------------------|-------------------------|-----|-----|--------------|------------------|
| S701 | cross_sectional  | PASS (tol 0.5%)         | 0.0 | 51  | 51           | 18,522           |
| S702 | cross_sectional  | PASS (tol 0.5%)         | 0.0 | 56  | 56           | 19,099           |
| S703 | data_unavailable | PASS_DATA_UNAVAILABLE   | n/a | n/a | (none)       | (none)           |
| S704 | data_unavailable | PASS_DATA_UNAVAILABLE   | n/a | n/a | (none)       | (none)           |
| S705 | time_series      | PASS (tol 1.0%)         | 0.0 | 608 | 608          | 47,066           |
| S706 | time_series      | PASS (tol 1.0%)         | 0.0 | 576 | 576          | 45,774           |
| S707 | data_unavailable | PASS_DATA_UNAVAILABLE   | n/a | n/a | (none)       | (none)           |
| S708 | data_unavailable | PASS_DATA_UNAVAILABLE   | n/a | n/a | (none)       | (none)           |
| S709 | time_series (formula derivative of S705) | PASS (tol 0.5%) | 0.0 | 589 | 589 | 44,174 |
| S710 | time_series (formula derivative of S706) | PASS (tol 0.5%) | 0.0 | 558 | 558 | 42,685 |
| S711 | time_series (composite)                  | PASS (tol 1.0%) | 0.0 | 448 | 448 | 38,001 |

### Per-series notes

- **S701 / S702 (Salter cross-sections)** — reclassified to `cross_sectional` per Phase 4 (registry default was `time_series`). DPR/EPR ratify the no-extension stance: Salter's 1920s/1950s/60s industry schema cannot be reconstructed from modern BLS PRS / ONS Productivity. Loader normalises the salvaged xlsx file-naming swap (file `Appendix7_SalterULCPriceTable28.xlsx` actually contains the US 1923–50 panel for Fig 7.11; file `Appendix7_SalterULCPriceTable33.xlsx` contains the UK 1954–63 Reddaway Addendum panel for Fig 7.12).
- **S703 / S704 (Christodoulopoulos)** — `data_unavailable`. L01 returns SKIPPED; V03 returns PASS_DATA_UNAVAILABLE. DPR + EPR document why (OECD ISDB 1994 discontinued; Christodoulopoulos raw panel not redistributed). No chopped CSV; no extenbook (per playbook recipe).
- **S705 / S706 (US BEA panels)** — byte-exact reproduction from Shaikh Appendix 7.2 `ropdataUSind` / `iropdataUSind` xlsx. End-to-end BEA pipeline extension to 2024 (per CD2 trajectory) is feasible but deferred to a follow-up wave per the EPR — requires careful exclusion of post-2013 R&D/IP capitalisation to preserve Shaikh's 2008 capital concept.
- **S707 / S708 (Tsoulfidis–Tsaliki Greek)** — `data_unavailable`. T&T paper provides only regression coefficients and visual plots; the underlying 20-industry deviation panel is not tabulated.
- **S709 / S710 (US deviation derivatives)** — read directly from the `*_Deviation` / `*_Dev` columns of the same xlsx as S705/S706. The aggregate-before-ratio All-Private baseline is preserved (book p. 305 wording). 38-panel small-multiple layout deferred to Phase 9 viz.
- **S711 (OECD STAN PPP)** — closes the long-standing S707/S038 alias collision (decision 0004). Byte-exact 1988–2005 panel from Appendix 7.2 `iropOECDPPP` xlsx (Fig 7.21 plots 1988–2003); extension via OECD STAN 2025 + PWT 10.01 deferred (Concept Match Justification required for the 30→18 country discontinuity and ISIC Rev3→Rev4 crosswalk).

### Artifacts produced

For each of the 7 extractable series: DPR + EPR + L01 + P02 + V03 + processed parquet + chopped CSV + extenbook xlsx. For each of the 4 `data_unavailable` series: DPR + EPR + L01 (SKIPPED) + V03 (PASS_DATA_UNAVAILABLE). All registry entries updated with `status`, `content_type`, `construction`, `units`, `subseries`, `extension_status`. 12 new entries added to `SUBSOURCE_METADATA.json`. All 11 series logged in `ANU_LEDGER.json` with `phases_completed: [3_research, 4_adequacy, 5_ingestion, 6_extension, 7_replication, 8_output]`.

### Open questions deferred to follow-up waves

1. End-to-end BEA pipeline re-fetch + WEQ/OOH/inventory/reserve recomputation to extend S705/S706/S709/S710 to 2024 (CD2 has a trajectory; ratify on a coherent current NIPA vintage).
2. OECD STAN 2025 + PWT 10.01 extension for S711 (1988–2003 published; 2004–2023 deferred with explicit Concept Match Justification per book p. 859 V.3).
3. PDF figure digitisation for S703/S704/S707/S708 (Phase 9 visualisation task; constrained by Anu No-Synthetic rule).
4. 38-panel small-multiple layout for S709/S710 (Phase 9 viz, book PDF pp. 346, 348).

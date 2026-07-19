# S601 — Corporate and Non-Corporate Profit Rates — Methodological History Report (MHR)

**Group:** ch6 (Capital and Profit) · **Construction:** composite · **Status:** book_period_validated
**Figures:** 6.1, 6.4, 6.5 · **Predecessor:** CD2 S026 · **Publish:** true
**Reasoning stance:** from Shaikh's own perspective — why *he* built the series this way.

> Grounding note: every author-intent claim below is anchored to a citable path — the research JSON
> (`Technical/research/S601_research.json`), the chapter summaries (`CH6_RESEARCH_SUMMARY.md`,
> `CH6_GPIM_SUMMARY.md`), the review (`Technical/methodology_review/CH06_review.json`), and the
> Phase-0 NIPA timeline. No claim is invented.

---

## 1. What it is (book definition + Appendix 6 table + figure)

S601 is the pair of **sectoral average profit rates** — corporate `rcorp`, noncorporate `rnoncorp`,
and the business aggregate `rbus` — that open Shaikh's empirical measurement of profitability
(book pp. 245–246). It is the series that motivates the whole chapter: once the two NIPA pathologies
are corrected (imputed-interest, and the noncorporate wage-equivalent), *"corporate and non-corporate
profit rates turn out to be very similar (figure 6.1)"* (p. 245, `book_quotes[0]`, role=definition),
which licenses Shaikh's use of the **corporate** rate as the simpler operational proxy for the general
rate of profit (p. 246, methodology_notes[2]).

Three figures live in this dossier per the CD2 S026 mapping:
- **Fig 6.1** — `rbus`, `rcorp`, `rnoncorp`, 1947–2011 (the "very similar" result).
- **Fig 6.4** — Shaikh's cointegration-derived capacity utilization `uK` against the FRB G.17 measure `uFRB`.
- **Fig 6.5** — normal-capacity profit and maximum profit rates (structural decomposition eqs 6.12/6.13).

The profit-rate decomposition Shaikh writes at p. 250 (`book_quotes[2]`, role=method) is the analytical
backbone of Figs 6.4/6.5: `r = P/K = (P/Y)·R_n·u_K` (6.12) and `r_n = (P/Y)_n·R_n` (6.13), where
`u_K = Y/Y_n` is capacity utilization (normal level 1) and `R_n = Y_n/K` is the Sraffian capacity-capital
maximum rate. Canonical published values are Appendix 6.8 **Table I-3** columns `S208AW` (Pcorp/KNCcorp(-1))
and `S208AX` (Pnoncorp/KNCnoncorp(-1)); capacity `uK`/`uFRB` come from **Table II-7**. The subseries ship as
S601-A `rcorp`/I3, S601-B `rnoncorp`/I3, S601-C `rbus`/I3, S601-D `uK`/II7, S601-E `uFRB`/II7
(`S601_DPR.md`).

## 2. Source lineage (the GPIM chain)

Primary sources, all public-domain, aggregated by Shaikh into Appendix 6.8 Tables I-3 / II-7:

| Input | Source table | Role in S601 |
|---|---|---|
| Corporate GVA / profit `P` | **BEA NIPA T1.14** | numerator base (corporate) |
| Net monetary interest `NMINT` (FISIM reversal) | **BEA NIPA T7.11** | imputed-interest adjustment → `NOS = P + NMINT` |
| Wage-equivalent `WEQ2` (proprietors/partners) | **NIPA T1.13/T1.14/T6.x** via Shaikh App. 6.7.I.2 | noncorporate surplus correction |
| Net fixed capital `KNC(-1)` by legal form | **BEA Fixed Asset T6.1** (current-cost net stock) | denominator (lagged) |
| Capacity output `Y_n`, `u_K` | Shaikh cointegration, App. 6.6 | Fig 6.4/6.5 normal-capacity |
| `u_FRB` | **Federal Reserve G.17** (post-1967) | Fig 6.4 comparison line |

Formula (research JSON `formula`): `rcorp = NOS_corp / KNC_corp(-1)`, `rnoncorp = NOS_noncorp / KNC_noncorp(-1)`,
`rbus = NOS_bus / KNC_bus(-1)`, with `NOS_corp = P + NMINT` and `NOS_noncorp = NOS − WEQ`.

Within the RSCD subseries scheme the GPIM construction internals feeding this chain are the **XS
appendix series** (Decision 0002): **XS003** (imputed-interest adjustment + sectoral rates rbus/rcorp/rnoncorp),
**XS001** (business-sector NOS via GDP/GDI decomposition), **XS002** (WEQ2 + corp/noncorp split), and the
GPIM capital stock **XS004** (KNC/KGC). S601's registry `components=[XS003, XS004, XS009]` reference this
chain; see §5 for the honest limit on how that reference is wired.

## 3. Why these sources — Shaikh's rationale + rejected alternatives

Shaikh's central methodological move is that **NIPA as published does not measure the classical profit
rate**, so he corrects it rather than adopting it:

- **Why reverse the FISIM imputation (T7.11), rejecting NIPA's published NOS.** NIPA treats banks as
  producing "banking services" imputed to depositors, which shifts net monetary interest out of profit.
  Shaikh reverses it: *"Removing the imputed quantities returns net operating surplus to being the sum of
  actual net monetary interest paid and NIPA profit, just as in classical and business accounts"* (p. 246,
  `book_quotes[1]`). The effect is small on value added (~1–2% in 2009) but ~10% on corporate NOS — material
  for the profit *share*, not the output-capital ratio.
- **Why the wage-equivalent (WEQ2) correction for the noncorporate sector.** NIPA books *all* proprietor
  income as operating surplus; Shaikh splits out the wage-equivalent of proprietors/partners (App. 6.7.I.2),
  lowering measured noncorporate surplus (~30% combined effect on total business NOS in 2009, p. 246).
- **Why the corporate rate is the workhorse.** Because after both corrections the sectors nearly coincide
  (Fig 6.1), and the corporate rate needs *only* the easy imputed-interest fix — no WEQ estimation — Shaikh
  adopts it as the operational proxy for the general rate (p. 246, methodology_notes[2]).
- **Why current-cost net stock lagged one period.** The rate is real by construction because numerator and
  denominator share the same current price level (p. 244); Shaikh rejects deflating separately.
- **Rejected alternative — BEA chain-weighted real capital.** Shaikh rejects BEA's quality-adjusted
  chain-weighted stock because it departs from the perpetual-inventory rule and distorts the output-capital
  trend (p. 244); this is the same objection that drives the GPIM in S602/S603 (his own gross stock KGC).
- **Rejected alternative — FRB capacity as the capacity measure.** For the *structural* decomposition Shaikh
  uses his own cointegration-derived `u_K`, not FRB G.17; FRB appears only as the Fig 6.4 comparison line
  (research JSON extension_candidates[3]).

## 4. Methodological-change exposure — NIPA vintage drift (KEY SECTION)

Shaikh's Appendix 6.7 footnote 1 fixes **all BEA data at the 2011 vintage**
(`NIPA_CHANGE_TIMELINE.md` §"Why this matters"; `CH6_GPIM_SUMMARY.md` OQ5). Every comprehensive revision
after 2011 changes the concepts S601 rests on:

- **2013 Comprehensive Update (14th).** R&D and entertainment/literary/artistic originals **capitalized** as
  fixed investment → new Intellectual Property Products category; ≈ +$400B to GDP; **CFC, NOS, and
  fixed-asset/capital-stock levels rise**, and the FISIM in T7.11 was restated by sector
  (`NIPA_CHANGE_TIMELINE.md` 2013 row). This directly perturbs both the S601 numerator (NOS via T1.14) and
  denominator (KNC via FA T6.1). Row order in T7.11 is *unchanged*, but magnitudes changed — so a
  post-2013 fetch must **not** be spliced onto the 2011-vintage `rcorp`.
- **2018 Comprehensive Update (15th).** Inserted a new monetary-interest sub-row in the financial-corporate
  block of **T7.11 → +1 line shift** for every line ≥ 28. Shaikh's 2011-vintage imputed-interest recipe
  (App. Table 6.7.11, p. 842) uses lines `4, 28, 44, 52, 53, 54, 73, 74, 75, 91`; on a 2018+ vintage these
  become `4, 29, 45, 53, 54, 55, 74, 75, 76, 92`. Any post-2011 extension of `NMINT_corp` (hence `NOS_corp`,
  hence `rcorp`) that uses hard-coded lines silently reads the wrong rows. The remap is documented in
  **`Technical/docs/methodology/NIPA_T711_FISIM_remap.md`** and resolved by BEA `LineDescription` stub label,
  not line number (`_nipa_t711_line_resolver.py`).
- **2023 Comprehensive Update (16th).** Reference year → 2017, 2017 benchmark I-O; smaller for S601 but shifts
  chain-index levels.

Because the S601 chopped series ends at 2011, the vintage-drift handling is **staged but untested**
(CH06_review finding L4): the FISIM resolver and BEA-1993 depreciation staging exist, but no extension has
exercised them. The binding practical constraint on any extension is that `NMINT_corp` from T7.11 is
incomplete for recent years (research JSON extension_candidates[1]) — freeze at last complete year, never
forward-fill.

## 5. Replication fidelity note

- **Bit-exact to Appendix 6.8.** CH06_review ground-truth check: S601 subseries (`rcorp/I3`, `rnoncorp/I3`,
  `rbus/I3`, `uK/II7`, `uFRB/II7`) reproduce the Shaikh workbook at **0.0000% max pct error**
  (n = 65/65/65/65/45). `V03_S601` round-trips at 1.0% tolerance.
- **Transcription of finished columns, not a live GPIM recompute.** What ships is Shaikh's *published*
  Appendix 6.8 columns transcribed verbatim (`SalvagedInputs/book_data/ShaikhChoppedTables/Appendix6_Table68{I3,II7}.xlsx`),
  not an end-to-end recomputation of `NOS/KNC` from raw NIPA. This is faithful for the book period and satisfies
  the anti-lazy-splice rule, but the profit-rate *formula* is not executed in code for 1947–2011.
- **XS→S6xx linkage is prose-only, not machine-wired** (CH06_review M1, verdict
  `declarative_prose_only_not_machine_wired`). `series_registry.json` lists `S601.components=[XS003,XS004,XS009]`,
  but `L01_S601.py` calls `_ch6_appendix_loader.load_variables('I3'/'II7', col)` reading the Appendix workbook
  columns directly; no XS output parquet is consumed. Harmless in the book period (both trace to the same
  Appendix 6.8, verified 0.0000%) but the GPIM→profit-rate chain is **non-executable** as wired.
- **`reference_values` are circular** (CH06_review M3): V03 round-trips the same XLSX the chopped is built from.
  S601 has no independent non-circular book anchor of its own (unlike S604's Table 6.24); Appendix Table 6.7.4
  (p. 832: rbus=7.7%, rcorp=7.5%, rnoncorp=8.1% for 2009, `CH6_GPIM_SUMMARY.md`) is the nearest external cross-check.
- **Units label defect** (CH06_review M4): S601's series-level units string mislabels the capacity-utilization
  subseries (uK/uFRB are percent-of-capacity, not decimal_rate); per-subseries units are correct.

## 6. Forward risk

- **Next NIPA benchmark re-defines capital again.** The 2013/2018/2023 sequence shows each comprehensive
  update can re-scope CFC, NOS, and the capital stock; a future benchmark (post-2023) will do so again. S601's
  numerator and denominator both move, so no historical `rcorp` value is vintage-stable — extension must
  re-fetch and re-compute on one coherent vintage (`NIPA_CHANGE_TIMELINE.md` §"Why this matters").
- **BEA-1993 depreciation archive recovery is a prerequisite for a *true* GPIM recompute.** The KNC/KGC that
  should feed S601's denominator (via XS004) needs the BEA 1993 finite-life depreciation/retirement rates that
  are no longer in the BEA iTable. They are staged at
  `SalvagedInputs/book_data/Reconstructed/BEA_1993_FA_methodology/BEA_1993_depreciation_retirement_rates.{csv,json}`
  and recoverable from the KB source `Inputs/Capitalism Data/.../Knowledge_Base/1993_DoC_Fixed_Reproducible_Tangible_Wealth/`.
  Until wired (M1), any extension uses BEA-published stock, not Shaikh's GPIM.
- **T7.11 FISIM resolver is untested at extension** (L4): the stub-label remap must be exercised on a live
  post-2018 fetch before `NMINT_corp` extension can be trusted; the `NMINT_corp` incompleteness bounds the
  extension window regardless.

# S602 — Corrected vs Conventional Corporate Profitability — Methodological History Report (MHR)

**Group:** ch6 (Capital and Profit) · **Construction:** formula · **Status:** book_period_validated
**Figures:** 6.2, 6.6 · **Predecessor:** CD2 S027 · **Publish:** true
**Reasoning stance:** from Shaikh's own perspective.

> Grounding: `Technical/research/S602_research.json`, `CH6_RESEARCH_SUMMARY.md`, `CH6_GPIM_SUMMARY.md`,
> `Technical/methodology_review/CH06_review.json`, `NIPA_CHANGE_TIMELINE.md`. No invented claims.

---

## 1. What it is (book definition + Appendix 6 table + figure)

S602 is the chapter's **flagship contrast**: it plots Shaikh's *corrected* corporate profitability measures
against the *NIPA-conventional* ones, six curves in all — corrected vs NIPA **maximum profit rate** `R`,
**average profit rate** `r`, and **profit share** `σ_P`. It is the empirical payoff of the corrections that
S601 introduced, and it is where Shaikh demonstrates that NIPA-only series *mask* the secular profit-rate decline.

The accounting definitions are eqs (6.8)–(6.10), stated verbatim at p. 248 (`book_quotes[0]`, role=definition):
`VA = NOS + EC`, `NOS = P + NMINT` (6.8); `σ_P = NOS/VA = 1 − EC/VA` (6.9); and the master average-rate identity
`r ≡ NOS/KTC(-1) = (P + NMINT)/(KGC(-1) + INV(-1))` (6.10), where `KGC` = gross current-cost fixed capital
(Shaikh's GPIM stock), `INV` = inventories, and `KTC = KGC + INV` = **total capital stock**.

- **Fig 6.2** (p. 248, `book_quotes[1]`, role=source) — uncorrected for capacity. The corrected maximum rate
  `VA/KTC(-1)` *"falls more, and more steadily, than the NIPA one"*, a gap Shaikh attributes primarily to the
  new gross fixed-capital measure (Appendix 6.8.II.5), since the imputed-interest effect on VA is <2% and the
  inventory/capital ratio is stable.
- **Fig 6.6** (p. 253, `book_quotes[2]`, role=caveat) — capacity-normalized. `Rcorp'_n`/`rcorp'_n` are corrected
  for **both** sets of variables (capital-stock + capacity, and imputed-interest + inventories); `Rcorp''_n`/`rcorp''_n`
  are the **proxy** variant corrected only for the first set. *"The corrected and proxy measures are fairly
  similar, which indicates that the capital stock and capacity utilization corrections are the crucial ones."*

Canonical values: Appendix 6.8 **Table II-7** columns `S013J` (rcorp), `S013O` (rcorpnipa), `S013I` (corrected
share NOS/VA), `S013N` (NIPA share P/VA), plus the maximum-rate columns. Ships as subseries `Rcorp`, `Rcorpnipa`,
`rcorp`, `rcorpnipa`, `Profshcorp`, `Profshcorpnipa` (CH06_review ground_truth_check; all n=65, 0.0000% error).

## 2. Source lineage (the GPIM chain)

| Input | Source table | Role |
|---|---|---|
| Corporate VA, `P`, `EC` | **BEA NIPA T1.14** | VA & share numerators/denominators |
| `NMINT` (FISIM reversal) | **BEA NIPA T7.11** | `NOS = P + NMINT` (imputed-interest adjustment) |
| **`KGC` gross current-cost fixed capital** | **Shaikh GPIM** on BEA FA investment flows (App. 6.7.V, 6.8.II.5) | corrected fixed-capital denominator |
| `INV` corporate inventories, current-cost | **IRS SOI corporate balance sheets** (1926–2011), scaled | inventory component of `KTC` |
| `KNC_corpbea` official net stock | **BEA Fixed Asset T6.1** | conventional (NIPA) denominator |
| `u_K`, `u_FRB` | Shaikh App. 6.6 cointegration; **FRB G.17** | Fig 6.6 capacity normalization |

The three divergence axes between corrected and conventional (research JSON methodology_notes[1]) are exactly the
three adjustments: (1) **GPIM `KGC` vs BEA `KNC_corpbea`** (capital-stock), (2) **`NOS = P + NMINT`**
(imputed-interest), (3) **`KTC = KGC + INV`** (inventory). These are formalized as the decomposition
`r/r_nipa = (x1/x2)·x3` (eq. 6.11) — the subject of **S603**.

GPIM internals feeding S602 are the **XS appendix series**: **XS004** (preferred GPIM `KNCcorp`/`KGCcorp`,
combining BEA-2011 initial value + BEA-1993 depreciation + IRS interwar adjustment), its sensitivity variants
**XS005–XS008**, and **XS009** (`KTCcorp = KGCcorp + INVcorp`, the corrected total-capital denominator).
Registry `S602.components=[XS003, XS004, XS009]`.

## 3. Why these sources — Shaikh's rationale + rejected alternatives

- **Why the GPIM over BEA's published net capital stock — the core of the chapter.** Shaikh rejects BEA's
  chain-weighted, quality-adjusted net stock because its quality adjustment and chain aggregation depart from the
  perpetual-inventory rule and distort the long-run output-capital trend (p. 244; research JSON
  extension_candidates[1].concerns). He substitutes his **Generalized Perpetual Inventory Method**: accumulate BEA
  current-cost gross investment flows under his own initial value and depreciation assumptions (Appendix 6.5,
  accumulation eqs 6.5.21–6.5.23; Appendix 6.7.V), yielding a *gross* current-cost stock `KGC`. Fig 6.2 shows the
  payoff: because `KGC` rises relative to BEA's `KNC`, the corrected maximum rate falls steadily where the NIPA one
  does not — this is the empirical evidence for Shaikh's claim that NIPA masks the secular decline. The initial-1925
  value matters enough (~28% level shift, p. 247, App. 6.7.V.4) that Shaikh runs four explicit GPIM sensitivity
  variants (XS005–XS008).
- **Why business-sector NOS with the imputed-interest (WEQ/FISIM) removal.** Same rationale as S601: restore
  `NOS = P + NMINT` so surplus matches classical/business accounts (p. 246). Here the effect is largest on the
  profit *share* (raising NOS ~10%), which is why the corrected share sits above the NIPA share in Fig 6.2.
- **The specific profit-rate concept `r = P/(K+INV)`.** Shaikh insists the denominator is **total** capital
  `KTC = KGC + INV`, not fixed capital alone: inventories are advanced capital that must earn the general rate, so
  omitting them (as NIPA/BEA fixed-asset tables do) understates the capital base. Numerator is the corrected
  `NOS = P + NMINT` at current cost, lagged denominator — real by construction (eq. 6.10).
- **Rejected alternative — NIPA fixed capital as the denominator.** That is precisely the *conventional* measure
  S602 is built to expose; Shaikh keeps it only as the contrast line `KNC_corpbea`.
- **Why the Fig 6.6 proxy variant exists.** The imputed-interest and IRS-inventory data are infeasible for OECD
  industries; Shaikh shows the capital-stock + capacity corrections alone reproduce the fully-corrected measures
  closely, licensing the proxy for the inter-sectoral/industry work of Ch7 and Ch9 (methodology_notes[4]).

## 4. Methodological-change exposure — NIPA vintage drift (KEY SECTION)

S602 is the **most vintage-exposed** Ch6 series because it depends on *all* the moving parts — NIPA VA/profit
(T1.14), FISIM (T7.11), the entire fixed-asset investment history that the GPIM accumulates (FA T6.1–6.8), and IRS
inventories. Shaikh fixes everything at the **2011 vintage** (App. 6.7 fn 1).

- **2013 Comprehensive Update.** Capitalizing R&D and entertainment originals as fixed investment (new IPP category,
  ≈+$400B GDP) **raises CFC, NOS, and the fixed-asset stock levels** and restates FISIM by sector
  (`NIPA_CHANGE_TIMELINE.md` 2013 row). This is the deepest exposure: the GPIM *accumulates the entire history of
  BEA gross investment*, so re-capitalized IPP flows change `KGC` at every year, not just recent ones. A post-2013
  GPIM is **a different capital concept** than Shaikh's 2011-vintage `KGC` — silently splicing would corrupt the very
  quantity (KGC vs KNC gap) that S602 exists to display (CH6_GPIM_SUMMARY OQ5; research JSON extension_candidates[1]).
- **2018 Comprehensive Update.** The **T7.11 +1 line shift** (new financial-corporate monetary-interest sub-row)
  breaks the hard-coded imputed-interest recipe for `NMINT` (2011 lines `4,28,44,52,53,54,73,74,75,91` →
  `4,29,45,53,54,55,74,75,76,92`); resolve by stub label via
  `Technical/docs/methodology/NIPA_T711_FISIM_remap.md` / `_nipa_t711_line_resolver.py`.
- **2023 Comprehensive Update.** Reference year → 2017, 2017 benchmark I-O; shifts chain-index levels underlying the
  FA tables.
- **Practical binding constraint.** `NMINT_corp` incompleteness in recent T7.11 (research JSON methodology_notes[3])
  bounds the corrected-measure extension window; freeze rather than impute.

Because the chopped ends 2011, this drift handling is **staged but untested** (CH06_review L4).

## 5. Replication fidelity note

- **Bit-exact.** All six S602 subseries reproduce Appendix 6.8.II.7 at **0.0000% max pct error** (n=65 each,
  CH06_review). `V03_S602` round-trips at 1.0% tolerance.
- **Transcription, not live recompute** (CH06_review M5). `construction:formula` is recorded, but `P02_S602.py`
  transcribes Shaikh's pre-computed II-7 columns rather than executing eqs (6.8)–(6.10) from raw NIPA/FA/IRS inputs.
  Faithful and verbatim for the book period; formula recompute is deferred to extension per EPR.
- **XS→S6xx linkage prose-only, not machine-wired** (CH06_review M1). `L01_S602.py` reads the Appendix workbook
  columns directly; XS004/XS009 (the GPIM `KGC` and `KTC`) outputs are never consumed. So the headline
  GPIM-vs-published-stock story is documented and 0.0000%-faithful, but the GPIM→profit-rate chain is not
  executable as wired.
- **Circular `reference_values`** (CH06_review M3): V03 round-trips the same XLSX the chopped is built from.
- **Banned mixed-units string** (CH06_review M4, D14 BELOW_THRESHOLD): `S602.units = "decimal_rate_and_share"` is
  banned by UNITS_VALIDATION_STANDARD (self-flagged, unremediated) because S602 mixes rates and shares at the
  series level; per-subseries units are correct.

## 6. Forward risk

- **Next NIPA benchmark re-defines capital.** Because the GPIM accumulates the full BEA investment history, *every*
  future comprehensive update that touches investment classification (as 2013 did with IPP) re-levels `KGC` across
  all years — the KGC-vs-KNC gap that is S602's entire message is vintage-specific. No corrected `Rcorp`/`rcorp`
  value is stable; extension must re-run the GPIM on one coherent vintage, never splice.
- **BEA-1993 depreciation archive recovery needed for full recompute.** The preferred GPIM (XS004) requires BEA 1993
  finite-life depreciation/retirement rates absent from the current iTable; staged at
  `SalvagedInputs/book_data/Reconstructed/BEA_1993_FA_methodology/` and sourced from KB
  `1993_DoC_Fixed_Reproducible_Tangible_Wealth`. Until XS004 is wired into `L01_S602`, extension can only use
  BEA-published stock — i.e. reproduce the *conventional* measure, not Shaikh's corrected one.
- **IRS SOI inventory availability post-2011** (research JSON open_questions[3]): sample-based, publication lag,
  format changes; the inventory component of `KTC` may need re-anchoring (FRB Z.1 as a candidate). Bounds the
  corrected denominator's extension.

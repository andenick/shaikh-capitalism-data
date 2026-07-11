# XS003 — Methodological History Report (MHR)

**Series**: XS003 — Imputed-Interest (FISIM) Adjustment and Corrected Sectoral Profit Rates
**Chapter**: 6 (Capital and Profit) · **Group**: XS / `xs_class: appendix` (GPIM construction internal)
**Perspective**: authored *from Shaikh's perspective* — why he built this object the way he did.
**Authored**: 2026-06-30 · **Read-only provenance**; every claim traces to a cited path.

Grounding: `Technical/research/XS003_research.json`; `Technical/docs/series/XS003_DPR.md` +
`XS003_EPR.md`; `Technical/docs/chapters/CH6_GPIM_SUMMARY.md`;
`Technical/methodology_review/CH_XS_review.json`;
`Technical/docs/methodology/NIPA_T711_FISIM_remap.md`;
`Technical/docs/methodology/_timelines/NIPA_CHANGE_TIMELINE.md`;
resolver `Technical/code/L01_loaders/_nipa_t711_line_resolver.py`.

---

## 1. What it is

XS003 is the **third and culminating correction of Shaikh's Chapter-6 profit-rate pipeline**: it strips
NIPA's fictitious bank-imputation flows (FISIM — Financial Intermediation Services Indirectly Measured)
out of business surplus, producing the **imputed-interest adjustment `BusImpIntAdj`**, and then combines
that with the XS001 business NOS and the XS002 wage-equivalent split to compute the **corrected sectoral
profit rates rbus, rcorp, rnoncorp** that are the empirical objects of Figures 6.1, 6.4, 6.5 and the whole
Ch16 profit-rate dynamics (`XS003_research.json` figures Fig6.1/6.4/6.5; methodology_notes).

Why the adjustment exists — Shaikh's statement of the problem (verbatim, book p. 835,
`XS003_research.json` definition quote):

> "NIPA insists on treating banks as if they were ordinary businesses. And since ordinary businesses must
> have positive value added and positive gross surplus, 'an imputation for implicit financial services
> produced by banks is included in the NIPA' under the category of net interest paid (Fixler, Reinsdorf,
> and Villones 2010, 347). Since banks are corporations, corporate net interest ends up being largely
> 'composed of imputations' (Ritter 2000, 18). For instance, in 2009 total net interest within aggregate
> NIPA NOS is $841.9 billion, of which $747.6 billion is imputed (NIPA table 7.12, lines 43, 44)."

### The T7.11 recipe (2011-vintage line numbers)

The imputed-interest adjustment is built from NIPA Table 7.11 ("Interest Paid and Received by Sector and
Legal Form"), verbatim book p. 842 (`XS003_research.json` source quote; `NIPA_T711_FISIM_remap.md`):

```
BankNetIntPaid   = T7.11(L4 + L44 + L73) - T7.11(L28 + L52 + L91)
NFNetImpIntPaid  = T7.11(L74 + L75)      - T7.11(L53 + L54)
BusImpIntAdj     = -BankNetIntPaid - NFNetImpIntPaid
```

Then the corrected surplus and rates (`XS003_research.json` formula; `XS003_DPR.md` §Construction):

```
Final business NOS = NOSbusnipa - WEQ2 + BusImpIntAdj
rcorp    = Pcorp    / KNCcorp(-1)
rnoncorp = Pnoncorp / KNCnoncorp(-1)
rbus     = Pbus     / KNCbus(-1)          # all capital stocks lagged one period (beginning-of-year)
```

### 2009 hand-check (Appendix Table 6.7.11, book p. 842)

`XS003_research.json` methodology_notes: **BankNetIntPaid = −37.6; NFNetImpIntPaid = −136.1;
BusImpIntAdj = 173.7**; Final Business NOS = 2,030.3 vs NIPA 2,533.8 (**68.0%**); Final Corporate NOS =
1,416.8 (110.4% of NIPA corporate NOS). Corrected profit rates (Appendix Table 6.7.4, p. 832):
**rbus = 7.7%, rcorp = 7.5%, rnoncorp (WEQ2) = 8.1%, rnoncorp1 (WEQ1) = 10.2%.** The closeness of rbus to
rcorp "validates using the corporate sector as a representative proxy" (book p. 855, Appendix 6.7 Section
VII).

The net magnitude, in Shaikh's words (verbatim, book p. 841, `XS003_research.json` method quote):

> "In 2009 the imputed interest adjustments raise business and corporate net value added measures by only
> 1% and 2%, respectively, but raise business and corporate net operating surpluses by 7% and 10%,
> respectively. But non-corporate operating surplus are also lowered by the transfer out of the wage
> equivalent of proprietors and partners, and this swamps the positive effect of the imputed interest
> adjustment so that the overall business sector NOS is lowered by more than 30%."

### Stub-label resolver (the row-caption map)

The 10 CD2 line numbers are resolved to BEA **stub labels** — the row captions BEA preserves across
vintages — so the recipe survives NIPA renumbering (`NIPA_T711_FISIM_remap.md` §Stub-label mapping):

| Recipe line | Stub label | 2011 line | 2018+ line |
|---|---|--:|--:|
| L4 | `domestic_business__financial_corporate__monetary_interest_paid` | 4 | 4 |
| L28 | `domestic_business__financial_corporate__monetary_interest_received` | 28 | 29 |
| L44 | `financial_corporate__monetary_interest_paid_by_banks` | 44 | 45 |
| L52 | `financial_corporate__monetary_interest_received_by_banks` | 52 | 53 |
| L53 | `nonfinancial_business__imputed_interest_received_for_depositor_services` | 53 | 54 |
| L54 | `nonfinancial_business__imputed_interest_received_for_other_services` | 54 | 55 |
| L73 | `financial_corporate__imputed_interest_paid_for_borrower_services` | 73 | 74 |
| L74 | `nonfinancial_business__imputed_interest_paid_for_borrower_services` | 74 | 75 |
| L75 | `nonfinancial_business__imputed_interest_paid_for_other_services` | 75 | 76 |
| L91 | `financial_corporate__imputed_interest_received_for_depositor_services` | 91 | 92 |

Seven chopped subseries (`XS003_DPR.md` Sources table): XS003-A `BankNetIntPaid`, XS003-B
`NFNetImpIntPaid`, XS003-C `BusImpIntAdj` (dollar adjustments); XS003-D `rbus`, XS003-E `rcorp`,
XS003-F `rnoncorp`, XS003-G `rnoncorp1` (profit rates). Appendix location: **Appendix 6.7 Section IV +
Appendix Tables 6.8.I.3 / 6.8.II.7, book pp. 835–842**; stylized classical-vs-NIPA accounts that *derive*
the BusImpIntAdj formula transparently are Appendix Tables 6.7.5–6.7.10 (pp. 836–840).

## 2. Source lineage

All inputs at the **2011 vintage** (Appendix 6.7 footnote 1, book p. 828). Line-level lineage
(`XS003_research.json` components; primary_source):

- **T7.11** "Interest Paid and Received by Sector and Legal Form" — lines **4, 28, 44, 52, 53, 54, 73, 74,
  75, 91** (the FISIM recipe above).
- **T7.12** "Imputations" — lines **43, 44** (the $747.6B-of-$841.9B imputed-interest illustration,
  book p. 835).
- **Aggregate business NOS** — from **XS001** output (Appendix Table 6.7.3 / 6.8.I.1).
- **WEQ2** — from **XS002** output.
- **KNCbus / KNCcorp / KNCnoncorp** — sectoral net fixed capital, current-cost — **BEA Fixed Asset Table
  6.1**, lines 2 / 9 / (6+7) respectively (the profit-rate denominators, from XS004/XS006).
- **CorpImpIntAdj** (a reported sub-component) — NonFin Corp Borrower Services Paid − NonFin Corp Imputed
  Interest Received = T7.11 line 74 − line 53 (`XS003_research.json` components).

Review touchpoint (`CH_XS_review.json`): kind **NIPA/FISIM**, "T7.11 FISIM imputed interest (lines
4/28/44/52/53/54/73/74/75/91) + T7.12; BEA FA T6.1; _nipa_t711_line_resolver handles vintage line remap;
corrected sectoral profit rates." Methodology sources Shaikh cites: **Fixler, Reinsdorf & Villones (2010)**
"FISIM: A New Approach," *SCB* 90(5) (the canonical imputation-methodology source, book p. 835);
**Ritter (2000)** on corporate net interest being "composed of imputations." Predecessor: **CD2 series
S208** (predecessor_ids.cd2_id = "S208").

## 3. Why these sources, from Shaikh's perspective + rejected alternatives

**Why strip the FISIM imputations at all.** NIPA cannot let banks show negative or zero value added, so it
*imputes* the value of unpriced banking services ("borrower services" and "depositor services") and books
them as net interest. The effect is huge and fictitious: in 2009, $747.6B of the $841.9B of net interest
inside aggregate NOS is imputed (book p. 835). Because "banks are corporations," these imputations inflate
*corporate* net interest and hence corporate/business surplus with flows that never corresponded to a
priced transaction. Shaikh's classical profit concept counts only surplus generated in production, so he
**removes the imputations to restore the classical accounting concept** (`XS003_research.json`
methodology_notes; Appendix 6.7 Section IV). The imputations "cancel out at the aggregate NOS level but
redistribute between the production sector and the banking sector" — so the correction is a *sectoral
re-allocation*, not a change to the total.

**Why the specific (L4+L44+L73)−(L28+L52+L91) / (L74+L75)−(L53+L54) recipe.** Shaikh derives it
transparently, not by assertion: Appendix Tables 6.7.5–6.7.10 (pp. 836–840) walk through stylized
"classical" vs "NIPA" accounts for three cases — production sector only; household-bank only; the combined
economy — so the reader can see exactly which paid/received imputed-interest rows must be netted out to
reverse the FISIM redistribution (`XS003_research.json` methodology_notes). `BankNetIntPaid` nets the
financial-corporate paid legs (monetary + borrower-services imputed) against its received legs;
`NFNetImpIntPaid` nets the nonfinancial-business imputed paid legs against its imputed received legs;
`BusImpIntAdj = −BankNetIntPaid − NFNetImpIntPaid` adds the removed banking imputations back to the
production sector.

**Why beginning-of-year (t−1) capital in the profit-rate denominators.** All rates use lagged capital
`K(-1)` "consistent with the convention that capital must be in place before producing the period's NOS"
(`XS003_research.json` methodology_notes) — the classical stock-flow timing.

**Why current-cost net fixed capital (BEA FA T6.1), not book value.** The denominators KNCbus/corp/noncorp
are *net current-cost* stocks; XS003 inherits the GPIM-corrected stocks (XS004/XS006) rather than IRS book
values, because the profit rate must value capital at replacement cost to be a classical rate of profit
(the deeper capital-stock argument is XS004–XS009's; XS003 consumes their output).

**Rejected alternative — accept NIPA's bank-as-business surplus.** This is precisely what XS003 overturns;
taking NIPA corporate net interest at face value would treat $747.6B of imputed flows as real 2009
corporate surplus (book p. 835), grossly overstating the corporate profit rate.

**Rejected alternative — adjust net value added instead of NOS.** Shaikh notes the imputed-interest
adjustment raises net *value added* by only 1–2% but net *operating surplus* by 7–10% (book p. 841): the
correction matters at the surplus/profit-rate level, which is where he applies it. The point of computing
both is to show the adjustment is small on value-added but decisive on the profit rate.

## 4. Methodological-change exposure — **the central section**

XS003 sits directly on the two RSCD "time-bomb" NIPA events, both in T7.11
(`NIPA_CHANGE_TIMELINE.md` §"Table-renumbering / silent-break events"; `NIPA_T711_FISIM_remap.md`):

1. **2013 Comprehensive Revision — T7.11 magnitude restatement (row order UNCHANGED).** The 2013 update
   (14th, rel. 2013-07-31) restated FISIM by sector as part of the R&D/IPP overhaul (≈ +$400B GDP). Row
   *order* in T7.11 did **not** change, but the per-row *magnitudes* did. Consequence: the 2011-vintage
   line numbers still point to the right captions, but **the values differ across the 2013 boundary — do
   NOT splice values across it** (`NIPA_CHANGE_TIMELINE.md` event 2; `NIPA_T711_FISIM_remap.md`
   §"Resolution approach"). This is a *magnitude* restatement, distinct from the *renumbering* below.

2. **2018 Comprehensive Update — T7.11 +1 line shift (renumbering).** The 2018 update (15th, rel.
   2018-07-27) **inserted one new monetary-interest sub-row** in the financial-corporate block, shifting
   every subsequent line number by **+1**. Shaikh's 2011-vintage recipe lines
   `4, 28, 44, 52, 53, 54, 73, 74, 75, 91` become, on a 2018+ vintage,
   `4, 29, 45, 53, 54, 55, 74, 75, 76, 92` — **line 4 unchanged; every line ≥ 28 shifts +1**
   (`NIPA_T711_FISIM_remap.md` mapping table; `NIPA_CHANGE_TIMELINE.md` event 1). **Vintages 2011–2017
   share the 2011 numbers; 2019–2024 share the 2018 numbers.** A naive hard-coded read on a post-2018
   vintage would silently compute BusImpIntAdj from the wrong rows.

3. **The stub-label resolver — how RSCD survives both.** RSCD does **not** rewrite the recipe with new
   hard-coded numbers (that "would simply move the time-bomb to the next BEA revision",
   `NIPA_T711_FISIM_remap.md`). Instead `_nipa_t711_line_resolver.py` maps each of the 10 lines to its BEA
   stub label and resolves to the live line number at fetch time. Public API:
   `resolve_t711_line(historical_line_num, vintage_year)`,
   `stub_label_to_current_line(stub_label, current_vintage)`,
   `compute_AS003_recipe(t711_values, current_vintage)`,
   `fetch_t711_via_api(year, vintage_year)`. The API helper keys on BEA's `LineDescription` field (not
   `LineNumber`), so it is robust even against future revisions; the pinned vintage table (2011, 2018,
   2024) exists for offline/cached-CSV fetches and diagnostics (`XS003_research.json` phase5_resolver:
   stub_label_count = 10, vintages_pinned = [2011, 2018, 2024]). This was Phase-5 Blocker **B2**, now
   RESOLVED (`XS003_research.json` review_history rscd-a3-ch6-blocker-batch, 2026-05-18).

4. **Failure discipline.** If a future BEA revision *splits or merges* any of the 10 captioned rows, the
   resolver **raises** on lookup and the loader must surface the year as `data_unavailable` rather than
   silently absorbing it (`NIPA_T711_FISIM_remap.md` §Caveats; `XS003_EPR.md` failure-mode table:
   "`_nipa_t711_line_resolver` falls back to nearest pinned vintage with logged warning"). The 2018
   inserted row itself (foreign-bank-branch vs primary-dealer category) is not material to the recipe —
   what matters is that the *captioned* economic content is preserved.

5. **BEA FA T6.1 denominator drift.** The profit-rate denominators come from BEA Fixed Asset T6.1; the
   2013 IPP reclassification **raises capital-stock levels** (`NIPA_CHANGE_TIMELINE.md`), and "BEA FA
   tables now separate IPP; structure of T6.1 may need re-mapping" (`XS003_research.json`
   extension_candidates). So even a correctly-resolved BusImpIntAdj feeds rates whose denominators drift
   with vintage.

**Anti-splice mandate.** Both the 2013 magnitude restatement and the 2018 renumbering are
comprehensive-revision boundaries; per `NIPA_CHANGE_TIMELINE.md`, an extension must re-compute end-to-end
on one coherent vintage and never splice across either boundary (CH6 open-question 5).

## 5. Replication fidelity note

RSCD reproduces XS003 **bit-exact to Appendix 6.8** by the read-the-truth-column pattern: L01 loads the
finished `BankNetIntPaid`/`NFNetImpIntPaid`/`BusImpIntAdj`/`rbus`/`rcorp`/`rnoncorp`/`rnoncorp1` columns
from `Appendix6_Table68*.xlsx`; V03 round-trips at **1.0% tolerance** (`XS003_DPR.md` §Validation
Expectation). Honest limits, disclosed:

- **Formula-declared-but-transcribed — finding F-XS-05 (MEDIUM).** XS003 declares
  `construction: formula` but "carr[ies] components:[] and no formula field, contra the Anu No-Lazy-Splices
  rule. The executable path is a pass-through transcription of Shaikh's Appendix 6.8 workbook (L01 loads
  finished … columns; P02 = schema-only pass-through)." The full FISIM recipe and the profit-rate formulas
  live in DPR prose + `CH6_GPIM_SUMMARY.md` + construction_steps + this MHR, and **the stub-label resolver
  is real code** — but the *end-to-end recompute* of BusImpIntAdj from raw T7.11 exists only in the
  deferred v1.1 EPR extension recipe (`XS003_EPR.md` §Method steps 4–5; `CH_XS_review.json` F-XS-05
  evidence "code/P02_processors/P02_XS004.py", "code/L01_loaders/L01_XS004.py"). So RSCD *has* the machine
  to survive vintage drift (the resolver) but does not exercise it for the book period — it transcribes.
- **Mixed-units leak — findings F-XS-01 (HIGH) + F-XS-07 (LOW).** XS003 is the worst offender in the group.
  Its dollar subseries (A/B/C, `billions_current_usd`) and rate subseries (D/E/F/G, `decimal_rate`) share
  one column, and the chopped artifact `chopped/XS003.csv` carries the **banned units string
  `mixed_billions_usd_and_decimal_rates` on every row** (`CH_XS_review.json` F-XS-01, evidence
  "chopped/XS003.csv (units col all rows)"; D14 gate note). The registry `units: per_subseries` fix "lives
  only in registry metadata" and did not reach the chopped CSV consumed by viz/public downloads; further,
  the registry subseries `native_units` still literally reads `mixed_billions_usd_and_decimal_rates` in 8
  places (**F-XS-07**, LOW). The DPR already prescribes the correct rendering: "XS003-A/B/C are dollar
  adjustments in `billions_current_usd`; XS003-D/E/F/G are profit rates in `decimal_rate`. Rendered as a
  two-panel chart (dollars / rates), never a single shared axis" (`XS003_DPR.md` §Units) — but the artifact
  must be regenerated to match. **This blocks external distribution** (D14 = 85, BELOW_90_BLOCKS_EXTERNAL).
- **Circular-validation caveat.** V03 confirms melt fidelity to the workbook, not an independent
  re-derivation from raw T7.11. The non-circular anchors are the book's printed 2009 figures
  (BankNetIntPaid −37.6; NFNetImpIntPaid −136.1; BusImpIntAdj 173.7; rbus 7.7% / rcorp 7.5% / rnoncorp
  8.1%, Appendix Tables 6.7.11 / 6.7.4), which the values are consistent with.

## 6. Forward risk

- **Exercise the resolver, don't just carry it.** The single highest-value forward step is to make the
  book period *recompute* BusImpIntAdj through `_nipa_t711_line_resolver.compute_AS003_recipe` rather than
  transcribe it (closing F-XS-05), so the pipeline that must survive the 2013/2018 boundaries is actually
  run and tested against the printed 2009 hand-check.
- **Regenerate the chopped artifact with per-subseries units.** F-XS-01/F-XS-07 must be fixed at the L01
  loader (which "hardcode[s] a single series-level unit string", `CH_XS_review.json`): dollars on A/B/C,
  `decimal_rate` on D/E/F/G, two-panel render — before any public release.
- **Row split/merge sentinel.** If BEA ever splits or merges one of the 10 captioned T7.11 rows, the
  resolver raises and the year must go `data_unavailable`, not silently absorbed (`NIPA_T711_FISIM_remap.md`
  §Caveats). New comprehensive revisions require adding a vintage entry to `_T711_LINE_INDEX` (never
  editing pinned vintages) and a new column to the stub-label table (`NIPA_T711_FISIM_remap.md` §"How to
  update").
- **T6.1 denominator re-mapping.** Post-2011 profit-rate denominators need BEA FA T6.1 re-mapped for the
  separated-IPP structure and re-leveled capital stocks (`XS003_research.json` extension_candidates);
  a correct BusImpIntAdj on a wrong-vintage denominator still yields a wrong rate.
- **Upstream propagation and downstream consumption.** XS003 consumes XS001 (business NOS), XS002 (WEQ2),
  and XS004/XS006 (capital denominators); it feeds **S601, S602, S603, S604** directly (`XS003_DPR.md`
  §"Why It Matters"). A vintage or units error here is the most consequential in the chapter — it lands on
  every published corrected profit rate. The 2011-vintage freeze must be preserved for the book series.

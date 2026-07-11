# XS002 — Methodological History Report (MHR)

**Series**: XS002 — Wage Equivalent (WEQ2) and Corporate/Noncorporate Split of Proprietor Income
**Chapter**: 6 (Capital and Profit) · **Group**: XS / `xs_class: appendix` (GPIM construction internal)
**Perspective**: authored *from Shaikh's perspective* — why he built this object the way he did.
**Authored**: 2026-06-30 · **Read-only provenance**; every claim traces to a cited path.

Grounding: `Technical/research/XS002_research.json`; `Technical/docs/series/XS002_DPR.md` +
`XS002_EPR.md`; `Technical/docs/chapters/CH6_GPIM_SUMMARY.md`;
`Technical/methodology_review/CH_XS_review.json`;
`Technical/docs/methodology/_timelines/NIPA_CHANGE_TIMELINE.md`.

---

## 1. What it is

XS002 is the **second step of Shaikh's Chapter-6 profit-rate pipeline**: it solves the
corporate/noncorporate *asymmetry* in NIPA's treatment of business income. NIPA records a corporate
manager's salary as employee compensation but lumps *all* of an unincorporated proprietor's residual
income into "proprietors' income" — as if none of it were profit. XS002 estimates the **wage equivalent**
of proprietors' and partners' labor (WEQ2), subtracts it from proprietors' income to recover the
**noncorporate profit** (Pnoncorp), and thereby makes the two sectors' surplus concepts comparable
(Appendix 6.7 Section III, book pp. 831–833). It plots two appendix figures (Appendix Figures 6.7.1,
6.7.2, `XS002_research.json` figures) but is itself a construction internal feeding XS003.

Shaikh's own statement of the asymmetry (verbatim, book p. 831, `XS002_research.json` definition quote):

> "Consider two firms, one a corporation and the other an unincorporated enterprise … each with a value
> added of $100 million out of which each pays $50 million to regular employees and charges $10 million as
> depreciation, leaving $40 million in each coffer. In the case of the corporation, NIPA accounts would
> record a further $10 million in salaries, bonuses, and certain stock option exercises as part of
> corporate employee compensation, so that the corporate business NOS would be $30 million. But in the
> case of the unincorporated business, NIPA would record all of the value added in excess of regular
> employee compensation (i.e., all $40 million) as personal earnings of proprietors and partners …
> No allowance would be made for the fact that some part of this sum is really the profit of
> unincorporated enterprises."

The construction (`XS002_research.json` formula; source quote book p. 832):

- **σ (sigma) = corporate wage-profit ratio = ECcorp / Pcorp = NIPA T1.14 line 4 ÷ line 11.**
- **WEQ2 = (σ · PropInc − ECprop) / (1 + σ)** — imposes the corporate wage/profit share on the
  noncorporate sector to split proprietors' income.
- **Pnoncorp = PropInc − WEQ2** — the recovered noncorporate profit.
- **WEQ1 (alternative, *not* preferred) = ecpriv · SEP**, where ecpriv = private-sector EC per FTE
  (T6.2/T6.3 line 3) and SEP = self-employed persons (T6.7 line 1).

Canonical worked example (Appendix Table 6.7.4, book p. 832, `XS002_research.json` methodology_notes),
**2009**: PropInc = 979.4; ECpriv = 761.4; SEP = 9,829; ecpriv = 60,920.9; WEQ1 = 598.8; Pnoncorp1 = 380.6;
**σ = 4.76**; **WEQ2 = 677.2**; **Pnoncorp (preferred) = 302.2**. Resulting profit rates: rbus = 7.7%,
rcorp = 7.5%, noncorp via WEQ2 (moncorp) = 8.1%, noncorp via WEQ1 (rnoncorp1) = 10.2%.

Seven chopped subseries (`XS002_DPR.md` Sources table): XS002-A `PropInc`, XS002-B `ECprop`,
XS002-C `WEQ2`, XS002-D `WEQ1`, XS002-E `Pnoncorp`, XS002-F `Pcorpnipa`, XS002-G `s` (sigma).

Appendix location: **Appendix 6.7 Section III + Appendix Table 6.8.I.2, book pp. 831–833.**

> **Sigma "≈3.65" mislabel note (finding F-XS-01 / XS002-G).** The shared brief flags a sigma value
> "~3.65"; the *worked-example* sigma printed in the book for 2009 is **4.76** (Appendix Table 6.7.4,
> p. 832) — sigma varies year to year, so both are legitimate period values, not a contradiction. The
> *actual* XS002 defect is a **units mislabel**: XS002-G `s` is a dimensionless ratio but the chopped
> artifact labels it `billions_current_usd` (`CH_XS_review.json` finding F-XS-01, evidence
> "chopped/XS002.csv XS002-G rows"). See §5.

## 2. Source lineage

All inputs are BEA NIPA at the **2011 vintage** (Appendix 6.7 footnote 1, book p. 828). Line-level lineage
(`XS002_research.json` components; source quote book p. 832):

- **PropInc** — Proprietors' and partnerships' income with IVA and CCAdj — NIPA **T1.13, line 23**.
- **Pcorp** — corporate NOS — NIPA **T1.14, line 11**.
- **ECcorp** — corporate employee compensation — NIPA **T1.14, line 4**.
- **σ (sigma)** — derived: ECcorp / Pcorp = T1.14 line 4 ÷ line 11.
- **ECprop** — employee compensation of proprietorships and partnerships — derived as
  `ECbusnipa (Appendix Table 7.1A) − ECcorpnipa (T1.14 line 4)` (`XS002_research.json` components).
- **SEP** — self-employed persons — NIPA **T6.7, line 1** (thousands of persons; feeds WEQ1 only).
- **ecpriv** — private-sector EC per FTE — NIPA **T6.2 line 3 / T6.3 line 3** (feeds WEQ1 only).

Review touchpoint (`CH_XS_review.json`): kind **NIPA**, "T1.13/T1.14 (proprietor+corp income), T6.2/T6.3,
T6.7; WEQ2 wage-equivalent + corp/noncorp profit split."

Methodological ancestry: closely related to the **Shaikh-Tonak (1994, 304–305)** wage-equivalent
methodology; **Jorgenson and Landefeld (2004, 15)** propose a BLS-style split Shaikh discusses but rejects
in favor of WEQ2 (`XS002_research.json` methodology_notes). Predecessor: **CD2 series S207**
(predecessor_ids.cd2_id = "S207").

## 3. Why these sources, from Shaikh's perspective + rejected alternatives

**Why impute a wage equivalent at all.** NIPA's asymmetry (the $40M-vs-$30M example above) means a
straight comparison of corporate NOS to proprietors' income would treat *all* unincorporated residual
income as if it were labor pay — understating noncorporate profit and biasing the economy-wide profit
rate. Shaikh's classical concept requires that "the full wage/profit share is the same in the two
sectors" (`XS002_research.json` methodology_notes, book p. 832), which he defends as "more reasonable than
NIPA's implicit assumption that all proprietors' income is labor compensation." So he *imports the
corporate wage/profit ratio σ into the noncorporate sector* and lets it partition proprietors' income.

**Why WEQ2 over WEQ1 — the central methodological choice.** Shaikh computes two wage equivalents and
explicitly prefers WEQ2 (verbatim, book p. 833, `XS002_research.json` method quote):

> "WEQ2, on the other hand, yields a much more plausible result. Its corresponding non-corporate rate of
> profit tracks the corporate rate quite closely, but is a bit smaller. … I use WEQ2 in all subsequent
> calculations. Hence, the overall business rate of profit … is defined as the sum of corporate profit and
> the non-corporate profit corresponding to WEQ2, divided by the sum of corporate and non-corporate
> current-cost capital stocks."

The reasoning (`XS002_research.json` methodology_notes):
- **WEQ2** imposes the corporate wage-profit ratio σ directly, producing a noncorporate profit rate that
  "tracks the corporate rate quite closely, but is a bit smaller" (8.1% vs 7.5% in 2009) — economically
  coherent with the premise that similarly-competitive sectors earn similar returns.
- **WEQ1** simply multiplies private-sector EC-per-FTE by the self-employed-persons count. Shaikh rejects
  it because after the 1990s "officer salaries inflate ecpriv," so the WEQ1 noncorporate rate "drifts
  implausibly above the corporate rate" (10.2% vs 7.5% in 2009). A wage equivalent that makes small
  unincorporated businesses *more* profitable than corporations is not believable.

**Rejected alternative — the Jorgenson-Landefeld (2004) BLS-style split.** Discussed and set aside in
favor of WEQ2 (`XS002_research.json` methodology_notes): Shaikh keeps the σ-based split for continuity
with his own Shaikh-Tonak (1994) methodology and because it yields the sector-tracking result he wants.

**Rejected alternative — accept NIPA's convention (all proprietors' income = labor).** This is exactly
what XS002 exists to overturn (p. 831 asymmetry quote); taking NIPA at face value would zero out
noncorporate profit and corrupt the business-sector profit rate.

**Why XS002 keeps *both* WEQ1 and WEQ2 in the chopped output.** Shaikh publishes both (subseries XS002-C
and XS002-D) and both noncorporate rates, so the reader can see *why* WEQ2 is preferred — the WEQ1 drift
is the evidence for the choice, not a discarded scratch calculation.

## 4. Methodological-change exposure

XS002 is NIPA-vintage-coupled and frozen at the **2011 vintage** (footnote 1, p. 828). Exposures per
`NIPA_CHANGE_TIMELINE.md`:

1. **IVA and CCAdj revisions on PropInc (T1.13 line 23) and on corporate NOS (T1.14 line 11).** Both the
   inventory-valuation adjustment and the capital-consumption adjustment are re-estimated at each
   comprehensive revision; a re-pull changes PropInc, Pcorp, and therefore σ, WEQ2, and Pnoncorp
   (`XS002_research.json` extension_candidates concerns: "Vintage drift from CCAdj/IVA methodology
   revisions", "IVA and CCAdj revisions").
2. **2013 Comprehensive Revision (14th).** R&D/entertainment capitalization → IPP re-levels corporate NOS
   and CFC (`NIPA_CHANGE_TIMELINE.md`), moving the σ ratio's denominator (Pcorp). Because σ enters WEQ2
   nonlinearly `(σ·PropInc − ECprop)/(1+σ)`, small σ shifts propagate to the whole split.
3. **2018 Comprehensive Update (15th).** Improved financial-services and nonprofit methods; T1.14 line
   numbering can shift — the EPR concern is explicit: "Line numbering in T1.14 may shift across vintages;
   map by stub label" (`XS002_research.json` extension_candidates). XS002 does **not** yet have a
   T1.14/T1.13 stub-label resolver (unlike XS003's T7.11 resolver), so the mapping discipline is narrated,
   not enforced in code.
4. **2023 Comprehensive Update (16th).** Reference year → 2017; re-bases any extended series.
5. **σ well-definedness boundary.** WEQ2 requires σ = ECcorp/Pcorp to be well-defined; "in years when
   Pcorp is small or negative (none in postwar US but possible internationally), the formula breaks"
   (`XS002_research.json` open_questions). A US book-period extension is safe; any non-US application must
   guard the denominator.

**Anti-splice mandate.** Per `NIPA_CHANGE_TIMELINE.md` §"Why this matters" and `XS002_EPR.md`, extension
re-fetches T1.13/T1.14/T6.x and re-runs the σ/WEQ2/Pnoncorp formula end-to-end on one coherent vintage —
it never appends post-2011 published values to the book series.

## 5. Replication fidelity note

RSCD reproduces XS002 **bit-exact to Appendix 6.8** by the read-the-truth-column pattern: L01 loads the
finished `PropInc`/`ECprop`/`WEQ2`/`WEQ1`/`Pnoncorp`/`Pcorpnipa`/`s` columns from
`Appendix6_Table68*.xlsx`; V03 round-trips at **1.0% tolerance** (`XS002_DPR.md` §Validation Expectation).
Honest limits, disclosed:

- **Transcribed-not-recomputed.** Nominally `construction: formula` (the σ/WEQ2 recipe is fully specified
  in the research JSON), but the runtime path is a **pass-through transcription** — L01 loads finished
  columns; P02 is schema-only. The σ→WEQ2→Pnoncorp recompute exists only in the deferred v1.1 EPR
  extension recipe. This is the group finding **F-XS-05** ("XS003–XS009 declare construction:formula but
  carry components:[]… executable path is pass-through transcription of Appendix 6.8"); XS002 is
  documented `composite` in the DPR header and *does* carry a populated `components` array, but shares the
  same transcribe-don't-recompute runtime reality.
- **Units mislabel — finding F-XS-01 (HIGH).** XS002-G `s` (sigma) is a **dimensionless ratio** but the
  chopped artifact labels it `billions_current_usd` (`CH_XS_review.json` F-XS-01, evidence
  "chopped/XS002.csv XS002-G rows"; D14 gate note names "XS002-G Sigma" among the mislabeled
  dimensionless/rate subseries). The registry triage claims a `units: per_subseries` fix, but the fix
  "lives only in registry metadata" and did not propagate to the chopped CSV consumed by viz/public
  downloads. **This is the sigma "≈3.65 mislabel note"**: the issue is the *unit label on the sigma
  column*, not the sigma value. Must remediate before external distribution (D14 = 85,
  BELOW_90_BLOCKS_EXTERNAL). WEQ1/WEQ2/Pnoncorp/PropInc/ECprop are genuine `billions_current_usd` and are
  correctly labeled.
- **Circular-validation caveat.** V03 confirms melt fidelity to the workbook, not an independent
  re-derivation. The non-circular anchor is the book's printed 2009 line (σ = 4.76, WEQ2 = 677.2,
  Pnoncorp = 302.2, Appendix Table 6.7.4 p. 832).

## 6. Forward risk

- **T1.13/T1.14 stub-label resolver not built.** σ, WEQ2, and Pnoncorp all read T1.14 lines 4/11 and T1.13
  line 23; the "map by stub label" discipline (`XS002_research.json`) is narrated but not wrapped in code
  the way XS003's T7.11 recipe is. Any 2013/2018/2023-vintage extension must first re-derive the
  T1.13/T1.14 line map by caption or the WEQ2 split will silently read the wrong rows.
- **Fix-not-propagated units debt.** The XS002-G sigma mislabel (F-XS-01) must be remediated in the L01
  loader (which "hardcode[s] a single series-level unit string instead of per-subseries units",
  `CH_XS_review.json` F-XS-01 detail) so the chopped artifact carries `dimensionless`/`ratio` on the sigma
  column before any public release.
- **σ denominator guard for non-US extension.** WEQ2 breaks where Pcorp ≤ 0; a guard is required before any
  international application (`XS002_research.json` open_questions).
- **Downstream propagation.** WEQ2 and Pnoncorp feed XS003 (imputed-interest correction applied to
  corrected noncorporate NOS) and thence S603 (noncorporate profit rate); the open question is whether
  S6xx cite XS002 for the WEQ2 methodology or invoke PropInc directly (`XS002_research.json`
  open_questions). A WEQ2 error propagates to every business-sector profit rate.
- **BEA API extension path.** `XS002_EPR.md` re-fetches via `S00_apis.bea_table` (needs `BEA_API_KEY`),
  logs `vintage_year`, and routes drift to documented per-year logging — never silent overwrite of the
  1947–2011 book period.

# NIPA Methodology-Change Compendium

**Canonical NIPA vintage-risk reference for the RSCD replication of Shaikh, *Capitalism* (2016).**

- **Compiled:** 2026-07-01 (RSCD Phase-3 NIPA-synthesis agent)
- **Aggregated from:** the Phase-0 web-verified timeline, the existing T7.11 resolver, and all 16 per-chapter
  methodology JSONs + review JSONs + 118 per-series MHRs. This file does **not** re-derive; it aggregates the
  emitted per-chapter `nipa_touch` records faithfully and cites the underlying artifacts for every claim.
- **Read-with:**
  - `Technical/docs/methodology/_timelines/NIPA_CHANGE_TIMELINE.md` (+ `.json`) — the web-verified comprehensive-revision timeline.
  - `Technical/docs/methodology/NIPA_T711_FISIM_remap.md` — the T7.11 stub-label resolver spec.
  - `Technical/code/L01_loaders/_nipa_t711_line_resolver.py` — the resolver implementation.
  - `Technical/methodology_review/CH*_methodology.json` — per-series `nipa_touch` records (source of the aggregation below).
  - `Technical/docs/methodology/series/*_MHR.md` §4 — per-series methodological-change exposure.

---

## 1. Executive summary

**How many RSCD series touch NIPA.** Of the 118 RSCD series, **110 carry a `nipa_touch` record** in the
per-chapter methodology JSONs. Of those, **38 series draw on concrete BEA NIPA / Fixed-Asset tables**; the
other **72** recorded an explicit *no-NIPA-exposure* disposition (`NONE` / `NOT APPLICABLE` — BLS/CPS labor
statistics, IMF/PWT foreign series, Jastram/gold-price series, closed-form theoretical illustrations, or
pre-modern-NIPA frozen compilations), or an *indirect* tie through a pre-computed column (e.g. MeasuringWorth's
BEA leg). Counts verified by scanning `methodology_review/CH*_methodology.json` for the `nipa_touch` field.

**Which chapters.** Concrete NIPA exposure concentrates in:
- **Ch6 "Capital and Profit"** (S601–S604) and its **XS-appendix construction internals** (XS001–XS009) — the
  densest NIPA user in the book (T1.14, T7.11, and the entire Fixed-Asset T6.x family).
- **Ch10 "Competition, Finance, and Interest Rates"** (S1007, S1008) — three NIPA tables simultaneously plus
  the T7.11 monetary-interest magnitude, with forward-recursion compounding.
- **Ch14 "Modern Money / distribution"** (S1401, S1403–S1408) — the T1.10 income-side account (compensation, GDP, CFC, NOS).
- **Ch15 "Modern Money and Inflation"** (S1504–S1507) — T1.1.4/T1.1.5 deflator+GDP, T5.3.5 investment, T1.16 NOS, T4.1 current account.
- Scattered T7.11/T7.12 touchpoints in **Ch2, Ch3, Ch7, Ch9, Ch16**.

**Headline vintage risk.** Shaikh froze all BEA data at the **~2011 vintage** (Appendix 6.7 footnote 1, p.828).
Every BEA comprehensive revision *after* 2011 reclassifies magnitudes and, in 2018, **renumbers NIPA table
lines**. The three principal forward hazards are:

1. **2013 (14th) comprehensive update** — R&D + entertainment/artistic originals capitalized into the new
   **Intellectual Property Products (IPP)** category (≈ **+$400B to GDP**), which **raises Fixed-Asset /
   capital-stock levels and restates NOS/CFC**. Shaikh's 2011 concept *excludes* IPP, so this is a
   **concept discontinuity**, not a mere level nudge.
2. **2018 (15th) comprehensive update** — inserted a new monetary-interest sub-row in **T7.11**, producing a
   **+1 line shift** for every subsequent line: a hard-coded-line-number **time-bomb** for Shaikh's FISIM recipe.
3. **T7.11 renumbering** as the canonical renumbering event (plus the 2023 reference-year → 2017 rebasing that
   moves every deflator level).

**The replication rule that falls out of this:** never splice a Shaikh series across a comprehensive-revision
boundary; any live extension must be re-computed **end-to-end on one coherent vintage**, with T7.11 (and any
other renumbering-prone table) resolved by BEA `LineDescription` **stub label**, not by line number.

**The three highest-risk NIPA exposures** (detailed in §3–§5): (a) the **T7.11 FISIM line renumbering**, the
most-touched table and a genuine renumbering time-bomb, load-bearing for Ch6 profit rates and Ch10's
forward-recursion; (b) the **already-confirmed Ch14 T1.10 wage-share numerator defect** (F1, HIGH) — a live
extension bug, not merely latent risk; (c) the **2013 IPP capitalization of the Fixed-Asset denominator**
(GPIM, Ch6/XS004–XS009) — a concept change that silently re-defines "corporate fixed capital."

---

## 2. The NIPA comprehensive-revision timeline (web-verified)

Reproduced from `_timelines/NIPA_CHANGE_TIMELINE.md` (every row cites a bea.gov / apps.bea.gov source; that file
is the authority — cite it rather than re-researching). BEA counts 16 comprehensive updates through 2023; the
modern set (1999–2023) is what bears on Shaikh's 2011-vintage construction and any extension.

| Date | Revision | Key changes | RSCD series families affected |
|------|----------|-------------|-------------------------------|
| **1999-10-28** | 1999 Comprehensive (11th) | **Software capitalized** as fixed investment; full switch to chain-type (Fisher) indexes + updated reference year; gov consumption/investment split | Fixed Assets, private fixed investment (equipment & software), chain-type indexes |
| **2003-12** | 2003 Comprehensive (12th) | Revised **implicitly-priced banking services (FISIM / reference-rate)** and property-casualty insurance; own-account software; new/redesigned tables | Corporate profits (financial vs nonfinancial), **FISIM / imputed interest (T7.11 family)**, PCE financial services |
| **2009-07-31** | 2009 Comprehensive (13th) | Incorporated **2002 benchmark I-O**; definition/classification/method/presentation changes | GDP-by-industry, investment, NIPA–IO integration |
| **2013-07-31** | 2013 Comprehensive (14th) | **R&D capitalized**; **entertainment/literary/artistic originals capitalized → new IPP category**; accrual accounting for DB pensions; expanded residential ownership-transfer costs; 2007 benchmark I-O; **FISIM restatement by sector. ≈ +$400B to GDP.** | GDP, private fixed investment (new IPP), **corporate profits, NOS/CFC, Fixed-Asset / capital-stock LEVELS RISE**, personal income & saving (pensions), **T7.11 magnitudes** |
| **2018-07-27** | 2018 Comprehensive (15th) | Incorporated **2012 benchmark I-O**; improved financial-services & nonprofit methods; personal-saving revisions. **Inserted a new monetary-interest sub-row in T7.11 → +1 line shift.** | GDP-by-industry, personal saving, **financial services (FISIM), T7.11 line numbering** |
| **2023-09-28** | 2023 Comprehensive Update of the National Economic Accounts (16th) | First **harmonized** NIPA + Industry-Economic-Accounts release; **2017 benchmark supply-use/I-O**; **reference year → 2017**; 2017-NAICS effects small | GDP (**reference year → 2017**), GDP-by-industry / supply-use, **chain-type deflator levels**, NIPA–IEA harmonization |

**Authoritative URLs** (from the Phase-0 timeline's Sources block):
- BEA — Information on previous updates of the National and Regional Economic Accounts — https://www.bea.gov/information-previous-updates-nipa-regional-accounts
- BEA — NIPA Handbook (Concepts and Methods) — https://www.bea.gov/resources/methodologies/nipa-handbook
- BEA SCB (Aug/Nov 1999) — 1999 Comprehensive Revision — https://apps.bea.gov/scb/pdf/national/nipa/1999/0899niw.pdf · https://apps.bea.gov/scb/pdf/national/NIPA/1999/1199gdp.pdf
- BEA SCB (Mar 2013) — Preview of the 2013 Comprehensive Revision — https://apps.bea.gov/scb/pdf/2013/03%20March/0313_nipa_comprehensive_revision_preview.pdf
- BEA FAQ 1024 — 2013 comprehensive revision changes — https://www.bea.gov/help/faq/1024
- BEA blog (2013-07-23) — R&D and entertainment capitalization — https://www.bea.gov/news/blog/2013-07-23/comprehensive-revisions-nipa-reconsidering-treatment-rd-and-entertainment
- BEA SCB (Apr/Sep 2018) — 2018 Comprehensive Update — https://apps.bea.gov/scb/issues/2018/04-april/0418-preview-2018-comprehensive-nipa-update.htm · https://apps.bea.gov/scb/issues/2018/09-september/0918-nipa-update.htm
- BEA SCB (Jun 2023) + Information page — 2023 Comprehensive Update — https://apps.bea.gov/scb/issues/2023/06-june/0623-nea-preview.htm · https://www.bea.gov/information-updates-national-economic-accounts-2023

**Table-renumbering / silent-break events** (the RSCD time-bombs, from the same file):
1. **T7.11 — 2018 +1 line shift.** Shaikh's Appendix 6.7.11 / XS003 recipe uses 2011-vintage lines
   `4, 28, 44, 52, 53, 54, 73, 74, 75, 91`; on a 2018+ vintage these become
   `4, 29, 45, 53, 54, 55, 74, 75, 76, 92` (line 4 unchanged). Vintages 2011–2017 share the 2011 numbers;
   2019–2024 share the 2018 numbers.
2. **T7.11 — 2013 FISIM magnitude restatement.** Row *order unchanged*, per-row magnitudes changed — same
   captions, different values across the 2013 boundary. Do not splice.

---

## 3. Per-table exposure map

Aggregated from the `nipa_touch.tables` fields across `methodology_review/CH*_methodology.json`. Vintage-sensitivity
key: **RENUM** = line-renumbering (hard-coded-line time-bomb) · **LEVEL** = magnitude/level restatement across a
comprehensive revision · **CONCEPT** = concept-change (what the row *measures* changes) · **REBASE** = deflator
reference-year rebasing (2023 → 2017).

| NIPA table (line focus) | RSCD series that depend on it | Chapters / group | Vintage sensitivity | Book-frozen or live? |
|---|---|---|---|---|
| **T7.11** — interest paid/received by sector (FISIM) | S213, S216, S301, **S601–S604**, S705, S706, S709, S901–S903, **S1007, S1008**, S1505, S1604, **XS003, XS004, XS005, XS006, XS007, XS008, XS009** | Ch2, Ch3, Ch6, Ch7, Ch9, Ch10, Ch15, Ch16, XS | **RENUM (2018 +1)** + LEVEL (2013 FISIM restatement) | Book-frozen at 2011; **resolver mandatory** for any extension |
| **Fixed Assets T6.1–T6.8** (net stock, chain deflators, gross investment, depreciation) | **S601–S604**, **XS004, XS005, XS006, XS007, XS008, XS009** (GPIM internals) | Ch6, XS | **CONCEPT (2013 IPP raises capital levels)** + REBASE (2023) | Book-frozen at 2011; extension must take an explicit IPP stance |
| **T1.14** — corporate GVA, profits (Pcorp), employee comp | S601–S604, **S1007, S1008**, XS002 | Ch6, Ch10, XS | LEVEL (2013 NOS/CFC/profits +$400B) | Book-frozen; NOS numerator |
| **T1.10** — GDP by income (compensation, T&I-net-subsidies, CFC, NOS residual) | **S1401, S1403, S1404, S1405, S1406, S1407, S1408**, XS001 | Ch14, XS | LEVEL (2013 IPP moves NOS residual) | **Live extension (Ch14 wage share) — ACTIVE F1 defect** |
| **T7.12** — imputations in the personal/business income accounts | S705, S902, XS001, XS003 | Ch7, Ch9, XS | RENUM (no stub-label resolver yet) + LEVEL | Book-frozen; **resolver gap flagged** |
| **T1.1.4 / T1.1.5** — real GDP / GDP price & quantity indexes | S1504, S1505, S1506, S1507 | Ch15 | REBASE (2023 → 2017) + LEVEL (2013) | Live extension candidate; growth-rates robust, levels not |
| **T5.2.3 / T5.6.3** — real / historical-cost private fixed investment | S1007, S1008 | Ch10 | LEVEL (2013/2018) + REBASE (2023) | Extension **deferred** pending vintage pin |
| **T5.3.5** — gross government / private investment (current $) | S604, S1505 | Ch6, Ch15 | LEVEL + REBASE | Book-frozen / deferred |
| **T1.16** — net operating surplus (private enterprise income) | S1505, S1506, S1507 | Ch15 | **RENUM (line-2 restructured — resolve by label)** + LEVEL (2013 NOS) | Live extension candidate; **T7.11-family time-bomb** |
| **T1.1.9** — implicit price deflator / gross investment index | S202, S1007, S1008, S1406, S1407, S1408 | Ch2, Ch10, Ch14 | REBASE (2023 → 2017) | Mixed; deflators robust as growth rates |
| **T4.1** — foreign transactions / current account (line 29) | S1504 | Ch15 | LEVEL + REBASE | Live extension candidate |
| **T6.2 / T6.3 / T6.5 / T6.7** — employment, comp-per-FTE, gross investment | XS002, S1406–S1408 | Ch14, XS | LEVEL + CONCEPT (FTE scope) | Book-frozen |
| **T1.13** — national income by sector (proprietors' income) | XS002 | XS | LEVEL (2013 IPP/pensions) | Book-frozen |
| **T1.7.5** — GDP, GNP, national income reconciliation (lines 1, 15) | XS001 | XS | LEVEL | Book-frozen |
| **T2.1** — personal income & its disposition | S1605 | Ch16 | LEVEL + REBASE | Book-frozen |

*72 further series carry a `nipa_touch` record that is explicitly `NONE` / `NOT APPLICABLE` / indirect and are
therefore out of the vintage-drift blast radius (BLS/CPS labor statistics, PWT/IMF/OECD foreign aggregates,
Jastram/MeasuringWorth gold-and-price series, closed-form theoretical illustrations such as S1301, and pre-modern-NIPA
frozen compilations). See the per-chapter JSONs for the individual dispositions.*

---

## 4. Case study — the T7.11 FISIM line-shift and its generalization

### 4.1 The canonical pattern (already built)

Shaikh's Appendix Table 6.7.11 (book p.842) defines the imputed-interest adjustment that reverses NIPA's
bank-as-business FISIM treatment back to the classical accounting concept, in **CD2 2011-vintage T7.11 line
numbers** (`NIPA_T711_FISIM_remap.md`; implemented in `code/L01_loaders/_nipa_t711_line_resolver.py`):

```
BankNetIntPaid  = T7.11(L4  + L44 + L73) - T7.11(L28 + L52 + L91)
NFNetImpIntPaid = T7.11(L74 + L75)       - T7.11(L53 + L54)
BusImpIntAdj    = -BankNetIntPaid - NFNetImpIntPaid
```

The 2018 comprehensive update inserted one monetary-interest sub-row, shifting **every line ≥ 28 by +1**
(line 4 unchanged): `28→29, 44→45, 52→53, 53→54, 54→55, 73→74, 74→75, 75→76, 91→92`. The 2013 update did **not**
reorder rows but **restated the magnitudes** — same captions, different values.

**The resolution — the pattern to generalize.** Do **not** re-hard-code new line numbers (that just moves the
time-bomb to the next revision). Instead map each of the 10 line numbers to a persistent **BEA stub label** (the
row caption BEA preserves across vintages) and resolve to the live line at fetch time. The resolver
(`_nipa_t711_line_resolver.py`) exposes:

```python
resolve_t711_line(historical_line_num, vintage_year) -> stub_label
stub_label_to_current_line(stub_label, current_vintage) -> int | None
compute_AS003_recipe(t711_values_by_stub, current_vintage) -> {BankNetIntPaid, NFNetImpIntPaid, BusImpIntAdj}
fetch_t711_via_api(year, vintage_year)   # keys BEA-API rows by LineDescription, bypassing line drift entirely
```

Pinned vintages: **2011** (source of truth), **2018**, **2024**; intermediate vintages fall back to the nearest
pinned vintage with a logged warning. If a future BEA revision *splits or merges* one of the 10 captioned rows,
the resolver **raises** on lookup and the loader must surface `data_unavailable` rather than silently absorbing
the break (`NIPA_T711_FISIM_remap.md` Caveats; resolver docstring). This raise-don't-absorb behavior is the
correct default for the whole renumbering-prone family.

### 4.2 Where the shift compounds

- **Ch10 forward recursion (S1007 → S1008).** S1007's adjusted rate of profit adds back the T7.11
  "monetary interest paid by the nonfinancial sector" — exactly a FISIM magnitude subject to the +1 shift
  (`S1007_MHR.md` §4; `CH10_methodology.json` S1007 `nipa_touch`/`forward_risk`). S1008's warranted-price path
  `prweq` is a **forward recursion in S1007's `rI`** (eq. 10.31), so **any S1007 vintage break accumulates down
  the entire warranted-price path**. Fix S1007 first; keep `BOOK_ADJ=6.75` pinned; both extensions are currently
  **deferred to Phase 6** pending vintage pinning + the exact monetary-interest line lookup.
- **Ch6 / XS GPIM numerator.** The corrected NOS = P + NMINT that feeds every Ch6 profit rate (S601–S604) runs
  the same T7.11 recipe through XS003; XS004–XS009 inherit the +1 shift via the post-1947 XS004/XS003 baseline
  even where their own inputs are Fixed-Asset tables (`CHXS_methodology.json` XS003/XS004 `nipa_touch`).
- **Ch15 σ denominator (T1.16).** S1505's σ is a ratio of two revised levels; T1.16 line-2 "Net Operating Surplus"
  was itself **restructured** and must be re-verified by `LineDescription` label before extending — an
  **explicit member of the T7.11 renumbering family** (`CH15_methodology.json` S1505; review F-nn).

### 4.3 The unresolved sibling — T7.12

XS001 (business NOS) and XS003 also draw on **T7.12** owner-occupied-housing and imputed-interest lines
(133–140; 43–44), for which **no stub-label resolver has been coded** — the mapping is narrated but not
implemented (`CHXS_methodology.json` XS001 `forward_risk`: "No T7.12 OOH stub-label resolver yet … 2013/2018/2023
vintage line drift"). This is the first generalization target of §6.

---

## 5. Vintage-drift risk register (per revision)

| Revision | RSCD series / concepts that change | What the replication must do |
|---|---|---|
| **2013 (14th) — R&D/IPP capitalization, ≈+$400B, FISIM restatement** | **Fixed-Asset/capital-stock levels rise** (S601–S604, XS004–XS009 GPIM denominator); **NOS/CFC/profits restated** (T1.14 → S601–S604, S1007/S1008; T1.10 NOS residual → Ch14, XS001); T7.11 magnitudes restated (same rows); Ch15 σ denominator (T1.16 NOS). **Shaikh's 2011 concept EXCLUDES IPP** → this is a *concept discontinuity*. | **Never splice across the 2013 boundary.** A live GPIM re-pull must take an explicit stance on IPP (Shaikh's definition excludes it); re-derive NOS and the capital denominator end-to-end on one post-2013 vintage. `CH06_review.json` L4 flags the drift-handling as *untested* (no extension built). |
| **2018 (15th) — 2012 benchmark I-O + T7.11 +1 line shift** | **T7.11 line renumbering** hits every FISIM user (Ch2/3/6/7/9/10/15/16 + XS003–XS009); financial-services & nonprofit method changes | Resolve T7.11 (and T1.16, T7.12) by **BEA `LineDescription` stub label**, never by line number; use `_nipa_t711_line_resolver.py`; on an unmapped row-split, raise → `data_unavailable`, never silently absorb. |
| **2023 (16th) — 2017 benchmark supply-use, reference year → 2017** | **Every deflator re-bases** (T1.1.4/T1.1.9 → Ch10 S1007-A real conversion, Ch14 GDPDEF productivity/inflation, Ch15 π); chain-index levels under Fixed-Asset tables shift | Growth-rate concepts (log-differences: gGDP, π, productivity growth) are *robust* to rebasing, but any series carrying a **level** (S1504 pp denominator, S1007 real conversion) must re-derive on one coherent 2017-based vintage; never mix a 2009-based book level with a 2017-based extension. |
| **1999 / 2003 / 2009 (11th–13th)** | Pre-2011 comprehensive revisions — **subsumed in Shaikh's 2011 frozen vintage**; matter only for the *provenance* of the book numbers (software capitalization 1999; FISIM/insurance 2003; 2002 benchmark I-O 2009) | No action for book-period replication (data are already 2011-vintage). Relevant only if a re-derivation reaches back before Shaikh's own inputs. |

**The universal rule:** for any series in the §3 map that extends live, fetch every NIPA input on **one coherent
vintage**, resolve renumbering-prone rows by label, and **recompute end-to-end** — the replication must never
concatenate a book-vintage segment with a post-revision segment across a 2013 / 2018 / 2023 boundary
(`NIPA_CHANGE_TIMELINE.md` "Why this matters"; CH6/CH7 open-question 5; every affected MHR §4).

**Active (not merely latent) defect on this axis — Ch14 F1 (HIGH).** The S1401 wage-share extension fetches the
**wrong FRED series** — `A576RC1` (wages & salaries) instead of `W209RC1` (total compensation of employees =
T1.10 line 2) — producing a spurious **~22% wage-share break at 2011→2012** (`CH14_review.json` F1;
`CH14_methodology.json` S1401 `nipa_touch`/`forward_risk`). This is a confirmed, D14-FAILing bug, not a hypothetical.
Remedy: swap `A576RC1 → W209RC1`, add a wage-share-numerator concept-guard (analogous to the exemplary per-hour
guard, F8), and re-derive on one coherent vintage at the next compensation re-benchmark.

**Other open review findings touching this axis:** `CH15` F11 (S1504 GDP agency ambiguity IMF-IFS vs NIPA
T1.1.5; plus the book's "Table 1.15" typo for T1.1.5); `CHXS` F-XS-05 (XS003/XS004 declare `construction:formula`
but transcribe values — the end-to-end recompute exercising `compute_AS003_recipe` is deferred to the v1.1 EPR);
`CH17` F-ch17-02 (NIPA touchpoint mis-tagged for S1702/S1703).

---

## 6. Recommendations

1. **Pin every live NIPA fetch to an ALFRED vintage.** No RSCD series currently carries an ALFRED vintage pin;
   the Ch10 (S1007/S1008), Ch14 (S1401, S1406–S1408) and Ch15 (S1504–S1507) extension candidates are current-vintage
   FRED mirrors that straddle all three comprehensive boundaries (`S1007_MHR.md` §4; per-chapter `forward_risk`).
   Any extension loader should fetch via a pinned ALFRED vintage (or BEA Data API with `vintage_year` logged) and
   record `vintage_year` in provenance — this is the precondition for un-deferring S1007/S1008.

2. **Generalize the T7.11 stub-label resolver beyond T7.11.** The `_nipa_t711_line_resolver.py` pattern
   (label catalog → pinned per-vintage line index → `LineDescription`-keyed API fetch → raise-on-row-split) is the
   canonical defense against renumbering. Extend it to the other renumbering-prone tables now identified in the
   §3 map, in priority order:
   - **T7.12** (XS001 OOH lines 133–140, XS003 lines 43–44) — narrated but *uncoded* today; the top gap.
   - **T1.16** (Ch15 σ denominator, line-2 NOS "restructured") — resolve line-2 by label before extending σ.
   - **T1.10** (Ch14 income-side) — a label-keyed fetch would have prevented the F1 wage/compensation mix-up.
   Follow the resolver's own "How to update when BEA publishes a new revision" procedure (add a new pinned vintage
   row; never edit existing pinned vintages).

3. **Enforce anti-splice mechanically, not just in prose.** The no-splice-across-comprehensive-revision rule is
   currently documentation-only for most series (cf. `CH9-F4`, `CH6-L4` untested drift handling). Wire a
   validation check that fails any extension concatenating segments whose source vintages cross a 2013/2018/2023
   boundary, and have renumbering-resolvers surface `data_unavailable` on a row split rather than absorbing it.

4. **Gate these extensions on the above.** Explicitly **blocked pending vintage-pinning + label resolution:**
   S1007 and S1008 (deferred to Phase 6; S1008 blocked behind S1007's forward recursion); the Ch6 GPIM /
   XS003–XS009 end-to-end recompute (F-XS-05, deferred to v1.1 EPR); the Ch15 σ extension (T1.16 label
   re-verification). **Fix-first, un-block regardless of extension:** the Ch14 F1 T1.10 wage/compensation swap —
   it corrupts the *published* wage-share series today.

---

*Compiled read-only. This compendium aggregates the emitted per-chapter `nipa_touch` records and cites their
source artifacts; it introduces no new NIPA claims beyond what those artifacts and the web-verified Phase-0
timeline already establish.*

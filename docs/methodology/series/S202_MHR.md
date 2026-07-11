# S202 — US Real Investment Index — Methodological History Report (MHR)

**Group:** ch2 (Turbulent Trends and Hidden Structures) · **Construction:** composite · **Status:** book_period_validated
**Figure:** 2.2 · **Predecessor:** CD/CD2 S002 · **Publish:** true · **Book period:** 1832–2010 · **Extension:** 2011–2025
**Reasoning stance:** from Shaikh's own perspective — why *he* built the series this way.

> Grounding note: every author-intent claim below is anchored to a citable path — the research JSON
> (`Technical/research/S202_research.json`), the DPR/EPR (`Technical/docs/series/S202_{DPR,EPR}.md`),
> the book KB (Body_Text `ch02_turbulent_trends.md`, Figure `ch02_fig_2.2.md`), the CH2 review
> (`Technical/methodology_review/CH02_review.json`, incl. touchpoint note), and the Phase-0 NIPA timeline
> (`Technical/docs/methodology/_timelines/NIPA_CHANGE_TIMELINE.md`). Where a rationale is not present in the
> corpus it is marked **"author rationale not located in corpus."**

---

## 1. What the series is

S202 is the annual **US Real Investment Index, 1832–2010**, plotted **log-scale** as **Figure 2.2**, the second
leg of Shaikh's Chapter-2 growth trio. It measures **real nonresidential business investment in fixed capital
(equipment + structures, excluding housing)**, rebased to **1958 = 100** (`S202_DPR.md` §1, §6). Shaikh's
analytical point is that investment is *more turbulent than output*: the book text (p. 56, KB
`Body_Text/ch02_turbulent_trends.md` lines 18–21; `S202_research.json` book_quotes[0], role=definition) reads —

> "Finally, it is obvious that growth is always turbulent, and that the path of investment is far more turbulent
> than that of output. Any adequate theory of growth must address patterns such as these."

The KB figure caption (`Figures/ch02/ch02_fig_2.2.md`) confirms the ~178-year span (1832–2010), the log y-axis
(1→10,000), and the observation that investment "has a higher average rate of growth (slope) in earlier epochs"
and is "far more turbulent than that of output."

The authoritative source line is **Appendix 2.1 (book p. 763)**, transcribed verbatim in
`S202_research.json` book_quotes[1] (role=source, verbatim_check=true):

> "Figure 2.2 US Real Investment Index, 1832–2010. Investment in Fixed Nonresidential Business Capital,
> 1832–1975 (1970 = 100) from BEA (1977, table B4) and 1901–2010 from BEA, Wealth Table 4.8, line 1 at
> http://www.bea.gov/iTable/index_FA.cfm. The two series were rebased to 1958 = 100 and spliced at 1901."

## 2. Source lineage

| Subseries | Coverage | Agency / table | Native units | Retrieval |
|---|---|---|---|---|
| **S202-A** | 1832–1975 | **BEA (1977), *Fixed Reproducible Tangible Wealth of the US, 1925–1975*, Table B4** — Investment in Fixed Nonres. Business Capital | Index 1970=100 | Salvaged chopped `Appendix2_RealInvestmentUS_1832-2010.xlsx` col `RealInvest1` |
| **S202-B** | 1901–2010 | **BEA Fixed-Asset Wealth Table 4.8, line 1** (Investment in Fixed Nonresidential Capital) | Constant dollars (2011 access vintage) | Salvaged chopped col `RealInvest2` |
| **S202-C** | 2011–2025 | **BEA NIPA Table 1.1.6, line 9** (Real Nonresidential Fixed Investment) | Billions of chained 2017$ | BEA iTable API |

**Exact chain (Appendix 2.1 p. 763 + `S202_DPR.md` §4):**

```
BEA (1977) Table B4 [1832–1975, native 1970=100]  → rebase to 1901=100
BEA FA Wealth Table 4.8 line 1 [1901–2010, constant $] → rebase to 1901=100
SPLICE at 1901: BEA-1977 for 1832–1900, BEA-Wealth for 1901–2010
    → re-anchor the spliced series to 1958=100
BEA NIPA T1.1.6 line 9 [2011–2025, chained 2017$] → reindex at 2010 overlap → append
```

Agency source-methodology grounding: BEA Fixed-Assets documentation
`SalvagedInputs/methodology_library/D_data_methodology/WL-D-FA-00{2,3}__BEA-Fixed-Assets.pdf` and
`WL-D-FA-00{4,5}__BEA-Fixed-Assets.html`; the NIPA extension touchpoint is documented in
`WL-D-NIPA-*__BEA-NIPA.pdf`. The pre-1925 back-cast in BEA (1977) Table B4 draws on historical-capital
compilations in the lineage of `WL-D-HistCap-00{3,4}_libgen.pdf` / `WL-D-HSUS-*__Census-HSUS`.

**Note on subseries labelling (concept, not a mislabel):** despite the Appendix wording "Investment in Fixed
… Capital," the underlying BEA (1977) / Wealth-Table series is an investment-flow index into fixed
nonresidential capital; the DPR treats it as equipment + structures excluding housing (`S202_DPR.md` §1;
`S202_research.json` methodology_notes[2]).

## 3. Why these sources, from the author's perspective

**The concept Shaikh measures.** Real fixed *business* investment — the accumulation flow whose turbulence,
larger than output's, is the chapter's thesis (book p. 56). The US-focus meta-rationale (book p. 56, KB
`Body_Text/ch02_turbulent_trends.md` lines 6–9) again governs: "I will often use the United States … because it
generally has the best available data."

**Why BEA (1977) *Fixed Reproducible Tangible Wealth* for the historical half.** It is the standard long-run
BEA compilation of US fixed-capital investment reaching back to 1832, native 1970=100 (Appendix 2.1 p. 763).
Shaikh names it directly; the extracted corpus contains no discussion of rejected historical investment series
(e.g. Kuznets/Gallman capital-formation estimates) — **author rationale for the historical-source choice is not
located in corpus** beyond the Appendix 2.1 naming.

**Why BEA Fixed-Asset Wealth Table 4.8 line 1 for the modern half.** It is the continuously-maintained BEA
fixed-nonresidential investment series, concept-matched to the historical half, spliced at 1901 where the two
overlap (Appendix 2.1; `S202_research.json` methodology_notes[0]).

**Why BEA NIPA T1.1.6 line 9 for the extension — and the explicit rejection of FRED GPDIC1 (the key
rationale).** This is the one place in the S202 corpus where a rejected alternative is documented with reasons.
`S202_research.json` extension_candidates[0].concerns states: *"GPDIC1 includes residential investment; Shaikh's
series is nonresidential business capital only. Prefer BEA NIPA Table 1.1.6 line 9 (Nonresidential fixed
investment) for a concept match."* The DPR §7 caveat 1 records this as a deliberate **anti-proxy** decision:
"Phase 4 substitution avoided: FRED GPDIC1 includes residential investment (silent proxy). BEA NIPA T1.1.6 line
9 is the concept-correct extension." The CH2 review promotes this to a formal touchpoint
(`CH02_review.json` touchpoints → S202: "BEA NIPA T1.1.6 line 9 (nonresidential fixed investment) extension
preferred over FRED GPDIC1 to avoid residential inclusion (concept-correct)"). CD2's S002 also identified GPDIC1
as a fallback but acknowledged the residential-inclusion concept mismatch (`S202_research.json`
methodology_notes[1]) — RSCD resolves it toward the concept-exact NIPA line.

## 4. Methodological-change exposure

S202 is the **NIPA/Fixed-Asset-exposed** member of the trio — both its modern book half (Wealth Table 4.8) and
its extension (NIPA T1.1.6 line 9) sit inside BEA's product/asset accounts, which the comprehensive revisions
restate. Key exposures from `NIPA_CHANGE_TIMELINE.md`:

- **2013 Comprehensive Update (14th) — the capital-stock uplift (KEY).** R&D and entertainment/literary/artistic
  originals were **capitalized** as fixed investment → new **Intellectual Property Products (IPP)** category;
  ≈ **+$400B** to GDP; and, critically for S202, **"Fixed Assets / capital-stock levels rise"**
  (`NIPA_CHANGE_TIMELINE.md` 2013 row; incorporated the 2007 benchmark I-O). Any post-2013 fetch of nonresidential
  fixed investment (T1.1.6 line 9) is on a *higher* IPP-inclusive concept than Shaikh's 2011-vintage series —
  a genuine concept discontinuity, not just a re-basing. The extension therefore **must not be spliced across the
  2013 boundary**; re-anchoring at the 2010 overlap on a single coherent post-2013 vintage is the only correct
  handling (`NIPA_CHANGE_TIMELINE.md` §"Why this matters"; `S202_DPR.md` §7 caveat 2 — "BEA's 2011 access vintage
  of Wealth Table 4.8 may differ from current BEA data; we preserve Shaikh's pulled values").
- **2018 Comprehensive Update (15th).** Incorporated the **2012 benchmark I-O**; the T7.11 +1 line shift affects
  the FISIM block — **not directly S202's T1.1.6 line 9**, but a reminder that NIPA line numbers are not
  vintage-stable, so any hard-coded line reference must be resolved by BEA `LineDescription`, not position.
- **2023 Comprehensive Update (16th).** Reference year → **2017**, 2017 benchmark supply-use I-O; shifts the
  chained-dollar level of T1.1.6 (base 2017$), absorbed by overlap-anchor reindex.
- **1999 revision** originally capitalized software; **2013** added R&D/IPP — the cumulative effect is that
  "nonresidential fixed investment" is a *broader* concept in every post-book vintage than in Shaikh's 2011 pull.

**I-O touchpoint:** indirect — Fixed-Asset levels incorporate successive benchmark I-O accounts (2002→2007→2012
→2017; `IO_CHANGE_TIMELINE.md`). **Concordance dependency:** the 1832–1901 back-cast rests on historical-capital
compilations whose industry basis predates SIC/NAICS; no live concordance is exercised in the book period.
**NIPA dependency:** direct, on the extension side (T1.1.6 line 9).

## 5. Replication fidelity note

- **RSCD reproduces the book recipe from Shaikh's own retrieved columns.** The 1832–1975 half reads salvaged
  chopped `RealInvest1`, the 1901–2010 half reads `RealInvest2`; both are rebased to 1901, spliced at 1901, and
  re-anchored to 1958=100 exactly as Appendix 2.1 specifies (`S202_DPR.md` §4). Expected MAE < 0.5% vs the
  salvaged book truth (`S202_DPR.md` §9). The 2011 access vintage of Wealth Table 4.8 is deliberately preserved
  rather than re-pulled, so the book segment is byte-faithful to what Shaikh plotted (`S202_DPR.md` §7 caveat 2;
  open question in `S202_research.json`: "Verify that BEA's Fixed-Asset Wealth Table 4.8 line 1 has the same
  definition in 2026 as it did in 2011 (CD2 accessed it 9/2/2011)").
- **The extension is concept-exact by construction** (T1.1.6 line 9, not GPDIC1) — the anti-proxy decision in §3
  is the fidelity guarantee that the post-2010 segment measures the *same* nonresidential concept as the book
  series (`S202_EPR.md` §3, "No-Proxy disclosure").
- **No synthetic fill:** BEA-API NaN propagates; overlap-year NaN triggers walk-back (2010→2009→…→2006) then a
  hard fail — never a silent splice on the wrong year (`S202_EPR.md` §2/§4/§5). API-key absence → publish book
  period only, stamped `extension_status: api_key_missing`.
- **No CH2-review findings against S202.** The HIGH/MED findings target S203 (F-01/F-04) and S214 (F-02); S202's
  only appearance in the review is as the positive NIPA touchpoint exemplar.
- **CD2 divergence** is reported informationally only (different extension anchor/vintage) and never causes a
  V03 FAIL (`S202_EPR.md` §6).

## 6. Forward risk

- **Next BEA comprehensive update re-scopes fixed investment again.** The 1999→2013 trajectory shows the
  "nonresidential fixed investment" concept has been *widened* twice (software, then R&D/IPP); a post-2023
  benchmark will likely widen or re-weight it again, raising levels. Because the extension re-fetches the whole
  post-book segment and re-anchors at 2010, a widening is absorbed at the *ratio* level — but the extended
  segment will silently be on a broader concept than the 1832–2010 book series. This is the structural limit of
  extending a pre-2013 investment series with post-2013 NIPA data; the honest handling is to freeze the book
  series at 2010 and treat the extension as concept-drifting, re-computed on one coherent vintage
  (`NIPA_CHANGE_TIMELINE.md` §"Why this matters").
- **T1.1.6 line-number instability.** Line 9 is not guaranteed vintage-stable across comprehensive updates
  (cf. the T7.11 +1 shift precedent); the loader must resolve by BEA `LineDescription` ("Nonresidential"), not
  by hard-coded position, or a future re-numbering silently reads the wrong line.
- **BEA (1977) Table B4 non-recoverability.** The 1832–1900 segment exists only in Shaikh's salvaged chopped
  column (BEA 1977 is a print volume); it can never be re-verified against a live BEA endpoint. Preserved at
  `SalvagedInputs/book_data/ShaikhChoppedTables/Appendix2_RealInvestmentUS_1832-2010.xlsx`.
- **Wealth Table 4.8 definitional drift** (open question, `S202_research.json`): confirm the 2026 Table 4.8 line 1
  still carries the 2011-vintage definition before any re-pull; if BEA has restructured the Fixed-Asset tables,
  the overlap anchor must be re-validated.

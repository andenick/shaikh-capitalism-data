# S901 — Methodological History Report (MHR)

**Series**: S901 — Market Prices vs Direct Prices (71-order 1947–1972 / 65-order 1998 IO)
**Chapter**: 9 (Competition and Inter-Industrial Relative Prices) · **Group**: ch9 / CH09
**Perspective**: authored *from Shaikh's perspective* — why he built this object the way he did.
**Authored**: 2026-06-30 · **Read-only provenance**; every claim traces to a cited path.

Grounding: `Technical/research/S901_research.json`; `Technical/docs/series/S901_DPR.md` +
`S901_EPR.md`; `Technical/docs/chapters/CH9_RESEARCH_SUMMARY.md`;
`Technical/methodology_review/CH09_review.json`; Phase-0
`Technical/docs/methodology/_timelines/IO_CHANGE_TIMELINE.md` (+ `NIPA_CHANGE_TIMELINE.md`);
`Technical/docs/methodology/concordances/_sources/SOURCES.md`.

---

## 1. What it is

S901 is Shaikh's **empirical price-comparison exhibit**: for each of six benchmark years it pairs,
industry by industry, the **normalized total market price** `tpm_norm` against the **normalized
total direct price** `td_norm` (a price proportional to vertically-integrated total labor time `tv`).
It is the data behind **Fig 9.1** (1998 65-order + 1972 71-order market-vs-direct scatter, log
scales), **Fig 9.2** (multi-year evolution), and **Fig 9.16** (the same substrate scattered against
prices of production, an S902 output).

Book definition (Shaikh 2016, Ch9 p.395, quoted verbatim in `S901_research.json`):
> "Figures 9.1 and 9.2 compare each of sixty-five industry normalized total market prices to the
> corresponding total direct prices, using log scales for both. Normalization reduces each price set
> to unit length … This gives both sets the same mean, so we can use a dotted 45-degree line in the
> graph as a visual reference (it is not a fitted regression line)."

The construction (`S901_DPR.md` §4) is a pure per-year unit-length normalization of Shaikh's
pre-computed `tpm`, `td`, `tv` columns:
`tpm_norm[j,t] = tpm[j,t] / Σⱼ tpm[j,t]` (and likewise for `td`, `tv`). Four distance measures are
reported per benchmark year in **Table 9.9** — %MAWD (Ochoa 1984), classical scale-free `δc`
(book eq. 9.13), CV, and Euclidean `δe`; %MAWD and `δc` coincide in the market-vs-direct case
because both weight by the same monetary equivalent μ = TP/TV (`S901_research.json` methodology_notes).
The appendix ground-truth workbooks are `Appendix9_1947fixed.xlsx … Appendix9_1972fixed.xlsx`,
`Appendix9_1998Circ.xlsx`, `Appendix9_1998Fixed.xlsx`
(`SalvagedInputs/book_data/ShaikhChoppedTables/`). Hand-check: S901-A_1947F = normalized `tpm`,
ind1 = 0.11025038, **EXACT** vs the workbook (`CH09_review.json` hand_check_results).

Appendix location: **Appendix 9.2 pp.867–868** (data & methods). Note (CH09-F8, INFO): the direct-price
column `td_norm` is numerically identical to `tv_norm` to ~1e-13 because direct prices
`dᵢ = μ·wᵢ·vᵢ` are proportional to integrated labor times — correct per Shaikh's theory, carrying no
information beyond `tv_norm`.

## 2. Source lineage

Two provenance eras feed one cross-sectional object (`S901_DPR.md` §3; `S901_research.json`
primary_source):

- **1947, 1958, 1963, 1967, 1972 — Ochoa/Shaikh 71-order (SIC-vintage).** "Input–output tables and
  labor coefficients for 1947–1972 were taken from Shaikh (1998a) as compiled in (Ochoa 1984). These
  tables were rebalanced to exclude the real estate sector, the great bulk of which is from OOH
  (Ochoa 1984, 252)." (Ch9 p.868, verbatim.) Per the Phase-0 IO timeline these correspond to BEA
  benchmark I-O years on 1957/1972-SIC bases; **1972 is the last of the Ochoa 71-order panel Shaikh
  uses** (`IO_CHANGE_TIMELINE.md` benchmark-year table).
- **1998 — BEA 65-order (NAICS-vintage).** "The following data was taken from the US Bureau of
  Economics … industry-by-industry sixty-five-order total requirements input–output tables B′, after
  redefinitions designed to match commodity flows to industries; the vector of direct sectoral wage
  bills W constructed from the Employee Compensation portions of value-added flows in the use tables …
  and the market values of industry gross outputs X′ … All data is available for 1997–2009, but here
  we use 1998 to illustrate the general patterns." (Ch9 p.867, verbatim.)

Eigensystem/normalization construction chain (`S901_research.json` components; `S901_DPR.md` §4):
Leontief inverse `(I−A′)⁻¹` derived from `B′` → vertically-integrated labor coefficients
`vulc = l′(I−A′)⁻¹` → market-price share `tpm_norm` and direct-price share `td_norm`, both
l1-normalized to unit length. Skill-adjusted labor coefficients `l′ⱼ = wⱼ·(Lⱼ/X′ⱼ)` use the jth-sector
wage relative to the economy-wide wage from **NIPA Tables 1.10 / 6.4D (1998)** — differing from Ochoa
(1984, 225), who deflates by the *lowest* sectoral wage (footnote 2, p.868). Owner-Occupied Housing
correction on the 1998 real-estate column uses **NIPA Table 7.12 lines 133–134** (applied *upstream* by
Shaikh in the `Appendix9_1998*.xlsx`; the RSCD loader reads corrected values, does not re-apply —
`CH09_review.json` touchpoints S901/nipa).

## 3. Why these sources, from Shaikh's perspective + rejected alternatives

- **Why benchmark I-O over annual I-O.** Shaikh needs a *fully articulated inter-industry matrix*
  `B′` to form the Leontief inverse and integrated labor times; only **benchmark** years carry
  detail/summary-level tables with the commodity-to-industry redefinitions he relies on
  (`IO_CHANGE_TIMELINE.md`: detail estimates exist *only* for benchmark years). Annual I-O tables are
  interpolated/less-detailed and would not support a clean `(I−A′)⁻¹`.
- **Why the Ochoa 71-order compilation for 1947–1972.** It is the only consistently-rebalanced,
  real-estate-excluded historical panel already vetted in Shaikh's own prior work (Shaikh 1998a) —
  reusing it preserves continuity with the price-of-production literature (Ochoa 1989) he is
  extending, and lets him report %MAWD on the same footing as Ochoa.
- **Why exclude real estate / apply the OOH correction.** The real-estate sector is dominated by the
  imputed rent of owner-occupied housing, which has no market transaction and would inflate the
  market-vs-direct distance artificially (`S901_research.json` methodology_notes: "Without this
  correction, the real estate sector's market-direct-price distance is artificially huge").
- **Rejected alternative — a continuous 1947→1998 industry time series.** Explicitly declined: the two
  eras use incompatible classifications (SIC 71-order vs NAICS 65-order) and *cannot* be spliced
  (§4 below; `CH09_review.json` CH9-P1). Shaikh treats each year as a frozen cross-section.
- **Rejected alternative — a fitted regression line.** He states the 45° line "is not a fitted
  regression line" (p.395): the claim is *proximity to identity*, not statistical association, so a
  regression would misrepresent the point.

## 4. Methodological-change exposure — **the central section**

S901 sits directly on the **SIC→NAICS classification wall** documented in the Phase-0 IO timeline
(`IO_CHANGE_TIMELINE.md`, "The SIC → NAICS break (the Ch9 wall)"):

1. **71-order SIC ↔ 65-order NAICS non-splice.** Last SIC benchmark = **1992**; first NAICS benchmark
   = **1997**. BEA explicitly states the pre-1997 historical benchmark tables "should not be used as a
   time series." Shaikh's panel jumps **1972 → 1998** precisely across this break. The 1947–1972
   Ochoa 71-order (SIC) cross-sections and the 1998 BEA 65-order (NAICS) Use table are **not
   conformable**; a single continuous industry panel across the gap is not reconstructable
   (`CH9_RESEARCH_SUMMARY.md` open-question 3). RSCD encodes this as a hard limit: each year is a
   separate `cross_sectional` exhibit (`S901_DPR.md` §7 caveat 2). **Machine-enforcement gap**
   (`CH09_review.json` CH9-F4, MEDIUM): `industry_index` is a bare 1..71 / 1..65 integer with no
   `classification_vintage` tag, so nothing *mechanically* prevents a downstream consumer from
   concatenating the two eras — the limit is narrated, not asserted. Recommended fix: tag each row
   `classification_vintage ∈ {SIC71, NAICS65}` + a loader assertion.
2. **Even within NAICS, industry order drifts.** The summary/detail row-column order is revised at
   each benchmark (1997/2002/2007/2012/2017), so industry indices are not stable across NAICS
   vintages either (`IO_CHANGE_TIMELINE.md`, "Industry order / detail notes"). Any post-1998
   benchmark addition needs a fresh OOH correction and new labor-coefficient construction
   (`S901_research.json` extension_candidates concerns; `S901_EPR.md` §1).
3. **Concordance authority.** The Census SIC↔NAICS bridges that would be required to even *attempt* a
   crosswalk are staged in `concordances/_sources/naics/` — `1987_SIC_to_1997_NAICS`,
   `1997_NAICS_to_1987_SIC`, and the NAICS revision chain 1997→2002→2007→2012→2017→2022
   (`SOURCES.md`). BEA's own I-O↔SIC/NAICS concordances live only as SCB-PDF appendix tables (SCB Dec
   2002 App. A for 1997 I-O codes). These document *why the crosswalk is lossy* (bold `to`-codes =
   many-to-one; italic `from`-codes = one-to-many), reinforcing the non-splice discipline.
4. **NIPA vintage coupling.** The 1998 labor coefficients and OOH correction draw NIPA Tables 1.10 /
   6.4D / 7.12; Shaikh fixes BEA data at the **2011 vintage** (`NIPA_CHANGE_TIMELINE.md`, "Why this
   matters for RSCD"). Any re-pull of the 1998 Use table post-2013/2018/2023 comprehensive revision
   would land on reclassified magnitudes (software→IPP capitalization, T7.11 renumbering) and must
   never be spliced across a comprehensive-revision boundary.

## 5. Replication fidelity note

RSCD reproduces S901 **bit-exact to Appendix 9** by the read-the-truth-column pattern: it re-reads
Shaikh's pre-computed `tpm`/`td`/`tv` columns and re-normalizes identically; V03 tolerance ±0.5%,
observed **MAE 0.0%** (`CH9_RESEARCH_SUMMARY.md` Phase 5–8 closure; `S901_DPR.md` §9). Honest limits,
disclosed:
- **Circular reference caveat** (`CH09_review.json` CH9-F6, LOW): V03 validates against the identical
  `Appendix9_*.xlsx` the chopped is melted from — MAE 0.0 confirms *melt fidelity*, not independent
  book confirmation. Genuine non-circular anchors *do* exist and were verified: `δc` of Tables
  9.9/9.14/9.16 (10/12 year-cells EXACT) in `REPLICATION_VALUECHECK_ch09`.
- **OOH applied upstream, not re-derived**: a v2 fetching raw BEA Use tables would need to re-apply
  the NIPA 7.12 correction (`CH9_RESEARCH_SUMMARY.md` open-question 2).
- **Non-splice discipline held**: the SIC71 and NAICS65 eras are shipped as separate cross-sections;
  RSCD does *not* build an illegal continuous panel (`CH09_review.json` CH9-P1, POSITIVE).

## 6. Forward risk

- **Future BEA benchmarks** (2017 is the most recent; a 2022 benchmark will follow) each arrive on a
  fresh NAICS vintage with revised industry order — no benchmark can be appended to the 1998
  cross-section without a full re-crosswalk and re-OOH-correction; the natural "extension" is
  benchmark-*addition*, never a splice (`S901_EPR.md` §1).
- **NIPA comprehensive revisions** (next after 2023) will keep shifting the 1998 Use-table magnitudes
  and NIPA line numbers underneath any re-pull; stay on a single coherent vintage
  (`NIPA_CHANGE_TIMELINE.md`).
- **BEA table re-vintaging**: BEA has revised the 1998 vintage tables since 2010; validate that the
  `anwarshaikhecon.org` workbook numbers still match a 2026 iTable reconstruction
  (`S901_research.json` open_questions 3).

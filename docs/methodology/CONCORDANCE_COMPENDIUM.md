# RSCD Concordance Compendium

**Comprehensive-review Phase-3 synthesis** — industry-classification concordances across the RSCD
replication of Shaikh, *Capitalism: Competition, Conflict, Crises* (2016).

- **Compiled:** 2026-06-30 (RSCD Phase-3 concordance-synthesis agent)
- **Aggregates:** the Phase-0 official Census/BEA sources (`concordances/_sources/`), the two Phase-0
  vintage timelines (`_timelines/{IO,NIPA}_CHANGE_TIMELINE.md`), every `concordance_touch` record in the
  16 `methodology_review/CH*_methodology.json` files, the ch7/ch8/ch9 methodology histories, and the
  30/31-industry key `SalvagedInputs/.../Shaikh_2008_Appendix_B_industries.csv`.
- **Machine-readable companions:** `concordances/rscd_series_classification_map.csv`,
  `concordances/sic_naics_bridge_seed.csv`, `concordances/io_benchmark_industry_seed.csv`
  (+ `concordances/_PROVENANCE.md`). Build plan: `CONCORDANCE_BUILD_SPEC.md`.

---

## 1. Executive summary

Shaikh's *Capitalism* draws on data classified under **five families of industry-classification
systems** spanning a century of statistical practice — what the ch7 review calls the **"five-taxonomy
museum"**: pre-SIC US industry categories, the UK SIC of 1958, the OECD ISDB/STAN ISIC schemes, the US
SIC, and NAICS 1997–2022, plus the BEA input-output industry orders (71-order and 65-order) that sit
underneath the national accounts. These systems are **not mutually translatable without loss**, and the
single most important fact about them for this project is a *governance* fact:

> **Concordances are never applied inside the book period.** Every book series is reproduced
> **historically**, on the exact classification vintage the author used, frozen. A crosswalk is
> exercised **only** when a series is **extended** past its book period onto a live modern
> classification. This is the discipline behind every "NO crosswalk applied (historical reproduction)"
> note in the ch8 records and every "frozen exhibit" note in ch7/ch9.

Why concordances matter, then, is entirely forward-looking: they are the machinery that would let a
future maintainer **extend** a Shaikh industry series onto today's data — and the honest finding of this
synthesis is that for a large share of the industry-classified series, that machinery is either **lossy**
(SIC↔NAICS is many-to-many), **not yet staged as data** (BEA I-O↔NAICS lives in SCB PDF appendices), or
**structurally impossible** (the SIC→NAICS I-O wall, the discontinued capital-flow matrix, the
country-coverage collapse of OECD STAN).

Of the **65 concordance touches** catalogued across the 118 RSCD series, **31 require an
industry / IO-order / NIPA-line classification crosswalk to extend**. The rest are non-industry touches:
within-agency source-code renames (BLS WPI→PPI, IMF IFS→SDMX), country/base rebases (Maddison, ISO3), or
frozen walls where no crosswalk is possible.

**The concordance hotspots, in priority order:**

| Chapter | Touches | Character |
|---|---:|---|
| **Ch7** (competition of industry profit rates) | 11 | The five-taxonomy museum; the NAICS-native 30-industry panel; the international ISIC Rev3→Rev4 case (S711); Greek and pre-SIC/UK-SIC frozen walls |
| **Ch8** (real competition / concentration) | 5 | SIC-era CR4/CR8 concentration; **no crosswalk applied** (historical reproduction); Bain-1935 pre-SIC-precursor wall |
| **Ch9** (input-output profit-rate / prices) | 3 | The Ochoa 71-order (SIC) ↔ BEA 65-order (NAICS) wall; the discontinued 1997 capital-flow matrix |
| **Ch6 / XS** (GPIM capital & profit) | 4 + 3 | NIPA T7.11 FISIM **line-label** vintage resolver; FA legal-form split; the BEA I-O nested-aggregation ladder (XS2101) |
| **Ch2 / Ch10 / Ch15 / Ch16** | light | OECD ISDB (S213/S214), NAICS banking 52-vs-5221 (S1001), NAICS industry series (S1502/S1503), T7.11 inheritance (S1007/S1008/S1604) |

---

## 2. The classification-system catalogue

### 2.1 US Standard Industrial Classification (SIC)
- **Where it appears:** the pre-1997 BEA benchmark I-O accounts (ch9: 1947/1958/1963/1967/1972 on the
  1957/1972 SIC; 1987/1992 benchmarks on 1987 SIC); the ch8 concentration literature (Eichner, Stigler,
  Bain) which classifies "concentrated vs competitive" industries by SIC-era Census manufacturing groups.
- **RSCD staging:** the official Census **1987 SIC** is the *earliest* rung of the staged bridge chain
  (`_sources/naics/1987_SIC_to_1997_NAICS.csv` + reverse). Anything below 1987 SIC — Bain's 1935 Census
  categories, Salter's pre-SIC US groups — falls **off the bottom of the chain** and is irrecoverable.
- **The wall:** the last SIC-basis BEA benchmark is **1992**; BEA states pre-1997 tables *"should not be
  used as a time series."*

### 2.2 NAICS 1997 / 2002 / 2007 / 2012 / 2017 / 2022
- **Where it appears:** the ch7 30-industry profit-rate panel is **NAICS-native from 1997** (S705/S706/
  S709/S710); ch15 NAICS industry series (S1502/S1503); ch10 banking (NAICS 52 vs 5221); the post-1997
  BEA benchmark I-O accounts (ch9 1997+, XS009/XS2101).
- **RSCD staging:** an **unbroken official Census revision chain** 1997→2002→2007→2012→2017→2022 (both
  directions) is staged in `_sources/naics/`, plus direct 1987-SIC↔2002-NAICS. The project's ch7-specific
  stability table `ADR-005_NAICS/data/naics_concordance_master.csv` sits on top of it.
- **Stability:** for Shaikh's 3-digit sample the NAICS revisions are mostly **Stable / Minor change**
  (see the ADR-005 table) — the volatile cells are Computers-electronics (334), Publishing (511),
  Data-processing (518), Non-store retail (454). The 1997/2002 revision is the largest.

### 2.3 ISIC Rev3 / Rev4 (OECD ISDB, OECD STAN)
- **Where it appears:** ch7 international profit-rate comparisons — the retired **OECD ISDB 1994**
  (S703/S704) and the **OECD STAN** panel on **ISIC Rev3** (S711, the richest international case); ch2
  international series (S213/S214).
- **RSCD staging:** **NONE.** `_sources/naics/` is **US-only**. Any ISIC Rev3→Rev4 crosswalk (the
  international analogue of SIC→NAICS) is external and unstaged. ISDB was discontinued with no drop-in
  successor; STAN is the deferred target, and some Shaikh short labels (Wood&publishing, sale.motor,
  Comp.act.) do not map cleanly. STAN's country coverage **collapses 30 (2003) → 18** in later vintages
  (drops Canada/UK) — a coverage wall on top of the classification wall.

### 2.4 BEA input-output industry orders (71-order, 65-order)
- **Where it appears:** ch9's price / profit-rate-of-return eigensystem. Shaikh's 1947–1972 cross-sections
  use **Ochoa (1984)'s 71-industry order** (real estate excluded); his 1998 cross-section uses BEA's
  **65-order** industry-by-industry Use table (real-estate column corrected via NIPA T7.12 lines 133–134).
- **The wall:** the two orders are **not conformable**. Even within NAICS, the summary/detail order is
  revised at each benchmark, so industry indices are not stable across benchmark years.

### 2.5 The UK SIC 1958 label
- **Where it appears:** exactly once — Salter's Table 28 column header *"Industry (1958 S.I.C.)"* (S702),
  used as a **row label, not a mapping**. UK SIC 1958 → SIC 2007 is a hard classification break; no UK
  crosswalk is staged (RSCD stages US Census SIC↔NAICS only). Frozen exhibit.

### 2.6 (Non-industry, catalogued for completeness)
NIPA **T7.11 line-label** vintage resolves (ch6/XS003/S1007/S1604 — the FISIM recipe); FA **legal-form**
splits (ch6); source-code remaps (BLS WPI→PPI, IMF IFS→SDMX, Fed legacy-DDP→FRED); country schemes
(Maddison base-year, ISO3); HS trade codes (XS2201). These touch a *concordance* but not an *industry
classification* — they are recorded in the series map with `needs_crosswalk_for_extension = FALSE`.

---

## 3. Per-series concordance-dependency table

Full machine-readable version: `concordances/rscd_series_classification_map.csv` (65 rows).
Condensed to the **industry / IO-order / NIPA-line** touches that need a crosswalk for extension:

| Series | Ch | Classification system used | Crosswalk for extension? | Official source table |
|---|---|---|---|---|
| S213, S214 | 2 | OECD ISDB / STAN ISIC Rev3(→Rev4) | Yes | **Not staged** (US-only); UN ISIC correspondence external |
| S215 | 2 | BEA I-O / SIC→NAICS | Yes (barred; pre-1997 frozen) | SCB App.A (URL); `_sources/naics/` |
| S601–S604 | 6 | NIPA T7.11 line-label + FA legal-form | Yes (vintage resolve) | `NIPA_T711_FISIM_remap.md` + resolver |
| S701 | 7 | Pre-SIC US (Salter) | No — irrecoverable wall | (frozen) |
| S702 | 7 | UK SIC 1958 (row label) | No — no UK crosswalk staged | (frozen) |
| S703, S704 | 7 | OECD ISDB → ISIC Rev3→Rev4 / SIC→NAICS | Yes | **Not staged** |
| S705, S706, S709, S710 | 7 | NAICS 1997→2022 (30-industry panel) | Yes | `_sources/naics/` revision chain + ADR-005 |
| S707, S708 | 7 | Greek ISIC → NACE Rev2 (figure recovery) | No — not operationalised in data | **Not staged** |
| S711 | 7 | ISIC Rev3→Rev4 (OECD STAN) — richest int'l | Yes | **Not staged** |
| S801–S805 | 8 | SIC (US) concentration CR4/CR8 | Yes **for extension only** (none applied in book) | `1987_SIC_to_1997_NAICS.csv` |
| S901, S902, S903 | 9 | BEA I-O 71-order(SIC) ↔ 65-order(NAICS) | Yes | SCB App.A (URL); `_sources/naics/` |
| S1001 | 10 | NAICS banking (52 vs 5221) | Yes | `_sources/naics/` revision chain |
| S1007, S1008 | 10 | NIPA T7.11 line-label | Yes (vintage resolve) | `NIPA_T711_FISIM_remap.md` + resolver |
| S1502, S1503 | 15 | NAICS industry + SIC→NAICS wall | Yes | `_sources/naics/` revision chain |
| S1604 | 16 | NIPA T7.11 line-label | Yes (vintage resolve) | `NIPA_T711_FISIM_remap.md` + resolver |
| XS003 | XS | NIPA T7.11 line-label | Yes (vintage resolve) | resolver (pinned 2011/2018/2024) |
| XS009 | XS | BEA I-O / SIC→NAICS | Yes | SCB App.A (URL); `_sources/naics/` |
| XS2101 | XS | BEA I-O nested-aggregation ladder + BLS-170 | Yes | SCB App.A (URL); `_sources/naics/` |

**Total requiring a crosswalk for extension: 31 series** (see CSV for the full 65-row set including the
FALSE non-industry touches).

---

## 4. The three canonical mapping problems

### 4.1 SIC ↔ NAICS (Census bridges — lossy, many-to-many)
The 1987-SIC↔1997-NAICS bridge is staged and **directly derivable** (see
`sic_naics_bridge_seed.csv`), but it is **not a clean bijection**. Of the 24 RSCD-relevant industries,
**19 draw a single NAICS 3-digit industry from more than one 1987-SIC 2-digit division** — NAICS 541
(professional services) spans **15** SIC divisions; NAICS 336 (transportation equipment) spans 8; even
"Textile mills" (313) and "Apparel" (315) each pull from 5. In the reverse Census file, **bold to-codes**
mark a target industry drawn from >1 source and **italic from-codes** mark a source split into ≥2 targets.
**Consequence:** a Shaikh SIC-era value cannot be mechanically re-mapped onto a NAICS industry without a
**share-based allocation** — the bridge tells you *which* industries are entangled, not *how much* of one
belongs to another. This is why ch8's concentration series are reproduced historically and their
extension is flagged, not performed.

### 4.2 BEA I-O benchmark-year industry re-definition
Every 5 years BEA re-benchmarks the I-O accounts, and the industry order changes — not just at the
SIC→NAICS break (1992→1997) but at *every* benchmark. Shaikh splices the **Ochoa 1947–1972 71-order (SIC)**
cross-sections with the **1998 BEA 65-order (NAICS)** Use table; these are **not conformable**, so a single
continuous 1972→1998 panel is not reconstructable (CH9 open-Q3) — each benchmark is a frozen exhibit. The
BEA I-O↔SIC/NAICS concordances that *would* let you re-map exist only as **SCB PDF appendix tables**
(SCB Dec 2002 for 1997 codes; Oct 2007 for 2002; Aug 2018 for 2007/2012) — **URLs only, not staged as CSV.**
Compounding this: the **benchmark capital-flow matrix** (which distributes fixed investment across
industries) was produced for the **last time in 1997** and discontinued thereafter — so any post-1998
fixed-capital replication must *approximate* the asset-by-industry distribution (CH9 open-Q4).

### 4.3 ISIC Rev3 → Rev4 + country-coverage collapse (S711)
The international analogue of SIC→NAICS. Shaikh's ch7 international panel is on **ISIC Rev3** (via OECD
ISDB/STAN); extending it onto **STAN 2025** requires an **ISIC Rev3→Rev4** crosswalk that RSCD **does not
stage** (`_sources/naics/` is US-only), and some of Shaikh's short labels do not map cleanly. On top of
the classification break sits a **country-coverage collapse**: 30 countries in 2003 → 18 in later STAN
(Canada and the UK drop out; book p.859 V.3). The predecessor CD2 reproduced the overlap at
mean-deviation MAE ≈ 0.04 with a careful hand-built crosswalk + PWT re-aggregation — evidence it is
*doable*, but only with bespoke per-label work, not a staged table.

---

## 5. Honest limits

1. **SIC↔NAICS is many-to-many, not a bijection.** The seed is a *sector-level correspondence*, not a
   mechanical re-mapping table. 19/24 RSCD rows are many-to-many. A faithful extension across the wall
   needs share weights the bridge does not supply.
2. **BEA I-O↔NAICS concordances are not yet CSV.** They live in SCB PDF appendices (URLs staged in
   `_sources/SOURCES.md`); extracting them to tables is a deferred build task (see spec §5).
3. **No 1947–1992 SIC-era I-O *code* concordance is staged.** The Ochoa 71-order ↔ SIC detail mapping
   behind ch9's historical cross-sections is not in-project; each benchmark stays a frozen exhibit.
4. **No international (ISIC/UK/Greek) crosswalks are staged at all.** `_sources/naics/` is US-only. S703,
   S704, S711 (ISIC), S702 (UK SIC-1958), S707/S708 (Greek ISIC→NACE) have **no** in-project crosswalk;
   the first three block a live extension, the last three are frozen/figure-recovery exhibits.
5. **The book period never needs any of this.** Reproducing Shaikh's numbers requires *only* faithful
   historical transcription on the original vintage. Concordances are an **extension-time** concern; the
   `industry_index` in ch9's chopped data is even stored as a bare 1..71 / 1..65 integer with **no
   vintage tag** (CH9-F4), which is fine for frozen exhibits but is exactly why extension must add a
   `classification_vintage` guard before any concatenation (see build spec §4 validation).
6. **NIPA T7.11 line numbers are a vintage time-bomb, already solved.** The 2018 comprehensive update
   inserted one line and shifted every subsequent number by +1; the working
   `_nipa_t711_line_resolver.py` resolves by BEA `LineDescription` stub label instead of line number.
   This is the **proven pattern** the build spec generalizes.

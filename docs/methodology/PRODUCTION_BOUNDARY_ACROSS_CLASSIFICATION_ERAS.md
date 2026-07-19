# The Production Boundary Across Classification Eras

**Cross-chapter methodology note for the RSCD comprehensive review** — Shaikh, *Capitalism:
Competition, Conflict, Crises* (2016), clean replication.

- **Compiled:** 2026-07-01 (RSCD methodology-synthesis agent, campaign item A2.3 / finding N6)
- **Purpose:** state, in one place, that the classical/Marxian **production boundary** — the partition
  of the economy into the profit-driven *competitive-capital* activity Shaikh wants to measure and the
  activity he strips out — is implemented at **two different levels** in RSCD (an institutional-sector
  level in Ch6 and an industry level in Ch7), and is **absent by construction** from the SIC-era
  input-output work (Ch9 / XS2001 / S216). This is faithful to Shaikh's own construction; it is a
  scope-definition discontinuity that must **never be "harmonized"** by a future maintainer.
- **Status:** READ-ONLY synthesis. Every claim traces to a cited RSCD path re-verified this session.
- **Companions:** `IO_METHODOLOGY_CHANGE_COMPENDIUM.md`, `CONCORDANCE_COMPENDIUM.md`,
  `NIPA_METHODOLOGY_CHANGE_COMPENDIUM.md`, `FUTURE_ADJUSTMENTS_ROADMAP.md` §5 (the two irreducible walls),
  and the per-chapter histories `CH06_METHODOLOGY_HISTORY.md`, `CH07_METHODOLOGY_HISTORY.md`,
  `CH09_METHODOLOGY_HISTORY.md`.

---

## 1. Why this note exists

Reviewers keep rediscovering, independently, that "the production boundary" means different things in
different chapters of the replication — and worse, that the input-output chapters draw no such boundary
at all. Each rediscovery costs a review cycle and risks a maintainer "fixing" an apparent inconsistency
that is in fact a faithful reproduction of how Shaikh built his data.

The fact is simple and load-bearing: **there is no single RSCD "production boundary" object.** Shaikh's
classical distinction between the surplus-generating competitive-capital economy and everything else is
operationalised at whatever level the underlying source statistics permit, and the level changes with the
data vintage and the chapter's question:

- **Chapter 6** draws the boundary on **NIPA institutional sectors** (business vs household / NPISH /
  government / government-enterprise) — *not* on industries.
- **Chapter 7** draws the boundary on **NAICS industries** — a 31-industry exclusion key that leaves ~30
  retained competitive-capital industries — and *only* on the NAICS side of the SIC↔NAICS wall.
- **Chapter 9** (and XS2001, and the Ch2 cross-section S216) draws **no productive/unproductive partition
  at all** — the Sraffa/relative-price eigensystem runs on the **whole economy** (with only a real-estate
  exclusion and an owner-occupied-housing correction, which are *not* the same thing as a
  competitive-capital partition).

These three facts are individually documented in the per-chapter histories, but nowhere as **one
statement**. This note is that statement.

---

## 2. The three implementations

### 2.1 Chapter 6 — the boundary drawn on NIPA institutional sectors (business NOS)

In Chapter 6 the production boundary is an **institutional-sector** partition executed at the NIPA
national-accounts level, not at the I-O industry level. The object Shaikh wants — the surplus of
capitalist enterprise — is reached by starting from NIPA aggregate domestic Net Operating Surplus and
subtracting the non-business institutional sectors out explicitly (`XS001_MHR.md` §1; `XS003_MHR.md`;
`CH06_METHODOLOGY_HISTORY.md` §1,§3):

```
Business NOS = Aggregate Domestic NOS
             − NOS_household − NOS_NPISH − NOS_government − NOS_government_enterprises
```

- The **government-enterprise** subtraction follows BLS: Shaikh adopts the tighter BLS boundary that
  "also correctly excludes government enterprises because they are nonprofit (Harper, Moulton, Rosenthal,
  and Wasshausen 2008)" — a `NOSgoventerp` subtraction (NIPA T1.10 line 22) a naive "NIPA business
  sector" read would miss (`XS001_MHR.md` §3, book p. 830).
- The **owner-occupied-housing (OOH)** imputed rental surplus inside the household sector is stripped via
  the NIPA **T7.12 OOH breakdown, lines 133–140** (attributed to Ritter 2000 and Mayerhauser & Reinsdorf
  2007); without it the "business" surplus is inflated by an activity with no market transaction
  (`XS001_MHR.md` §2 source lineage + §3, `XS001_research.json`).
- The **FISIM / imputed-interest** pathology — NIPA's fictitious bank-imputation flows — is reversed by
  the T7.11 recipe `BusImpIntAdj = −BankNetIntPaid − NFNetImpIntPaid`, resolved by **BEA stub label, not
  line number**, in `Technical/code/L01_loaders/_nipa_t711_line_resolver.py`
  (documented in `NIPA_T711_FISIM_remap.md`; `XS003_MHR.md` §1). This corrects *which* surplus counts,
  reinforcing the same classical boundary.
- All of it is **frozen at the 2011 NIPA vintage** (Appendix 6.7 footnote 1; `XS001_MHR.md` §2,
  `CH06_METHODOLOGY_HISTORY.md` §4).

**Scope:** institutional sectors of the *whole* national economy. There is **no industry dimension** to
the Ch6 boundary — it does not touch NAICS or the I-O industry orders. It is inherited by transcription of
Appendix 6.8 columns, not recomputed in code (`XS001_MHR.md` §5; `CH06_METHODOLOGY_HISTORY.md` §5).

### 2.2 Chapter 7 — the boundary drawn as a NAICS-era industry exclusion key

In Chapter 7 the production boundary is an **industry** partition, and it exists **only on the NAICS side
of the SIC↔NAICS wall.** From the 61 NAICS private industries in BEA GDPbyIndustry, Shaikh **excludes 31
and retains 30**, "with a concomitant redefinition of the overall rate of profit" (book p. 858;
`CH07_METHODOLOGY_HISTORY.md` §"The 30-vs-31 industry panel"). The exclusion key is recovered verbatim
from Shaikh 2008 Table 9.A1 (p. 190) at:

> `SalvagedInputs/book_data/Reconstructed/Shaikh_2008_Appendix_B_industries.csv` — **31 rows**

Re-verified this session: 31 industry rows, on four exclusion grounds (`exclusion_ground` column):

| Exclusion ground (verbatim CSV values) | Example industries |
|---|---|
| `non-profit-or-noncompetitive` | Farms; Forestry, fishing |
| `internationally-noncompetitive` | Oil & gas extraction; Mining; Textile mills; Apparel |
| `low-or-negative-profit-rate-period-average` | Primary metals; Computers & electronics; Motor vehicles; Air/Rail/Water transport |
| `inadequate-WEQ-data-or-dominated-by-non-profit` / `dominated-by-non-profit` | Legal; Computer systems design; Education; Health; Arts; Other services |

The **30 retained** industries = the NAICS rows *not* in the CSV; they are the competitive-capital arenas
on which S705 / S706 / S709 / S710 are built, and the All-Private aggregate baseline (used for every
deviation in S709/S710) is defined over exactly those 30 — so a change to the exclusion set moves *every*
deviation (`CH07_METHODOLOGY_HISTORY.md` §"The 30-vs-31 industry panel").

**Scope:** NAICS private industries, 1997→2022 vintages. The US Ch7 panel (S705/S706/S709/S710) is
**NAICS-native from birth** — Shaikh starts a fresh construction in 1987 rather than extending his SIC-era
figures across the wall (`CH07_METHODOLOGY_HISTORY.md` §"The SIC↔NAICS story"). RSCD **inherits** the
reduction by transcribing Shaikh's already-reduced Appendix 7.2 panels rather than applying the CSV as a
code filter (review M3) — faithful, but the exclusion key is documentary, not an executed pipeline stage
(`CH07_METHODOLOGY_HISTORY.md` §"The 30-vs-31 industry panel"; `IO_METHODOLOGY_CHANGE_COMPENDIUM.md` §5).

### 2.3 Chapter 9 / XS2001 / S216 — no productive/unproductive partition (whole-economy)

The input-output / Sraffa-price work draws **no productive/unproductive (competitive-capital) partition
whatsoever.** The eigensystem — market vs direct prices (S901), Sraffa standard prices and integrated
output-capital ratios (S902), actual wage-profit curves (S903), and the price/value aggregate-ratio study
XS2001, and the frozen 1972 direct-price scatter S216 — runs on the **whole economy**
(`CH09_METHODOLOGY_HISTORY.md` §1–§2; `IO_METHODOLOGY_CHANGE_COMPENDIUM.md` §3).

The substrate splices **nothing** across the biggest discontinuity in US industry statistics; it *jumps*
1972 → 1998 and freezes each benchmark as a cross-section (`CH09_METHODOLOGY_HISTORY.md` §2):

- **1947, 1958, 1963, 1967, 1972**: Ochoa (1984) / Shaikh (1998a) **71-order, SIC-vintage** I-O tables,
  **real estate excluded** ("the great bulk of which is from OOH", Ch9 p. 868).
- **1998**: BEA **65-order, NAICS-vintage** industry-by-industry Use table, **OOH-corrected** via NIPA
  T7.12 lines 133–134.

Two points of precision the note must keep straight, so a maintainer does not mistake them for a
competitive-capital partition:

1. **The real-estate exclusion (Ochoa 71-order) and the OOH correction are not a production boundary.**
   They remove a specific imputation artefact (owner-occupied housing) so the price system is not
   distorted by a non-market flow — the same OOH concern as Ch6, but here it is a single-industry
   correction to a **whole-economy** matrix, not a 31-industry competitive-capital exclusion.
2. **The two I-O orders are not conformable.** Ochoa 71-order (SIC) and BEA 65-order (NAICS) sit on either
   side of the SIC↔NAICS wall (last SIC benchmark 1992; first NAICS benchmark 1997; BEA states the
   pre-1997 tables "should not be used as a time series") — so there is no continuous industry panel into
   which any boundary *could* be carried (`CH09_METHODOLOGY_HISTORY.md` §2;
   `IO_METHODOLOGY_CHANGE_COMPENDIUM.md` §1,§4(i); `CONCORDANCE_COMPENDIUM.md` §2.4,§4.2).

**Scope:** the whole I-O economy, benchmark by benchmark, each a frozen cross-section. No competitive-
capital partition is applied on either side.

### 2.4 The three implementations at a glance

| Chapter | Boundary level | Instrument | Retained scope | Applied in code? | File citations |
|---|---|---|---|---|---|
| **Ch6** (S601–604 / XS001, XS003) | **NIPA institutional sector** | Business-NOS subtraction (− HH − NPISH − govt − govt-enterprise), OOH strip (T7.12 L133–140), FISIM reversal (T7.11 resolver) | business sector of the whole economy | inherited by transcription (2011 vintage) | `XS001_MHR.md`, `XS003_MHR.md`, `CH06_METHODOLOGY_HISTORY.md` |
| **Ch7** (S705/706/709/710) | **NAICS industry** | 31-industry exclusion key (Shaikh 2008 Table 9.A1) | ~30 competitive-capital industries | inherited by transcription; key not applied as code filter | `Shaikh_2008_Appendix_B_industries.csv`, `CH07_METHODOLOGY_HISTORY.md` |
| **Ch9 / XS2001 / S216** | **none** (whole-economy) | Sraffa eigensystem on Ochoa 71-order (SIC) + BEA 65-order (NAICS); real-estate exclusion + OOH correction only | whole economy | frozen cross-sections | `CH09_METHODOLOGY_HISTORY.md`, `IO_METHODOLOGY_CHANGE_COMPENDIUM.md` |

---

## 3. What does NOT exist — and why that is faithful

Two absences are deliberate and correct. Neither is a defect to be closed.

1. **No SIC-era productive/unproductive partition.** The Ch9 / XS2001 / S216 I-O work has **no**
   competitive-capital exclusion analogous to Ch7's 31-industry key. This is faithful: Shaikh's Chapter-9
   project is a *relative-price / wage-profit-geometry* vindication of classical value theory on the whole
   inter-industrial system, not a real-competition profit-rate comparison across a curated set of
   competitive arenas. The two chapters ask different questions and therefore draw different (or no)
   boundaries. Inventing a SIC-era exclusion key to "match" Ch7 would fabricate an object Shaikh never
   built (`CH09_METHODOLOGY_HISTORY.md` §1–§2; `IO_METHODOLOGY_CHANGE_COMPENDIUM.md` §3).

2. **No cross-wall concordance of the boundary.** The 30-industry competitive-capital scope exists **only
   on the NAICS side** (Ch7). It is **not** carried backward across the SIC↔NAICS wall as an industry
   concordance, because the wall itself makes that impossible: the Ochoa 71-order (SIC) and BEA 65-order
   (NAICS) schemes are non-conformable, the SIC↔NAICS Census bridge is lossy and many-to-many (19 of 24
   RSCD-relevant industries are many-to-many; NAICS 541 alone spans 15 SIC divisions), and no SIC-era I-O
   *code* concordance is staged anywhere (`CONCORDANCE_COMPENDIUM.md` §4.1,§4.2,§5;
   `FUTURE_ADJUSTMENTS_ROADMAP.md` §5 Wall 1). So the boundary is a **scope-definition discontinuity ON
   TOP of the classification wall** — two distinct discontinuities stacked on the same 1992/1997 seam.

The consequence to internalise: RSCD's production boundary is **not one object mapped across time**. It is
three era- and chapter-specific constructions that happen to serve the same classical purpose. That is
exactly how Shaikh built the data, and the replication's honesty depends on never pretending otherwise.

---

## 4. Maintainer guardrails

1. **Never harmonize the three implementations.** Do not "unify" the Ch6 institutional-sector boundary,
   the Ch7 NAICS exclusion key, and the Ch9 whole-economy scope into a single object. They are faithful to
   three different chapter projects on three different classification substrates. A single harmonised
   "production boundary" would be a fabrication.

2. **Never back-cast the Ch7 exclusion key across the SIC↔NAICS wall.** The 30-industry competitive-capital
   scope is NAICS-side only. There is no faithful way to project it onto the Ch9 SIC-era 71-order I-O
   tables — and no need to, because Ch9 draws no such boundary. Any attempt would require a share-based
   allocation the lossy Census bridge cannot supply (`CONCORDANCE_COMPENDIUM.md` §4.1,§5).

3. **Never wait for a BEA release to close either absence.** Both walls under the boundary are irreducible:
   the pre-1997 SIC-era I-O *code* concordance (Wall 1) and the post-1997 benchmark capital-flow matrix
   (Wall 2) will not be reopened by any comprehensive update, benchmark, or NAICS revision
   (`FUTURE_ADJUSTMENTS_ROADMAP.md` §5). The honest ceiling is freeze-as-cross-section.

4. **The correct guard is a `classification_vintage` tag, not a boundary rewrite.** The one actionable
   machine-enforcement item is finding **CH9-F4 (MEDIUM)**: `industry_index` currently ships as a bare
   untagged integer (`1..71` for the SIC era, `1..65` for the NAICS era) with no `classification_vintage ∈
   {SIC71, NAICS65, NAICS_<year>}` tag, so nothing mechanically prevents a downstream consumer from
   illegally concatenating the two eras (`IO_METHODOLOGY_CHANGE_COMPENDIUM.md` §5;
   `CH09_METHODOLOGY_HISTORY.md` §2). The remedy is the backlog non-splice guard **SI-3 / T4.4
   (`classification_vintage`)** in `FUTURE_ADJUSTMENTS_ROADMAP.md` §4.3,§5 — a *tag that refuses illegal
   concatenation*, which also fences the boundary discontinuity described here. It does **not** license
   rewriting or harmonising the boundary itself.

> **Note on the briefing's "Decision D-7."** The A2.3 briefing referred to "Decision D-7
> classification_vintage tags." No decision numbered `D-7` exists in `Technical/docs/decisions/` (the
> ratified series runs 0001–0007, none of which is the `classification_vintage` guard). The real artifact
> is the **backlog** item **T4.4 (`classification_vintage`)**, tied to non-splice guard **SI-3**, in
> `FUTURE_ADJUSTMENTS_ROADMAP.md` §4.3,§5, and the finding it closes is **CH9-F4**. This note cites those
> real artifacts. See the Provenance section and the accompanying report's fact-corrections flag.

---

## 5. Provenance

**Files read and re-verified this session (2026-07-01):**

- `Technical/docs/methodology/IO_METHODOLOGY_CHANGE_COMPENDIUM.md` — voice/format model; §1,§3,§4(i),§5
  (the SIC↔NAICS wall, whole-economy I-O, CH9-F4 machine-enforcement gap, the ch7 exclusion-key note).
- `Technical/docs/methodology/CONCORDANCE_COMPENDIUM.md` — §2.4,§4.1,§4.2,§5 (BEA I-O orders, lossy
  many-to-many SIC↔NAICS bridge, honest limits, no cross-wall concordance).
- `Technical/docs/methodology/CH06_METHODOLOGY_HISTORY.md` — §1,§3,§4,§5 (NIPA-sector business-NOS
  boundary, 2011 vintage, transcribed-not-recomputed).
- `Technical/docs/methodology/CH07_METHODOLOGY_HISTORY.md` — §"The 30-vs-31 industry panel", §"The
  SIC↔NAICS story" (the 31-industry exclusion key, NAICS-native panel, inheritance by transcription).
- `Technical/docs/methodology/CH09_METHODOLOGY_HISTORY.md` — §1,§2 (whole-economy Sraffa system, 1972→1998
  non-splice, real-estate exclusion + OOH correction, CH9-F4).
- `Technical/docs/methodology/series/XS001_MHR.md` — §1,§2,§3,§5 (Business NOS formula; T7.12 L133–140 OOH
  strip; BLS government-enterprise exclusion; 2011 vintage).
- `Technical/docs/methodology/series/XS003_MHR.md` — §1,§4 (T7.11 FISIM reversal recipe; stub-label
  resolver).
- `Technical/docs/methodology/FUTURE_ADJUSTMENTS_ROADMAP.md` — §4.3,§5 (SI-3 / T4.4 `classification_vintage`
  guard; the two irreducible walls).
- `SalvagedInputs/book_data/Reconstructed/Shaikh_2008_Appendix_B_industries.csv` — 31 rows, four
  `exclusion_ground` values, re-counted and re-read in full.
- `Technical/code/L01_loaders/_nipa_t711_line_resolver.py` — confirmed present (the FISIM stub-label
  resolver referenced by Ch6).

**Verification note.** Every formula, key, scope, and file path above was read this session. Two deviations
from the A2.3 briefing were found and corrected in-place: (a) the briefing's "Decision D-7" is not a
literal artifact — the real object is the backlog SI-3 / T4.4 `classification_vintage` guard + finding
CH9-F4 (see §4 note); (b) the Ch6 OOH strip uses T7.12 lines **133–140** (Ch6/XS001) while the Ch9
real-estate OOH correction uses T7.12 lines **133–134** — these are two distinct corrections on the same
table, stated separately above rather than conflated.

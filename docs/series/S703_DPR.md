# S703 — Figure 7.13 — World Manufacturing WORLDAVG Rate of Profit, 1970–1990 (Christodoulopoulos/ISDB)

**Data Provenance Record (DPR)**

**Series ID**: S703
**Status**: book_period_validated
**Authored**: 2026-05-18 · **Machine-digitization revision**: 2026-07-02
**Author**: Anu Framework pipeline · **2026-07-02 revision**: opus M3 ingestion agent
**Related artifacts**:
- Research dossier: research dossier
- Adequacy: chapter adequacy report
- Extension Provenance Record: extension provenance record
- Registry entry: series registry → `series.S703`
- Subsource registry: subsource registry → `CHRISTODOULOPOULOS_1995_FIG7_13`
- **Durable digitized source**: internal remediation record
- **Overlay evidence**: internal remediation record
- **Adjudication log**: internal remediation record
- **Adversarial verification report**: internal remediation record

---

## 0. Recovery update (2026-07-02, Decision 0019 — amends 0018) — supersedes the data_unavailable framing below

S703 was **RECOVERED** from `data_unavailable` to `book_period_validated` by **machine digitization of the printed figure**. The underlying OECD ISDB / Christodoulopoulos raw data remain unrecoverable (unpublished NSSR working paper, discontinued 1994 ISDB vintage), but the single **WORLDAVG open-circle line** was read directly off Shaikh's printed Figure 7.13 (average panel) at reading fidelity. The status flip and method were authorized under the standing instruction "keep it safe, do what you want with it."

Fig 7.13 is a **9-series marker-coded "spaghetti" plot** (8 industries + WORLDAVG). We digitized **only the WORLDAVG open-circle (○) line** in the average panel, discriminating it at every year from the MACHEQP open diamond (◇) and the PAPER crossed-square (⊠). `provenance: machine_digitized`. §§1–9 below are updated; the original data_unavailable rationale is retained only as historical context where noted.

---

## 1. Definition

**S703** is the **WORLDAVG (world manufacturing AVERAGE rate of profit) aggregate line** Shaikh displays in the top/average panel of Fig 7.13. Coverage: 1970–1990, **20 points** (1974 omitted — see §7). It is one line — the world average — isolated from a 9-line figure; the 8 individual world-industry lines are not digitized.

Following the 2026-07-02 recovery (§0), this is a **machine-digitized book-period series**, not a `data_unavailable` one: the loader reads the digitized consensus values, the validator round-trips against them, and a chopped CSV plus an extenbook are produced. (The earlier `data_unavailable` handling — loader SKIPPED, validator `PASS_DATA_UNAVAILABLE`, no CSV — no longer applies; it is retained below only as historical context.)

## 2. Why it matters in Chapter 7

Ch7's empirical case for turbulent profit-rate equalization layers several exhibits: US BEA (S705–S710), the Greek manufacturing pair (S707/S708), OECD STAN (S711), and the **Christodoulopoulos (1995) world ISDB reconstruction** (S703 = Fig 7.13). The Christodoulopoulos panel is the longest-running multi-country evidence in the chapter. Its **raw data are no longer recoverable**, but the printed WORLDAVG line — the world average around which the 8 industry rates cluster — has now been machine-digitized and stands as the recovered aggregate exhibit.

## 3. Sources

| Subseries | Coverage | Publisher | Status |
|---|---|---|---|
| S703-A (WORLDAVG open-circle line, machine-digitized) | 1970–1990 | MACHINE_DIGITIZED_FIG713_WORLDAVG | **book_period_validated** (provenance: machine_digitized) |

The underlying OECD ISDB 1994 vintage was discontinued by OECD; Christodoulopoulos' New School (NSSR) working paper was never published and the raw dataset is not in `SalvagedInputs`. The Phase 4 B5 search recorded the dead-source finding at reconstructed book source data; that note is retained as history and is **superseded** by the 2026-07-02 machine-digitization recovery, which reads Shaikh's printed WORLDAVG line rather than the (still-missing) authors' table.

## 4. Construction

Machine digitization of the printed WORLDAVG open-circle line in Fig 7.13's average panel (1970–1990, 20 points). The method chain:

1. **Dual independent extraction.** Two agents extracted the WORLDAVG line blind to each other — extractor-A geometry-first (marker detection + axis-geometry calibration) and extractor-B sampling-first (curve sampling) — each producing an independent (year, value) table.
2. **Mechanical agreement test.** The two extractions were compared point-by-point; agreement within a threshold (≤2% of the y-range) passed a point RAW.
3. **Per-year crop-level marker-identity adjudication.** Every disputed year was re-viewed at high zoom on a cropped image to confirm the WORLDAVG open circle (○) and reject the MACHEQP open diamond (◇) and PAPER crossed-square (⊠).
4. **Adversarial verification.** A fresh agent, working from scratch off the figure and its printed axis glyphs (extractor notes not read), tried and **failed to refute** the curve. Verdict: **CONFIRMED**, no point refuted.

The consensus values are the durable digitized source (`S703_consensus.csv`). The loader (`L01_S703`) reads that consensus under a returns-precedence guard (see §8) → `data/raw` parquet; `P02_S703` passes it through → `data/processed/S703.parquet`; `V03_S703` round-trips and applies the reference-vertex and plausibility checks (§9). Chopped: `chopped/S703.csv` (20 rows, subseries **S703-A**, long-form). Extenbook: `extenbooks/S703_extenbook.xlsx`.

## 5. Year coverage

- **Book period**: 1970–1990 (20 points; **1974 omitted**, §7)
- **Extension period**: not applicable — the ISDB source is discontinued and not splice-compatible with modern OECD STAN (see `S703_EPR.md`)

**Caption-vs-figure disclosure.** The printed book **caption** reads "1970–1989," but the figure plots a data column hard on the right frame at **1990**, which the adversarial verifier confirmed is the **sharpest circle-vs-diamond discrimination in the whole series**. We honestly include 1990 as a WORLDAVG point; the discrepancy is between the caption text and the plotted figure, and we follow the figure.

## 6. Units

**rate (decimal).** The Fig 7.13 y-axis is decimal, 0–0.45. Values are stored decimal; the chopped `units` column reads `rate_decimal`.

## 7. Caveats

1. **Reading-grade, not table-exact.** The series was recovered by machine digitization of the printed figure, so it is faithful to Shaikh's plotted WORLDAVG line rather than to the authors' exact underlying table (which is not redistributed and remains unrecoverable). The printed figure is the authoritative record.
2. **1974 is an honest gap, not filled.** On the steep 1973→1975 descent, no defensible open-circle marker is resolvable — the only resolvable markers in that column are the PAPER crossed-square, the MINERALS filled-square, and a diamond, none of them an open circle. Per the no-interpolation / no-guess rule the 1974 value is **left as a gap** rather than guessed. (The adversarial verifier notes a soft ~0.14 circle is arguably present, but rules the omission a defensible conservative choice.)
3. **Two knots carry soft marker identity.** The **1973 peak-knot** (circle buried under the PAPER crossed-square) and the **1975 V-trough** (circle ≈ diamond overlap) have soft marker identity; this is already reflected in their low per-point confidences (0.45, 0.47).
4. **Transcription confidence MEDIUM-HIGH, ≈ ±0.005 decimal.** Per-point confidence ranges 0.45–0.90 (mean 0.666).
5. **No modern substitute** can splice onto the discontinued ISDB panel without violating the Anti-Degradation rule (ISIC Rev3→Rev4 industry break, sparse modern capital stock). Any modern continuation is methodologically separate, not an extension.
6. **Scope: average-panel WORLDAVG line only (Decision 0019, 2026-07-02).** The digitization recovered only the WORLDAVG open-circle line from the average-rate (top) panel of Fig 7.13. The incremental-rate (bottom) panel — same 9 lines, 1972–1989, y-axis −0.6 to 0.8 — was NOT digitized. This was an explicit scoping decision (Decision 0019). The display_name was corrected on 2026-07-17 from "World manufacturing average and incremental rates of profit" to "World manufacturing average rate of profit, 1970–1990" to accurately reflect the shipped scope. The incremental panel remains a future digitization candidate. Evidence: internal source record.

## 8. Cross-references

- **CD legacy ID** (identifier in CD, an earlier predecessor build of this dataset): `S032`
- **Book reference**: Shaikh (2016), Ch. 7 (Fig 7.13); Appendix 7.1 II / IV (book pp. 856, 859).
- **Durable digitized source + evidence**: internal remediation record — `S703_consensus.csv`, `S703_consensus_overlay.png`, `M2_adjudication_log.md`, `M3_verify_report.md`.
- **Precedence rule (keep forever).** If a human-guided digitization is ever filed at internal remediation record, it **SUPERSEDES** this machine consensus (provenance rank `human_guided` > `machine_digitized`). The `L01_S703` loader carries a returns-precedence guard that prefers the returns file when present.

## Notation (plain-language key)

Short forms used above, in plain language (this record is a downloadable external artifact):

- **S### / -A** — series identifiers in this project (e.g. S703). A trailing letter (e.g. S703-A) marks a *subseries* — one data line within that series.
- **WORLDAVG** — the world manufacturing **average** rate of profit: the single aggregate line (world total profit over world total capital) around which the 8 industry lines cluster in Fig 7.13.
- **Open circle / open diamond / crossed square** — the printed marker glyphs that distinguish the figure's 9 lines: WORLDAVG = open circle (○), MACHEQP = open diamond (◇), PAPER = crossed square (⊠).
- **DPR / EPR** — Data Provenance Record (this file) / Extension Provenance Record (its companion).
- **Phase N** — Anu Framework pipeline stages: Phase 4 = adequacy/readiness review, Phase 5 = ingestion, Phase 6 = extension, Phase 9 = visualization.
- **L01 / P02 / V03** — the per-series load / process / validate scripts.
- **CD / CD2** — earlier predecessor builds of this dataset (CD is older; CD2 is the later predecessor).
- **ROP** — (average) rate of profit.
- **ISDB** — International Sectoral Database (OECD).
- **STAN** — OECD Structural Analysis database.
- **NSSR** — New School for Social Research.

## 9. Validation

- **Round-trip**: `V03_S703` reads the digitized consensus back through the loader/processor and confirms the stored values are byte-faithful — **PASS**.
- **Three reference vertices** (Decision 0002; three well-separated, low-ambiguity anchors, decimal): **1970 = 0.1455** (start), **1982 = 0.119** (V-trough), **1990 = 0.1562** (end). Tolerance **±0.005 decimal**, consistent with the MEDIUM-HIGH transcription confidence.
- **Plausibility**: all values lie within the figure y-axis (0–0.45) and within the WORLDAVG band (0.10–0.20).
- **Anchor suite**: wired to the Decision-0011 anchor suite — **3 GREEN independent anchors**.
- **Gate outcome**: passed the M2 mechanical agreement gate **RAW** (19/20 compared = 95%); the M3 adversarial verifier returned **CONFIRMED**, **no point refuted**. → `publish: true`.

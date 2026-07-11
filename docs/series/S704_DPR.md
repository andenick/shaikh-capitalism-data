# S704 — Figure 7.14 — US Manufacturing Average Rate of Profit (USMANAVG line), 1960–1989

**Data Provenance Record (DPR)**

**Series ID**: S704
**Status**: book_period_validated
**Authored**: 2026-05-18
**Author**: Anu Framework pipeline
**Revised**: 2026-07-02 — machine-digitization recovery (Decision 0019, amending 0018) by **opus M3 ingestion agent**. The original 2026-05-18 authorship note stands; this revision supersedes its `data_unavailable` disposition.
**Related artifacts**:
- Research dossier: research dossier
- Adequacy: chapter adequacy report
- Extension Provenance Record: extension provenance record
- Registry entry: series registry → `series.S704`
- Subsource registry: subsource registry → `CHRISTODOULOPOULOS_1995_FIG7_14`
- **Durable source (machine consensus)**: internal remediation record
- **Recovery evidence**: `.../machine/S704_consensus_overlay.png`, `.../machine/M2_adjudication_log.md`, `.../machine/M3_verify_report.md`, `.../machine/S704_1990_omission_ruling.md`

---

## 1. Definition

**S704** is the **US manufacturing AVERAGE rate of profit** — the aggregate line Shaikh labels USMANAVG, displayed as the top/average panel of **Figure 7.14**. Period: 1960–1989, annual, unsmoothed. The underlying data are the Christodoulopoulos (1995) reconstruction of the OECD ISDB 1994 vintage (US subset); that raw dataset is discontinued and unrecoverable, so the **printed figure is the only surviving source**.

Fig 7.14 is a marker-coded multi-line ("spaghetti") plot of ~14 US manufacturing sub-industries plus the aggregate. The USMANAVG aggregate is the **boldest solid line, heaviest stroke, carrying NO markers**. RSCD digitized **only that single line** in the average panel; the individual marked sub-industry lines are not extracted.

As of 2026-07-02 this series is **RECOVERED** from `data_unavailable` to `book_period_validated` by machine digitization of the printed figure (Decision 0019). One subseries, **S704-A**, ships 30 annual points.

## 2. Why it matters in Chapter 7

Ch7's empirical case for turbulent profit-rate equalization layers several exhibits: the US BEA construction (S705–S706), the Greek deviation series (S707/S708), and the **Christodoulopoulos (1995) ISDB reconstruction** (S703 world / S704 US). S704 is the single-country, raw, unsmoothed test: it shows that average rates of profit differ persistently in level even at the national scale, before Shaikh pivots to BEA-NAICS for the 1987+ US window (S705/S706). The USMANAVG line is the aggregate summary of that panel — the one line that stands for "US manufacturing as a whole."

## 3. Sources

| Subseries | Coverage | Source | Status |
|---|---|---|---|
| **S704-A** | 1960–1989 | **MACHINE_DIGITIZED_FIG714_USMANAVG** | **book_period_validated** |

The ultimate data source — OECD ISDB 1994 vintage (US subset), as reconstructed in Christodoulopoulos' unpublished New School working paper — was discontinued by OECD and is not held in `SalvagedInputs`. The Phase 4 B5 search documented this at reconstructed book source data. Because the raw table cannot be recovered, the **published figure itself** was digitized: the boldest markerless USMANAVG vertex was traced off the average panel and stored as the durable machine consensus at `.../machine/S704_consensus.csv`.

## 4. Construction

Recovery was by **machine digitization of the printed Fig 7.14 average panel** (Decision 0019). The method chain:

1. **Dual independent extraction.** Two extractors read the USMANAVG line blind to each other — **extractor-A** geometry-first (tracing the continuous bold stroke, x-calibrated against the printed axis labels) and **extractor-B** sampling-first (column sampling). Neither saw the other's output.
2. **Mechanical agreement test (M2).** The two readings were compared point-by-point.
3. **Per-year boldness adjudication.** Where they disagreed, each disputed year was independently re-measured at crop level using **stroke-width (distance-transform half-width)**: the boldest markerless stroke at that column = USMANAVG. This resolved every disputed point.
4. **Adversarial verification (M3).** A third pass rebuilt the x-calibration from scratch and re-checked year registration.

**The +1-year x-offset diagnosis.** The raw M2 agreement gate FAILED at **53%** — but the failure was systematic, not random. Extractor-B carried a **+1-year x-offset**: it mis-numbered the tick ladder because the first tick mark sits about one year to the RIGHT of the printed "1960" label, so B read every column position one year early. This is a calibration error, not a disagreement about the data. Every failing point was re-measured by the boldest-markerless-stroke criterion and resolved to **extractor-A**.

**Three agreeing measurements.** The adversarial verifier then rebuilt the x-calibration independently — data-anchored on the evenly-spaced annual marker comb, calibration-free — and **independently confirmed extractor-A's year registration** (peak at 1965, trough at 1982), explicitly ruling out the +1-year shift. So each of the 30 stored values carries **three agreeing measurements**: (a) extractor-A's geometry-first trace, (b) the M2 boldness re-measurement, and (c) the verifier's from-scratch rebuild. Verdict: **CONFIRMED**, no point refuted.

Pipeline wiring:
- `L01_S704.py` loads the machine consensus (with a returns-path guard, see §7 caveat 3), converts the figure's percent to decimal by dividing by 100, and writes `data/raw/S704.parquet`.
- `P02_S704.py` is a pass-through to `data/processed/S704.parquet`.
- `V03_S704.py` validates (see §9).
- `chopped/S704.csv` (30 rows, subseries S704-A) and `extenbooks/S704_extenbook.xlsx` are regenerated.

## 5. Year coverage

- **Book period**: 1960–1989 — **30 annual points, complete.**
- **1990 column: OMITTED** (see §7 caveat 1).
- **Extension period**: not applicable (see `S704_EPR.md`; ISDB discontinued and not splice-compatible with modern BEA NAICS).

## 6. Units

**rate of profit (decimal)** — stored as `units = rate_decimal`, matching sibling series S705/S706.

The figure's own y-axis is drawn in **percent, spanning −10% to 60%**. RSCD stores rates of profit in decimal, so the digitized percent value is **divided by 100** on load (e.g. 25.31% → 0.2531). All values in `chopped/S704.csv` and the parquet are decimal.

## 7. Caveats

1. **The 1990 column is deliberately OMITTED (marker-occluded).** A 31st annual data column exists at the right edge of the figure — several *marked* industry series do plot a 1990 point there. But the boldest *markerless* USMANAVG vertex is **not resolvable at 1990**: the 12–14% band at that column is occupied by a filled-triangle marker, and the bold stroke's dominance (which cleanly isolates USMANAVG through 1987–89) collapses into a marker-dominated knot at 1990. Adding a 1990 point would mean guessing which converging stroke is USMANAVG — forbidden by the no-guess rule. This was settled by a targeted post-consensus measurement documented at `.../machine/S704_1990_omission_ruling.md`. Disclosed honestly; not silently dropped.
2. **Transcription tolerance ±0.5 percentage points.** Confidence is HIGH but these are values read off a printed curve, not an exact table. Per-point confidence ranges 0.52–0.85 (mean 0.757). Reproduction is faithful to the *published figure*, not to Christodoulopoulos' lost underlying table.
3. **Human digitization supersedes this machine consensus.** If a human-guided digitization is ever filed at `digitization_packet/returns/S704_aggregate_digitized.csv`, it **takes precedence** over the machine consensus, and `L01_S704.py`'s returns-guard prefers it automatically. This precedence rule is permanent.
4. **No modern substitute** can splice onto the discontinued ISDB panel: the 1960–89 ISDB and the 1987–2005 BEA NAICS panels are explicitly **not splice-compatible** (schema and gross-vs-net capital-stock breaks), which is why S705/S706 are a separate construction rather than an extension of S704.

## 8. Cross-references

- **CD legacy ID** (identifier in CD, an earlier predecessor build of this dataset): `S033`
- **Book reference**: Shaikh (2016), Ch. 7 (Fig 7.14, average panel); Appendix 7.1 §II / §IV (book pp. 856, 859).
- **Sibling**: S703 (the world/multi-country panel, Fig 7.13) — recovered by the same machine-digitization method on the same date.
- **B5 provenance document**: reconstructed book source data (documents the lost raw table; retained as the historical unavailability record).

## Notation (plain-language key)

Short forms used above, in plain language (this record is a downloadable external artifact):

- **S### / -A** — series identifiers in this project (e.g. S704). A trailing letter (S704-A) marks a *subseries* — one data line within that series.
- **DPR / EPR** — Data Provenance Record (this file) / Extension Provenance Record (its companion).
- **Phase N** — Anu Framework pipeline stages: Phase 4 = adequacy/readiness review, Phase 5 = ingestion, Phase 6 = extension, Phase 9 = visualization.
- **L01 / P02 / V03** — the per-series load / process / validate scripts.
- **CD / CD2** — earlier predecessor builds of this dataset (CD is older; CD2 is the later predecessor).
- **USMANAVG** — the ISDB internal code for the US-manufacturing AVERAGE aggregate line (the one line S704 digitizes).
- **ROP** — (average) rate of profit.
- **ISDB** — International Sectoral Database (OECD).
- **BEA / NAICS** — US Bureau of Economic Analysis / North American Industry Classification System.
- **M2 / M3** — the mechanical-agreement adjudication step and the adversarial-verification step of the digitization method chain.
- **distance transform** — an image measurement that gives a stroke's half-width, used to identify the *boldest* line at a column.

## 9. Validation expectation

- **Round-trip**: PASS — decimal parquet reloads to the stored consensus (percent ÷ 100) with no drift.
- **Three reference vertices** (well-separated, DECIMAL): 1965 = **0.2531** (peak), 1982 = **0.1038** (trough), 1989 = **0.1375** (end).
- **Plausibility**: all values within the decimal axis band (−0.10 … 0.60); observed band 0.05–0.30; structural check **trough(1982) < peak(1965)** holds.
- **Anchor suite** (Decision 0011): 3 independent anchors GREEN.
- **Adversarial verification (M3)**: **CONFIRMED** — extractor-A's year registration independently reproduced from scratch; +1-year shift ruled out; no point refuted.
- **Status**: `book_period_validated`.

# S203 -- US Real GDP per Capita (MeasuringWorth), 1889-2025

**Data Provenance Record (DPR)**

**Series ID**: S203
**Status**: book_period_validated
**Authored**: 2026-05-18
**Author**: Anu Framework pipeline
**Related artifacts**:
- Research dossier: research dossier
- Adequacy: chapter adequacy report
- Extension Provenance Record: extension provenance record
- Registry entry: series registry -> `series.S203`

---

## 1. Definition

Real GDP per capita on MeasuringWorth's continuously-updated annual reconstruction (Officer & Williamson). Plotted 1889-2010 in the book.

In Shaikh (2016) the series appears as **Figure 2.3** in Chapter 2 ("Turbulent Trends and Hidden Structures").

## 2. Why it matters in Chapter 2

Third leg of Shaikh's opening trio (industrial production, investment, GDP/cap); illustrates 150-year secular growth in per-capita real output.

## 3. Sources (per subseries)

| Subseries | Coverage | Publisher / Series ID | Native units | Retrieval |
|---|---|---|---|---|
| **S203-A** | 1889-2010 | MeasuringWorth Real GDP per Capita | real 2005 dollars | salvaged chopped |
| **S203-B** | 2011-2025 | FRED A939RX0Q048SBEA (Real GDP per Capita, chained 2017$) | chained 2017$ | FRED API |

## 4. Construction

`direct` construction, with a documented source-corruption correction (Decision 0008).

1. Read MeasuringWorth Real GDP per Capita column from salvaged chopped table.
2. **Correct the corrupt Great-Depression span (Decision 0008 / T1.2, applied 2026-07-01):**
   the salvaged book column is corrupt across **1930–1944** — real GDP/capita impossibly
   RISES through 1929–1934 (1929=8,187.56 → 1934=14,705.52 where history requires a
   ~25–30% fall). `P02_S203._correct_depression()` replaces ONLY those 15 rows with the
   fresh MeasuringWorth `usgdp` re-pull (2026 vintage, year-2017 dollars; retrieved
   2026-07-01; raw committed at `data/raw/S203_MEASURINGWORTH_USGDP_repull_20260701.csv`),
   re-based to the book 2005$ level by **overlap reindex at 1929**
   (scale = book(1929)/repull(1929) = 0.83778289). Decision 0008 named a 2010 overlap, but
   the book column ends at 2000 (2001–2010 NaN in the salvaged workbook), so the anchor is
   the last non-corrupt year adjacent to the replaced span; far-boundary continuity at 1945
   is −1.05% (within ordinary MeasuringWorth vintage drift). Corrected 1929→1933 falls
   −28.57%, strictly monotone. All other rows are byte-identical to the salvaged column;
   the salvaged workbook itself is untouched (historical evidence).
3. Extension: rescale FRED A939RX0Q048SBEA at 2010 overlap.

## 5. Year coverage

- **Book period**: 1889-2010
- **Extension period**: 2011-2025

## 6. Units

Real GDP per capita, constant 2005 dollars (per MeasuringWorth methodology)

## 7. Caveats

1. MeasuringWorth license is academic-use with attribution.
2. MeasuringWorth occasionally revises historical estimates; document access date.

## 8. Cross-references

- Book reference: Shaikh (2016), Ch. 2, Figure 2.3
- Knowledge Base: figure-linkage reference
- Predecessor (CD2): see registry `predecessor_ids` block.

## 9. Validation expectation

- **Tolerance**: +/- 1.0% per year (per playbook).
- **Expected MAE** (vs salvaged book truth): < 0.5% for the retained (non-corrupt) years.
  The corrected span **1930–1944 is excluded** from the book round-trip (the book source is
  corrupt there — see §4 step 2); V03_S203 additionally asserts the Decision-0011
  independent-anchor / plausibility suite (registry rule `S203_depression_must_fall`:
  1929→1933 strictly falling), and a plausibility RED FAILS the validator.

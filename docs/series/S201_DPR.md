# S201 — US Industrial Production Index, 1860–2025

**Data Provenance Record (DPR)**
**Phase**: 5 (Ingestion)
**Series ID**: S201
**Status**: ingested
**Authored**: 2026-05-18
**Author**: opus-pilot-S201
**Related artifacts**:
- Research dossier: `Technical/research/S201_research.json`
- Adequacy: `Technical/docs/chapters/CH2_ADEQUACY_REPORT.json`
- Extension Provenance Record: `Technical/docs/series/S201_EPR.md`
- Registry entry: `Technical/series_registry.json` → `series.S201`
- Subsource registry: `Technical/SUBSOURCE_METADATA.json` → `BEA_LTEG_1966`, `FRB_G17_INDPRO`, `FRED_INDPRO`

---

## 1. Definition

**S201** is the annual **United States Industrial Production Index, 1860–2025**, on a 1958=100 base. It tracks real industrial output (manufacturing + mining + electric & gas utilities) of the US economy at annual frequency.

In Shaikh (2016) the series appears as **Figure 2.1** ("US Industrial Production Index, 1860–2010"), opening Chapter 2 ("The Wealth of Nations: A Long View"). Shaikh uses it as the leading empirical illustration of the "system's apparently inexorable tendency toward growth" (p. 56).

## 2. Why it matters in Chapter 2

Chapter 2 introduces the empirical backbone of the book — the secular regularity of capitalist growth over 150 years, the persistence of cyclical fluctuations within that trend, and the magnitude of crises that punctuate it (the Long Depression, the Great Depression, the 1970s stagflation, the 2007–2009 crisis). The industrial production index, more than GDP, is the cleanest available real-output series running back to the antebellum period; it is therefore the natural choice for Shaikh's opening figure.

## 3. Sources (per subseries)

| Subseries | Coverage | Publisher / Series ID | Native units | Retrieval |
|---|---|---|---|---|
| **S201-A** | 1860–1918 | BEA, *Long Term Economic Growth, 1860–1965* (1966), Table A15 / Series A173 | Index 1913=100 | Salvaged chopped table `Appendix2_IndustrialProduction.xlsx` (column `IndProdHS_BEA`) |
| **S201-B** | 1919–2010 | Federal Reserve Board (FRB), Statistical Release G.17, *Industrial Production Index — All Industries* | Originally Index 2007=100 (now 2017=100) | Salvaged chopped table (column `IndProd_FRB`) — values as Shaikh retrieved them, ~2011 |
| **S201-C** | 2011–2025 | Federal Reserve Economic Data (FRED), series ID `INDPRO` (which is the FRB G.17 series republished by St. Louis Fed) | Index 2017=100 | Live API: `https://api.stlouisfed.org/fred/series/observations?series_id=INDPRO`; annual frequency = simple mean of monthly values |

The Phase 4 adequacy review confirmed FRB G.17 and FRED INDPRO both return HTTP 200 on the relevant endpoints, justifying the `ready_for_phase5` classification.

## 4. Construction

S201 is **composite** in the Anu sense: a single output series assembled from multiple non-overlapping (or overlapping-but-anchored) inputs. The construction recipe — exactly as Shaikh describes on book p. 763 — is:

1. **Load** S201-A (BEA LTEG, Index 1913=100) for years 1860–1959.
2. **Load** S201-B (FRB G.17, Index 2007=100 as originally retrieved) for years 1919–2010.
3. **Rebase** S201-A: scale factor `100 / BEA_1958` (~`100 / 457.0` = `0.21882`) — produces `IndProdHS1_BEA`.
4. **Rebase** S201-B: scale factor `100 / FRB_1958` (~`100 / 20.22705` = `4.94388`) — produces `IndProd1_FRB`.
5. **Splice at 1919**: use S201-B (FRB, rebased) from 1919 onward; use S201-A (BEA, rebased) for 1860–1918. *Note: at the splice year 1919 the two rebased series differ slightly (BEA = 24.77, FRB = 24.31) — Shaikh uses the FRB value, not an average.*
6. **Extend (Phase 6)** with S201-C (FRED INDPRO) for 2011–2025, anchored at the most recent overlap year so the post-2010 segment is on the same 1958=100 base. See `S201_EPR.md`.

**Formula** (none — composite, no algebraic combination):
```
S201[year] =
  IF year in [1860, 1918] : BEA_LTEG_A173[year] * (100 / BEA_LTEG_A173[1958])
  IF year in [1919, 2010] : FRB_G17[year]       * (100 / FRB_G17[1958])
  IF year in [2011, 2025] : FRED_INDPRO[year]   * (S201_processed[overlap_year] / FRED_INDPRO[overlap_year])
```

## 5. Year coverage

- **Book period**: 1860–2010 (inclusive, annual) — 151 observations
- **Extension period**: 2011–2025 (inclusive, annual) — 15 observations
- **Total coverage**: 1860–2025 — 166 observations
- **Gaps**: none expected in the book period (BEA LTEG covers continuously 1860–1965; FRB G.17 covers continuously 1919–present). If FRED API is unavailable at runtime, the loader degrades gracefully and S201 is published 1860–2010 only with status `extension_unavailable: api_key_missing` in the registry.

## 6. Units

- **S201 (final)**: Index, 1958 = 100.
- Every chopped CSV row carries the unit string `"index_1958=100"` in the registry; every parquet file embeds it in pandas-level metadata; every extenbook records it in the `Sources` sheet.

## 7. Caveats

1. **Splice gap at 1919 (~1.9%).** The BEA-rebased and FRB-rebased values at 1919 disagree by ~0.46 index points (24.77 vs 24.31). Shaikh explicitly uses the FRB value (per Appendix 2.1 documentation). No interpolation or averaging — `IndProd_Final[1919] = IndProd1_FRB[1919]`.
2. **BEA LTEG (1966) is out of print.** Shaikh's source is the original 1966 print volume. The numerical values are preserved in the salvaged chopped table (column `IndProdHS_BEA`), which is the authoritative source for the 1860–1918 segment of this replication. We do not attempt to re-digitize from microfilm.
3. **FRED INDPRO base year drift.** FRED rebases INDPRO periodically (2007 → 2012 → 2017 base most recently). The level of the raw FRED values changes when rebased, but the *ratios* are preserved, so an overlap-anchor reindex always recovers a 1958=100 series. We reindex on every load — never cache the rebased values across runs.
4. **Annual aggregation method.** FRB G.17 is published monthly. The book uses the annual average (arithmetic mean of 12 months). FRED's `frequency=a, aggregation_method=avg` parameter reproduces this directly.
5. **No proxy substitution.** FRED INDPRO **is** the FRB G.17 series, redistributed by St. Louis Fed under a public-domain license. There is no proxy here — same agency, same release, same concept — so the registry records `"proxy": false`.
6. **Discontinued?** No. As of the date of this DPR, FRB G.17 continues to publish monthly Industrial Production data and FRED republishes it without latency. Should the series ever be discontinued, the EPR documents the replacement path.

## 8. Cross-references

- **CD legacy ID**: `S001` (same concept, frozen)
- **CD2 legacy ID**: `S001` (same concept, frozen; values divergent — CD2 used a different reindex anchor for FRB; see V03 validator output)
- **Predecessor artifact**: `SalvagedInputs/extension_benchmarks/CD2_v1.3/Series/S001_us_industrial_production_index.xlsx`
- **Book reference**: Shaikh (2016), Ch. 2, p. 56 (text), p. 57 (Figure 2.1), p. 763 (Appendix 2.1, source documentation)
- **Knowledge Base**: see `SalvagedInputs/figures_reference/HDARP_SERIES_LINKAGE.json` → Fig2.1 entry

## 9. Validation expectation

- **Tolerance**: ±1.0% per year, computed as `abs(S201[y] - book_chopped[y]) / book_chopped[y]`, on the overlap range 1860–2010.
- **Expected MAE** (against the book chopped table `IndProd_Final` column): < 0.1% (we recompute Shaikh's exact recipe from his exact source columns).
- **Expected divergence vs CD2's S001**: ~1–2% post-1919, because CD2 used a different reindex anchor. This is *not* a failure of S201 — it is evidence that CD2 deviated from the book recipe.

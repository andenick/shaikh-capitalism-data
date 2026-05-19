# S404 — Automotive Unit Labor Cost (Fig 4.19)

**Data Provenance Record (DPR)**
**Phase**: 5 (Ingestion)
**Series ID**: S404
**Status**: ingested (data_unavailable)
**Authored**: 2026-05-18
**Author**: opus-subagent-ch4-fanout
**Related artifacts**:
- Research dossier: `Technical/research/S404_research.json`
- Adequacy: `Technical/docs/chapters/CH4_ADEQUACY_REPORT.json`
- Extension Provenance Record: `Technical/docs/series/S404_EPR.md`
- Registry entry: `Technical/series_registry.json` → `series.S404`
- Subsource registry: `Technical/SUBSOURCE_METADATA.json` → `INMAN_1995_ENGINEERING_ECONOMIST`

---

## 1. Definition

**S404** is Shaikh's Figure 4.19 (book p. 162) — simulated **automotive unit labor cost** (USD per car) plotted against annual vehicle production (in thousands). The figure is reproduced from Inman (1995), p. 61, fig. 3. Inman's underlying values are the means of a Monte-Carlo simulation of an automotive assembly plant's cost structure across output levels 0 to ~450 thousand vehicles/year, with explicit shift-addition markers and a vertical segment at engineering capacity.

This is a **cost-vs-output curve, not a calendar time series.**

## 2. Why it matters in Chapter 4

Inman's empirical curves (S404–S407) supply the empirical counterpart to Shaikh's theoretical curves (S401–S402). Shaikh's claim on p. 161 — that Inman's curves are "strikingly similar" to the theoretical curves he derived from Appendix 4.2 — is the empirical anchor for the chapter's revisionist account of cost curves. Fig 4.19 specifically demonstrates the "deformed U-shape with spikes at the beginning of each shift and roughly similar minimum points for each shift" pattern.

## 3. Sources (per subseries)

| Subseries | Coverage | Publisher / Series ID | Native units | Retrieval |
|---|---|---|---|---|
| **S404-A** | output range 0–~450 thousand vehicles/year | Inman, R. R. (1995), *The Engineering Economist* 41(1), 53–67 | USD per car vs. annual vehicle production (thousands) | **NOT RETRIEVABLE** without paywalled article access or unauthorized figure digitization |

**Citation correction (per Phase 4)**: agency is Robert R. Inman (not Robert P. Inman, as the Phase 3 dossier draft had it). The canonical citation, verified via Crossref API, is:

> Inman, R. R. (1995). "Shape Characteristics of Cost Curves Involving Multiple Shifts in Automotive Assembly Plants." *The Engineering Economist* 41(1), 53–67. DOI: 10.1080/00137919508967475

## 4. Construction

Per Inman (1995), `ulc(Q) = (fixed_labor_cost + variable_labor_cost(Q)) / Q`, where the variable component sums overtime, full-time, under-time, and second/third-shift premia, and the fixed component encodes layoff pay (95% of after-tax pay less $17.50/week). All cost values are means of a Monte-Carlo simulation.

**The underlying numerical series is not published as tabulated data** — Inman 1995 reports the simulation only as figures 3–6. The Taylor & Francis full text is paywalled. No salvaged dataset for Inman 1995 exists under `SalvagedInputs/` (confirmed by recursive `iname *inman*` search 2026-05-18).

## 5. Year coverage

Not applicable (cross-sectional cost-vs-output curve, single 1995 simulation).

## 6. Units

USD per car vs. annual vehicle production (thousands). Native to Inman's simulation; not normalized to a base year.

## 7. Caveats

1. **Data unavailable.** The chapter playbook's `data_unavailable` recipe applies:
   > "DPR + EPR documenting the chart-only source and why no underlying data exists; L01 returns `{status: SKIPPED, reason: data_unavailable}`; V03 returns `{status: PASS_DATA_UNAVAILABLE}`; No chopped CSV; Extenbook contains only the DPR + EPR + Source pages; Phase 8 viz uses the book figure image directly."
2. **Anti-fabrication**: figure digitization from the book reproduction (Shaikh p. 162) is technically possible via WebPlotDigitizer-style tooling, but per Phase 3 anti-fabrication compliance and the lack of an auditable underlying simulation, we **do not** digitize values into the parquet/CSV pipeline. The reference figure remains the canonical artifact; any future digitization would require a separate Decision Log entry.
3. **Bibliography corrected**: Phase 3 dossiers carried the wrong "Robert P. Inman" and a placeholder Google Books URL pointing to an unrelated Brookings volume. The DPR + the registry primary_source fields now reflect the Crossref-verified Robert R. Inman (1995) record.
4. **Paywall verified**: Tandfonline DOI proxy returned 403 (anti-bot, not invalid URL) on Phase 4 reachability check; documented as `unverified-rate-limited`, not failed.

## 8. Cross-references

- **CD legacy ID**: none
- **CD2 legacy ID**: none
- **Book reference**: Shaikh (2016), Ch. 4, p. 162 (Fig 4.19); narrative pp. 160–161.
- **Cross-series**: S405 (marginal labor cost from same Inman simulation, fig. 4), S406 (average total cost derived from S404 + amc), S407 (marginal cost derived from S405 + marginal material cost).

## 9. Validation expectation

- **Status**: `PASS_DATA_UNAVAILABLE` — the validator confirms the loader correctly SKIPPED and the DPR documents the rationale, but does not compute MAE.
- **Tolerance**: not applicable.
- **Future remediation**: should Inman 1995 underlying data become available (library access, author contact, replication study), the loader and validator can be extended without breaking the current pipeline contract.

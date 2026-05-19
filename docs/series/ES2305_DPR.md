# ES2305 — RMB Misalignment Estimates, Macroeconomic Balance Approach (Literature Compilation)

**Data Provenance Record (DPR)**
**Phase**: 5 (Ingestion)
**Series ID**: ES2305
**Content type**: `derived` (literature compilation scatter)
**Status**: ingested
**Authored**: 2026-05-18
**Author**: opus-fanout-ES

## 1. Definition

ES2305 is the scatter compilation of RMB misalignment estimates in
Weber & Shaikh (2020) Appendix Figure 5 (p. 455), filtered to estimates
that used the **macroeconomic balance** (MB / current-account-norm)
methodology, as opposed to the extended-PPP approach of ES2304.

Per paper note 17, ES2305 is compiled from the SAME 4 literature
reviews as ES2304:

- Cline & Williamson (2007) PIIE
- Dunaway & Li (2005) IMF WP/05/202
- Cheung, Chinn & Fujii (2010a) La Follette WP
- Cheung (2012) CESifo WP 3797

## 2. Why it matters

Section 4.4 (p. 443) shows that even the MB approach — which directly
relates to the CA balance and is therefore the methodology preferred
by currency-manipulation proponents — produces estimates from -100%
to +40%. This is independent evidence against the
currency-manipulation hypothesis on the MB approach's own grounds.

## 3. Sources

| Subseries | Coverage | Source | Native units | Retrieval |
|---|---|---|---|---|
| ES2305-A | 1999–2012 | Literature compilation per paper note 17 | percent | `SalvagedInputs/book_data/Reconstructed/ES2305_literature_compilation.csv` |

## 4. Construction

Same compilation rule as ES2304, with methodology filter set to
`macroeconomic_balance` instead of `extended_PPP`. Chopped CSV is the
canonical data structure.

## 5. Year coverage

Paper window: 1999-2012. **Extension status**:
`not_applicable_literature_compilation` — see ES2304_EPR for full
rationale; identical reasoning applies.

## 6. Units

`percent`.

## 7. Caveats

Identical to ES2304: v1.0 captures only the two paper-text-named
endpoint estimates (+40% Goldstein 2004 and -100% Bayoumi-Gagnon-
Saborowski 2015). Full ~30-35 point scatter reconstruction deferred
to v1.1 literature-extraction subagent.

## 8. Cross-references

- Dossier: `Technical/research/ES2305_research.json`
- Companion: `ES2304` (extended PPP, same 4 reviews)

## 9. Validation expectation

- Tolerance: 0.5% (verbatim transcription).

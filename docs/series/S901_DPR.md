# S901 — Market Prices vs Direct Prices (cross-section, 6 benchmark years)

**DPR** · **Phase**: 5 · **Series ID**: S901 · **Status**: ingested · **Authored**: 2026-05-18

---

## 1. Definition

**S901** is the per-industry pair `(tv_norm, tpm_norm)` — vertically-integrated labor times vs market prices, both normalized to unit length — for the six benchmark years:

- 1947, 1958, 1963, 1967, 1972 (71 industries, post-OOH-corrected SIC-vintage IO tables from Ochoa 1984 / Shaikh 1998a)
- 1998 (65 industries, BEA NAICS-vintage Use Tables, circulating model + fixed model both included)

Plus the dual `(tv_norm, td_norm)` direct-price pair. Together these supply Fig 9.1 (1998 + 1972 market-vs-direct scatter) and Fig 9.2 (multi-year evolution). Fig 9.16 is the same dataset, scattered against prices of production (an S902 output).

## 2. Why it matters

Empirical core of Shaikh's "0.95-correlation" finding: market prices are within a few percent of vertically-integrated labor times across capitalist industries, at all benchmark years, in both Krelle/Ochoa-style %MAWD and his own scale-free δc / CV / δe distance measures (Table 9.9). This is the empirical wedge against neoclassical "many prices, no labor anchor" claims.

## 3. Sources (per subseries)

| Subseries | Coverage | Source | Native units | Retrieval |
|---|---|---|---|---|
| **S901-1947** | 71 industries (1947) | Shaikh (1998a) / Ochoa (1984) post-OOH IO table | normalized share | `Appendix9_1947fixed.xlsx`, columns `tpm`, `td`, `tv` |
| **S901-1958** | 71 industries (1958) | same | normalized share | `Appendix9_1958fixed.xlsx` |
| **S901-1963** | 71 industries (1963) | same | normalized share | `Appendix9_1963fixed.xlsx` |
| **S901-1967** | 71 industries (1967) | same | normalized share | `Appendix9_1967fixed.xlsx` |
| **S901-1972** | 71 industries (1972) | same | normalized share | `Appendix9_1972fixed.xlsx` |
| **S901-1998C** | 65 industries (1998 circulating model) | BEA Use Tables 1998 + Shaikh redefinitions | normalized share | `Appendix9_1998Circ.xlsx`, columns `tpm`, `td`, `tv` |
| **S901-1998F** | 65 industries (1998 fixed-capital model) | BEA Use + Fixed Asset Tables 3.1ES/3.4ES | normalized share | `Appendix9_1998Fixed.xlsx`, same columns |

For each year, we emit two variables per industry: market-price share `tpm_norm` and direct-price share `td_norm`. The X-axis for scatter is `tv_norm` (labor-time share).

## 4. Construction

Per industry j and year t:
```
tpm_norm[j,t] = tpm[j,t] / sum_j tpm[j,t]
td_norm[j,t]  = td[j,t]  / sum_j td[j,t]
tv_norm[j,t]  = tv[j,t]  / sum_j tv[j,t]
```
These are the exact normalizations Shaikh uses in Fig 9.1/9.2 ("normalization reduces each price set to unit length"). All values come directly from his pre-computed `tpm`, `td`, `tv` columns in the Appendix9 workbooks; no fresh IO solve is required for this series.

## 5. Year coverage / coverage

6 benchmark years × 65-71 industries × 2 series per row (S901-A market-norm, S901-B direct-norm) = ~840 row pairs total.

## 6. Units

Normalized share (dimensionless, sums to 1 within each subseries-year). Loader column `units = "normalized_share"`.

## 7. Caveats

1. **OOH (Owner-Occupied Housing) correction.** The 1998 real-estate column in A' and X' is rescaled by Shaikh per NIPA Table 7.12 lines 133-134 to remove imputed owner-occupied gross output and intermediate inputs. The Appendix9_1998*.xlsx workbooks have this correction already applied; the loader does not re-apply.
2. **Industry classification mismatch.** 1947-1972 tables are 71-industry SIC-vintage; 1998 tables are 65-industry NAICS-vintage. The two epochs are NOT spliceable into a continuous panel; each year is a separate cross-section. This is a hard limit, documented in Phase 4 ratification.
3. **Two 1998 variants.** Shaikh runs both circulating-capital (K=A, D=0) and fixed-capital (K and D from Fixed Asset Tables) models on the 1998 data. We emit both as separate subseries so downstream visualizations can render either.
4. **No proxies.** All values are Shaikh's pre-computed tpm/td/tv, which trace to BEA Use Tables (1998) or Ochoa (1984) compiled SIC tables (1947-1972).

## 8. Cross-references

- CD/CD2 legacy ID: `S047`.
- Book: Shaikh (2016) Ch9 pp.395-396; Appendix 9.2 pp.867-868.
- Figure list (Phase 4 ratified): Fig 9.1, 9.2, 9.16.
- Companion: S902 (eigensystem standard prices on the same data substrate).

## 9. Validation expectation

- Tolerance: **±0.5%** per industry (cross_sectional).
- Truth source: re-read `tpm`, `td` from the same workbooks, normalize identically, compare cell-by-cell.
- Expected MAE: 0% (read-the-truth-column pattern).
- Diagnostic: report %MAWD = Σ |tpm_norm - td_norm|·tv_norm per year (Ochoa 1984 mean absolute weighted deviation) as informational output.

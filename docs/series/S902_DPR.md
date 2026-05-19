# S902 — Integrated Output-Capital Ratios and Standard Prices

**DPR** · **Phase**: 5 · **Series ID**: S902 · **Status**: ingested · **Authored**: 2026-05-18

---

## 1. Definition

**S902** is the eigensystem standard-price decomposition of Shaikh's IO data (book eq. 9.1.5 and §9.20). For each industry j and each benchmark year t it carries:

- `tp(r)_norm[j,t]` — normalized standard price of industry j at the observed profit rate r_obs(t)
- `tv_norm[j,t]` — normalized labor-time share (same as S901's tv_norm; the labor-value composition `VR0_j`)
- Per-year observed profit rate `r_obs(t)` (Appendix9_ObservedProfitRates.xlsx)

Together they supply Figs 9.4, 9.5, 9.6, 9.7, 9.9, 9.10, 9.11, 9.13, 9.14, 9.15, 9.18 — the eigensystem and distance-measure outputs.

## 2. Why it matters

Shaikh's Sraffa-eigensystem result: even with realistic IO data and a fixed-capital model, the actual `(VR(r)_j)` paths are near-linear in r/R and the standard prices `p(r)_j/v_j` deviate from labor values by only a few percent over the full r ∈ [0, R] range. Empirical demonstration of the classical relevance of the standard commodity at real-world capital intensities.

## 3. Sources (per subseries)

| Subseries | Coverage | Source | Native units | Retrieval |
|---|---|---|---|---|
| **S902-1947F** | 71 industries (1947 fixed-capital) | Shaikh (1998a) / Ochoa (1984) | normalized share | `Appendix9_1947fixed.xlsx`, columns `tp(r)`, `tv` |
| **S902-1958F** | 71 industries (1958) | same | normalized share | `Appendix9_1958fixed.xlsx` |
| **S902-1963F** | 71 industries (1963) | same | normalized share | `Appendix9_1963fixed.xlsx` |
| **S902-1967F** | 71 industries (1967) | same | normalized share | `Appendix9_1967fixed.xlsx` |
| **S902-1972F** | 71 industries (1972) | same | normalized share | `Appendix9_1972fixed.xlsx` |
| **S902-1998C** | 65 industries (1998 circulating) | BEA Use Tables (post-redef) + OOH correction | normalized share | `Appendix9_1998Circ.xlsx` |
| **S902-1998F** | 65 industries (1998 fixed-capital) | BEA Use + Fixed Asset Tables 3.1ES/3.4ES + 1997 capital flow benchmark | normalized share | `Appendix9_1998Fixed.xlsx` |
| **S902-ROBS** | 7 (year, r_obs) pairs (1947, 58, 63, 67, 72, 1998C, 1998F) | book Table 9.18 + Appendix9 sheet headers | decimal | `Appendix9_ObservedProfitRates.xlsx` |

## 4. Construction

Per industry j and year t (the loader reads pre-computed columns):
```
tp(r)_norm[j,t] = tp(r)[j,t] / sum_j tp(r)[j,t]
tv_norm[j,t]    = tv[j,t]    / sum_j tv[j,t]
```
plus the observed-profit-rate scalar table.

The deep computation (eigenvalue decomposition of KT = K·(I-(A+D))^-1 yielding the maximum profit rate R_t and the standard prices p(r)_j) is documented in Appendix 9.1. We adopt Shaikh's pre-computed `tp(r)` column and the published `r observed` header rather than re-solving the eigensystem from scratch — this matches the playbook's "read the truth column" pattern for V03 PASS and defers a fresh eigenvalue replication to a Phase-9-style scientific-validation skill.

## 5. Year coverage

Same 6+1 benchmark years as S901 (the 1998 year is double-counted via 1998C and 1998F variants); observed profit rates from the ObservedProfitRates workbook for 1947 (0.236), 1958 (0.176), 1963 (0.21), 1967 (0.229), 1972 (0.188), 1998 (0.1258 fixed; 0.2971 circulating per the sheet headers).

## 6. Units

`normalized_share` (dimensionless) for price/value vectors. `decimal_profit_rate` for r_obs.

## 7. Caveats

1. **Pre-computed standard prices, not re-solved.** v1 trusts Shaikh's tp(r) columns. A fresh dominant-eigenvalue solve of KT to recover Table 9.18's R_t values (1947=1.088, 1958=0.9734, 1963=0.8547, 1967=0.7644, 1972=0.7033, 1998=0.7317) is a documented Phase-5 open task per CH9_ADEQUACY — but blocking it would block all of Ch9, so v1 uses Shaikh's already-published standard-price vectors and treats the eigenvalue replication as a downstream concern.
2. **Two 1998 model variants.** Circulating (K=A, D=0) and fixed-capital both emitted; downstream visualizations select per figure.
3. **OOH correction applied upstream.** Same as S901.
4. **No proxies.**

## 8. Cross-references

- CD/CD2 legacy ID: `S048`.
- Book: Shaikh (2016) Ch9 pp.406-407; Appendix 9.1 + 9.2 pp.860-869.
- Figure list (Phase 4 ratified): Fig 9.4, 9.5, 9.6, 9.7, 9.9, 9.10, 9.11, 9.13, 9.14, 9.15, 9.18 (11 figures).
- Sibling: S901 (same data substrate), S903 (wage-profit curves from same eigensystem).

## 9. Validation expectation

- Tolerance: **±0.5%** per industry (cross_sectional).
- Truth source: same `tp(r)` and `tv` columns from the Appendix9 workbooks, normalized identically; r_obs values from the ObservedProfitRates workbook.
- Expected MAE: 0% (read-the-truth-column pattern).
- Diagnostic: report per-year δc = Σ|tp(r)_norm/tv_norm - 1|·tv_norm — the scale-free standard-price-vs-labor-value distance measure (Table 9.12 / 9.13 values).

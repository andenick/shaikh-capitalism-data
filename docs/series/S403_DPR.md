# S403 — Total Profit with Different Wage Arrangements (Fig 4.18)

**Data Provenance Record (DPR)** — the internal, full-provenance companion to the public Explainer.
**Record type**: Data Provenance Record (source-and-construction detail)
**Series ID**: S403
**Status**: book_period_validated
**Authored**: 2026-05-18
**Prepared by**: RSCD data-construction pipeline
**Related artifacts**:
- Series research notes: research dossier
- Adequacy: chapter adequacy report
- Extension Provenance Record: extension provenance record
- Registry entry: series registry → `series.S403`
- Subsource registry: subsource registry → `SHAIKH_APPENDIX_4_2`

---

## 1. Definition

**S403** reproduces Shaikh's Figure 4.18 (book p. 157) — total daily profit profiles `PL = p·XR − tc'` (per-worker wages) and `PH = p·XR − tc` (per-hour wages), tabulated against cumulative output `XR`. Output price `p = 7`.

## 2. Why it matters in Chapter 4

Fig 4.18 demonstrates Shaikh's central theoretical claim about the failure of the neoclassical `p = mc` profit-maximization rule. The chosen output level differs by wage convention:

- **Per-worker wages**: maximum profit at the end of **shift 2** (the second mc-spike).
- **Per-hour wages**: maximum profit at **engineering capacity** (end of shift 3).

`p = mc` admits multiple solutions in both cases (because mc is non-monotonic with spikes at shift boundaries). The classical cost-minimizing output and the neoclassical profit-maximizing output therefore diverge — a distinction Shaikh develops in chapters 7–8.

## 3. Sources (per subseries)

| Subseries | Coverage | Publisher / Series ID | Native units | Retrieval |
|---|---|---|---|---|
| **S403-A** (the dataset's two profit columns) | output rows 0–20 (21 points) | Shaikh, *Capitalism* (2016), Appendix 4.2 Table 4.2.4, profit columns | money units | Reconstructed CSV reconstructed book source data, columns `XR`, `PL`, `PH` |

## 4. Construction

A `derived` series (built by formula). The data-loading step reads the tabulated profit columns from the same table as S401/S402.

```
PL = p * XR − tc'    (per-worker wages; tc' from S401)
PH = p * XR − tc     (per-hour   wages; tc  from S402)

p = 7  (book p. 781)
```

At XR=0, PL = PH = −70 (negative of fixed cost alone).

## 5. Year coverage

Not applicable (XR axis).

## 6. Units

Money units (total daily profit; illustrative).

## 7. Caveats

Same XR-axis / Appendix-parameter caveats as S401. Additionally:

1. **Maximum profit is unique within each wage convention**, but the two conventions select different XR values — Shaikh's substantive point.
2. **Profit is negative for low XR** because total revenue does not yet cover fixed cost. Negative profits at XR rows 1–5 (PL) and rows 1–4 (PH) are visible in Fig 4.18.

## 8. Cross-references

- **Book reference**: Shaikh (2016), Ch. 4, p. 157 (Fig 4.18); Appendix 4.2, p. 781.
- **Cross-series**: derives from S401 (per-worker total cost) and S402 (per-hour total cost); the registry records this dependency.

## 9. Validation expectation

- **Tolerance**: ±0.5%.
- **Expected mean absolute error (MAE)**: 0 — a direct round-trip of the same table (via the validation step).

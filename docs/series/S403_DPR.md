# S403 — Total Profit with Different Wage Arrangements (Fig 4.18)

**Data Provenance Record (DPR)**
**Phase**: 5 (Ingestion)
**Series ID**: S403
**Status**: ingested
**Authored**: 2026-05-18
**Author**: opus-subagent-ch4-fanout
**Related artifacts**:
- Research dossier: `Technical/research/S403_research.json`
- Adequacy: `Technical/docs/chapters/CH4_ADEQUACY_REPORT.json`
- Extension Provenance Record: `Technical/docs/series/S403_EPR.md`
- Registry entry: `Technical/series_registry.json` → `series.S403`
- Subsource registry: `Technical/SUBSOURCE_METADATA.json` → `SHAIKH_APPENDIX_4_2`

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
| **S403-A** | XR rows 0–20 (21 points) | Shaikh, *Capitalism* (2016), Appendix 4.2 Table 4.2.4, profit columns | money units | Reconstructed CSV `SalvagedInputs/book_data/Reconstructed/Appendix_4_2_Table4.csv`, columns `XR`, `PL`, `PH` |

## 4. Construction

`derived` / `formula`. Loader consumes the tabulated profit columns from the same CSV as S401/S402.

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
- **Cross-series**: derives from S401 (tc') and S402 (tc). Cross_references field in registry records this dependency.

## 9. Validation expectation

- **Tolerance**: ±0.5%.
- **Expected MAE**: 0 — direct CSV round-trip.

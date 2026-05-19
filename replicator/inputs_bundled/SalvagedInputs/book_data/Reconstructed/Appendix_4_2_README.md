# Appendix 4.2 Reconstruction — Shaikh (2016) *Capitalism*

**Status**: RESOLVED — Verbatim transcription from book PDF
**Created**: 2026-05-18
**Resolves**: CH4 blocker B1 (Phase 5)
**Used by**: S401, S402, S403 (Figures 4.16, 4.17, 4.18)

---

## Source

- **Book**: Anwar Shaikh, *Capitalism: Competition, Conflict, Crises* (Oxford University Press, 2016)
- **Appendix**: 4.2 "Numerical Calculations for Figures 4.1–4.18", book pp. 772–781
- **PDF location**: `Inputs/Capitalism Data/Inputs/[2016] Shaikh - Capitalism Competition, Conflict, Crises.pdf`
- **PDF page numbers**: 810–819 (book pp. 772–781)
- **Tables transcribed**: 4.2.1, 4.2.2, 4.2.3, 4.2.4

The original Shaikh-website data-companion workbook for Appendix 4.2 is **NOT** present in `ShaikhChoppedTables/` (which only contains Appendices 2, 5–17). The companion file on Shaikh's website (`Inputs/Capitalism Data/Inputs/ShaikhWebsiteTables/_Appendix 4.2 Numerical Calculations Production and Costs.docx`) is a TEXT-only document with `[INSERT Appendix 4.2, Table N: …]` placeholders — the numerical tables are not embedded. Therefore the only source for these tables is the book PDF itself.

## Files produced

| File | Source page (PDF) | Source page (book) | Rows | Cols | Description |
|---|---|---|---|---|---|
| `Appendix_4_2_Table1.csv` | p. 811 | p. 773 | 21 (h=0..20) | 8 | Productivity, output, and production coefficients for intensity i=1 |
| `Appendix_4_2_Table2.csv` | p. 814 | p. 776 | 21 (H=0..20) | 8 | PPF and shift-combination outputs (20:0, 17:3, 3:17, 12:8, 10:10) at i=1 |
| `Appendix_4_2_Table3.csv` | pp. 815–816 | pp. 777–778 | 21 (incl. h=0) | 15 | Production patterns for socially normal shift lengths & intensity (i=0.80) — wide format combining both sub-pages |
| `Appendix_4_2_Table4.csv` | pp. 817–818 | pp. 779–780 | 21 (incl. XR=0) | 14 | Cost curves and profit — both per-worker (primed) and per-hour wage variants in a single wide table |

Total: 4 CSVs, 84 data rows.

## Table-specific column glossaries

### Table 4.2.1 (`Appendix_4_2_Table1.csv`)
- `h`: shift hours (length of working day)
- `xr`: average productivity of labor (XR/H)
- `H`: cumulative labor-hours (= h for single shift)
- `XR`: cumulative daily output
- `l`: labor coefficient (H/XR = 1/xr)
- `mpl`: marginal product of labor (∂XR/∂H)
- `a`: materials coefficient (constant = 0.30)
- `mk`: machine coefficient (MK/XR with MK=14)

### Table 4.2.2 (`Appendix_4_2_Table2.csv`)
- `H`: cumulative daily labor-hours (0..20)
- `XR_20_0`: cumulative output, single 20-hr shift
- `XR_17_3`: cumulative output, 17+3 shift combination
- `XR_3_17`: cumulative output, 3+17 shift combination
- `XR_12_8`: cumulative output, 12+8 shift combination
- `XR_10_10`: cumulative output, 10+10 shift combination (the maximum-output combo)
- `xr_10_10`: average labor productivity for 10:10 combo (= XR_10_10 / H)
- `mpl_10_10`: marginal product of labor for 10:10 combo

### Table 4.2.3 (`Appendix_4_2_Table3.csv`)
Wide-format merge of the two PDF sub-pages.
- `shift`: shift label (`Shift_1`/`Shift_2`/`Shift_3`)
- `N`: cumulative employment
- `shift_hours_h`: hours within the current shift (1..8 for shifts 1–2, 1..4 for shift 3)
- `H`: cumulative labor-hours (1..20)
- `HMK`: cumulative machine-hours (H × MK = H × 14)
- `XR`: cumulative output
- `xr_prime`: output per worker (XR/N)
- `mkn`: machines per worker (MK/N)
- `xr`: output per worker-hour (XR/H)
- `mkh_prime`: machines per worker-hour (MK/H)
- `mkh`: machine-hours per worker-hour (= MK/N, constant 14)
- `mk`: machine coefficient (MK/XR)
- `a`: materials coefficient (0.30)
- `l_prime`: employment coefficient (N/XR)
- `l`: labor coefficient (H/XR = 1/xr)

### Table 4.2.4 (`Appendix_4_2_Table4.csv`)
Wide-format merge of the two PDF sub-pages combining per-worker (primed) and per-hour wage costs side-by-side.
- `shift`: shift label
- `XR`: cumulative output (from Table 3)
- `afc`: average fixed cost (d · pMK · mk)
- `ulc_prime`: unit labor cost, wages per worker (wN · l′)
- `avc_prime`: average variable cost, per-worker (ulc′ + pa·a)
- `ac_prime`: average total cost, per-worker (afc + avc′)
- `tc_prime`: total cost, per-worker (ac′ · XR)
- `mc_prime`: marginal cost, per-worker
- `ulc`: unit labor cost, wages per hour (wh · l)
- `avc`: average variable cost, per-hour
- `ac`: average total cost, per-hour
- `tc`: total cost, per-hour
- `mc`: marginal cost, per-hour
- `PL`: total profit, wages per worker (p·XR − tc′)
- `PH`: total profit, wages per hour (p·XR − tc)

## Parameters (book pp. 774, 778, 781)

| Symbol | Value | Meaning |
|---|---|---|
| `a1, a2, a3` | 2, 1.2, 0.05 | Productivity equation coefficients (eq. 4.2.1) — published values; see note below |
| `MK` | 14 | Stock of machines |
| `N` | 1, 2, 3 | Workers per shift (one per machine; cumulative across shifts) |
| `a` | 0.30 | Materials coefficient (constant) |
| `d` | 0.05 | Depreciation rate |
| `pMK` | 100 | Machine price |
| `pa` | 10 | Materials price |
| `wN` | 100 | Wage per worker (per shift) |
| `wh` | 12.5 | Hourly wage rate (note: wh · 8 = 100 = wN, consistent baseline) |
| `p` | 7 | Output price |
| `i` | 1 (Tables 1–2), 0.80 (Tables 3–4) | Intensity of labor |

## Validation

Verbatim transcription, spot-checked against book printed values:

**Table 4.2.1**: h=1 → xr=3.55 ✓, h=12 → xr=9.60 (peak) ✓, h=17 → xr=8.35 ✓, h=20 → xr=6.40 ✓ — all match book exactly.

**Table 4.2.4 derived columns** (recomputed from Table 4.2.3 values using formulas on book p. 781):

| Row | Quantity | Book | Recomputed | Δ |
|---|---|---|---|---|
| XR=2.84 | afc = d·pMK·mk = 0.05·100·4.930 | 24.648 | 24.650 | +0.002 (rounding) |
| XR=2.84 | ulc′ = wN·l′ = 100·0.3521 | 35.21 | 35.21 | 0 |
| XR=2.84 | avc′ = 35.21+3.00 | 38.21 | 38.21 | 0 |
| XR=2.84 | ac′ = 24.648+38.21 | 62.86 | 62.858 | 0 |
| XR=2.84 | tc′ = 62.858·2.84 | 178.52 | 178.517 | −0.003 |
| XR=2.84 | ulc = wh·l = 12.5·0.3521 | 4.40 | 4.401 | +0.001 |
| XR=2.84 | ac = 24.648+7.40 | 32.05 | 32.048 | −0.002 |
| XR=2.84 | tc = 32.048·2.84 | 91.0 | 91.016 | +0.016 |
| XR=2.84 | PL = 7·2.84 − 178.52 | −158.64 | −158.640 | 0 |
| XR=2.84 | PH = 7·2.84 − 91.0 | −71.14 | −71.120 | +0.020 |

All deviations are at the rounding-noise level (≤0.02). The transcription is internally consistent and reproduces every derived column from primary input columns to within published precision.

## Caveats / known discrepancies

1. **Eq. 4.2.1 with published a1=2, a2=1.2, a3=0.05 does NOT reproduce Table 4.2.1 numerically.** Plugging in h=1 gives xr = 2 + 1.2 − 0.05 = 3.15, but Table 4.2.1 has 3.55 (offset +0.40). At h=12, formula gives 9.20, table gives 9.60 (same +0.40 offset). The published parameters are evidently illustrative; the actual tabulated values use slightly different coefficients (likely a1 ≈ 2.40 with a2=1.2, a3=0.05, which back-solves cleanly: 2.40+1.2−0.05=3.55 ✓ and 2.40+14.4−7.20=9.60 ✓). The peak h*=a2/(2a3)=12 still holds; the point of absolute overextension h**=17 still holds.
2. **Implication for downstream loaders**: L01 should consume the tabulated CSVs (Tables 1 and 3) directly rather than re-deriving from eq. 4.2.1 with the published a1=2. If the formula must be used, use back-solved `a1=2.40` (subject to Phase 5 ratification).
3. **XR=0 rows**: marked with blank fields where the original tables show empty cells (productivity, costs, marginal quantities undefined at zero output). `afc` is shown only as the fixed-cost-alone entry `70` in Table 4.2.4 (book's "shaded entry" per text on p. 781). `PL` and `PH` at XR=0 are both −70 (negative of fixed cost).
4. **No interpolation, no rounding, no estimation**: every value reproduces the book PDF verbatim. Where the book leaves a cell blank, we leave it blank (CSV empty field).

## Provenance trail

- Extracted via PyMuPDF (`fitz`) text dump of book PDF pages 810–819
- Cross-verified column-by-column against the linearized text stream
- Validation script: see `Spot check` section above (regenerable from CSVs + parameter values on book p. 781)

## Downstream loaders (Phase 5)

- **S401** (Fig 4.16, per-worker cost curves): reads `Appendix_4_2_Table4.csv` columns `XR`, `afc`, `ulc_prime`, `avc_prime`, `ac_prime`, `mc_prime`
- **S402** (Fig 4.17, per-hour cost curves): reads `Appendix_4_2_Table4.csv` columns `XR`, `afc`, `ulc`, `avc`, `ac`, `mc`
- **S403** (Fig 4.18, profit profiles): reads `Appendix_4_2_Table4.csv` columns `XR`, `PL`, `PH`
- Common upstream: `Appendix_4_2_Table3.csv` supplies the XR sequence and component coefficients (mk, l′, l) underlying Table 4

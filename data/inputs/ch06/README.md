# Chapter 6: The Rate of Profit and Its Components - Anu Chopped Data

**Book Chapter**: Chapter 6, "The General Rate of Profit" (Shaikh 2016, pp. 226-263)
**Figures**: Fig 6.1 through Fig 6.7
**Files**: 10 Anu Chopped CSVs
**Standard**: Anu Chopped v1.0 (Row 1: metadata, Row 2: subseries IDs, Row 3+: data)
**Last Audited**: 2026-02-23 (validator: 10/10 PASS)

---

## File Inventory

| File | Series | Key Columns | Year Range | Table | Extension Source |
|------|--------|-------------|------------|-------|-----------------|
| `Appendix6_Table68I1.csv` | S206 | 55 Shaikh + 14 EXT + 2 COMBINED | 1947-2024 | Table 6.8.I-1 | BEA NIPA T1.7.5, T1.10 |
| `Appendix6_Table68I2.csv` | S207 | 17 Shaikh + 7 EXT + 4 COMBINED | 1947-2024 | Table 6.8.I-2 | BEA NIPA T1.13, T1.14 |
| `Appendix6_Table68I3.csv` | S208 | 51 Shaikh + 5 EXT + 5 COMBINED | 1925-2024 | Table 6.8.I-3 | BEA NIPA T7.11, FA T6.1 |
| `Appendix6_Table68II1.csv` | S209 | 19 Shaikh + 8 EXT + 4 COMBINED | 1925-2024 | Table 6.8.II-1 | BEA FA T6.1-T6.8 |
| `Appendix6_Table68II2.csv` | S210 | 5 Shaikh + 1 EXT + 1 COMBINED | 1925-2024 | Table 6.8.II-2 | BEA FA T6.1 |
| `Appendix6_Table68II3.csv` | S211 | 16 Shaikh + 1 EXT + 1 COMBINED | 1925-2024 | Table 6.8.II-3 | BEA FA T6.1 |
| `Appendix6_Table68II4.csv` | S212 | 6 Shaikh + 1 EXT + 1 COMBINED | 1925-2024 | Table 6.8.II-4 | BEA FA T6.1 |
| `Appendix6_Table68II5.csv` | S213 | 6 Shaikh + 1 EXT + 1 COMBINED | 1925-2024 | Table 6.8.II-5 | BEA FA T6.1 |
| `Appendix6_Table68II6.csv` | S214 | 14 Shaikh + 3 EXT + 3 COMBINED | 1946-2024 | Table 6.8.II-6 | BEA FA + IRS ratio proxy |
| `Appendix6_Table68II7.csv` | S013 | 52 Shaikh + 6 EXT + 6 COMBINED | 1947-2024 | Table 6.8.II-7 | BEA NIPA + FA derived |

---

## Table Structure

Shaikh's Appendix 6.7/6.8 contains a multi-step calculation chain for the rate of profit:

```
Table 6.8.I-1  (S206): GDP/GDI decomposition -> Aggregate and Business NOS
Table 6.8.I-2  (S207): WEQ2 wage-equivalent calculation -> Corporate vs Noncorporate split
Table 6.8.I-3  (S208): Imputed interest adjustment -> Corrected sectoral profit rates
Table 6.8.II-1 (S209): GPIM capital stock estimation (BEA current/constant/historical cost)
Table 6.8.II-2 (S210): GPIM variant - BEA 2011 initial value
Table 6.8.II-3 (S211): GPIM variant - BEA 1993 initial value
Table 6.8.II-4 (S212): GPIM variant - IRS adjusted
Table 6.8.II-5 (S213): GPIM variant - Interwar adjusted
Table 6.8.II-6 (S214): IRS corporate inventories + total capital stock
Table 6.8.II-7 (S013): Final profit rate measures (rcorp, profsh, x1, x2, x3, IROP)
```

---

## Column Structure (Anu Chopped 3-Column Extension Pattern)

Extension columns follow the subsource-level pattern since Ch06 has multi-column tables:

```
Year | S###A (raw subsource 1) | S###B (raw 2) | ... | S###X_EXT (API extension for subsource X) | S###X_COMBINED (spliced)
```

- **S###A through S###ZZ**: Shaikh's original calculation columns (subsources, intermediates, finals)
- **S###X_EXT**: BEA API extension data for subsource X, in native API units
- **S###X_COMBINED**: Spliced series: Shaikh data through 2011 + BEA extension post-2011

**Note**: Unlike Ch02 where each file has one final series, Ch06 files are multi-column calculation worksheets. Extensions target the key output columns needed for downstream calculations.

---

## Series Mapping to Figures

| Series ID | Figure | Description | Key Columns |
|-----------|--------|-------------|-------------|
| S026 | Fig 6.1, 6.4, 6.5 | Sectoral profit rates | S208AW (rcorp), S208AX (rnoncorp) |
| S027 | Fig 6.2, 6.6 | Corrected vs conventional profit rate | S013J (rcorp), S013O (rcorpnipa) |
| S028 | Fig 6.3 | Component ratios x1, x2, x3 | S013P, S013Q, S013R |
| S105 | Fig 6.7 | Incremental rate of profit (IROP) | S013AO (iropcorp), S013AP (iropcorpnipa) |

---

## Extension Methodology

### Data Source
All extension data is pulled from BEA NIPA and Fixed Assets tables via the BEA API using `Technical/scripts/pull_bea_ch06.py`. Pull date: 2026-02-11.

### Splice Approach
1. **Direct continuation**: Where BEA table/line numbers match Shaikh's sources exactly (e.g., T1.10 line 11 for NOS)
2. **Ratio splice**: Where Shaikh used derived calculations, we replicate the formula using current BEA data (e.g., WEQ2, imputed interest adjustment)
3. **Proxy**: Where source data is unavailable via API (e.g., IRS corporate inventories held at constant 2011 ratio)

### Key BEA Tables Used
| BEA Table | Lines | Used For |
|-----------|-------|----------|
| T1.7.5 | 1, 15 | GDP, Statistical Discrepancy |
| T1.10 | 1-23 | GDI components, NOS, CFC |
| T1.13 | 23 | Proprietors' Income |
| T1.14 | 1-11 | Corporate sector accounts |
| T7.11 | 4, 53-54, 74-75 | Imputed interest |
| FA T6.1 | 1-7 | Capital stocks (current-cost net) |
| FA T6.2 | 2 | Capital stocks (chain index) |
| FA T6.3 | 2 | Capital stocks (historical cost) |
| FA T6.4 | 2 | Depreciation |
| FA T6.7 | 2 | Gross investment |
| FA T6.8 | 2 | Investment quantity index |

---

## Extension Data Sources (API)

| API | Table | Line(s) | Description | Used For | Script |
|-----|-------|---------|-------------|----------|--------|
| BEA | T1.10 | 1-23 | GDI components | S206 extensions | `pull_bea_ch06.py` |
| BEA | T1.13 | 23 | Proprietors' Income | S207 WEQ2 | `pull_bea_ch06.py` |
| BEA | T1.14 | 1-11 | Corporate accounts | S207, S208 | `pull_bea_ch06.py` |
| BEA | T7.11 | 4, 53-75 | Imputed interest | S208 adjustment | `pull_bea_ch06.py` |
| BEA | FA T6.1-6.8 | 1-7 | Capital stocks | S209-S213 | `pull_bea_ch06.py` |
| IRS | N/A | N/A | Corporate inventories | S214 (proxy) | Not API-accessible |

**API Key Required**: `BEA_API_KEY` environment variable.
- BEA: https://apps.bea.gov/API/signup/ (free)

**Rebuild workflow**:
```bash
# 1. Pull API data
python Technical/scripts/pull_bea_ch06.py

# 2. Rebuild extensions
python Technical/scripts/rebuild_extensions_ch06.py
```

---

## Validator Exceptions (Documented)

All 10 ch06 files pass the Anu Chopped validator (`validate_chopped.py`). The following warnings are known and intentional:

| Warning | File(s) | Count | Reason |
|---------|---------|-------|--------|
| V2 | All 10 files | ~76 total | Subsource-level extension IDs (`S206A_EXT`, `S207G_COMBINED`, etc.) don't match the base `S###_EXT` regex. These are valid extensions at the subsource level, which is the correct pattern for multi-column Ch06 tables. |

The validator's regex `^S\d{3}_(EXT|COMBINED)$` does not cover subsource-level extensions like `S206A_EXT` or `S207G_COMBINED`. This is a known pattern gap, not a data error.

---

## Calculation Chain Dependencies

The Ch06 tables form a dependency chain. Extensions must be validated in order:

```
S206 (Table I-1: NOS aggregation)
  -> S207 (Table I-2: WEQ2 calculation)
    -> S208 (Table I-3: Imputed interest + profit rates)

S209 (Table II-1: GPIM capital stock)
  -> S210-S213 (Tables II-2 through II-5: GPIM variants)
    -> S214 (Table II-6: IRS inventories + total capital)
      -> S013 (Table II-7: Final profit rate measures)
```

**S013 (Table 6.8.II-7)** is the terminal table producing all published figures. It depends on outputs from both the I-series (profit) and II-series (capital stock) chains.

---

## Known Data Quality Caveats

1. **WEQ2 (S207)**: Self-employment wage-equivalent uses the corporate wage-profit ratio (sigma). Post-2011 sigma is calculated from BEA T1.14 data, which may not match Shaikh's original methodology exactly.
2. **Imputed Interest (S208)**: BEA T7.11 line numbering changed in comprehensive revisions. Extension uses current line numbers — Shaikh's original used pre-2013 line numbers.
3. **GPIM Capital Stock (S209-S213)**: Post-1997 BEA depreciation rates differ from Shaikh's pre-1997 estimates. R&D capitalization (added by BEA in 2013) is included in the extension but was not in Shaikh's original.
4. **IRS Inventories (S214)**: IRS corporate balance sheet data is not available via API. Post-2011 inventories are proxied at a constant 2011 INV/KGC ratio applied to BEA-derived KGC.
5. **x1 Interest Ratio (S013P)**: Extension limited because NMINTcorp from T7.11 requires careful line matching. Frozen after 2013 where data becomes incomplete.
6. **x2/x3 Ratios (S013Q, S013R)**: Depend on IRS inventory proxy. Effectively frozen at 2011 ratio behavior.
7. **Capacity Utilization (S013V, S013W)**: Not extended. Requires HP filter estimation that is outside the scope of simple API extension.
8. **IROP (S013AO-S013AY)**: Partially limited by multi-step dependencies on all upstream extensions.

---

## Cross-Chapter Data References

Chapter 6 final measures appear in Chapter 2:

| Ch02 Figure | Series | Source Table | Ch06 Column |
|-------------|--------|-------------|-------------|
| Fig 2.11 | S013 | Table 6.8.II-7 | S013J (rcorp) |

---

## How to Use This Data

**For the Shiny app**: The `data_loader.R` function loads Ch06 CSVs and extracts the key output columns. The `_COMBINED` columns provide complete series through 2024.

**For extension work**: Compare `S###X` (Shaikh original) and `S###X_EXT` (BEA extension) at the 2011 overlap year. The `_COMBINED` column shows the spliced result.

**For provenance**: Row 1 of each CSV contains full BEA table/line source citations. The `ANU_CHOPPED_CATALOG.json` in the parent directory has machine-readable metadata. API provenance is in `Inputs/API_Data/BEA/provenance.json`.

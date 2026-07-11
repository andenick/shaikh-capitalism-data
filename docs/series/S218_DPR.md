# S218 -- GDP per Capita Richest Four and Poorest Four Countries (Maddison), 1600-2000

**Data Provenance Record (DPR)**

**Series ID**: S218
**Status**: book_period_validated
**Authored**: 2026-05-18
**Author**: Anu Framework pipeline
**Related artifacts**:
- Research dossier: research dossier
- Adequacy: chapter adequacy report
- Extension Provenance Record: extension provenance record
- Registry entry: series registry -> `series.S218`

---

## 1. Definition

Average GDP per capita of the 4 richest countries and 4 poorest countries at each decennial benchmark, plus the ratio (richest4/poorest4). Shaikh excludes Kuwait/Qatar/Venezuela from the top 4 (1950+).

In Shaikh (2016) the series appears as **Figures 2.16 and 2.17** in Chapter 2 ("Turbulent Trends and Hidden Structures").

## 2. Why it matters in Chapter 2

Closes the chapter with a stark quantitative measure of global inequality: the richest-four to poorest-four ratio rises from 7.1 in 1900 to 64.2 in 2000.

## 3. Sources (per subseries)

| Subseries | Coverage | Publisher / Series ID | Native units | Retrieval |
|---|---|---|---|---|
| **S218-A** | 1600-2000 | Maddison (2003) RICHEST 4 with Shaikh exclusions | 1990 GK $/cap | salvaged chopped |
| **S218-B** | 1600-2000 | Maddison (2003) POOREST 4 | 1990 GK $/cap | salvaged chopped |
| **S218-C** | 1600-2000 | Computed ratio | ratio | salvaged chopped (precomputed) |

## 4. Construction

`formula` construction.

**Formula**: `richest4_avg = mean(top 4 excluding KW/QA/VE); poorest4_avg = mean(bottom 4); ratio = richest4/poorest4`

1. Read precomputed RICHEST 4, POOREST 4, RATIO rows from chopped table.
2. Extension: MPD 2023 requires re-applying the exclusion rule (and possibly adding Macao, Luxembourg). Deferred.

## 5. Year coverage

- **Book period**: 1600-2000
- **Extension period**: N/A

## 6. Units

1990 GK $/cap (levels); ratio (S218-C)

## 7. Caveats

1. Shaikh exclusion rule (Kuwait, Qatar, Venezuela from top 4, 1950+) must be reapplied for MPD 2023.
2. Ratio (S218-C) is base-year-invariant; level series (S218-A/B) require rebasing for MPD 2023 splice.
3. Modern panel may need additional exclusions (Macao, Luxembourg) per anu-framework no-proxy rule.

## 8. Cross-references

- Book reference: Shaikh (2016), Ch. 2, Figures 2.16 and 2.17
- Knowledge Base: figure-linkage reference
- Predecessor (CD2): see registry `predecessor_ids` block.

## 9. Validation expectation

- **Tolerance**: +/- 1.0% per year (per playbook).
- **Expected MAE** (vs salvaged book truth): < 0.5% when source data is pulled directly from the chopped table.

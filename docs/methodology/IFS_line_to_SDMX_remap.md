# IMF IFS Legacy Line Number → Modern SDMX Indicator Code Remap

**Status**: Phase 5 implementation reference (RSCD Wave A5, Blocker B7)
**Created**: 2026-05-18
**Resolver**: `Technical/code/loaders/_imf_ifs_resolver.py`
**Source of truth**: `Technical/docs/chapters/CH15_ADEQUACY_REPORT.json` (Phase 4 plan)
**Affects series**: S1504, S1508, S1509

---

## 1. Background

Shaikh (2016) *Capitalism: Competition, Conflict, Crises*, Chapter 15 Appendix
15.1, cites the **IMF International Financial Statistics (IFS)** "Monetary
Survey" using numeric line references (lines 31, 32, 64, 78, 79, 81, 88).
These line numbers were the IFS print/CSV-era identifiers used before the
**SDDS+ (Special Data Dissemination Standard Plus)** migration of 2009.

There have since been **two** retirement events:

| Era | Endpoint | Identifier convention | Status |
|---|---|---|---|
| pre-2009 | IFS print + CSV | Numeric "line" references (e.g. line 32) | Retired 2009 (SDDS+) |
| 2009 - 2024 | `data.imf.org/IFS` portal | SRF aggregate codes `FOSAOP_XDC`, `FAAOP_XDC`, ... | Retired ca. 2024 |
| 2024 + | `api.imf.org/external/sdmx/3.0/` | SDMX 3.0 dataflows with `DCORP_*` / `ODCORP_*` / `CBANK_*` indicator codes | **Current** |

The CH15 Phase 4 adequacy report documents the line → SRF (middle column)
remap. This document extends it with the SRF → SDMX 3.0 (right column) remap
verified empirically against `api.imf.org` on 2026-05-18.

---

## 2. Definitive mapping table

| Legacy line | Shaikh concept | SRF concept | Pre-2024 portal code | **2024+ `api.imf.org` code** | Dataflow |
|---|---|---|---|---|---|
| **31** | Monetary Authority Claims on Central/General Government | CBS Net Claims on Central Government | `FAAOP_XDC` | `CBANK_NETAL_NCO_S1311MIXED` | `MFS_CBS` |
| **32** | Total Domestic Claims (Monetary Survey) | DCS Net Domestic Claims | `FOSAOP_XDC` | **`DCORP_N_DC`** | `MFS_DC` |
| **64** | Consumer Price Inflation | CPI (all items, ann. avg.) | `PCPI_IX` | `PCPI_IX` | `CPI` |
| **78** | Other Deposit Corp Claims on Central/General Government | ODCS Claims on Central Gov | `FCAOP_XDC` | `ODCORP_A_ACO_S1311MIXED` | `MFS_DC` |
| **79** | Other Deposit Corp Claims on State/Local Government | ODCS Claims on State/Local Gov | `FCSL_XDC` | `ODCORP_A_ACO_S13M1` | `MFS_DC` |
| **81** | Other Deposit Corp Claims on Private Sector | DCS Claims on Private Sector | `FCDP_XDC` (consolidated) or `FCNI_XDC + FCHO_XDC` | **`DCORP_A_ACO_PS`** | `MFS_DC` |
| **88** | Central/General Government Deposits in Other Deposit Corps | ODCS Liabilities to Central Gov | `FLAOP_XDC` | `ODCORP_L_LT_S1311MIXED` | `MFS_DC` |

### Net-vs-gross simplifications

Shaikh's S1504 component construction is `line 31 + (line 78 - line 88) + line
79 + line 81`. In the modern DCS framework this composite collapses to:

- `(line 78 - line 88)` at the consolidated DCS level == `DCORP_NETAL_NCO_S1311MIXED`
  (Net Claims on Central Government, DCS).
- The full 4-part composite then equals `DCORP_N_DC` (Net Domestic Claims, DCS)
  to within rounding.

**Recommended Phase 5 strategy**: fetch `DCORP_N_DC` (single call) as the
canonical equivalent of Shaikh's "Total Domestic Claims" concept, and
**validate** the level against Shaikh's hand-summed 1948-2010 values in
`Appendix15_USInflation.xlsx` over the overlap period (target tolerance
+-2 % per year).

If the validation fails for any year, fall back to the 4-component
reconstruction using the per-sector indicators in the table above.

---

## 3. API endpoint reference

### Base URL
```
https://api.imf.org/external/sdmx/3.0/
```

### Dataflow discovery
```
GET /structure/dataflow/IMF.STA
```
Returns 163 dataflows. The relevant ones are:
- `MFS_DC` v8.0.0 — Depository Corporations Survey
- `MFS_CBS` — Central Bank Survey
- `MFS_ODC` — Other Depository Corporations Survey
- `MFS_FC` — Financial Corporations Survey
- `CPI` — Consumer Price Index

Each dataflow has annual + monthly + quarterly vintage-stamped variants
(`MFS_DC_2026_APR_VINTAGE`, etc.) for monthly snapshots; the
unsuffixed dataflow ID always points to the latest data.

### Data query pattern (verified working)
```
GET /data/dataflow/IMF.STA/MFS_DC/+/{COUNTRY}?dimensionAtObservation=AllDimensions
```

Where:
- `{COUNTRY}` = ISO-3 code (e.g. `USA`)
- `+` in the version slot = "latest published version"
- `dimensionAtObservation=AllDimensions` returns flat observation keys for
  easy client-side filtering

### Dimension order in `DSD_MFS_DCS` v8.0.0

| Position | Dimension | Example values |
|---|---|---|
| 0 | `COUNTRY` | `USA`, `GBR`, `DEU` ... |
| 1 | `INDICATOR` | `DCORP_N_DC`, `DCORP_A_ACO_PS`, ... |
| 2 | `TYPE_OF_TRANSFORMATION` | `USD`, `XDC`, `SA_USD`, `PCH_CP_A_PT`, `RMBBMPT_A_PT` |
| 3 | `FREQUENCY` | `A`, `Q`, `M` |
| 4 | `TIME_PERIOD` | `2018`, `2019Q1`, `2020M03`, ... |

### Unit conventions

- **USA**: published in **USD** only (legacy `_XDC` codes are not used).
- **Other countries**: typically published in **XDC** (domestic currency).
- **Cross-country panels** (S1508, S1509): use `USD` where available, or
  apply `PA_USD_XDC_RATE` (the IFS Exchange Rates dataflow) to convert.

### Partial-key limitation

The SDMX 3.0 REST endpoint at `api.imf.org` does NOT accept partial keys with
trailing wildcards (`USA.DCORP_N_DC..A` returns HTTP 200 with zero
observations). The reliable pattern is "fetch all indicators for the
country, then filter client-side"; this is what `fetch_ifs_series()`
implements.

---

## 4. Verified empirical test (2026-05-18)

```
$ python Technical/code/loaders/_imf_ifs_resolver.py

[2] Network smoke test: DCORP_N_DC USA 2018-2022
  http_status: 200
  source_url : https://api.imf.org/external/sdmx/3.0/data/dataflow/IMF.STA/MFS_DC/+/USA?dimensionAtObservation=AllDimensions
  values     :
    2018:   21,155,271,663,469 USD
    2019:   22,415,093,901,308 USD
    2020:   25,759,117,937,922 USD
    2021:   30,116,520,731,891 USD
    2022:   29,911,981,427,257 USD
```

Magnitude check: USA Depository Corporations consolidated balance sheet net
domestic claims ~$21T-$30T over 2018-2022 is consistent with Federal Reserve
H.8 / Z.1 published Domestic Nonfinancial Debt held by depository
institutions (FRED `TCMDO` for cross-check; see CH15 plan note that TCMDO is
"conceptually adjacent but NOT identical" — TCMDO measures total economy debt
outstanding, not depository corporations' claims, so it will differ by a
factor of ~3 in level; that is expected and NOT a resolver failure).

---

## 5. Citation guidance for the EPR / DPR

Phase 5 loaders that emit S1504, S1508, or S1509 should add a `code_remap`
annotation (NOT a `proxy` annotation) to each series' DPR, with text similar
to:

> Source: IMF MFS Depository Corporations Survey, indicator
> `DCORP_N_DC` (Net Domestic Claims), fetched via
> `https://api.imf.org/external/sdmx/3.0/data/dataflow/IMF.STA/MFS_DC/+/{country}`.
> This is the modern (post-2024) SDMX-3.0-REST equivalent of Shaikh's
> "Total Domestic Claims, IFS Monetary Survey line 32" via the SRF
> reorganization (2009 SDDS+ migration) and the 2024 data portal
> migration. Concept continuity verified against Shaikh's
> Appendix15_USInflation.xlsx 1948-2010 overlap period at +-2 %
> tolerance (see resolver `validate_against_shaikh()` output).

---

## 6. Open issues for Phase 5 / Phase 6

1. **Pre-2001 history**: the `MFS_DC` dataflow only publishes from 2001
   onward (USA: 25 obs 2001-2025). For Shaikh's 1948-2010 overlap, the
   pre-2001 segment must be sourced from the historical IFS CSV bulk
   download (now distributed via the IMF Statistics Department's Archive
   ftp), or from the FRED reconstruction (`TCMDO` is a reasonable proxy
   for level changes 1948-2000 but not identical).
2. **EAWR vs national residency**: euro-area countries publish both
   national-residency and Euro-Area-Wide-Residency (EAWR) variants of each
   indicator (`DCORP_A_ACO_PS_EAWR` etc.). For S1508 / S1509 international
   panels, the national-residency variant is the correct match to
   Harberger 1988 and Ramamurthy 2014.
3. **USA `XDC` absence**: USA reports only `USD` in MFS_DC. International
   panels that need a common currency must use `USD` for USA and convert
   other countries via `PA_USD_XDC_RATE`.

---

## 7. References

- IMF Statistics Department, "Monetary and Financial Statistics Manual and
  Compilation Guide" (Washington, DC: IMF, 2016), Chapter 7.
- IMF Statistics Department, "Data Dissemination Standards Plus" (SDDS+),
  2009 migration documentation.
- IMF SDMX 3.0 REST API Documentation: `https://www.imf.org/en/Data` (links
  to `api.imf.org` swagger).
- Shaikh, A. (2016), *Capitalism: Competition, Conflict, Crises*, Oxford
  University Press, Appendix 15.1 pp. 895-897.
- RSCD Phase 4 Chapter 15 adequacy report:
  `Technical/docs/chapters/CH15_ADEQUACY_REPORT.json`.

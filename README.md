# Capitalism: Competition, Conflict, Crises — Data Replication Package

**Complete replication and extension of all 113 empirical data series from Anwar Shaikh's *Capitalism: Competition, Conflict, Crises* (Oxford University Press, 2016), with extensions through 2025 using public government APIs.**

---

## Key Findings

| Measure | 1966 (peak) | 1982 (trough) | 2007 (pre-crisis) | 2024 (extended) |
|---------|-------------|---------------|-------------------|-----------------|
| Corporate profit rate (r = NOS/K) | 17.1% | 5.5% | 9.9% | 10.7% |
| Manufacturing productivity index | 100 (1958=100) | 217 | 570 | 660 |
| US unemployment rate | 3.8% | 9.7% | 4.6% | 4.0% |
| Real investment index | 100 (1958=100) | 350 | 973 | 1,975 |
| Industrial production index | 100 (1958=100) | 213 | 486 | 520 |

The secular decline in the corporate profit rate — from 17.1% at the Golden Age peak to 5.5% at the neoliberal trough, with partial recovery to ~10% — is the central empirical finding. Shaikh argues this reflects the inherent dynamics of capital accumulation, not policy failure. See Chapters 6 and 16 of the book for the full theoretical argument.

---

## Quick Start

```bash
git clone https://github.com/andenick/shaikh-capitalism-data.git
cd shaikh-capitalism-data
pip install -r requirements.txt
python replicate.py --dry-run          # Show the processing plan
python replicate.py                    # Run the full pipeline (~1 second)
```

API keys (free registration) are needed only for series that fetch live data from FRED and BEA. See [INSTALL.md](INSTALL.md) for setup. The included data files allow immediate validation without API keys.

---

## What This Replicates

Anwar Shaikh's *Capitalism* (2016) is a comprehensive treatise on the dynamics of capitalist economies, grounded in 161 years of US data across 113 empirical series. The book's central argument — that the rate of profit has a persistent downward tendency, modulated by cyclical fluctuations and counteracting factors — rests on meticulous data construction from BEA, BLS, FRED, OECD, and other public sources.

This package:

1. **Replicates** every data series from the book's appendices (Chapters 2, 5–17), reconstructing each from its original government sources
2. **Extends** 79 of 96 processable series to the present (2019–2025) using the same public APIs Shaikh used
3. **Validates** every value against the book's published tables — 1,126 reference value checks, all passing; 99.89% raw data faithfulness across 15,173 cells

The remaining 17 un-extended series are genuinely non-extendable: cross-sectional snapshots (IO tables, income distributions), fixed historical windows (1955–1970 Phillips curves), or theoretical diagrams.

---

## Data Sources

All data is publicly available. No proprietary or private datasets are required.

| Source | Institution | API | Registration | Series Used |
|--------|-----------|-----|-------------|-------------|
| FRED | Federal Reserve Bank of St. Louis | `fredapi` | [Free key](https://fred.stlouisfed.org/docs/api/api_key.html) | INDPRO, GPDIC1, OPHMFG, UNRATE, COMPRMS, DGS10, AAA, CMDEBT, FODSP, +20 more |
| BEA NIPA | Bureau of Economic Analysis | BEA REST | [Free key](https://apps.bea.gov/api/signup/) | Tables 1.14, 7.11, 1.13, Fixed Assets |
| BEA GDP-by-Industry | Bureau of Economic Analysis | BEA REST | Same key | Table 6 (GOS), Table 16 (Gross Output) |
| MeasuringWorth | Officer & Williamson | Manual download | None | CPI (1774–present), GDP (1790–present) |
| World Bank WDI | World Bank | Open API | None | Argentina GDP, exchange rate, credit |
| OECD STAN | OECD | SDMX API | None | Industry value added, capital formation |
| Penn World Table | Groningen | Excel download | None | PPP conversion factors (10.01) |
| Damodaran | NYU Stern | Excel download | None | S&P 500 total return (1928–2025) |
| Maddison Project | Groningen | Excel download | None | GDP per capita (1710–2022) |
| Shiller | Yale | Excel download | None | Stock price, dividends, CPI |

---

## Repository Structure

```
shaikh-capitalism-data/
├── replicate.py               Master orchestrator
├── requirements.txt           Python dependencies
├── LICENSE                    MIT (code) + CC-BY-4.0 (data)
├── CITATION.cff               Citation metadata
├── INSTALL.md                 Setup guide
│
├── config/
│   ├── registry.json          Series registry (single source of truth)
│   ├── chapters.json          Chapter metadata + dependency graph
│   └── api_keys.env.example   Template for API keys
│
├── loading/                   Phase 1: Parse source data
│   └── ch02.py ... ch17.py   One module per chapter
│
├── processing/                Phase 2: Construct + extend series
│   └── ch02.py ... ch17.py   One module per chapter
│
├── lib/                       Shared library
│   ├── extension.py           Centralized extension engine
│   ├── registry.py            Registry loader
│   ├── fetchers/              API clients (FRED, BEA, World Bank, OECD)
│   ├── transforms/            Reindex, splice, HP filter, aggregate
│   └── formats/               Chopped CSV, Extenbook Excel writers
│
├── data/
│   ├── inputs/                Shaikh's original appendix data (READ-ONLY)
│   │   └── ch02/ ... ch17/   Organized by chapter
│   └── output/                Pipeline output
│       ├── series/            Final single-column CSVs (96 series)
│       └── chopped/           Multi-column CSVs with subseries
│
└── docs/
    ├── ASSUMPTIONS.md         Methodological assumptions
    ├── DECISION_LOG.md        Design decisions with rationale
    └── series/                Per-series documentation
```

---

## Series Coverage

| Chapter | Series | Content | Period |
|---------|--------|---------|--------|
| Ch 2 | S001–S017 | Industrial production, investment, GDP, unemployment, productivity | 1780–2025 |
| Ch 5 | S010–S025 | Gold prices, wholesale price indexes (US, UK) | 1780–2025 |
| Ch 6 | S013–S214 | Corporate profit rate, corrected profitability, IROP, component ratios | 1947–2024 |
| Ch 7 | S034–S038, S215–S225 | US and OECD industry profit rates, IROPs, deviations | 1987–2019 |
| Ch 8 | S841–S846 | Bain, Semmler, Stigler, Demsetz cross-sectional industry data | 1936–1956 |
| Ch 9 | S047–S049 | Input-output prices, wage-profit curves | 1947–1998 |
| Ch 10 | S040–S059 | Interest rates, bond/equity returns, warranted stock price | 1857–2025 |
| Ch 11 | S060–S063, S200–S201 | Trade balances, real exchange rates, law of one price | 1960–2025 |
| Ch 12 | S064–S067, S203 | Phillips curves (multiple periods) | 1948–2025 |
| Ch 14 | S068–S075, S202 | Classical Phillips curves, wage share, unemployment intensity | 1948–2026 |
| Ch 15 | S076–S092, S225 | CPI, industry growth rates, inflation, Argentina credit/GDP | 1774–2025 |
| Ch 16 | S093–S101, S220–S224 | Golden waves, wage suppression, debt ratios, OECD interest rates | 1786–2025 |
| Ch 17 | S102–S104 | Income distribution, global crisis comparison | Cross-sectional |

**96 processable series | 79 extended | 1,126 reference value checks | 0 failures**

---

## Validation

| Check | Description | Result |
|-------|-------------|--------|
| V01 Reference Values | 1,126 values from Shaikh's appendices | **1,126/1,126 PASS** |
| V05 Cross-Series | 122 consistency checks between related series | **122/122 PASS** |
| V08 Hash Integrity | SHA-256 checksums on all output files | **288/288 PASS** |
| V09 Exhaustive | 15,173 raw data cells compared value-by-value | **99.89% exact match** |

The 0.11% non-exact cells are in reindexed subseries where the output correctly applies a base-year transformation that changes the raw value — these are correct transformations, not errors.

---

## Citation

```bibtex
@book{shaikh2016capitalism,
  author    = {Shaikh, Anwar},
  title     = {Capitalism: Competition, Conflict, Crises},
  publisher = {Oxford University Press},
  year      = {2016},
  isbn      = {978-0199390632}
}
```

See [CITATION.cff](CITATION.cff) for this replication package's citation metadata.

---

## Requirements

- **Python 3.10+**
- **API keys** (optional, for live data fetching): FRED, BEA (free registration)
- **Disk**: ~15 MB (repository) + ~5 MB (computed outputs)
- **Time**: ~1 second for full pipeline run

# anu/dpr — Data Provenance Records

Per-source and per-family provenance for the replication package.

| Doc | Source / family | Fetcher |
|---|---|---|
| [D01_fred_dpr.md](D01_fred_dpr.md) | FRED (St. Louis Fed) — primary live-extension source | L01 |
| [D02_bea_dpr.md](D02_bea_dpr.md) | BEA (API + salvaged historical tables) | L02 |
| [D03_worldbank_dpr.md](D03_worldbank_dpr.md) | World Bank Open Data | L03 |
| [D04_imf_weo_dpr.md](D04_imf_weo_dpr.md) | IMF WEO/IFS/MFS + BLS ILC | L04 |
| [D05_census_ft900_dpr.md](D05_census_ft900_dpr.md) | U.S. Census FT-900 foreign trade | L05 |
| [D06_shiller_dpr.md](D06_shiller_dpr.md) | Shiller (Yale) long-run data | L06 |
| [D07_damodaran_dpr.md](D07_damodaran_dpr.md) | Damodaran (NYU Stern) returns | L07 |
| [D08_bundled_salvaged_inputs_dpr.md](D08_bundled_salvaged_inputs_dpr.md) | Bundled book-period inputs (SalvagedInputs) | L08 |
| [D09_series_families_dpr.md](D09_series_families_dpr.md) | Series-family index → per-series DPRs in `docs/series/` | — |

The 118 per-series DPRs and EPRs live in [`docs/series/`](../../docs/series/)
(one pair per series). Machine-readable subsource provenance lives in
[`SUBSOURCE_METADATA.json`](../../SUBSOURCE_METADATA.json) at the repo root.

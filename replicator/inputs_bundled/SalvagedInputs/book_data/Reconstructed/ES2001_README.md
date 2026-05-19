# ES2001 Reconstructed Data

Source: Shaikh (2020), "An Empirically Sufficient Form for Sraffa Prices",
Tables 1 and 2 (paper p. 10).

## Files

- `ES2001_aggregate_ratios.csv` — Tables 1 (circulating capital) and 2 (fixed
  capital) merged into a single long-form table. Each row is one
  (model, year, aggregate) triple. Values are price/value ratios at the
  observed rate of profit. Per Shaikh's Section 3, these ratios all fall
  in [0.94, 1.08] across both models and all six benchmark years
  (1947, 1958, 1963, 1967, 1972, 1998).

## Columns

| Column | Description |
|---|---|
| `model` | `circulating` (Table 1) or `fixed` (Table 2) |
| `year` | Benchmark year |
| `matrix_size` | 71 for 1947-1972 (BEA historical detailed IO), 65 for 1998 |
| `r_obs` | Observed rate of profit |
| `r_obs_over_R` | r_obs / R (profit-rate share of maximum) |
| `constant_capital`..`max_rate_profit_R` | Aggregate price-to-value ratios |

## Provenance

Verbatim transcription of Tables 1 and 2 from the published PDF
`[2020] Shaikh - An Empirically Sufficient Form for Sraffa Prices.pdf`
(SalvagedInputs / Shaikh Publications). The PDF is also the canonical
URL-of-record substitute since `anwarshaikhecon.org` was DNS-unreachable
at the time of Phase 4 (decision 0005).

The two paper averages reported in the right-hand "Average" columns of
Tables 1 and 2 are computed across the six benchmark years; they can be
re-derived from this CSV.

## What this does NOT cover

The paper's Figures 1-9 (illustrative 403-sector price-value curves,
Bienenfeld linear/quadratic approximations, wage-profit curve,
output-capital ratio) require regenerating the 2002 403-order BEA Use/Make
matrix and solving Sraffa prices `p(r) = (1-r/R) v + r p(r) H`. That
regeneration is deferred — see `ES2001_EPR.md` for the rationale and
v1.1 plan. The aggregate-ratio extraction here is the empirical time
series content of the paper that is directly auditable against the printed
tables.

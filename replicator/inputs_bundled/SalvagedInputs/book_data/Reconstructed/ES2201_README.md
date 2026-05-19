# ES2201 Reconstructed Data

Source: Shaikh & Jacobo (2020), "Economic Arbitrage and the Econophysics
of Income Inequality", Review of Behavioral Economics 7: 1-17. Table 1
(paper p. 5).

## File

- `ES2201_fitted_parameters.csv` — five jointly-fitted parameters of the
  two-class econophysics model for US individual income, tax years
  2002-2016. Each row is one tax year; columns are the five Table 1
  parameter estimates.

## Columns

| Column | Symbol | Description | Units |
|---|---|---|---|
| `year` | t | IRS tax year | year |
| `G_prime` | G' | Gini coefficient of the bottom 97% (Brooks midpoint method) | dimensionless |
| `r_mean` | <r> | Overall average AGI per return (total AGI / total returns) | thousands USD |
| `w_mean` | <w> | Bottom-97% mean income / "income temperature" (MLE of ln C(r) slope) | thousands USD |
| `f_top3` | f | Top-3% income share, derived as 1 - <w>/<r> | dimensionless |
| `alpha` | alpha | Top-3% power-law exponent (MLE of ln C(r) vs ln r) | dimensionless |

## Provenance

Verbatim transcription of Table 1 from the published PDF
`[2020] Shaikh & Jacobo - Economic Arbitrage and the Econophysics of
Income Inequality.pdf` (SalvagedInputs / Shaikh Publications). The
underlying IRS SOI Publication 1304 Table 1.4 and Table 1 are
US Federal Government public-domain sources (17 USC 105) and the paper's
five parameters are jointly fitted per the MLE protocol described in
the paper appendix.

## What this does NOT cover

Figures 1, 2, 3 (cumulative-probability plots for tax year 2011) are
illustrative snapshots, not time-series, and require re-fetching the
raw 2011 IRS Table 1.4 binned data to reproduce. Per the paper note,
the time-series content of the paper IS Table 1 (transcribed here).

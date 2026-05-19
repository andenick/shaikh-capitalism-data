# Codebook Column Reference

This file explains every column in `CD2_Codebook_v1.3.csv`. The codebook has one row per series and is the index for the rest of the package.

## Columns

| Column | Meaning | Example |
|---|---|---|
| `series_id` | The package's identifier for the series. Of the form `S###` (S001, S002, ...). Used to name the per-series Excel workbook in `Series/`. | `S001` |
| `name` | Human-readable series name as it appears in the book and in figures. | `US Industrial Production Index` |
| `definition` | One-line description. In most series this matches `name`; for derived series (ratios, deviations) it clarifies what is being computed. | `US Industrial Production Index` |
| `units` | The units of the constructed series. Common forms: `Index YYYY=100`, `percent`, `ratio`, `billions_usd`, `Current dollars`. | `Index 1958=100` |
| `frequency` | Time-step of the data: `annual`, `quarterly`, or `monthly`. All published series in this package are `annual` (monthly/quarterly source data is aggregated to annual averages). | `annual` |
| `coverage_start` | First year covered. | `1860` |
| `coverage_end` | Last year covered (includes any modern extension). | `2026` |
| `n_observations` | Count of non-missing annual observations. | `167` |
| `content_type` | Classification of what kind of data this is. One of: `time_series` (a sequence of values indexed by year), `cross_sectional` (a single year's snapshot across industries or countries — does not get extended), `theoretical` (a diagram or formula illustration with no underlying empirical data), `derived` (computed from other series in this package). | `time_series` |
| `chapter` | The chapter of Shaikh (2016) in which this series appears. | `2` |
| `figures` | The figure(s) in the book that use this series. Multiple figures separated by comma. | `Fig2.1` |
| `source_primary` | The original public source as used by Shaikh. Includes the publication, table number, and base year where relevant. | `BEA LTEG 1860-1970, TA15 p.185` |
| `source_extension` | The public source used to extend the series beyond the book's original range. Blank for series that are not extended. | `FRED INDPRO` |
| `extended` | `Yes` if the series has been extended beyond the book's original range; `No` otherwise. Some series are deliberately not extended — see the per-series workbook for the reason. | `Yes` |
| `splice_year` | The year at which the historical source and the modern extension are joined. Blank for non-extended series. | `2010` |
| `notes` | Free-text notes when the construction or extension required a non-routine choice. Most rows are blank. | (empty) |

## Where to read more

- Open the matching `Series/S###_*.xlsx` workbook for full provenance (sources, transformations, research notes, construction methodology, validation values).
- Open `CD2_Methodology_v1.3.pdf` for the full methodological narrative across all series.
- `CD2_All_Series_v1.3.xlsx` is the flat data file with one column per final series.

## On series identifiers

Within the per-series workbooks you will encounter dash-suffixed identifiers:

- `S001-A`, `S001-B`, … — raw historical sources (segments of the series, each from a distinct publication).
- `S001-EXT` — modern API extension (post-book values).
- `S001-COMBINED` — the spliced final series joining the historical segments with the modern extension.
- `S001-F` — extension data re-indexed to match the historical segment at the splice year (used in the visualization to show the extension on the same scale as the historical data).
- `CS###-N`, `CS###-D` — for ratio/rate series, the numerator and denominator components. The parent series `S###` is the ratio.

The bare identifier `S001` (no suffix) is always the final published series — the one that appears in the book's figure and in `CD2_All_Series_v1.3.xlsx`.

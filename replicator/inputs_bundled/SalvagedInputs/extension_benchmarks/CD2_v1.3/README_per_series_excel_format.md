# Per-Series Excel Workbook Format

Every file under `Series/` (e.g. `S001_us_industrial_production_index.xlsx`) is one constructed data series. Each workbook contains four sheets, each answering a different question.

## The four sheets

### 1. Data

The constructed values themselves, year by year.

- **Column 1:** Year.
- **Columns 2–N:** The series components. Column headers use the `S###-LETTER` notation explained at the end of this file. The final column (no suffix) is the published series — the same values plotted in the book's figure.

If the workbook covers an extended series, the modern API extension appears as a `-EXT` column and the joined version as a `-COMBINED` column.

### 2. Provenance

Where the data came from. Documents:

- The original publication and table number for each historical segment.
- The public URL of the modern data source used for extension (where applicable).
- The DARP / OCR extraction note when text or tables were extracted from a PDF rather than downloaded directly from a public database. (DARP is a multi-engine PDF-extraction protocol; errors are possible and are flagged here.)

### 3. Research

Verbatim quotes from the book's appendix describing how Shaikh originally constructed the series. Use this sheet when you want to know "what does the book say, in Shaikh's own words, about this series?"

### 4. Construction

The step-by-step transformation chain that turns the raw historical sources into the final published series. Each row is one operation: `load`, `reindex`, `splice`, `aggregate`, or `calculate`. Reading this sheet top-to-bottom tells you exactly how the series was built.

---

## Header notation

Within the Data sheet, column headers follow this convention:

| Header | What it is |
|---|---|
| `S001-A`, `S001-B`, … | Raw historical sources. Each letter is a distinct publication or segment. |
| `S001-EXT` | Modern API extension (values added after the book's original range). |
| `S001-COMBINED` | The spliced final series joining historical segments with the modern extension. |
| `S001-F` | Extension data re-indexed to match the historical segment at the splice year. |
| `CS001-N`, `CS001-D` | For ratio/rate series, the numerator and denominator components. The parent `S001` is the ratio. |
| `S001` | The final published series — the values plotted in the book's figure. |

## On reindexing

When a header reads "reindexed to 1958 = 100" or shows units like `Index 1958=100`, every value in that column has been scaled so that the year 1958 equals 100. This is the base year used in Shaikh (2016) for cross-series comparability. The raw source may have used a different base (e.g. 1913=100 or 2017=100); the reindexed column preserves the source's growth rates while shifting the level so the units are comparable across the package.

## On splicing

When historical data ends in year Y and a modern API takes over, the two segments are joined at Y so the combined series has consistent scale. Two splice methods are used:

- **growth_rate splice** — preserves period-to-period growth across the join. `combined[t] = historical[Y] * (modern[t] / modern[Y])` for `t > Y`. Used when the modern source's level may differ from the historical source's level (e.g. a different base year or methodological revision) but its growth rates are trustworthy.
- **direct splice** — uses the modern values as-is. Used when source units already match.

The splice method and splice year are recorded on the Provenance sheet of every extended series.

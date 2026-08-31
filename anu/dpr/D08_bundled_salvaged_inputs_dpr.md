# D08: Bundled Book-Period Inputs (SalvagedInputs) — Data Provenance Record

## What this covers
The frozen book-period ground truth: Shaikh's own chopped tables and working
spreadsheets, historical statistical compendia, and literature tables that
cannot be re-downloaded today. This is the largest source family — 76
subsources serving 96 series.

## Source
- **Name**: SalvagedInputs (bundled inside this repository)
- **Location**: `replicator/inputs_bundled/SalvagedInputs/` (shipped with the
  repo; no download required)
- **License**: mixed — underlying U.S. federal statistics are public domain;
  Shaikh's workbooks are copyright OUP, redistributed here for replication
  with attribution (see repo LICENSE and CITATION.cff)
- **Retrieved**: frozen at salvage time; provenance per subsource in
  `SUBSOURCE_METADATA.json`
- **Format**: XLSX chopped tables, CSV, staged transcriptions

## What is in it (by origin)
| Origin | Examples |
|---|---|
| Shaikh's companion materials (anwarshaikhecon.org — now offline; preserved via Wayback Machine) | Appendix chopped tables, working spreadsheets for Ch. 7, 15, 16 |
| Shaikh / Ochoa (1994) worksheets | Power of labour / power of capital constructions for Ch. 7 |
| Historical statistical compendia | BEA Long Term Economic Growth 1860–1965; Cleveland Trust (Ayres); NBER/FRB/ERP series |
| Jastram / MeasuringWorth | Pre-Federal-Reserve price and metallic-currency series |
| Ibbotson Associates | Early bond/equity return yearbooks feeding Ch. 10 |
| Literature compilations | Christodoulopoulos, Tsoulfidis & Tsaliki, Allen & Bowley 1935, Salter 1969, Stigler 1963, Inman 1952, Eiteman & Guthrie 1952 |
| Author constructions | Appendix 4.2 illustrative cost curves, Appendix 6.8 wage-share panels, NetLogo simulation outputs |

## Construction method
Per-series loaders read the bundled workbooks directly (see
`code/L01_loaders/`). Nothing in this family requires network access: the
book period reproduces offline. Where a table was only available as a figure,
digitisation provenance is recorded (`pdf_vector_digitization` in
SUBSOURCE_METADATA).

## Transformations applied
- byte-exact transcription where the book table is the source of truth
- reindexing to the book's base year where the salvaged table differs
- staging markers for tables transcribed from scans (md5 recorded)

## Known issues
- The hosting site anwarshaikhecon.org is offline (DNS dead at salvage time);
  the bundled copies with Wayback provenance are the only stable source.
- Two series remain `data_unavailable` (see registry `quality.status`) — no
  synthetic values were fabricated to fill them.
- Scanned-table transcriptions carry per-table fidelity flags in
  SUBSOURCE_METADATA.

## Validation
Book-period values are the reference: V03 validators compare constructed
output against these tables at certified spot-check years (tolerance 1%).
V01 package gate checks presence/coverage/units of the final chopped output.

## Series served
See `python anu/scripts/L08_load_bundled_inputs.py --list`.

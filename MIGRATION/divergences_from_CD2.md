# RSCD Divergences from CD2

**Created**: 2026-07-10 (F-3D-02, P4.3 docs batch)
**Purpose**: Consolidated registry of documented divergences from the CD2 predecessor
project. Every row records where RSCD intentionally differs from CD2 and why.
**Sources consolidated**: `Technical/docs/decisions/` (RSCD-0001 through RSCD-0019),
`MIGRATION/CD2_to_RSCD_crosswalk.csv` (notes column), `docs/reviews/DEVIATION_TRIAGE.md`.
**Promise**: `INPUTS_README.md` states that CD2 series not brought forward have a recorded
reason; every unmapped CD2 series below satisfies that promise.

---

## Divergence Table

| Series (RSCD) | CD2 ID | Divergence | Direction | Rationale | Decision ref |
|---|---|---|---|---|---|
| XS001–XS009 | AS001–AS009 (CD2 S206–S214) | ID prefix changed AS→XS; chapter 6 GPIM construction internals re-classed as XS appendix | CD2→RSCD | GPIM internals are analytical constructs, not primary book series; XS prefix avoids flat-S namespace collision and signals derivation from S6xx series | RSCD-0002, RSCD-0015 |
| XS2001, XS2101, XS2201, XS2301–XS2305 | ES2001, ES2101, ES2201, ES2301–ES2305 (not in CD2) | ID prefix changed ES→XS; study series re-classed as XS external_study | CD2→RSCD | AS/ES prefix families retired in XS migration (2026-06-10); single XS family simplifies routing | RSCD-0001; MIGRATION/crosswalk.csv |
| S214, S215 | n/a (not in CD2) | New series (extension-only); status = extension_only_validated | New in RSCD | CD2 did not cover S214/S215; RSCD adds IRS corporate inventories + total capital stock as XS009 precursor components; S214/S215 are book-period-absent extension-only series | RSCD-0002 |
| S207 | CD2 S007 | Source updated: BLS discontinued; alternative spliced | RSCD extends | CD2 used the original BLS Manufacturing Productivity and Real Wages series (discontinued); RSCD decision to defer until Phase 4 adequacy | RSCD-0005 |
| S703, S704 | CD2 not present (CD had S032/S033) | Machine digitization recovery (2026-07-02); from data_unavailable → book_period_validated | RSCD extends | CD2 had no coverage; RSCD recovered the Christodoulopoulos Fig 7.13/7.14 aggregate lines by dual-extraction machine digitization under Decision 0019 | RSCD-0018, RSCD-0019 |
| S707 | CD2 S038 (OECD IROP — wrong mapping) | Content mismatch corrected: S707 = Greek manufacturing (Tsoulfidis & Tsaliki 2011, Fig 7.19); CD2 S038 was OECD IROP (Fig 7.21 content, now in S711) | RSCD corrects | CD2 crosswalk mapped S038 to S707 based on a stale wrong registry name; corrected in Phase 3. S707 predecessor is null; S711 is the true S038 successor | RSCD-0003 |
| S711 | CD2 S038 (correct mapping) | S711 = OECD IROP deviations (Fig 7.21, 1988–2003); inherits CD2 S038 methodology | CD2→RSCD | New series ID per RSCD chapter-encoding scheme; content is faithful to CD2 S038 per series research dossier | RSCD-0004 |
| S801 | CD2 S042 (false match) | S801 = Eichner 1973 wholesale-price chart (Fig 8.1, 1965–1973); CD2 S042 was Ch10 Jastram long-run interest-rate series | RSCD corrects | CD2 S042 mapped to S801 based on a false name match in HDARP_SERIES_LINKAGE.json; predecessor_ids nulled | RSCD-0003, CD2_to_RSCD_crosswalk.csv notes |
| S803 | CD2 S041 (false match) | S803 = Bain 1951 QJE profit-rate-on-equity vs CR8 (Fig 8.3/8.4, 42 industries 1936–1940); CD2 S041 was Ch10 interest-rate/price series | RSCD corrects | False name match; predecessor_ids nulled | RSCD-0003, CD2_to_RSCD_crosswalk.csv notes |
| S709, S710 | CD2 S035, S037 | Series type in crosswalk was recorded as 'promoted to AS series per decision 0002' — incorrect | RSCD corrects | S709/S710 are standard S-series US deviation panels (Figs 7.16/7.18); only XS001–XS009 were promoted per RSCD-0002. Crosswalk note was a mis-reference; S-series designation stands | RSCD-0002; CD2_to_RSCD_crosswalk.csv notes |
| chopped_format | CD2 wide | Long-form chopped (year, value, subseries_id, source_id, units) | RSCD narrows | Long-form is canonical per Decision 0005; wide-form from CD2 is NOT supported | RSCD-0005 |
| `reference_values` in registry | CD2: not required | Required in RSCD for all validated series; round-trip-against-XLSX is not a substitute | RSCD adds | Auditability requirement; Decision 0002 | RSCD-0002 |
| `extension` block | CD2: not enforced | Required for any series with -EXT subseries (binary invariant) | RSCD adds | Decision 0003; B22 cleanup populated ES series; all new extensions must carry full 6-field extension block | RSCD-0003 |
| `status: ingested` | CD2: allowed | Banned in RSCD; remapped to book_period_validated / study_complete / data_unavailable | RSCD removes | Non-canonical value; removed in v1.0.1 (101 series remapped) | CLAUDE.md anti-pattern #3 |
| S1004 HP lambda | CD2: lambda=3 (book-cited) | RSCD: lambda=100 (standard annual HP parameter actually implemented) | RSCD corrects | Book p. 467 states 'parameter = 3' but the pipeline uses lambda=100; dossier formula corrected 2026-07-10 per F-2E-02 | RSCD-0008 (S1004 adequacy) |
| Unmapped CD2 series (S020, S021, S051, S058, S064–S067, S080–S092, S094–S098, S096, S200–S203 (CD2 numbering), S215–S217 (CD2), S220–S225, S840–S846) | Various | Not brought forward into RSCD | CD2→RSCD gap | No figure linkage found in CD HDARP_SERIES_LINKAGE.json (see crosswalk notes column 'unmapped'); either duplicate tables, source-only tables without a figure series, or figures not in scope for v1.0 | CD2_to_RSCD_crosswalk.csv (unmapped rows) |
| S1301 status | CD2: not present | RSCD: theoretical_validated (new status class per TD.4) | RSCD adds | S1301 is a purely theoretical illustration (eq. 13.43 random walk with drift); new status class theoretical_validated introduced 2026-07-10 to avoid book_period_validated inflation | TD.4 (anu-ingestion v5.3) |
| DEVIATION_TRIAGE benign large-pct-err series | CD2: not documented | RSCD: 9 series with max_pct_err > 5% documented as benign in DEVIATION_TRIAGE.md | RSCD adds | 7 theoretical model figures (S301–S309 subset) + 1 near-zero-denominator artifact (S1004); all are expected, not data errors | docs/reviews/DEVIATION_TRIAGE.md |

---

## Notes

1. **Sources per row**: Decision refs are `Technical/docs/decisions/RSCD-{NNNN}_*.md`
   (using RSCD- prefix per Decision RSCD-0020 / TD.5 namespace convention; existing files
   with bare integer names are cited as `RSCD-{NNNN}` without physical rename).
2. **CD2 crosswalk notes column**: `MIGRATION/CD2_to_RSCD_crosswalk.csv` carries a `notes`
   column per row; the most informative notes are condensed here.
3. **INPUTS_README.md promise**: "Every CD2 series not mapped to an RSCD series has a
   documented reason." This table + the crosswalk notes together satisfy that promise.
4. **This file is authoritative; do not edit without a dated note.**

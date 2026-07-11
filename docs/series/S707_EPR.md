# S707 — Extension Provenance Record

**Series**: S707 — Figure 7.19 — Greek Manufacturing Profit-Rate Deviations, 1962–1991 (Tsoulfidis & Tsaliki 2011 Fig 4)

**Construction classification**: `digitized` (book-period figure digitization — recovered 2026-05-26; supersedes the earlier `data_unavailable` classification)
**Extension method**: not applicable — no faithful time-extension exists (see §2)
**Authored**: 2026-05-18 · **Recovery update**: 2026-05-26
**Author**: Anu Framework pipeline
**Related**: `S707_DPR.md`

---

## 1. Classification

`provenance = digitized`, `status = book_period_validated`. This exhibit was **recovered by offline
figure digitization**: the plotted coordinates of Tsoulfidis & Tsaliki (2011) Figure 4 — the
20-industry profit-rate-deviation grid Shaikh reproduces as Fig 7.19 — were read directly off the
vector-drawn chart in the paper's full text (MPRA working-paper 51334, 2013 revised version),
per-panel calibrated to each panel's own axis ticks, and clipped to Shaikh's 1962–1991 window.
Method, validation and caveats are documented in the DPR (`S707_DPR.md` §0) and the extraction
report (Tsoulfidis-Tsaliki extraction worklog). There is a recovered book-period
dataset; there is no byte-exact underlying table to *extend* (that remains obtainable only from the
original authors).

## 2. Why no time-extension is attempted

- The digitized panel reproduces the published figure faithfully but is not the authors' exact
  tabulated data, and Tsoulfidis & Tsaliki did not redistribute the raw 1962–1991 series.
- The closest modern source (ELSTAT — the Greek statistical service, successor to ESYE — for the
  post-2010 Greek track) has incompatible industry classifications, capital-stock coverage, and a
  2010 ESYE→ELSTAT methodology break.
- Any modern panel would be a methodologically separate exhibit, not a faithful continuation. Per
  the Anti-Degradation rule, we do not splice. *(The world/US OECD-ISDB continuation question belongs
  to the separate S703/S704 Christodoulopoulos exhibit, not to this Greek panel.)*

## 3. Method

No time-extension. The book-period recovery method (offline PDF vector digitization of the source
figure) is described in `S707_DPR.md` §0/§4 and the extraction report.

## 4. No-Proxy disclosure

**None used.** No proxy series stands in for the Greek panel.

## 5. No-Synthetic disclosure

The values are **digitized from the published chart** (`provenance: digitized`) — a documented
figure-digitization recovery of the authors' own plotted points, not fabricated, interpolated, or
frozen values. Precision is figure-digitization grade rather than table-exact; the aggregate
Figure-5 validation anchor (DPR §0) reproduces the paper's published moments to ±0.006, confirming
the vector pipeline recovers the authors' actual data points. No values were invented where the
chart was unreadable.

## 6. Failure-mode table

| Failure | Action |
|---|---|
| Loader (`L01_S707`) invoked | Reads the digitized panel workbook and emits long-form deviations (no longer SKIPPED) |
| Validator (`V03_S707`) invoked | Round-trips against the panel's deviation columns: `PASS`, n=600, MAE 0.0 |

## 7. CD2 divergence pre-disclosure

CD2 (the predecessor build) had no per-series CSV matching this exhibit's content. The CD2-vs-RSCD
comparison is not meaningful here.

## 8. Remaining recovery path (table-exact, out of scope for Phase 6)

The book-period figure has already been recovered by digitization. The only outstanding path to the
authors' **exact** tabulated panel is **author contact** (Tsoulfidis & Tsaliki are alive and
contactable). That would upgrade the provenance from `digitized` to a redistributed source table;
it is not required for the current book-period reproduction.

## Notation (plain-language key)

- **ROP / IROP** — (average) rate of profit / incremental rate of profit (the return on newly added capital).
- **Digitized (`provenance: digitized`)** — values recovered by reading coordinates off a published chart, faithful to the figure rather than to an exact underlying table.
- **ESYE / ELSTAT** — the Greek national statistical service and its post-2010 successor.
- **ISDB** — OECD International Sectoral Database (relevant to the separate S703/S704 exhibit, not this Greek panel).
- **MPRA** — the Munich Personal RePEc Archive (hosts the full-text source paper, working paper 51334).
- **L01 / V03** — the load and validate scripts that build and check the series.
- **CD2** — the predecessor build of this dataset.
- **Phase 5 / Phase 6** — Anu pipeline stages: ingestion / extension.

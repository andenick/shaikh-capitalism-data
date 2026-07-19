# RSCD v1.6.1 — Validation Hardening + Provenance Completion

**Release date**: 2026-07-17 · **Supersedes**: v1.6.0 (2026-07-11) · **Tag**: `v1.6.1`
**Campaign**: `RSCD_100_PERCENT_COMPLETION_PLAN.md` (evidence: `Technical/completion_100/`)

---

## NUMERIC_CHANGES

**None.** Zero data-value changes in this release. Every chopped CSV is value-identical to
v1.6.0 (the XS2301 loader was re-run after cache repopulation and reproduces the shipped values
with max |Δ| = 0.0005 bn — a float-representation artifact, not a data change; byte-level hashes
otherwise unchanged). All changes are validation-infrastructure, metadata, documentation, and
output-format. Certification counts are unchanged and class-partitioned as in v1.6:
**106 book-period/extension PASS · 8 theoretical · 2 cross-sectional-unavailable ·
2 extension-only · 2 data-unavailable (118 total, zero FAIL).**

## 1. Independent-anchor architecture completion (P40: 7 → 1)

218 new `validation.independent_anchors` registered, each sourced from a printed artifact
**independent of the file its loader reads** (the P40 circular-validation criterion):

| Series | Anchors | Source artifact |
|---|---|---|
| XS2001 | 108 | Shaikh (2020) *An Empirically Sufficient Form for Sraffa Prices*, Tables 1–2 p.10 (108/108 MATCH) |
| XS2201 | 75 | Shaikh & Jacobo (2020) Table 1, printed p.5 (75/75 MATCH) |
| XS2101 | 10 | Shaikh, Coronado & Nassif-Pires (2020) Section 5 / Fig 6, printed p.272 (10/10 MATCH) |
| S1702 | 9 | IRS SOI 2011 Pub 1304 Table 1.4 (7 exact + 2 bin-choice near, toleranced) |
| S1703 | 6 | IRS SOI 2011 Pub 1304 Table 1.4 (6/6 exact) |
| XS2301 | 6 | Weber & Shaikh Appendix Fig 1 printed p.453, 2005/2010/2015 densification (5% tolerance) |
| S201 | 4 | BEA *Long Term Economic Growth 1860–1965* (1966) Table A15, printed pp.168–169 (≤0.002% diff) |

- **XS2001 source paper located** in the project library (was a cataloging gap, not an acquisition gap).
- **S201 rescued from the deferral list**: the BEA LTEG 1966 source volume was on disk; its printed
  Table A15 (industrial production index, 1913=100) anchors the series independently of the loader's
  Appendix 2 workbook, using the printed table's own 1958 = 457.00 as the rebase denominator.
- **S202 is the sole remaining P40 WARN**: its printed source (BEA 1977 *Fixed Reproducible Tangible
  Wealth*) requires academic-library access; the deferral is documented in the registry
  (not a `no_printed_anchor_available` census case — printed anchors exist).
- anu-doctor (the framework self-audit tool) P40 now reads **1/113** (was 7/113).

## 2. XS2301 re-run risk retired

- **Cache repopulated**: Census FT900 c0004 + c5700 live-fetched into `api_cache/census_ft900/`
  (was empty; a re-run during a Census outage would have regressed 46 → 5 rows).
- **Parser fix**: `S00_apis.py` year extraction updated for the current Census HTML layout
  (year now read from the `TOTAL YYYY` row label). Fix ported to all four shipped copies
  (canonical, Technical replicator, bundle `code/`, bundle `replicator/lib/`).
- **Re-run proof**: value-identical (46 rows, 2002–2024, both subseries).
- **Mutation blind cell closed**: anchor set densified 4 → 10 figure-read points
  (2005/2010/2015 added at 5% tolerance); mutation suite PASS. The `scale_+1pct` cell is
  documented-exempt — sub-pixel-reading-error mutations are structurally undetectable from
  printed-figure anchors (`tools/mutation_exemptions.json`).

## 3. Extenbook Provenance sheets (format defect fixed)

All 118 workbooks regenerated: the Provenance sheet is now populated from the registry
(root cause: the writer read a nonexistent ledger key). Publish bundle carries the 112
distributable workbooks (5 publish:false series + S1006 excluded per the publish filter, as before).

## 4. Registry + documentation hygiene (2026-07-17 comprehensive review dispositions)

- **S801**: `content_type` corrected cross_sectional → time_series; `panel_dimension` added.
- **S803**: stale `cd2_source_file` (ch10 reference) nulled.
- **S306/S307**: `validation_class` corrected to `data_unavailable`; triage refreshed to the
  2026-07-10 A4 outcome; `data_unavailable_reason` now carries the documented unlock path
  (library scan of Board of Trade Cd.3864 (1908)).
- **Digitized-series honesty**: `construction: machine_digitized` on S404–S407, S703, S704,
  S707, S708, S801 (previously `direct`; provenance notes already documented digitization).
- **S1104**: triage now states all three subseries ship (C-line constructed 2026-07-02 via WDI;
  book-figure fidelity UNVERIFIED pending the human digitization-packet verdict).
- **S703/S704**: `display_name` scope-corrected (average panel only; incremental-rate panels
  of Figs 7.13/7.14 remain a future digitization candidate).
- **Upstream book-prose-vs-datafile discrepancies documented** (no data change; RSCD faithfully
  reproduces Shaikh's own data files): S709 (31 industries / 17 zero-crossers in the source
  workbook vs 30/18 in the book's prose, p.305 + Appendix B) and S710 (max-crossings assigned
  to Printing in the source workbook vs Broadcast in the book's prose, p.305, KB-verified).
- DPR/EPR repairs: S404–S407 recovery-banner contradictions, S207 VREF narrative, S210 title
  and code-vs-shipped reconciliation, S1403 VREF date, S1603 range consistency, S703/S704 scope
  notes, ch04 research-JSON premise correction (the ch04 KB IS extracted).

## 5. Public-text + surfaces

- Site explainer for S1104 now describes the shipped C-line (was: "left out"); ch04 explainers
  carry verified verbatim book quotes; S703/S704 explainers scope-corrected.
- Educational disclaimer added to the static-site footer (canonical text).
- `WEB_MANIFEST.json` gains a `repository` field (hub ↔ GitHub link).
- `CITATION.cff`: version 1.6.1, `repository-code` + `url` added (was 0.1.0-pre).
- RELEASE_NOTES_v1.5 erratum appended: the "118/118 PASS" headline is now class-partitioned.
- Drive README: workbook count corrected (112 + S1006 withheld explained); GitHub URL added.
- Bundle README: DPR/EPR defined at first use.

## 6. Gates (all green at release)

`run.py --gate` PASS (anu-doctor **0 FAIL / 1 WARN** [P40: S202 documented deferral] ·
anchor suite **0 RED** (53 series) · V03 batch **118/118 non-FAIL**) ·
mutation suite **PASS** (all cells caught or documented-exempt) ·
publish audit (pinned `transparency-bundle` profile) **exit 0** ·
publish filter verified: 0 SBBI data values, 0 publish:false artifacts, 0 workspace paths (FAIL-severity class).

## 7. Known residual items (honest backlog)

- **S202** P40 deferral (printed source requires library access).
- **SBBI in git history**: the v2.0.0-era commit `da978f1` (ancestor of `master`) contains the
  S1006 workbook with licensed Ibbotson SBBI values. The v1.6+ *tree* is clean (the file is
  excluded by the publish filter); the *history* purge (git filter-repo + force-push) is a
  user-level decision tracked in the completion plan (D11).
- **ch2 anchor coverage**: the KB printed-appendix pilot yielded 0/15 for ch2
  (the book's ch2 data appendix was published online-only); viable for chapters with printed
  appendix tables (fleet decision recorded).
- **Extenbook scrub check gap**: the publish audit did not scan workbook Data sheets for
  withheld-source values (caught by manual review this cycle); a scrub-harness improvement
  ticket is recorded.

*Release manager: completion_100 campaign. Evidence tree: `Technical/completion_100/`.*

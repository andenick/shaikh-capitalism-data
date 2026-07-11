# RSCD v1.5 — Release Notes

**Release date**: 2026-07-02
**Tag**: `v1.5`
**Framework**: Anu v12.2 · Schema v2.3.0
**Predecessor**: v1.4 (2026-06-11, AS/ES → XS migration + provenance reconciliation)
**Campaign**: RSCD v1.5 Skeptical Review & Remediation (`/megaexecute`)

---

## Summary

v1.5 is a **skeptical-review and remediation release**. It executed a 26-item
remediation backlog against the whole 118-series project, ran an independent
118/118 chapter skeptical sweep, and added a standing **validation-infrastructure
layer** (independent anchors, splice/plausibility guards, vintage pinning, a
classification-vintage guard, and a generalized NIPA line resolver). Eight
Gate-0 scope questions were ratified by the user before work began (rulings
**D-1 … D-9** plus the **Tier-5** digitization deferral), and eleven decision
documents (**0008–0018**) were authored.

Every close-out gate passed:

- **anu-doctor**: 38 PASS / 0 WARN / 0 FAIL (project) · 0/0 (framework)
- **V03 validator suite**: 118 / 118 PASS
- **Anchor suite**: 84 series — anchor / splice / plausibility all GREEN
- **D14 outward-facing intelligibility**: all 16 data chapters ≥ 90

No unexplained data changes. The only non-byte-reproducible series is **S207**
(live-FRED tail; see §Known-remaining).

This release also **closes the publish-leak vector** flagged during the campaign:
the public `Outputs/Publish/` mirror is now **publish-filtered** so that the
7 `publish:false` series and the licensed **Ibbotson SBBI** subseries inside
S1006 are excluded from all data artifacts (Decision 0010).

---

## What changed — data (NUMERIC_CHANGES)

All tables below were computed by diffing the pre-change backups
(`Technical/remediation_campaign/_backups/*.csv.pre_*`) against the current
`Technical/chopped/`. Book-period rows are byte-identical everywhere except where
noted; only the changes listed here occurred.

### C1 — S1401-A wage share, 2012–2025 (input series corrected)

The extension input was corrected from FRED **A576RC1** (wages & salaries only)
to **W209RC1 ÷ GDP** (compensation of employees, NIPA Table 1.10 line 2 — the
concept Shaikh's Appendix 14.3 wage share actually uses). This removed a ~22%
spurious splice break at the 2011→2012 boundary (now −3.8%, continuous).
14 values changed; no rows added/removed:

| year | old (A576RC1 wages&salaries) | new (W209RC1 compensation) |
|---|---|---|
| 2012 | 0.426240 | 0.527096 |
| 2013 | 0.421428 | 0.523379 |
| 2014 | 0.424593 | 0.525337 |
| 2015 | 0.429598 | 0.530166 |
| 2016 | 0.430276 | 0.529973 |
| 2017 | 0.432101 | 0.531529 |
| 2018 | 0.430847 | 0.530457 |
| 2019 | 0.432921 | 0.531412 |
| 2020 | 0.442820 | 0.542599 |
| 2021 | 0.434762 | 0.529318 |
| 2022 | 0.426903 | 0.515970 |
| 2023 | 0.421854 | 0.510846 |
| 2024 | 0.422824 | 0.512905 |
| 2025 | 0.421808 | 0.511243 |

### C4 — S203-A US real GDP/capita, 1930–1944 (MeasuringWorth re-pull, D-1)

The 1929–1934 source-workbook corruption (the old column *rose* through the
Depression trough) was fixed by re-pulling MeasuringWorth real GDP/capita
(2017$, re-pull 2026-07-01) and re-basing to the book series. The series now
falls strictly 1929→1933 (trough 1933, −28.57%). 15 values changed:

| year | old (corrupt) | new (MeasuringWorth re-pull, rebased) |
|---|---|---|
| 1930 | 8831.99 | 7411.56 |
| 1931 | 10240.48 | 6883.17 |
| 1932 | 11999.11 | 5956.72 |
| 1933 | 13771.49 | 5848.29 |
| 1934 | 14705.52 | 6440.10 |
| 1935 | 14381.68 | 6964.75 |
| 1936 | 12675.67 | 7812.40 |
| 1937 | 12323.25 | 8162.74 |
| 1938 | 12645.35 | 7831.27 |
| 1939 | 12364.94 | 8391.38 |
| 1940 | 13224.86 | 9055.55 |
| 1941 | 14007.01 | 10556.91 |
| 1942 | 14296.55 | 12415.16 |
| 1943 | 14709.99 | 14329.54 |
| 1944 | 14362.87 | 15283.82 |

### DF-1 — S1406-B Phillips inflation/productivity, 2012–2024 (denominator fixed)

The productivity-growth denominator was corrected from FRED
**B4701C0A222NBEA** (hours) to **A4301C0A173NBEA** (full-time-equivalent
employees — the correct per-worker basis), and the extension was carried to 2024.
11 values changed; 4 rows added (S1406-A/B for 2023 and 2024):

| year | S1406-B old (hours) | S1406-B new (FTE) |
|---|---|---|
| 2012 | 0.003705 | 0.003138 |
| 2013 | 0.005743 | 0.004786 |
| 2014 | 0.004881 | 0.004519 |
| 2015 | 0.010354 | 0.006815 |
| 2016 | 0.003929 | 0.002789 |
| 2017 | 0.010344 | 0.008832 |
| 2018 | 0.012972 | 0.011281 |
| 2019 | 0.013146 | 0.009636 |
| 2020 | 0.038783 | 0.033805 |
| 2021 | 0.025290 | 0.032165 |
| 2022 | −0.009293 | −0.013711 |

Rows added: `S1406-A 2023`, `S1406-A 2024`, `S1406-B 2023`, `S1406-B 2024`.

### C5 — S604 real-rate curves, +2 curves (Figure 6.7 completed)

Two of the four printed real-corporate-rate columns of Fig 6.7 were missing.
They were reconstructed from `SalvagedInputs/…/Appendix6_Table68II7.xlsx`
(columns `iroprcorp`, `iroprcorpnipa`):

| subseries | status | n | mean |
|---|---|---|---|
| S604-A | unchanged (byte-stable) | 64 | — |
| S604-B | unchanged (byte-stable) | 64 | — |
| **S604-C** (added) | new | 64 (1948–2011) | 0.095011 |
| **S604-D** (added) | new | 64 (1948–2011) | 0.084927 |

128 rows added; 0 existing values changed; 4/4 Table-6.24 anchors GREEN.

### C6 — S1104-C third GDP line (BLOCKED — external acquisition)

S1104's US/EU12 relative-GDP third line **cannot** be built from the salvage
(no US/EU12 GDP column exists; the CD2 "relative GDP" column was a mislabeled
copy of `realintratediff1`, exact match — a predecessor-data defect). Building it
requires a live 13-country OECD QNA / World Bank WDI fetch (a DPR Phase-9 item).
**No data changed** (S1104 100 rows unchanged); the line is documented as a
known-remaining acquisition item, never proxied.

> **↳ RESOLVED post-release — see "Post-release addendum (2026-07-02, FU-1)" below.**

### Row removals (partial-year / duplicate-splice hygiene)

| series | row removed | reason |
|---|---|---|
| **S207-D** | 2010 | duplicate splice-year: real-comp book column (S207-B) ends 2010 and the extension (S207-D) also started 2010; the A/C productivity pair's clean-handoff convention was applied (book Y → ext Y+1). |
| **S210-A** | 2026 | partial-year cap to the last complete year (2025); the 2026 reference-value anchor was moved to the 2025 realized value. |

S207-A/B/C carry sub-`1e-12` last-digit float jitter from reprocessing
(negligible; S207 is a live-FRED series — see §Known-remaining).

### Forecast flagging (D-2 — flag, don't truncate)

A trailing optional `is_forecast` column is now carried through the long-form
chopped writer. Realized rows are byte-identical; forecast rows are flagged, not
dropped.

| series | is_forecast=True | span | subseries |
|---|---|---|---|
| **S1701** | 14 rows | 2012–2025 | S1701-C |
| **XS2302** | 14 rows | 2025–2031 (IMF WEO) | XS2302-level, XS2302-pctgdp |

### Units-string corrections (values byte-identical in every case)

Banned / misleading `units` strings were replaced with established vocabulary;
no data values changed (verified by row-diff):

| series | old units | new units |
|---|---|---|
| S1502 | `rate_decimal_log_diff` | `decimal_annual_growth_rate` |
| S1503 | `rate_decimal_log_diff` | `decimal_annual_growth_rate` |
| XS002 | `billions_current_usd` (all) | `billions_current_usd` + `dimensionless_ratio` (per subseries) |
| XS003 | `mixed_billions_usd_and_decimal_rates` | `billions_current_usd` + `decimal_rate` (per subseries) |
| XS005 | `billions_current_usd` (all) | `billions_current_usd` + `dimensionless_ratio` (per subseries) |
| XS006 | `billions_current_usd` (all) | `billions_current_usd` + `decimal_rate` (per subseries) |
| S602 | `decimal_rate_and_share` | `decimal_rate` + `ratio` (per subseries) |
| S308 / S309 | `*_aggregate_demand_model_units` (aggregate) | per-agent (representative agent, y=200) |

---

## Judgment calls (documented deviations)

1. **S203 reindex anchor = 1929, not 2010.** Decision 0008/D-1 specified a 2010
   overlap reindex, but the book column ends in 2000, so no 2010 overlap exists.
   The re-pull was reindexed at **1929** instead. The transform preserves ratios
   exactly (1933/1929 = 0.71429 in both the re-pull and the rebased chopped), so
   the fix is faithful; the anchor-year deviation is recorded here and in the
   S203 provenance.
2. **XS2302 `year_range` = full span `[1997, 2031]`.** Per the D-2 convention the
   forecast tail is *flagged, not truncated*, so the registry `year_range`
   reconciles to the full span including the WEO forecast years, while
   `reference_values` use realized years only (the 2031 anchor was moved to 2024).
3. **S203 retained `publish: true`.** Decision 0008 blocked publish only *until*
   the fix landed; landing the MeasuringWorth re-pull satisfied the block
   condition, so S203 stays published.

---

## Validation infrastructure (new, standing)

| Component | What it does |
|---|---|
| **Independent anchors** (`code/V03_validators/_v03_anchor_lib.py`, `run_anchor_suite.py`) | 24 authoritative book-value anchors wired into 7 series (Tables 6.24, 9.18, 10.1/10.2, Harberger/Ramamurthy, Phillips a/c/R², T14.3-deferred). Registry tolerance reconciled to a 1% canonical band across 37 validators. |
| **Splice-continuity check** | Fails a splice when `|Δsplice| > max(3× trailing-5yr σ, 5%)` — this is what caught the S1401 −22% break. |
| **Level-plausibility check** | MHR-hooked sanity bounds — caught the S203 Depression-trough inversion. |
| **Vintage manifest + helper** (`config/VINTAGE_MANIFEST.json`, `code/utils/vintage_manifest.py`, `check_vintage_manifest.py`) | Pins the ALFRED realtime vintage for all 15 live-FRED loaders (26 series×fred_id pairs); coverage check PASSes. (Full ALFRED fetch migration is a documented follow-up.) |
| **Classification-vintage guard** (`O06_chopped_writer.py`) | Tags I-O subseries with `classification_vintage` (SIC71 / NAICS65 / NAICS_YYYY) and refuses to concat mixed classification eras (negative test fails-as-designed). |
| **Generalized NIPA line resolver** (`code/L01_loaders/_nipa_line_resolver.py`, `docs/methodology/concordances/line_label_index.csv`, `scheme_registry.csv`) | 40-row line index (T7.11 + T7.12 + T1.10 + Z1 + T2.1), by-caption + nearest-pinned-vintage fallback; resolver unit tests GREEN. |
| **run.py XS regex + ES/XS fallback** | Per-series `--series XS####` now matches only the XS validator (no S-series leakage), and the canonical V03/L01 loaders gained the XS→legacy-ES truth-CSV fallback (XS2201/XS2304/XS2305) so the full suite runs 118/118. |

---

## D14 outward-facing intelligibility re-score

All 16 data chapters clear the D14 ≥ 90 external-distribution gate after the
jargon scrub, the From-the-book restorations, and the C-wave content fixes.
(Formal re-score: `Technical/remediation_campaign/D14_RESCORE.md`.)

| Chapter | Prior | Re-score |
|---|---:|---:|
| ch3 | 82 | 95 |
| ch4 | 85 | 95 |
| ch6 | 88 | 93 |
| ch7 | 85 | 92 |
| ch8 | 85 | 92 |
| ch10 | 85 | 90 |
| ch14 | ~88 | 96 |
| ch15 | 84 | 95 |
| ch17 | 88 | 96 |
| XS / ch0 | 85 | 95 |

(ch10 raised to a clean 90 by the S1003–S1008 EPR inline-glossary micro-scrub
shipped in this release.)

---

## Known remaining items (not blocking)

1. **S703 / S704** — user-gated guided WebPlotDigitizer of the aggregate line in
   the 9-series Christodoulopoulos spaghetti (Tier-5; scheduled as a separate
   human-gated session, never proxied).
2. **S1104-C** — ✅ RESOLVED post-release (FU-1, 2026-07-02): built from WDI
   NY.GDP.MKTP.KD with the fixed EU12 basket. See the post-release addendum.
   (Book-figure numerical fidelity remains unverified pending figure digitization.)
3. **Full ALFRED migration** — rewrite the live-FRED loaders to fetch by pinned
   realtime vintage (the G1 manifest + helper + coverage check is the standing
   deliverable; the fetch migration is the Phase-N follow-up).
4. **SI-2 P2/P3/P4** — concordance build-spec follow-ups: `concordance_edges.csv`
   (Census SIC/NAICS chain, BEA I-O SCB), ISIC Rev3↔Rev4, the full
   `concordance_resolver.py`; plus T7.12 exact BEA captions + 2018 line-shift
   verification.
5. **S207 live-FRED repro caveat** — S207 has a live-FRED tail (OPHMFG, COMPRMS)
   and its loaders are not yet pinned to ALFRED vintages, so S207 is inherently
   non-byte-reproducible across pulls; its recorded repro hash is a stale
   intermediate (content validates; the double-2010 fix is present). Consider
   excluding live-FRED series from byte-exact repro hashing until vintage pinning
   lands.

---

## Distribution

- **`Outputs/Publish/`** — public replication bundle, **publish-filtered**
  (7 withheld series + S1006 SBBI subseries excluded from all data artifacts;
  registry copy publish-filtered). `Outputs/Publish/` is a mirror tree, not a
  git repo; `deploy/sites/rscd.yml` serves it wholesale, so the filter is what
  keeps the licensed data off the public surface.
- **`site/`** — regenerated static download site (registry-driven publish filter,
  XS scheme, no JSON links).
- **`Outputs/rscd-shaikh-2016-replication_Web_v1.1.0`** — web-profile export
  (anu-publish P01–P15 clean; SBBI subseries excluded).
- **`Technical/replicator/`** — self-contained clean-venv replicator.

## How to reproduce any value

1. `chopped/{SID}.csv` — the value
2. `research/{SID}_research.json` — Shaikh's verbatim quote
3. `docs/series/{SID}_DPR.md` — source provenance
4. `docs/series/{SID}_EPR.md` — extension method
5. `python replicator/scripts/replicate.py --series {SID}` — reproduce

Note: the S1006 Ibbotson SBBI subseries are `publish:false` (Morningstar-licensed)
and are not redistributed in the public bundle; the open Damodaran-NYU alternates
(`S1006-*-ext`) are the public surface (Decision 0010).

---

## Post-release addendum (2026-07-02, FU-1) — C6 / S1104-C resolved

This addendum records work done *after* the v1.5 release; it does not rewrite
the history above. The C6 item shipped as **BLOCKED**; a follow-up agent (FU-1)
subsequently built the line.

**What was done.** The third line of Figure 11.7, **S1104-C US/EU12 relative
real GDP (index 2002=100)**, was constructed from World Bank WDI
`NY.GDP.MKTP.KD` (real GDP, constant 2015 USD) for the United States and
Shaikh's **fixed pre-1995 EU12 basket** (BE, DK, FR, DE, GR, IE, IT, LU, NL,
PT, ES, GB): `US_realGDP / Σ EU12_realGDP`, rebased so 2002=100. WDI has
complete 1960-2009 coverage for all 13 countries (0 gaps, verified 2026-07-02).
Retrieved 2026-07-02; raw snapshot at
`Technical/data/raw/S1104C_WDI_NY_GDP_MKTP_KD_2026-07-02.csv`.

**NUMERIC ADDITIONS (nothing changed).** +50 rows added to `chopped/S1104.csv`
(S1104-C, 1960-2009). The existing **S1104-A and S1104-B rows are byte-identical**
(0 rows changed). New chopped sha256:
`c75987388b30ad3b9059289b7b4e49c7d345a7c88d6ec12bcf58941a62fa9592`
(recorded in `remediation_campaign/repro_hashes_C.txt`).

**Validation.** V03_S1104 PASS (n=150; S1104-C checked by an *independent* WDI
re-construction, MAE 0.0). Anchor suite ALL GREEN including the new
`S1104C_relgdp_band` plausibility rule (index ∈ [70,120]; 0 violations).
anu-doctor project mode 38/0/0. Direction corroborates Shaikh p.534 (relative
GDP rises as the REER falls — "opposite directions").

**Honest caveat (not overclaimed).** No digitized book-figure values exist for
Fig 11.7's third line (`FIGURE_MASTER_v4` carries only metadata), so **exact
numerical fidelity to Shaikh's printed curve is UNVERIFIED pending a
figure-digitization pass**. The line is a concept-faithful reconstruction, not a
byte-for-byte reproduction of Shaikh's undocumented `RelGDPR`. It is a live-API
series: WDI revisions may shift values across vintages. CD2's "S063 relative
GDP" was confirmed to be a mislabeled real-interest-rate differential and was
**not** ported.

**Docs touched:** `S1104_DPR.md` (§1,3,4,5,6,7,9 + deferral removed),
`S1104_EPR.md` (realized fetch provenance), `S1104_MHR.md` (§5 update note),
`series_registry.json` (S1104-C subseries + plausibility rule + realized
reference values), `SUBSOURCE_METADATA.json` (`WB_GDP_MKTP_KD_US_EU12`).

---

## Addendum — 2026-07-02 · Vintage Refresh (VREF): S201, S1403, S207

**Deliberate action (USER RULING 2026-07-02).** The v1.5 SI-1/FU-3 work pinned
every live-FRED loader to its *shipped* ALFRED vintage for byte-reproducibility,
and surfaced three series carrying newer BEA/FRED vintages than shipped
(`evidence_FU3.md` §9.1). Per user ruling, **S201 (INDPRO)**, **S1403 (W209RC1
quarterly + GDP/UNRATE/UEMPMEAN)**, and **S207 (OPHMFG/COMPRMS)** were
deliberately refreshed to the **LATEST FRED/ALFRED vintage** (realtime pins
advanced to **2026-07-02** in `Technical/config/VINTAGE_MANIFEST.json`). This
does *not* rewrite prior history: the shipped-vintage pins remain recorded in the
`series_registry.json.pre_VREF` backup and this file's earlier sections.

**NUMERIC CHANGES (extension-period only; book rows byte-identical).**

| Series | Subseries | Year(s) | Old → New | Δ |
|---|---|---|---|---|
| S201 | S201-C (INDPRO) | 2025 | 491.341892 → 491.331214 | −0.0107 (−0.0022%) |
| S207 | S207-C (OPHMFG) | 2025 | 2937.845631 → 2937.254182 | −0.591 (−0.020%) |
| S207 | S207-D (COMPRMS) | 2025 | 854.935152 → 854.272080 | −0.663 (−0.078%) |
| S1403 | S1403-WSH_ANNUALAVG_HP100 | 2025 | 0.511136 → 0.510557 | −5.79e-4 (−0.113%) |
| S1403 | S1403-WSH_ANNUALAVG_HP100 | 2024 | 0.511586 → 0.511488 | −9.7e-5 |

The S1403 W209RC1-q 2025Q4 revision (16022.5 → 15949.5) re-ran the HP(100)
filter over the whole quarterly wage-share series; only the 2024–2025 tail moved
materially (pre-2024 shifts are ~1e-15 float ULP). **S1403-ULINT is unchanged**
(UNRATE/UEMPMEAN are never-revised), so `validation.reference_values`
(ref-subseries S1403-ULINT, 2025 = 0.095978) still holds — no registry
reference-value edits were required. S201/S207 reference-values are all
book-period and unchanged.

**Gates (all green).** V03 all 3 **PASS** (book-period MAE 0.0). Anchor suite
**ALL GREEN** (84 series; S1403 book→extension splice re-fired GREEN — WSH jump
−0.26% vs 5% threshold, ULINT unchanged). anu-doctor project **38 PASS / 0 / 0**;
framework **0 / 0**. Byte-stable re-run verified (S201). New chopped sha256 in
`remediation_campaign/repro_hashes_C.txt` (VREF block).

**Artifacts refreshed.** `chopped/{S201,S1403,S207}.csv`,
`extenbooks/{...}_extenbook.xlsx`, `series_registry.json` (VREF provenance notes),
`config/VINTAGE_MANIFEST.json` (pins + `vintage_refresh_VREF` block),
`VALIDATION_REPORT.json`. Surgical Publish re-mirror (3 series' chopped +
extenbooks + registry notes + validation rows) and web-export patch
(`chopped` + `parquet`) applied; export copies verified byte-identical to
canonical. Evidence: `remediation_campaign/evidence_VREF.md`.

**Caveat.** These are live-FRED extension tails: values are vintage-dependent and
will shift again on future BEA/FRED revisions. The 2026-07-02 pin makes this
refresh itself reproducible.

---

## Addendum — M3/M4 machine digitization: S703 & S704 recovered (2026-07-02)

**S703 and S704 recovered by machine digitization** of the printed Christodoulopoulos
Fig 7.13 / 7.14 aggregate lines (Decision 0019, which amends 0018; user-authorized). Both flip
`data_unavailable → book_period_validated`, `publish: false → true`. The chapter-7 turbulent-
profit-rate exhibits are now numerically complete.

**Method.** Dual independent extraction (geometry-first + sampling-first, blind to each other) →
mechanical agreement test → crop-level adjudication (viewed at high zoom) → adversarial verification
(a fresh agent that tried and failed to refute each curve; both CONFIRMED, no point refuted). Values
carry honest per-point transcription confidence; gaps stay gaps. Human `returns/` digitization
remains a permanent **superseding** path (provenance rank human_guided > machine_digitized).

- **S703** — World manufacturing average rate of profit (WORLDAVG open-circle line), 1970–1990,
  **20 points** (1974 omitted — no defensible open-circle marker on the 1973→1975 descent).
  `rate_decimal`, 0–0.45. Confidence MEDIUM-HIGH (~±0.005, mean 0.666). Passed the agreement gate
  raw (95%).
- **S704** — US manufacturing average rate of profit (USMANAVG boldest markerless line), 1960–1989,
  **30 points** (1990 column omitted — marker-occluded; ruling in
  `machine/S704_1990_omission_ruling.md`). `rate_decimal` (figure percent ÷ 100). Confidence HIGH
  (~±0.5pp, mean 0.757). The raw agreement gate failed (53%) purely on extractor-B's diagnosed
  +1-year x-offset; every point resolved to extractor-A and independently re-confirmed by the
  adversarial verifier's from-scratch data-anchored rebuild — three agreeing measurements per point.

**S1104-C (M4).** The built US/EU12 relative-real-GDP line's fidelity to printed Fig 11.7 was
**machine-assessed: MINOR DIVERGENCE — shape and level faithful** (1974 trough and 2005/2009 endpoints
near-exact after rebasing to the printed 2002 base; the 1960s plateau prints slightly higher/flatter).
Marked machine-assessed; human confirmation optional and superseding.

**`data_unavailable` count: 4 → 2.** RSCD is **118/118** with data present for every chapter-7
profit-rate exhibit. Two series remain `data_unavailable` — **S306 / S307** (1904 UK working-class-
budget Engel series), a separate, unrelated open item, not part of this recovery.

### NUMERIC ADDITIONS (all rows are additions — nothing changed or removed)

| Series | New chopped rows | Period | Units | sha256 (chopped) |
|---|---|---|---|---|
| S703 | 20 (added; was empty/absent) | 1970–1990 | rate_decimal | `b8c04e6983fffec4b527c2cd2c0f38c3429cdafff320e1e048cf394c591c6812` |
| S704 | 30 (added; was empty/absent) | 1960–1989 | rate_decimal | `22821375f39a938e4631f1b4abc543c8860db976fbc809f1eb69257e6731521f` |

No existing series' values were modified. Full method + evidence:
`Technical/remediation_campaign/digitization_packet/machine/` (consensus CSVs, overlays,
M2_adjudication_log.md, M3_verify_report.md, S704_1990_omission_ruling.md) and Decision 0019.

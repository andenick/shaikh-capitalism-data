# S502 — US and UK Wholesale Price Indexes, 1790–2010 — Methodological History Report (MHR)

**Group:** ch5 (Exchange, Money, and Price) · **Construction:** composite · **Status:** book_period_validated
**Figure:** 5.4 · **Predecessor:** CD/CD2 S023 · **Publish:** true · **Book period:** 1790–2010 · **Extension:** US 2011–2026 (FRED PPIACO); UK deferred
**Reasoning stance:** from Shaikh's own perspective — why *he* built the series this way.

> Grounding note: every author-intent claim below is anchored to a citable path — the research JSON
> (`Technical/research/S502_research.json`), the DPR/EPR (`Technical/docs/series/S502_{DPR,EPR}.md`),
> the chapter summary (`Technical/docs/chapters/CH5_RESEARCH_SUMMARY.md`), the book KB (Body_Text
> `ch05_exchange_money_price.md`, Figure `ch05/ch05_fig_5.4.md`, Equations `ch05_equations.md`), the
> Ch5 review (`Technical/methodology_review/CH05_review.json`), and the Phase-0 timelines
> (`Technical/docs/methodology/_timelines/{NIPA,IO}_CHANGE_TIMELINE.md`). Where a rationale is not present
> in the corpus it is marked **"author rationale not located in corpus."**

---

## 1. What the series is

S502 is the annual **US and UK wholesale price indexes over the full long run 1790–2010**, both rebased to
**1930 = 100** and plotted on a **log scale** (10–10,000) as **Figure 5.4** (KB `Figures/ch05/ch05_fig_5.4.md`).
It is the **empirical centerpiece** of Ch5's argument: where S501/Fig 5.3 shows the trendless pre-fiat epoch,
S502/Fig 5.4 extends the span to 2010 and shows (book p. 188, `S502_research.json` book_quotes[0],
role=definition, verbatim_check=true) that "these patterns change dramatically after **1939/40**. Prices rise
more or less continuously in this new epoch, and the previous stationary fluctuations … are swamped by the
cumulative effects of persistent inflation. By 2010 the price level in the United Kingdom had risen
**fifty-eight-fold** relative to its prewar base in 1939, and that in the United States **fourteen-fold** from
its prewar base in 1940." These two multiples are direct V03 regression targets.

S502 is the **parent series** of the chapter: S501 (1790–1940 slice), S503 (UK WPI-in-gold), and S504 (US
WPI-in-gold) all draw their WPI legs from S502's two country columns (`S502_DPR.md` §1, `CH5_RESEARCH_SUMMARY.md`
cross-refs: `S502 → {S501, S503, S504}`). It is also the *same underlying data* as Ch2 Fig 2.8 (RSCD S210) — the
CH2 dossier explicitly names Ch5 as the canonical deep home of the WPI/gold family. ~458 chopped rows
(221 US + 221 UK book + 16 US extension). Final units: **Index, 1930 = 100**, annual (`S502_DPR.md` §6).

## 2. Source lineage

Per Appendix 5.2 (book pp. 788–789, transcribed in `S502_research.json` book_quotes[2–3], role=source,
verbatim_check=true) and `S502_research.json` components[], the composite splices, per country:

**US line (S502-A):**
| Segment | Coverage | Source / id | Native units | Operation |
|---|---|---|---|---|
| US WPI backfill | 1790–1799 | **US CPI** (Fig 2.5 sources) rescaled by the **1800 WPI/CPI ratio** | Index 1930=100 | interpolated |
| US WPI historical | 1800–1976 | **Jastram (1977) Table 7** (pp. 145–146) | Index 1930=100 | native basis |
| US PPI extension | 1977–2010 | **BLS `WPS00000000`** (PPI All Commodities) | growth rate | extended via implicit growth rates of WPS |

**UK line (S502-B):**
| Segment | Coverage | Source / id | Native units | Operation |
|---|---|---|---|---|
| UK WPI historical | 1790–1938 | **Jastram (1977) Table 2** | Index 1930=100 | native basis |
| UK WPI gap-fill | 1939–1945 | **NBER macrohistory `m04053.dat`** (UK PPI all commodities, monthly) | growth rate | missing Jastram years filled via implicit annual growth rates |
| UK WPI historical | 1946–1976 | Jastram (1977) Table 2 | Index 1930=100 | native basis |
| UK PPI extension | 1977–2010 | **ONS `PLLU`** ("Price Index of UK Output of Mfg Goods", statbase) | growth rate | extended via implicit growth rates of PLLU |

**RSCD modern extension (post-book):**
| Subseries | Coverage | Source / id | Native units | Operation |
|---|---|---|---|---|
| S502-C (US) | 2011–2026 | **FRED `PPIACO`** = BLS `WPU00000000` (successor to frozen WPS) | Index 1982=100 | monthly→annual avg, level-anchored at **2010** to the book USWPI |
| S502-D (UK) | 2011–2025 | ONS `PLLU` | Index 2015=100 | **not fetched** — ONS PLLU CDN returns 502 from our IP; UK 2011+ left NaN |

Retrieval: book columns `USWPI`/`UKWPI` from `Appendix5_DATALRprices.xlsx`; US extension from FRED
`PPIACO` (no key required). anwarshaikhecon.org is DNS-dead; local XLSX canonical (`S502_DPR.md` §3;
`CH5_RESEARCH_SUMMARY.md` §Phase 5–8).

## 3. Why these sources — author's perspective

Shaikh's concept is **long-run price-level behavior across two monetary regimes** (metallic → fiat), and the
demonstration hangs on the *longest possible internally-consistent price record spliced to its live successor*:

- **Why Jastram (1977).** As with S501, Jastram's Tables 2/7 give a multi-century WPI on a common 1930 = 100
  basis with a matching gold series — the exact ingredients the chapter later needs to form p' = WPI/gold
  (S503/S504). Explicit rejection of alternatives (HSUS, JST, Officer/Williamson's own WPI) is **author
  rationale not located in corpus**.
- **Why the specific national extensions (BLS WPS, ONS PLLU).** These are the **direct national successors** to
  the historical wholesale-price concept, and Shaikh splices them **by implicit growth rate** so Jastram's level
  basis is preserved — a fidelity choice (continue the same concept forward on the same base), not a proxy
  (`S502_research.json` book_quotes[2–3]). The growth-rate discipline is what lets a 1982=100 BLS feed extend a
  1930=100 historical index without a level break.
- **Why 1930 = 100 as the common base.** It is Jastram's own base, and it sits comfortably inside the metallic
  regime, so both the pre-1940 stationary epoch and the post-1940 inflationary epoch are read against the same
  reference — making the 58× / 14× multiples legible on one log axis. This choice is inherited from Jastram, not
  imposed by Shaikh.
- **The deeper "why" of the whole figure.** Fig 5.4 is Shaikh's empirical case *against the Quantity Theory of
  Money* (eq. 5.7, `ch05_equations.md`) and *for* the classical/Marxian view (eq. 5.9, developed fully in
  S503/S504): the regime break at 1939/40 — not any change in M/XR·v — is what turns a trendless price level
  into an exponential one, because that is when the money-price-of-gold anchor is cut.

## 4. Methodological-change exposure

- **NIPA / IO timelines DO NOT apply.** S502 is built from **BLS/ONS price indexes and Jastram's historical
  tables — none of it is NIPA or benchmark I-O data.** The BEA comprehensive-revision events in
  `NIPA_CHANGE_TIMELINE.md` (1999–2023) and the SIC→NAICS wall in `IO_CHANGE_TIMELINE.md` **do not touch this
  series.** The relevant vintage event is the BLS WPI→PPI rename, not any NIPA revision. Stated explicitly per
  the task contract.
- **BLS WPI → PPI rename/renumber (the WPS→WPU issue) — this is the live concordance risk, and it is real
  here.** Shaikh's cited US extender **`WPS00000000` is a legacy code BLS froze** (≈1974 in the modern feed);
  its live successor under the same PPI All-Commodities program is **`WPU00000000`** (FRED `PPIACO`). RSCD
  extends S502-C with `PPIACO`/`WPU00000000` as a **direct within-agency successor, `proxy: false`**, verified
  live through 2026-04 with the 2026-04 value (283.764) matching the Phase 4 reachability check
  (`S502_EPR.md` §5, `S502_DPR.md` §7.1, `CH5_RESEARCH_SUMMARY.md` §Phase 5–8). PPI re-basing (1982=100) is
  absorbed by the growth-rate/level-anchor splice at 2010, so the 1930=100 basis is untouched.
- **ONS UK price-index revisions.** `PLLU` survives ONS's re-basings (2010=100 → 2015=100) but the CDN threw a
  **502** from our IP at Phase 4/5; the UK extension is honestly left NaN rather than proxied
  (`S502_DPR.md` §7.3, `S502_EPR.md` §4).
- **Registry-convention note (L4, non-substantive).** The US extension ships as subseries **`S502-C`** rather
  than a formal `-EXT` block, which sidesteps the Decision 0003 `-EXT` binary invariant and the D10 `-EXT/-F`
  naming convention; it remains internally consistent under the long-form canonical (Decision 0005) and is
  documented via `construction_steps` + EPR (`CH05_review.json` finding L4).

## 5. Replication fidelity note

- **Truth basis:** RSCD reads truth columns `USWPI`/`UKWPI` directly; V03 MAE 0.0% at ±1.0%
  (`S502_DPR.md` §9; `CH05_review.json` D13 = 100, 754 book-period cells at MAE 0.0). Book-claim diagnostics
  reproduce: **US 2010/1940 = 13.656×** (book "fourteen-fold") and **UK 2010/1939 = 57.992×** (book
  "fifty-eight-fold"), within rounding of Shaikh's text (`CH5_RESEARCH_SUMMARY.md` §Phase 5–8).
- **WPU-substitutes-frozen-WPS:** US 2011–2026 extension uses FRED `PPIACO`/`WPU00000000` anchored at 2010,
  `proxy: false`, on the 1930=100 base (`S502_EPR.md` §3, §5).
- **UK extension deferred, not fabricated:** ONS PLLU 502 → UK 2011+ NaN, `extension_status:
  api_unavailable_ons_pllu_cdn_502`; no different-concept UK PPI substituted, no 2010 value carried forward
  (`S502_EPR.md` §4, §6).
- **CD2 continuity + caution:** S502 reproduces CD2 S023's book-period values exactly; but CD2's legacy table
  carried post-book anomalies (1996 = 857.3, 2020 = 1305.3) that look like a USWPI-only column and must not
  contaminate the dual-line book dossier (`S502_research.json` methodology_notes[3], open_questions[1]).

## 6. Forward risk

- **ONS PLLU discontinuation is the top live-source risk** — already threw a 502; confirm the unchanged
  successor before lifting the UK extension from `not_attempted` to `feasible` (via an ONS bulk MM22 fetch or a
  different-IP re-probe) (`S502_research.json` open_questions, `CH5_RESEARCH_SUMMARY.md` open-question 1).
- **BLS PPI re-basing / renumber** affects only the growth-rate/anchor input, not the 1930=100 basis — low
  risk, but re-verify `WPU00000000`/`PPIACO` identity each refresh.
- **Jastram base is frozen** — the pre-1977 historical segment is fixed forever; no forward risk there.
- **Companion-site fragility:** the salvaged `Appendix5_DATALRprices.xlsx` is the sole canonical copy of the
  book values (anwarshaikhecon.org DNS-dead) and is the blocking dependency for every Ch5 series' re-derivation.

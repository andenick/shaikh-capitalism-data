# Chapter 11 — International Competition and the Theory of Exchange Rates — Methodology History Dossier

**Group:** ch11 · **Series:** S1101–S1104 (4) · **Book pages:** 523–534 (figures); 875–880 (Appendix 11.1)
**Reasoning stance:** from Anwar Shaikh's own perspective — why *he* constructed each series as he did.
**Companion per-series MHRs:** `Technical/docs/methodology/series/S110{1..4}_MHR.md`
**Machine-readable twin:** `Technical/methodology_review/CH11_methodology.json`

> Grounding: every claim is anchored to a citable path — the research JSONs (`Technical/research/S110N_research.json`),
> `Technical/docs/chapters/CH11_RESEARCH_SUMMARY.md`, the adequacy report
> (`Technical/docs/chapters/CH11_ADEQUACY_REPORT.json`), the Phase-1 review
> (`Technical/methodology_review/CH11_review.json`), the DPRs/EPRs, the registry slice
> (`Technical/series_registry.json`), and the method source Shaikh & Antonopoulos 2012
> (`Technical/MethodologyLibrary/SHAIKH_2016_BIBLIOGRAPHY.csv` BIB-0491). No claim is invented.

---

## 1. What the chapter builds

Chapter 11 develops Shaikh's **classical theory of real exchange rates**: real effective exchange rates
(REERs) are *not* stationary — strong-form purchasing-power parity (PPP) is false — yet they **gravitate
around relative real unit labour costs**, adjusted for tradable/non-tradable composition. The four series
map one-to-one to the chapter's four empirical figures and form a single argument:

| SID | Fig | What it is | Construction | Role in the argument |
|-----|-----|------------|--------------|----------------------|
| S1101 | 11.2 | Trade balances (X/M ratio), 15 countries | composite | the *phenomenon*: persistent, non-mean-reverting imbalances |
| S1102 | 11.3 | REER (PPI-basis), US & Japan | formula (eq. 11.16) | *rejects PPP*: REERs non-stationary in short and long run |
| S1103 | 11.6 | Law of One Price at the aggregate level, US & Japan | formula (REER ÷ adjusted RULC) | the *fundamental*: REER/RULC ratio is long-run stable |
| S1104 | 11.7 | US trade balance + REER + relative GDP | composite (3-line overlay) | the *synthesis*: competitiveness vs income pull opposite ways |

## 2. The one source family — Appendix 11.1

**Every series in the chapter chains back to Shaikh's Appendix 11.1 raw inputs** (`CH11_RESEARCH_SUMMARY`
"Chapter focus"; `CH11_ADEQUACY_REPORT.scope_note`). There is **no BEA NIPA and no input-output touch
anywhere in the chapter** — the spine is international-statistics providers:

- **IMF International Financial Statistics (IFS)** — goods exports X and imports M in USD (S1101; S1104-A;
  and the trade *weights* `w_j = (X_j+M_j)/Σ` for the REER basket). Belgium 1960–1992 backfilled from AMECO.
- **BLS International Labor Comparisons (ILC)** — Table 11 exchange rates `e` and Table 9 manufacturing unit
  labour costs (feeds S1102 REER and the S1103 RULC denominator). **Discontinued 2013.**
- **World Bank WDI** — producer price indices PPI (deflation and partner basket) and, for the deferred
  S1104-C, real GDP `NY.GDP.MKTP.KD`.
- **BLS/FRED CPI** — enters the `RULC = ULC/CPI` and `τ = CPI/PPI` adjustments of S1103 (remains active).

The published method for the REER/LOP machinery is **Shaikh & Antonopoulos (2012)**, *"Explaining
Long-Term Exchange Rate Behavior in the United States and Japan"* (BIB-0491), realised as **equation
(11.16)** of the book, quoted verbatim in Appendix 11.1.III (p. 876).

## 3. Why these sources — the two concepts that define the chapter

**(A) The real-exchange-rate concept — PPI-deflated, multilateral, trade-weighted (S1102, and S1104-B).**
Shaikh's competitive mechanism runs through **tradable** goods, so the REER is deflated by **producer
prices**, not consumer prices — a CPI-deflated REER is the very PPP object he is disproving (cf.
Froot & Rogoff 1995 in the chapter bibliography). It is **multilateral** (trade-weighted geometric mean of
partner PPIs), not bilateral, because *"in international competition countries compete against others in the
same league."* The specific sources — BLS ILC Table 11 for `e`, WDI for PPI, IMF IFS for weights — are
chosen because BLS ILC uniquely delivered internationally-harmonised *manufacturing* (tradables) data
across the 19-country sample, and IFS supplies the same X+M flows that already anchor S1101. Rejected
alternatives: CPI-deflated REER (wrong concept), bilateral USD/JPY (wrong scope). See `S1102_MHR.md` §3.

**(B) The vertically-integrated real-unit-labour-cost concept — the LOP fundamental (S1103).** Shaikh's
classical "law of one price at the aggregate level" says the REER is anchored not by PPP but by **relative
real unit labour costs**. The *proper* measure is the **vertically integrated** RULC (direct + indirect
labour cost per unit of tradable output). Shaikh states verbatim (p. 876) that, *"due to lack of data on
vertically integrated costs,"* he substitutes **direct RULC = ULC/CPI as an explicit, author-declared
proxy** — a book-period data-limitation proxy over an absent source, entirely distinct from the post-2009
extension proxy in §4. The `τ = CPI/PPI` factor then re-weights for tradable/non-tradable composition so
the RULC denominator aligns with the PPI-deflated numerator. Manufacturing ULC from BLS ILC Table 9 is
chosen for the same tradables-comparability reason as `e`. See `S1103_MHR.md` §3.

**Two presentation choices worth recording.** (i) S1101 uses the X/M ratio (a break-even at 1.0 across 15
economies); S1104-A switches to the **net-trade ratio `(X−M)/(X+M)`** (centred on zero, ideal for the
single-country overlay) — a deliberate within-chapter unit contrast, empirically confirmed by CD2's
negative sample values. (ii) S1104-C measures relative income against Shaikh's **pre-1995 EU12** bloc
(BE, DK, FR, DE, GR, IE, IT, LU, NL, PT, ES, GB), his "competitive league," not the modern Euro Area.

## 4. Methodological-change exposure — the BLS ILC → BIS proxy, and its exact temporal scope (KEY SECTION)

The chapter's single defining methodological event is the **discontinuation of the BLS International Labor
Comparisons program in 2013**, which killed three of the four REER inputs and both of the RULC inputs on
Shaikh's original sources. This forces a **proxy for the deferred post-2009 extension — and for the
post-2009 extension ONLY. Every 1960–2009 book-period value in the chapter is Shaikh's own Appendix 11.1
and is verified bit-exact (§5). No substitute touches any book-period chart.** This scope point is the
chapter's chief documentation hazard (`review.proxy_audit`; `review.F3`).

| Series | Book period (1960–2009) | Post-2009 proxy | Concept-match verdict |
|--------|-------------------------|-----------------|------------------------|
| **S1101** | IMF IFS X/M (Appendix 11.1) | **NONE** — IMF IFS/DOTS continuation (same agency/concept) | proxy:false (code_remap only) |
| **S1102** | Appendix 11.1 `rxr1` | **BIS PPI-based EER broad index** | ACCEPTABLE (trade-weighted multilateral PPI-deflated REER; basket/weighting differ, concept identical) |
| **S1103** | Appendix 11.1 `rxrrulcratio1` | **dual:** BIS (numerator) + OECD `ULC_QUA` (open) / Conference Board ILC (hi-fi) (denominator) | numerator ACCEPTABLE; OECD denominator PARTIAL (whole-economy vs Shaikh's manufacturing — sectoral-narrowing note); Conference Board DIRECT (licensed) |
| **S1104** | A: IFS `(X−M)/(X+M)`; B: `rxr1`; C: deferred | **S1104-B only** inherits S1102's BIS proxy; S1104-A none; S1104-C concept-exact backfill (no proxy) | S1104-B ACCEPTABLE; A/C proxy:false |

**The concept-match, precisely.** BIS PPI EER and Shaikh's REER are both *"trade-weighted multilateral real
exchange rates deflated by producer prices"* answering the identical economic question; the differences are
**basket and weighting** (BIS ~60 partners, rolling 3-yr weights, base 2010=100 vs Shaikh's static
19-country IFS-weighted basket, base 2002=100 — reindexed over the 1994–2009 overlap), **not concept**, and
**producer-price deflation is preserved** (`review.proxy_audit.concept_match_verdict`;
`CH11_ADEQUACY_REPORT.data_substitutions_recorded[0]`). Because S1102/S1103 are `formula` series, the No-
Lazy-Splices rule forbids growth-splicing the published columns — the extension substitutes a *published
REER* (BIS) and re-computes the LOP ratio from re-extended parts (`CH11_ADEQUACY_REPORT` Q6). The rejected
alternative — a bespoke Shaikh-method reconstruction from current WDI PPI + IMF e + IMF weights — was set
aside as effort-heavy for marginal gain over the canonical BIS series, optionally publishable later as a
methodology *variant* (`CH11_ADEQUACY_REPORT.bls_ilc_substitution_summary.alternative_considered`).

**Temporal-scope wording action (F3, MEDIUM).** S1102 and S1104 justifications carry the explicit
"Post-2009 extension…" clause; **S1103's leading clause omits it** and must be aligned so no external reader
can infer a book-period substitution (`review.proxy_audit.scope_issue`; `review.F3`). These MHRs supply the
gloss; the registry wording is the outstanding one-line fix.

## 5. Replication fidelity — bit-exact book period, honestly-scoped proxies, one coverage gap

- **All four series reproduce Shaikh's Appendix 11.1 bit-exact.** Independent hand-check: 8/8 tested
  subseries `max_abs_diff = 0.0, n = 50` each; non-circular in-text anchors all match — Australia in deficit
  43/50 years (EXACT), S1102 2002 base = 100 (EXACT), S1103 rescale (EXACT Japan / 0.07% US) and the S1103
  internal formula `rxr1/rulcadjratio1rescaled → rxrrulcratio1` (EXACT) (`review.hand_check`). D13 data
  authenticity **PASS**; no `np.random`, no synthetic/frozen values; loaders read the `Appendix11_*.xlsx`
  workbooks (`review.gate_detail.D13_data_authenticity`).
- **Proxies are pre-registered, flagged, and post-2009 only.** No-proxy compliance `COMPLIANT`; all
  extensions are `not_attempted_v1`/`partial` — the `proxy:true` flags describe the *future* Phase-9 splice,
  not shipped data (`review.proxy_audit`; per-series EPRs).
- **Two distinct proxies in S1103 — kept straight.** (a) Shaikh's *own* book-period proxy (direct RULC for
  vertically-integrated RULC, an author-declared data-limitation substitution present in the 1960–2009
  chart); (b) the *extension* proxy (BIS + OECD/Conference Board, post-2009 only). Neither overwrites a
  published value.
- **The one coverage gap: S1104-C (F1, HIGH).** Published Fig 11.7 is a 3-line overlay; RSCD ships **2 of 3
  lines** (S1104-A + S1104-B). S1104-C (US/EU12 relative GDP) is not emitted — no salvaged file; the 12
  pre-1995 EU-member real-GDP backfill is deferred to Phase 9. Registry `S1104.formula` names 3 lines while
  `subseries` holds 2, a known internal inconsistency (`review.F1`). Honestly disclosed, not silently
  dropped.
- **S1103 figure-label reconciliation (F2, MEDIUM).** Book plots dashed-US/solid-Japan appear swapped vs
  A=Japan/B=US, but hand-check confirms RSCD is faithful to the authoritative appendix (both bit-exact).
  Add a reconciliation note; **do NOT swap data** (`review.F2`).
- **Integration score 90.0, certification COMPLETE**; D14 intelligibility 90 *conditional* — blocked from
  external distribution only until the proxy temporal-scope note (F3) and a jargon glossary are added
  (`review.integration_score`; `review.gate_detail.D14_intelligibility`).

## 6. Forward risk (chapter-level)

- **Coordinate the shared BIS numerator.** S1102, S1103-numerator and S1104-B all use the same BIS PPI EER
  substitution — the splice years (2010+), the 1994–2009 reindex window and the rebase to 2002=100 must be
  **identical** across all three, or the LOP ratio double-counts the splice error (`S1103_EPR.md` §2;
  `CH11_ADEQUACY_REPORT` recommendation coordination note).
- **S1103 is a single coordinated dual-reconstruction.** Re-extend numerator (BIS) and denominator (OECD or
  Conference Board ULC) together, recompute the ratio, rescale the denominator to the REER period average as
  Shaikh did; ship `S1103_open` (OECD, CC-BY) as distributable and `S1103_hifi` (Conference Board, licensed)
  only where access exists (`S1103_EPR.md` §2–3).
- **Close the S1104-C coverage gap** (concept-exact EU12 backfill) to make Fig 11.7 fully reproducible and
  reconcile the registry formula/subseries count (`review.F1`).
- **Preserve honest scoping everywhere.** Keep `proxy:true` strictly post-2009 with the temporal-scope note
  (align S1103 wording, F3); keep the intentional S1101 X/M vs S1104-A net-trade unit contrast (do not
  harmonise); keep Shaikh's disclosed vertically-integrated-RULC proxy note in S1103; never fold China
  (S1101-E) into Shaikh's 15-country statistics.
- **Provider-code migration for S1101.** The clean IFS→DOTS/SDMX continuation is a *code_remap* annotation,
  not a proxy — mind the 1991 Germany reunification splice and the updated AMECO URL
  (`Technical/docs/methodology/IFS_line_to_SDMX_remap.md`; `CH11_ADEQUACY_REPORT` URL substitutions).

# XS2303 — Methodological History Report (MHR)

**Series**: XS2303 — China Official Foreign Exchange Reserves Excluding Gold, 1990–2024 (World Bank WDI)
**Chapter**: 0 · **xs_class**: external_study · **Group**: 23 (Weber–Shaikh 2020 family)
**Perspective**: authored *from Shaikh's perspective* (co-author of Weber & Shaikh 2020).
**Authored**: 2026-06-30 · **Read-only provenance**; every claim traces to a cited path.

Grounding: `Technical/research/XS2303_research.json`; `Technical/docs/series/XS2303_DPR.md` + `XS2303_EPR.md`;
`Technical/docs/external_studies/XS2301_paper_summary.md` + `ES_PHASE_5_8_CLOSURE.md`. Paper: Weber & Shaikh (2020),
IRAE 35(3–4):432–455, DOI 10.1080/02692171.2020.1814221.

---

## 1. What it is

XS2303 is the paper's **Appendix Figure 3 (p. 454)**: China's **official foreign exchange reserves, excluding gold**,
in current USD, plotted 1990–2016 as a single dotted line (y-axis Billion USD, 0–4,500). The figure caption fixes the
measure verbatim (`XS2303_research.json` book_quotes, role=source, p. 454; note the paper's own typo):

> "China Foreign Reserves (without Gold) in current USD, 1990-2016. Data sourcre: World Bank, 2018."

"without Gold" maps unambiguously to WDI indicator **`FI.RES.XGLD.CD`** (Total reserves *minus* gold, current US$) —
**not** the companion `FI.RES.TOTL.CD` (total reserves *including* gold), which is a different series and must not be
substituted (`XS2303_research.json` methodology_notes; `XS2303_DPR.md` §7 caveat 1). The series is a single AnuData row;
the loader divides the raw WDI current-USD value by 1e9 for the paper's Billion-USD display (`XS2303_DPR.md` §4).

Trajectory (`XS2303_research.json` formula): ~$30 bn (1990) → ~$168 bn (2000) → ~$2,914 bn (2010) → **~$3,840 bn peak
(2014)** → ~$3,030 bn (2016). Paper Section 1 (p. 433) supplies three text anchors used as loader QA (`XS2303_DPR.md`
§7 caveat 3): the reserves "increased almost 17-fold from 2000 to 2010" (WDI 2914/168 = 17.3×); "By 2013 … reached a
level of USD 3.6 trillion"; and Section 3 (p. 438) "China's foreign exchange reserves had stabilised at around USD 3
trillion, almost 30% lower than its 2014 peak of nearly USD 4 trillion."

Fig 3 is the *manipulation-proponents'* own headline evidence turned against them: reserve accumulation is what
Bergsten/Gagnon/Krugman cite as proof of undervaluation (p. 433), so Weber & Shaikh plot it explicitly to then argue
(Sections 3–5) that reserve build-up reflects endogenous capital flows under real-cost imbalance, not a manipulated peg.

## 2. Source lineage

Single indicator, single country (`XS2303_DPR.md` §3; `XS2303_research.json` primary_source):

| Subseries | Coverage | Source | Native units | Retrieval |
|---|---|---|---|---|
| XS2303-A | 1990–2024 | World Bank WDI indicator **`FI.RES.XGLD.CD`** (Total reserves minus gold, current US$) for `CHN` | current USD | World Bank Data API (`api.worldbank.org/v2/country/CHN/indicator/FI.RES.XGLD.CD?format=json`); no auth; **CC-BY-4.0** |

- **Agency / product**: World Bank *World Development Indicators (WDI)*, "Total reserves minus gold (current US$)"
  (`XS2303_research.json` primary_source). **License CC-BY-4.0** — the strongest open-redistribution posture of the five
  XS2301–XS2305 series.
- **RSCD access path**: a **LIVE WDI API pull** via `S00_apis.worldbank_indicator(country='CHN',
  indicator='FI.RES.XGLD.CD', start=1990, end=2024)` (`XS2303_EPR.md` §2; `ES_PHASE_5_8_CLOSURE.md` API-clients).
- **Upstream / cross-check chain** (`XS2303_research.json` secondary_sources_used): WDI `FI.RES.XGLD.CD` ultimately
  sources from **IMF International Financial Statistics (IFS)** (higher-frequency, gold separate); China **SAFE**
  Official Reserve Assets is the national upstream (cross-validate only). The with-gold companion `FI.RES.TOTL.CD` is
  listed only to be explicitly *rejected* for this figure.

**No NIPA and no benchmark-IO lineage** — `nipa_touch` and `io_touch` empty.

## 3. Why these sources, from Shaikh's perspective + rejected alternatives

- **Why WDI, not IMF IFS directly or SAFE.** WDI gives a single clean annual, internationally-comparable, openly-licensed
  series that is the "published recipe" the figure cites; IFS (the upstream) is monthly and access-gated, and SAFE is a
  Chinese-language national source better used only for cross-validation (`XS2303_EPR.md` §6). WDI is the reproducible,
  redistributable choice.
- **Why ex-gold, not total reserves.** The figure title is explicit ("without Gold"). Excluding gold is a deliberate
  methodological choice: gold-valuation effects would otherwise contaminate the accumulation trajectory the paper wants
  to show (`XS2303_EPR.md` §6 disambiguation). Including gold (`FI.RES.TOTL.CD`) would answer a different question.
- **Why official reserves, not broader FX assets or SWF holdings.** `FI.RES.XGLD.CD` is the official-sector reserve
  concept (foreign-currency assets + SDR holdings + IMF reserve position); it **excludes** sovereign-wealth-fund assets
  (e.g. CIC, ~$1T) and broader banking-system FX assets. The paper's claim is specifically about *official reserve
  accumulation* as alleged manipulation evidence, so Phase 5 must not fold in CIC (`XS2303_research.json`
  methodology_notes; `XS2303_EPR.md` §6).
- **Rejected alternatives**: `FI.RES.TOTL.CD` (with gold — wrong concept for this figure); IFS monthly (right data,
  wrong frequency/access for an annual replicable pull); SAFE (national source, cross-validate only).

Fig 3's role in the argument: it neutralises the strongest *prima facie* manipulation evidence by putting the reserve
build-up on the record and then (Sections 3–5) reframing it as a symptom of persistent real-cost imbalance financed by
capital flows — consistent with the ULC-7.8 Absolute-Cost story and with the misalignment-literature disarray in Figs 4–5.

## 4. Methodological-change exposure

No NIPA-vintage or IO-benchmark exposure; drift is confined to the WDI/IFS reserve-measurement chain:

1. **WDI vintage revisions.** Historical values 1990–2016 can be revised across WDI vintages; the paper used the **2018
   vintage**, RSCD uses a later live vintage (`XS2303_EPR.md` §7). Tolerance budget (±10% at the anchor, ±1% per year
   elsewhere) absorbs typical revisions (`XS2303_DPR.md` §9).
2. **Release lag.** WDI typically lags 6–12 months from year-end; for the most-recent year the API may return NaN, which
   the loader **propagates (no carry-forward)** (`XS2303_DPR.md` §7 caveat 2).
3. **Concept boundary drift.** The ex-gold official-reserve definition is stable, but any temptation to modernise onto
   total-reserves or to include SWF assets would be a concept break (`XS2303_EPR.md` §6). Gold is separately valued in
   IFS, so a switch of upstream could reintroduce gold-valuation noise.
4. **Country-code stability.** ISO3 `CHN` across the World Bank API — stable, but a concordance-touch point for the pull.

The `_timelines/{NIPA,IO}_CHANGE_TIMELINE.md` risks do not reach XS2303; "2018" on the figure is a WDI access vintage.

## 5. Replication fidelity note

RSCD pulls the exact WDI indicator the figure cites — direct pass-through, no proxy (`XS2303_EPR.md` §6). V03_XS2303
**PASS**, MAE 109, **max 6.7%**, 35 chopped rows (`ES_PHASE_5_8_CLOSURE.md`). The material honesty item:

- **The 2013 anchor is 6.7% off — and this is understood, not a bug.** The paper rounds to "USD 3.6 trillion" for 2013
  (Section 1, p. 433), while WDI reports ~$3,839–3,880 bn for 2013 (`XS2303_research.json` methodology_notes;
  `ES_PHASE_5_8_CLOSURE.md` open-issue 1). $3,600 vs $3,839 ≈ 6.2–6.7% — hence the validator tolerance is deliberately
  set to 10% to absorb the paper's *rounding* of a text-quoted anchor, not a data discrepancy. The other text anchors
  reconcile cleanly (17-fold 2000→2010 = 17.3×; 2014 peak ~$3,843 bn ≈ "nearly USD 4 trillion"). The "almost 30% lower"
  claim (p. 438) is the paper's loosely-rounded characterisation of the 2014→2016/2019 decline (actual 2014→2019 ≈ 19%);
  documented as paper-side rounding, not a replication error.
- **Self-consistency caveat.** The validator compares the processed parquet against a fresh API pull (identity match
  expected for direct pass-through); it does *not* re-read the 2018-vintage Fig 3 independently — that would require
  digitising the chart (`XS2303_EPR.md` §7).
- **Concept-fidelity held.** RSCD uses ex-gold official reserves only; it does not fold in `FI.RES.TOTL.CD` (with gold)
  or CIC/SWF assets (`XS2303_DPR.md` §7 caveat 1; `XS2303_EPR.md` §6). No agency or concept substitution.

## 6. Forward risk

- **WDI release lag on the current year.** For 2024 the API may lag into early 2025; the loader propagates NaN rather
  than carry forward — extensions must not backfill (`XS2303_DPR.md` §7 caveat 2; `XS2303_research.json`
  extension_candidates).
- **Vintage revisions on history.** Later WDI vintages keep re-touching 1990–2016; pin `data_vintage_pulled_at` and
  absorb within tolerance (`XS2303_EPR.md` §7).
- **Indicator-code stability.** `FI.RES.XGLD.CD` is unlikely to be renamed, but a change must fail loud, not silently
  substitute the with-gold indicator (`XS2303_EPR.md` §5).
- **Concept-drift temptation.** Future maintainers must not switch to `FI.RES.TOTL.CD` or add SWF holdings — either
  would break the paper's ex-gold official-reserve concept (`XS2303_EPR.md` §6).
- **Optional companion.** A `FI.RES.TOTL.CD` (with-gold) comparator could be offered as a *related* series for context,
  but never as the Fig-3 replication (`XS2303_research.json` open_questions).

---

### Dossier JSON

```json
{
  "sid": "XS2303",
  "primary_concept": "China official foreign exchange reserves EXCLUDING gold, current USD (World Bank WDI indicator FI.RES.XGLD.CD for CHN), 1990-2024 (paper window 1990-2016; Weber-Shaikh 2020 Fig 3, p.454)",
  "sources": ["World Bank WDI indicator FI.RES.XGLD.CD (Total reserves minus gold, current US$) for CHN", "World Bank Data API (live pull; CC-BY-4.0)", "IMF International Financial Statistics (IFS) - WDI upstream (cross-check)", "China SAFE Official Reserve Assets (national upstream, cross-validate only)"],
  "rejected_alternatives": ["WDI FI.RES.TOTL.CD (total reserves INCLUDING gold - wrong concept; gold-valuation contamination)", "IMF IFS monthly reserves (right data, wrong frequency/access for an annual replicable pull)", "China SAFE (national-language source; cross-validate only)", "sovereign-wealth-fund assets (CIC ~$1T) - excluded from the official-reserve concept"],
  "nipa_touch": [],
  "io_touch": [],
  "concordance_touch": ["country-code: ISO3 CHN across World Bank WDI API", "reserve-concept mapping: FI.RES.XGLD.CD (ex-gold) vs FI.RES.TOTL.CD (incl. gold) vs SWF/CIC (excluded)", "upstream provenance chain WDI <- IMF IFS <- SAFE"],
  "forward_risk": ["WDI 6-12 month release lag on current year (2024 may lag into 2025); NaN propagated, no carry-forward", "WDI vintage revisions keep re-touching 1990-2016 history vs paper 2018 vintage", "indicator-code rename must fail loud, never substitute with-gold indicator", "concept-drift temptation to FI.RES.TOTL.CD or SWF inclusion would break the ex-gold official-reserve concept", "2013 anchor 6.7% off is paper-side rounding ('USD 3.6 trillion' vs WDI ~3839) - tolerance set to 10% by design, monitor if tightened"]
}
```

# XS2302 — Methodological History Report (MHR)

**Series**: XS2302 — China Current Account Balance, level (Billion USD) AND percent of GDP, 1997–2024 (IMF WEO)
**Chapter**: 0 · **xs_class**: external_study · **Group**: 23 (Weber–Shaikh 2020 family)
**Perspective**: authored *from Shaikh's perspective* (co-author of Weber & Shaikh 2020).
**Authored**: 2026-06-30 · **Read-only provenance**; every claim traces to a cited path.

Grounding: `Technical/research/XS2302_research.json`; `Technical/docs/series/XS2302_DPR.md` + `XS2302_EPR.md`;
`Technical/docs/external_studies/XS2301_paper_summary.md` + `ES_PHASE_5_8_CLOSURE.md`. Paper: Weber & Shaikh (2020),
IRAE 35(3–4):432–455, DOI 10.1080/02692171.2020.1814221.

---

## 1. What it is

XS2302 is the paper's **Appendix Figure 2 (p. 453)**: China's **current account balance** as a **dual-axis** chart —
a solid line in **Billion current USD** (left axis, 0–450) and a dotted line in **percent of nominal GDP** (right
axis, 0–12), both over 1997–2017. The figure caption fixes the measure verbatim (`XS2302_research.json` book_quotes,
role=source, p. 453):

> "China Current Account Balance, 1997-2017. China Current Account Balance in Billions USD. China Current Account
> Balance in Percent of GDP. Data Source: IMF, 2018."

The two lines are the **same current-account concept** in two non-commensurable units, which is exactly why the figure
uses a dual y-axis and why the RSCD loader is required to emit **two distinct AnuData rows** — `XS2302-level` (IMF WEO
subject `BCA`) and `XS2302-pctgdp` (subject `BCA_NGDPD`) — never one mixed-unit series (`XS2302_DPR.md` §4;
`XS2302_research.json` methodology_notes, "DUAL-UNIT REQUIREMENT"). The narrative shape (`XS2302_research.json`
formula): the level peaks ~$420 bn in 2007–2008 and falls to ~$165 bn by 2017; the %-of-GDP line peaks ~10% in 2007
and falls to ~1.3% by 2017.

This is the paper's *reversal* exhibit — the empirical fact that China's surplus **collapsed** from ~10% of GDP to near
balance while the US-China bilateral deficit kept widening (Section 1, p. 432: the surplus "sharply decreased to 0.4%
of its GDP" per IMF 2019a). That divergence is the core counter-evidence against currency manipulation: a manipulated,
persistently-undervalued RMB should sustain a large surplus, yet the surplus vanished.

**Distinct from S1101** (`XS2302_research.json` methodology_notes): S1101 uses the IMF **IFS** goods X/M ratio; XS2302
uses IMF **WEO** BCA/BCA_NGDPD — different IMF product, different concept (current account vs goods balance), different
unit choice.

## 2. Source lineage

Single agency, two WEO subjects for country `CHN` (`XS2302_DPR.md` §3; `XS2302_research.json` primary_source):

| Subseries | Coverage | Source | Native units | Retrieval |
|---|---|---|---|---|
| XS2302-level | 1997–2024 | IMF WEO subject **`BCA`** (Current account balance, USD billions) for `CHN` | Billion current USD | IMF Datamapper JSON API (`imf.org/external/datamapper/api/v1/BCA/CHN`) |
| XS2302-pctgdp | 1997–2024 | IMF WEO subject **`BCA_NGDPD`** (Current account balance, % of GDP) for `CHN` | Percent of nominal GDP | IMF Datamapper JSON API |

- **Agency / product**: IMF *World Economic Outlook (WEO) Database*, semi-annual vintages (April & October); the paper
  used the **2018 vintage** (`XS2302_research.json` primary_source; References p. 450 cites "International Monetary
  Fund (IMF). 2018. 'World Economic Database'", URL root `https://www.imf.org/`). Canonical modern DB URL:
  `imf.org/en/Publications/WEO/weo-database`.
- **RSCD access path**: a **LIVE IMF WEO API pull** via `S00_apis.imf_weo_country(country_iso3='CHN',
  subjects=('BCA','BCA_NGDPD'))` (`XS2302_EPR.md` §2; `ES_PHASE_5_8_CLOSURE.md` API-clients). The Datamapper API is
  auth-free; fallback is the WEO bulk CSV.
- **Secondary/cross-check (not spliced)**: IMF *External Sector Report* (annual since 2012), which gives
  multilaterally-consistent CA estimates with asymmetry adjustments — used for cross-validation only, because ESR
  values differ from WEO (`XS2302_research.json` primary_source.secondary_sources_used).

**No NIPA and no benchmark-IO lineage** — XS2302 is IMF macro data, so `nipa_touch` and `io_touch` are empty.

## 3. Why these sources, from Shaikh's perspective + rejected alternatives

- **Why IMF WEO, not China SAFE BoP releases.** Weber & Shaikh want the internationally-comparable, single-provider
  current-account series with a long back-run (WEO reports CHN BCA continuously since 1980) rather than the Chinese
  national BoP source (`XS2302_EPR.md` §6). WEO is the "published recipe" the figure cites.
- **Why current account, not the goods balance.** Fig 1 (XS2301) already carries the bilateral *goods* deficit; Fig 2
  deliberately shifts to the *current account* — the broadest external-balance concept (goods + services + primary +
  secondary income) — because the reversal argument is about China's **overall external position** collapsing to near
  balance, which is stronger evidence against manipulation than any single bilateral line (`XS2302_EPR.md` §6).
- **Why both level and % of GDP.** The level shows the *absolute* magnitude of the surplus at its peak (~$420 bn); the
  %-of-GDP normalisation shows how *dramatic* the reversal is relative to the size of the Chinese economy (10%→1.3%).
  Together they make the "surplus vanished" point undeniable regardless of scaling (`XS2302_DPR.md` §2).
- **Rejected alternative — IMF External Sector Report EBA CA gap.** The ESR gives a *model-assessed* CA norm/gap, not
  the realised CA balance the figure plots; it is offered only as a `cross_validate_not_splice` companion
  (`XS2302_research.json` extension_candidates).

The place of Fig 2 in the Absolute-Cost-Theory argument: with the surplus gone but the bilateral imbalance persisting,
the imbalance cannot be a currency-manipulation artifact (which would require a sustained surplus); it must reflect
persistent real-cost differences financed by endogenous capital flows — the thesis Figs 4–5 then reinforce by showing
the misalignment literature has no consensus.

## 4. Methodological-change exposure

XS2302 carries **no NIPA-vintage or IO-benchmark exposure**; its drift lives entirely in the IMF WEO vintage machinery
and — critically — in the **forecast tail**:

1. **Semi-annual vintage revisions.** WEO revises historical CA values (and the NGDPD denominator) with *every*
   April/October vintage; a re-pull at any later vintage can shift 1997–2017 values by 0.1–0.5 percentage points vs the
   paper's 2018 vintage (`XS2302_DPR.md` §7 caveat 1; `XS2302_research.json` methodology_notes). Extensions must pin the
   vintage (`data_vintage_pulled_at`).
2. **FORECAST CONTAMINATION (the defining exposure).** WEO is not a pure historical series — each vintage carries ~5+
   years of **IMF forecasts** past the current year. The live RSCD pull absorbed these forecast years directly into the
   realised series (see §5). This is the single most important methodological-change fact for XS2302 and is treated in
   full in the fidelity note.
3. **Subject-code stability.** A WEO subject rename (e.g. `BCA` → `CAB`) would break the pull; the EPR mandates a
   *fail-loud* rather than a silent substitution (`XS2302_EPR.md` §5).
4. **Interpretive breaks.** 2020 (COVID) and 2022 (commodity shock) are structural-break observations, not data gaps
   (`XS2302_DPR.md` §7 caveat 2).

None of the `_timelines/{NIPA,IO}_CHANGE_TIMELINE.md` risks reach XS2302; the "2018" on the figure is a WEO data-access
vintage, not a NIPA benchmark year.

## 5. Replication fidelity note

RSCD pulls the same two WEO subjects for CHN that the paper cites — no proxy, no agency substitution
(`XS2302_EPR.md` §6). V03_XS2302 **PASS**, MAE 0.38, max 2.0%, 70 chopped rows (`ES_PHASE_5_8_CLOSURE.md`). But the
honest limits here include a **HIGH-severity honesty failure that must not be understated**:

- **⚠ FINDING F-XS-02 (HIGH) — IMF WEO forecast years presented as realised data.** The chopped for XS2302 **includes
  IMF WEO FORECAST years 2025–2031** (level values 718.6 / 749.3 / 781.7 among them) **inside a series whose DPR,
  `display_name`, and subseries all declare the window 1997–2024** (per shared brief; `XS2302_DPR.md` §1/§5 both say
  1997–2024). The consequences:
  1. The registry `year_range` **silently absorbs to [1997, 2031]** — six forecast years beyond the declared 2024 end.
  2. A **2031 FORECAST value is used as a `reference_value`** for validation — i.e. an IMF projection is being treated
     as a ground-truth anchor.
  3. The forecast years are presented as **realised data with NO projection flag** in the chopped/emitted series.

  This is a genuine data-honesty defect, not a rounding or vintage nuance: it conflates IMF *projections* with *realised
  observations*, and it does so invisibly. Any downstream consumer (a chart, a table, a citation) that reads XS2302
  will treat 2025–2031 IMF forecasts as observed Chinese current-account outcomes. **Remediation**: truncate the emitted
  series at the last realised year (the WEO "estimates start after" boundary for the pinned vintage — realised through
  2024 at most), OR tag forecast years with an explicit `is_forecast=true` / projection flag; and remove the 2031
  forecast from `reference_values`. Until then, XS2302's declared window and its actual content disagree.

- **Vintage vs paper-figure drift.** Because RSCD uses a *later* live vintage than the paper's 2018 vintage, historical
  values can differ slightly from the printed Fig 2; the validator compares the melt against the reconstructed pull, not
  against an independent re-read of the 2018-vintage figure (self-consistency caveat, cf. `XS2302_DPR.md` §9).
- **F-XS-01 units-leak family (context).** The broader XS group carries a chopped units-leak finding
  (`mixed_billions_usd_and_decimal_rates`) where dimensionless/rate subseries are mislabeled billions (per shared
  brief). XS2302 is intrinsically dual-unit (level in `billion_usd`, %-of-GDP in `percent_of_nominal_gdp`); the loader
  correctly tags each subseries (`XS2302_EPR.md` §7), but the presence of a `percent` subseries alongside a `billion_usd`
  subseries is exactly the shape that the F-XS-01 units-hygiene check must confirm is not collapsed to a single mislabeled
  unit.

## 6. Forward risk

- **Fix F-XS-02 before any republish (highest priority).** Truncate to realised years or add an explicit projection
  flag; drop the 2031 forecast from `reference_values`; reconcile the registry `year_range` back to the declared window.
  A published XS2302 that ships IMF forecasts as realised data is a citable-integrity liability.
- **Vintage pinning discipline.** Each re-pull lands a new WEO vintage with revised history *and a new forecast tail*;
  pin and document the vintage every time, and re-apply the forecast-truncation rule (`XS2302_DPR.md` §7).
- **Subject-code monitoring.** Watch for WEO subject renames (`BCA`/`BCA_NGDPD`); fail loud, never substitute
  (`XS2302_EPR.md` §5).
- **Datamapper API availability.** If the Datamapper JSON API returns 4xx/5xx, fall back to the WEO bulk CSV rather than
  degrading silently (`XS2302_DPR.md` §7 caveat 3).
- **Interpretive breaks (2020/2022) persist** in any extension and should be narrated, not smoothed.

---

### Dossier JSON

```json
{
  "sid": "XS2302",
  "primary_concept": "China current account balance in two units - level (Billion current USD, IMF WEO subject BCA) and percent of nominal GDP (BCA_NGDPD) - for country CHN, declared 1997-2024 (paper window 1997-2017; Weber-Shaikh 2020 Fig 2, p.453, dual-axis)",
  "sources": ["IMF World Economic Outlook (WEO) Database, subject BCA for CHN (level)", "IMF WEO subject BCA_NGDPD for CHN (percent of GDP)", "IMF Datamapper JSON API (live pull path)", "WEO bulk CSV (fallback)", "IMF External Sector Report (cross-validate only, not spliced)"],
  "rejected_alternatives": ["China SAFE national BoP releases (national source; WEO is the internationally-comparable published recipe)", "goods trade balance instead of current account (reserved for XS2301; CA is the broader reversal concept)", "IMF ESR EBA CA-gap/norm (model-assessed, not realised CA; cross-validate only)", "single mixed-unit series (dual-axis figure requires two AnuData rows)"],
  "nipa_touch": [],
  "io_touch": [],
  "concordance_touch": ["country-code: ISO3 CHN across IMF WEO / Datamapper", "IMF WEO subject-code mapping BCA (level) vs BCA_NGDPD (% of GDP) vs NGDPD (denominator)", "unit-split concordance level (billion_usd) vs pctgdp (percent_of_nominal_gdp)"],
  "forward_risk": ["F-XS-02 (HIGH): chopped includes IMF WEO FORECAST years 2025-2031 (levels 718.6/749.3/781.7) inside a declared 1997-2024 series; registry year_range silently absorbs to [1997,2031]; a 2031 forecast used as reference_value; forecasts presented as realised with NO projection flag - remediate by truncation or explicit forecast flag", "semi-annual WEO vintage revisions shift 1997-2017 by 0.1-0.5pp vs paper 2018 vintage; each re-pull adds a fresh forecast tail", "WEO subject-code rename (BCA->CAB) must fail loud, not substitute silently", "F-XS-01 units-hygiene: dual-unit series must keep billion_usd vs percent subseries labels distinct", "Datamapper API 4xx/5xx -> fall back to WEO bulk CSV, do not degrade silently", "COVID-2020 and 2022 commodity-shock interpretive breaks"]
}
```

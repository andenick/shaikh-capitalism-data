# XS2301 — Methodological History Report (MHR)

**Series**: XS2301 — US Merchandise Trade Balance, World Total and China, 2002–2024 (Census FT900)
**Chapter**: 0 · **xs_class**: external_study · **Group**: 23 (Weber–Shaikh 2020 family)
**Perspective**: authored *from Shaikh's perspective* (co-author of Weber & Shaikh 2020) — why the paper built this object the way it did.
**Authored**: 2026-06-30 · **Read-only provenance**; every claim traces to a cited path.

Grounding: `Technical/research/XS2301_research.json`; `Technical/docs/series/XS2301_DPR.md` + `XS2301_EPR.md`;
`Technical/docs/external_studies/XS2301_paper_summary.md` (covers the whole 2301–2305 Weber–Shaikh family) +
`ES_PHASE_5_8_CLOSURE.md`. Paper: Weber, I. & Shaikh, A. (2020), "The U.S.-China trade imbalance and the theory of
free trade: debunking the currency manipulation argument," *International Review of Applied Economics* 35(3–4):432–455,
DOI 10.1080/02692171.2020.1814221. Source PDF: `SalvagedInputs/methodology_library/B_shaikh_post2016/WL-B-Weber-001_libgen.pdf`.

---

## 1. What it is

XS2301 is the paper's **headline empirical exhibit — Appendix Figure 1 (p. 453)**: the annual **US merchandise
(goods) trade balance** plotted for two trading partners on one chart, the **World Total** (solid line) and **China**
(dashed line), both in Billion current USD, both negative throughout (the US runs a goods deficit). The figure's own
caption fixes the measure verbatim (`XS2301_research.json` book_quotes, role=source, p. 453):

> "U.S. Trade Balance in Billion USD, 2002-2017. *Total Exports Value minus Customs Import Value in USD. World Total.
> China. Data Source: U.S. Census Bureau, 2018."

The asterisk note is the operative definition: the plotted balance is **Total Exports Value − Customs Import Value**,
i.e. the **Census-basis** goods balance (not the BEA balance-of-payments-basis goods balance, and not the current
account). Per `XS2301_DPR.md` §4 the RSCD loader reads the `TOTAL {YYYY}` annual Balance row (current USD millions)
off the Census FT900 country pages and divides by 1000 to present Billion USD.

The empirical point the figure makes (paper Section 1, p. 432, `book_quotes` role=definition): China's share of the
US deficit rose "from around one-fifth in 2002 … to about one-third in 2008." 2002 is the deliberate start year —
"the first year after China's accession to the World Trade Organisation (WTO)" (p. 432) — so the exhibit isolates the
post-WTO bilateral divergence. Endpoint magnitudes (`XS2301_DPR.md` §1): World Total −468.3 bn (2002) → −792.4 bn
(2017); China −103.1 bn (2002) → −375.2 bn (2017); paper figure-reads ≈ −474/−810 (World) and ≈ −103/−376 (China).

**Distinct from S1101** (`XS2301_research.json` methodology_notes): the book's Ch11 "Trade Balances in Major Countries"
uses the **IMF IFS goods X/M ratio** (unitless) for a 15-country panel 1960–2009; XS2301 uses the Census FT900 **USD
trade-balance level** for the US bilaterally against China and World, 2002–2017. Different source, unit, coverage, window.

## 2. Source lineage

Single agency, two partner pages (`XS2301_DPR.md` §3; `XS2301_research.json` primary_source):

| Subseries | Coverage | Source | Native units | Retrieval |
|---|---|---|---|---|
| XS2301-world | 2002–2024 | US Census FT900, all-countries goods-balance page (**c0004**) | Millions USD | `census.gov/foreign-trade/balance/c0004.html` |
| XS2301-china | 2002–2024 | US Census FT900, China goods-balance page (**c5700**) | Millions USD | `census.gov/foreign-trade/balance/c5700.html` |

- **Agency**: U.S. Census Bureau, Foreign Trade Division, *U.S. International Trade in Goods and Services (FT900)* —
  monthly release; country detail via Exhibit 14 (Trade in Goods with China) and Exhibit 1 (US total goods)
  (`XS2301_research.json` primary_source.publication). Both country pages are public, key-free HTML carrying one
  `TOTAL {YYYY}` annual row (Exports / Imports / Balance, current USD millions, Census basis).
- **License**: U.S. Federal Government public domain (17 USC 105) — the cleanest license posture of the family.
- **Secondary/alternative access** (not chart sources): USA Trade Online (`usatrade.census.gov`, same underlying FT900
  microdata, custom HS-code aggregations, bulk download requires an account) and — as a *narrative* source only for the
  post-window "USD 419 billion 2018 record" headline (p. 432) — the U.S. Treasury *Report to Congress on Macroeconomic
  and Foreign Exchange Policies of Major Trading Partners (May 2019)*.

There is **no NIPA and no BEA I-O lineage here** — XS2301 sits entirely on Census customs-documented trade statistics,
so it carries none of the GPIM/Sraffa NIPA-vintage or benchmark-IO exposure that dominates the appendix (XS001–XS009)
and Sraffa (XS2001/XS2101) series.

## 3. Why these sources, from Shaikh's perspective + rejected alternatives

- **Why Census FT900, not BEA International Transactions (BoP basis).** Weber & Shaikh want the *most direct, most
  granular bilateral* goods balance, at the country level, that the public record supplies monthly. Census customs
  documentation is the primary observation; BEA's ITA Table 4.1 goods balance layers on balance-of-payments coverage
  and timing adjustments (`XS2301_EPR.md` §7). Using the Census basis keeps the exhibit at the level of the raw
  bilateral flows the currency-manipulation debate actually invokes, and the figure footnote pins it explicitly
  ("Total Exports Value minus Customs Import Value").
- **Why the World Total AND the China line on one chart.** The paper's rhetorical hook is a *share*: the bilateral
  US-China deficit as a fraction of the total US deficit (one-fifth→one-third, p. 432). Plotting both lines lets the
  reader see the China wedge widen against the whole — the empirical entry point for the entire currency-manipulation
  critique that Sections 4–5 then dismantle.
- **Why 2002 as the start.** WTO accession (Dec 2001) is the structural pivot; starting in 2002 makes the figure a
  clean "post-WTO" bilateral story rather than a mixed pre/post-accession series (`XS2301_research.json` methodology_notes).
- **Rejected alternative — current account instead of goods balance.** Deliberately not used for Fig 1: the current
  account (which XS2302 supplies from IMF WEO) adds services, primary and secondary income; Fig 1 is specifically the
  *goods* bilateral, because that is where the "China deficit" political salience lives (`XS2301_EPR.md` §6).
- **Rejected alternative — a single US-China number without the World denominator.** That would show a level but not
  the *share* dynamic that motivates the paper's framing; the two-line design is the argument.

The deeper "why" (shared across XS2301–XS2305): these are the paper's Absolute-Cost-Theory evidence base. Figs 1–3
establish that the imbalance is *large, persistent, and financed by reserve accumulation*; Figs 4–5 then show the
misalignment literature cannot even agree on the sign of RMB misalignment (−36% to +50%), so the imbalance must be
explained by **real cost differences** (US/China manufacturing ULC ratio 7.8, Golub et al. 2018, p. 437), not currency
manipulation. XS2301 is the "how big is the imbalance" foundation of that chain.

## 4. Methodological-change exposure

XS2301 has **no NIPA-vintage and no benchmark-IO exposure** (`nipa_touch` and `io_touch` are empty) — it is not built
on the national accounts or the input-output tables. Its methodological drift is concentrated in the Census trade
apparatus and in the post-window policy regime:

1. **HS-code / classification revisions in FT900.** Census periodically revises the Harmonized System aggregations
   underlying FT900. Per `XS2301_research.json` extension_candidates.concerns, "Census periodically revises HS code
   aggregations; 2022 HS revision may affect comparability of fine-grained subcategories but **not the country-level
   total**." Because XS2301 consumes only the country-level `TOTAL` balance, the HS-code churn is a
   *concordance-touch* risk on any sub-category drill-down, not on the plotted series itself.
2. **Census-basis vs BoP-basis.** FT900 Exhibit 1 publishes both a Census-basis and a BoP-basis goods balance
   (`XS2301_research.json` extension_candidates). The paper uses Census basis (per the Fig 1 footnote); any re-pull must
   stay on Census basis for splice consistency (`XS2301_DPR.md` §7 caveat 1). Silently switching to BoP basis would
   introduce a coverage/timing discontinuity.
3. **Section 301 tariff valuation break (2018–).** The Trump Section-301 tariffs (covering ~$370bn of Chinese imports
   by 2019) mean post-2018 customs import *values* now embed tariff-inclusive valuations for some HTS lines
   (`XS2301_EPR.md` §6; `XS2301_research.json` extension_candidates). This is a genuine valuation-methodology shift
   inside the extension window, documented as interpretive (structural break), not a data gap.
4. **COVID-2020 compression.** 2020 briefly narrowed the bilateral deficit (`XS2301_research.json` extension_candidates)
   — a one-off, again interpretive.

None of these is a NIPA comprehensive-revision or IO-benchmark exposure; the `_timelines/{NIPA,IO}_CHANGE_TIMELINE.md`
risks that dominate the GPIM/Sraffa series do **not** reach XS2301. The frozen "2018 data-access vintage" on the figure
is a Census vintage, not a NIPA benchmark.

## 5. Replication fidelity note

RSCD reproduces XS2301 by pulling **exactly the source the paper cites** (Census FT900), not a proxy — no agency and no
concept substitution (`XS2301_EPR.md` §6). Honest limits, disclosed:

- **Figure-read vs source-value tolerance.** The World-Total endpoints are *eyeballed* off the appendix chart
  (−474/−810); the constructed Census source values (−468.3/−792.4) differ by 1.2–2.2%, inside the ±10% validator
  tolerance; the China endpoints match to <1% (`XS2301_DPR.md` §7 caveat 3, §10). V03_XS2301 **PASS** (4/4 anchors,
  max 2.17% error; `ES_PHASE_5_8_CLOSURE.md`).
- **Truncation-repair history (the honest scar).** The *earlier* loader keyed the annual figure off a four-digit
  *column header* that does not exist on the Census country pages; the scrape silently failed and the series degraded
  to the five salvaged **Fig-1 anchor** points (World 2002/2017; China 2002/2017/2018) — figure-reads, truncated at
  2018 — while the DPR *claimed* continuous coverage to 2024 (`XS2301_DPR.md` §8). This was repaired 2026-06-11:
  `L01_XS2301.py` + new `S00_apis.census_country_annual_balance` now read the `TOTAL {YYYY}` rows directly from c0004
  (World) and c5700 (China), yielding **23 real annual observations per partner, 2002–2024, no fabrication, no
  interpolation** (`XS2301_DPR.md` §8; `XS2301_EPR.md` §2). The verbatim Fig-1 anchors survive only as a last-resort
  per-partner fallback if a page fetch fails.
- **FINDING F-XS-04 (stale registry `year_range`).** The loader was rebuilt to 2024, but the **registry
  `year_range=[2002,2018]` is STALE** (per shared brief; `ES_PHASE_5_8_CLOSURE.md` open-issue 2). The registry
  understates the actual coverage by six years — a documentation/registry-reconciliation defect, not a data defect.
- **Source-id note (registry drift).** The World subseries now draws on c0004, but the registry still records
  `CENSUS_FT900_EXH1` / `exh1.txt`, a historical path that **now 404s** (`XS2301_DPR.md` §8). Recommended
  reconciliation: rename the World subsource to `CENSUS_FT900_C0004` with `source_url = …/balance/c0004.html`
  (flagged in the triage patch; registry read-only in that pass).
- **SPA caveat.** Census per-country *interactive* pages are JS-rendered SPAs with no static data URL in the current
  vintage (`ES_PHASE_5_8_CLOSURE.md` open-issue 2), which is *why* v1.0 originally fell back to Fig-1 anchors; the
  rebuild instead reads the plain HTML `balance/cNNNN.html` pages.

## 6. Forward risk

- **Registry reconciliation (immediate).** Fix F-XS-04 (`year_range → [2002,2024]`) and the `CENSUS_FT900_EXH1 →
  CENSUS_FT900_C0004` source-id/URL rename before any republish, or downstream consumers will trust a stale bound and a
  404 URL (`XS2301_DPR.md` §8).
- **Census HTML layout drift.** The loader degrades gracefully (publishes whichever partner parsed;
  `XS2301_EPR.md` §5) but a Census portal redesign could break the `TOTAL {YYYY}` parse; the SPA-only interactive path
  is deliberately avoided. Monitor c0004/c5700 page structure at each extension.
- **Section-301 / tariff-regime continuation.** Post-2018 customs valuations remain tariff-inclusive for covered HTS
  lines; any narrative use of the extension must keep flagging the valuation break rather than reading it as a pure
  volume signal (`XS2301_EPR.md` §6).
- **HS-code revisions (2022 and future).** Country-level totals are robust, but any future sub-category decomposition
  needs the HS revision concordance to remain comparable (`XS2301_research.json` extension_candidates).
- **BoP-basis temptation.** Future maintainers must not "modernise" onto the BEA ITA BoP-basis goods balance — that
  would silently break continuity with the paper's Census-basis recipe (`XS2301_EPR.md` §7).

---

### Dossier JSON

```json
{
  "sid": "XS2301",
  "primary_concept": "US merchandise (goods) trade balance, Census basis (Total Exports Value - Customs Import Value), for World Total and China, 2002-2024 (paper window 2002-2017; Weber-Shaikh 2020 Fig 1, p.453)",
  "sources": ["US Census Bureau FT900 all-countries goods-balance page (c0004)", "US Census Bureau FT900 China goods-balance page (c5700)", "FT900 Exhibit 1 (US total goods) and Exhibit 14 (Trade in Goods with China)", "USA Trade Online (usatrade.census.gov, secondary access)", "US Treasury 2019 FX Report (narrative only, 2018 $419bn headline)"],
  "rejected_alternatives": ["BEA International Transactions Table 4.1 BoP-basis goods balance (coverage/timing adjustments break continuity)", "current account instead of goods balance (adds services/income; reserved for XS2302)", "single US-China level without the World denominator (loses the share dynamic that is the argument)", "USA Trade Online auth API (auth-gated; public HTML pages used instead)"],
  "nipa_touch": [],
  "io_touch": [],
  "concordance_touch": ["Census FT900 HS-code aggregation revisions (2022 HS revision affects sub-categories, not country-level total)", "country-code mapping: Census page code c0004 (World/all-countries) vs c5700 (China)", "Census-basis vs BoP-basis goods-balance basis reconciliation"],
  "forward_risk": ["F-XS-04: registry year_range=[2002,2018] STALE vs loader rebuilt to 2024", "registry source-id drift: CENSUS_FT900_EXH1/exh1.txt now 404s -> rename to CENSUS_FT900_C0004", "Census SPA/HTML layout change could break the TOTAL {YYYY} parse (SPA interactive path deliberately avoided)", "Section 301 tariff-inclusive customs valuations create a post-2018 valuation break", "COVID-2020 one-off compression; future HS-code revisions on any sub-category drill-down", "risk of silent modernisation onto BEA ITA BoP-basis (would break paper's Census-basis recipe)"]
}
```

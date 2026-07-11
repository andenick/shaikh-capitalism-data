# S212 — US & UK Wholesale Prices in Ounces of Gold, 1790–2010 — Methodological History Report (MHR)

**Group:** ch2 (Turbulent Trends and Hidden Structures) · **Construction:** formula (WPI ÷ gold price) · **Status:** book_period_validated
**Figure:** 2.10 · **Predecessor:** CD S012 (reproduced via CD2 S024 UK + S025 US) · **Publish:** true · **Book period:** 1790–2010 (registry span 1780–2024) · **Extension:** 2011–2025 (formula recompute)
**Reasoning stance:** from Shaikh's own perspective — why *he* built the series this way.

> Grounding note: every author-intent claim below is anchored to a citable path — the research JSON
> (`Technical/research/S212_research.json`), the DPR/EPR (`Technical/docs/series/S212_{DPR,EPR}.md`),
> the registry (`Technical/series_registry.json` → `series.S212`), the book KB (Body_Text
> `ch02_turbulent_trends.md`, Figure `ch02_fig_2.10.md`), the predecessor dossiers
> (`SalvagedInputs/methodology_decisions/CD2_research_md/S024.md` UK, `S025.md` US), the CH2 review
> (`Technical/methodology_review/CH02_review.json`), and the Phase-0 NIPA timeline
> (`Technical/docs/methodology/_timelines/NIPA_CHANGE_TIMELINE.md`). Where a rationale is not present in the
> corpus it is marked **"author rationale not located in corpus."** Underlying WPI/gold detail is in the
> sibling **`S210_MHR.md`**.

---

## 1. What the series is

S212 is a **derived (formula) series**: the **US and UK wholesale price levels expressed in ounces of gold,
1790–2010**, each obtained by **dividing the national WPI by that country's gold price**, then both rebased to
**1930 = 100** and plotted on a log scale as **Figure 2.10** (KB `Figures/ch02/ch02_fig_2.10.md`, book p. 64).
Shaikh's definition (book p. 64, `S212_research.json` book_quotes[0], role=definition): "It is therefore
instructive to consider UK and US prices not in terms of their respective national currencies, but in terms of
the common international standard of gold. To do this, one only needs to divide the price level in each country
by the price of gold in that same currency … The resulting **'golden waves'** show us something quite
fascinating." The payoff (KB `ch02_fig_2.10.md`, body text lines 468–475): expressed in gold, the pre-war long
waves reappear *and* **two postwar long waves emerge — peaking in 1970 and 2000** — with periodicities close to
Kondratieff's, tying the 2007–2008 crisis to the downswing of the second postwar wave (and forward to the
crisis dating in Chs 16/17).

**Ch5/App 5.3 shared data:** S212's gold-denominated construction is the Ch2 face of the *same* dossier that
Chapter 5 develops as **Figs 5.5 (UK) and 5.6 (US)** — "UK/US Wholesale Price Indexes in Gold Ounces and …
Price of Gold" — decomposing the price index into golden price × the currency price of gold per Marx's
equation (5.9) (`CD2_research_md/S024.md`, `S025.md`). Appendix 2.1 cross-references Appendix 5.3; the canonical
deep dossier lives in Ch5.

Final units: **Index, 1930 = 100** (log), representing WPI deflated by the gold price (`S212_DPR.md` §6).

## 2. Source lineage — the formula and its inputs

**Formula (`series_registry.json` S212.formula; `S212_DPR.md` §4):**

> `WPI_in_gold[country, t] = WPI[country, t] / gold_price[country, t]`, both rebased to **1930 = 100**.

**Numerator — WPI:** the same US and UK wholesale price indexes as **S210** (`S210-A`, `S210-B`; Jastram 1977
Tables 7/2 + growth-rate extensions). See `S210_MHR.md` §2.

**Denominator — gold price (per Appendix 2.1, book p. 764):**
| Segment | Coverage | Source / id | Native units | Note |
|---|---|---|---|---|
| **US gold, early estimate** | **1780–1785** | **estimated from the 1786 US/UK gold-price ratio** | $/oz | UK gold exists in Jastram for 1780–85; the US price is inferred via the 1786 ratio, "essentially constant until 1800" |
| US gold, official | 1786–1790 | **MeasuringWorth** (official price) | $/oz | Officer & Williamson, "The Price of Gold, 1257–2010" |
| US gold, market | 1791–2010 | MeasuringWorth (market price) | $/oz | |
| UK gold, £ | 1786–1949 | MeasuringWorth (market gold price in £) | £/oz | |
| UK gold, £ (converted) | 1950–2010 | MeasuringWorth US$ gold **÷ US$–£ exchange** (Officer, "Dollar–Pound Exchange Rate From 1791") | £/oz | source publishes UK gold in US$ after 1949; converted back to £ |

Both country ratios are then indexed to **1930 = 100**. Grounding: MeasuringWorth gold dataset
(`https://www.measuringworth.com/datasets/gold/`); Jastram base referenced from HathiTrust
`Record/000404889`. The 1780–1785 US ratio estimate is the one genuinely bespoke construction step in the
denominator.

## 3. Why these sources — author's perspective

- **Why express prices in gold at all (the golden-wave rationale).** Shaikh's explicit argument (book p. 64,
  body text lines 385–391): "money is not a single thing. It is a series of layers: **credit money**, which
  rests on the health of a particular bank; **national currency**, which rests on the health of a particular
  national government; and widely exchangeable commodities such as **gold**, whose … status rests on the health
  of global commodity circulation." Gold is the "**(now unofficial) currency of last resort for the international
  system**" (body text line 460). Dividing each national WPI by its own gold price strips out
  national-currency-specific inflation/devaluation and re-states prices in a **common international standard**,
  which is what lets the postwar long waves (invisible in national-currency prices) reappear. This is the
  strongest, best-grounded rationale in the whole family.
- **Why Jastram + MeasuringWorth specifically.** Jastram's *Golden Constant* was built precisely to pair a
  wholesale price index with a matching gold series over centuries, so WPI ÷ gold is native to the source; the
  gold price itself is extended/back-filled with MeasuringWorth (Officer & Williamson), the standard scholarly
  long-run gold compilation. An explicit statement of *why these over alternatives* (e.g. Jastram's own
  *Silver: The Restless Metal*, or other gold histories) is **author rationale not located in corpus** — the
  salvaged library holds no Shaikh text weighing gold-source alternatives.
- **Why the 1786-ratio estimate for 1780–85 US gold.** A pragmatic completeness choice: the US gold price is
  unavailable that early, but the US/UK ratio is "essentially constant until 1800," so the UK price (which does
  exist) carries the early US denominator — preserving the 1790-start figure without fabricating a level.

## 4. Methodological-change exposure

- **BLS WPI→PPI rename/renumber** flows through the **numerator** exactly as in S210 (WPS00000000 frozen →
  WPU00000000 successor for the post-1974 US WPI). Because S212 is a **ratio**, the extension must **recompute**
  from extended WPI and extended gold — never splice the ratio directly (`S212_research.json`
  extension_candidates[0]; `S212_DPR.md` §7; `S212_EPR.md` §2).
- **Gold-price source (denominator).** **MeasuringWorth (Officer & Williamson) is a stable, frozen historical
  compilation** — historical gold values are not revised, only extended — so the denominator carries low
  methodological-change risk; the only open item is verifying the through-year on refresh
  (`S212_research.json` open_questions; `series_registry.json` adequacy.issues_outstanding).
- **ONS UK price revisions** apply only via the UK numerator extension (`PLLU`), same as S210.
- **NIPA / IO timelines DO NOT apply.** S212 is built from BLS/ONS/Jastram wholesale prices and MeasuringWorth
  gold — **no NIPA and no benchmark I-O content.** The BEA comprehensive-revision / T7.11 events in
  `NIPA_CHANGE_TIMELINE.md` do not touch this series. Stated explicitly per the task contract.

## 5. Replication fidelity note

- **Truth basis:** RSCD reproduces the book-period values from **CD2 S024 (UK, Fig 5.5)** and **CD2 S025 (US,
  Fig 5.6)** — the Ch5 gold-denominated counterparts (`CD2_research_md/S024.md`, `S025.md`; `S212_DPR.md` §3).
  Registry `reference_values`: 1780 = 122.050, 1902 = 68.2 (`series_registry.json` validation), matching CD2
  S025 US-in-gold 1780 = 122.0500.
- **Formula-recompute extension (no lazy ratio splice):** the 2011–2025 extension **recomputes** WPI ÷ gold
  from extended S210 components + extended gold price (FRED `WPU00000000` numerator, FRED
  `GOLDPMGBD228NLBM` gold denominator), rescaled to 1930 = 100 at the 2010 anchor — per the Anu no-lazy-splice
  rule for derived quantities (`S212_DPR.md` §4, §7; `S212_EPR.md` §2, status `feasible`).
- **WPU-substitutes-frozen-WPS:** direct BLS successor, not a proxy (`S212_EPR.md` §3).
- **Honest limits:** the **UK gold-denominated extension is deferred to Phase 9** (requires a GBP gold price +
  UK WPI extension, and the ONS `PLLU` numerator itself is DEFERRED on a transient 502 — see `S210_MHR.md` §5);
  `S212_DPR.md` §7. Where any API returns NaN, the NaN propagates — no synthetic fill (`S212_EPR.md` §4).

## 6. Forward risk

- **BLS PPI re-basing / renumber** (numerator) — same low-risk growth-rate splice exposure as S210; re-verify
  `WPU00000000` on refresh.
- **Gold-source updates** — MeasuringWorth may extend but rarely revises history; confirm the through-year and,
  for the extension denominator, that FRED `GOLDPMGBD228NLBM` remains published (it is at some discontinuation
  risk as an LBMA daily gold series).
- **ONS UK discontinuation** — blocks completion of the deferred UK-in-gold extension until `PLLU` successor
  identity is confirmed.
- **Derived-series integrity** — the standing risk is that a future maintainer splices the *ratio* directly
  instead of recomputing from components; the EPR/DPR pin the recompute rule to prevent this.

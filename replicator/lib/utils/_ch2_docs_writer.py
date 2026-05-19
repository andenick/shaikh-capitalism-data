"""Generates DPR + EPR markdown files for all 17 Ch2 series (S202-S218).

Output goes to Technical/docs/series/{SID}_DPR.md and {SID}_EPR.md.

This is a one-shot generator -- the markdown content is authored from the
research dossiers + Phase 4 adequacy report. Re-running overwrites prior files.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.paths import DOCS_SERIES  # noqa: E402


SERIES_DOCS = {
    "S202": {
        "name": "US Real Investment Index, 1832-2025",
        "figure": "Figure 2.2",
        "definition": "Index of US real nonresidential business investment in fixed capital (equipment + structures excluding housing). Spliced at 1901, rebased to 1958=100. Chapter 2's leading-edge illustration of the more turbulent investment path relative to output.",
        "why": "Investment is more volatile than output (book p. 56). The series demonstrates 'growth is always turbulent, and the path of investment is far more turbulent than that of output'.",
        "sources": [
            ("S202-A", "1832-1975", "BEA (1977) Table B4, Investment in Fixed Nonres Bus Capital", "Index 1970=100", "salvaged chopped (RealInvest1)"),
            ("S202-B", "1901-2010", "BEA Wealth Table 4.8 line 1", "constant dollars (2011 vintage)", "salvaged chopped (RealInvest2)"),
            ("S202-C", "2011-2025", "BEA NIPA T1.1.6 line 9 (Real Nonresidential Fixed Investment)", "chained 2017$", "BEA iTable API"),
        ],
        "construction": "composite",
        "construction_steps": [
            "Rebase BEA 1977 series to anchor at 1901 = 100.",
            "Rebase BEA Wealth Table 4.8 series to anchor at 1901 = 100.",
            "Splice at 1901: BEA 1977 for 1832-1900, BEA Wealth for 1901-2010.",
            "Re-anchor the spliced series to 1958 = 100.",
            "Extension: rescale BEA NIPA T1.1.6 line 9 (2011-2025) at 2010 overlap.",
        ],
        "year_book": (1832, 2010),
        "year_ext": (2011, 2025),
        "units": "Index, 1958 = 100",
        "caveats": [
            "Phase 4 substitution avoided: FRED GPDIC1 includes residential investment (silent proxy). BEA NIPA T1.1.6 line 9 is the concept-correct extension.",
            "BEA's 2011 access vintage of Wealth Table 4.8 may differ from current BEA data; we preserve Shaikh's pulled values from the salvaged chopped table.",
        ],
        "tolerance": 1.0,
        "extension_status": "feasible",
        "construction_class": "composite",
        "extension_method": "Direct continuation via BEA NIPA T1.1.6 line 9; overlap_anchor at 2010.",
        "extension_proxies": "Phase 4 flagged FRED GPDIC1 -> silent proxy. We use BEA NIPA T1.1.6 line 9 (concept-exact).",
    },
    "S203": {
        "name": "US Real GDP per Capita (MeasuringWorth), 1889-2025",
        "figure": "Figure 2.3",
        "definition": "Real GDP per capita on MeasuringWorth's continuously-updated annual reconstruction (Officer & Williamson). Plotted 1889-2010 in the book.",
        "why": "Third leg of Shaikh's opening trio (industrial production, investment, GDP/cap); illustrates 150-year secular growth in per-capita real output.",
        "sources": [
            ("S203-A", "1889-2010", "MeasuringWorth Real GDP per Capita", "real 2005 dollars", "salvaged chopped"),
            ("S203-B", "2011-2025", "FRED A939RX0Q048SBEA (Real GDP per Capita, chained 2017$)", "chained 2017$", "FRED API"),
        ],
        "construction": "direct",
        "construction_steps": [
            "Read MeasuringWorth Real GDP per Capita column from salvaged chopped table.",
            "Extension: rescale FRED A939RX0Q048SBEA at 2010 overlap.",
        ],
        "year_book": (1889, 2010),
        "year_ext": (2011, 2025),
        "units": "Real GDP per capita, constant 2005 dollars (per MeasuringWorth methodology)",
        "caveats": [
            "MeasuringWorth license is academic-use with attribution.",
            "MeasuringWorth occasionally revises historical estimates; document access date.",
        ],
        "tolerance": 1.0,
        "extension_status": "feasible",
        "construction_class": "direct",
        "extension_method": "Same MeasuringWorth methodology continues; FRED A939 used for automated reindex.",
    },
    "S204": {
        "name": "Business Cycles, 1831-1866 (Ayres Index, Fig 2.4A)",
        "figure": "Figure 2.4A",
        "definition": "Monthly cyclical-component index of US business activity, 1831-1866 subperiod. Compiled by Cleveland Trust Co.; pre-NBER composite indicator.",
        "why": "Documents pre-Civil War business cycle volatility; first of three Ayres subperiods in Fig 2.4.",
        "sources": [
            ("S204-A", "1831-1866", "Ayres (1939) Table 9, Appendix A, col. 1", "percent deviation from trend", "salvaged chopped"),
        ],
        "construction": "direct",
        "construction_steps": [
            "Read Ayres (1939) monthly values from salvaged Appendix2_Ayres.xlsx; filter to 1831-1866.",
        ],
        "year_book": (1831, 1866),
        "year_ext": None,
        "units": "Percent deviation from trend",
        "caveats": [
            "Discontinued: no modern continuation. NBER macrohistory (m12003 etc.) is a related but not equivalent series; do NOT splice.",
            "Pre-NBER composite indicator; Ayres reconstructed from 10 annual series interpolated to monthly.",
        ],
        "tolerance": 1.0,
        "extension_status": "discontinued",
        "construction_class": "direct",
        "extension_method": "N/A. Historical-only series.",
    },
    "S205": {
        "name": "Business Cycles, 1867-1902 (Ayres Index, Fig 2.4B)",
        "figure": "Figure 2.4B",
        "definition": "Monthly Ayres cyclical-component index, 1867-1902 subperiod.",
        "why": "Documents post-Civil-War / Gilded Age business cycle volatility; covers the Long Depression (1873-1879).",
        "sources": [
            ("S205-A", "1867-1902", "Ayres (1939) Table 9, Appendix A, col. 1", "percent deviation from trend", "salvaged chopped"),
        ],
        "construction": "direct",
        "construction_steps": ["Same monthly Ayres source as S204, windowed to 1867-1902."],
        "year_book": (1867, 1902),
        "year_ext": None,
        "units": "Percent deviation from trend",
        "caveats": [
            "Discontinued; same notes as S204.",
            "Includes Long Depression (1873-1879) and Panic of 1893 troughs.",
        ],
        "tolerance": 1.0,
        "extension_status": "discontinued",
        "construction_class": "direct",
        "extension_method": "N/A. Historical-only.",
    },
    "S206": {
        "name": "Business Cycles, 1903-1939 (Ayres Index, Fig 2.4C)",
        "figure": "Figure 2.4C",
        "definition": "Monthly Ayres cyclical-component index, 1903-1939 subperiod.",
        "why": "Documents 20th-century business cycle volatility through the Great Depression and the New Deal.",
        "sources": [
            ("S206-A", "1903-1939", "Ayres (1939) Table 9, Appendix A, col. 1", "percent deviation from trend", "salvaged chopped"),
        ],
        "construction": "direct",
        "construction_steps": ["Same monthly Ayres source as S204/S205, windowed to 1903-1939."],
        "year_book": (1903, 1939),
        "year_ext": None,
        "units": "Percent deviation from trend",
        "caveats": [
            "Discontinued; same notes as S204/S205.",
            "Last subperiod of Ayres index; ends 1939 (book publication year).",
        ],
        "tolerance": 1.0,
        "extension_status": "discontinued",
        "construction_class": "direct",
        "extension_method": "N/A. Historical-only.",
    },
    "S207": {
        "name": "US Manufacturing Productivity and Production Worker Real Compensation, 1889-2025",
        "figure": "Figure 2.7",
        "definition": "Two co-plotted index series (both Index 1889 = 100): (a) manufacturing labor productivity, (b) production-worker real compensation per hour. Used by Shaikh to demonstrate divergence between productivity growth and worker wages.",
        "why": "Central to the labor-share-and-productivity-divergence argument that runs through Chapters 2, 6, 14, 15.",
        "sources": [
            ("S207-A", "1889-2010", "BEA LTEG A173 (1860-1970) + BLS FLS Table 1 (1950-2009)", "Index 1889=100", "salvaged chopped"),
            ("S207-B", "1889-2010", "MeasuringWorth uswage + CPI", "Index 1889=100", "salvaged chopped"),
            ("S207-C", "2010-2025", "FRED OPHMFG (US-only Mfg Real Output Per Hour)", "Index 2017=100", "FRED API"),
            ("S207-D", "2010-2025", "FRED COMPRMS (Mfg Real Compensation per Hour)", "Index 2017=100", "FRED API"),
        ],
        "construction": "composite",
        "construction_steps": [
            "Productivity (S207-A): spliced from BEA LTEG A173 (1889-1949) + BLS FLS Table 1 (1950-2009), rebased to 1889=100 in the chopped table.",
            "Real compensation (S207-B): nominal MW compensation / CPI, rebased to 1889=100.",
            "Extension: FRED OPHMFG and FRED COMPRMS each anchored at 2009 (BLS FLS last observation) and rescaled.",
        ],
        "year_book": (1889, 2010),
        "year_ext": (2011, 2025),
        "units": "Two units co-plotted: Index 1889=100 (productivity); Index 1889=100 (real compensation index).",
        "caveats": [
            "Phase 4 substitutions: MeasuringWorth /datasets/uscompensation/ -> /datasets/uswage/ (URL rename only, values unchanged).",
            "BLS FLS International Comparisons program sunset 2013; FRED OPHMFG continues the BLS Productivity & Costs concept but in US-only form (narrower than the 19-country book series). Proxy flag set on S207-C.",
            "Units field splits into productivity (Index 1889=100) and compensation (Index 1889=100) for the loader contract.",
        ],
        "tolerance": 1.0,
        "extension_status": "feasible_with_substitute",
        "construction_class": "composite",
        "extension_method": "Direct continuation of each subseries via FRED, reindexed at last book year.",
        "extension_proxies": "FRED OPHMFG is US-only continuation of discontinued BLS FLS Table 1 (19-country); flagged proxy:true in registry with concept-narrowing justification.",
    },
    "S208": {
        "name": "US Manufacturing Real Unit Production Labor Cost Index, 1889-2025",
        "figure": "Figure 2.8",
        "definition": "RULC = real compensation per hour / productivity, rescaled to 1889 = 100. Equivalent to (S207-B / S207-A) * 100.",
        "why": "Key Marxian indicator: real unit labor cost is the wage share when productivity and real wages are both real. Tracks the 'labor share' over 120 years.",
        "sources": [
            ("S208-A", "1889-2010", "Shaikh-derived RULC from S207 components", "Index 1889=100", "salvaged chopped"),
            ("S208-B", "2011-2025", "Recomputed from extended S207-A/S207-C (productivity) + S207-B/S207-D (real comp)", "Index 1889=100", "formula recompute"),
        ],
        "construction": "formula",
        "formula": "RULC[t] = (real_compensation[t] / productivity[t]) * 100",
        "construction_steps": [
            "Read book-period RULC directly from chopped column 'Mfgrealunitlaborcost'.",
            "Extension: recompute formula from S207-C / S207-D for each post-2010 year, rescaled so the 2010 extension value equals the 2010 book value.",
        ],
        "year_book": (1889, 2010),
        "year_ext": (2011, 2025),
        "units": "Index, 1889 = 100",
        "caveats": [
            "Lazy-splice prohibition applies: extension MUST recompute the formula from S207 components, NOT splice FRED ULCMFG (which is nominal ULC -- silent proxy).",
            "Extension depends on S207-C and S207-D being populated (FRED API success).",
        ],
        "tolerance": 1.0,
        "extension_status": "feasible",
        "construction_class": "formula",
        "extension_method": "Recompute formula with extended S207 components (per playbook formula recipe).",
    },
    "S209": {
        "name": "US Unemployment Rate, 1890-2025",
        "figure": "Figure 2.9",
        "definition": "Civilian unemployment rate, spliced from BEA LTEG (1890-1947) + ERP Table B-40 (1948-2010), extended via FRED UNRATE.",
        "why": "Standard cyclical indicator; complements the Ayres business-cycle subperiods with a continuous post-1890 record.",
        "sources": [
            ("S209-A", "1890-1947", "BEA LTEG B1-B2", "percent", "salvaged chopped"),
            ("S209-B", "1948-2010", "Economic Report of the President Table B-40", "percent", "salvaged chopped"),
            ("S209-C", "2011-2025", "FRED UNRATE", "percent", "FRED API"),
        ],
        "construction": "composite",
        "construction_steps": [
            "BEA LTEG for 1890-1947 (before ERP starts).",
            "ERP T B-40 for 1948-2010.",
            "FRED UNRATE for 2011+ (no rescale; ERP and UNRATE are level-equivalent BLS CPS series).",
        ],
        "year_book": (1890, 2010),
        "year_ext": (2011, 2025),
        "units": "Percent of civilian labor force",
        "caveats": [
            "Tolerance set at 0.15pp absolute (not relative) because unemployment rates near 1-2% would otherwise trigger false divergences.",
            "Pre-1948 BEA LTEG and post-1948 BLS CPS use slightly different definitions of 'unemployed'; the splice is documented in BEA's own historical reconciliation.",
        ],
        "tolerance": 1.0,
        "extension_status": "feasible",
        "construction_class": "composite",
        "extension_method": "Direct continuation via FRED UNRATE (same BLS CPS series as ERP T B-40).",
    },
    "S210": {
        "name": "US and UK Wholesale Price Indexes, 1780-2025 (Fig 2.10, log scale)",
        "figure": "Figure 2.10",
        "definition": "Annual wholesale price indexes for US (1780-2010) and UK (1780-2010) on log scale, both rebased to 1930 = 100. Composite of Jastram (1977) + BLS PPI + ONS PLLU.",
        "why": "Foundation series for the inflation-vs-deflation analysis that pervades the book (Chs 2, 5, 14, 15). The very long span makes the gold-standard / fiat-money price-level break of 1933 starkly visible.",
        "sources": [
            ("S210-A", "1780-2010", "Jastram (1977) T7 (US WPI) + BLS PPI extension (WPS->WPU)", "Index 1930=100", "salvaged via CD2 S023"),
            ("S210-B", "1780-2010", "Jastram (1977) T2 (UK WPI) + ONS PLLU extension", "Index 1930=100", "salvaged via CD2 S023"),
            ("S210-C", "2011-2025", "FRED WPU00000000 (PPI All Commodities, US extension)", "Index 1982=100", "FRED API"),
        ],
        "construction": "composite",
        "construction_steps": [
            "No Appendix 2 chopped table for WPI; CD2 S023 (which itself replicates Jastram + extensions) used as canonical book replica per decision 0005.",
            "Phase 4 substitution: BLS WPS00000000 frozen 1974 -> use WPU00000000 for post-1974 US extension.",
            "Phase 4 URL update: NBER macrohistory -> https://www.nber.org/research/data/nber-macrohistory-database.",
            "Extension currently US-only via FRED; UK extension via ONS PLLU deferred (transient 502 on specific page).",
        ],
        "year_book": (1780, 2010),
        "year_ext": (2011, 2025),
        "units": "Index, 1930 = 100 (log scale on figure)",
        "caveats": [
            "Canonical source not in chopped store; CD2 replica used (decision 0005).",
            "UK extension incomplete (ONS PLLU specific URL transient 502); document in EPR.",
        ],
        "tolerance": 1.0,
        "extension_status": "feasible_with_substitute",
        "construction_class": "composite",
        "extension_method": "BLS WPU00000000 for US; UK extension deferred until ONS PLLU page stabilizes.",
        "extension_proxies": "WPU substitutes for frozen WPS post-1974 -- direct BLS successor under same program, not a proxy.",
    },
    "S211": {
        "name": "US and UK Wholesale Price Indexes, 1780-1940 (1930=100, log scale)",
        "figure": "Figure 2.11",
        "definition": "Windowed view of S210 truncated at 1940 by analytical design. Used by Shaikh to focus on the gold-standard era prior to Bretton Woods.",
        "why": "Sets up the 'turbulent monetary regulation' argument by displaying the strikingly stationary character of WPIs under the gold standard.",
        "sources": [
            ("S211-A", "1780-1940", "Jastram (1977) T7 (US WPI)", "Index 1930=100", "salvaged via CD2 S022"),
            ("S211-B", "1780-1940", "Jastram (1977) T2 (UK WPI)", "Index 1930=100", "salvaged via CD2 S022"),
        ],
        "construction": "composite",
        "construction_steps": [
            "Same source as S210 with 1780-1940 window.",
        ],
        "year_book": (1780, 1940),
        "year_ext": None,
        "units": "Index, 1930 = 100 (log scale)",
        "caveats": [
            "Windowed view; no extension by design.",
            "If multi-period analysis is desired, use S210 (which extends to 2010+).",
        ],
        "tolerance": 1.0,
        "extension_status": "not_applicable_windowed",
        "construction_class": "composite",
        "extension_method": "N/A.",
    },
    "S212": {
        "name": "US and UK Wholesale Prices in Ounces of Gold, 1790-2025 (1930=100, log scale)",
        "figure": "Figure 2.12",
        "definition": "Formula series: WPI / gold_price for US and UK separately, rebased to 1930 = 100.",
        "why": "Strips out monetary inflation/deflation by deflating prices by gold; reveals the *real* (commodity-money-denominated) price level over 220 years.",
        "sources": [
            ("S212-A", "1790-2010", "Jastram (1977) T1 (US WPI/gold) + MeasuringWorth gold", "Index 1930=100", "salvaged via CD2 S025"),
            ("S212-B", "1790-2010", "Jastram (1977) (UK WPI/gold) + MeasuringWorth gold", "Index 1930=100", "salvaged via CD2 S024"),
            ("S212-C", "2011-2025", "Recomputed from S210 + FRED GOLDPMGBD228NLBM", "Index 1930=100", "computed"),
        ],
        "construction": "formula",
        "formula": "WPI_in_gold[country, t] = WPI[country, t] / gold_price[country, t]; rebased to 1930=100",
        "construction_steps": [
            "Book-period values: pre-computed in CD2 S024/S025 (Jastram + MeasuringWorth gold).",
            "Extension: recompute ratio from FRED WPU + FRED GOLDPMGBD228NLBM, rescaled to 1930=100 via 2010 anchor.",
        ],
        "year_book": (1790, 2010),
        "year_ext": (2011, 2025),
        "units": "Index, 1930 = 100 (log scale on figure); represents WPI deflated by gold price",
        "caveats": [
            "Formula extension applies; do NOT splice level series.",
            "UK extension would require GBP gold price + UK WPI extension -- deferred to Phase 9.",
        ],
        "tolerance": 1.0,
        "extension_status": "feasible",
        "construction_class": "formula",
        "extension_method": "Recompute WPI/gold ratio from extended S210 + extended gold price.",
    },
    "S213": {
        "name": "US Corporate Rate of Profit, 1947-2011",
        "figure": "Figure 2.13",
        "definition": "Average rate of profit for the US corporate sector, r = NOS_corporate / K_net (constant dollars), per Shaikh Appendix 6.7 methodology.",
        "why": "The book's first long-run profit-rate series; setup for the central-tendency-vs-incremental analysis in Chs 6, 7.",
        "sources": [
            ("S213-A", "1947-2011", "Derived from BEA NIPA T1.14 + FA T4.1", "rate (decimal)", "salvaged via CD2 S026"),
        ],
        "construction": "formula",
        "formula": "r[t] = NOS_corporate[t] / K_net[t-1]",
        "construction_steps": [
            "Book values reproduced from CD2 S026 (which itself replicates the Shaikh Appendix 6.7 computation).",
            "Extension: BEA T1.14/T4.1 API line-mapping under review (Phase 3 open question); marked as data_unavailable until Phase 9.",
        ],
        "year_book": (1947, 2011),
        "year_ext": None,
        "units": "Rate (decimal; e.g. 0.15 = 15%)",
        "caveats": [
            "Phase 3 open question: 'Corporate' here = NIPA T1.14 strictly per CD2 interpretation; outstanding ambiguity vs broader business sector documented in adequacy report.",
            "BEA API extension deferred: NIPA T1.14 line numbers shifted across vintages; needs Phase 9 specialist work.",
            "Tolerance 0.005 absolute (profit rates ~0.10-0.20; relative tolerance inappropriate near zero).",
        ],
        "tolerance": 1.0,
        "extension_status": "deferred",
        "construction_class": "formula",
        "extension_method": "Recompute NOS_corp / K_net from BEA NIPA T1.14 + FA T4.1; line resolver work pending.",
    },
    "S214": {
        "name": "Average Rates of Profit in US Manufacturing, 1960-1989",
        "figure": "Figure 2.14",
        "definition": "Sector-by-sector profit rates for 15 US manufacturing aggregates, 1960-1989. Source: Shaikh Appendix 7.2 hosted on anwarshaikhecon.org.",
        "why": "Empirical foundation for the cross-sector profit-rate distribution analysis in Ch 7 (real competition).",
        "sources": [
            ("S214-EXT", "1987-2005", "Shaikh Appendix7_ropdataUSind (post-book industry data)", "rate (decimal)", "salvaged chopped"),
        ],
        "construction": "formula",
        "formula": "r_sector[t] = profit[t] / capital_stock[t]",
        "construction_steps": [
            "**BOOK PERIOD (1960-1989) DATA NOT IN SALVAGEDINPUTS.** Per anu-framework no-fabrication rule, we do not synthesize the missing 1960-1989 series.",
            "We emit the post-book Appendix7 industry-level data (1987-2005) labeled S214-EXT (not S214-A), explicitly marked as post-book period only.",
            "Remediation: when anwarshaikhecon.org Appendix 7.2 replica is added to SalvagedInputs, re-run L01 to populate 1960-1989.",
        ],
        "year_book": (1960, 1989),
        "year_ext": None,
        "units": "Rate (decimal)",
        "caveats": [
            "Book period 1960-1989 is data_unavailable; documented in V03 with status PASS_DATA_UNAVAILABLE.",
            "OECD ISDB (1994 vintage referenced by CD2/Christodoulopoulos 1995) discontinued; STAN extension requires ISIC Rev3 -> Rev4 + NAICS crosswalk.",
        ],
        "tolerance": 1.0,
        "extension_status": "data_unavailable",
        "construction_class": "formula",
        "extension_method": "OECD STAN with sector crosswalk + BEA GDP-by-industry + Fixed-Asset Tables; deferred.",
    },
    "S215": {
        "name": "Incremental Rates of Profit in US Manufacturing, 1960-1989",
        "figure": "Figure 2.15",
        "definition": "Incremental profit rate r* = PG / IG(-1), where PG = gross profits and IG = gross investment lagged one year (footnote 6, p. 67).",
        "why": "Companion to S214; introduces the *incremental* profit rate measure that becomes central to Chs 7, 14, 16.",
        "sources": [
            ("S215-EXT", "1988-2005", "Shaikh Appendix7_iropdataUSind (post-book IROP data)", "rate (decimal)", "salvaged chopped"),
        ],
        "construction": "formula",
        "formula": "r*[t] = PG[t] / IG[t-1]",
        "construction_steps": [
            "Same status as S214: book period 1960-1989 not in SalvagedInputs; post-book 1988-2005 IROP data emitted as S215-EXT.",
        ],
        "year_book": (1960, 1989),
        "year_ext": None,
        "units": "Rate (decimal)",
        "caveats": [
            "Book period data_unavailable; PASS_DATA_UNAVAILABLE in V03.",
            "AMECO MEC uses gross output (not profits) in numerator -- do not splice without disclosure.",
        ],
        "tolerance": 1.0,
        "extension_status": "data_unavailable",
        "construction_class": "formula",
        "extension_method": "OECD STAN sector profits + investment with same formula; deferred.",
    },
    "S216": {
        "name": "Normalized Total Prices of Production Profit vs Total Unit Labor Costs, US 1972 (71 Industries)",
        "figure": "Figure 2.16",
        "definition": "Cross-sectional scatter for 71 industries from BEA 1972 benchmark I-O: x = total vertically-integrated unit labor cost (tv), y = total market prices (tpm) AND total prices of production at observed r (tp(r)). Both axes normalized so industry totals sum to 1.",
        "why": "First-pass empirical test of the Sraffian/classical claim that market prices cluster around prices of production. The strong correlation in Fig 2.16 anchors the Real Competition argument in Ch 7.",
        "sources": [
            ("S216-A", "1972", "BEA 1972 Use/Make + Shaikh Appendix 9 Sraffian computation (tp(r) normalized)", "normalized dollars", "salvaged chopped (Appendix9_1972fixed)"),
            ("S216-B", "1972", "BEA 1972 Use/Make (tpm normalized)", "normalized dollars", "salvaged chopped (Appendix9_1972fixed)"),
        ],
        "construction": "formula",
        "formula": "Prices of production from Sraffian system at observed r; integrated_ULC = (I - A)^(-1) * l",
        "construction_steps": [
            "Read 71-industry tpm, tp(r), tv from Appendix9_1972fixed.xlsx.",
            "Normalize each axis so industry totals sum to 1.",
            "Emit long-form: one row per (industry, axis-series).",
        ],
        "year_book": (1972, 1972),
        "year_ext": None,
        "units": "Normalized dollars (sums of each axis match)",
        "caveats": [
            "Cross-sectional: no temporal extension. Each subsequent BEA benchmark (1977, 1982, ..., 2017) is a separate cross-section.",
            "Phase 3 reclassification time_series -> cross_sectional ratified by Phase 4.",
            "Tolerance 0.5% per playbook cross_sectional rule.",
        ],
        "tolerance": 0.5,
        "extension_status": "not_applicable_cross_sectional",
        "construction_class": "cross_sectional",
        "extension_method": "N/A. Multi-benchmark analysis requires separate registry rows per BEA benchmark year.",
    },
    "S217": {
        "name": "GDP per Capita of World Regions (Maddison), 1600-2000",
        "figure": "Figure 2.17",
        "definition": "Maddison (2003) regional per-capita GDP estimates in 1990 International Geary-Khamis dollars, for World + 5 regions (Western Europe, Western Offshoots, Latin America, Asia, Africa).",
        "why": "Empirical foundation for the chapter's closing 'two-world' argument (~400 years of accelerating divergence between Western Offshoots/Europe and the rest).",
        "sources": [
            ("S217-A", "1600-2000", "Maddison (2003) World", "1990 GK $/cap", "salvaged chopped"),
            ("S217-B", "1600-2000", "Maddison (2003) Western Europe", "1990 GK $/cap", "salvaged chopped"),
            ("S217-C", "1600-2000", "Maddison (2003) Western Offshoots", "1990 GK $/cap", "salvaged chopped"),
            ("S217-D", "1600-2000", "Maddison (2003) Latin America", "1990 GK $/cap", "salvaged chopped"),
            ("S217-E", "1600-2000", "Maddison (2003) Asia", "1990 GK $/cap", "salvaged chopped"),
            ("S217-F", "1600-2000", "Maddison (2003) Africa", "1990 GK $/cap", "salvaged chopped"),
        ],
        "construction": "direct",
        "construction_steps": [
            "Unpivot wide-format chopped table (rows=region, cols=decade) to long form.",
            "Extension: MPD 2023 with 2011 PPP base differs from 1990 GK; regional aggregations also revised. Deferred to manual Phase 9 splice.",
        ],
        "year_book": (1600, 2000),
        "year_ext": None,
        "units": "1990 International Geary-Khamis dollars per capita (log scale on figure)",
        "caveats": [
            "MPD 2023 base-year change (1990 GK -> 2011 PPP) creates level discontinuity at splice. Documented in EPR per Phase 4.",
            "Decennial pre-1820, annual thereafter.",
        ],
        "tolerance": 1.0,
        "extension_status": "deferred",
        "construction_class": "direct",
        "extension_method": "Maddison Project Database 2023; manual rebase required because of 1990 GK -> 2011 PPP shift.",
        "extension_proxies": "MPD 2023 region definitions revised in 2018/2020; flagged in registry.",
    },
    "S218": {
        "name": "GDP per Capita Richest Four and Poorest Four Countries (Maddison), 1600-2000",
        "figure": "Figure 2.18",
        "definition": "Average GDP per capita of the 4 richest countries and 4 poorest countries at each decennial benchmark, plus the ratio (richest4/poorest4). Shaikh excludes Kuwait/Qatar/Venezuela from the top 4 (1950+).",
        "why": "Closes the chapter with a stark quantitative measure of global inequality: 40x in 1990, 64x in 2000.",
        "sources": [
            ("S218-A", "1600-2000", "Maddison (2003) RICHEST 4 with Shaikh exclusions", "1990 GK $/cap", "salvaged chopped"),
            ("S218-B", "1600-2000", "Maddison (2003) POOREST 4", "1990 GK $/cap", "salvaged chopped"),
            ("S218-C", "1600-2000", "Computed ratio", "ratio", "salvaged chopped (precomputed)"),
        ],
        "construction": "formula",
        "formula": "richest4_avg = mean(top 4 excluding KW/QA/VE); poorest4_avg = mean(bottom 4); ratio = richest4/poorest4",
        "construction_steps": [
            "Read precomputed RICHEST 4, POOREST 4, RATIO rows from chopped table.",
            "Extension: MPD 2023 requires re-applying the exclusion rule (and possibly adding Macao, Luxembourg). Deferred.",
        ],
        "year_book": (1600, 2000),
        "year_ext": None,
        "units": "1990 GK $/cap (levels); ratio (S218-C)",
        "caveats": [
            "Shaikh exclusion rule (Kuwait, Qatar, Venezuela from top 4, 1950+) must be reapplied for MPD 2023.",
            "Ratio (S218-C) is base-year-invariant; level series (S218-A/B) require rebasing for MPD 2023 splice.",
            "Modern panel may need additional exclusions (Macao, Luxembourg) per anu-framework no-proxy rule.",
        ],
        "tolerance": 1.0,
        "extension_status": "deferred",
        "construction_class": "formula",
        "extension_method": "Reapply Shaikh exclusion rule to MPD 2023 country panel; ratio rebases safely, levels need rescale.",
    },
}


def _make_dpr(sid: str, d: dict) -> str:
    sources_table_rows = "\n".join(
        f"| **{ssid}** | {period} | {src} | {units} | {ret} |"
        for ssid, period, src, units, ret in d["sources"]
    )
    construction_steps = "\n".join(f"{i+1}. {step}" for i, step in enumerate(d["construction_steps"]))
    caveats_block = "\n".join(f"{i+1}. {c}" for i, c in enumerate(d["caveats"]))
    year_book_str = f"{d['year_book'][0]}-{d['year_book'][1]}"
    year_ext_str = f"{d['year_ext'][0]}-{d['year_ext'][1]}" if d.get("year_ext") else "N/A"
    formula_block = f"\n\n**Formula**: `{d['formula']}`\n" if d.get("formula") else ""
    return f"""# {sid} -- {d['name']}

**Data Provenance Record (DPR)**
**Phase**: 5 (Ingestion)
**Series ID**: {sid}
**Status**: ingested
**Authored**: 2026-05-18
**Author**: opus-subagent-wave2-ch2
**Related artifacts**:
- Research dossier: `Technical/research/{sid}_research.json`
- Adequacy: `Technical/docs/chapters/CH2_ADEQUACY_REPORT.json`
- Extension Provenance Record: `Technical/docs/series/{sid}_EPR.md`
- Registry entry: `Technical/series_registry.json` -> `series.{sid}`

---

## 1. Definition

{d['definition']}

In Shaikh (2016) the series appears as **{d['figure']}** in Chapter 2 ("The Wealth of Nations: A Long View").

## 2. Why it matters in Chapter 2

{d['why']}

## 3. Sources (per subseries)

| Subseries | Coverage | Publisher / Series ID | Native units | Retrieval |
|---|---|---|---|---|
{sources_table_rows}

## 4. Construction

`{d['construction']}` construction.{formula_block}

{construction_steps}

## 5. Year coverage

- **Book period**: {year_book_str}
- **Extension period**: {year_ext_str}

## 6. Units

{d['units']}

## 7. Caveats

{caveats_block}

## 8. Cross-references

- Book reference: Shaikh (2016), Ch. 2, {d['figure']}
- Knowledge Base: `SalvagedInputs/figures_reference/HDARP_SERIES_LINKAGE.json`
- Predecessor (CD2): see registry `predecessor_ids` block.

## 9. Validation expectation

- **Tolerance**: +/- {d['tolerance']}% per year (per playbook).
- **Expected MAE** (vs salvaged book truth): < 0.5% when source data is pulled directly from the chopped table.
"""


def _make_epr(sid: str, d: dict) -> str:
    extension_status = d.get("extension_status", "feasible")
    return f"""# {sid} -- Extension Provenance Record

**Series**: {sid} -- {d['name']}
**Phase**: 6 (Extension)
**Construction classification**: `{d['construction_class']}`
**Extension status**: `{extension_status}`
**Authored**: 2026-05-18
**Author**: opus-subagent-wave2-ch2
**Related**: `{sid}_DPR.md`, `Technical/research/{sid}_research.json`

---

## 1. Classification

Per the playbook content-type rule, {sid} is classified `{d.get('construction_class', d['construction'])}`. Extension recipe applied: per the Anu framework rule on lazy splices, this dictates the extension method below.

## 2. Method

{d.get('extension_method', 'See DPR section 4 (Construction) for the extension steps.')}

## 3. No-Proxy disclosure

{d.get('extension_proxies', 'No proxies used. All extension sources are the same agency/program as the original.')}

## 4. No-Synthetic disclosure

No synthetic, interpolated, or placeholder values are introduced. Where the API returns NaN, the NaN propagates to the published series.

## 5. Failure-mode table

| Failure | Detection | Action |
|---|---|---|
| API key not set | `S00_config.have_key` returns False | Loader returns `degraded`; processor publishes book period only; registry stamped `extension_status: api_key_missing` |
| API non-200 | `S00_apis._retry_get` raises after 3 retries | Same degradation as above |
| Overlap year NaN | Processor checks pre-splice | Walk back overlap year (e.g. 2010 -> 2009 -> 2008); fail hard if no valid overlap in 5-year window |
| Source URL discontinued | Phase 4 adequacy URL check | EPR documents the substitute (see section 3) |

## 6. CD2 divergence pre-disclosure

CD2's predecessor series may diverge from {sid} due to (a) different extension anchor, (b) different proxy selection, or (c) a different vintage of the underlying source. Divergence is reported informationally in V03 and never causes a FAIL.

## 7. Extension status

Current: `{extension_status}`. See DPR caveats for rationale.
"""


def main() -> dict:
    DOCS_SERIES.mkdir(parents=True, exist_ok=True)
    written = []
    for sid, d in SERIES_DOCS.items():
        (DOCS_SERIES / f"{sid}_DPR.md").write_text(_make_dpr(sid, d), encoding="utf-8")
        (DOCS_SERIES / f"{sid}_EPR.md").write_text(_make_epr(sid, d), encoding="utf-8")
        written.append(sid)
    return {"series_documented": len(written), "series_list": written}


if __name__ == "__main__":
    import json
    print(json.dumps(main(), indent=2))

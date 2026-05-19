# S707 / S708 underlying data — UNAVAILABLE without chart digitization

**Series affected**
- S707 = Capitalism (2016) Figure 7.19 — Greek manufacturing **average** ROP
  deviations, 20 industries, 1962-1991
- S708 = Capitalism (2016) Figure 7.20 — Greek manufacturing **incremental**
  ROP deviations, 20 industries, 1962-1991

**Source of both figures** (per book Appendix 7.1 IV, p. 859 / PDF p. 897):
> Tsoulfidis, L. and Tsaliki, P. (2011), "Classical Competition and
> Regulating Capital: Theory and Empirical Evidence."
> MPRA Paper No. 51334.

**Canonical URL**
- Abstract: https://mpra.ub.uni-muenchen.de/51334/
- Direct PDF: https://mpra.ub.uni-muenchen.de/51334/1/MPRA_paper_51330.pdf
  (NOTE: the dossier stubs S707 and S708 listed the WRONG MPRA URL
  `mpra.ub.uni-muenchen.de/35908/`, which resolves to an unrelated paper.
  The correct identifier is 51334. This README documents the correction.)

**Local cache**
- `D:/Arcanum/Projects/RSCD/_tmp_tsoulfidis2011.pdf` (downloaded
  2026-05-18; 928 162 bytes; 42 pages).

---

## What the source PDF actually contains

The full text of Tsoulfidis & Tsaliki (2011) was extracted with PyMuPDF
and inspected. The paper contains exactly five tables (`Table 1` through
`Table 5`). None of them is a year-by-year industry-level deviation
panel. Specifically:

| Table | Page | Content |
|-------|------|---------|
| 1 | ~p.12 | Summary statistics of concentration indexes (CR4, HHI), cross-section, 1958/1969/1984/1988 |
| 2 | ~p.15 | Pearson and Spearman correlation coefficients (concentration vs profitability), cross-section |
| 3 | ~p.21 | KSS non-linear unit-root test statistics by industry (single value per industry) |
| 4 | p.25 | AR(1) regression coefficients (a, b, a/(1-b), R^2) for deviation series of 20 industries, 1959-1991. **NOT the year-by-year deviation values** — only the four estimated parameters per industry. |
| 5 | p.37 | AR(1) regression coefficients for Baxter-King-filtered IROP deviations of 20 industries, 1962-1992. **Same form as Table 4 — parametric summaries only.** |

The underlying 20-industry x 30-year deviation **time series** (which is
what Tsoulfidis & Tsaliki's Figures 4 and 5 plot, and which Shaikh
reproduces as his Figures 7.19 and 7.20) is **NOT tabulated** in the
2011 MPRA paper. It exists in the paper only as line charts.

## Why this is `data_unavailable` not `extracted`

Per project constraint:
> No fabricated values. Verbatim extraction from tables if found. If only
> charts exist, mark `data_unavailable` (Phase 6 may use WebPlotDigitizer
> manually; LLM agents cannot reliably digitize charts).

The deviation values can in principle be recovered from the chart panels
on pp. 19 (Fig. 4) and 30 (Fig. 5) of the MPRA PDF, but only via manual
chart digitization (WebPlotDigitizer or equivalent). That task is out of
scope for an LLM agent and is deferred to Phase 6.

## What CAN be reproduced today from the available source

The qualitative findings and the AR(1) regression coefficients in Table
4 (for S707 / Fig 7.19) and Table 5 (for S708 / Fig 7.20). These are
sufficient to reproduce Shaikh's textual claims (pp. 305-306 of
Capitalism) about the long-run gravitation behavior of the deviation
series, but are NOT sufficient to redraw Figures 7.19 and 7.20.

## Recommendation for Phase 5 plotting

Two viable paths:

1. **Reproduce the figures from the chapter PDF / book scan directly**
   (treat as image inclusion, no underlying data needed). This is the
   pragmatic option for an LLM-driven build because no digitization is
   required.

2. **Queue for Phase 6 manual digitization.** WebPlotDigitizer on Tsoulfidis
   & Tsaliki (2011) Figures 4 (p. 19) and 5 (p. 30) would yield the
   20-industry x 30-year panel. If this is done, the resulting CSV should
   be staged here as `Tsoulfidis_Tsaliki_2011_Greek_deviations.csv` with
   an additional README block documenting the digitization tool, operator,
   and date.

## Author contact (optional human path)

The original Greek industry-level data was processed by Lefteris
Tsoulfidis (University of Macedonia, Thessaloniki) and Persefoni Tsaliki
(Aristotle University of Thessaloniki). A direct email request to the
authors for the underlying panel may succeed where MPRA does not.

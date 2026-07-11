# S801 — Extension Provenance Record

**Series**: S801 — Wholesale Prices in Oligopolistic and Competitive Industries, 1965-1973 (Eichner Fig 8.1)

**Construction classification**: `direct` (digitized reproduction of Shaikh's Figure 8.1)
**Extension method**: not applicable — a modern reconstruction would be a proxy, see §2
**Authored**: 2026-05-18 · **Recovery update**: 2026-05-26
**Author**: Anu automated extraction pipeline
**Related**: `S801_DPR.md`

---

> **Recovery (2026-05-26):** This record was originally authored when S801 was `data_unavailable`.
> S801 was subsequently **recovered by figure digitization**: an offline native-vector trace of Shaikh's
> Figure 8.1 (which reproduces Eichner 1973, p. 1187) from the book PDF, overlay-validated against the
> figure. The series now carries two index lines (Oligopolistic, Competitive), 1965-1973, base 1957-59 = 100,
> with `provenance: digitized` (digitization fidelity, not Eichner's exact unpublished table). Round-trip
> validation PASS (n=18, MAE 0.0). The sections below have been rewritten to the recovered state; the earlier
> `data_unavailable` framing was superseded by the recovery.

## 1. Classification

`content_type = time_series` (two annual index lines, 1965-1973), `construction = direct`. The book-period
data now exists as a digitized reproduction of Shaikh's Figure 8.1 and is byte-stable against its recovered
source workbook. There is, however, no faithful modern **extension** — see §2.

## 2. Why no extension is attempted

- Eichner (1973, p. 1187) published Figure 8.1 as a **chart only**; there is no underlying table, and the
  specific set of industries in Eichner's 1965-1973 "concentrated" and "competitive" aggregates is not
  recoverable from the published article.
- The closest modern source (US producer-price indices by industry, partitioned by Census concentration
  ratios) uses incompatible industry classifications (1965-1973 SIC codes vs. post-1997 NAICS) and would
  require re-selecting an industry set to mirror Eichner's — which is itself unrecoverable.
- Any modern continuation would therefore be a **proxy reconstruction**, not a faithful extension of the
  original figure. Under the no-proxy and no-synthetic rules this is not undertaken; it would be a new
  series requiring an explicit concept-match justification and human review.

## 3. Method

The book-period values are a digitized reproduction (native-vector figure trace, overlay-validated). No
extension method is applied.

## 4. No-Proxy disclosure

**No proxy used.** A modern producer-price reconstruction is *not* a proxy for Eichner's chart — it would be
a re-construction requiring (a) a SIC-to-NAICS concordance, (b) re-application of concentration thresholds,
and (c) selection of an industry set mirroring Eichner's (itself unrecoverable). Such a reconstruction would
not meet the no-proxy bar without explicit human review.

## 5. No-Synthetic disclosure

**None.** The book-period values are recovered by figure digitization (overlay-validated), not interpolated,
extrapolated, or synthetically generated. Digitization fidelity is flagged with `provenance: digitized`.

## 6. Failure-mode table

| Failure | Action |
|---|---|
| Loader cannot find recovered source workbook | Returns `{"status": "FAIL", "reason": "source_missing"}` |
| Round-trip divergence against recovered workbook | FAIL — investigate the digitized workbook vs. the figure trace |
| Extension requested | Not applicable — a modern reconstruction would be a proxy (see §2) |

## 7. Predecessor divergence pre-disclosure

No genuine predecessor per-series dataset matches this exhibit's content. The stub's earlier `S042` link was a
stale carryover from a Chapter 10 interest-rate series and has been nulled. A predecessor comparison is not
meaningful here.

## 8. Recovery record and future work

1. **Recovered (2026-05-26)**: native-vector trace of Shaikh's Figure 8.1 from the book PDF, overlay-validated,
   `provenance: digitized`. This is the current state of the series.
2. **Author's underlying spreadsheet** (out of scope): Alfred Eichner died in 1988; archived working papers may
   contain the original values, but these are not accessible to this project.
3. **Modern producer-price reconstruction** (out of scope): would be a NEW series classified as a proxy
   substitution, requiring a formal concept-match justification and human review — not an extension of S801.

# XS2305 — Extension Provenance Record

**Series**: XS2305 — RMB Misalignment, Macro-Balance Approach (Literature Compilation)
**Phase**: 6 (Extension)
**Construction**: `composite` (literature compilation)
**Extension status**: `not_applicable_literature_compilation`
**Authored**: 2026-05-18

Identical reasoning as XS2304_EPR (same 4 cited reviews, same
non-extensibility rationale).

## v1.0 scope

Two named endpoint estimates only:
- +40% Goldstein 2004 (via Cline-Williamson 2007 review)
- -100% Bayoumi-Gagnon-Saborowski 2015 (via Cheung 2012 review)

Full scatter reconstruction (~30-35 points) deferred to v1.1.

## Methodology distinction from XS2304

Both XS2304 and XS2305 sample from the same 4 reviews. The split is
on the underlying estimate's equilibrium-RER methodology:
- XS2304 = extended PPP / BEER
- XS2305 = macroeconomic balance / current-account norm (Williamson 1994)

Each of the 4 reviews covers BOTH methodologies. Phase 5 v1.1
literature extraction must apply the methodology label correctly per
estimate.

## Conceptual continuity vs adjacent concepts

The data object `RMB misalignment estimates compiled from 4 literature
reviews, filtered to macroeconomic-balance methodology` measures
`equilibrium real-exchange-rate deviation under current-account-norm
calibration (Williamson 1994 family)` rather than `extended-PPP /
BEER` or `IMF EBA estimates` because:
- Source agency choice: identical to XS2304 — the same four literature
  reviews fixed by paper note 17. No additional sources.
- Methodology continuity: the methodology filter restricts to
  macroeconomic-balance estimates *within* the same 4 reviews; the
  underlying calibration approach (CA-norm + RER elasticities) is
  preserved across all sampled estimates.
- Disambiguation: macroeconomic-balance (XS2305) is methodologically
  distinct from extended-PPP (XS2304) even when both are sampled from
  the same 4 reviews; MB vs BEER differ in what they treat as the
  equilibrium anchor (CA norm vs estimated fundamentals regression);
  MB ≠ raw current-account divergence (which is the input, not the
  output).

The book's original concept (Weber & Shaikh 2020 Section 4.4, p. 443)
was: even the MB approach — "directly related to the current account
balance and hence the methodology of choice for proponents of the
currency-manipulation hypothesis" — produces estimates ranging from
-100% to +40%, undermining the manipulation argument on its own terms.
The modern series preserves the 4-review compilation rule and the
MB methodology filter while permitting v1.0 truncation to two
paper-text-named endpoints (+40% Goldstein 2004; -100%
Bayoumi-Gagnon-Saborowski 2015). This is NOT a proxy substitution
forbidden by the No-Proxy rule because the underlying estimates are
verbatim from their cited working papers; the series is intrinsically
non-extensible past 2012 (`extension_status:
not_applicable_literature_compilation`).

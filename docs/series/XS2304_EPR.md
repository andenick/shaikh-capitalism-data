# XS2304 — Extension Provenance Record

**Series**: XS2304 — RMB Misalignment, Extended PPP Approach (Literature Compilation)
**Phase**: 6 (Extension)
**Construction**: `composite` (literature compilation)
**Extension status**: `not_applicable_literature_compilation`
**Authored**: 2026-05-18

## 1. Why this series is NOT extendable

Per paper note 17, Fig 4 is a compilation of estimates from 4
literature reviews dated 2005, 2007, 2010, 2012. The RMB-misalignment
debate cooled substantially after 2014 as China shifted to a managed-
float regime. Since 2015, the IMF External Sector Report has
generally found RMB "broadly in line with fundamentals", using the
EBA (External Balance Assessment) model.

Extending Fig 4 to post-2012 requires *either*:
- New academic literature reviews of equivalent scope (none produced
  under the same compilation rule as paper note 17); or
- Substitution with IMF EBA model output, which is methodologically
  distinct — a different empirical object, not a continuation.

We therefore flag `extension_status: not_applicable_literature_compilation`
per the playbook's content-type recipe for compilation series.

## 2. Compilation methodology (paper note 17 verbatim, p. 448)

> "Figure 4 and Figure 5 are compiled based on the selection of studies
> contained in the four literature reviews ... If a source reported
> more than one estimate of the RMB misalignment, each estimate was
> treated as a separate data point in the scatter plots. If the estimate
> of the RMB misalignment is reported as a range, the maximum and minimum
> value are reported in the scatter plots as two separate estimates."

## 3. v1.0 scope

The chopped CSV captures the two named endpoint estimates that Weber
& Shaikh quote in body text:
- +50% Coudert-Couharde 2007 (via Cline-Williamson 2007 review)
- -36% Cheung 2012

The remaining ~30-35 unnamed scatter points are deferred to v1.1
literature extraction.

## 4. Proxies

None. Each individual estimate is published verbatim in its source
literature review.

## 5. Synthetic data

None permitted. v1.0 chart-digitization of unnamed scatter points is
explicitly excluded per Anu Framework no-fabrication rule.

## 6. Conceptual continuity vs adjacent concepts

The data object `RMB misalignment estimates compiled from 4 literature
reviews, filtered to extended-PPP methodology` measures `equilibrium
real-exchange-rate deviation under BEER-style reduced-form regressions`
rather than `IMF EBA model output` or `simple PPP-deviation` because:
- Source agency choice: paper note 17 explicitly names Cline & Williamson
  2007 (PIIE), Dunaway-Li 2005 (IMF WP), Cheung-Chinn-Fujii 2010a (La
  Follette WP), Cheung 2012 (CESifo WP). No other reviews are
  substituted — even if they would expand coverage, the paper's
  compilation rule restricts to these four.
- Methodology continuity: each cited estimate already used the BEER-style
  extended-PPP methodology when published 1999-2010. The compilation
  preserves both the originating-estimate methodology label and the
  paper's filter to extended-PPP studies only.
- Disambiguation: extended-PPP (XS2304) ≠ macroeconomic-balance (XS2305)
  even when sampled from the same 4 reviews; extended-PPP regression on
  fundamentals ≠ raw PPP deviation; the IMF EBA model (post-2014) is
  methodologically a *different empirical object*, not a continuation.

The book's original concept (Weber & Shaikh 2020 note 17, p. 448, verbatim)
was: "Figure 4 and Figure 5 are compiled based on the selection of
studies contained in the four literature reviews ... If a source reported
more than one estimate of the RMB misalignment, each estimate was treated
as a separate data point in the scatter plots." The modern series
preserves the 4-review compilation rule and the methodology filter while
permitting the v1.0 truncation to two paper-text-named endpoints (+50%
Coudert-Couharde 2007; -36% Cheung 2012). This is NOT a proxy
substitution forbidden by the No-Proxy rule because the underlying
estimates are verbatim from their cited working papers; v1.1 literature
extraction will populate the remaining ~30-35 scatter points from the
same 4 sources. The series is intrinsically non-extensible past 2012
because the paper's compilation universe is fixed (`extension_status:
not_applicable_literature_compilation`).

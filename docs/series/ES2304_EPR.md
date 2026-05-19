# ES2304 — Extension Provenance Record

**Series**: ES2304 — RMB Misalignment, Extended PPP Approach (Literature Compilation)
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

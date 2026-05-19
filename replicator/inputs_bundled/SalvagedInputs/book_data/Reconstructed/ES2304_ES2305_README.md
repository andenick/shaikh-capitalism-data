# ES2304 / ES2305 Literature-Compilation Data

Source: Weber & Shaikh (2020), "The U.S.-China trade imbalance and the
theory of free trade", Figures 4 and 5 (Appendix pp. 454-455).

## Figures

- **Figure 4** — Estimates of RMB misalignment based on extended PPP approach
  (scatter, 1999-2010, ~35-40 individual estimates)
- **Figure 5** — Estimates of RMB misalignment based on macroeconomic balance
  approach (scatter, 1999-2012, ~30-35 individual estimates)

## Compilation rule (paper note 17, p. 448, verbatim)

> "Figure 4 and Figure 5 are compiled based on the selection of studies
> contained in the four literature reviews (Cline and Williamson 2007;
> Dunaway and Li 2005; Cheung, Chinn, and Fujii 2010a; Cheung 2012). If
> a source reported more than one estimate of the RMB misalignment, each
> estimate was treated as a separate data point in the scatter plots.
> If the estimate of the RMB misalignment is reported as a range, the
> maximum and minimum value are reported in the scatter plots as two
> separate estimates."

## Files

- `ES2304_literature_compilation.csv` — extended PPP estimates (Fig 4)
- `ES2305_literature_compilation.csv` — macroeconomic balance estimates (Fig 5)

## Scope of this verbatim extraction

Each CSV captures the **named endpoint estimates** that Weber & Shaikh
quote in body text — that is, only the high/low estimates that the
paper itself reports by name with both value and citing source. These
are:

- Fig 4 (ES2304): high = +50% (Coudert and Couharde 2007, via
  Cline-Williamson 2007 review); low = -36% (Cheung 2012)
- Fig 5 (ES2305): high = +40% (Goldstein 2004, via Cline-Williamson 2007
  review); low = -100% (Bayoumi, Gagnon, Saborowski 2015, via Cheung
  2012 review)

The remaining ~30-35 scatter points per figure are **not** verbatim
tabulated by the paper — they are only plotted as scatter dots on the
appendix charts. Per Anu Framework no-fabrication rule and the playbook
anti-pattern list, we do not chart-digitize the individual unnamed
points. Full reconstruction of the scatter requires re-extracting each
estimate from the 4 cited literature reviews and the original primary
papers they cite, following paper note 17's compilation rule exactly.

This is documented in `ES2304_EPR.md` and `ES2305_EPR.md` under the
`compilation_methodology` block, with a v1.1 plan to commission a
literature-extraction subagent to populate the full ~70-point dataset
via direct PDF reads of the 4 cited reviews.

## Provenance

- `paper_text_anchor` column points to the exact page in the published
  PDF (`[2020] Weber & Shaikh - The U.S.-China trade imbalance...pdf`)
  where the named endpoint estimate is stated by Weber and Shaikh.
- All 4 cited literature reviews are publicly available (URLs verified
  HEAD 200/202 OK 2026-05-18 in the Phase 4 adequacy report).
- `extension_status: not_applicable_literature_compilation` — the 4
  cited reviews are 2005-2012 snapshots and the RMB-misalignment
  debate moved to IMF EBA model post-2014 (methodologically distinct).

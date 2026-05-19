# ES2101 Reconstructed Summary Statistics

Source: Shaikh, Coronado, Nassif-Pires (2020), "On the empirical
regularities of Sraffa prices", EJEEP 17(2): 265-275.

## File

- `ES2101_summary_statistics.csv` — verbatim summary statistics quoted
  in the paper's Section 5 conclusions (p. 272).

The paper's primary empirical objects are Figures 6 (Average CI by
matrix size, scatter, 2002 + 2007) and Figure 7 (Theil indexes for
2002 and 2007, scatter). These are NOT tabulated in the paper; the
underlying ~295 (matrix-size, average-CI) and ~295 (matrix-size,
Theil) points are visible only as scatter plots.

Per Anu Framework no-fabrication rule and the playbook anti-pattern
list, we do not chart-digitize the scatter points. Instead we
capture the **named summary statistics** that the paper's text quotes
verbatim:

- Average CI range across all aggregation levels: 0.03 to 0.06 (both
  2002 and 2007)
- 425 sectors plotted in 2002 (largest matrix); 387 in 2007
- 26 of 425 (6.1%) 2002 prices switch sides of their labor value
- 4 of 425 (0.9%) 2002 prices switch on the Bienenfeld line
- None of those 4 with deviation greater than 1%

## Full distribution reconstruction (v1.1)

The full CI/Theil scatter requires building the BEA-to-Sraffa pipeline
shared with ES2001 (regenerate A matrices at 295 aggregation levels,
compute Sraffa prices and Bienenfeld linear at each, integrate
arc-length for CI). Deferred to v1.1 per CHES adequacy recommendation.

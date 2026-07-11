# S704 1990 open-item ruling (M3 STEP 0, 2026-07-02)

**Question (from the M3 verifier's completeness flag):** Fig 7.14 carries a 31st annual
data column at x≈1299 (=1990). Should a 1990 USMANAVG point be appended to the consensus?

**Method:** Re-cropped the 1990 column region of `images/S704_fig7.14_avg_panel.png` at
4×/8×/16× zoom (`machine/S704_1990_probe_zoom.png`, `_terminus_ticks.png`, `_col_16x.png`),
VIEWED each, and ran an objective per-column stroke-width scan (OpenCV distance-transform
half-width, mirroring the M2 boldness criterion) at 1987, 1988, 1989, 1990, using the
verifier's data-anchored calibration (x: col#1=1960 at x140, step 38.65 px/yr → 1990 at
x1300; y: pct = −0.11017·y + 65.148).

**Findings:**
1. **The 1990 column is real.** Multiple *marked* series plot a 1990 point (a gray
   filled-circle ~16.6%, an X-marker ~14.9%, and a filled-triangle/open-tent compound
   marker spanning ~11.9–13.9%). The figure does run to 1990, confirming the verifier.
2. **No resolvable markerless USMANAVG vertex at 1990.** At 1987–1989 the USMANAVG bold
   line is a single clearly-dominant *markerless* run (DT half-width 6.4–7.0 at 13.6–14.6%).
   At 1990 that dominance collapses: the max black-stroke DT falls to 5.0 and splits across
   two runs (13.9% y465 and 11.9% y483) that both coincide with the vertical extent of the
   filled-triangle marker. The 16× crop shows the bold strokes arriving from 1989 converging
   INTO the triangle/tent + circle markers, with no clean markerless stroke passing through.

**Ruling: OMIT 1990.** Attributing a markerless USMANAVG value at the 1990 column would
require guessing which converging stroke is USMANAVG at a knot dominated by a triangle
marker — precisely the borrow/guess forbidden by plan §1.3 ("no value interpolated or
guessed; gaps stay gaps") and §7 ("never force"). This is the direct analogue of the
consensus's own S703-1974 omission (a value arguably present but marker-identity ambiguous,
so omit rather than guess). The packet instructions and the consensus already treat 1989 as
the cutoff; this ruling confirms it on independent targeted measurement.

**Consequence:** No `S704_consensus_v2.csv` is created. The original `S704_consensus.csv`
(30 points, 1960–1989) is the durable ingest source. S704 published coverage = 30/30 of the
resolvable USMANAVG columns; the 1990 column is disclosed as omitted-because-marker-occluded.

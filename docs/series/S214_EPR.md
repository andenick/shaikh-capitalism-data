# S214 -- Extension Provenance Record

**Series**: S214 -- Average Rates of Profit in US Manufacturing (post-book, 1987-2005)

**Construction classification**: `formula`
**Extension status**: `shipped` (Shaikh Appendix-7 companion data; NOT a live-API extension)
**Validation class**: `extension_only` (book period 1960-1989 genuinely `data_unavailable`)
**Authored**: 2026-05-18
**Rewritten**: 2026-07-10 (P1.1 remediation, campaign v1.6) to describe what actually ships
**Related**: `S214_DPR.md`, research dossier

---

## 1. What this series actually is

S214 ships a single subseries, `S214-EXT` (`role: post_book_only`), covering **1987-2005**.
It is the **mean across 12 US manufacturing industries** of the average rate of profit, taken
directly from Shaikh's own Appendix-7 companion workbook
book appendix source table. This is Shaikh's
own author data, not a modern reconstruction and not a live-API extension.

The **book period 1960-1989** (Fig 2.12 / Fig 2.14 panel) is genuinely `data_unavailable`:
the original inputs (anwarshaikhecon.org Appendix 7.2 + OECD ISDB 1994 vintage) are not in
`SalvagedInputs/`. Per the no-fabrication rule, no book-period values are synthesized. Because
no book-window observation was ever validated against book truth, the registry status is
`validated:extension_only` (NOT `book_period_validated`) and `validation_class: extension_only`.

## 2. Method (as shipped)

`L01_S214.py` reads the Appendix-7 workbook and averages the 12 manufacturing-industry columns:
**Chemicals, Electr.Equ., Fab.Metal., Food, Mach., Paper, Petroleum, Plastic, Prim.Metal.,
Printing, Text.Mills, Wood** (workbook header spellings). `P02_S214.py` is a pass-through;
`O06` writes the chopped CSV and extenbook. `splice_method = not_applicable_book_data_unavailable`
because there is no book segment to splice with.

**Motor Vehicles is genuinely absent** from this Appendix-7 panel, so the recoverable
manufacturing set is 12 industries (not the 13 an earlier draft named).

## 3. The 2026-07-10 correction (F-4C-02 CRITICAL)

Before this fix, the loader used a hard-coded industry list whose spellings did not match the
workbook headers. The `have = [c for c in MFG_INDUSTRIES if c in df.columns]` intersection
silently kept only **6 of 12** columns (Chemicals, Electr.Equ., Fab.Metal., Food, Paper, Wood)
and dropped the other 6 real manufacturing industries (Machinery, Petroleum, Plastics, Primary
Metals, Printing, Textiles) because they are spelled differently in the file. The shipped series
was therefore a **6-of-12-industry mean**, ~20-42% off the correct manufacturing average every
year. The loader now uses an explicit normalization mapping with a hard
`assert len(matched) == 12` guard, so any future header drift FAILS the run loudly instead of
silently shrinking the average. See internal review record
(Adversarial verification / VERIFY_4C).

## 4. No-Proxy / No-Synthetic disclosure

No proxies. No synthetic, interpolated, or placeholder values. The 12-industry mean is a faithful
replication of Shaikh's Appendix-7 companion data. The book period is left empty (not filled).

## 5. Independent validation

`validation.independent_anchors` carries three hand-recomputed 12-industry means (1990, 1996,
2002) taken directly from the raw workbook, independent of the loader path. They were proven RED
against the pre-fix (6-column) data and GREEN against the corrected output (evidence:
internal remediation record). `validation.reference_values` are
regression guards only (they round-trip against the corrected chopped) — not an independent check.

## 6. Deferred future extension (NOT shipped)

A modern extension via **OECD STAN** (ISIC Rev3 -> Rev4 + NAICS crosswalk) + BEA GDP-by-industry
+ Fixed-Asset Tables remains a **deferred, unbuilt** long-term target (scope decision required;
OECD ISDB 1994 vintage discontinued). Nothing from OECD STAN currently ships in S214.

## 7. Failure-mode table

| Failure | Detection | Action |
|---|---|---|
| Appendix-7 workbook missing | `CHOPPED.exists()` False in L01 | Loader returns `FAIL`; no data shipped |
| Manufacturing header drift | `assert len(matched) == 12` in L01 | Run FAILS loudly (never a silent partial average) — this is the F-4C-02 guard |
| Book period requested | book_period_status = `data_unavailable` | No synthesis; 1960-1989 stays empty until the source is recovered to SalvagedInputs |

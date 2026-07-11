# S703 — Extension Provenance Record

**Series**: S703 — Figure 7.13 — World Manufacturing WORLDAVG Rate of Profit, 1970–1990 (Christodoulopoulos/ISDB)

**Construction classification**: `machine_digitized` (book-period only)
**Extension method**: not applicable — see §2
**extension_status**: `discontinued`
**Authored**: 2026-05-18 · **Machine-digitization revision**: 2026-07-02
**Author**: Anu Framework pipeline · **2026-07-02 revision**: opus M3 ingestion agent
**Related**: `S703_DPR.md`

---

## 1. Classification

The book-period WORLDAVG line now **exists** — it was machine-digitized off Shaikh's printed Fig 7.13 on 2026-07-02 (see `S703_DPR.md` §0). But there is still **no live-API extension**: the digitized series is **book-period-only** (1970–1990). `extension_status = discontinued`.

## 2. Why no extension is attempted

- The original raw data (OECD ISDB 1994 vintage, via Christodoulopoulos 1995) is **discontinued** and not redistributed in any public form; recovering the book-period values by digitizing the printed figure does **not** make the source live-extendable.
- The closest modern source, **OECD STAN**, is **not splice-compatible**: it carries an **ISIC Rev3 → Rev4 industry break** against ISDB's 8-industry schema, and its **capital-stock coverage is sparse** (many country-industry cells lack gross capital stock — the same obstacle that limited Shaikh's own later OECD work to IROP only).
- Any modern panel would therefore be a methodologically separate exhibit, not a faithful extension. Per the Anti-Degradation rule, we do not splice.

## 3. Method

N/A — no extension. The book-period values are the machine-digitized WORLDAVG line documented in `S703_DPR.md` §4.

## 4. No-Proxy disclosure

**None attempted.** No modern proxy could meet the Anu No-Proxy bar across the ISIC Rev3→Rev4 break and the sparse-capital-stock gap.

## 5. No-Synthetic disclosure

**None.** No interpolation. The 1974 point is **left as an honest gap**, not filled (see `S703_DPR.md` §7). The book-period digitization itself is a disclosed reading of the printed figure (`provenance: machine_digitized`), not synthetic infill.

## 6. Failure-mode table

| Situation | Action |
|---|---|
| Loader invoked | Reads the digitized consensus (returns-precedence guard); emits the 20-point book-period series |
| Extension requested | None — `extension_status = discontinued`; ISDB is not splice-compatible with OECD STAN |
| Validator invoked | Round-trips the digitized values + 3 reference vertices + plausibility band — PASS |

## 7. CD2 divergence pre-disclosure

CD2 (the predecessor build of this dataset) had no per-series CSV that matches this exhibit's WORLDAVG content. The CD2-vs-RSCD comparison is not meaningful here.

## 8. Recovery / supersession paths

The book-period recovery is **done** (machine digitization, 2026-07-02). The one remaining path is a **superseding** one, not an extension: if a human-guided digitization is filed at internal remediation record, it replaces the machine consensus (`human_guided` > `machine_digitized`); `L01_S703` prefers it automatically. A full data reconstruction from an archived ISDB copy or an OECD-STAN redo would be a *new* exhibit, not an extension of this line.

## Notation (plain-language key)

Short forms used above, in plain language (this record is a downloadable external artifact):

- **S### / -A** — a series identifier / subseries in this project (e.g. S703, S703-A).
- **WORLDAVG** — the world manufacturing average rate of profit (the single aggregate line in Fig 7.13).
- **DPR / EPR** — Data Provenance Record / Extension Provenance Record (this file).
- **Phase N** — Anu Framework pipeline stages: Phase 6 = extension, Phase 9 = visualization.
- **CD2** — the predecessor build of this dataset.
- **ROP** — (average) rate of profit.
- **ISDB** — OECD International Sectoral Database (discontinued 1994 vintage).
- **STAN** — OECD Structural Analysis database (successor; ISIC Rev4).
- **ISIC Rev3 / Rev4** — successive revisions of the international industry classification; the Rev3→Rev4 break blocks a clean splice.
- **NSSR** — New School for Social Research.

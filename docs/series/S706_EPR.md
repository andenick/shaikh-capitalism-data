# S706 — Extension Provenance Record

**Series**: S706 — Figure 7.17 — US Industry Incremental Rates of Profit, 1988–2005 (BEA/Shaikh 2008)
**Phase**: 6 (Extension)
**Construction classification**: `composite`
**Extension method**: Phase 5 = **direct byte-exact replication** from Shaikh Appendix 7.2 (salvaged xlsx). Extension to current year = **end-to-end BEA / OECD primary re-fetch** (deferred per Phase 4 adequacy)
**Authored**: 2026-05-18
**Author**: opus-subagent-ch7-fanout
**Related**: `S706_DPR.md`

---

## 1. Why this series is extendable in principle

`content_type = time_series` and the underlying primaries (BEA GDP-by-Industry; BEA Fixed Assets; OECD STAN; FRB Z.1) are continuously published. The Phase 4 adequacy confirmed all primary endpoints return HTTP 200.

## 2. Construction classification

`composite`. Per the Anu rule on lazy splices:

> "If the original computed a formula (P*=D/(r-g), r=NOS/K, ratio=X/Y), the extension must compute the same formula with extended component data."

This applies here. The series is **not** a directly-observed time series — it is computed from multiple BEA / OECD components with non-trivial methodological adjustments (WEQ removal, OOH removal, inventory/reserve additions, exclusion-list restriction, aggregate-before-ratio). Therefore extension to 2024 cannot be a growth-rate splice on the published value; it must **re-fetch the components** and **re-compute the formula**.

## 3. Method

### 3.1 Phase 5 byte-exact replication (this wave)

```
INPUTS
  Shaikh Appendix 7.2 xlsx in SalvagedInputs/book_data/ShaikhChoppedTables/

PROCEDURE
  L01: read xlsx with header at row 1 (descriptive title at row 0)
  L01: write one raw parquet per industry column (long form: year, value, subseries_id, source_id, units)
  P02: union the raw parquets, sort by year + subseries_id, emit data/processed/S706.parquet
  V03: compare row-by-row vs xlsx; expect MAE ≈ 0
```

### 3.2 Phase 6 extension (deferred)

```
INPUTS (deferred wave)
  BEA GDPbyInd_VA_NAICS via BEA API (apps.bea.gov; current vintage)
  BEA Fixed Asset Tables 3.1ES / 3.4ES / 3.7ES via BEA API
  NIPA Table 7.12 for OOH lines
  FRB Z.1 release for L.109 / L.114–117 reserve flows
  Shaikh_2008_Appendix_B_industries.csv for the 31-industry drop key

PROCEDURE
  L01_ext: fetch above (cache 30 days)
  P02_ext: re-apply WEQ/OOH/inventory/reserve, EXCLUDING post-2013 R&D/IP capitalization to preserve Shaikh's 2008 capital concept
  V03_ext: re-validate against book-period; overlap should match within 1.0%; extension years carry tolerance documentation
```

Byte-exact 1988-2005 in Phase 5; BEA extension deferred (post-2008 IROP regime is high-volatility per CD2 — sign-flipping near zero denominators; default presentation per playbook = raw unwinsorized when extended).

## 4. Component re-fetching

Required for any extension. The Anu rule explicitly forbids splicing a derived rate; we re-fetch and re-compute.

## 5. Proxies

**None.** Shaikh's Appendix 7.2 panel is itself derived from BEA primaries; the BEA primaries remain the canonical source. No substitution.

## 6. Synthetic data

**None.** No interpolation.

## 7. Failure modes & graceful degradation

| Failure | Detection | Action |
|---|---|---|
| Salvaged xlsx missing | L01 file-exists check | FAIL (re-fetch from Wayback snapshot) |
| Excluded industry not present in panel | P02 schema check | log warning; emit panel-as-is |
| BEA endpoint 4xx/5xx (extension only) | L01_ext fetcher | retry 3× w/ 2s backoff; degrade extension |

## 8. Splice diagnostics (reported by V03)

V03 emits MAE, max absolute error, and a divergence list of any year where the byte-exact reproduction differs from the xlsx column by > {tol}%. For S705/S706/S709/S710/S711, that tolerance is **1.0%** (time_series default); in practice MAE ≈ 0 because the L01 reads the xlsx directly.

## 9. CD2 divergence pre-disclosure

CD2's per-series CSV for `S036` is the closest legacy comparison. CD2 used the same Shaikh Appendix 7.2 source for the book period and applied its own end-to-end re-run for the 2006–2024 extension. RSCD's Phase 5 deliverable does not extend; in this wave RSCD's book-period values should agree with CD2 at MAE = 0 (modulo presentation choices on the All-Private aggregate column).

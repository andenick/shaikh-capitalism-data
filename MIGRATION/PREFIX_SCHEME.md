# Series ID Prefix Scheme

**Project**: RSCD — Shaikh (2016) Replication
**Convention**: Anu Framework v12.2, Series ID Spec v2.2
**Last revised**: 2026-07-10 (XS-era rewrite; F-3D-04)
**Migration applied**: AS/ES → XS migration 2026-06-10 (see `MIGRATION/crosswalk.csv`)

This document is the binding spec for series identifiers. Every series in
`series_registry.json` MUST follow exactly one of the two active patterns below.
Validators (anu-doctor P12) reject any ID that does not match.

> **XS migration (2026-06-10):** The legacy `AS###` and `ES####` prefix families
> are **retired**. All former AS (GPIM internals) and ES (external-study) series have
> been consolidated under the `XS` prefix. The old→new mapping is in
> `MIGRATION/crosswalk.csv`. **anu-doctor P12 now rejects AS/ES IDs.**

---

## `S###` — Book Series (active)

**Meaning**: Empirical data series that appears in Anwar Shaikh, *Capitalism: Competition,
Conflict, Crises* (Oxford University Press, 2016). One series ≈ one underlying data
construct, even if it appears in multiple figures or tables.

**Pattern**: `S{chapter}{seq}` where
- `{chapter}` = the 1- or 2-digit dominant chapter number (1–17). When a series spans
  chapters, use the chapter of its primary construction.
- `{seq}` = a 2-digit sequence within that chapter, starting at `01`.

**Examples**:
- `S201` — Chapter 2, series 01 (US Industrial Production Index, Fig 2.1)
- `S1601` — Chapter 16, series 01
- `S503` — Chapter 5, series 03

**Capacity**: 99 series per chapter (more than the book ever uses).

**Migration note**: CD used flat `S001–S105` (no chapter info). CD2 used flat `S001–S113`.
RSCD IDs encode chapter, so CD2 `S047` (Ch6) becomes `S605` in RSCD. Crosswalk:
`MIGRATION/CD2_to_RSCD_crosswalk.csv`.

---

## `XS###` — Extra Series (active; introduced v1.3, replaces AS + ES)

**Meaning**: Series that are not primary book constructs but travel alongside them in the
RSCD project. There are two sub-classes, distinguished by the `xs_class` registry field:

| `xs_class` | Semantics | Former prefix | Chapter |
|---|---|---|---|
| `appendix` | GPIM construction internals from Chapter 6 Appendix; analytical/derived series used to build the S6xx book series | `AS###` (retired) | `chapter: 6` |
| `external_study` | Replication of a Shaikh-adjacent external study (Shaikh 2020, Shaikh-Coronado-Nassif-Pires 2020, Shaikh-Jacobo 2020, Weber-Shaikh 2020) | `ES####` (retired) | `chapter: 0` |

**Pattern**: `XS{seq}` where `{seq}` is a 3-digit sequence starting at `001` (appendix
class) OR `XS{group}{seq}` where group is a 4-digit study code (external-study class).

**Active XS series**:

| XS ID | Former ID | xs_class | Description |
|---|---|---|---|
| `XS001` | `AS001` | appendix | GDP/GDI Decomposition and Business NOS |
| `XS002` | `AS002` | appendix | Wage Equivalent and Corporate/Noncorporate Split |
| `XS003` | `AS003` | appendix | Imputed Interest Adjustment and Sectoral Profit Rates |
| `XS004` | `AS004` | appendix | GPIM Corporate Capital Stock |
| `XS005` | `AS005` | appendix | GPIM Variant — BEA 2011 Initial Value |
| `XS006` | `AS006` | appendix | GPIM Variant — BEA 1993 vs 2011 |
| `XS007` | `AS007` | appendix | GPIM Variant — IRS Adjusted |
| `XS008` | `AS008` | appendix | GPIM Variant — Interwar Adjusted |
| `XS009` | `AS009` | appendix | IRS Corporate Inventories and Total Capital Stock |
| `XS2001` | `ES2001` | external_study | Shaikh (2020) Sraffa prices series 01 |
| `XS2101` | `ES2101` | external_study | Shaikh-Coronado-Nassif-Pires (2020) series 01 |
| `XS2201` | `ES2201` | external_study | Shaikh-Jacobo (2020) series 01 |
| `XS2301` | `ES2301` | external_study | Weber-Shaikh (2020) US-China trade series 01 |
| `XS2302` | `ES2302` | external_study | Weber-Shaikh (2020) series 02 |
| `XS2303` | `ES2303` | external_study | Weber-Shaikh (2020) series 03 |
| `XS2304` | `ES2304` | external_study | Weber-Shaikh (2020) series 04 (publish: false) |
| `XS2305` | `ES2305` | external_study | Weber-Shaikh (2020) series 05 (publish: false) |

**Required registry fields for all XS series**:
- `xs_class: "appendix"` or `xs_class: "external_study"`
- `xs_attribution`: citation / attribution string
- `chapter: 6` (appendix class) or `chapter: 0` (external_study class)

---

## Retired Prefixes

The following ID patterns are **invalid** and will be rejected by anu-doctor P12:

| Pattern | Status | Replacement | Note |
|---|---|---|---|
| `AS###` | **RETIRED 2026-06-10** | `XS001`–`XS009` | Former GPIM construction internals; migration applied |
| `ES####` | **RETIRED 2026-06-10** | `XS2001`–`XS2305` | Former external-study series; migration applied |
| Flat `S001–S999` | Invalid from day 1 | `S{ch}{seq}` | CD/CD2 convention, not RSCD |
| `T###` / `N###` | Invalid | — | RMWND's pre-migration ST2 convention |
| IDs with spaces, lowercase, or hyphens | Invalid | — | — |
| Leading zeros for ambiguous chapter (e.g. `S0201`) | Invalid | `S201` | Chapter 2 series 01 is `S201` |

---

## Validator

`code/utils/id_validator.py` validates at runtime. Accepts:
- `^S\d{3,4}$` — S-series (chapter 1–17, seq 01–99)
- `^XS\d{3}$` — XS appendix class (001–009 allocated; extensible)
- `^XS\d{4,5}$` — XS external-study class (2001+)

It is called by every L01/P02/V03/O06 script as the first action on its `run()` entry point.

---

## Migration Reference

Full AS/ES → XS mapping: `MIGRATION/crosswalk.csv`
CD2 → RSCD mapping (including XS re-target): `MIGRATION/CD2_to_RSCD_crosswalk.csv`
Migration log: `MIGRATION/MIGRATE_SCHEME_LOG.md`

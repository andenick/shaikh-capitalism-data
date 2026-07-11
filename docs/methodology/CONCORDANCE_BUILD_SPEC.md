# RSCD Concordance Resolver — Build Specification

**Phase-3 build-spec (NOT wired into loaders this pass).** A design for canonical machine-readable
concordance tables and a resolver that generalizes the working
`code/L01_loaders/_nipa_t711_line_resolver.py` pattern — label/code-based lookup that survives vintage
revision. Implementation is a **follow-up pass**; this document specifies the schema, interface,
validation, and a prioritized backlog.

- **Compiled:** 2026-06-30 (RSCD Phase-3 concordance-synthesis agent)
- **Reads from:** `concordances/rscd_series_classification_map.csv`,
  `concordances/sic_naics_bridge_seed.csv`, `concordances/io_benchmark_industry_seed.csv`,
  `concordances/_sources/` (official Census bridges), `_timelines/{IO,NIPA}_CHANGE_TIMELINE.md`.
- **Non-goal (this pass):** editing any `L01_*`/`P02_*` loader, the registry, or the replicator.
  This is a **paper design + seeds**; nothing here is imported by running code yet.

---

## 1. Design principle (inherited from the T7.11 resolver)

The T7.11 resolver's core idea is the whole design in miniature: **resolve by a persistent semantic key,
not by a positional index that revisions move.** For T7.11 the persistent key is the BEA `LineDescription`
stub label (survives every vintage); the fragile index is the line number (the 2018 update shifted it +1).
Generalize:

| Concordance | Persistent key (resolve by THIS) | Fragile index (never hard-code) |
|---|---|---|
| NIPA line resolves (T7.11, T1.10, Z.1) | BEA/Fed row **stub label** | published **line number** (moves at comprehensive updates) |
| SIC ↔ NAICS | Census **code + title** pair, with explicit part-indicator | a presumed 1:1 code map (it is many-to-many) |
| BEA I-O order (71/65) | **classification_vintage** tag + industry **title** | bare 1..71 / 1..65 integer index |
| ISIC Rev3 ↔ Rev4 | ISIC **code + title** + revision tag | short author label (does not map cleanly) |
| Source-code remap (WPI→PPI, IFS→SDMX) | **concept** id (agency + concept), not the string id | the discontinued provider string id |

Every resolve returns not just an answer but a **provenance record**: which source file/URL, which
vintage, whether the mapping was one-to-one or required allocation, and a confidence flag.

---

## 2. Canonical table schema

Three canonical machine-readable table types under `concordances/canonical/` (to be built):

### 2.1 `concordance_edges.csv` — the universal edge list
One row per directed mapping edge. Superset of all crosswalk types.

```
concordance_id      TEXT   -- e.g. "sic1987_naics1997", "naics1997_naics2002", "io71_naics65",
                           --      "isic_rev3_rev4", "t711_linelabel"
from_scheme         TEXT   -- "1987_SIC" | "1997_NAICS" | "OCHOA_71" | "ISIC_REV3" | "T711_2011" ...
from_code           TEXT   -- code or stub-label in the source scheme
from_title          TEXT
to_scheme           TEXT
to_code             TEXT
to_title            TEXT
part_indicator      TEXT   -- Census "part" flag; "" if whole
cardinality         TEXT   -- "1:1" | "1:N" | "N:1" | "N:N"
allocation_weight   REAL   -- share in [0,1] when a split needs weights; NULL if unknown/not-applicable
source_file         TEXT   -- e.g. "_sources/naics/1987_SIC_to_1997_NAICS.csv"
source_url          TEXT   -- authoritative URL (Census/BEA)
retrieval_date      DATE   -- 2026-06-30
confidence          TEXT   -- "official" | "derived" | "manual" | "approximate"
notes               TEXT
```

### 2.2 `line_label_index.csv` — vintage-stable NIPA/Fed line resolves
Generalizes the `_T711_LINE_INDEX` dict to a table so T1.10, Z.1 D.3, T2.1 etc. can be added.

```
table_id            TEXT   -- "T7.11" | "T1.10" | "Z1_D3" | "T2.1"
stub_label          TEXT   -- normalized persistent caption (the resolve key)
bea_linedescription TEXT   -- exact published caption (for API LineDescription match)
vintage_year        INT    -- 2011 | 2018 | 2024 ...
line_number         INT    -- published line at that vintage
source_url          TEXT
notes               TEXT   -- e.g. "2018 +1 shift for lines >= 44"
```

### 2.3 `scheme_registry.csv` — the classification-system catalogue
```
scheme_id           TEXT   -- "1987_SIC", "1997_NAICS", ..., "OCHOA_71", "BEA_65", "ISIC_REV3", "UK_SIC_1958"
family              TEXT   -- "SIC" | "NAICS" | "ISIC" | "BEA_IO" | "NIPA_LINE" | "UK_SIC"
vintage_year        INT
authority           TEXT   -- "US Census" | "BEA" | "OECD" | "UN" | "ONS"
staged_in_project   BOOL   -- TRUE only for the US Census SIC/NAICS chain + T7.11 today
frozen              BOOL   -- TRUE = book-period-only, no live extension target (pre-SIC, UK-1958, Ochoa-71)
notes               TEXT
```

---

## 3. Resolver interface

A single module `concordances/canonical/concordance_resolver.py` (to be built), generalizing the T7.11
functions. All functions are **pure lookups over the canonical CSVs** — no network unless an explicit
`live=True` is passed (mirrors `fetch_t711_via_api`).

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class ResolveResult:
    to_scheme: str
    to_codes: list[str]          # >1 when many-to-many
    to_titles: list[str]
    cardinality: str             # "1:1" | "1:N" | "N:1" | "N:N"
    allocation_weights: list[float] | None
    confidence: str              # "official" | "derived" | "manual" | "approximate"
    provenance: dict             # {source_file, source_url, retrieval_date, vintage}

def resolve_industry(code: str, from_scheme: str, to_scheme: str,
                     *, allow_many: bool = True) -> ResolveResult:
    """Map an industry code across schemes via concordance_edges.csv.
    Raises ManyToManyError if allow_many=False and cardinality in {1:N, N:N}."""

def resolve_line(table_id: str, stub_label: str, vintage_year: int) -> int | None:
    """NIPA/Fed line resolve by persistent stub label (generalizes resolve_t711_line +
    stub_label_to_current_line). Falls back to nearest pinned vintage with a logged warning."""

def resolve_line_by_caption(table_id: str, bea_linedescription: str,
                            vintage_year: int) -> int | None:
    """Resolve straight from a BEA-API LineDescription string (bypasses line-number drift)."""

def chain_resolve(code: str, path: list[str]) -> ResolveResult:
    """Walk a multi-hop path, e.g. ['1987_SIC','1997_NAICS','2002_NAICS',...,'2022_NAICS'] or
    ['ISDB','1987_SIC','1997_NAICS']. Composes cardinality (any N-hop => N:N) and multiplies
    allocation weights when present."""

def scheme_info(scheme_id: str) -> dict:
    """Return scheme_registry row; callers check `frozen` before attempting a live extension."""
```

**Inputs:** the three canonical CSVs (§2). **Outputs:** `ResolveResult` with an always-populated
`provenance` dict. **Provenance fields:** `source_file`, `source_url`, `retrieval_date`, `vintage`,
`confidence`, plus `cardinality`/`allocation_weights` so a caller can *see* when a mapping is lossy and
refuse to proceed silently.

---

## 4. Validation

Ported from the T7.11 self-test discipline and extended:

1. **Round-trip.** For every 1:1 edge, `resolve(resolve(x, A→B), B→A) == x`. For N:N edges, the reverse
   set must **contain** x (documented non-invertibility, not a failure).
2. **Coverage.** Every `sid` with `needs_crosswalk_for_extension = TRUE` in
   `rscd_series_classification_map.csv` must have at least one resolvable path in `concordance_edges.csv`
   **or** an explicit `frozen`/`not_staged` marker in `scheme_registry.csv`. No silent gaps.
3. **Many-to-many handling.** A resolve that returns cardinality ∈ {1:N, N:N} with
   `allow_many=False` MUST raise, never pick one arbitrarily. When weights are absent, `confidence` must
   be `"approximate"` and the caller must log it.
4. **Vintage guard (the CH9-F4 fix).** Any I-O industry index concatenation across benchmark years must
   assert matching `classification_vintage`; mixing `OCHOA_71` (SIC) and `BEA_65` (NAICS) rows raises.
5. **Provenance completeness.** Every edge row must have a non-empty `source_file` OR `source_url` and a
   `retrieval_date`. CI check: no fabricated rows (every Census-derived edge must re-derive from the file
   in `_sources/naics/`).
6. **Line-label persistence.** For each `table_id`, the set of `stub_label`s must be identical across all
   pinned `vintage_year`s (a caption that disappears signals a real BEA change needing a new mapping row,
   per the T7.11 module's "ADD a new vintage row rather than editing" rule).

---

## 5. Prioritized build backlog

Ordered by *how many extensions each concordance unblocks*, keyed to the series map.

| # | Build item | Unblocks | Effort | Source ready? |
|---|---|---|---|---|
| **P1** | **`line_label_index.csv` + port the T7.11 resolver into the generic module.** Add T1.10 (ch14 wage-share) and Z.1 D.3 / T2.1 (ch16 S1605) line-label rows. | **8 series** (S601–S604, S1007, S1008, S1604, XS003) + hardens ch14/ch16 | Low — the working resolver + `NIPA_T711_FISIM_remap.md` already encode T7.11; extend the table. | **Yes** (pinned 2011/2018/2024) |
| **P2 — DONE (2026-07-02, FU-2)** | **Materialize `concordance_edges.csv` for the US Census SIC↔NAICS + NAICS revision chain** from the 14 staged CSVs, with `cardinality` + `part_indicator` populated. → `concordances/concordance_edges.csv` (19,607 edges); generator `remediation_campaign/scripts/build_concordance_edges.py`; seed cross-val 24/24, round-trip consistent. | **~13 series** (ch7 30-industry S705/706/709/710; ch8 S801–805; ch10 S1001; ch15 S1502/1503) | Medium — mechanical parse of `_sources/naics/*.csv`; the `sic_naics_bridge_seed.csv` is the pilot. | **Yes** |
| **P3** | **Extract the BEA I-O↔NAICS concordances from the SCB PDF appendices to CSV** (SCB Dec 2002 App.A = 1997 codes; Oct 2007 = 2002; Aug 2018 = 2007/2012) and add as edges with `from_scheme = BEA_65 / IO_2002...`. | **5 series** (S901–903, XS009, XS2101) — the ch9 wall + the IO ladder | High — PDF-table extraction (fullread/Sraffa); URLs staged in `_sources/SOURCES.md`. | **URLs only** |
| P4 | ISIC Rev3↔Rev4 crosswalk (import the UN/OECD correspondence; map Shaikh's short labels by hand). | 4 int'l series (S213/214, S703/704, S711) | High | **Not staged** (external) |
| P5 | `scheme_registry.csv` with `frozen`/`staged`/`not_staged` flags — the cheap enabler for validation §2. | All (coverage gate) | Low | **Yes** |

**Recommended order: P1 → P5 → P2 → P3 → P4.** P1 and P5 are low-effort and immediately harden the
already-working line-label + coverage-gate machinery; P2 turns the pilot seed into the full US Census
edge list (biggest series count); P3 is the high-value-but-high-effort ch9 unblock; P4 is the
international frontier and can trail.

**Explicitly out of scope (structural, not a build task):** the 1947–1992 SIC-era I-O *code* concordance
(never published in staged form) and the post-1997 benchmark **capital-flow matrix** (discontinued by BEA
after 1997) — both are documented walls in `IO_CHANGE_TIMELINE.md`, to be approximated, not resolved.

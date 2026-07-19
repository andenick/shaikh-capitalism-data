"""Generalized NIPA/Fed line-label resolver (SI-2 P1, Block G2a).

Generalizes ``_nipa_t711_line_resolver`` (which is T7.11-specific) into a
table-agnostic resolver driven by the canonical seed
``docs/methodology/concordances/line_label_index.csv`` (built by
``remediation_campaign/scripts/build_line_label_index.py``).

The design principle is inherited verbatim from the T7.11 resolver and
CONCORDANCE_BUILD_SPEC.md Sec 1: **resolve by a persistent semantic key (the BEA/Fed
row stub label or its published caption), never by the positional line number that
comprehensive revisions move.** This module extends that pattern to T7.12 (the
owner-occupied-housing imputation strip — the named T7.11-only generalization gap),
T1.10, Z.1 D.3 and T2.1.

All functions are **pure lookups** over the CSV (no network). Interface follows the
build-spec Sec 3 resolver contract: ``resolve_line`` and ``resolve_line_by_caption``.

Usage
-----
    from L01_loaders._nipa_line_resolver import resolve_line, resolve_line_by_caption

    # T7.11 (matches the legacy resolver's stub_label_to_current_line):
    resolve_line("T7.11", "financial_corporate__monetary_interest_paid_by_banks", 2024)  # -> 45

    # T7.12 OOH strip (the generalization gap this closes):
    resolve_line("T7.12", "owner_occupied_housing__net_imputed_rental_income", 2011)     # -> 134

    # By published caption, bypassing line-number drift:
    resolve_line_by_caption("T1.10", "Compensation of employees", 2024)                  # -> 2
"""
from __future__ import annotations

import csv
import logging
from functools import lru_cache
from pathlib import Path

logger = logging.getLogger(__name__)

# Canonical seed table (built from the T7.11 resolver + project docs).
_INDEX_CSV = (
    Path(__file__).resolve().parents[2]
    / "docs" / "methodology" / "concordances" / "line_label_index.csv"
)


@lru_cache(maxsize=1)
def _load_index() -> list[dict[str, str]]:
    """Parse line_label_index.csv into a list of row dicts (cached)."""
    if not _INDEX_CSV.exists():
        raise FileNotFoundError(
            f"line_label_index.csv not found at {_INDEX_CSV}; run "
            f"remediation_campaign/scripts/build_line_label_index.py"
        )
    with _INDEX_CSV.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def _pinned_vintages(table_id: str) -> list[int]:
    return sorted(
        {int(r["vintage_year"]) for r in _load_index() if r["table_id"] == table_id}
    )


def _nearest_vintage(table_id: str, vintage_year: int) -> int | None:
    pinned = _pinned_vintages(table_id)
    if not pinned:
        return None
    earlier = [v for v in pinned if v <= vintage_year]
    return max(earlier) if earlier else min(pinned)


def _effective_vintage(table_id: str, vintage_year: int) -> int | None:
    if vintage_year in _pinned_vintages(table_id):
        return vintage_year
    nearest = _nearest_vintage(table_id, vintage_year)
    if nearest is not None:
        logger.warning(
            "%s vintage %s not pinned; falling back to nearest pinned vintage %s",
            table_id, vintage_year, nearest,
        )
    return nearest


def resolve_line(table_id: str, stub_label: str, vintage_year: int) -> int | None:
    """Resolve a NIPA/Fed line number by persistent stub label.

    Generalizes ``stub_label_to_current_line`` across tables. Falls back to the
    nearest pinned vintage with a logged warning when ``vintage_year`` is not pinned.
    Returns ``None`` if the (table_id, stub_label) pair is unknown.
    """
    eff = _effective_vintage(table_id, vintage_year)
    if eff is None:
        return None
    for r in _load_index():
        if (r["table_id"] == table_id
                and r["stub_label"] == stub_label
                and int(r["vintage_year"]) == eff):
            return int(r["line_number"])
    return None


def resolve_line_by_caption(
    table_id: str, bea_linedescription: str, vintage_year: int
) -> int | None:
    """Resolve straight from a BEA/Fed-published caption string (bypasses line drift).

    Matching is case-insensitive and whitespace-trimmed. Returns ``None`` if no
    caption matches for the (nearest-pinned) vintage.
    """
    eff = _effective_vintage(table_id, vintage_year)
    if eff is None:
        return None
    target = bea_linedescription.strip().lower()
    for r in _load_index():
        if (r["table_id"] == table_id
                and int(r["vintage_year"]) == eff
                and r["bea_linedescription"].strip().lower() == target):
            return int(r["line_number"])
    return None


def stub_labels(table_id: str) -> list[str]:
    """Return the distinct stub labels registered for a table (helper for tests/callers)."""
    return sorted({r["stub_label"] for r in _load_index() if r["table_id"] == table_id})


def tables() -> list[str]:
    """Return the distinct table_ids in the index."""
    return sorted({r["table_id"] for r in _load_index()})


if __name__ == "__main__":
    print("=== _nipa_line_resolver smoke test ===")
    print("tables:", tables())
    for tid in tables():
        print(f"  {tid}: {len(stub_labels(tid))} stub labels, "
              f"vintages {_pinned_vintages(tid)}")
    # T7.11 spot-checks (must agree with the legacy resolver)
    assert resolve_line("T7.11", "financial_corporate__monetary_interest_paid_by_banks", 2011) == 44
    assert resolve_line("T7.11", "financial_corporate__monetary_interest_paid_by_banks", 2024) == 45
    # T7.12 (the generalization gap)
    assert resolve_line("T7.12", "owner_occupied_housing__net_imputed_rental_income", 2011) == 134
    # by-caption path
    assert resolve_line_by_caption("T1.10", "Compensation of employees", 2024) == 2
    print("OK")

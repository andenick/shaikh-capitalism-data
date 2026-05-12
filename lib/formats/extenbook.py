"""Write Anu Extenbook Excel with 4 sheets: Data, Provenance, Research, Construction."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


def write_extenbook(
    data_dict: dict[str, pd.Series],
    registry: dict[str, Any],
    research_data: dict[str, Any] | None,
    series_id: str,
    output_dir: str | Path,
) -> Path:
    """Generate a 4-sheet Extenbook Excel workbook for a series.

    Parameters
    ----------
    data_dict : dict[str, pd.Series]
        Mapping from subseries ID to a pandas Series with integer year index.
    registry : dict
        Full registry dict (output of ``load_registry()``).
    research_data : dict or None
        Parsed contents of ``S###_research.json``, or ``None``.
    series_id : str
        Top-level series key, e.g. ``"S001"``.
    output_dir : Path
        Directory to write the Excel file into.

    Returns
    -------
    Path
        Absolute path to the written file.
    """
    series_config = registry["series"][series_id]
    subseries_defs = series_config["subseries"]
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{series_id}_extenbook.xlsx"

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        _write_data_sheet(writer, data_dict, subseries_defs, series_id)
        _write_provenance_sheet(writer, subseries_defs)
        _write_research_sheet(writer, research_data)
        _write_construction_sheet(writer, series_config)

    return output_path.resolve()


def _column_header(sub_id: str, sub_def: dict[str, Any]) -> str:
    """Build column header, appending [R:YYYY] for reindexed subseries."""
    if sub_def.get("is_reindexed") and sub_def.get("reindex_base_year"):
        return f"{sub_id} [R:{sub_def['reindex_base_year']}]"
    return sub_id


def _write_data_sheet(
    writer: pd.ExcelWriter,
    data_dict: dict[str, pd.Series],
    subseries_defs: dict[str, Any],
    series_id: str,
) -> None:
    """Sheet 1: Year + all subseries columns with data."""
    columns = sorted(subseries_defs.keys())
    all_years: set[int] = set()
    for col_id in columns:
        if col_id in data_dict:
            all_years.update(int(y) for y in data_dict[col_id].index)

    if not all_years:
        pd.DataFrame({"Year": []}).to_excel(writer, sheet_name="Data", index=False)
        return

    years = sorted(all_years)
    records: list[dict[str, Any]] = []
    for year in years:
        row: dict[str, Any] = {"Year": int(year)}
        for col_id in columns:
            header = _column_header(col_id, subseries_defs[col_id])
            if col_id in data_dict and year in data_dict[col_id].index:
                val = data_dict[col_id][year]
                if isinstance(val, pd.Series):
                    val = val.iloc[0]
                try:
                    row[header] = val if pd.notna(val) else None
                except (ValueError, TypeError):
                    row[header] = None
            else:
                row[header] = None
        records.append(row)

    df = pd.DataFrame(records)
    df["Year"] = df["Year"].astype(int)
    df.to_excel(writer, sheet_name="Data", index=False)


def _write_provenance_sheet(
    writer: pd.ExcelWriter,
    subseries_defs: dict[str, Any],
) -> None:
    """Sheet 2: one row per subseries with provenance metadata."""
    rows: list[dict[str, Any]] = []
    for sub_id in sorted(subseries_defs.keys()):
        sub = subseries_defs[sub_id]
        period = sub.get("period", [None, None])
        rows.append({
            "subseries_id": sub_id,
            "name": sub.get("name", ""),
            "source": sub.get("source", ""),
            "period": f"{period[0]}–{period[1]}" if period and len(period) == 2 else "",
            "units": sub.get("units", ""),
            "is_reindexed": sub.get("is_reindexed", False),
            "derived_from": sub.get("derived_from", ""),
            "color": sub.get("color", ""),
        })

    pd.DataFrame(rows).to_excel(writer, sheet_name="Provenance", index=False)


def _write_research_sheet(
    writer: pd.ExcelWriter,
    research_data: dict[str, Any] | None,
) -> None:
    """Sheet 3: research entries from the per-series research JSON."""
    if not research_data or "entries" not in research_data:
        pd.DataFrame(columns=[
            "entry_id", "type", "source_location", "quote",
            "subseries_affected", "confidence",
        ]).to_excel(writer, sheet_name="Research", index=False)
        return

    rows: list[dict[str, Any]] = []
    for entry in research_data["entries"]:
        affected = entry.get("subseries_affected", [])
        rows.append({
            "entry_id": entry.get("entry_id", ""),
            "type": entry.get("type", ""),
            "source_location": entry.get("source_location", ""),
            "quote": entry.get("quote", ""),
            "subseries_affected": ", ".join(affected) if isinstance(affected, list) else str(affected),
            "confidence": entry.get("confidence", ""),
        })

    pd.DataFrame(rows).to_excel(writer, sheet_name="Research", index=False)


def _write_construction_sheet(
    writer: pd.ExcelWriter,
    series_config: dict[str, Any],
) -> None:
    """Sheet 4: construction steps from the registry."""
    steps = series_config.get("construction", [])
    if not steps:
        pd.DataFrame(columns=["step", "op", "input", "output", "parameters"]).to_excel(
            writer, sheet_name="Construction", index=False,
        )
        return

    rows: list[dict[str, str]] = []
    for s in steps:
        input_val = (
            s.get("input")
            or ", ".join(s.get("inputs", s.get("subseries", [])))
        )
        params: list[str] = []
        for key in ("base_year", "at_year", "method", "match_to", "desc"):
            if key in s:
                params.append(f"{key}={s[key]}")
        rows.append({
            "step": str(s.get("step", "")),
            "op": s.get("op", ""),
            "input": input_val,
            "output": s.get("output", ""),
            "parameters": "; ".join(params),
        })

    pd.DataFrame(rows).to_excel(writer, sheet_name="Construction", index=False)

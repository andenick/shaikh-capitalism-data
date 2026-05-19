"""
RSCD viz chart factory.

Dispatches per `content_type`:
    time_series       -> overlaid line traces (one per subseries), extension dashed
    cross_sectional   -> scatter / bar across subseries
    theoretical       -> analytic curve (point/line) from chopped CSV
    derived           -> treated as time_series (still year-indexed)
    data_unavailable  -> empty figure with explanatory annotation
"""
from __future__ import annotations

from typing import Optional

import pandas as pd
import plotly.graph_objects as go

from data_loader import load_chopped, get_series

# Plotly default color cycle — used when a subseries doesn't define one.
_FALLBACK_PALETTE = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
    "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
]


def _subseries_meta(sid: str) -> dict[str, dict]:
    s = get_series(sid) or {}
    return s.get("subseries") or {}


def _color_for(sub_id: str, sub_meta: dict, fallback_idx: int) -> str:
    c = sub_meta.get("color")
    if c:
        return c
    return _FALLBACK_PALETTE[fallback_idx % len(_FALLBACK_PALETTE)]


def _is_extension(sub_meta: dict) -> bool:
    role = (sub_meta.get("role") or "").lower()
    return "extension" in role


def _empty_figure(message: str) -> go.Figure:
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        xref="paper", yref="paper", x=0.5, y=0.5,
        showarrow=False, font=dict(size=14, color="#555"),
    )
    fig.update_layout(
        template="plotly_white",
        height=460,
        margin=dict(l=40, r=20, t=60, b=40),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
    )
    return fig


def _layout(title: str, units: str, content_type: str) -> dict:
    return dict(
        title=dict(text=title, x=0.02, xanchor="left", font=dict(size=15)),
        template="plotly_white",
        height=480,
        margin=dict(l=60, r=20, t=70, b=50),
        hovermode="x unified" if content_type in ("time_series", "derived", "theoretical") else "closest",
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02,
            xanchor="left", x=0, font=dict(size=10),
        ),
        xaxis=dict(
            title="Year" if content_type in ("time_series", "derived") else (
                "Step" if content_type == "theoretical" else "Industry / Category"
            ),
            gridcolor="rgba(0,0,0,0.06)",
        ),
        yaxis=dict(title=units or "", gridcolor="rgba(0,0,0,0.06)"),
    )


def _filter_year_range(df: pd.DataFrame, year_range: Optional[tuple[int, int]]) -> pd.DataFrame:
    if year_range is None or "year" not in df.columns:
        return df
    lo, hi = year_range
    return df[(df["year"] >= lo) & (df["year"] <= hi)]


# ---------------------------------------------------------------------------
# Per-content-type builders
# ---------------------------------------------------------------------------

def _build_time_series(sid: str, df: pd.DataFrame, year_range: Optional[tuple[int, int]],
                       title: str, units: str, content_type: str) -> go.Figure:
    fig = go.Figure()
    sub_meta = _subseries_meta(sid)
    filtered = _filter_year_range(df, year_range)

    # Plot in the order subseries are declared in the registry, then any extras
    declared_order = list(sub_meta.keys())
    present_subs = list(filtered["subseries_id"].dropna().unique()) if "subseries_id" in filtered.columns else []
    ordered = [s for s in declared_order if s in present_subs] + \
              [s for s in present_subs if s not in declared_order]

    for idx, sub_id in enumerate(ordered):
        sub = sub_meta.get(sub_id, {})
        chunk = filtered[filtered["subseries_id"] == sub_id].sort_values("year")
        if chunk.empty:
            continue
        color = _color_for(sub_id, sub, idx)
        is_ext = _is_extension(sub)
        name = sub.get("name") or sub_id
        # Truncate over-long names for legend readability
        legend_name = f"{sub_id}: {name}"
        if len(legend_name) > 65:
            legend_name = legend_name[:62] + "..."
        fig.add_trace(go.Scatter(
            x=chunk["year"],
            y=chunk["value"],
            mode="lines+markers" if len(chunk) < 30 else "lines",
            name=legend_name,
            line=dict(color=color, width=2, dash="dash" if is_ext else "solid"),
            marker=dict(size=5),
            hovertemplate=(
                f"<b>{sub_id}</b><br>Year: %{{x}}<br>"
                f"Value: %{{y:.4g}} {units}<extra></extra>"
            ),
        ))

    fig.update_layout(**_layout(title, units, content_type))
    return fig


def _build_cross_sectional(sid: str, df: pd.DataFrame, title: str, units: str) -> go.Figure:
    """
    Cross-sectional: scatter of subseries pairs by industry/category index.
    S216 example: S216-A (prices of production) vs S216-B (unit labor costs)
    indexed by industry_index.
    """
    fig = go.Figure()
    sub_meta = _subseries_meta(sid)
    x_axis_col = None
    for cand in ("industry_index", "category", "category_index", "rank"):
        if cand in df.columns:
            x_axis_col = cand
            break

    if x_axis_col is None:
        # Fall back to row order
        df = df.copy()
        df["_idx"] = range(len(df))
        x_axis_col = "_idx"

    for idx, (sub_id, sub) in enumerate(sub_meta.items()):
        chunk = df[df["subseries_id"] == sub_id]
        if chunk.empty:
            continue
        color = _color_for(sub_id, sub, idx)
        name = sub.get("name") or sub_id
        legend_name = f"{sub_id}: {name}"[:65]
        fig.add_trace(go.Scatter(
            x=chunk[x_axis_col],
            y=chunk["value"],
            mode="markers",
            name=legend_name,
            marker=dict(color=color, size=7, opacity=0.75),
            hovertemplate=(
                f"<b>{sub_id}</b><br>{x_axis_col}: %{{x}}<br>"
                f"Value: %{{y:.4g}}<extra></extra>"
            ),
        ))

    layout = _layout(title, units, "cross_sectional")
    layout["xaxis"]["title"] = x_axis_col.replace("_", " ").title()
    fig.update_layout(**layout)
    return fig


def _build_theoretical(sid: str, df: pd.DataFrame, title: str, units: str) -> go.Figure:
    """
    Theoretical: analytic curve points, one trace per subseries.
    X axis is whatever 'year' field holds (often a step or iteration index).
    """
    fig = go.Figure()
    sub_meta = _subseries_meta(sid)
    for idx, (sub_id, sub) in enumerate(sub_meta.items()):
        chunk = df[df["subseries_id"] == sub_id].sort_values("year") if "subseries_id" in df.columns else df
        if chunk.empty:
            continue
        color = _color_for(sub_id, sub, idx)
        name = sub.get("name") or sub_id
        legend_name = f"{sub_id}: {name}"[:65]
        fig.add_trace(go.Scatter(
            x=chunk["year"],
            y=chunk["value"],
            mode="lines+markers",
            name=legend_name,
            line=dict(color=color, width=2),
            marker=dict(size=4),
            hovertemplate=(
                f"<b>{sub_id}</b><br>Step: %{{x}}<br>"
                f"Value: %{{y:.4g}}<extra></extra>"
            ),
        ))

    layout = _layout(title, units, "theoretical")
    fig.update_layout(**layout)
    return fig


# ---------------------------------------------------------------------------
# Public factory
# ---------------------------------------------------------------------------

def build_figure(sid: str, year_range: Optional[tuple[int, int]] = None) -> go.Figure:
    """Build the appropriate Plotly figure for `sid`."""
    meta = get_series(sid)
    if not meta:
        return _empty_figure(f"Series {sid} not found in registry.")

    content_type = (meta.get("content_type") or "time_series").lower()
    name = meta.get("name", sid)
    units = meta.get("units", "")
    figs = meta.get("figures") or []
    fig_suffix = f" — {', '.join(figs)}" if figs else ""
    title = f"{sid}: {name}{fig_suffix}"

    df = load_chopped(sid)
    if df is None or df.empty:
        if content_type == "data_unavailable" or meta.get("status") == "data_unavailable":
            return _empty_figure(
                f"{sid} — data unavailable.\n"
                "This series is intentionally not extracted (see DPR / EPR for the reason)."
            )
        return _empty_figure(f"{sid}: no chopped CSV present.")

    if content_type in ("time_series", "derived"):
        return _build_time_series(sid, df, year_range, title, units, content_type)
    if content_type == "cross_sectional":
        return _build_cross_sectional(sid, df, title, units)
    if content_type == "theoretical":
        return _build_theoretical(sid, df, title, units)

    # Default fallback
    return _build_time_series(sid, df, year_range, title, units, "time_series")

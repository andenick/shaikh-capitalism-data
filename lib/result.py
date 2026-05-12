"""Standard result types for loading and processing phases."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pandas as pd


@dataclass
class LoadResult:
    series_id: str
    status: str = "ok"
    source_file: str = ""
    obs_count: int = 0
    columns: list[str] = field(default_factory=list)
    message: str = ""


@dataclass
class SeriesResult:
    series_id: str
    status: str = "ok"
    data: dict[str, pd.Series] = field(default_factory=dict)
    extension: pd.Series | None = None
    steps: list[dict[str, str]] = field(default_factory=list)
    year_range: str = ""
    message: str = ""

    def step(self, name: str, status: str, detail: str = ""):
        self.steps.append({"name": name, "status": status, "detail": detail})

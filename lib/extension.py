"""Centralized extension engine for all series."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import pandas as pd

from .transforms.splice import splice

log = logging.getLogger(__name__)


class ExtensionEngine:
    """Fetch API data and extend series using registry-driven configuration."""

    def __init__(self, registry: dict, cache_dir: Path):
        self.registry = registry.get("series", registry)
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._api_key_cache: dict[str, str] = {}

    def extend(
        self,
        series_id: str,
        original: pd.Series,
        method: str | None = None,
    ) -> tuple[pd.Series, pd.Series | None, str]:
        """Extend a series using its registry extension config.

        Returns (extended_series, ext_only_data, description).
        If no extension configured or fetch fails, returns (original, None, reason).
        """
        entry = self.registry.get(series_id, {})
        ext_cfg = entry.get("extension")
        if not ext_cfg or not isinstance(ext_cfg, dict):
            return original, None, "no extension configured"

        splice_year = ext_cfg.get("splice_year")
        if splice_year is None:
            splice_year = int(original.index.max())

        ext_method = method or ext_cfg.get("method", "growth_rate")
        source = ext_cfg.get("source", "")
        api_series = ext_cfg.get("api_series_id", ext_cfg.get("api_series", ""))

        try:
            upstream = self._fetch(source, api_series, ext_cfg)
            if upstream is None or upstream.empty:
                return original, None, f"fetch returned empty for {source}/{api_series}"

            if ext_method == "direct_append":
                divide_by = ext_cfg.get("divide_by", 1)
                if divide_by != 1:
                    upstream = upstream / divide_by
                new_yrs = upstream[upstream.index > splice_year].dropna()
                if new_yrs.empty:
                    return original, None, "no new years after splice"
                extended = pd.concat([original, new_yrs]).sort_index()
                return extended, new_yrs, f"direct append from {source}, +{len(new_yrs)} years"

            elif ext_method in ("growth_rate", "growth_rate_splice"):
                extended = splice(original, upstream, at_year=splice_year, method="growth_rate")
                new_yrs = extended[~extended.index.isin(original.index)]
                if new_yrs.empty:
                    return original, None, "growth splice produced no new years"
                return extended, new_yrs, f"growth-rate splice from {source} at {splice_year}, +{len(new_yrs)} years"

            elif ext_method == "formula":
                return original, None, "formula extension must be handled in processing module"

            else:
                return original, None, f"unknown method: {ext_method}"

        except Exception as e:
            log.warning("Extension failed for %s: %s", series_id, e)
            return original, None, f"failed: {e}"

    def _fetch(self, source: str, api_series: str, config: dict) -> pd.Series | None:
        """Dispatch to the appropriate fetcher."""
        source_lower = source.lower()

        if "fred" in source_lower:
            return self._fetch_fred(api_series)
        elif "bea" in source_lower:
            return self._fetch_bea(config)
        elif "world bank" in source_lower or "worldbank" in source_lower:
            return self._fetch_worldbank(config)
        elif "measuringworth" in source_lower:
            return self._fetch_cached_json(api_series)
        elif "shiller" in source_lower:
            return self._fetch_shiller(config)
        elif "damodaran" in source_lower:
            return self._fetch_damodaran(config)
        elif "maddison" in source_lower:
            return self._fetch_maddison(config)
        elif "oecd" in source_lower:
            return None  # OECD handled in ch07/ch15 processing modules

        return None

    def _get_fred_key(self) -> str | None:
        if "FRED" in self._api_key_cache:
            return self._api_key_cache["FRED"]
        import os
        key = os.environ.get("FRED_API_KEY")
        if not key:
            key_file = Path(__file__).resolve().parent.parent / "config" / "api_keys.env"
            if key_file.exists():
                for line in key_file.read_text().splitlines():
                    if line.startswith("FRED_API_KEY="):
                        key = line.split("=", 1)[1].strip()
        self._api_key_cache["FRED"] = key
        return key

    def _fetch_fred(self, series_id: str) -> pd.Series | None:
        import requests
        key = self._get_fred_key()
        if not key:
            return None
        cache = self.cache_dir / f"fred_{series_id}.json"
        if cache.exists():
            import json
            data = json.loads(cache.read_text(encoding="utf-8"))
        else:
            resp = requests.get(
                "https://api.stlouisfed.org/fred/series/observations",
                params={"series_id": series_id, "api_key": key,
                        "file_type": "json", "frequency": "a"},
                timeout=30,
            )
            if resp.status_code != 200:
                return None
            data = resp.json()
            cache.write_text(resp.text, encoding="utf-8")

        obs = data.get("observations", [])
        records = {}
        for o in obs:
            try:
                records[int(o["date"][:4])] = float(o["value"])
            except (ValueError, KeyError):
                continue
        if not records:
            return None
        s = pd.Series(records).sort_index()
        s.index.name = "year"
        return s

    def _fetch_bea(self, config: dict) -> pd.Series | None:
        return None  # BEA handled in processing modules with specific table logic

    def _fetch_worldbank(self, config: dict) -> pd.Series | None:
        return None  # WorldBank handled in processing modules

    def _fetch_cached_json(self, series_id: str) -> pd.Series | None:
        import json
        for cache in sorted(self.cache_dir.glob(f"*{series_id}*.json")):
            data = json.loads(cache.read_text(encoding="utf-8"))
            obs = data.get("observations", [])
            records = {}
            for o in obs:
                try:
                    records[int(o.get("year", o.get("date", "")))] = float(o.get("value", 0))
                except (ValueError, TypeError):
                    continue
            if records:
                return pd.Series(records).sort_index()
        return None

    def _fetch_shiller(self, config: dict) -> pd.Series | None:
        return None  # Handled in ch10 processing

    def _fetch_damodaran(self, config: dict) -> pd.Series | None:
        return None  # Handled in ch10 processing

    def _fetch_maddison(self, config: dict) -> pd.Series | None:
        return None  # Handled in ch02 processing

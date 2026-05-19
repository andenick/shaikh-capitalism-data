"""S00 setup phase: API clients, on-disk cache, configuration loader.

These modules are loaded at the start of every pipeline run. They have no
per-series state and provide infrastructure that L01/P02/V03 scripts depend on.

Public API:
    S00_apis.fred_observations(series_id, frequency='a', aggregation='avg') -> pd.DataFrame
    S00_apis.fred_health() -> dict
    S00_apis.bea_table(dataset, table_name, frequency, year) -> pd.DataFrame   (stub for future use)
    S00_cache.get(source, query_hash) -> pd.DataFrame | None
    S00_cache.put(source, query_hash, df, metadata) -> Path
    S00_config.load() -> dict
    S00_config.have_key(key_name) -> bool
"""

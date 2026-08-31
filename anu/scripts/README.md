# anu/scripts — how to run the pipeline

## Prerequisites
- Python 3.10+
- `pip install -r ../requirements.txt` (run from `anu/`)

## Execution order

```bash
python _build_registry.py            # (already run; regenerate if registries change)
python L01_fetch_fred.py --fetch     # per-source fetches (see --list first)
python L02_fetch_bea.py --fetch      # BEA key needed
python L08_load_bundled_inputs.py --fetch   # offline book-period inputs
python P01_construct_series.py --all  # full construction (or --series/--fetcher)
python P02_write_chopped.py           # stage anu/data/final/chopped + MANIFEST.csv
python V01_validate.py --dir ../data/final/chopped
```

`V01_validate.py` with no arguments validates the shipped reference output
(`chopped/` at the repo root) key-free — this is what CI runs.

## What you get
`data/final/chopped/` contains one CSV per producible series (116 of 118; the
other two are formally `data_unavailable`), matching the
`series_registry.json` contract. `data/final/MANIFEST.csv` records sha256,
row counts and year ranges.

## Exit codes
Every script exits non-zero on failure. `V01_validate.py` exits 0 with
warnings (honest gap markers, stale registry coverage) and 1 on any hard
failure (missing series, extra files, null years, non-positive index values,
coverage starts before the declared start).

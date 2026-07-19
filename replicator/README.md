# RSCD Replicator — Shaikh (2016) Replication v1.0

Self-contained reproduction package for the RSCD project: replicates Shaikh's
*Capitalism: Competition, Conflict, Crises* (Oxford, 2016) empirical work
(118 series across 17 chapters + 5 external studies + 9 analytical series),
extended to 2025.

## Quickstart

```bash
# 1. Clone or unpack this directory
cd replicator/

# 2. Set up API keys (FRED required, BEA strongly recommended)
cp config/api_keys.env.example config/api_keys.env
# edit config/api_keys.env  (FRED registration is free, takes 30 seconds)

# 3. Create a clean venv and install
python -m venv .venv
.venv/Scripts/activate          # Windows PowerShell: .\.venv\Scripts\Activate.ps1
# source .venv/bin/activate     # macOS / Linux
pip install -r requirements.txt

# 4. Verify environment
python scripts/replicate.py --health

# 5. Run a single series (smoke test)
python scripts/replicate.py --series S201

# 6. Full pipeline (118 series, ~45 min on clean cache)
python scripts/replicate.py --all

# 7. Summarize results
python scripts/replicate.py --report
```

Outputs land in `data/final/`:
- `data/final/chopped/` — 109 series CSVs (`{SID}.csv`)
- `data/final/extenbooks/` — 109 series XLSX workbooks (`{SID}_extenbook.xlsx`)

The 9 series without chopped output are legitimately data-unavailable
(see `inputs_bundled/series_registry.json` -> per-series `validation_status`).

## What's bundled

| Directory | What | Why bundled |
|-----------|------|-------------|
| `lib/` | Full pipeline code (S00, L01, P02, V03, O06, run.py, utils) | Self-contained execution |
| `inputs_bundled/SalvagedInputs/` | Shaikh's chopped tables + figure metadata + CD2 v1.3 reference | Frozen ground-truth needed by L01 loaders |
| `inputs_bundled/series_registry.json` + sidecars | 118-series schema, subsource metadata, correspondence matrix | Pipeline metadata |
| `config/api_keys.env.example` | Template for FRED/BEA/BLS keys | Required for extension fetching |

## What's NOT bundled (intentional)

- Raw API response caches (`data/raw/`) — populated at run time
- CD / CD2 legacy intermediate frames — 200 MB; replaced by SalvagedInputs subset
- Visualization app (Plotly Dash) — distributed separately in `Publish/`

## Run-time architecture

```
config/api_keys.env  →  FRED_API_KEY, BEA_API_KEY into S00_apis
       ↓
scripts/replicate.py  →  bootstraps workdir/RSCD/Technical/ layout
       ↓                   (symlinks lib/ to Technical/code/,
       ↓                    bundled SalvagedInputs/ to project root)
lib/run.py            →  walks S00 → L01 → P02 → V03 → O06 per series
       ↓
data/raw/             →  API caches (parquet)
data/processed/       →  intermediate frames
data/final/chopped/   →  109 chopped CSVs (the deliverable)
data/final/extenbooks → 109 extension workbooks (XLSX)
```

## Reproducibility guarantee

A clean-venv run on a different machine should produce byte-identical chopped
CSVs for all 109 series, modulo:

1. Vintage drift in FRED/BEA series (some are revised; pipeline pins observation
   end-dates per `series_registry.json` -> `extension_endpoint`)
2. Floating-point representation (IEEE 754 + same numpy/pandas version)
3. Locale (formatter output guards against this; CSVs are locale-neutral)

## Citation

```
Anderson, N. (2026). RSCD: Replication and Extension of Shaikh (2016)
  "Capitalism: Competition, Conflict, Crises". https://github.com/andenick/rscd

Shaikh, A. (2016). Capitalism: Competition, Conflict, Crises.
  Oxford University Press.
```

## License

- Code (lib/, scripts/): MIT
- Data (data/final/, inputs_bundled/SalvagedInputs/ShaikhChoppedTables/): CC-BY-4.0
- See LICENSE in the parent package

## Troubleshooting

- **`FRED_API_KEY missing`** — register at https://fred.stlouisfed.org/, paste
  into `config/api_keys.env`
- **`module 'utils.paths' has no attribute 'X'`** — make sure you're running
  from the replicator/ root with `python scripts/replicate.py`, not from inside
  lib/
- **Network timeouts on first run** — re-run; raw cache picks up where it left
  off
- **Validator FAILs** — expected for 11 series flagged as PASS_DATA_UNAVAILABLE;
  see `--report` output for status semantics

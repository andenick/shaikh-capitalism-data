# RSCD Replicator — Shaikh (2016) Replication v1.6

Self-contained reproduction package for the RSCD project: replicates the empirical
material in Anwar Shaikh's *Capitalism: Competition, Conflict, Crises* (Oxford, 2016)
and extends it to 2025.

- **118 canonical series** (17 book chapters + 5 external studies + 9 analytical
  constructs).
- **113 series are published** (`publish: true`); 5 are withheld (`publish: false`:
  S306, S307, S408, XS2304, XS2305).
- **113 chopped CSVs** and **112 extension workbooks** ship as the deliverable
  (S1006's workbook is withheld — it embeds Ibbotson/SBBI values under copyright;
  S1006's public `-ext` (Damodaran) rows still ship in `chopped/`).

## Quickstart

```bash
# 1. Clone or unpack this directory
cd replicator/

# 2. Set up API keys (extension rows only — book period is fully offline)
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

Outputs land in `data/final/` (re-created on each run; git-ignored):
- `data/final/chopped/` — 113 series CSVs (`{SID}.csv`)
- `data/final/extenbooks/` — 112 series XLSX workbooks (`{SID}_extenbook.xlsx`)

The 5 withheld series (`publish: false`) produce no shipped output. S306 and S307
are genuinely `data_unavailable` (1904 UK working-class budgets not recovered).

## Offline scope (what needs the network)

| Period | Needs a key? | Detail |
|--------|--------------|--------|
| **Book period (1860–2010/11)** | **No** | Every series reproduces offline from the bundled `inputs_bundled/SalvagedInputs/` ground-truth (Shaikh's chopped tables + the S703/S704 digitization packet). |
| **Extension (2011–2025)** | Yes, for ~22 series | These carry an `extension.api` in `series_registry.json`. FRED_API_KEY covers most (10 FRED + 2 combined). BEA_API_KEY is optional (2 BEA series). A handful use Damodaran (NYU), Shiller, IMF (MFS/WEO), IRS-SOI, Census, and World-Bank public endpoints (no key). |

**Inter-series dependencies.** A few composite series read another series'
intermediate frame — e.g. `S1008` (warranted stock price) consumes `S1007`'s
`iropcorp` (real interest rate). These reproduce correctly under `--all`, which
runs dependencies before dependents. A standalone `--series S1008` executed before
`S1007` will report `inputs missing`; this is dependency ordering, **not** an API
requirement (S1008's book period is fully offline).

## Integrity / hash manifest

`MANIFEST_SHA256.txt` records a SHA-256 for every bundled replicator file (code,
inputs, config templates) in standard `sha256sum` format; `MANIFEST_SHA256.json`
carries the summary (`file_count`, `aggregate_sha256`). Verify the package was
transmitted intact before running, from the `replicator/` root:

```bash
sha256sum -c MANIFEST_SHA256.txt        # coreutils

# …or portable Python:
python - <<'PY'
import hashlib, pathlib
bad = []
for line in pathlib.Path("MANIFEST_SHA256.txt").read_text().splitlines():
    want, rel = line.split(None, 1)
    p = pathlib.Path(rel.strip())
    got = hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
    if got != want:
        bad.append(rel.strip())
print("OK" if not bad else f"{len(bad)} mismatched: {bad[:5]}")
PY
```

## What's bundled

| Directory | What | Why bundled |
|-----------|------|-------------|
| `lib/` | Full pipeline code (S00, L01, P02, V03, O06, run.py, utils) | Self-contained execution |
| `inputs_bundled/SalvagedInputs/` | Shaikh's chopped tables + figure metadata + CD2 v1.3 reference | Frozen ground-truth read by L01 loaders |
| `inputs_bundled/remediation_campaign/digitization_packet/` | S703/S704 machine-digitized consensus CSVs + the 1990-omission ruling | Loader-needed source for the two recovered digitizations (offline) |
| `inputs_bundled/series_registry.json` + sidecars | 118-series schema, subsource metadata, correspondence matrix, ledger, validation report | Pipeline metadata |
| `config/api_keys.env.example` | Template for FRED/BEA keys | Required only for extension fetching |

## What's NOT bundled (intentional)

- Raw / processed API caches (`data/raw/`, `data/processed/`) — re-fetched at run time.
- CD / CD2 legacy intermediate frames — replaced by the SalvagedInputs subset.
- Visualization app (Plotly Dash) — interactive exploration is on the project hub.
- Internal build/campaign state (Anu `PIPELINE_STATE.json`, `Build/` step logs) — not
  needed to reproduce data.

## Run-time architecture

```
config/api_keys.env  →  FRED_API_KEY, BEA_API_KEY into S00_apis
       ↓
scripts/replicate.py  →  bootstraps workdir/RSCD/Technical/ layout,
       ↓                  copies registries + SalvagedInputs into place,
       ↓                  wires the S703/S704 digitization packet
lib/run.py            →  walks S00 → L01 → P02 → V03 → O06 per series
       ↓
data/raw/             →  API caches (parquet)
data/processed/       →  intermediate frames (cross-series deps live here)
data/final/chopped/   →  113 chopped CSVs (the deliverable)
data/final/extenbooks → 112 extension workbooks (XLSX)
```

## Reproducibility guarantee

A clean-venv run on a different machine produces byte-identical **book-period**
chopped rows for every published series, modulo:

1. Vintage drift in FRED/BEA extension series (some are revised; the pipeline pins
   observation end-dates per `series_registry.json` → `extension_endpoint`).
2. Floating-point representation (IEEE 754 + same numpy/pandas version).
3. Locale (formatter output is guarded; CSVs are locale-neutral, LF line endings).

## Citation

```
Anderson, N. (2026). RSCD: Replication and Extension of Shaikh (2016)
  "Capitalism: Competition, Conflict, Crises". https://github.com/andenick/shaikh-capitalism-data

Shaikh, A. (2016). Capitalism: Competition, Conflict, Crises.
  Oxford University Press.
```

## License

- Code (lib/, scripts/): MIT
- Data (data/final/, inputs_bundled/SalvagedInputs/ShaikhChoppedTables/): CC-BY-4.0
- See LICENSE in the parent package.

## Troubleshooting

- **`FRED_API_KEY missing`** — register at https://fred.stlouisfed.org/, paste into
  `config/api_keys.env` (only needed for extension rows).
- **`inputs missing` on a single composite series** — run `--all` (or run the
  dependency series first); see "Inter-series dependencies" above.
- **`module 'utils.paths' has no attribute 'X'`** — run from the `replicator/` root
  with `python scripts/replicate.py`, not from inside `lib/`.
- **Network timeouts on first run** — re-run; the raw cache resumes where it left off.
- **Validator status semantics** — `--report` prints per-series verdicts
  (`PASS`, `PASS_THEORETICAL`, `PASS_DATA_UNAVAILABLE`, `extension_only_validated`).

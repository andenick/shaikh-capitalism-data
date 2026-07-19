# RSCD — Replication of Shaikh (2016)

[![Replicator Check](https://github.com/andenick/shaikh-capitalism-data/actions/workflows/replicator_check.yml/badge.svg)](https://github.com/andenick/shaikh-capitalism-data/actions/workflows/replicator_check.yml)
[![License: MIT](https://img.shields.io/badge/Code-MIT-blue.svg)](LICENSE)
[![License: CC BY 4.0](https://img.shields.io/badge/Data-CC--BY--4.0-orange.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-v1.6-green.svg)](CHANGELOG.md)

Open replication and 1860–2025 extension of the empirical material in:

> Shaikh, Anwar (2016). *Capitalism: Competition, Conflict, Crises.* Oxford University Press.

**118 canonical series** across 17 chapters, 5 external studies, and 9 analytical
constructs. **113 series** are in the public bundle (`publish:true` in
`series_registry.json`); 5 are withheld (`publish:false`: `S306`, `S307`, `S408`,
`XS2304`, `XS2305` — non-renderable cross-section stubs or literature-compilation
stubs pending a full reconstruction pass). All 113 published series produce populated
chopped CSVs.

## What's here

```
Publish/
├── README.md                  ← you are here
├── LICENSE                    ← MIT (code) + CC-BY-4.0 (data)
├── CITATION.cff               ← machine-readable citation
├── INSTALL.md                 ← environment setup
├── RELEASE_NOTES_v1.0.md      ← v1.0 changelog + roadmap
├── requirements.txt           ← Python deps
├── series_registry.json       ← canonical 118-series metadata
├── SUBSOURCE_METADATA.json    ← per-source provenance
├── SERIES_CORRESPONDENCE_MATRIX.json   ← Shaikh → modern source crosswalk
├── ANU_LEDGER.json            ← series ledger (status, vintage, owner)
├── VALIDATION_REPORT.json     ← per-series V03 results (MAE, max_abs, n)
├── code/                      ← pipeline (S00, L01, P02, V03, M04, A05, O06)
│   ├── run.py                 ← orchestrator (--series / --health / --report / --gate)
│   ├── S00_setup/             ← config, cache, API clients
│   ├── L01_loaders/           ← 118 per-series loaders
│   ├── P02_processors/        ← 118 per-series constructors
│   ├── V03_validators/        ← 118 per-series validators
│   ├── O06_output/            ← generic chopped + extenbook writers
│   └── utils/paths.py         ← centralized path resolution
├── replicator/                ← self-contained reproduction package
│   ├── scripts/replicate.py   ← clean-venv end-to-end runner
│   ├── lib/                   ← bundled copy of code/
│   ├── inputs_bundled/        ← SalvagedInputs + registries
│   └── MANIFEST_SHA256.txt    ← SHA-256 of every bundled replicator file
├── chopped/                   ← 113 chopped CSVs (the deliverable)
├── extenbooks/                ← 112 extension workbooks (XLSX; S1006 withheld — SBBI value-leak)
├── research/                  ← 112 *_research.json dossiers (verbatim quotes; S1006 withheld)
├── docs/
│   ├── chapters/              ← per-chapter research summaries + adequacy reports
│   ├── series/                ← per-series DPRs + EPRs (226 docs = 113 + 113)
│   │                            (DPR = Data Provenance Record: sources, construction, units;
│   │                             EPR = Extension Provenance Record: post-book extension methodology)
│   ├── decisions/             ← architectural decision records
│   └── methodology/           ← NIPA T7.11 FISIM remap + IFS line→SDMX remap
└── Build/
    ├── BUILD_NARRATIVE.md     ← stage-by-stage chronology
    ├── STEP_LOG.jsonl         ← 1,376 timestamped pipeline events
    ├── PHASE3_VALIDATION_REPORT.json
    ├── PHASE4_VALIDATION_REPORT.json
    └── VIZ_QUALITY_REPORT.json
```

## Quickstart

```bash
git clone https://github.com/andenick/shaikh-capitalism-data.git
cd rscd
python -m venv .venv && .venv/Scripts/activate
pip install -r requirements.txt

# API keys
cp replicator/config/api_keys.env.example replicator/config/api_keys.env
# edit api_keys.env — see INSTALL.md for details:
#   Book-period data (1860–2010): reproduces offline from bundled SalvagedInputs
#                                 for every series — no API key needed.
#   Extension data (2011–2025):   ~22 series pull live modern data. FRED_API_KEY
#                                 (free at fred.stlouisfed.org) covers all but a
#                                 handful; BEA_API_KEY is optional (2 BEA series);
#                                 a few use Damodaran/Shiller/IMF/Census/World-Bank
#                                 public endpoints (no key). See the per-series
#                                 `extension.api` field in series_registry.json.

# Smoke test (single series)
python replicator/scripts/replicate.py --series S201

# Full replication (~45 min; book period offline, extension needs FRED key)
python replicator/scripts/replicate.py --all

# NOTE: a few composite series read another series' intermediate output
# (e.g. S1008 consumes S1007's `iropcorp`). These reproduce under `--all`, which
# runs dependencies first; a standalone `--series S1008` before S1007 will report
# "inputs missing". This is dependency ordering, NOT an API requirement.

# Full validation gate (doctor + anchors + all validators)
python code/run.py --gate
```

Interactive exploration lives on the project hub (see the RSCD study page); the
Plotly Dash app is not shipped in this replication bundle.

See **[INSTALL.md](INSTALL.md)** for detailed environment setup and
**[replicator/README.md](replicator/README.md)** for clean-venv reproduction.

## Headline results

| Metric | Value |
|--------|-------|
| Canonical series | 118 |
| Series in public bundle (publish:true) | 113 |
| Chopped CSVs shipped | 113 |
| Extension workbooks shipped | 112 (S1006 withheld — SBBI value-leak) |
| Research dossiers shipped | 112 (S1006 withheld) |
| Series withheld (publish:false) | 5 (S306, S307, S408, XS2304, XS2305) |
| Series data_unavailable | 2 (S306, S307) |
| Series extension_only_validated (no book-period data) | 2 (S214, S215) |
| Series PASS_THEORETICAL | 8 (no empirical match expected) |
| Verbatim Shaikh quotes in shipped research/ | 112/112 (118/118 canonical) |
| Chapter adequacy gate PASS | 17/17 |
| Mean validation MAE (face-value match) | < 1.5% |
| Visualization QA score | 11/11 PASS (+ 1 N/A) |

## Citation

```bibtex
@misc{anderson2026rscd,
  author = {Anderson, Nicholas},
  title  = {RSCD: Replication and Extension of Shaikh (2016)
            ``Capitalism: Competition, Conflict, Crises''},
  year   = {2026},
  url    = {https://github.com/andenick/shaikh-capitalism-data},
  version = {1.6}
}

@book{shaikh2016capitalism,
  author    = {Shaikh, Anwar},
  title     = {Capitalism: Competition, Conflict, Crises},
  publisher = {Oxford University Press},
  year      = {2016}
}
```

## License

- Code: MIT
- Data: CC-BY-4.0 (require attribution to Shaikh + this repo)

See [LICENSE](LICENSE).

## Predecessor projects

This is the v1.0 rebuild on the Anu Framework v12.0. Earlier prototypes:
- **Capitalism Data (CD)** — 105 series, Anu v4.x, frozen 2025
- **Capitalism Data v2 (CD2)** — 114 series, Anu v6.0, frozen 2026-04

Crosswalks: `MIGRATION/CD_to_RSCD_crosswalk.csv`, `MIGRATION/CD2_to_RSCD_crosswalk.csv`

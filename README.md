# RSCD — Replication of Shaikh (2016)

[![License: MIT](https://img.shields.io/badge/Code-MIT-blue.svg)](LICENSE)
[![License: CC BY 4.0](https://img.shields.io/badge/Data-CC--BY--4.0-orange.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-v1.0-green.svg)](RELEASE_NOTES_v1.0.md)

Open replication and 1860–2025 extension of the empirical material in:

> Shaikh, Anwar (2016). *Capitalism: Competition, Conflict, Crises.* Oxford University Press.

**118 series** across 17 chapters, 5 external studies, and 9 analytical
constructs. 109 producible chopped CSVs; the remaining 9 are formally classified
`PASS_DATA_UNAVAILABLE` or `PASS_THEORETICAL` (see VALIDATION_REPORT.json).

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
├── PIPELINE_STATE.json        ← stage progression (v1.0 = stage_8 complete)
├── ANU_LEDGER.json            ← series ledger (status, vintage, owner)
├── VALIDATION_REPORT.json     ← per-series V03 results (MAE, max_abs, n)
├── code/                      ← pipeline (S00, L01, P02, V03, M04, A05, O06)
│   ├── run.py                 ← orchestrator (--series / --health / --report)
│   ├── S00_setup/             ← config, cache, API clients
│   ├── L01_loaders/           ← 118 per-series loaders
│   ├── P02_processors/        ← 118 per-series constructors
│   ├── V03_validators/        ← 118 per-series validators
│   ├── O06_output/            ← generic chopped + extenbook writers
│   └── utils/paths.py         ← centralized path resolution
├── viz/                       ← Plotly Dash app
│   ├── app.py                 ← entrypoint
│   ├── data_loader.py
│   └── chart_builder.py
├── replicator/                ← self-contained reproduction package
│   ├── scripts/replicate.py   ← clean-venv end-to-end runner
│   ├── lib/                   ← bundled copy of code/
│   └── inputs_bundled/        ← SalvagedInputs + registries
├── chopped/                   ← 109 chopped CSVs (the deliverable)
├── extenbooks/                ← 109 extension workbooks (XLSX)
├── research/                  ← 118 *_research.json dossiers (verbatim quotes)
├── docs/
│   ├── chapters/              ← per-chapter research summaries + adequacy reports
│   ├── series/                ← per-series DPRs + EPRs (236 docs)
│   ├── decisions/             ← 6 architectural decision records
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
git clone https://github.com/andenick/rscd.git
cd rscd
python -m venv .venv && .venv/Scripts/activate
pip install -r requirements.txt

# API keys
cp replicator/config/api_keys.env.example replicator/config/api_keys.env
# edit FRED_API_KEY (and optionally BEA_API_KEY)

# Smoke test (single series)
python replicator/scripts/replicate.py --series S201

# Full replication (~45 min)
python replicator/scripts/replicate.py --all

# Browse interactively
python viz/app.py     # http://127.0.0.1:8050
```

See **[INSTALL.md](INSTALL.md)** for detailed environment setup and
**[replicator/README.md](replicator/README.md)** for clean-venv reproduction.

## Headline results

| Metric | Value |
|--------|-------|
| Series authored | 118 |
| Series producing chopped output | 109 |
| Series PASS_DATA_UNAVAILABLE | 11 (S801, S703, S704, S707, S708, S214, S215, S404, ES2306, plus 2 others) |
| Series PASS_THEORETICAL | 8 (no empirical match expected) |
| Verbatim Shaikh quotes in research/ | 118/118 |
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
  url    = {https://github.com/andenick/rscd},
  version = {1.0}
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

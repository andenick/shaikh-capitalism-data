# RSCD — Install Guide

## Requirements

- Python 3.11 or later
- ~5 GB free disk for raw API caches
- ~500 MB for chopped outputs and extenbooks
- API keys: FRED (free), BEA (free), BLS (free, optional)

## Setup

```bash
cd D:/Arcanum/Projects/RSCD/Technical
python -m venv .venv
.venv/Scripts/activate    # Windows
pip install -r requirements.txt
```

## API Keys

Copy the template and fill in your keys:

```bash
cp config/api_keys.env.template config/api_keys.env
# then edit config/api_keys.env to add your FRED_API_KEY, BEA_API_KEY etc.
```

Alternatively, set them as environment variables — `S00_config.load()` reads
`api_keys.env` without overwriting anything already in the process environment.

| API | Register (Free) | Required For |
|-----|----------------|--------------|
| **FRED** | https://fred.stlouisfed.org/docs/api/api_key.html | Ch2 extensions (INDPRO, UNRATE, M1, M2, etc.) |
| **BEA** | https://apps.bea.gov/api/signup/ | Ch5–6 profit rate chain (NIPA tables) |
| **BLS** | https://data.bls.gov/registrationEngine/ | Optional (industry-level) |
| **World Bank** | No key | International comparisons |
| **MeasuringWorth** | No key | Pre-1860 historical |

The pipeline degrades gracefully if optional keys are missing.

## Health Check

```bash
python code/run.py --health
```

Expected output: all imports succeed, all API keys present, `Inputs/` paths
resolve, `series_registry.json` parses, ANU_LEDGER schema valid.

## First Run

```bash
python code/run.py --list                 # enumerate every script
python code/run.py --validate-only        # run all V03 validators
python code/run.py --series S201          # single series end-to-end
python code/run.py --chapter 2            # all series in chapter 2
```

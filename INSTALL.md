# Installation Guide

## Prerequisites

- **Python 3.10+**
- **pip** (Python package manager)

## Step 1: Clone the repository

```bash
git clone https://github.com/andenick/shaikh-capitalism-data.git
cd shaikh-capitalism-data
```

## Step 2: Install dependencies

```bash
pip install -r requirements.txt
```

## Step 3: API keys (optional)

API keys are needed only for fetching live data from government statistical agencies. All keys are free.

```bash
cp config/api_keys.env.example config/api_keys.env
```

Edit `config/api_keys.env` with your keys:

| API | Register | Used For |
|-----|----------|----------|
| **FRED** | [fred.stlouisfed.org/docs/api/api_key.html](https://fred.stlouisfed.org/docs/api/api_key.html) | Industrial production, unemployment, interest rates, compensation |
| **BEA** | [apps.bea.gov/api/signup](https://apps.bea.gov/api/signup/) | Profit rates, GDP by industry, fixed assets |

The World Bank, OECD, and Maddison APIs do not require keys.

## Step 4: Run the pipeline

```bash
python replicate.py                    # Full pipeline
python replicate.py --chapter 2       # Single chapter
python replicate.py --dry-run         # Show plan without executing
```

## Troubleshooting

**Import errors**: Ensure you're using Python 3.10+. Check with `python --version`.

**API timeouts**: FRED and BEA APIs occasionally have maintenance windows. Retry after a few minutes. The pipeline degrades gracefully — it warns but doesn't crash if a key is missing.

**Missing data files**: The `data/inputs/` directory contains all source data. If files are missing, re-clone the repository.

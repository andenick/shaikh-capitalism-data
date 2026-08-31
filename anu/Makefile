.PHONY: registry fetch list construct chopped validate check all clean

registry:
	python scripts/_build_registry.py

list:
	@for s in scripts/L0*_*.py; do echo "== $$s"; python $$s --list | head -5; done

fetch-fred:
	python scripts/L01_fetch_fred.py --fetch

fetch-bea:
	python scripts/L02_fetch_bea.py --fetch

fetch-worldbank:
	python scripts/L03_fetch_worldbank.py --fetch

fetch-imf:
	python scripts/L04_fetch_imf_weo.py --fetch

fetch-census:
	python scripts/L05_fetch_census_ft900.py --fetch

fetch-shiller:
	python scripts/L06_fetch_shiller.py --fetch

fetch-damodaran:
	python scripts/L07_fetch_damodaran.py --fetch

fetch-bundled:
	python scripts/L08_load_bundled_inputs.py --fetch

construct:
	python scripts/P01_construct_series.py --all

chopped:
	python scripts/P02_write_chopped.py

validate:
	python scripts/V01_validate.py

# Key-free: regenerate the registry and gate the shipped reference output
check: registry validate

all: construct chopped
	python scripts/V01_validate.py --dir data/final/chopped

clean:
	rm -rf data/raw data/processed data/final

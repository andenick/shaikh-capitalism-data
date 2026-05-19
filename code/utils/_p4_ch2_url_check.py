"""
One-shot URL reachability scan for Ch2 adequacy review.

Performs HTTP HEAD (falls back to GET on 405/501) with a 10s timeout
and an explicit User-Agent. Prints CSV-like rows to stdout so the
reviewer can paste status codes into the adequacy report.
"""
from __future__ import annotations

import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

UA = "Mozilla/5.0 (compatible; RSCD-Phase4-AdequacyBot/1.0; +rscd-replication)"

URLS: list[tuple[str, str, str]] = [
    ("S201", "primary", "https://www.federalreserve.gov/releases/g17/"),
    ("S201", "extension_FRED", "https://fred.stlouisfed.org/series/INDPRO"),
    ("S202", "primary", "https://apps.bea.gov/iTable/?reqid=10"),
    ("S202", "extension_FRED", "https://fred.stlouisfed.org/series/GPDIC1"),
    ("S202", "extension_BEA_NIPA", "https://apps.bea.gov/iTable/?reqid=19&step=2&isuri=1&categories=survey"),
    ("S203", "primary", "https://www.measuringworth.com/datasets/usgdp/"),
    ("S203", "extension", "https://www.measuringworth.com/datasets/usgdp/"),
    ("S204", "primary_hathitrust", "https://catalog.hathitrust.org/Record/001141928"),
    ("S205", "primary_hathitrust", "https://catalog.hathitrust.org/Record/001141928"),
    ("S206", "primary_hathitrust", "https://catalog.hathitrust.org/Record/001141928"),
    ("S207", "primary_mw_comp", "https://www.measuringworth.com/datasets/uscompensation/"),
    ("S207", "extension_FRED_OPHMFG", "https://fred.stlouisfed.org/series/OPHMFG"),
    ("S208", "primary_BLS_lpc", "https://www.bls.gov/lpc/"),
    ("S208", "extension_FRED_ULCMFG", "https://fred.stlouisfed.org/series/ULCMFG"),
    ("S208", "extension_FRED_OPHMFG", "https://fred.stlouisfed.org/series/OPHMFG"),
    ("S209", "primary_govinfo_ERP", "https://www.govinfo.gov/app/collection/erp"),
    ("S209", "extension_FRED_UNRATE", "https://fred.stlouisfed.org/series/UNRATE"),
    ("S210", "primary_MW_gold", "https://www.measuringworth.com/datasets/gold/"),
    ("S210", "extension_FRED_PPIACO", "https://fred.stlouisfed.org/series/PPIACO"),
    ("S210", "extension_ONS_PLLU", "https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/pllu/mm22"),
    ("S211", "primary_hathitrust", "https://catalog.hathitrust.org/Record/000404889"),
    ("S212", "primary_MW_gold", "https://www.measuringworth.com/datasets/gold/"),
    ("S212", "extension_MW_gold", "https://www.measuringworth.com/datasets/gold/"),
    ("S213", "primary_BEA_iTable", "https://apps.bea.gov/iTable/?reqid=19"),
    ("S213", "extension_BEA_iTable", "https://apps.bea.gov/iTable/?reqid=19"),
    ("S214", "primary_OECD_STAT", "https://stats.oecd.org/"),
    ("S214", "extension_OECD_STAN", "https://stats.oecd.org/Index.aspx?DataSetCode=STAN"),
    ("S215", "primary_OECD_STAN", "https://stats.oecd.org/Index.aspx?DataSetCode=STAN"),
    ("S215", "extension_AMECO", "https://economy-finance.ec.europa.eu/economic-research-and-databases/economic-databases/ameco-database_en"),
    ("S216", "primary_BEA_IO", "https://apps.bea.gov/iTable/?reqid=151"),
    ("S216", "extension_BEA_IO_zip", "https://apps.bea.gov/industry/Release/XLS/IOUse_Before_Redefinitions_Summary.zip"),
    ("S217", "primary_Maddison_GGDC", "https://www.rug.nl/ggdc/historicaldevelopment/maddison/"),
    ("S217", "extension_MPD2023", "https://www.rug.nl/ggdc/historicaldevelopment/maddison/releases/maddison-project-database-2023"),
    ("S218", "primary_Maddison_GGDC", "https://www.rug.nl/ggdc/historicaldevelopment/maddison/"),
    ("S218", "extension_MPD2023", "https://www.rug.nl/ggdc/historicaldevelopment/maddison/releases/maddison-project-database-2023"),
]


def check(url: str) -> tuple[str, str]:
    """Return (status_code_string, note)."""
    req = urllib.request.Request(url, headers={"User-Agent": UA}, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return (str(r.status), r.headers.get("Content-Type", ""))
    except urllib.error.HTTPError as e:
        if e.code in (405, 501):
            # try GET
            req2 = urllib.request.Request(url, headers={"User-Agent": UA}, method="GET")
            try:
                with urllib.request.urlopen(req2, timeout=10) as r:
                    return (str(r.status), r.headers.get("Content-Type", "") + " [GET-fallback]")
            except Exception as e2:
                return (f"HTTP_GET_ERR_{type(e2).__name__}", str(e2)[:120])
        return (f"HTTP_{e.code}", e.reason or "")
    except urllib.error.URLError as e:
        return ("URLError", str(e.reason)[:120])
    except TimeoutError as e:
        return ("Timeout", str(e)[:120])
    except Exception as e:
        return (f"ERR_{type(e).__name__}", str(e)[:120])


def main():
    results = []
    for sid, role, url in URLS:
        status, note = check(url)
        print(f"{sid}\t{role}\t{status}\t{url}\t{note}")
        results.append({"sid": sid, "role": role, "url": url, "status": status, "note": note})
        time.sleep(0.3)
    out = Path(__file__).resolve().parents[2] / "Build" / "ch2_url_check.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nWrote: {out}", file=sys.stderr)


if __name__ == "__main__":
    main()

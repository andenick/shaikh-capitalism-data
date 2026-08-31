# D04: IMF — Data Provenance Record

## What this covers
International Monetary Fund inputs (World Economic Outlook, IFS, Monetary
Financial Statistics) plus the BLS International Labor Comparisons workbooks
they are paired with, used by the Chapter 11 price-competitiveness material
and the China external-study series. Serves 14 series.

## Source
- **Name**: IMF (WEO / IFS / MFS) and BLS International Labor Comparisons
- **URLs**:
  - https://www.imf.org/external/datamapper/api/v1/BCA/CHN
  - https://www.imf.org/external/datamapper/api/v1/BCA_NGDPD/CHN
  - https://data.imf.org/ (IFS / MFS endpoints)
  - https://www.bls.gov/ilc/
- **License**: IMF terms permit research replication with attribution; BLS
  ILC is U.S. government public domain
- **Retrieved**: API subsources fetched at run time (open, no key); appendix
  workbook material is bundled
- **Format**: JSON API; salvaged workbooks

## Subsources served
| Subsource | What it is | Fetch mode |
|---|---|---|
| IMF_WEO_BCA_CHN | WEO current account balance, China (BoP, USD) | open API |
| IMF_WEO_BCA_NGDPD_CHN | WEO current account, % of GDP, China | open API |
| IMF_MFS_DC_DCORP_N_DC | MFS domestic credit breakdown | API |
| IMF_IFS_XM_APPENDIX_11_1 | IFS exports/imports for Ch. 11 | bundled transcription |
| BLS_ILC_REER_PPI_APPENDIX_11_1 | BLS ILC real effective exchange rate (PPI basis) | bundled workbook |
| BLS_ILC_LOP_RATIO_APPENDIX_11_1 | BLS ILC law-of-one-price ratio | bundled workbook |
| SHAIKH_2016_APPENDIX_15_1 | Shaikh's Appendix 15.1 working spreadsheet | bundled |
| SHAIKH_APPENDIX_16_2 | Shaikh's appendix 16.2 series (originally on anwarshaikhecon.org, now offline) | bundled |

## Construction method
Open-API subsources are fetched by the shared clients with TTL caching and
annualised where needed; the Ch. 11 cross-country material is loaded from the
bundled workbooks because BLS ILC was discontinued and the IFS vintages used
in the book are no longer retrievable.

## Transformations applied
- percent-of-GDP vs BoP-USD unit alignment (both served; per-subseries units)
- splice anchors documented per series in the registry

## Known issues
- anwarshaikhecon.org is offline; its workbooks are preserved in the bundled
  inputs with Wayback Machine provenance.
- WEO figures are revised twice yearly; vintage drift is expected.

## Validation
V03 spot-checks; V01 package gate.

## Series served
See `python anu/scripts/L04_fetch_imf_weo.py --list`.

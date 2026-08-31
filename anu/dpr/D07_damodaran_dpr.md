# D07: Damodaran (NYU Stern) — Data Provenance Record

## What this covers
Aswath Damodaran's posted historical-return datasets (annual returns on
stocks, long-term government bonds and Baa corporate bonds) feeding the
Chapter 10 bond/equity total-return series. Serves 1 series.

## Source
- **Name**: Aswath Damodaran, NYU Stern
- **URL**: https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/histretSP.html
- **License**: open academic (freely posted by the author)
- **Retrieved**: at run time (HTML scrape, cached)
- **Format**: HTML table

## Construction method
The Damodaran client (`S00_apis.damodaran_histret`) parses the historical
returns table and annualises to the book's convention. Book-period values
match the vintages used by Shaikh; extensions append new years as posted.

## Subservices
DAMODARAN_rslarge (stocks), DAMODARAN_rbcorplt_Baa (Baa corporates),
DAMODARAN_rbgovlt (long governments).

## Transformations applied
- percent → decimal where registry units are decimal
- chaining of annual total returns where the series is a cumulative index

## Known issues
- The page layout changes occasionally; the parser is defensive and cached.

## Validation
V03 spot-checks; V01 package gate.

## Series served
See `python anu/scripts/L07_fetch_damodaran.py --list`.

# Shaikh Chopped Tables

## CRITICAL: DO NOT MODIFY THESE FILES

These 72 xlsx files contain Anwar Shaikh's original data from 
"Capitalism: Competition, Conflict, Crises" (2016).

They are the **authoritative source** for all data replication.

---

## File Naming Convention

```
Appendix{N}_{TableName}.xlsx
```

Examples:
- `Appendix6_Table68II7.xlsx` - Chapter 6, Appendix Table 6.8.II.7
- `Appendix2_IndustrialProduction.xlsx` - Chapter 2, Industrial Production data
- `Appendix9_1998Fixed.xlsx` - Chapter 9, Fixed Capital I-O Analysis for 1998

---

## File Structure Patterns

### Pattern A: Standard Time Series (Most Common)

```
Row 0: Metadata - Source citations, methods, base years, splicing info
Row 1: Headers - Variable names (Year, Column1, Column2, ...)
Row 2+: Data - Year-indexed values
```

Example (Appendix2_IndustrialProduction.xlsx):
```
Row 0: "INDUSTRIAL PRODUCTION, U.S.: 1860-present_Spliced at 1919..."
Row 1: Year | IndProdHS_BEA | IndProd_FRB | IndProd_Final
Row 2: 1860 | 2.3 | NaN | 2.3
...
```

### Pattern B: Wide Table Format

```
Row 0: Table title and description
Row 1: Table | Description | Source | Variable | 1947 | 1948 | ...
Row 2+: Data rows with years as columns
```

Example (Appendix6_Table68I2.xlsx):
```
Row 0: "Appendix Table 6.8.I.2: Measures of Aggregate Profits..."
Row 1: Table | Description | Source | Variable | 1947 | 1948 | ...
Row 2: Noncorporate | Proprietors Income | T 1.13, line 23 | PropInc | 34.5 | 39.2 | ...
```

### Pattern C: Cross-Section/Matrix Data

```
Row 0: Calculation file reference and observed parameters
Row 1: Index | Market Prices | Direct Prices | Labor Values | ...
Row 2+: Industry-indexed values
```

Example (Appendix9_1998Fixed.xlsx):
```
Row 0: "LTVCalc1998stdREadjFixed.xmcd | r observed = 0.1258"
Row 1: Index | tpm | td | tv | tp(r) | ...
Row 2: 1 | 207859 | 157562 | 2792 | 3852 | ...
```

---

## Metadata Extraction Guide

### Source Citations Found in Row 0:

| Pattern | Meaning |
|---------|---------|
| `T 1.14, line 7` | NIPA Table 1.14, Line 7 |
| `BEA, FA Table 6.1` | Fixed Assets Table 6.1 |
| `FRED, G-17` | Federal Reserve Industrial Production |
| `Long Term Eco Growth` | BEA Historical Statistics (1973) |
| `Jastram (1977)` | Book citation with year |
| `MeasuringWorth.com` | Historical economics database |
| `Ibbotson SBBI` | Stock/Bond returns yearbook |
| `Shiller` | Robert Shiller's historical data |

### Splicing Information:

Many series are spliced from multiple sources:
```
"Spliced at 1919: HS series 1860-1918, FRB series 1919-2010"
```

This means:
- 1860-1918: Historical Statistics (BEA 1973)
- 1919-2010: Federal Reserve Board G-17

---

## Files by Chapter

### Chapter 2 - Turbulent Trends (8 files)
- Appendix2_Ayres.xlsx - Business cycles (Ayres 1939)
- Appendix2_GDPperCapita.xlsx - Per capita GDP with interpolations
- Appendix2_IndustrialProduction.xlsx - Industrial production 1860-2010
- Appendix2_ManufacturingProductivity.xlsx - Manufacturing productivity
- Appendix2_ManufacturingProductivityAndRealWages1889-2010.xlsx
- Appendix2_MeasuringWorthGDP_1889-2010.xlsx
- Appendix2_RealInvestmentUS_1832-2010.xlsx
- Appendix2_Unemployment.xlsx - Unemployment 1890-2010

### Chapter 5 - Exchange, Money, Price (2 files)
- Appendix5_DATALRprices.xlsx - Long-run price data
- Appendix5_Documentation.xlsx - Documentation

### Chapter 6 - Capital and Profit (11 files) - CRITICAL
- Appendix6_Contents.xlsx - Table of contents
- Appendix6_Table68I1.xlsx - Business sector measurement
- Appendix6_Table68I2.xlsx - Aggregate profits measures
- Appendix6_Table68I3.xlsx - Corrected business accounts
- Appendix6_Table68II1.xlsx - GPIM capital stock accuracy
- Appendix6_Table68II2.xlsx - Initial value effects
- Appendix6_Table68II3.xlsx - Depletion rate effects
- Appendix6_Table68II4.xlsx - Great Depression/WWII effects
- Appendix6_Table68II5.xlsx - Net and gross stocks
- Appendix6_Table68II6.xlsx - Corporate inventories
- Appendix6_Table68II7.xlsx - **Final profit rates** (MOST IMPORTANT)

### Chapter 7 - Real Competition (8 files)
- Appendix7_ropdataUSind.xlsx - Average profit rates by industry
- Appendix7_iropdataUSind.xlsx - Incremental profit rates by industry
- Appendix7_iropOECDPPP.xlsx - OECD incremental profit rates
- Appendix7_SalterTable9.xlsx, SalterTable10.xlsx - Salter data
- Appendix7_SalterULCPriceTable28.xlsx, SalterULCPriceTable33.xlsx

### Chapter 8 - Perfect vs Imperfect Competition (6 files)
- Appendix8_Bain42IndustryProfit.xlsx - Bain industry profits
- Appendix8_CorrectedBainData.xlsx - Corrected Bain data
- Appendix8_DemsetzRatesOfReturn.xlsx - Demsetz returns
- Appendix8_StiglerRatesOfProfit.xlsx - Stigler profits
- Appendix8_Semmler19843.3.xlsx - Semmler data

### Chapter 9 - Relative Prices (14 files)
- Appendix9_1947fixed.xlsx through Appendix9_1998Fixed.xlsx - I-O analyses
- Appendix9_1998Circ.xlsx - Circulating capital model
- Appendix9_ObservedProfitRates.xlsx - Observed rates
- Appendix9_PennWorldTables.xlsx - International comparisons
- Appendix9_pvdevexample.xlsx - Price-value deviation example
- Appendix9_ReswitchExamples.xlsx - Reswitching examples

### Chapter 10 - Finance and Interest (4 files)
- Appendix10_Ibbotson.xlsx - SBBI returns data
- Appendix10_IntroPPrice.xlsx - Interest rate data
- Appendix10_USLR.xlsx - Long-run interest rates

### Chapter 11 - International Competition (3 files)
- Appendix11_USJPNdata.xlsx - US-Japan comparison
- Appendix11_XMData.xlsx - Trade data

### Chapter 12 - Macroeconomics (1 file)
- Appendix12_CreditInflUnempl.xlsx - Credit, inflation, unemployment

### Chapter 14 - Wages and Unemployment (2 files)
- Appendix14_InflationULdata.xlsx - Inflation and labor data

### Chapter 15 - Money and Inflation (7 files)
- Appendix15_Argentina.xlsx - Argentina inflation
- Appendix15_MeasuringWorthCPI.xlsx - Historical CPI
- Appendix15_USInflation.xlsx - US inflation data
- Appendix15_WorldInflationDataByCountry.xlsx - World inflation

### Chapter 16 - Growth, Profitability, Crises (5 files)
- Appendix16_ProfitRates.xlsx - Profit rate data
- Appendix16_DebtIncRatio.xlsx - Debt-income ratios
- Appendix16_HouseholdDebtService.xlsx - Household debt
- Appendix16_WageProdData.xlsx - Wage-productivity data

### Chapter 17 - Summary (1 file)
- Appendix17_USIRS2011.xlsx - IRS income data

---

## Absorbed Data Location

All data has been extracted to:
```
Technical/ShinyApp/data/ShaikhAbsorbed/
├── SHAIKH_MASTER_CATALOG.csv   (1,587 series cataloged)
├── SHAIKH_SOURCES.json         (72 files with metadata)
└── chapter_NN_data.csv         (Per-chapter data extracts)
```

---

*This folder is READ-ONLY. All processing outputs go to Technical/ or Output/*
*Last absorption: December 12, 2025 - 48,071 data points extracted*


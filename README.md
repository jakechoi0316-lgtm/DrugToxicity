# BC Unregulated Drug Deaths – Extracted Data

**Source:** BC Coroners Service, Unregulated Drug Toxicity Deaths dashboard.
Data up to end of June 2026, last refreshed 11 Aug 2026.
Questions to the source: BCCS.Stats@gov.bc.ca

All files are in long ("tidy") format: one row per region per time period.
This format loads straight into Python (pandas), R, Power BI or Excel.

## Files

| File | What it holds | Years |
|---|---|---|
| **hsda_yearly.csv** | Deaths, population and rate per 100k by HSDA. **Main file for the map.** | 2015–2026 |
| population_hsda.csv | BC Stats population by HSDA, female / male / total | 2015–2026 |
| population_ha.csv | BC Stats population by health authority | 2015–2025 |
| **hsda_monthly.csv** | Deaths and monthly rate by HSDA | Jun 2025–Jun 2026 |
| ha_yearly.csv | Deaths and rate by health authority, plus BC total | 2015–2026 |
| ha_monthly.csv | Deaths and monthly rate by health authority, plus BC | Jun 2025–Jun 2026 |
| bc_monthly.csv | BC deaths by month | 2015–2026 |
| lha_yearly.csv | Deaths and rate by Local Health Area (LHA) | 2016–2026 |
| township_yearly.csv | Deaths by township (top 17 plus "Other") | 2015–2026 |
| age_group_yearly_bc.csv | BC deaths and rate by age group | 2015–2026 |
| sex_yearly_by_ha.csv | Deaths and rate by sex, BC and each HA | 2015–2026 |
| place_of_injury_by_ha.csv | Deaths by place of injury, BC and each HA | 2023–2026 |
| drugs_involved_by_ha.csv | % of deaths with each drug type involved | 2015–2025 |
| fentanyl_detected_by_ha.csv | % of deaths with fentanyl detected | 2015–2026 |
| expedited_tox_monthly_by_ha.csv | % of tested deaths with each drug type | Jul 2025–Jun 2026 |
| income_assistance_day_bc.csv | Average deaths per day, payday week vs other days | 2016–2026 |

## Key columns

- `hsda_code` – standard BC HSDA code (11–53). Use this to join to the HSDA boundary file. Check the codes match the boundary file.
- `months_covered` – 12 for full years, **6 for 2026** (Jan–Jun only).
- `rate_per_100k` – deaths per 100,000 people. **2026 rates are annualized** (`rate_annualized = yes`), so you can compare them with full years.
- `rate_per_100k_month` – monthly rate, **not** annualized. Multiply by 12 to compare with yearly rates.

## Things to know

1. **Population comes from BC Stats P.E.O.P.L.E.** (released May 20, 2026), the same source the dashboard uses. 2015–2025 are estimates; **2026 is a projection** (`population_type`). Deaths ÷ population reproduces every dashboard rate (yearly and monthly).
2. **2026 is half a year and preliminary.** Numbers change as investigations close. The source says to read 2026 rates with caution.
3. **Monthly data only covers 13 months.** The dashboard only shows a rolling 13-month window. Older months by region are not in this snapshot.
4. **Blanks in monthly and age tables = 0.** The dashboard leaves a cell empty when the count is 0. The totals confirm this, so these are stored as 0.
5. **Blanks in the LHA table = suppressed.** Small counts are hidden for privacy. They are left empty, with `value_status` = "blank in source (suppressed)".
6. **LHA totals can be 1–3 lower than HSDA totals.** BCCDC prepares the LHA data, and a few deaths cannot be placed in an LHA. The gap is always small and always in the same direction.
7. **Place of injury per HA was derived.** In the snapshot, each filtered page showed "all of BC except one HA". Each HA's numbers were calculated as BC minus that page. The results add up exactly to each HA's total.
8. **Some LHA year positions were read from the image layout.** Haida Gwaii and Stikine and Snow Country have many blank cells. The `row_note` column flags them. Peace River South and Fort Nelson were confirmed using Northeast totals.
9. **Not in this snapshot:** Fentanyl Concentration (p.13), Expedited Tox 2 (p.15), Mode of Consumption (p.16), Occupation Industry (p.18). Also missing: the Carfentanil, Xylazine and Medetomidine views on p.12, and monthly views for age, sex and township.

## Quality checks

Run `python build_data.py`, then `python add_population.py` (in that order; the second adds population to `hsda_yearly.csv`). Together they run **3,232 checks**. All pass, for example:
- Female + male = total population, and HSDA populations add up to each health authority.
- Deaths ÷ population matches the dashboard rate for all 192 HSDA-years and 208 HSDA-months.
- HSDAs add up to each HA, and HAs add up to BC, for every year and month.
- Jan–Jun 2026 months add up to the 2026 yearly totals.
- Age groups, sex, townships and place of injury add up to the published totals.
- Each filtered page matches the HA it claims to show.

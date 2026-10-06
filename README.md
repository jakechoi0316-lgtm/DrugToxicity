# BC Drug Harms Map

**Live map:** `https://<your-username>.github.io/<repo-name>/` *(replace with your GitHub Pages link)*

A map of BC's 16 health regions that puts **drug harm** (deaths, paramedic-attended overdoses) and **support** (naloxone sites and kits) side by side. It helps non-profit outreach teams send limited resources where they are most likely to prevent deaths.

---

## Job story

> **When** I am deciding, for a non-profit, where to send outreach staff and naloxone supplies each month,
> **I want** to see in one place which regions have high overdose harm but few support services,
> **So that I can** put limited resources where they are most likely to prevent deaths.

## Main proposition

**One map that shows where harm is high and support is thin, so limited resources go where they save the most lives.**

- **The problem we solve:** outreach resources are limited, and people keep dying. Teams need to know where to send supplies first.
- **Our goal:** help teams use the same resources more efficiently, by matching supplies to need.

---

## 1. Problem evidence

| Fact | Number | Source |
|---|---|---|
| Deaths from unregulated drugs, Jan 2016 – Jun 2026 | **about 19,000** | BC Coroners Service |
| Deaths in 2025 | **1,828** (about **5 per day**) | BC Coroners Service |
| Peak year | 2,591 deaths (2023) | BC Coroners Service |
| Gap between highest and lowest region, 2025 | **55.5 vs 9.6** per 100,000 (5.8×) | BC Coroners Service, BC Stats |
| Take-home naloxone kits shipped in BC, 2025 | **375,183** (down 22% from 484,000 in 2024) | BCCDC |

**Supplies are not matched to need.** In 2025, the number of naloxone kits shipped for each paramedic-attended overdose varied **more than 5 times** between regions:

| Region (2025) | Deaths per 100k | Paramedic overdoses per 100k | Kits shipped | Kits per overdose |
|---|---:|---:|---:|---:|
| **Fraser East** | 36.0 | 583 | 19,363 | **9.0** (lowest) |
| Fraser South | 24.0 | 259 | 38,031 | 13.9 |
| Vancouver | 55.0 | 729 | 89,662 | 16.1 |
| *BC overall* | *32.1* | *359* | *375,183* | *18.3* |
| Northern Interior | 55.5 | 550 | 23,229 | 27.3 |
| Northwest | 43.1 | 237 | 8,752 | 46.8 |
| **Richmond** | 9.6 | 71 | 8,175 | **48.4** (highest) |

Fraser East has the **2nd-highest** overdose rate in BC (after Vancouver) but receives the **fewest kits per overdose**. Richmond has the **lowest** death rate but receives the **most kits per overdose**. Full table for all 16 regions: [`evidence_2025_by_region.csv`](evidence_2025_by_region.csv).

> Kits are counted by the address of the site they were shipped to. Kits can be carried and used in other regions.

---

## 2. Data evidence

All data is **public, aggregated** (no personal information), and **already downloaded** into this repo.

| Data | Source | Level | Years |
|---|---|---|---|
| Drug deaths | BC Coroners Service dashboard | 16 regions, by month | 2015 – Jun 2026 |
| Paramedic-attended opioid overdoses | BCCDC dashboard (BC Emergency Health Services) | 16 regions, by month | 2015 – Jul 2026 |
| Naloxone sites and kits shipped | BCCDC dashboard (Take Home Naloxone Program) | 16 regions, by month | 2015 – Jul 2026 |
| Opioid agonist treatment clients | BCCDC dashboard | 16 regions, by month | 2015 – Jun 2026 |
| Population | BC Stats (P.E.O.P.L.E.) | 16 regions, by year | 2015 – 2026 |
| Region boundaries | BC Geographic Warehouse | 16 regions | 2022 boundaries |

**Quality checks we ran**
- Deaths from two separate sources (Coroners Service and BCCDC) **match exactly** for all 192 region-years.
- Our calculated rates (deaths ÷ population) **match the official published rates** for every region, year and month.
- 3,000+ automated checks in `build_data.py` and `add_population.py`. All pass.

**Known limits**
- 2026 is part of the year only (Jan–Jun or Jan–Jul) and preliminary.
- Paramedic-attended overdoses nearly doubled from mid-2025 into 2026 while deaths fell. **We have not yet confirmed** whether this is real or a change in how BCCDC counts them.
- Overdose prevention site data is only available for the 5 health authorities, not the 16 regions.
- Small regions can change a lot from year to year.

See [`DATA.md`](DATA.md) for every file and column.

---

## 3. What we built so far

An interactive map ([`index.html`](index.html)) with a year slider (2015–2026) and four views:
1. **Deaths** per 100,000 people
2. **Paramedic overdoses** per 100,000 people
3. **Naloxone sites** per 100,000 people
4. **Gap:** flags regions with **more overdoses and fewer naloxone sites** than the BC rate. In 2024–2026 this is **Okanagan**.

---

## 4. Why this is different

We did not find a public tool that puts harm and supplies side by side by region. Each existing source answers only part of the question:

| Source | What it has | What is missing |
|---|---|---|
| BC Coroners Service dashboard | Deaths | No services or supplies |
| BCCDC dashboard | Harms and services | Each on a separate page; no combined comparison |
| BC Stats | Population | No health data |

**What we add**
- **Harm and supplies in one view**, for the same region and year.
- **A direct answer:** the gap view and kits-per-overdose show where supplies fall short of need.
- **Fair comparison:** everything is per 100,000 people or per overdose, compared with the BC rate.
- **Early warning:** paramedic overdoses can rise before deaths are confirmed.
- **Free and easy to refresh** from public downloads.

---

## 5. What we are taking into Build Session 2

1. **Supplies view on the map:** naloxone kits shipped per overdose, by region, with the year slider.
2. **Confirm the overdose increase** with BCCDC before using it in our pitch.
3. **Talk to 1–2 people** at harm reduction non-profits: how do they decide where supplies go today?
4. **Trend alert:** flag regions where overdoses have risen several months in a row.
5. **Add opioid agonist treatment** as another support measure.

---

## Repository contents

| Path | What it is |
|---|---|
| `index.html` | The live map |
| `evidence_2025_by_region.csv` | Harm and supplies for all 16 regions, 2025 |
| `hsda_yearly.csv`, `bccdc_*.csv` | Cleaned data tables |
| `raw_population/`, `raw_bccdc/` | Original downloads |
| `build_data.py`, `build_bccdc.py`, `add_population.py` | Scripts that rebuild and check the data |
| `map/` | Map source and build script |
| `DATA.md` | Data dictionary and notes |

## Sources

- BC Coroners Service, [Statistical Reports on Deaths in BC](https://www2.gov.bc.ca/gov/content/life-events/death/coroners-service/statistical-reports) (data to June 30, 2026)
- BCCDC, [Unregulated Drug Poisoning Emergency Dashboard](http://www.bccdc.ca/health-professionals/data-reports/substance-use-harm-reduction-dashboard) (updated Aug 6, 2026)
- BC Stats, [Population Estimates & Projections](https://www.bcstats.gov.bc.ca/apps/PopulationProjections.aspx) (released May 20, 2026)
- BC Data Catalogue, [Health Service Delivery Area Boundaries](https://catalogue.data.gov.bc.ca/) (2022)

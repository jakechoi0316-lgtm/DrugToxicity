"""Transcribe BC Coroners Service dashboard (data to Jun 30, 2026; refreshed Aug 11, 2026)
into tidy CSVs, and cross-check every table against the dashboard's own totals."""
import csv, os, zipfile
from collections import defaultdict

OUT = "bc_drug_deaths_data"
os.makedirs(OUT, exist_ok=True)

def parse(s, cast):
    return [None if t == "-" else cast(t) for t in s.split()]
def I(s): return parse(s, int)
def F(s): return parse(s, float)

YEARS = list(range(2015, 2027))
LHA_YEARS = list(range(2016, 2027))
M13 = [(2025,6),(2025,7),(2025,8),(2025,9),(2025,10),(2025,11),(2025,12),
       (2026,1),(2026,2),(2026,3),(2026,4),(2026,5),(2026,6)]
M12 = M13[1:]
HAS = ["Interior", "Fraser", "Vancouver Coastal", "Island", "Northern"]
def mc(y): return 6 if y == 2026 else 12   # months covered
def ann(y): return "yes" if y == 2026 else "no"

problems, passed = [], []
def check(ok, msg):
    (passed if ok else problems).append(msg)

def write(name, header, rows):
    with open(os.path.join(OUT, name), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(header)
        for r in rows: w.writerow(["" if v is None else v for v in r])
    return len(rows)

# ---------------------------------------------------------------- BC by month (page 2)
bc_m = {
 1:"43 86 148 134 94 80 188 215 231 221 166 154", 2:"31 58 125 108 87 79 177 203 198 204 132 115",
 3:"32 76 129 158 122 120 173 185 216 219 143 139", 4:"34 73 156 136 81 130 187 174 240 196 174 120",
 5:"41 51 149 119 93 175 173 213 200 198 160 110", 6:"34 72 130 117 73 189 177 159 204 201 151 138",
 7:"40 74 122 151 72 186 199 200 224 194 152", 8:"53 65 126 126 83 161 202 192 199 210 155",
 9:"50 63 97 139 63 142 161 192 191 192 162", 10:"53 77 98 119 79 176 212 212 217 163 146",
 11:"52 140 110 132 81 170 216 203 230 158 136", 12:"65 162 104 127 64 166 226 234 241 163 151"}
bc_total = dict(zip(YEARS, I("528 997 1494 1566 992 1774 2291 2382 2591 2319 1828 776")))
bc_rate = dict(zip(YEARS, F("11.1 20.5 30.3 31.2 19.4 34.3 43.8 44.4 47.0 40.9 32.1 27.5")))
bc_monthly = {}
for m, s in bc_m.items():
    for y, v in zip(YEARS, I(s)): bc_monthly[(y, m)] = v
for y in YEARS:
    check(sum(v for (yy, _), v in bc_monthly.items() if yy == y) == bc_total[y], f"BC monthly sums to yearly total {y}")
write("bc_monthly.csv", ["year","month","deaths"], [[y,m,bc_monthly[(y,m)]] for (y,m) in sorted(bc_monthly)])

# ---------------------------------------------------------------- HA yearly (page 5)
ha_y = {"Interior":"64 169 246 234 140 287 375 407 439 412 320 132",
        "Fraser":"207 337 495 522 328 584 792 711 702 625 527 206",
        "Vancouver Coastal":"160 276 446 456 289 492 627 660 746 613 492 200",
        "Island":"72 163 241 252 168 275 342 416 492 461 342 165",
        "Northern":"25 52 66 102 67 136 155 188 212 208 147 73"}
ha_yr = {"Interior":"8.5 22.0 31.4 29.2 17.2 34.6 44.5 47.3 50.1 46.4 35.8 30.0",
         "Fraser":"11.7 18.7 27.0 27.9 17.2 30.2 40.4 35.1 33.3 28.4 23.7 18.6",
         "Vancouver Coastal":"13.7 23.2 37.2 37.5 23.3 39.2 49.9 51.4 56.3 45.2 36.6 30.0",
         "Island":"9.1 20.2 29.3 30.1 19.7 31.9 39.2 46.6 54.3 50.1 36.9 35.9",
         "Northern":"8.6 17.8 22.6 34.8 22.8 46.3 52.9 63.8 71.0 68.6 48.0 48.5"}
HA_Y = {ha: dict(zip(YEARS, I(s))) for ha, s in ha_y.items()}
HA_YR = {ha: dict(zip(YEARS, F(s))) for ha, s in ha_yr.items()}
for y in YEARS:
    check(sum(HA_Y[h][y] for h in HAS) == bc_total[y], f"HA yearly sums to BC {y}")
rows = [["British Columbia", y, mc(y), bc_total[y], bc_rate[y], ann(y)] for y in YEARS]
rows += [[h, y, mc(y), HA_Y[h][y], HA_YR[h][y], ann(y)] for h in HAS for y in YEARS]
write("ha_yearly.csv", ["health_authority","year","months_covered","deaths","rate_per_100k","rate_annualized"], rows)

# ---------------------------------------------------------------- HA monthly (page 6)
ha_m = {"Interior":"31 23 26 20 25 21 22 31 15 22 15 18 31",
        "Fraser":"49 45 39 50 34 37 50 44 20 38 32 35 37",
        "Vancouver Coastal":"35 43 44 45 46 41 36 37 38 36 38 24 27",
        "Island":"30 31 29 33 28 23 30 29 30 32 25 23 26",
        "Northern":"6 10 17 14 13 14 13 13 12 11 10 10 17",
        "British Columbia":"151 152 155 162 146 136 151 154 115 139 120 110 138"}
ha_mr = {"Interior":"3.5 2.6 2.9 2.2 2.8 2.4 2.5 3.5 1.7 2.5 1.7 2.0 3.5",
         "Fraser":"2.2 2.0 1.8 2.2 1.5 1.7 2.2 2.0 0.9 1.7 1.4 1.6 1.7",
         "Vancouver Coastal":"2.6 3.2 3.3 3.3 3.4 3.1 2.7 2.8 2.9 2.7 2.9 1.8 2.0",
         "Island":"3.2 3.3 3.1 3.6 3.0 2.5 3.2 3.2 3.3 3.5 2.7 2.5 2.8",
         "Northern":"2.0 3.3 5.6 4.6 4.2 4.6 4.2 4.3 4.0 3.7 3.3 3.3 5.6",
         "British Columbia":"2.7 2.7 2.7 2.8 2.6 2.4 2.7 2.7 2.0 2.5 2.1 1.9 2.4"}
HA_M = {h: dict(zip(M13, I(s))) for h, s in ha_m.items()}
HA_MR = {h: dict(zip(M13, F(s))) for h, s in ha_mr.items()}
for ym in M13:
    check(sum(HA_M[h][ym] for h in HAS) == HA_M["British Columbia"][ym], f"HA monthly sums to BC {ym}")
    check(HA_M["British Columbia"][ym] == bc_monthly[ym], f"HA-month BC matches BC-by-month table {ym}")
for h in HAS:
    check(sum(HA_M[h][(2026, m)] for m in range(1, 7)) == HA_Y[h][2026], f"{h} Jan-Jun 2026 months sum to 2026 total")
rows = [[h, y, m, HA_M[h][(y, m)], HA_MR[h][(y, m)]] for h in ["British Columbia"] + HAS for (y, m) in M13]
write("ha_monthly.csv", ["health_authority","year","month","deaths","rate_per_100k_month"], rows)

# ---------------------------------------------------------------- HSDA (page 7)
HSDA = [  # code, name, HA
 (11,"East Kootenay","Interior"),(12,"Kootenay Boundary","Interior"),(13,"Okanagan","Interior"),
 (14,"Thompson Cariboo Shuswap","Interior"),(21,"Fraser East","Fraser"),(22,"Fraser North","Fraser"),
 (23,"Fraser South","Fraser"),(31,"Richmond","Vancouver Coastal"),(32,"Vancouver","Vancouver Coastal"),
 (33,"North Shore/Coast Garibaldi","Vancouver Coastal"),(41,"South Vancouver Island","Island"),
 (42,"Central Vancouver Island","Island"),(43,"North Vancouver Island","Island"),
 (51,"Northwest","Northern"),(52,"Northern Interior","Northern"),(53,"Northeast","Northern")]
hsda_y = {
 "East Kootenay":"2 13 7 6 1 18 24 19 26 24 16 7",
 "Kootenay Boundary":"6 11 17 15 14 23 29 32 41 42 31 22",
 "Okanagan":"43 78 155 128 84 147 172 200 223 200 167 70",
 "Thompson Cariboo Shuswap":"13 67 67 85 41 99 150 156 149 146 106 33",
 "Fraser East":"41 68 105 97 84 121 183 194 201 155 133 74",
 "Fraser North":"73 106 148 152 86 182 243 197 191 179 141 47",
 "Fraser South":"93 163 242 273 158 281 366 320 310 291 253 85",
 "Richmond":"6 14 28 12 14 19 33 29 28 25 23 5",
 "Vancouver":"138 231 373 401 249 423 532 577 658 525 420 179",
 "North Shore/Coast Garibaldi":"16 31 45 43 26 50 62 54 60 63 49 16",
 "South Vancouver Island":"26 78 105 125 75 140 141 173 183 171 126 63",
 "Central Vancouver Island":"33 58 99 96 63 101 132 172 217 188 153 81",
 "North Vancouver Island":"13 27 37 31 30 34 69 71 92 102 63 21",
 "Northwest":"6 10 8 15 16 18 44 57 48 50 34 14",
 "Northern Interior":"15 24 35 63 34 86 80 105 130 132 86 44",
 "Northeast":"4 18 23 24 17 32 31 26 34 26 27 15"}
hsda_yr = {
 "East Kootenay":"2.5 15.7 8.3 7.0 1.1 20.4 26.7 20.7 27.8 25.3 16.8 14.9",
 "Kootenay Boundary":"7.5 13.5 20.7 18.0 16.6 27.1 33.7 36.7 46.4 47.0 34.5 49.9",
 "Okanagan":"11.7 20.7 40.2 32.4 20.8 35.7 40.9 46.4 50.8 44.9 37.2 31.6",
 "Thompson Cariboo Shuswap":"5.8 29.3 28.8 35.7 17.0 40.5 60.8 62.0 58.2 56.4 40.9 26.0",
 "Fraser East":"13.6 22.0 33.2 29.9 25.4 36.2 54.1 56.4 57.1 42.8 36.0 40.3",
 "Fraser North":"11.1 15.8 21.8 22.0 12.3 25.6 33.8 26.6 24.8 22.4 17.6 11.8",
 "Fraser South":"11.6 19.8 28.9 31.9 18.0 31.5 40.5 34.0 31.4 28.0 24.0 16.1",
 "Richmond":"2.9 6.7 13.4 5.6 6.5 8.7 14.9 12.7 11.9 10.3 9.6 4.2",
 "Vancouver":"20.5 33.8 54.1 57.3 34.8 58.6 74.2 79.0 87.2 68.0 55.0 47.2",
 "North Shore/Coast Garibaldi":"5.5 10.5 15.0 14.1 8.4 15.9 19.5 16.6 18.0 18.4 14.4 9.5",
 "South Vancouver Island":"6.6 19.5 25.8 30.2 17.8 32.7 32.5 38.9 40.5 37.1 27.2 27.4",
 "Central Vancouver Island":"12.0 20.6 34.5 32.9 21.2 33.7 43.4 55.6 69.3 59.2 47.8 51.2",
 "North Vancouver Island":"10.5 21.3 28.7 23.6 22.6 25.3 50.7 51.2 65.5 71.7 44.0 29.7",
 "Northwest":"8.1 13.4 10.7 20.1 21.4 23.9 58.0 74.8 62.3 64.1 43.1 35.9",
 "Northern Interior":"10.4 16.4 23.8 42.4 22.8 57.8 54.0 70.3 85.9 85.9 55.5 57.8",
 "Northeast":"5.6 25.4 32.7 34.2 24.3 46.2 45.0 37.5 48.4 36.3 37.4 42.3"}
# Monthly (Jun 2025-Jun 2026). Source leaves a cell blank when the count is 0;
# the positions below were rebuilt from HA subtotals and confirmed against the rate tables.
hsda_m = {
 "East Kootenay":"1 1 3 2 0 0 1 3 2 0 0 0 2",
 "Kootenay Boundary":"4 5 2 3 0 2 3 6 5 4 2 0 5",
 "Okanagan":"11 12 12 11 12 12 10 18 5 13 5 12 17",
 "Thompson Cariboo Shuswap":"15 5 9 4 13 7 8 4 3 5 8 6 7",
 "Fraser East":"12 10 8 13 10 11 10 8 4 16 11 16 19",
 "Fraser North":"10 12 16 12 7 9 11 11 8 5 7 8 8",
 "Fraser South":"27 23 15 25 17 17 29 25 8 17 14 11 10",
 "Richmond":"1 2 3 1 2 0 4 2 1 1 1 0 0",
 "Vancouver":"32 36 38 41 37 38 29 32 33 32 35 22 25",
 "North Shore/Coast Garibaldi":"2 5 3 3 7 3 3 3 4 3 2 2 2",
 "South Vancouver Island":"14 10 12 12 11 9 16 10 10 16 9 9 9",
 "Central Vancouver Island":"10 16 14 12 11 10 10 16 17 11 15 9 13",
 "North Vancouver Island":"6 5 3 9 6 4 4 3 3 5 1 5 4",
 "Northwest":"0 3 5 1 2 3 1 2 1 3 4 1 3",
 "Northern Interior":"5 5 11 10 9 7 10 8 10 6 4 5 11",
 "Northeast":"1 2 1 3 2 4 2 3 1 2 2 4 3"}
hsda_mr = {
 "East Kootenay":"1.0 1.0 3.1 2.1 0 0 1.0 3.2 2.1 0 0 0 2.1",
 "Kootenay Boundary":"4.5 5.6 2.2 3.3 0 2.2 3.3 6.8 5.7 4.5 2.3 0 5.7",
 "Okanagan":"2.4 2.7 2.7 2.4 2.7 2.7 2.2 4.1 1.1 2.9 1.1 2.7 3.8",
 "Thompson Cariboo Shuswap":"5.8 1.9 3.5 1.5 5.0 2.7 3.1 1.6 1.2 2.0 3.2 2.4 2.8",
 "Fraser East":"3.3 2.7 2.2 3.5 2.7 3.0 2.7 2.2 1.1 4.4 3.0 4.4 5.2",
 "Fraser North":"1.2 1.5 2.0 1.5 0.9 1.1 1.4 1.4 1.0 0.6 0.9 1.0 1.0",
 "Fraser South":"2.6 2.2 1.4 2.4 1.6 1.6 2.7 2.4 0.8 1.6 1.3 1.0 0.9",
 "Richmond":"0.4 0.8 1.3 0.4 0.8 0 1.7 0.8 0.4 0.4 0.4 0 0",
 "Vancouver":"4.2 4.7 5.0 5.4 4.8 5.0 3.8 4.2 4.3 4.2 4.6 2.9 3.3",
 "North Shore/Coast Garibaldi":"0.6 1.5 0.9 0.9 2.1 0.9 0.9 0.9 1.2 0.9 0.6 0.6 0.6",
 "South Vancouver Island":"3.0 2.2 2.6 2.6 2.4 1.9 3.4 2.2 2.2 3.5 2.0 2.0 2.0",
 "Central Vancouver Island":"3.1 5.0 4.4 3.7 3.4 3.1 3.1 5.1 5.4 3.5 4.7 2.8 4.1",
 "North Vancouver Island":"4.2 3.5 2.1 6.3 4.2 2.8 2.8 2.1 2.1 3.5 0.7 3.5 2.8",
 "Northwest":"0 3.8 6.3 1.3 2.5 3.8 1.3 2.6 1.3 3.8 5.1 1.3 3.8",
 "Northern Interior":"3.2 3.2 7.1 6.5 5.8 4.5 6.5 5.3 6.6 3.9 2.6 3.3 7.2",
 "Northeast":"1.4 2.8 1.4 4.2 2.8 5.5 2.8 4.2 1.4 2.8 2.8 5.6 4.2"}
HS_Y = {n: dict(zip(YEARS, I(s))) for n, s in hsda_y.items()}
HS_YR = {n: dict(zip(YEARS, F(s))) for n, s in hsda_yr.items()}
HS_M = {n: dict(zip(M13, I(s))) for n, s in hsda_m.items()}
HS_MR = {n: dict(zip(M13, F(s))) for n, s in hsda_mr.items()}
HS_HA = {n: ha for _, n, ha in HSDA}
for h in HAS:
    for y in YEARS:
        check(sum(HS_Y[n][y] for n in HS_Y if HS_HA[n] == h) == HA_Y[h][y], f"HSDA yearly sums to {h} {y}")
    for ym in M13:
        check(sum(HS_M[n][ym] for n in HS_M if HS_HA[n] == h) == HA_M[h][ym], f"HSDA monthly sums to {h} {ym}")
for n in HS_M:
    check(sum(HS_M[n][(2026, m)] for m in range(1, 7)) == HS_Y[n][2026], f"{n} Jan-Jun 2026 months sum to 2026 total")
    for ym in M13:  # zero deaths <-> zero rate, and rate per death is steady
        check((HS_M[n][ym] == 0) == (HS_MR[n][ym] == 0), f"{n} {ym} zero count matches zero rate")
rows = [[c, n, ha, y, mc(y), HS_Y[n][y], HS_YR[n][y], ann(y)] for c, n, ha in HSDA for y in YEARS]
write("hsda_yearly.csv", ["hsda_code","hsda","health_authority","year","months_covered","deaths","rate_per_100k","rate_annualized"], rows)
rows = [[c, n, ha, y, m, HS_M[n][(y, m)], HS_MR[n][(y, m)]] for c, n, ha in HSDA for (y, m) in M13]
write("hsda_monthly.csv", ["hsda_code","hsda","health_authority","year","month","deaths","rate_per_100k_month"], rows)

# ---------------------------------------------------------------- LHA (page 8), 2016-2026, "-" = blank in source
LHA = [  # hsda, lha, deaths, rates, note
 ("East Kootenay","Fernie","2 0 0 1 3 0 1 1 1 2 -","12.4 0.0 0.0 5.8 17.1 0.0 5.5 5.4 5.3 10.5 -",""),
 ("East Kootenay","Cranbrook","2 3 2 0 10 16 11 20 15 10 6","7.3 11.0 7.3 0.0 35.5 56.3 38.1 67.6 50.1 33.5 41.1",""),
 ("East Kootenay","Kimberley","3 0 2 0 0 2 0 1 3 0 0","31.4 0.0 20.6 0.0 0.0 19.7 0.0 9.4 27.7 0.0 0.0",""),
 ("East Kootenay","Windermere","4 3 1 0 3 1 1 1 1 0 1","40.5 29.1 9.4 0.0 25.8 8.2 8.1 7.9 7.8 0.0 15.5",""),
 ("East Kootenay","Creston","1 0 0 0 1 3 3 1 4 3 0","7.7 0.0 0.0 0.0 7.4 22.2 21.5 7.1 27.8 20.8 0.0",""),
 ("East Kootenay","Golden","1 1 1 0 1 2 3 2 0 1 -","14.0 13.8 13.6 0.0 13.3 26.1 38.3 24.9 0.0 12.3 -",""),
 ("Kootenay Boundary","Kootenay Lake","0 0 0 0 1 1 0 1 0 1 -","0.0 0.0 0.0 0.0 27.6 27.3 0.0 26.0 0.0 25.1 -",""),
 ("Kootenay Boundary","Nelson","5 4 2 2 7 7 12 16 10 8 6","18.9 15.0 7.4 7.3 25.4 25.2 43.0 55.9 34.5 27.5 42.1",""),
 ("Kootenay Boundary","Castlegar","3 2 0 5 3 6 6 4 7 6 3","21.1 13.9 0.0 33.9 20.1 40.0 38.8 25.7 44.0 37.2 37.8",""),
 ("Kootenay Boundary","Arrow Lakes","0 1 2 1 2 1 2 1 1 2 1","0.0 21.0 41.5 20.9 41.2 20.4 40.3 19.7 19.4 38.4 39.4",""),
 ("Kootenay Boundary","Trail","2 5 2 3 4 6 5 11 13 11 9","10.0 24.8 9.8 14.6 19.4 28.7 23.7 52.4 61.6 51.9 86.5",""),
 ("Kootenay Boundary","Grand Forks","0 4 9 3 3 5 4 6 9 3 3","0.0 44.5 100.0 33.3 33.4 54.0 42.6 63.4 94.2 31.5 64.3",""),
 ("Kootenay Boundary","Kettle Valley","1 1 0 0 2 3 2 2 2 0 -","27.7 26.8 0.0 0.0 46.5 67.0 44.0 42.5 41.8 0.0 -",""),
 ("Okanagan","Southern Okanagan","1 3 6 2 3 4 10 9 6 8 3","5.0 14.6 28.6 9.3 13.7 18.0 44.6 40.0 26.7 35.7 27.4",""),
 ("Okanagan","Penticton","7 17 16 22 17 28 31 25 29 15 6","16.3 38.8 35.5 48.1 36.9 60.0 65.8 53.0 61.5 31.5 25.7",""),
 ("Okanagan","Keremeos","0 3 3 2 4 2 4 1 3 2 1","0.0 54.7 54.1 35.9 70.7 34.3 67.5 16.7 49.7 33.5 34.4",""),
 ("Okanagan","Princeton","0 6 5 1 3 3 1 3 2 1 2","0.0 122.7 100.8 19.9 57.4 56.6 18.9 55.7 36.7 18.4 74.8",""),
 ("Okanagan","Armstrong/Spallumcheen","1 0 1 0 3 2 1 1 1 3 0","9.4 0.0 9.2 0.0 27.6 18.2 8.8 8.7 8.8 26.2 0.0",""),
 ("Okanagan","Vernon","14 30 24 14 30 43 52 59 45 29 12","20.2 42.4 33.4 19.1 40.2 56.7 67.3 75.0 56.6 36.3 30.5",""),
 ("Okanagan","Central Okanagan","54 90 66 42 80 84 96 118 109 102 46","26.5 43.1 30.7 19.1 35.4 36.2 40.0 48.0 43.3 40.1 36.5",""),
 ("Okanagan","Summerland","0 4 2 1 2 0 3 4 3 4 0","0.0 31.8 15.8 7.9 15.6 0.0 22.9 30.9 23.2 31.0 0.0",""),
 ("Okanagan","Enderby","1 1 4 0 5 6 2 3 2 2 0","13.3 13.1 51.5 0.0 62.4 74.0 23.9 35.6 23.3 22.8 0.0",""),
 ("Thompson Cariboo Shuswap","Revelstoke","0 0 5 0 4 4 4 3 3 2 0","0.0 0.0 57.1 0.0 43.6 43.4 43.2 31.8 30.3 20.0 0.0",""),
 ("Thompson Cariboo Shuswap","Salmon Arm","4 5 6 3 9 18 13 21 9 10 2","11.5 14.0 16.5 8.1 24.0 46.9 32.9 52.2 22.3 24.7 10.1",""),
 ("Thompson Cariboo Shuswap","Kamloops","49 41 51 28 66 83 98 94 96 58 19","41.4 33.8 40.8 22.0 51.1 63.6 73.5 68.9 69.3 41.9 28.0",""),
 ("Thompson Cariboo Shuswap","100 Mile House","0 1 3 2 2 6 3 3 4 7 2","0.0 6.6 19.9 13.2 13.0 38.6 18.7 18.5 24.3 42.0 24.3",""),
 ("Thompson Cariboo Shuswap","North Thompson","0 1 2 1 2 6 2 3 2 2 1","0.0 23.5 46.3 23.2 46.2 139.0 45.4 67.8 44.0 44.3 45.2",""),
 ("Thompson Cariboo Shuswap","Cariboo/Chilcotin","4 7 9 3 10 11 19 13 19 15 4","15.5 27.1 34.4 11.4 38.0 41.5 71.8 48.9 71.5 56.4 30.8",""),
 ("Thompson Cariboo Shuswap","Lillooet and South Cariboo","2 3 4 1 4 7 5 5 6 6 0","18.5 27.6 36.6 9.2 37.0 64.5 45.4 44.6 54.0 54.9 0.0",""),
 ("Thompson Cariboo Shuswap","Merritt","8 9 5 3 2 14 11 7 5 5 5","71.1 79.8 43.8 26.1 17.6 123.9 97.5 61.5 43.7 44.4 91.1",""),
 ("Fraser East","Hope","2 4 3 5 7 9 8 12 8 4 2","23.9 46.8 34.4 56.1 79.2 99.9 87.6 135.3 86.0 42.3 43.0",""),
 ("Fraser East","Chilliwack","15 25 38 22 38 66 52 60 41 38 25","15.4 24.9 36.7 20.8 35.4 60.5 46.7 52.9 34.8 31.7 41.8",""),
 ("Fraser East","Abbotsford","40 53 41 44 64 86 92 90 75 78 32","27.0 35.1 26.6 27.9 40.1 53.4 56.1 53.3 43.5 44.4 36.6",""),
 ("Fraser East","Mission","8 18 13 12 11 18 35 33 26 10 12","17.7 38.8 27.5 25.1 23.0 37.3 72.1 65.9 50.2 19.0 46.1",""),
 ("Fraser East","Agassiz/Harrison","3 5 2 1 1 4 7 6 4 3 0","29.7 48.7 19.0 9.4 9.4 37.4 63.9 55.0 35.0 26.4 0.0",""),
 ("Fraser North","New Westminster","10 24 35 20 35 48 32 38 37 34 7","13.4 31.5 44.8 25.0 42.6 57.9 37.5 43.1 40.3 36.9 15.2",""),
 ("Fraser North","Burnaby","40 44 49 29 59 80 69 52 58 35 14","16.4 17.9 19.6 11.4 22.8 30.6 25.4 18.3 19.6 11.7 9.4",""),
 ("Fraser North","Maple Ridge/Pitt Meadows","32 35 30 16 41 50 38 53 42 41 17","30.1 32.1 26.8 14.2 36.2 43.3 31.8 42.9 32.9 32.3 26.8",""),
 ("Fraser North","Tri-Cities","24 45 38 21 47 65 58 48 42 30 9","9.8 18.1 15.1 8.3 18.4 25.2 21.9 17.5 14.8 10.6 6.5",""),
 ("Fraser South","Langley","31 37 33 24 37 57 45 46 45 49 19","20.6 23.8 20.7 14.7 22.3 33.7 25.1 24.5 22.7 24.5 19.0",""),
 ("Fraser South","Delta","12 20 21 14 20 23 26 22 15 19 2","11.2 18.4 19.0 12.5 17.5 19.9 22.0 18.0 11.8 14.9 3.2",""),
 ("Fraser South","Surrey","115 174 197 113 206 266 228 222 214 175 61","25.0 37.2 41.3 23.1 41.3 52.7 43.6 40.3 36.7 29.4 20.5",""),
 ("Fraser South","South Surrey/White Rock","5 11 22 7 18 20 21 20 17 10 3","4.8 10.3 20.2 6.3 15.9 17.4 17.6 15.9 12.9 7.5 4.5",""),
 ("Richmond","Richmond","14 28 12 14 19 33 28 28 25 23 5","6.7 13.4 5.6 6.5 8.7 14.9 12.3 11.9 10.3 9.6 4.2",""),
 ("Vancouver","Vancouver - City Centre","36 84 70 46 65 96 117 128 100 95 27","27.9 64.6 53.1 34.2 47.8 71.2 85.2 90.2 68.9 66.2 37.9",""),
 ("Vancouver","Vancouver - Centre North","139 186 215 148 254 299 327 399 310 225 112","217.3 288.5 328.9 221.5 376.5 446.7 479.9 566.6 430.4 315.9 316.8",""),
 ("Vancouver","Vancouver - Northeast","13 25 38 18 24 38 37 44 23 32 7","12.2 23.2 34.8 16.1 21.3 34.0 32.5 37.4 19.1 26.9 11.8",""),
 ("Vancouver","Vancouver - Westside","12 9 12 6 10 15 9 7 11 6 6","8.9 6.6 8.7 4.2 7.0 10.5 6.2 4.6 7.1 3.9 7.9",""),
 ("Vancouver","Vancouver - Midtown","16 39 35 18 38 48 49 43 49 39 16","15.2 36.8 32.6 16.4 34.3 43.6 43.7 37.1 41.4 33.3 27.5",""),
 ("Vancouver","Vancouver - South","15 30 31 13 32 36 38 37 31 23 11","10.5 20.8 21.2 8.7 21.2 24.0 24.9 23.4 19.2 14.4 13.9",""),
 ("North Shore/Coast Garibaldi","North Vancouver","13 18 16 12 22 18 21 24 26 14 5","8.8 12.1 10.6 7.9 14.3 11.6 13.1 14.6 15.4 8.3 6.0",""),
 ("North Shore/Coast Garibaldi","West Vancouver/Bowen Island","5 6 6 3 7 5 7 7 5 7 2","9.6 11.4 11.3 5.6 13.0 9.2 12.6 12.3 8.6 12.2 7.1",""),
 ("North Shore/Coast Garibaldi","Sunshine Coast","3 7 6 3 7 12 9 14 14 11 2","9.7 22.4 18.9 9.3 21.5 36.2 26.7 41.2 40.8 31.8 11.7",""),
 ("North Shore/Coast Garibaldi","Powell River","7 5 9 6 12 17 11 6 13 10 5","34.5 24.4 43.3 28.5 56.3 78.5 50.1 27.0 58.0 44.4 45.2",""),
 ("North Shore/Coast Garibaldi","Howe Sound","3 8 6 2 2 9 5 9 4 5 2","7.3 18.7 13.5 4.4 4.2 18.5 10.0 17.5 7.6 9.5 7.7",""),
 ("North Shore/Coast Garibaldi","Bella Coola Valley","- - - - - - - - - - -","- - - - - - - - - - -","all values blank in source"),
 ("North Shore/Coast Garibaldi","Central Coast","- - - - - - - - - - -","- - - - - - - - - - -","all values blank in source"),
 ("South Vancouver Island","Greater Victoria","65 92 98 62 117 116 146 152 137 94 48","27.5 38.5 40.6 25.3 47.5 47.0 58.2 59.9 53.1 36.3 37.6",""),
 ("South Vancouver Island","Western Communities","7 10 18 7 17 18 12 17 22 22 10","8.6 11.8 20.5 7.7 18.0 18.3 11.5 15.9 19.8 19.4 17.4",""),
 ("South Vancouver Island","Saanich Peninsula","4 3 8 5 4 4 10 9 8 10 4","6.0 4.4 11.7 7.3 5.8 5.7 14.0 12.5 11.0 13.8 11.3",""),
 ("South Vancouver Island","Southern Gulf Islands","2 0 1 1 2 3 5 5 4 0 1","12.7 0.0 6.0 5.8 11.3 16.4 26.9 26.5 20.9 0.0 10.6",""),
 ("Central Vancouver Island","Cowichan Valley South","10 13 27 12 23 27 33 38 44 36 21","16.6 21.2 43.4 19.1 36.4 42.4 51.0 58.3 66.9 54.4 64.3",""),
 ("Central Vancouver Island","Cowichan Valley West","1 1 2 2 1 3 5 4 1 2 1","15.5 15.2 29.7 29.1 14.3 43.0 70.8 55.8 13.7 27.3 27.7",""),
 ("Central Vancouver Island","Cowichan Valley North","4 4 3 3 5 3 6 3 3 3 2","20.0 19.5 14.5 14.3 23.6 14.1 27.6 13.7 13.6 13.4 18.0",""),
 ("Central Vancouver Island","Greater Nanaimo","29 59 42 28 42 59 87 119 98 75 44","25.5 50.8 35.3 23.1 34.1 47.3 68.3 91.8 74.2 56.2 66.6",""),
 ("Central Vancouver Island","Oceanside","8 10 7 8 21 16 13 15 18 16 6","16.5 20.2 14.0 15.7 40.9 30.6 24.5 28.0 33.2 29.2 22.1",""),
 ("Central Vancouver Island","Alberni/Clayoquot","6 12 14 10 9 23 28 38 24 21 7","18.6 36.8 42.2 29.6 26.3 65.9 78.9 106.1 66.4 57.9 39.2",""),
 ("North Vancouver Island","Comox Valley","11 17 15 12 14 35 37 37 33 21 12","16.0 24.2 20.9 16.5 18.9 46.7 48.4 47.6 41.6 26.2 30.3",""),
 ("North Vancouver Island","Greater Campbell River","15 19 15 15 17 26 30 47 59 40 8","33.9 42.2 32.7 32.3 36.2 54.7 61.8 96.3 119.9 81.0 32.9",""),
 ("North Vancouver Island","Vancouver Island North and West","1 1 1 3 3 7 4 8 10 2 1","7.4 7.4 7.4 22.1 22.2 51.4 29.0 58.1 72.5 14.5 14.9",""),
 ("Northwest","Haida Gwaii","- - - 2 - 1 2 0 1 0 -","- - - 45.5 - 22.5 44.8 0.0 22.1 0.0 -","year positions read from image layout; verify"),
 ("Northwest","Prince Rupert","4 2 0 2 4 3 9 5 7 6 1","28.4 14.1 0.0 14.1 28.2 21.1 63.5 35.5 49.2 42.2 14.4",""),
 ("Northwest","Upper Skeena","- - - - - - - - - - -","- - - - - - - - - - -","all values blank in source"),
 ("Northwest","Smithers","1 2 7 3 1 10 7 7 6 7 4","5.9 11.7 40.9 17.4 5.8 57.1 39.8 39.7 34.1 40.0 46.7",""),
 ("Northwest","Kitimat","1 0 0 0 1 3 7 9 5 0 0","10.5 0.0 0.0 0.0 10.5 31.3 73.0 90.7 49.2 0.0 0.0",""),
 ("Northwest","Stikine and Snow Country","- - - 0 0 0 - - 0 0 -","- - - 0.0 0.0 0.0 - - 0.0 0.0 -","year positions read from image layout; verify"),
 ("Northwest","Terrace","4 3 6 7 10 17 27 21 26 18 6","18.9 14.2 28.3 32.8 46.2 78.3 123.0 93.8 113.9 78.2 53.0",""),
 ("Northwest","Nisga'a","- - - - - - - - - - -","- - - - - - - - - - -","all values blank in source"),
 ("Northwest","Telegraph Creek","- - - - - - - - - - -","- - - - - - - - - - -","all values blank in source"),
 ("Northern Interior","Quesnel","1 7 5 6 18 10 7 12 18 14 -","4.2 29.0 20.6 24.8 74.6 41.6 29.2 49.9 74.4 57.9 -",""),
 ("Northern Interior","Burns Lake","3 0 0 1 0 0 0 6 0 0 -","46.0 0.0 0.0 15.4 0.0 0.0 0.0 93.5 0.0 0.0 -",""),
 ("Northern Interior","Nechako","1 1 1 1 5 11 9 11 7 3 6","6.1 6.1 6.2 6.2 31.4 68.8 56.1 68.6 43.7 18.6 76.3",""),
 ("Northern Interior","Prince George","19 27 55 26 63 59 89 101 107 69 33","19.1 26.9 54.2 25.5 61.5 58.0 86.6 96.3 100.0 63.8 62.0",""),
 ("Northeast","Peace River South","3 17 12 - - 20 - - 8 - -","10.7 61.1 43.4 - - 74.7 - - 28.7 - -","positions confirmed by Northeast HSDA totals"),
 ("Northeast","Peace River North","14 4 12 9 22 8 13 20 13 14 8","37.5 10.8 32.1 23.9 58.7 21.4 34.6 52.3 33.3 35.5 41.1",""),
 ("Northeast","Fort Nelson","1 2 0 - - 3 - - 5 - -","17.8 37.8 0.0 - - 62.5 - - 103.8 - -","positions confirmed by Northeast HSDA totals"),
]
code = {n: c for c, n, _ in HSDA}
rows, lha_sum, lha_blank = [], defaultdict(int), defaultdict(int)
for hs, lha, d, r, note in LHA:
    D, R = I(d), F(r)
    check(len(D) == 11 and len(R) == 11, f"LHA {lha} has 11 year cells")
    for y, dv, rv in zip(LHA_YEARS, D, R):
        check((dv is None) == (rv is None), f"LHA {lha} {y} blank count matches blank rate")
        if dv is not None: check((dv == 0) == (rv == 0), f"LHA {lha} {y} zero count matches zero rate")
        rows.append([code[hs], hs, HS_HA[hs], lha, y, mc(y), dv, rv, ann(y),
                     "blank in source (suppressed)" if dv is None else "", note])
        if dv is None: lha_blank[(hs, y)] += 1
        else: lha_sum[(hs, y)] += dv
write("lha_yearly.csv", ["hsda_code","hsda","health_authority","lha","year","months_covered","deaths",
      "rate_per_100k","rate_annualized","value_status","row_note"], rows)
lha_report = []
for _, hs, _ in HSDA:
    for y in LHA_YEARS:
        s, b, t = lha_sum[(hs, y)], lha_blank[(hs, y)], HS_Y[hs][y]
        if b == 0 and s != t: lha_report.append(f"{hs} {y}: LHA sum {s} vs HSDA {t} (no blanks)")
        if b > 0 and s > t: lha_report.append(f"{hs} {y}: LHA sum {s} > HSDA {t} (has blanks)")

# ---------------------------------------------------------------- Township (page 9)
twp = {"Abbotsford":"26 40 52 41 44 64 86 91 90 76 78 33","Burnaby":"15 40 44 49 29 59 80 68 52 58 35 14",
 "Chilliwack":"10 14 22 37 21 38 64 49 59 38 35 24","Coquitlam":"11 15 30 22 11 28 30 36 25 26 22 4",
 "Greater Victoria Area":"26 76 105 124 74 138 138 168 178 167 126 62","Kamloops":"7 44 38 47 26 60 76 92 86 91 54 17",
 "Kelowna":"20 47 72 54 34 60 74 83 104 90 83 37","Langley":"10 31 37 33 24 37 57 45 46 44 51 19",
 "Nanaimo":"18 30 56 40 27 39 55 80 115 94 71 43","New Westminster":"12 10 24 35 20 36 48 32 38 37 35 7",
 "North Vancouver":"7 13 19 16 11 22 18 20 23 25 15 6","Other Township":"123 237 349 350 229 424 592 609 679 617 491 216",
 "Penticton":"3 7 15 16 21 17 27 31 24 28 16 6","Prince George":"12 18 24 51 25 60 56 85 93 107 67 30",
 "Richmond":"6 14 28 12 14 19 33 29 28 25 23 5","Surrey":"76 118 182 215 119 222 282 243 237 228 177 63",
 "Vancouver":"138 231 373 401 249 423 532 577 658 525 420 179","Vernon":"8 12 24 23 14 28 43 44 56 43 29 11"}
TW = {k: dict(zip(YEARS, I(v))) for k, v in twp.items()}
for y in YEARS: check(sum(TW[k][y] for k in TW) == bc_total[y], f"Townships sum to BC {y}")
write("township_yearly.csv", ["township","year","months_covered","deaths"],
      [[k, y, mc(y), TW[k][y]] for k in TW for y in YEARS])

# ---------------------------------------------------------------- Age (page 3, yearly)
age = {"0-18":"5 13 26 19 13 17 29 34 27 21 25 5","19-29":"117 204 271 304 173 309 323 338 345 307 211 82",
 "30-39":"136 263 400 399 276 413 543 562 645 570 414 169","40-49":"130 234 355 346 220 410 499 533 576 586 462 202",
 "50-59":"110 230 315 363 216 413 593 575 587 478 397 158","60-69":"29 50 120 127 90 195 271 303 366 307 275 135",
 "70-79":"1 3 7 8 4 17 33 34 43 49 40 25",
 "80+":"0 0 0 0 0 0 0 1 0 0 3 0",            # blanks = 0 (rebuilt from yearly totals)
 "Not available":"0 0 0 0 0 0 0 2 2 1 1 0"}
age_r = {"0-18":"0.6 1.4 2.8 2.0 1.4 1.8 3.1 3.5 2.8 2.1 2.6 1.0","19-29":"16.6 28.4 36.8 39.7 21.9 39.3 41.7 42.2 40.9 35.0 24.8 20.7",
 "30-39":"21.4 40.0 59.2 57.2 38.1 55.3 70.5 69.9 75.9 64.0 45.9 37.5","40-49":"19.9 35.9 54.7 53.4 33.9 62.9 75.6 78.4 81.6 79.6 61.2 52.7",
 "50-59":"15.0 31.1 43.1 50.3 30.2 58.3 84.6 82.6 85.4 70.1 58.7 47.0","60-69":"4.9 8.1 19.0 19.7 13.7 29.2 39.8 43.8 51.9 42.9 38.4 37.9",
 "70-79":"0.3 0.9 1.9 2.0 1.0 3.9 7.3 7.2 8.7 9.6 7.5 9.1"}
AG = {k: dict(zip(YEARS, I(v))) for k, v in age.items()}
AGR = {k: dict(zip(YEARS, F(v))) for k, v in age_r.items()}
for y in YEARS: check(sum(AG[k][y] for k in AG) == bc_total[y], f"Age groups sum to BC {y}")
write("age_group_yearly_bc.csv", ["age_group","year","months_covered","deaths","rate_per_100k","rate_annualized"],
      [[k, y, mc(y), AG[k][y], AGR.get(k, {}).get(y), ann(y)] for k in AG for y in YEARS])

# ---------------------------------------------------------------- Sex by HA (page 4, yearly)
sex = {
 "British Columbia":("106 201 272 318 233 333 502 512 579 579 411 191","422 796 1222 1248 759 1441 1789 1870 2012 1740 1417 585",
   "4.4 8.2 10.9 12.6 9.0 12.8 19.1 18.9 20.8 20.2 14.3 13.4","17.9 33.1 50.0 50.2 29.9 56.1 69.0 70.5 73.6 61.9 50.2 41.9"),
 "Interior":("11 37 48 51 33 59 84 82 82 101 59 32","53 132 198 183 107 228 291 325 357 311 261 100",
   "2.9 9.5 12.1 12.7 8.1 14.2 19.8 19.0 18.6 22.6 13.2 14.5","14.2 34.6 50.9 45.9 26.3 55.3 69.4 75.8 81.7 70.3 58.7 45.7"),
 "Fraser":("45 59 80 86 59 109 155 135 146 143 113 37","162 278 415 436 269 475 637 576 556 482 414 169",
   "5.1 6.5 8.7 9.1 6.2 11.2 15.7 13.3 13.8 12.9 10.1 6.6","18.5 31.0 45.5 46.9 28.3 49.3 65.2 57.2 52.9 43.9 37.4 30.7"),
 "Vancouver Coastal":("30 59 76 98 77 93 139 134 165 147 105 49","130 217 370 358 212 399 488 526 581 466 387 151",
   "5.0 9.8 12.4 15.8 12.2 14.6 21.8 20.5 24.5 21.3 15.3 14.4","22.7 37.2 62.8 59.9 34.7 64.6 79.0 83.5 89.3 70.0 58.8 46.3"),
 "Island":("17 32 53 54 46 40 74 94 117 123 81 49","55 131 188 198 122 235 268 322 375 338 261 116",
   "4.2 7.8 12.6 12.7 10.6 9.1 16.6 20.6 25.3 26.1 17.1 20.8","14.2 33.0 46.6 48.2 29.2 55.5 62.6 73.7 84.7 75.1 57.6 51.8"),
 "Northern":("3 14 15 29 18 32 50 67 69 65 53 24","22 38 51 73 49 104 105 121 143 143 94 49",
   "2.1 9.9 10.6 20.3 12.6 22.3 35.0 46.6 47.3 43.8 35.5 32.6","14.8 25.3 34.0 48.6 32.5 69.2 70.0 80.1 93.5 92.2 60.0 63.6")}
rows = []
for h, (fd, md, fr, mr) in sex.items():
    FD, MD, FR, MR = I(fd), I(md), F(fr), F(mr)
    tot = bc_total if h == "British Columbia" else HA_Y[h]
    for i, y in enumerate(YEARS):
        check(FD[i] + MD[i] == tot[y], f"Sex sums to {h} total {y}")
        rows.append([h, y, mc(y), "Female", FD[i], FR[i], ann(y)])
        rows.append([h, y, mc(y), "Male", MD[i], MR[i], ann(y)])
write("sex_yearly_by_ha.csv", ["health_authority","year","months_covered","sex","deaths","rate_per_100k","rate_annualized"], rows)

# ---------------------------------------------------------------- Place of injury (page 10)
# The 5 filtered pages show BC MINUS one HA (all HAs except the darker button were selected).
# Per-HA values are derived as BC minus that page. Blank cells = 0 (totals reconcile).
PL = ["Private Residence","Other Residence","Outside","Public Building: Other","Not available",
      "Public Building: Washroom","Medical Facility","Industrial/Construction/Manufacturing/Natural Resource Sites",
      "Correctional Facility/Police Cell"]
PY = [2023, 2024, 2025, 2026]
def place(d): return {k: I(v) for k, v in d.items()}
bc_pl = place({"Private Residence":"1222 1110 881 409","Other Residence":"731 649 478 196","Outside":"491 440 383 139",
 "Public Building: Other":"66 62 42 9","Not available":"21 11 19 12","Public Building: Washroom":"22 17 9 1",
 "Medical Facility":"17 15 11 4","Industrial/Construction/Manufacturing/Natural Resource Sites":"13 9 0 2",
 "Correctional Facility/Police Cell":"8 6 5 4"})
excl = {
 "Interior": place({"Private Residence":"973 877 703 321","Other Residence":"647 573 421 174","Outside":"405 364 313 121",
   "Public Building: Other":"55 48 32 9","Not available":"18 8 16 11","Medical Facility":"16 12 10 4",
   "Public Building: Washroom":"18 13 8 1","Correctional Facility/Police Cell":"8 5 5 2",
   "Industrial/Construction/Manufacturing/Natural Resource Sites":"12 7 0 1"}),
 "Fraser": place({"Private Residence":"796 717 554 284","Other Residence":"623 545 411 162","Outside":"371 347 282 103",
   "Public Building: Other":"47 41 30 6","Not available":"16 10 8 8","Medical Facility":"12 14 9 3",
   "Public Building: Washroom":"14 9 5 1","Industrial/Construction/Manufacturing/Natural Resource Sites":"9 8 0 1",
   "Correctional Facility/Police Cell":"1 3 2 2"}),
 "Vancouver Coastal": place({"Private Residence":"1042 964 757 354","Outside":"353 314 268 91","Other Residence":"334 337 243 107",
   "Public Building: Other":"53 50 35 7","Not available":"15 8 16 8","Public Building: Washroom":"18 13 7 1",
   "Medical Facility":"9 8 5 2","Correctional Facility/Police Cell":"8 6 5 4",
   "Industrial/Construction/Manufacturing/Natural Resource Sites":"13 6 0 2"}),
 "Island": place({"Private Residence":"966 887 712 316","Other Residence":"638 537 394 159","Outside":"377 334 305 109",
   "Public Building: Other":"54 51 35 6","Not available":"16 10 18 11","Public Building: Washroom":"17 17 8 1",
   "Medical Facility":"14 11 9 3","Correctional Facility/Police Cell":"8 4 5 4",
   "Industrial/Construction/Manufacturing/Natural Resource Sites":"9 7 0 2"}),
 "Northern": place({"Private Residence":"1111 995 798 361","Other Residence":"682 604 443 182","Outside":"458 401 364 132",
   "Public Building: Other":"55 58 36 8","Not available":"19 8 18 10","Medical Facility":"17 15 11 4",
   "Public Building: Washroom":"21 16 8 0","Correctional Facility/Police Cell":"7 6 3 4",
   "Industrial/Construction/Manufacturing/Natural Resource Sites":"9 8 0 2"})}
excl_tot = {"Interior":[2152,1907,1508,644],"Fraser":[1889,1694,1301,570],"Vancouver Coastal":[1845,1706,1336,576],
            "Island":[2099,1858,1486,611],"Northern":[2379,2111,1681,703]}
for i, y in enumerate(PY):
    check(sum(bc_pl[p][i] for p in PL) == bc_total[y], f"Place (BC) sums to BC {y}")
rows = [["British Columbia", y, mc(y), p, bc_pl[p][i], "as shown"] for p in PL for i, y in enumerate(PY)]
for h in HAS:
    for i, y in enumerate(PY):
        check(sum(excl[h][p][i] for p in PL) == excl_tot[h][i], f"Place page (BC minus {h}) sums to its total {y}")
        check(bc_total[y] - excl_tot[h][i] == HA_Y[h][y], f"Place page {h} is BC minus {h} {y}")
        derived = {p: bc_pl[p][i] - excl[h][p][i] for p in PL}
        check(min(derived.values()) >= 0, f"Place derived {h} {y} no negatives")
        check(sum(derived.values()) == HA_Y[h][y], f"Place derived {h} sums to {h} total {y}")
        rows += [[h, y, mc(y), p, derived[p], "derived: BC minus all-except-HA page"] for p in PL]
write("place_of_injury_by_ha.csv", ["health_authority","year","months_covered","place_of_injury","deaths","source"], rows)

# ---------------------------------------------------------------- Drugs involved (page 11), % of completed investigations
DR = ["Fentanyl","Cocaine","Meth/amph","Benzodiazepines","Other opioid","Other stimulants","Alcohol"]
DY = list(range(2015, 2026))
drugs = {
 "British Columbia":["28.6 65.9 81.6 85.2 83.6 83.2 86.6 85.4 85.0 84.1 79.4","48.8 47.3 47.1 48.3 45.9 43.0 41.1 40.5 42.2 48.5 49.3",
   "29.0 31.2 29.4 36.0 39.5 42.5 45.5 46.3 49.5 50.4 51.3","4.6 5.0 3.8 3.1 6.6 13.8 29.2 30.3 43.8 47.9 44.6",
   "55.4 44.7 25.1 34.3 31.3 20.6 21.6 20.1 20.3 18.7 19.3","2.3 2.0 2.1 2.2 2.9 3.2 2.0 2.4 1.9 2.6 2.7",
   "23.8 24.4 25.2 28.3 26.6 26.4 24.8 20.9 18.8 16.9 15.2"],
 "Interior":["32.8 69.2 84.6 85.4 81.4 82.0 87.5 85.8 82.3 81.6 78.8","48.4 40.2 50.0 40.3 41.4 37.8 44.3 41.4 39.1 51.6 54.5",
   "21.9 31.4 28.5 40.3 34.3 39.6 44.6 49.9 51.4 51.6 50.0","4.7 6.5 4.1 1.7 5.0 11.7 32.0 33.7 45.6 48.4 42.4",
   "46.9 37.9 17.9 25.3 25.0 20.1 18.7 18.0 20.5 17.1 14.9","6.3 3.0 2.8 3.4 2.1 4.9 1.7 3.2 2.6 1.5 2.1",
   "17.2 27.8 28.5 27.9 28.6 27.6 24.8 20.2 17.4 18.1 17.0"],
 "Fraser":["26.5 60.8 78.3 84.2 86.1 85.1 87.4 86.7 84.1 82.8 78.2","48.5 50.7 41.9 45.6 44.1 42.0 35.8 37.6 39.6 43.3 42.9",
   "27.0 27.6 25.5 28.5 35.8 37.7 39.8 43.7 46.1 45.1 52.9","5.4 6.2 4.0 2.5 4.3 18.1 35.6 33.5 47.1 53.6 51.4",
   "52.0 42.1 25.9 33.5 29.0 18.4 19.2 18.8 20.0 18.5 20.1","1.5 1.5 1.6 2.1 2.5 2.8 2.3 2.2 1.3 1.8 2.7",
   "23.0 17.5 22.1 26.9 26.2 23.4 24.6 16.0 18.0 14.7 15.6"],
 "Vancouver Coastal":["25.6 65.2 81.2 84.2 81.5 81.4 88.1 85.3 86.9 86.7 79.7","50.0 46.0 49.8 51.9 50.7 44.8 46.0 45.4 46.1 49.2 48.4",
   "31.3 36.2 33.0 40.9 45.5 47.0 50.9 44.5 46.8 50.6 48.0","3.1 4.0 3.6 2.4 11.2 10.8 23.6 22.9 34.8 36.8 37.9",
   "58.8 47.1 25.1 36.3 34.6 25.4 27.0 21.5 22.0 19.0 22.3","3.1 2.5 1.8 1.1 2.4 3.1 1.8 2.3 2.2 3.9 2.7",
   "23.8 27.5 24.0 28.1 24.1 27.0 24.5 23.5 20.8 19.2 12.7"],
 "Island":["30.6 73.5 87.1 89.3 86.3 84.4 84.0 85.3 88.9 85.4 83.3","44.4 47.5 48.3 52.9 43.1 47.6 43.2 40.3 44.8 51.3 58.0",
   "38.9 31.5 30.8 34.3 41.3 44.2 48.5 46.8 53.6 52.4 52.6","6.9 3.7 4.2 6.6 5.0 13.0 24.7 32.6 50.6 51.3 43.6",
   "66.7 55.6 30.4 33.1 31.9 21.6 21.3 22.9 18.0 20.4 19.2","0.0 1.9 2.5 1.7 5.6 2.2 1.9 2.5 1.0 1.8 1.9",
   "29.2 26.5 30.8 31.8 26.9 25.7 25.0 23.9 17.4 14.2 16.3"],
 "Northern":["48.0 67.3 78.8 84.3 79.1 81.3 79.9 79.8 77.4 82.0 75.2","56.0 53.8 51.5 52.9 49.3 42.5 35.4 32.8 37.0 49.0 43.6",
   "20.0 26.9 31.8 46.1 38.8 49.3 49.3 53.0 57.7 58.3 57.1","0.0 1.9 1.5 3.9 4.5 11.9 22.2 31.7 45.2 54.9 50.4",
   "52.0 36.5 25.8 53.9 40.3 11.9 18.8 19.1 19.7 17.5 15.8","0.0 0.0 4.5 5.9 1.5 3.7 2.1 1.1 3.4 4.9 5.3",
   "32.0 34.6 24.2 28.4 34.3 35.8 27.1 24.6 20.2 20.4 15.8"]}
# filter check: 2015 percentages must be whole-death fractions of that HA's 2015 deaths
for h, d in drugs.items():
    n = bc_total[2015] if h == "British Columbia" else HA_Y[h][2015]
    for s in d: check(len(F(s)) == 11, f"Drugs {h} row has 11 years")
for h in ["Interior", "Island", "Vancouver Coastal", "Northern"]:
    n = HA_Y[h][2015]
    ok = all(abs(round(p * n / 100) / n * 100 - p) < 0.06 for p in [F(s)[0] for s in drugs[h]])
    check(ok, f"Drugs page for {h}: 2015 % match whole deaths out of {n} (confirms filter)")
rows = [[h, y, dr, v] for h, d in drugs.items() for dr, s in zip(DR, d) for y, v in zip(DY, F(s))]
write("drugs_involved_by_ha.csv", ["health_authority","year","drug_type","pct_of_deaths"], rows)

# ---------------------------------------------------------------- Fentanyl detected (page 12), chart labels
fent = {"British Columbia":"29 67 82 86 83 84 87 86 85 84 79 74","Interior":"33 69 84 86 81 83 89 86 83 82 79 73",
        "Fraser":"28 62 79 85 85 86 87 87 84 82 78 74","Vancouver Coastal":"25 66 82 84 81 83 88 85 88 86 81 79",
        "Island":"32 75 87 89 85 84 85 86 89 86 82 74","Northern":"48 69 79 86 79 84 79 80 78 82 75 66"}
write("fentanyl_detected_by_ha.csv", ["health_authority","year","pct_fentanyl_detected"],
      [[h, y, v] for h, s in fent.items() for y, v in zip(YEARS, I(s))])

# ---------------------------------------------------------------- Expedited toxicology (page 14)
TOX = ["Fentanyl & analogues","Stimulant","Other Opioids","Benzodiazepine"]
tox = {
 "British Columbia":["86.4 81.6 17.6 42.4","82.4 83.2 22.1 42.0","90.4 76.5 16.9 49.3","84.6 94.3 15.4 43.1","84.2 85.1 17.5 39.5","80.6 84.5 18.4 34.0",
   "81.3 83.5 13.7 33.8","83.7 82.7 19.4 42.9","82.7 82.7 19.7 36.2","83.5 91.7 19.3 33.9","80.0 81.1 21.1 36.8","73.2 82.1 20.5 25.0"],
 "Interior":["95.5 86.4 13.6 54.5","61.9 90.5 28.6 28.6","94.4 77.8 16.7 33.3","81.0 90.5 4.8 19.0","83.3 83.3 16.7 50.0","75.0 100.0 8.3 33.3",
   "82.8 93.1 0.0 41.4","100.0 91.7 16.7 50.0","72.7 90.9 27.3 45.5","75.0 83.3 8.3 41.7","82.4 88.2 17.6 58.8","69.6 82.6 13.0 21.7"],
 "Fraser":["83.3 88.9 19.4 47.2","81.3 81.3 21.9 62.5","85.4 73.2 19.5 58.5","88.9 96.3 14.8 63.0","71.4 82.1 25.0 39.3","82.4 82.4 20.6 29.4",
   "73.0 75.7 16.2 32.4","80.0 80.0 13.3 46.7","90.9 72.7 15.2 42.4","86.2 93.1 20.7 34.5","80.0 83.3 20.0 26.7","83.3 86.7 16.7 33.3"],
 "Vancouver Coastal":["91.2 85.3 11.8 35.3","89.7 76.9 25.6 41.0","88.9 75.0 25.0 41.7","84.6 89.7 20.5 38.5","89.2 83.8 18.9 35.1","80.0 80.0 8.0 32.0",
   "91.4 77.1 20.0 31.4","82.4 88.2 26.5 47.1","78.8 87.9 24.2 30.3","83.3 88.9 25.0 25.0","89.5 78.9 15.8 31.6","72.0 80.0 32.0 12.0"],
 "Island":["88.0 64.0 24.0 32.0","91.7 87.5 20.8 25.0","96.7 90.0 10.0 50.0","83.3 100.0 16.7 41.7","90.0 90.0 10.0 30.0","82.6 82.6 34.8 30.4",
   "84.6 96.2 11.5 30.8","82.1 71.4 14.3 25.0","83.3 76.7 13.3 20.0","78.3 100.0 17.4 26.1","73.7 78.9 21.1 31.6","72.7 72.7 22.7 27.3"],
 "Northern":["50.0 75.0 25.0 50.0","80.0 86.7 6.7 46.7","90.9 54.5 0.0 63.6","83.3 100.0 16.7 58.3","90.9 90.9 9.1 54.5","77.8 88.9 11.1 66.7",
   "66.7 75.0 25.0 33.3","77.8 88.9 22.2 66.7","88.9 100.0 22.2 66.7","100.0 88.9 11.1 77.8","70.0 70.0 40.0 50.0","58.3 91.7 16.7 33.3"]}
rows = []
for h, months in tox.items():
    check(len(months) == 12, f"Tox {h} has 12 months")
    for (y, m), s in zip(M12, months):
        rows += [[h, y, m, t, v] for t, v in zip(TOX, F(s))]
write("expedited_tox_monthly_by_ha.csv", ["health_authority","year","month","drug_type","pct_of_tested_deaths"], rows)

# ---------------------------------------------------------------- Income assistance day (page 17), chart labels
ia_y = list(range(2016, 2027))
ia_a = F("3.6 6.0 5.6 3.8 5.8 7.4 8.7 8.0 7.5 6.1 5.5"); ia_b = F("2.6 3.7 4.0 2.5 4.7 6.1 6.1 6.9 6.1 4.8 4.1")
write("income_assistance_day_bc.csv", ["year","avg_deaths_per_day_payday_to_sunday","avg_deaths_per_day_other_days"],
      [[y, a, b] for y, a, b in zip(ia_y, ia_a, ia_b)])

# ---------------------------------------------------------------- report + zip
print(f"CHECKS PASSED: {len(passed)}   FAILED: {len(problems)}")
for p in problems: print("  FAIL:", p)
print("LHA vs HSDA differences:", len(lha_report))
for r in lha_report: print("  ", r)

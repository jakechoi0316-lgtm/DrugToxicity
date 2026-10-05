"""Read BC Stats population files (raw_population/), build tidy population tables,
add population to hsda_yearly.csv, and check that deaths / population reproduces
the dashboard's published rates."""
import csv, glob, os

HERE = os.path.dirname(os.path.abspath(__file__))
HA_NAME = {"Vancouver Island": "Island"}  # BC Stats name -> dashboard name

hsda_pop, ha_pop = [], []
for f in sorted(glob.glob(os.path.join(HERE, "raw_population", "*.csv"))):
    rows = list(csv.reader(open(f, encoding="utf-8-sig")))
    level = rows[3][0].replace("Geographic level: ", "")
    for r in rows[7:]:
        if len(r) < 6 or not r[0].strip().isdigit():
            continue
        rec = dict(code=int(r[0]), name=HA_NAME.get(r[1], r[1]), year=int(r[2]),
                   type=r[3], sex=r[4], pop=int(r[5].replace(",", "").strip()))
        (hsda_pop if level == "Health Service Delivery Area" else ha_pop).append(rec)

def write(name, header, rows):
    with open(os.path.join(HERE, name), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(header); w.writerows(rows)

SEX = {"F": "Female", "M": "Male", "T": "Total"}
write("population_hsda.csv", ["hsda_code", "hsda", "year", "estimate_type", "sex", "population"],
      [[p["code"], p["name"], p["year"], p["type"], SEX[p["sex"]], p["pop"]]
       for p in sorted(hsda_pop, key=lambda p: (p["code"], p["year"], p["sex"]))])
write("population_ha.csv", ["ha_code", "health_authority", "year", "estimate_type", "sex", "population"],
      [[p["code"], p["name"], p["year"], p["type"], SEX[p["sex"]], p["pop"]]
       for p in sorted(ha_pop, key=lambda p: (p["code"], p["year"], p["sex"]))])

tot = {(p["code"], p["year"]): p for p in hsda_pop if p["sex"] == "T"}
problems, n_checks = [], 0
def check(ok, msg):
    global n_checks; n_checks += 1
    if not ok: problems.append(msg)

# F + M = T in every file
for kind in (hsda_pop, ha_pop):
    by = {}
    for p in kind: by.setdefault((p["code"], p["year"]), {})[p["sex"]] = p["pop"]
    for k, v in by.items(): check(v["F"] + v["M"] == v["T"], f"F+M=T {k}")

# HSDA populations add up to HA populations (2015-2025)
ha_t = {(p["name"], p["year"]): p["pop"] for p in ha_pop if p["sex"] == "T"}
rows = list(csv.DictReader(open(os.path.join(HERE, "hsda_yearly.csv"))))
hsda_ha = {int(r["hsda_code"]): r["health_authority"] for r in rows}
for (ha, y), v in ha_t.items():
    s = sum(t["pop"] for (c, yy), t in tot.items() if yy == y and hsda_ha[c] == ha)
    check(s == v, f"HSDA pops sum to {ha} {y}: {s} vs {v}")

# add population to hsda_yearly.csv and check rates
out = []
for r in rows:
    p = tot[(int(r["hsda_code"]), int(r["year"]))]
    deaths, months = int(r["deaths"]), int(r["months_covered"])
    calc = round(deaths * (12 / months) / p["pop"] * 1e5, 1)
    check(abs(calc - float(r["rate_per_100k"])) <= 0.1,
          f"rate {r['hsda']} {r['year']}: calculated {calc} vs dashboard {r['rate_per_100k']}")
    r = {k: r[k] for k in ["hsda_code", "hsda", "health_authority", "year", "months_covered", "deaths"]} | {
        "population": p["pop"], "population_type": p["type"],
        "rate_per_100k": r["rate_per_100k"], "rate_annualized": r["rate_annualized"]}
    out.append(r)
with open(os.path.join(HERE, "hsda_yearly.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)

# monthly rates use the same populations (not annualized)
for r in csv.DictReader(open(os.path.join(HERE, "hsda_monthly.csv"))):
    p = tot[(int(r["hsda_code"]), int(r["year"]))]["pop"]
    calc = round(int(r["deaths"]) / p * 1e5, 1)
    check(abs(calc - float(r["rate_per_100k_month"])) <= 0.1,
          f"monthly rate {r['hsda']} {r['year']}-{r['month']}: {calc} vs {r['rate_per_100k_month']}")

print(f"HSDA population rows: {len(hsda_pop)}, HA rows: {len(ha_pop)}")
print(f"CHECKS: {n_checks}, FAILED: {len(problems)}")
for p in problems: print("  FAIL:", p)

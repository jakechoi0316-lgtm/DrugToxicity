"""Build the interactive map (bc_drug_toxicity_map.html) from the cleaned CSVs and simplified boundaries."""
import csv, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "..")

hsda, rows = {}, []
for r in csv.DictReader(open(os.path.join(DATA_DIR, "hsda_yearly.csv"))):
    c = int(r["hsda_code"])
    hsda[c] = {"code": c, "name": r["hsda"], "ha": r["health_authority"]}
    rows.append([c, int(r["year"]), int(r["deaths"]), int(r["population"]), float(r["rate_per_100k"])])
bc = {int(r["year"]): {"d": int(r["deaths"]), "r": float(r["rate_per_100k"])}
      for r in csv.DictReader(open(os.path.join(DATA_DIR, "ha_yearly.csv"))) if r["health_authority"] == "British Columbia"}
geo = json.load(open(os.path.join(HERE, "hsda_boundaries_simplified.geojson")))

# the map and the death data must share the same 16 HSDA codes
assert {f["properties"]["hsda_code"] for f in geo["features"]} == set(hsda), "HSDA codes differ"
for f in geo["features"]:
    p = f["properties"]
    assert p["hsda"] == hsda[p["hsda_code"]]["name"], p

data = {"hsda": sorted(hsda.values(), key=lambda h: h["code"]), "rows": rows, "bc": bc}
html = open(os.path.join(HERE, "map_template.html")).read()
html = html.replace("/*__DATA__*/null", json.dumps(data, separators=(",", ":")))
html = html.replace("/*__GEO__*/null", json.dumps(geo, separators=(",", ":")))
open(os.path.join(HERE, "bc_drug_toxicity_map.html"), "w").write(html)
print("ok", len(rows), "rows,", round(len(html) / 1024), "KB")

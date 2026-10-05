"""Simplify the BC Geographic Warehouse HSDA boundaries (33 MB) into a small GeoJSON for the web map."""
import json, sys
from shapely.geometry import shape, mapping
from shapely.geometry.polygon import orient
from shapely.geometry import Polygon, MultiPolygon

SRC, OUT, TOL = sys.argv[1], sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 0.003

def rnd(c):  # round coordinates to ~10 m
    return [[round(x, 4), round(y, 4)] for x, y in c]

feats = []
for f in json.load(open(SRC))["features"]:
    p = f["properties"]
    g = shape(f["geometry"]).simplify(TOL, preserve_topology=True)
    polys = [g] if isinstance(g, Polygon) else list(g.geoms)
    # d3 (spherical) needs clockwise outer rings; drop tiny islands under ~0.3 km2
    polys = [orient(q, sign=-1.0) for q in polys if q.area > 3e-5]
    coords = [[rnd(q.exterior.coords)] + [rnd(i.coords) for i in q.interiors] for q in polys]
    feats.append({"type": "Feature",
                  "properties": {"hsda_code": int(p["HLTH_SERVICE_DLVR_AREA_CODE"]),
                                 "hsda": p["HLTH_SERVICE_DLVR_AREA_NAME"],
                                 "health_authority": p["HLTH_AUTHORITY_NAME"],
                                 "area_km2": round(p["FEATURE_AREA_SQM"] / 1e6)},
                  "geometry": {"type": "MultiPolygon", "coordinates": coords}})
json.dump({"type": "FeatureCollection", "features": feats}, open(OUT, "w"), separators=(",", ":"))
print(len(feats), "features")

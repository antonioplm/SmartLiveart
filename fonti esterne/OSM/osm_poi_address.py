import json
import csv
import time
import requests
import os
import sys
from shapely.geometry import Point, Polygon
from shapely.errors import ShapelyError
from shapely.ops import unary_union

# ----------------------------
# Parametri da riga di comando
# ----------------------------
if len(sys.argv) < 2:
    print("Uso: python enrich_osm_poi.py <NOME_COMUNE> [--use-cache|--no-cache]")
    sys.exit(1)

CITY_NAME = sys.argv[1]
CITY_CAPITALIZED = " ".join(word.capitalize() for word in CITY_NAME.split())
city_slug = CITY_CAPITALIZED.lower().replace(" ", "_")

USE_CACHE = "--no-cache" not in sys.argv  # di default usa la cache

# ----------------------------
# Config dinamica
# ----------------------------
INPUT_JSON = f"{city_slug}_osm_poi.json"
OUTPUT_JSON = f"{city_slug}_osm_address.json"
QUARTIERI_JSON = f"{city_slug}_neighborhood.json"
CACHE_FILE = f"{city_slug}_nominatim_cache.json"

NOMINATIM_URL = "https://nominatim.openstreetmap.org/reverse"

print(f"Comune: {CITY_CAPITALIZED}")
print(f"Input: {INPUT_JSON}")
print(f"Quartieri: {QUARTIERI_JSON}")
print(f"Output: {OUTPUT_JSON}")
print(f"Cache: {'attiva' if USE_CACHE else 'disattivata'}")

# ----------------------------
# Cache Nominatim
# ----------------------------
if USE_CACHE and os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        NOMINATIM_CACHE = json.load(f)
else:
    NOMINATIM_CACHE = {}

def save_cache():
    if USE_CACHE:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(NOMINATIM_CACHE, f, ensure_ascii=False, indent=2)

def reverse_geocode(lat, lon):
    key = f"{lat},{lon}"

    # Usa la cache solo se abilitata
    if USE_CACHE and key in NOMINATIM_CACHE:
        return NOMINATIM_CACHE[key]

    params = {
        "lat": lat,
        "lon": lon,
        "format": "json",
        "addressdetails": 1,
        "accept-language": "it"
    }
    url = NOMINATIM_URL + "?" + requests.compat.urlencode(params)
    time.sleep(1)
    try:
        r = requests.get(url, headers={"User-Agent": "SLKB-Geocoder"})
        if r.status_code == 200:
            data = r.json()
            if USE_CACHE:
                NOMINATIM_CACHE[key] = data
                save_cache()
            return data
        return None
    except Exception as e:
        print(f"❌ Errore Nominatim per {lat},{lon}: {e}")
        return None

def estrai_address(addr):
    if not addr:
        return ""
    parts = []
    for k in ["road", "pedestrian", "footway", "house_number", "postcode"]:
        if k in addr:
            parts.append(addr[k])
    return ", ".join(parts)

# ----------------------------
# Carica e normalizza quartieri
# ----------------------------
def load_quartieri(path_json):
    with open(path_json, "r", encoding="utf-8") as f:
        raw = json.load(f)

    elements = raw.get("elements", [])
    quartieri_poligoni = []

    print(f"Trovati {len(elements)} elementi raw Overpass")

    def safe_polygon(coords):
        try:
            poly = Polygon(coords)
            if not poly.is_valid:
                poly = poly.buffer(0)
            return poly if poly.is_valid else None
        except ShapelyError:
            return None

    for el in elements:
        nome = el.get("tags", {}).get("name", "unknown").strip() or "unknown"
        geom = None

        if el["type"] == "way" and "geometry" in el:
            coords = [(n["lon"], n["lat"]) for n in el["geometry"]]
            if len(coords) >= 4:
                geom = safe_polygon(coords)

        elif el["type"] == "relation":
            polys = []
            for member in el.get("members", []):
                if member["type"] == "way" and "geometry" in member:
                    coords = [(n["lon"], n["lat"]) for n in member["geometry"]]
                    if len(coords) >= 4:
                        p = safe_polygon(coords)
                        if p:
                            polys.append(p)
            if polys:
                try:
                    geom = unary_union(polys)
                    if not geom.is_valid:
                        geom = geom.buffer(0)
                except ShapelyError:
                    geom = None

        if geom:
            quartieri_poligoni.append((nome, geom))
        else:
            print(f"Ignorata feature {nome}, geometria non valida")

    print(f"Caricati {len(quartieri_poligoni)} poligoni di quartieri")
    return quartieri_poligoni

# ----------------------------
# Determina quartiere da coordinate
# ----------------------------
def quartiere_from_point(lat, lon, quartieri_poligoni):
    """
    Determina il quartiere (municipalità) più vicino al punto dato.
    Applica buffer progressivi e seleziona sempre il poligono più vicino,
    anche se più di uno include il punto.
    """
    pt = Point(lon, lat)
    best_name = None
    best_dist = float("inf")
    best_tol = 0

    # Buffer progressivi (~55m, ~165m, ~330m, ~660m, ~1300m, ~2600m)
    buffer_steps = [0.0005, 0.0015, 0.003, 0.006, 0.012, 0.024]

    for tol in buffer_steps:
        candidates = []

        for nome, pol in quartieri_poligoni:
            if pol is None:
                continue
            try:
                if pol.buffer(tol).contains(pt):
                    dist = pol.distance(pt)
                    candidates.append((nome, dist, tol))
            except Exception:
                continue

        # Se ci sono candidati per questa tolleranza, scegli quello più vicino
        if candidates:
            candidates.sort(key=lambda x: x[1])  # ordina per distanza
            best_name, best_dist, best_tol = candidates[0]
            print(f"⚠️ {lat:.6f},{lon:.6f} incluso in {best_name} con tolleranza {best_tol*111000:.0f} m (distanza {best_dist*111000:.1f} m)")
            return best_name

    # Fallback: se nessuno lo contiene, assegna il più vicino entro 400 m
    for nome, pol in quartieri_poligoni:
        if pol is None:
            continue
        try:
            dist = pol.distance(pt)
            if dist < best_dist:
                best_name = nome
                best_dist = dist
        except Exception:
            continue

    if best_name and best_dist < 0.004:
#        print(f"{lat:.6f},{lon:.6f} assegnato a {best_name} (distanza {best_dist*111000:.1f} m)")
        return best_name

#    print(f"Nessun quartiere trovato per {lat:.6f},{lon:.6f}")
    return ""


# ----------------------------
# Arricchimento POI
# ----------------------------
def arricchisci(poi, quartieri_poligoni):
    lat = poi.get("latitudine")
    lon = poi.get("longitudine")

    tags = poi.get("tag_k3", "").split(";")
    for tag in tags:
        if tag.startswith("contact:phone="):
            poi["contatti"] = tag.split("=", 1)[1]
        if tag.startswith("contact:email="):
            poi["contatti"] = tag.split("=", 1)[1]
        if tag.startswith("website=") or tag.startswith("contact:website="):
            poi["sito_web"] = tag.split("=", 1)[1]
        if tag.startswith("opening_hours="):
            poi["orari"] = tag.split("=", 1)[1]

    data = reverse_geocode(lat, lon)
    if data and "address" in data:
        poi["address"] = estrai_address(data["address"])

    poi["quartiere_area_urbana"] = quartiere_from_point(lat, lon, quartieri_poligoni)
    return poi

# ----------------------------
# Main
# ----------------------------
def main():
    quartieri_poligoni = load_quartieri(QUARTIERI_JSON)

    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        pois = json.load(f)

    enriched = []
    for i, poi in enumerate(pois):
        print(f"{i+1}/{len(pois)}  {poi.get('nome_poi')}")
        enriched.append(arricchisci(poi, quartieri_poligoni))

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(enriched, f, ensure_ascii=False, indent=2)

    print(f"\nArricchimento completato → {OUTPUT_JSON}")

if __name__ == "__main__":
    main()

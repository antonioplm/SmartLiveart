import json
import pandas as pd
import sys, os
from math import radians, cos, sin, asin, sqrt

sys.path.append(r"packages")
from slkb_osm_cleaner.cleaner import clean_list


# ---------------------------
# Legge argomenti da riga di comando
# ---------------------------
if len(sys.argv) < 2:
    print("❌ Uso: python script.py <CITTÀ>")
    sys.exit(1)

CITY_NAME = sys.argv[1]
CITY_CAPITALIZED = " ".join(word.capitalize() for word in CITY_NAME.split())
city_slug = CITY_CAPITALIZED.lower().replace(" ", "_")
INPUT_JSON = f"{city_slug}_osm_address.json"
OUTPUT_JSON = f"{city_slug}_osm_poi_name.json"



def haversine(lat1, lon1, lat2, lon2):
    """Distanza in metri tra due coordinate geografiche"""
    R = 6371000
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    return 2 * R * asin(sqrt(a))


def merge_nearby_poi(pois, max_distance_m=50):
    """
    Unisce POI con stesso nome e distanza inferiore a max_distance_m (default 50 m)
    per ridurre duplicati visivi come fermate bus adiacenti.
    """
    merged = []
    fusi = []  # lista per tenere traccia dei POI fusi

    for poi in pois:
        found = False
        for m in merged:
            if (
                poi["nome_poi"] == m["nome_poi"]
                and haversine(poi["latitudine"], poi["longitudine"], m["latitudine"], m["longitudine"]) < max_distance_m
            ):
                found = True
                fusi.append((poi, m))  # salva la coppia: POI attuale e quello già presente
                break
        if not found:
            merged.append(poi)

    # stampa dettagliata dei POI fusi
    for poi, m in fusi:
        print(f"Fuso POI '{poi['nome_poi']}' ({poi['latitudine']},{poi['longitudine']}) "
              f"in '{m['nome_poi']}' ({m['latitudine']},{m['longitudine']})")

    print(f"Totale POI finali: {len(merged)}")
    return merged


def main():
    # Carica JSON arricchito
    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        pois = json.load(f)

    # Applica pulizia automatica nomi
    pois_clean = clean_list(pois)

    # Applica fusione dei POI troppo vicini con stesso nome
    pois_final = merge_nearby_poi(pois_clean, max_distance_m=50)

    # Salva JSON pulito
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(pois_final, f, ensure_ascii=False, indent=2)

    print("Pulizia e fusione completate")
    print(f"→ {OUTPUT_JSON}")
 

if __name__ == "__main__":
    main()

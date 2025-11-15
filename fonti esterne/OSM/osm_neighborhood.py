import requests
import sys
import time
import json

# --- Legge il nome del comune da riga di comando ---
if len(sys.argv) < 2:
    print("Uso: python script.py <NOME_COMUNE>")
    sys.exit(1)

CITY_NAME = sys.argv[1]
CITY_CAPITALIZED = " ".join(word.capitalize() for word in CITY_NAME.split())
city_slug = CITY_CAPITALIZED.lower().replace(" ", "_")

OUTPUT_JSON = f"{city_slug}_neighborhood.json"


# --- Lista server Overpass pubblici ---
OVERPASS_SERVERS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.openstreetmap.fr/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter"
]

# --- Funzione POST con retry e gestione risposta vuota ---
def post_with_retry(servers, query, retries=3, wait=5):
    last_error = None
    for server in servers:
        for attempt in range(retries):
            try:
                print(f"Richiesta a {server}, tentativo {attempt+1}/{retries}")
                response = requests.post(server, data={"data": query}, timeout=300)
                response.raise_for_status()
                if not response.text.strip():
                    raise Exception("Risposta vuota dal server")
                return response
            except Exception as e:
                print(f"Errore: {e}")
                last_error = e
                time.sleep(wait)
    raise Exception(f"Tutti i server falliti: {last_error}")

# --- Query per la relation del comune ---
query_relation = f"""
[out:json][timeout:180];
relation["name"="{CITY_CAPITALIZED}"]["admin_level"="8"];
out ids tags;
"""

# --- Ottieni la relation ---
try:
    response = post_with_retry(OVERPASS_SERVERS, query_relation)
    data = response.json()
except Exception as e:
    print(f"❌ Errore ottenimento relation: {e}")
    sys.exit(1)

elements = data.get("elements", [])
if not elements:
    print(f"Comune '{CITY_CAPITALIZED}' non trovato in OSM.")
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump({"error": "Comune non trovato", "quartieri_trovati": 0}, f, ensure_ascii=False, indent=2)
    sys.exit(0)

relation_id = elements[0]["id"]

# --- Query per ottenere i quartieri (più completa e dinamica) ---
query_quartieri = f"""
[out:json][timeout:300];
relation({relation_id});
map_to_area->.a;
(
  // Quartieri amministrativi (municipalità, circoscrizioni, ecc.)
  relation(area.a)["boundary"="administrative"]["admin_level"~"9|10"];

  // Zone urbane non amministrative ma denominate (es. Barra, Ponticelli, ecc.)
  relation(area.a)["place"~"suburb|neighbourhood|quarter"];
  way(area.a)["place"~"suburb|neighbourhood|quarter"];
);
out geom;
"""

# --- Esegui query quartieri ---
try:
    response = post_with_retry(OVERPASS_SERVERS, query_quartieri)
    data = response.json()
except Exception as e:
    print(f"Errore ottenimento quartieri: {e}")
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump({"error": str(e), "quartieri_trovati": 0}, f, ensure_ascii=False, indent=2)
    sys.exit(1)

# --- Salva direttamente il JSON raw ---
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

elements = data.get("elements", [])
print(f"File salvato in '{OUTPUT_JSON}' con {len(elements)} elementi.")

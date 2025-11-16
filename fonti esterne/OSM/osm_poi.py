#!/usr/bin/env python3
"""
osm_to_slkb_safe_full.py

Estrae POI da Overpass (città parametrica) evitando query troppo grandi,
classifica secondo la tassonomia fornita e genera:
 - osm_poi_<citta>.json

Mantiene tutte le funzionalità degli script originali, con limite globale sui POI.
"""

import requests
import time
import json
import uuid
import sys
from html import unescape

# ---------- CONFIG ----------
OVERPASS_SERVERS = [
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass.openstreetmap.fr/api/interpreter",
    "https://overpass-api.de/api/interpreter"
]
RETRY = 5
SLEEP_BETWEEN_RETRY = 10  # seconds
SLEEP_BETWEEN_QUERIES = 5  # secondi tra query successive

if len(sys.argv) < 2:
    print("Errore: devi specificare una città.")
    sys.exit(1)

CITY_NAME = sys.argv[1]
CITY_CAPITALIZED = " ".join(word.capitalize() for word in CITY_NAME.split())
city_slug = CITY_CAPITALIZED.lower().replace(" ", "_")
OUTPUT_JSON = f"{city_slug}_osm_poi.json"

# valori di default:
# MAX_POI = 0 (illimitato)
# FILTER_ONLY_WITH_LINKS = False (non limitato ai soli poi con web url

# MAX_POI (opzionale)
if len(sys.argv) > 2:
    try:
        MAX_POI = int(sys.argv[2])
    except ValueError:
        print("MAX_POI non valido, uso il default")
        MAX_POI = 0
else:
    MAX_POI = 0

# FILTER_ONLY_WITH_LINKS (opzionale)
if len(sys.argv) > 3:
    try:
      FILTER_ONLY_WITH_LINKS = sys.argv[3].lower() in ("1", "true", "yes")
    except ValueError:
        print("FILTER_ONLY_WITH_LINKS non valido, uso il default")
        FILTER_ONLY_WITH_LINKS = False
else:
    FILTER_ONLY_WITH_LINKS = False


# ---------- MAPPATURE ----------
OSM_TO_TOURISM = {
    ("amenity", "restaurant"): "Ristorante / Osteria / Trattoria",
    ("amenity", "fast_food"): "Ristorante / Osteria / Trattoria",
    ("amenity", "cafe"): "Pasticceria / Bar storico",
    ("amenity", "bar"): "Pasticceria / Bar storico",
    ("amenity", "pub"): "Pasticceria / Bar storico",
    ("shop", "wine"): "Enoteca / Cantina",
    ("shop", "deli"): "Ristorante / Osteria / Trattoria",
    ("tourism", "hotel"): "Hotel / Albergo",
    ("tourism", "guest_house"): "B&B / Affittacamere",
    ("tourism", "hostel"): "Ostello / Foresteria",
    ("tourism", "motel"): "Hotel / Albergo",
    ("railway", "station"): "Trasporto pubblico",
    ("railway", "halt"): "Fermata urbana",
    ("highway", "bus_stop"): "Fermata urbana",
    ("public_transport", "platform"): "Fermata urbana",
    ("public_transport", "stop_position"): "Fermata urbana",
    ("amenity", "parking"): "Parcheggio / Area sosta",
    ("tourism", "viewpoint"): "Belvedere / Punto panoramico",
    ("leisure", "park"): "Giardino storico / Orto botanico",
    ("amenity", "theatre"): "Evento teatrale / spettacolo",
    ("amenity", "cinema"): "Evento culturale",
    ("amenity", "arts_centre"): "Evento culturale",
    ("amenity", "community_centre"): "Vita locale / di quartiere",
    ("natural", "water"): "Spiaggia / Lago / Fiume"
}

OSM_TO_PERSISTENT = {
    ("tourism", "artwork"): "Opera d’arte",
    ("tourism", "sculpture"): "Statua / Monumento",
    ("tourism", "installation"): "Opera contemporanea",
    ("amenity", "restaurant"): "Locale enogastronomico",
    ("amenity", "cafe"): "Locale enogastronomico",
    ("amenity", "bar"): "Locale enogastronomico",
    ("tourism", "hotel"): "Struttura ricettiva",
    ("tourism", "guest_house"): "Struttura ricettiva diffusa",
    ("leisure", "park"): "Spazio verde / Parco",
    ("tourism", "viewpoint"): "Belvedere",
    ("railway", "station"): "Infrastruttura di trasporto",
    ("highway", "bus_stop"): "Infrastruttura di trasporto",
    ("amenity", "parking"): "Parcheggio",
    ("amenity", "theatre"): "Teatro",
    ("amenity", "cinema"): "Cinema"
}

TAG_PRIORITY = ["amenity", "shop", "tourism", "leisure", "public_transport", "highway", "railway", "natural"]

OUTPUT_FIELDS = [
    "poi_id","nome_poi","categoria_persistente","categoria_turistica","tag_k3",
    "autore_compilazione","data_compilazione","citta_comune","quartiere_area_urbana",
    "zona_turistica","sito_complesso_appartenenza","distanza_landmark","storia_cronologia",
    "architettura_arte_forma","rilevanza_culturale","curiosita","esperienza","atmosfera",
    "relazione_con_il_luogo","orari","tipo_accesso","contatti","sito_web","durata_consigliata",
    "attivita_consigliate","foto","video","modello_3d","audio","latitudine","longitudine",
    "tipo_geometria","address","wikipedia","wikidata","source"
]

# ---------- QUERY TEMPLATE ----------
TEMPLATE = '''
[out:json][timeout:90];
area["name"="{city}"]["boundary"="administrative"]["admin_level"="8"]->.a;
({element_selector}(area.a););
out center;
'''

# ---------- LISTA POI/TAG ----------  
POI_QUERIES = [

    # Belvedere / panorami
    'node["tourism"="viewpoint"]',
    'way["tourism"="viewpoint"]',

    # Parchi e giardini
    'node["leisure"="park"]',
    'way["leisure"="park"]',

    # Ristorazione e locali
    'node["amenity"~"restaurant|cafe|bar|pub|fast_food"]',
    'way["amenity"~"restaurant|cafe|bar|pub|fast_food"]',

    # Negozi tipici (vino, gastronomia locale)
    'node["shop"~"wine|deli"]',
    'way["shop"~"wine|deli"]',

    # Hotel / alloggi
    'node["tourism"~"hotel|guest_house|hostel|motel"]',
    'way["tourism"~"hotel|guest_house|hostel|motel"]',

    # Servizi utili al turista
    'node["amenity"~"atm|toilets|pharmacy|bank|clinic|post_office"]',

    # Trasporti
    'node["public_transport"~"stop_position|platform"]',
    'node["highway"="bus_stop"]',
    'node["railway"~"station|halt"]',
    'way["railway"~"station|halt"]',

    # Parcheggi
    'node["amenity"="parking"]',

    # Cultura leggera (non ICCD)
    'node["amenity"~"theatre|cinema|arts_centre|community_centre"]',
    'way["amenity"~"theatre|cinema|arts_centre|community_centre"]',

    # Storici "leggeri" ammessi
    'node["historic"="memorial"]',
    'node["historic"="statue"]',
    'node["historic"="wayside_shrine"]',
    'node["historic"="plaque"]',
    'node["man_made"="cross"]',

]


# ---------- HELPERS ----------    
def run_overpass_query(query):
    """
    Tenta la query su tutti i server alternativi finché non va a buon fine.
    """
    for server in OVERPASS_SERVERS:
        for attempt in range(1, RETRY+1):
            try:
                resp = requests.post(server, data={"data": query}, timeout=180)
                resp.raise_for_status()
                print(f"Query eseguita con successo su {server}")
                time.sleep(SLEEP_BETWEEN_QUERIES)  # riduce frequenza query
                return resp.json().get("elements", [])
            except Exception as e:
                print(f"Tentativo {attempt} su {server} fallito: {e}")
                time.sleep(SLEEP_BETWEEN_RETRY)
        print(f"Server {server} non ha risposto correttamente, passo al successivo...")
    print("❌ Tutti i server hanno fallito per questa query.")
    return []
    

def normalize_name(tags):
    name = tags.get("name")
    if name:
        return unescape(name).strip()
    key = next((k for k in TAG_PRIORITY if k in tags), None)
    val = tags.get(key) if key else None
    return val.capitalize() if val else "POI senza nome"

def build_k3_tags(tags):
    """
    Seleziona fino a 5 tag utili per arricchire l'esperienza turistica,
    evitando informazioni ICCD e metadati tecnici.
    """
    candidates = []

    # 1) Tag direttamente utili all'utente
    preferred_keys = [
        "cuisine",          # tipo cucina
        "internet_access",  # wifi
        "wheelchair",       # accessibilità
        "opening_hours",    # orari
        "payment:cards",    # pagamenti elettronici
        "viewpoint",        # punto panoramico
        "stars",            # stelle hotel
    ]
    for k in preferred_keys:
        if k in tags:
            candidates.append(f"{k}={tags[k]}")

    # 2) Tag descrittivi soft (non ICCD)
    soft_context_keys = [
        "amenity", "tourism", "shop", "leisure", "craft"
    ]
    for k in soft_context_keys:
        if k in tags and len(candidates) < 5:
            candidates.append(f"{k}={tags[k]}")

    # 3) Recupera eventuali tag "interessanti" ma non tecnici
    for k, v in tags.items():
        if len(candidates) >= 5:
            break
        if k.startswith("addr:") or k in ("name", "source", "wikidata", "wikipedia"):
            continue
        if k in ("historic", "building"):   # ← questi verranno gestiti da ICCD
            continue
        candidates.append(f"{k}={v}")

    return candidates[:5]

def pick_tag_priority(tags):
    for key in TAG_PRIORITY:
        if key in tags:
            return key, tags[key]
    return None, None

def map_to_tourism(tags):
    key, val = pick_tag_priority(tags)
    return OSM_TO_TOURISM.get((key,val), "Altro / Generico")

def map_to_persistent(tags):
    key, val = pick_tag_priority(tags)
    return OSM_TO_PERSISTENT.get((key,val), f"{key}:{val}" if key else "Altro")

def is_iccd_poi(tags):
    iccd_tags = [
        ("historic","monument"), ("historic","archaeological_site"),
        ("historic","castle"), ("historic","palace"), ("historic","city_gate"),
        ("historic","ruins"), ("building","church"), ("building","cathedral"),
        ("building","monastery"), ("tourism","museum")
    ]
    for k,v in iccd_tags:
        if tags.get(k) == v:
            return True
    return False

def process_elements(elements):
    rows = []
    for el in elements:
        tags = el.get("tags", {}) or {}
        if FILTER_ONLY_WITH_LINKS and ("wikidata" not in tags and "wikipedia" not in tags):
            continue
        if is_iccd_poi(tags):
            continue
        lat = el.get("lat") or el.get("center", {}).get("lat")
        lon = el.get("lon") or el.get("center", {}).get("lon")
        if lat is None or lon is None:
            continue
        poi = {
            "poi_id": str(uuid.uuid4()),
            "osm_type": el.get("type", ""),
            "osm_id": el.get("id", ""),
            "nome_poi": normalize_name(tags),
            "categoria_persistente": map_to_persistent(tags),
            "categoria_turistica": map_to_tourism(tags),
            "tag_k3": ";".join(build_k3_tags(tags)),
            "autore_compilazione": "",
            "data_compilazione": "",
            "citta_comune": CITY_CAPITALIZED,
            "quartiere_area_urbana": tags.get("addr:suburb",""),
            "zona_turistica": "",
            "sito_complesso_appartenenza": tags.get("is_in",""),
            "distanza_landmark": "",
            "storia_cronologia": "",
            "architettura_arte_forma": "",
            "rilevanza_culturale": "",
            "curiosita": "",
            "esperienza": "",
            "atmosfera": "",
            "relazione_con_il_luogo": "",
            "orari": "",
            "tipo_accesso": "",
            "contatti": tags.get("contact:phone",""),
            "sito_web": tags.get("website", tags.get("contact:website","")),
            "durata_consigliata": "",
            "attivita_consigliate": "",
            "foto": tags.get("image",""),
            "video": "",
            "modello_3d": "",
            "audio": "",
            "latitudine": lat,
            "longitudine": lon,
            "tipo_geometria": "point",
            "address": ", ".join([tags.get(k,"") for k in ("addr:street","addr:housenumber","addr:postcode","addr:city") if k in tags]),
            "wikipedia": tags.get("wikipedia", ""),
            "wikidata": tags.get("wikidata", ""),
            "source": "OpenStreetMap (ODbL)"
        }
        rows.append(poi)
    return rows

# ---------- MAIN ----------
def main():
    all_pois = []
    for el_selector in POI_QUERIES:
        query = TEMPLATE.format(city=CITY_CAPITALIZED, element_selector=el_selector)
        print(f"Eseguo query: {el_selector} ...")
        elements = run_overpass_query(query)
        processed = process_elements(elements)
        print(f"  POI trovati: {len(processed)}")
        all_pois.extend(processed)

    # 🔹 Deduplica per osm_type e osm_id        
    seen = set()
    pois_by_category = {}
    for poi in all_pois:
        key = (poi["osm_type"], poi["osm_id"])  # DEDUP REALMENTE CORRETTO
        if key in seen:
            continue
        seen.add(key)
        cat = poi["categoria_turistica"] or "Altro"
        if cat not in pois_by_category:
            pois_by_category[cat] = []
        pois_by_category[cat].append(poi)
        

    # 🔹 Selezione round-robin tra categorie fino a MAX_POI (0 o negativo = senza limite)
    unique_pois = []
    categories_with_pois = list(pois_by_category.keys())

    while (MAX_POI <= 0 or len(unique_pois) < MAX_POI) and categories_with_pois:
        for cat in categories_with_pois.copy():  # copia per iterare in sicurezza
            if pois_by_category[cat]:
                unique_pois.append(pois_by_category[cat].pop(0))
                if MAX_POI > 0 and len(unique_pois) >= MAX_POI:
                    break
            if not pois_by_category[cat]:  # rimuovi categoria vuota
                categories_with_pois.remove(cat)

    # Salva output
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(unique_pois, f, ensure_ascii=False, indent=2)

    print(f"Output creato: {OUTPUT_JSON} ({len(unique_pois)} POI)")
    
if __name__ == "__main__":
    main()    

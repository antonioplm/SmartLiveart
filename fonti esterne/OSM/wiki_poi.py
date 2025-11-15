#!/usr/bin/env python3

import sys
import json
import requests
import wikipediaapi
from urllib.parse import quote

import os

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False



# ---------------------------
# Argomenti CLI
# ---------------------------
if len(sys.argv) < 2:
    print("Uso: python enrich_poi_city.py <CITTÀ>")
    sys.exit(1)

CITY_NAME = sys.argv[1]
CITY_CAPITALIZED = " ".join(word.capitalize() for word in CITY_NAME.split())
city_slug = CITY_CAPITALIZED.lower().replace(" ", "_")
INPUT_JSON = f"{city_slug}_osm_poi_name.json"
OUTPUT_JSON = f"{city_slug}_poi.json"

print(f"Input: {INPUT_JSON}")
print(f"Output previsto: {OUTPUT_JSON}\n")


# ---------------------------
# Utility: parse tag_k3 → dict
# ---------------------------
def parse_tags(raw):
    tags = {}
    for part in raw.split(";"):
        if "=" in part:
            k, v = part.split("=", 1)
            tags[k.strip()] = v.strip()
    return tags


# ---------------------------
# OSM: contatti entro raggio
# ---------------------------
def get_osm_contact_data(lat, lon, radius=50):
    query = f"""
    [out:json];
    (
      node(around:{radius},{lat},{lon});
      way(around:{radius},{lat},{lon});
      relation(around:{radius},{lat},{lon});
    );
    out center tags;
    """
    try:
        r = requests.post("https://overpass-api.de/api/interpreter", data=query, timeout=20)
        data = r.json().get("elements", [])
    except:
        return {}

    for el in data:
        tags = el.get("tags", {})
        if any(k in tags for k in ["website", "contact:website", "opening_hours", "phone", "contact:phone"]):
            return {
                "sito_web": tags.get("contact:website") or tags.get("website", ""),
                "orari": tags.get("opening_hours", ""),
                "contatti": tags.get("contact:phone") or tags.get("phone", ""),
            }
    return {}


# ---------------------------
# Wikipedia init
# ---------------------------
wiki = wikipediaapi.Wikipedia(
    language="it",
    user_agent="SmartLiveArt-Bot/1.0 (mailto:info@smartliveart.it)"
)


# ---------------------------
# Wikidata helpers
# ---------------------------
def get_wikidata_metadata(qcode):
    url = f"https://www.wikidata.org/wiki/Special:EntityData/{qcode}.json"
    headers = {
        "User-Agent": "SmartLiveArt-Bot/1.0 (mailto:info@smartliveart.it)"
    }
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        data = r.json()
        entity = data.get("entities", {}).get(qcode)
        if not entity:
            print(f"⚠️ Wikidata Q{qcode} non trovato")
            return None, None, None

        # Descrizione (può essere None)
        desc_it = entity.get("descriptions", {}).get("it", {}).get("value")
        desc_en = entity.get("descriptions", {}).get("en", {}).get("value")
        short_desc = desc_it or desc_en

        # Titolo Wikipedia
        sitelinks = entity.get("sitelinks", {})
        title_it = sitelinks.get("itwiki", {}).get("title")
        title_en = sitelinks.get("enwiki", {}).get("title")
        wikipedia_title = title_it or title_en

        wikipedia_url = None
        if wikipedia_title:
            from urllib.parse import quote
            wikipedia_url = f"https://it.wikipedia.org/wiki/{quote(wikipedia_title.replace(' ', '_'))}"

        return short_desc, wikipedia_title, wikipedia_url

    except requests.exceptions.RequestException as e:
        print(f"Errore nel recuperare Wikidata Q{qcode}: {e}")
        return None, None, None
    except Exception as e:
        print(f"Errore inatteso Wikidata Q{qcode}: {e}")
        return None, None, None


def try_get_page_by_explicit_titles(wiki_title):
    if not wiki_title:
        return None
    page = wiki.page(wiki_title)
    return page if page.exists() else None


def get_wikipedia_page(nome, comune=None):
    # combinazioni per aumentare le probabilità
    candidates = [nome]
    if comune:
        candidates.append(f"{nome} ({comune})")
    # prefissi comuni
    for prefix in ["Stazione di", "Hotel", "Teatro", "Piazza", "Villa", "Parco"]:
        candidates.append(f"{prefix} {nome}")
        if comune:
            candidates.append(f"{prefix} {nome} ({comune})")

    for c in candidates:
        page = wiki.page(c)
        if page.exists():
            return page

    # fallback ricerca API
    search = f"https://it.wikipedia.org/w/api.php?action=query&list=search&format=json&utf8=&srsearch={quote(nome)}"
    try:
        r = requests.get(search, timeout=10).json()
    except:
        return None

    results = r.get("query", {}).get("search", [])
    if results:
        page = wiki.page(results[0]["title"])
        if page.exists():
            return page

    return None

def ai_summarize(text, target_chars=1200):
    """
    Riassume e riformula il testo in stile turistico, mantenendo coerenza e riducendo
    a target_chars caratteri circa. Usa GPT se disponibile, altrimenti una sintesi semplice.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    
    # Se c'è API key e openai è disponibile, usa GPT
    if api_key and OPENAI_AVAILABLE:
        openai.api_key = api_key
        prompt = (
            f"Riformula il seguente testo in stile turistico, chiaro e coerente, "
            f"non più lungo di {target_chars} caratteri:\n\n{text}"
        )
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=int(target_chars * 1.5 // 4)  # approssimazione: 1 token ~ 4 char
            )
            summarized_text = response.choices[0].message.content.strip()
            return summarized_text
        except Exception as e:
            print(f"Errore GPT, uso riduzione semplice: {e}")

    # Riduzione semplificata se GPT non disponibile
    if len(text) <= target_chars:
        return text

    sentences = text.split(". ")
    summary = ""
    for s in sentences:
        if len(summary) + len(s) + 2 > target_chars:
            break
        summary += s + ". "
    return summary.strip()

def extract_section(page, names):
    # Trova sezione corrispondente
    for section in page.sections:
        if section.title.lower() in [n.lower() for n in names]:
            full_text = section.text.strip()
            
            # Sezione trovata, riassumi/riformula (~40-50%)
            summary = ai_summarize(full_text, target_chars=1200)
            return summary
    return ""


import re

# Lista parole chiave dei POI generici da saltare
generic_keywords = [
    "parcheggio", "bancomat", "farmacia",
    "bar", "ristorante", "poste italiane", "belvedere",
    "piazza", "fontana", "parco", "stazione", "hotel",
    "villa", "teatro", "scuola", "ospedale",
    # combinazioni fermate
    "fermata treno",
    "fermata autobus",
    "fermata tram",
    "fermata metropolitana"
]

def is_generic_poi(poi):
    nome = poi["nome_poi"].lower()
    address = poi.get("address", "").lower()
    
    for keyword in generic_keywords:
        if nome.startswith(keyword):
            remainder = nome[len(keyword):].strip()
            # se il resto è vuoto o coincide con l'indirizzo, consideralo generico
            if not remainder or remainder in address:
                return True
    return False

def get_wikipedia_info(poi, coord_tolerance=0.01):
    """
    Recupera informazioni da Wikipedia per un POI senza modificare 'nome_poi'.
    Controlla che la pagina trovata sia coerente con la città o le coordinate.
    coord_tolerance: tolleranza in gradi decimali per confronto coordinate.
    """
 
    # --- SKIP POI GENERICI ---
    if is_generic_poi(poi):
        print(f"[SKIP] POI generico: {poi['nome_poi']}")
        return {}

    nome = poi["nome_poi"]
    citta = poi.get("citta_comune", "").lower()
    categoria = poi.get("categoria_persistente", "").lower()
    lat_poi = poi.get("latitudine")
    lon_poi = poi.get("longitudine")

    # 1. Prepara candidati
    candidates = [nome]
    if categoria:
        candidates.append(f"{categoria} {nome}")
    if citta:
        candidates.append(f"{nome} ({citta})")
        if categoria:
            candidates.append(f"{categoria} {nome} ({citta})")

    keywords = ["stazione", "station", "ferroviaria", "railway", "halt",
                "hotel", "teatro", "piazza", "villa", "parco"]
    for kw in keywords:
        candidates.append(f"{nome} {kw}")
        if citta:
            candidates.append(f"{nome} {kw} ({citta})")

    candidates = list({re.sub(r"\s+", " ", c).strip() for c in candidates})

    # 2. Prova Wikidata
    page = None
    wikidata_q = poi.get("wikidata")
    if wikidata_q:
        desc, wp_title, wp_url = get_wikidata_metadata(wikidata_q)
        if wp_title:
            page = try_get_page_by_explicit_titles(wp_title)
        if wp_url and not poi.get("wikipedia"):
            poi["wikipedia"] = wp_url

    # 3. Se Wikidata non ha sitelink, cerca candidati con città
    if not page and citta:
        for name in candidates:
            # assicura che la città sia presente nel nome
            if "(" not in name:
                name = f"{name} ({citta})"
            candidate_page = get_wikipedia_page(name)
            if candidate_page and candidate_page.exists():
                # Controllo sicurezza: testo o titolo contiene la città
                title_ok = citta in candidate_page.title.lower()
                text_ok = citta in candidate_page.text.lower()[:500]  # primi 500 caratteri
                if title_ok or text_ok:
                    page = candidate_page
                    break

    # 4. Controllo coordinate se possibile (richiede coordinate Wikipedia)
    # wikipediaapi non fornisce coordinate; si può integrare con API MediaWiki, opzionale

    if not page:
        return {}

    return {
        "storia_cronologia": extract_section(page, ["Storia", "Cenni storici"]),
        "architettura_arte_forma": extract_section(page, ["Descrizione", "Architettura", "Caratteristiche"]),
        "wikipedia": page.fullurl if page.exists() else ""
    }



# ---------------------------
# enrich_poi
# ---------------------------
import time

def enrich_poi(poi):
    # ---------------------------
    # 1. Parse tag_k3 → tags dict
    # ---------------------------
    poi["tags"] = parse_tags(poi.pop("tag_k3", ""))

    # ---------------------------
    # 2. Recupera Wikidata da campo o dai tag
    # ---------------------------
    wikidata_q = poi.get("wikidata") or poi["tags"].get("wikidata")
    if wikidata_q:
        poi["wikidata"] = wikidata_q  # normalizza
        desc, wp_title, wp_url = get_wikidata_metadata(wikidata_q)

        if wp_url and not poi.get("wikipedia"):
            poi["wikipedia"] = wp_url

    # ---------------------------
    # 3. Contatti OSM
    # ---------------------------
    poi.setdefault("sito_web", poi["tags"].get("website", ""))
    poi.setdefault("contatti", poi["tags"].get("phone", ""))
    poi.setdefault("orari", poi["tags"].get("opening_hours", ""))

    # ---------------------------
    # 4. Storia, architettura e Wikipedia 
    # ---------------------------
    t0 = time.time()
    wiki_info = get_wikipedia_info(poi)
    poi.update(wiki_info)
    print(f"[{poi['nome_poi']}] Wikipedia fetch: {time.time()-t0:.3f}s")

    return poi


# ---------------------------
# Caricamento + salvataggio
# ---------------------------
print("⏳ Carico POI...")
with open(INPUT_JSON, "r", encoding="utf-8") as f:
    pois = json.load(f)

print(f"POI da processare: {len(pois)}")

result = []
for i, poi in enumerate(pois):
    print(f" → ({i+1}/{len(pois)}) {poi['nome_poi']}")
    result.append(enrich_poi(poi))

print("\nSalvo output...")
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"\nCompletato! File generato: {OUTPUT_JSON}")

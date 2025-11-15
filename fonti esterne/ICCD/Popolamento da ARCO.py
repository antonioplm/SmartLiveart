import re
import json
import argparse
from SPARQLWrapper import SPARQLWrapper, JSON
from docx import Document

endpoint_url = "https://dati.cultura.gov.it/sparql"

# --- Leggi parametro città da linea di comando ---
parser = argparse.ArgumentParser()
parser.add_argument("--city", type=str, required=True, help="Nome della città da filtrare")
args = parser.parse_args()
city_name = args.city.lower()  # mettiamo in minuscolo per il filtro

# Query principale per ottenere POI e URI di dating
# Attualmente la query è esplicitamente limitata al grafo GRAPH <https://w3id.org/arco/data> { ... }
# Questo significa che il motore SPARQL cerca solo nel dataset “ArCo”, cioè quello dell’Istituto Centrale per il Catalogo e la Documentazione (ICCD) — https://w3id.org/arco
sparql_query = f"""
SELECT 
  ?s AS ?s_norm
  (SAMPLE(STR(?l)) AS ?label)
  (SAMPLE(?Categoria) AS ?Categoria)
  (SAMPLE(?Indirizzo) AS ?Indirizzo)
  (SAMPLE(COALESCE(?LatGeom, ?Lat)) AS ?Latitudine)
  (SAMPLE(COALESCE(?LongGeom, ?Long)) AS ?Longitudine)
  (SAMPLE(?Descrizione) AS ?Descrizione)
  (GROUP_CONCAT(DISTINCT STR(?Dating); separator=" | ") AS ?DatingURIs)
WHERE {{
  GRAPH <https://w3id.org/arco/data> {{
    ?s a arco:ImmovableCulturalProperty ;
       rdfs:label ?l ;
       a-loc:hasCulturalPropertyAddress ?address .
    ?address clvapit:hasCity ?city .
    ?city rdfs:label ?cityLabel .

    FILTER(LCASE(STR(?cityLabel)) = "{city_name}")

    OPTIONAL {{ ?address clvapit:fullAddress ?Indirizzo }}
    OPTIONAL {{ ?address geo:lat ?Lat }}
    OPTIONAL {{ ?address geo:long ?Long }}
    OPTIONAL {{ 
      ?s clvapit:hasGeometry ?geom .
      ?geom a-loc:hasCoordinates ?coords .
      OPTIONAL {{ ?coords a-loc:lat ?LatGeom }}
      OPTIONAL {{ ?coords a-loc:long ?LongGeom }} 
    }}
    OPTIONAL {{ ?s dc:description ?Descrizione }}
    OPTIONAL {{ ?s dc:type ?Categoria }}
    OPTIONAL {{ ?s a-cd:hasDating ?Dating }}

    BIND(REPLACE(STR(?s), ".*/", "") AS ?rawId)
    BIND(REPLACE(?rawId, "[^0-9]+$", "") AS ?idBase)
  }}
}}
GROUP BY ?idBase ?s
"""


categoria_map = {
    # Architetture religiose
    "chiesa": "Chiesa",
    "basilica": "Basilica / Duomo",
    "cattedrale": "Basilica / Duomo",
    "cappella": "Cappella / Oratorio",
    "oratorio": "Cappella / Oratorio",
    "monastero": "Monastero / Convento",
    "convento": "Monastero / Convento",
    "canonica": "Monastero / Convento",

    # Architettura civile e militare / Palazzo storico
    "palazzo": "Palazzo storico",
    "villa": "Palazzo storico",
    "castello": "Castello / Fortezza",
    "torre": "Torre / Campanile",
    "porta": "Porta / Mura urbane",
    "mura": "Porta / Mura urbane",
    "piazza": "Piazza / Spazio urbano",
    "ponte": "Ponte / Acquedotto",
    "acquedotto": "Ponte / Acquedotto",
    "convitto": "Palazzo storico",
    "casa privata": "Palazzo storico",
    "casa": "Palazzo storico",
    "edificio residenziale": "Palazzo storico",
    "rifugio": "Palazzo storico",
    "scuola": "Palazzo storico",
    "accademia": "Palazzo storico",
    "orfanotrofio": "Palazzo storico",
    "canonico": "Palazzo storico",
    "mercato": "Piazza / Spazio urbano",
    "architettura dello stato": "Palazzo storico",
    "edificio-residenziale": "Palazzo storico",
       
    # Musei e Collezioni
    "museo": "Museo",
    "galleria": "Mostra / Galleria",
    "mostra": "Mostra / Galleria",

    # Archeologia
    "area archeologica": "Area archeologica",
    "monumento antico": "Monumento antico",

    # Arte e Scultura
    "statua": "Statua / Monumento",
    "monumento": "Statua / Monumento",
    "fontana": "Fontana",
    "opera d’arte": "Opera d’arte",
    "dipinto": "Opera d’arte",
    "affresco": "Opera d’arte",
    "scultura": "Opera d’arte",
    "mosaico": "Opera d’arte",

    # Paesaggio e Natura
    "parco": "Parco / Giardino",
    "giardino": "Parco / Giardino",
    "belvedere": "Belvedere / Panorama",
    "panorama": "Belvedere / Panorama",
    "riserva naturale": "Riserva naturale",

    # Memoria e Identità
    "monumento ai caduti": "Luogo simbolico / Memoria",
    "lapide": "Luogo simbolico / Memoria",

    # Area urbana
    "centro storico": "Piazza / Spazio urbano",
    
    # Convitto / Casa privata ecc.
    "convittorio": "Palazzo storico",
    "casa-privata": "Palazzo storico",

    # Contemporaneo e urbano
    "installazione": "Opera contemporanea",
    "arredo urbano": "Elemento urbano (generico)",

    # Beni immateriali e territoriali
    "tradizione": "Tradizione / Rituale / Folklore",
    "rituale": "Tradizione / Rituale / Folklore",
    "folklore": "Tradizione / Rituale / Folklore",
    "percorso urbano": "Percorso urbano esperienziale",
    "itinerario culturale": "Itinerario culturale territoriale",

    # Servizi e spazi contemporanei
    "centro eventi": "Centro eventi / Teatro / Auditorium",
    "teatro": "Centro eventi / Teatro / Auditorium",
    "auditorium": "Centro eventi / Teatro / Auditorium",
    "spazio pubblico": "Spazio pubblico contemporaneo",
}

# Vocabolario tag K3
k3_vocab = {
    "preistorico": "TE:periodo", "protostorico": "TE:periodo", "antico": "TE:periodo",
    "medievale": "TE:periodo", "rinascimentale": "TE:periodo", "barocco": "TE:periodo",
    "neoclassico": "TE:periodo", "moderno": "TE:periodo", "contemporaneo": "TE:periodo",
    "romanico": "TE:stile", "gotico": "TE:stile", "barocco": "TE:stile", "neoclassico": "TE:stile",
    "pietra": "TE:materiale", "marmo": "TE:materiale", "legno": "TE:materiale", "bronzo": "TE:materiale",
    "affresco": "TE:tecnica", "mosaico": "TE:tecnica",
    "religione": "TE:tema", "memoria": "TE:tema", "tradizione": "TE:tema", "storia": "TE:tema",
    "comunità": "TE:tema", "territorio": "TE:tema", "paesaggio": "TE:tema", "artigianato": "TE:tema",
    "musica": "TE:tema", "enogastronomia": "TE:tema"
}

# Lista di parole comuni da ignorare nei tag liberi
stopwords = set([
    "della","delle","del","dell","dei","da","di","e","il","la","le","lo","un","una","in","sul","sul","con","per","al","ai","dal","dai","sul","sulla","sant", "santa", "san"
])

def clean_poi_name(nome_poi: str) -> str:
    """Rimuove la parte dopo il trattino nel Nome POI."""
    if '-' in nome_poi:
        nome_poi = nome_poi.split('-')[0].strip()
    return nome_poi

def generate_tags(nome_poi: str, descrizione: str, storia: str, max_k3=5, max_free=3):
    nome_poi = clean_poi_name(nome_poi)
    testo = f"{nome_poi} {descrizione} {storia}".lower()

    # --- Tag dal vocabolario K3 ---
    k3_tags = []
    for keyword in k3_vocab:
        if re.search(rf'\b{re.escape(keyword)}\b', testo) and keyword not in k3_tags:
            k3_tags.append(keyword)
        if len(k3_tags) >= max_k3:
            break

    # --- Tag liberi significativi ---
    words = re.findall(r'\b[a-zA-Z]{4,}\b', testo)  # parole di almeno 4 lettere
    free_tags = []
    for w in words:
        if w not in k3_tags and w not in free_tags and w not in stopwords:
            free_tags.append(w)
        if len(free_tags) >= max_free:
            break

    return k3_tags + free_tags

def run_sparql_query(endpoint, query):
    print(f"query: {query}")
    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    try:
        results = sparql.query().convert()
        return results["results"]["bindings"]
    except Exception as e:
        print("Errore SPARQL:", e)
        return []

def fetch_dating_details(dating_uri):
    """
    Restituisce solo label in italiano, time e description
    dai Dating URI, eliminando duplicati.
    """
    query = f"""
    SELECT ?label ?lang ?time ?timeLabel ?altTime ?descr
    WHERE {{
      GRAPH <https://w3id.org/arco/data> {{
        <{dating_uri}> <https://w3id.org/arco/ontology/context-description/hasDatingEvent> ?event .
        OPTIONAL {{ ?event <http://www.w3.org/2000/01/rdf-schema#label> ?label . }}
        OPTIONAL {{
          ?event <https://w3id.org/arco/ontology/context-description/specificTime> ?time .
          OPTIONAL {{ ?time <http://www.w3.org/2000/01/rdf-schema#label> ?timeLabel . }}
        }}
        OPTIONAL {{ ?event <http://www.w3.org/2006/time#atTime> ?altTime . }}
        OPTIONAL {{ ?event <https://w3id.org/arco/ontology/core/description> ?descr . }}
      }}
      BIND(LANG(?label) AS ?lang)
    }}
    """

    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    try:
        res = sparql.query().convert()
        bindings = res.get("results", {}).get("bindings", [])

        triples = []
        seen = set()  # per eliminare duplicati basati solo su descr

        # Itera i binding in ordine inverso
        for r in bindings[::-1]:
            label = r.get("label", {}).get("value", "")
            lang = r.get("lang", {}).get("value", "")

            # Prendi solo label in italiano
            if lang != "it" or not label:
                continue

            # time: preferenza rdfs:label, altrimenti URI pulito
            if r.get("timeLabel", {}).get("value"):
                time = r["timeLabel"]["value"]
            elif r.get("time", {}).get("value"):
                time = r["time"]["value"].split("/")[-1].replace("-", " - ")
            else:
                time = ""

            altTime = r.get("altTime", {}).get("value", "")
            descr = r.get("descr", {}).get("value", "")

            # usa solo descr come chiave per i duplicati
            if descr in seen:
                continue
            seen.add(descr)

            triples.append((label, time or altTime, descr))

        return triples

    except Exception as e:
        print(f"Errore fetch_dating_details per {dating_uri}: {e}")
        return []

def create_docx(data, city_name, filename=None):

    if filename is None:
        # costruisci il nome del file includendo la città
        safe_city = city_name.replace(" ", "_")  # sostituisci spazi con underscore
        filename = f"Dati_ICCD_{safe_city}.docx"
        
    doc = Document()
    doc.add_heading("Dati da ICCD", level=0)

    for poi in data:
        doc.add_heading(poi.get("label", {}).get("value", "POI sconosciuto"), level=1)
        
        table = doc.add_table(rows=1, cols=2)
        table.style = 'Table Grid'
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = "Nome Campo"
        hdr_cells[1].text = "Valore"

        # POI ID
        row = table.add_row().cells
        row[0].text = "POI ID"
        row[1].text = poi.get("s_norm", {}).get("value", "")

        # Nome POI
        row = table.add_row().cells
        row[0].text = "Nome POI"
        row[1].text = poi.get("label", {}).get("value", "")
        
        # Categoria Persistente
        row = table.add_row().cells
        row[0].text = "Categoria Persistente"
        arco_categoria = poi.get("Categoria", {}).get("value", "")
        categoria_iccd = map_categoria(arco_categoria)
        row[1].text = categoria_iccd

        # --- RIGA TAG ---
        row = table.add_row().cells
        row[0].text = "Tag"

        # Storia e cronologia
        row = table.add_row().cells
        row[0].text = "Storia e cronologia"
        
        storia_text = ""
        descr_seen = set()  # per evitare duplicati di descr

        dating_uris = poi.get("DatingURIs", {}).get("value", "").split(" | ")

        for uri in dating_uris:  # scorri tutti gli URI
            uri = uri.strip()
            if not uri:
                continue

            triples = fetch_dating_details(uri)
            for label, time, descr in triples:
                # aggiungi solo se almeno uno dei campi non è vuoto
                if any([label, time, descr]):
                    # se la descr è già stata aggiunta, salta
                    if descr in descr_seen:
                        continue
                    descr_seen.add(descr)

                    # formattazione desiderata
                    storia_text += f"{label}, {time}\n{descr}\n\n"

        row[1].text = storia_text.strip()

        # Architettura / Arte / Forma
        row = table.add_row().cells
        row[0].text = "Architettura / Arte / Forma"
        row[1].text = poi.get("Descrizione", {}).get("value", "")

        # genera o recupera i tag del POI
        nome_poi = poi.get("label", {}).get("value", "")
        descrizione = poi.get("Descrizione", {}).get("value", "")
        tags_list = generate_tags(nome_poi, descrizione, storia_text.strip())

        # unisci i tag in una stringa separata da virgola
        row[1].text = ", ".join(tags_list)
        print(f"tag: {row[1].text}")

        # Latitudine / Longitudine
        row = table.add_row().cells
        row[0].text = "Latitudine"
        row[1].text = poi.get("Latitudine", {}).get("value", "")
        row = table.add_row().cells
        row[0].text = "Longitudine"
        row[1].text = poi.get("Longitudine", {}).get("value", "")

    doc.save(filename)
    print(f"DOCX generato: {filename}")


def map_categoria(arco_categoria):
    """
    Mappa un valore qualsiasi di Categoria ARCO alla Categoria Persistente ICCD.
    Usa keyword matching: se una keyword è presente nel testo, restituisce la categoria ICCD corrispondente.
    Se non trova corrispondenza, restituisce il valore originale.
    """
    arco_categoria_lower = arco_categoria.lower()

    for keyword, categoria_iccd in categoria_map.items():
        if keyword in arco_categoria_lower:
            return categoria_iccd

    print(f"fallback categoria: {arco_categoria}")
    # fallback: restituisci la Categoria originale della query
    return arco_categoria


if __name__ == "__main__":
    results = run_sparql_query(endpoint_url, sparql_query)
    create_docx(results, city_name)

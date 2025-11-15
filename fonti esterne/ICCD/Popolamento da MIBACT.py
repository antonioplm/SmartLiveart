import argparse
from SPARQLWrapper import SPARQLWrapper, JSON
from docx import Document

ENDPOINT = "https://dati.cultura.gov.it/sparql"


def build_query(city):
    city = city.lower().replace('"', '\\"')  # escape degli eventuali doppi apici

    query = """
SELECT ?s ?Nome_Istituzionale ?Descrizione ?Indirizzo
       ?Latitudine ?Longitudine
       (GROUP_CONCAT(DISTINCT ?Prenotazioni; separator=" | ") AS ?PrenotazioniAggregata)
       (GROUP_CONCAT(DISTINCT ?Orari_di_apertura; separator=" | ") AS ?OrariAggregati)
       (GROUP_CONCAT(DISTINCT ?Biglietti; separator=" | ") AS ?BigliettiAggregati)
       (GROUP_CONCAT(DISTINCT ?Servizi; separator=" | ") AS ?ServiziAggregati)
       (GROUP_CONCAT(DISTINCT ?Telefono; separator=" | ") AS ?TelefoniAggregati)
       (GROUP_CONCAT(DISTINCT ?Email; separator=" | ") AS ?EmailAggregati)
       (GROUP_CONCAT(DISTINCT ?WebSite; separator=" | ") AS ?WebSiteAggregati)
WHERE {{
  GRAPH <http://dati.beniculturali.it/mibact/luoghi> {{
    ?s rdf:type cis:CulturalInstituteOrSite ;
       cis:institutionalCISName ?Nome_Istituzionale .
    
    OPTIONAL {{ ?s l0:description ?Descrizione }}
    
    OPTIONAL {{ 
      ?s cis:hasSite [cis:siteAddress ?address] .
      OPTIONAL {{ ?address clvapit:fullAddress ?Indirizzo }}
    }}

    OPTIONAL {{ ?s geo:lat ?Latitudine }}
    OPTIONAL {{ ?s geo:long ?Longitudine }}

    OPTIONAL {{ ?s accessCondition:hasAccessCondition [rdf:type accessCondition:Booking ; rdfs:label ?Prenotazioni] }}
    OPTIONAL {{ ?s accessCondition:hasAccessCondition [rdf:type accessCondition:OpeningHoursSpecification ; l0:description ?Orari_di_apertura] }}
    OPTIONAL {{ ?s cis:providesService [l0:name ?Servizi] }}

    OPTIONAL {{
      ?s potapit:hasTicket ?ticket .
      ?offer potapit:includes ?ticket ;
             potapit:hasPriceSpecification [potapit:hasCurrencyValue ?Biglietti]
    }}

    OPTIONAL {{ 
      ?s smapit:hasOnlineContactPoint ?contactPoint .
      OPTIONAL {{ ?contactPoint smapit:hasTelephone [smapit:telephoneNumber ?Telefono] }}
      OPTIONAL {{ ?contactPoint smapit:hasEmail [smapit:emailAddress ?Email] }}
      OPTIONAL {{ ?contactPoint smapit:hasWebSite [smapit:URL ?WebSite] }} 
    }}

    FILTER(BOUND(?Indirizzo) && CONTAINS(LCASE(?Indirizzo), "{city}"))
  }}
}}
GROUP BY ?s ?Nome_Istituzionale ?Descrizione ?Indirizzo ?Latitudine ?Longitudine
"""
    return query.format(city=city)


# ---------------------------
# SPARQL QUERY EXECUTION
# ---------------------------
def run_sparql(query):
    sparql = SPARQLWrapper(ENDPOINT)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    try:
        res = sparql.query().convert()
        return res["results"]["bindings"]
    except Exception as e:
        print("Errore SPARQL:", e)
        return []


# ---------------------------
# DOCX CREATION
# ---------------------------
def create_doc(data, city, filename=None):

    safe_city = city.replace(" ", "_")

    if not filename:
        filename = f"Dati_MiBACT_{safe_city}.docx"

    doc = Document()
    doc.add_heading(f"Dati MiBACT – Luoghi della Cultura ({city})", level=0)

    for row in data:

        nome = row.get("Nome_Istituzionale", {}).get("value", "")
        doc.add_heading(nome, level=1)

        table = doc.add_table(rows=1, cols=2)
        table.style = "Table Grid"
        hdr = table.rows[0].cells
        hdr[0].text = "Campo"
        hdr[1].text = "Valore"

        def add(label, key):
            r = table.add_row().cells
            r[0].text = label
            r[1].text = row.get(key, {}).get("value", "")

        add("URI", "s")
        add("Nome istituzionale", "Nome_Istituzionale")
        add("Descrizione", "Descrizione")
        add("Indirizzo", "Indirizzo")
        add("Latitudine", "Latitudine")
        add("Longitudine", "Longitudine")
        add("Prenotazioni", "PrenotazioniAggregata")
        add("Orari di apertura", "OrariAggregati")
        add("Biglietti", "BigliettiAggregati")
        add("Servizi", "ServiziAggregati")
        add("Telefono", "TelefoniAggregati")
        add("Email", "EmailAggregati")
        add("Sito web", "WebSiteAggregati")

    doc.save(filename)
    print(f"\n📄 Documento generato: {filename}")


# ---------------------------
# MAIN
# ---------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--city", required=True, help="Nome della città per filtrare gli indirizzi")
    args = parser.parse_args()

    query = build_query(args.city)
    results = run_sparql(query)
    create_doc(results, args.city)

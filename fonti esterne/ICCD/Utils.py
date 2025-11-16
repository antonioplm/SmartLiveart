import re
import argparse
import spacy
from collections import Counter

# spinner_task
import threading
import itertools
import sys
import time


# Endpoint SPARQL comune
ENDPOINT = "https://dati.cultura.gov.it/sparql"

def get_city_from_args():
    """
    Legge il parametro --city dalla linea di comando.
    Restituisce la città in minuscolo e capitalizzata.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--city", type=str, required=True, help="Nome della città da filtrare")
    args = parser.parse_args()
    
    city_lowered = args.city.lower()
    city_capitalized = args.city.title()
    return city_lowered, city_capitalized
    

class Spinner:
    def __init__(self, message="Caricamento..."):
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=spinner_task, args=(self.stop_event, message))

    def __enter__(self):
        self.thread.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop_event.set()
        self.thread.join()



def spinner_task(stop_event, message="Caricamento..."):
    """
    Mostra uno spinner animato finché stop_event non è impostato.
    
    Args:
        stop_event (threading.Event): evento per fermare lo spinner
        message (str): messaggio da mostrare accanto allo spinner
    """
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if stop_event.is_set():
            break
        sys.stdout.write(f'\r{message} {c}')
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write(f'\r{message} completato!        \n')



# carica modello italiano (una sola volta)
nlp = spacy.load("it_core_news_sm")

# Vocabolario K3 e stopwords
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

stopwords = set([
    "sant","santa","san","s.","s",
    "elemento","orizzontale","verticale","realizzazione","attuale","presente","oggi",
    "schema","progetto","piano","costruzione","struttura","copertura","pavimentazione","altro"
])

italian_prepositions = {
    "di","a","da","in","con","su","per","tra","fra",
    "del","della","dello","dei","degli","delle",
    "al","allo","alla","ai","agli","alle",
    "dal","dallo","dalla","dai","dagli","dalle",
    "nel","nello","nella","nei","negli","nelle",
    "sul","sullo","sulla","sui","sugli","sulle"
}

def generate_tags(nome_poi, descrizione, storia, arch_text, city_lowered="", num_tags=6, exclude_tags=None):
    """
    Restituisce una lista di tag rilevanti per un POI.
    city_lowered: nome della città in minuscolo, da escludere dai tag
    """
    if exclude_tags is None:
        exclude_tags = []

    exclude_lower = set(t.lower() for t in exclude_tags)

    def contains_stopword_internal(text):
        parts = text.lower().split()
        return any(p in stopwords or p in italian_prepositions for p in parts)

    # testo completo
    testo = f"{nome_poi} {descrizione} {storia} {arch_text}"
    # print(f"testo: {testo}")
    doc = nlp(testo)

    # K3 tags
    testo_lower = testo.lower()
    k3_tags = [
        kw for kw in k3_vocab
        if kw.lower() != city_lowered
        and kw.lower() not in exclude_lower
        and re.search(rf'\b{re.escape(kw.lower())}\b', testo_lower)
    ]

    # Named Entities
    entity_tags = []
    for ent in doc.ents:
        cleaned = re.sub(r'[^\w\s\.-]', ' ', ent.text.strip())
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        if not cleaned or cleaned.lower() == city_lowered or cleaned.lower() in exclude_lower:
            continue
        words = [w for w in cleaned.split() if w.lower() not in italian_prepositions]
        if not words:
            continue
        cleaned = " ".join(words)
        if re.search(r'(are|ere|ire|ato|uto|ito|ando|endo|e)$', cleaned.lower()):
            continue
        entity_tags.append(cleaned)

    # Token liberi
    words = []
    for token in doc:
        t = token.text
        if (token.is_stop or token.is_punct or token.like_num
            or token.pos_ in ["VERB", "AUX", "ADP", "CCONJ", "DET", "PRON"]
            or len(t) < 3):
            continue
        clean = re.sub(r'[^\w\-]', ' ', t).strip()
        if not clean or contains_stopword_internal(clean):
            continue
        low = clean.lower()
        if low in stopwords or low == city_lowered or low in italian_prepositions or low in exclude_lower:
            continue
        words.append(clean)

    freq = Counter(words)

    # arch_terms: bigram/trigram
    arch_tokens = re.sub(r'[^\w\s\-]', ' ', arch_text).lower().split()
    arch_terms = set(arch_tokens)
    for i in range(len(arch_tokens)-1):
        arch_terms.add(f"{arch_tokens[i]} {arch_tokens[i+1]}")
    for i in range(len(arch_tokens)-2):
        arch_terms.add(f"{arch_tokens[i]} {arch_tokens[i+1]} {arch_tokens[i+2]}")

    candidate_tokens = list(set(words + entity_tags + k3_tags))

    def token_score(word):
        wl = word.lower()
        proper_bonus = 25 if (word[0].isupper() and not word.isupper()) else 0
        tech_bonus = 20 if any(wl in t for t in arch_terms) else 0
        length_bonus = min(len(wl), 12)
        freq_bonus = freq.get(wl, 0)
        stop_penalty = -10 if len(wl) <= 3 else 0
        return proper_bonus + tech_bonus + length_bonus + freq_bonus + stop_penalty

    candidate_tokens_sorted = sorted(candidate_tokens, key=token_score, reverse=True)

    tags_cleaned = []
    seen_lower = set(exclude_lower)
    for t in candidate_tokens_sorted:
        t_lower = t.lower()
        if any(t_lower in tag.lower() or tag.lower() in t_lower for tag in tags_cleaned):
            continue
        if len(t.split()) == 1 and any(t_lower in ent.lower() for ent in entity_tags):
            continue
        if t_lower not in seen_lower:
            tags_cleaned.append(t)
            seen_lower.add(t_lower)
        if len(tags_cleaned) >= num_tags:
            break

    return tags_cleaned[:num_tags]

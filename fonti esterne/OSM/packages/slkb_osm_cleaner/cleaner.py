from .mappings import GENERIC_NAMES

def is_generic(name: str) -> bool:
    """Verifica se il nome è generico (es. 'Park', 'Bar', 'Farmacia', ecc.)"""
    if not name:
        return False
    return name.strip().lower() in GENERIC_NAMES


def normalize_name(name: str, indirizzo: str = "", categoria: str = "", quartiere: str = "") -> str:
    """
    Normalizza i nomi generici (es. 'Farmacia', 'Bar', 'Pizzeria') arricchendoli con
    informazioni come indirizzo, quartiere o categoria.
    """
    n = name.strip()
    if not is_generic(n):
        return n

    base_name = n.capitalize()
    via = indirizzo.split(",")[0].strip() if indirizzo else ""
    quart = quartiere.strip() if quartiere else ""

    # Costruzione dinamica del nome
    if via and quart:
        return f"{base_name} ({via}, {quart})"
    elif via:
        return f"{base_name} ({via})"
    elif quart:
        return f"{base_name} — {quart}"
    elif categoria:
        return f"{base_name} — {categoria}"
    else:
        return base_name

def apply_name_cleaning(poi):
    """
    Normalizza nome_poi usando address/tag.
    Mantiene tutte le funzionalità precedenti e aggiunge la normalizzazione
    per categorie generiche (es. post_office -> Ufficio Postale).
    """

    import re
    import unicodedata

    name = (poi.get("nome_poi") or "").strip()
    original_name = name  # salvo il nome originale
    tag = (poi.get("tag_k3") or "").lower()
    categoria = (poi.get("categoria_persistente") or "").strip()
    address = (poi.get("address") or "").strip()
    city = (poi.get("citta_comune") or "").strip()
    rfi_count = poi.get("rfi_count", 1)  # fallback a 1

    # ----------------------------
    # Traduzioni inglese → italiano
    # ----------------------------
    EN_TO_IT = {
        "parking": "Parcheggio", "restaurant": "Ristorante", "bar": "Bar",
        "cafe": "Caffè", "fast food": "Fast food", "hotel": "Hotel",
        "guest house": "Affittacamere", "bed & breakfast": "B&B",
        "pharmacy": "Farmacia", "bank": "Banca", "atm": "Bancomat",
        "post office": "Ufficio postale", "post_office": "Ufficio postale",
        "theatre": "Teatro", "cinema": "Cinema", "viewpoint": "Belvedere",
        "platform": "Piattaforma", "stop": "Fermata", "station": "Stazione",
        "park": "Parco", "hospital": "Ospedale", "clinic": "Clinica",
        "school": "Scuola", "university": "Università", "library": "Biblioteca",
        "museum": "Museo", "supermarket": "Supermercato", "marketplace": "Mercato",
        "church": "Chiesa", "chapel": "Cappella",
    }

    name_clean = name.lower().replace("_", " ").strip()
    for en, it in EN_TO_IT.items():
        if name_clean == en:
            name = it
            break
        if name_clean.startswith(en + " "):
            name = re.sub(rf"(?i)^{en}\b", it, name, 1)
            break

    # ----------------------------
    # Pulizia indirizzo (short)
    # ----------------------------
    def clean_address_for_name(addr):
        if not addr:
            return ""
        a = re.sub(r"\b\d{5}\b", "", addr)               # rimuove CAP
        if city:
            a = re.sub(rf"(?i)\b{re.escape(city)}\b", "", a)
        a = re.sub(r"[()]", "", a)
        a = re.sub(r"\s{2,}", " ", a)
        return a.strip(" ,")

    via_clean_short = clean_address_for_name(address)

    # ----------------------------
    # Utility: smart_capitalize (gestisce apostrofi e iniziali)
    # ----------------------------
    def smart_capitalize(s: str) -> str:
        if not s:
            return s
        exceptions = {"di", "del", "della", "dei", "da", "e", "a", "al", "ai", "alle",
                      "degli", "delle", "nel", "sul", "sulla"}

        def cap_word(w):
            if "." in w and len(w) <= 6:
                parts = [p for p in w.split(".") if p]
                if len(parts) == 2 and len(parts[0]) == 1:
                    return f"{parts[0].upper()}. {parts[1].capitalize()}"
            if "'" in w:
                pre, post = w.split("'", 1)
                return f"{pre.capitalize()}'{post.capitalize()}"
            return w.capitalize()

        words = s.split()
        out = []
        for i, w in enumerate(words):
            wl = w.lower()
            if i != 0 and wl in exceptions:
                out.append(wl)
            else:
                out.append(cap_word(w))
        return " ".join(out)

    # ----------------------------
    # Utility: normalize_for_match, strip_city_from_name
    # ----------------------------
    def normalize_for_match(s):
        s = (s or "").lower()
        s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
        return re.sub(r"[^a-z0-9 ]+", " ", s).strip()

    def strip_city_from_name(name_str, city_str):
        if not city_str:
            return name_str
        n = re.sub(rf"(?i)^\s*{re.escape(city_str)}\s*[-,–:]?\s*", "", name_str.strip())
        n = re.sub(rf"(?i)\s*[-,–:]\s*{re.escape(city_str)}\s*$", "", n)
        return n.strip()

    # ----------------------------
    # Utility: Decide se aggiungere la via in base alla sovrapposizione di parole significative.
    # ----------------------------
    def should_add_via(name_str, via_str):
        stopwords = {"via", "viale", "corso", "piazza", "largo", "vico", "vicolo",
                     "del", "della", "di", "dei", "da", "san", "santa", "santo", "ss"}

        def words(s):
            return set(w for w in normalize_for_match(s).split() if w not in stopwords)

        name_words = words(name_str)
        via_words = words(via_str)

        if not via_words:
            return False

        common = name_words & via_words

        # 🌟 Caso speciale: l'unica parola in comune è l’ultima del nome (tipico dei cognomi nelle vie)
        if len(common) == 1:
            last_name_word = list(name_words)[-1]
            if last_name_word in common:
                return False

        ratio = len(common) / len(via_words)

        # Se più del 50% della via è già nel nome → NON aggiungere
        return ratio < 0.5

    # ----------------------------
    # Utility: fix_initials_in_name usa smart_capitalize
    # ----------------------------
    def fix_initials_in_name(s: str) -> str:
        if not s:
            return s
        # Gestione iniziali singole e multiple mantenendo capitalizzazione del resto
        s = re.sub(r'\b([A-Za-z])\.\s*([A-Za-z][\w\'\-]*)',
                   lambda m: f"{m.group(1).upper()}. {smart_capitalize(m.group(2))}", s)
        s = re.sub(r'\b((?:[A-Za-z]\.){2,})(\s*[A-Za-z].+)',
                   lambda m: " ".join(c.upper()+'.' for c in re.findall(r'[A-Za-z]', m.group(1))) + " " + smart_capitalize(m.group(2)),
                   s)
        return s

    # ----------------------------
    # Parsing tag_k3 -> dict
    # ----------------------------
    def parse_tag_dict(tag_str):
        d = {}
        for p in tag_str.split(";"):
            if "=" in p:
                k, v = p.split("=", 1)
                d[k.strip().lower()] = v.strip().lower()
        return d

    tag_dict = parse_tag_dict(tag)

    # ----------------------------
    # Trasporto pubblico (logica invariata)
    # ----------------------------
    FERROVIA_SUBURBANA_KEYWORDS = [
        "circumvesuviana", "eav", "trenord", "ferrovienord", "ferrovie nord", "fnm",
        "ferrovie appulo lucane", "ferrovie appulo-lucane", "fal",
        "ferrovie della calabria", "ferrovie calabria", "fcal",
        "ferrovie sud est", "fse",
        "roma–viterbo", "roma-viterbo", "roma viterbo"
    ]

    def is_suburban_rail(name_str, tag_info):
        base = (name_str or "").lower() + " " + tag_info.get("operator", "") + " " + tag_info.get("network", "")
        return any(k in base.lower() for k in FERROVIA_SUBURBANA_KEYWORDS)

    if any(k in tag for k in [
        "public_transport=", "highway=bus_stop", "bus=yes",
        "railway=", "train=yes", "tram=yes", "light_rail=yes",
        "subway=yes", "funicular=yes"
    ]):
        name_no_city = strip_city_from_name(name, city)

        # DECISIONE PREFISSO
        if "bus=yes" in tag or "highway=bus_stop" in tag:
            prefix = "Fermata autobus"
        elif is_suburban_rail(name_no_city, tag_dict):
            prefix = "Fermata treno"
        elif "railway=station" in tag:
            if tag_dict.get("operator", "") == "rfi" or tag_dict.get("network", "") == "rfi":
                prefix = "Stazione Ferroviaria"
                name_no_city = city if city else name
                # aggiungi indirizzo solo se più stazioni nazionali
                if rfi_count > 1 and via_clean_short:
                    name_no_city = f"{name_no_city} - {via_clean_short}"
            else:
                prefix = "Stazione Ferroviaria"
        elif "train=yes" in tag or "railway=stop" in tag:
            prefix = "Fermata treno"
        elif "subway=yes" in tag:
            prefix = "Stazione metropolitana"
        elif "funicular=yes" in tag:
            prefix = "Stazione funicolare"
        elif "tram=yes" in tag or "light_rail=yes" in tag:
            prefix = "Fermata tram"
        else:
            prefix = "Fermata"

        # Nomi inutili OSM -> sostituisci con indirizzo
        meaningless_name_patterns = {"stop", "stop position", "stop_position",
                                     "platform", "piattaforma", "fermata", "bus stop", "halt"}
        base = normalize_for_match(name_no_city)
        is_meaningless_name = (base in meaningless_name_patterns or len(base) <= 3)

        if is_meaningless_name:
            toponimo = via_clean_short.strip()
            name = f"{prefix} {smart_capitalize(toponimo)}" if toponimo else prefix
        else:
            if not name_no_city.lower().startswith(prefix.lower()):
                name = f"{prefix} {name_no_city}".strip()
            else:
                name = name_no_city.strip()


    # ----------------------------
    # CATEGORIE GENERICHE + ARTE E SCULTURA
    # ----------------------------
    CATEGORY_TO_NAME = {
        "post_office": "Ufficio Postale",
        "bank": "Banca",
        "atm": "Bancomat",
        "pharmacy": "Farmacia",
        "hospital": "Ospedale",
        "school": "Scuola",
        "supermarket": "Supermercato",
        "hotel": "Hotel",
        "bar": "Bar",
        "cafe": "Caffè",
        "restaurant": "Ristorante",
        "belvedere": "Belvedere",
        "pub": "Pub",
        "parcheggio": "Parcheggio",
        "teatro": "Teatro",
        "parco": "Parco",
        # categorie artistiche
        "Opera d’arte": "Opera d’arte",
        "Statua / Monumento": "Statua / Monumento",
        "Opera contemporanea": "Opera contemporanea"
    }

    # normalizza la categoria per confronti robusti (minuscole + apostrofo uniforme)
    cat_base = (categoria.split(":")[-1] if ":" in categoria else categoria).strip()
    cat_base_norm = cat_base.lower().replace("’", "'").replace("`", "'").replace("‘", "'")

    original_words = original_name.split()

    print(f"name: {name}")
    print(f"original_name: {original_name}")
    print(f"cat_base: {cat_base}")
    print(f"cat_base_norm: {cat_base_norm}")

    # ----------------------------
    # ARTE / SCULTURA - costruzione nome senza prefisso generico
    # ----------------------------
    if cat_base_norm in {"opera d'arte", "statua / monumento", "opera contemporanea"}:
        # mappa artwork_type -> italiano
        ARTWORK_TYPE_IT = {
            "sculpture": "Statua / Monumento",
            "bust": "Busto",
            "installation": "Opera contemporanea",
            # altri tipi se necessario
        }

        artwork_type = tag_dict.get("artwork_type", "").replace('"','').strip().lower()
        inscription = tag_dict.get("inscription", "").replace('"','').strip()

        # rimuove città dall'inscription se presente (case-insensitive)
        if city and inscription:
            inscription = re.sub(re.escape(city), "", inscription, flags=re.IGNORECASE).strip()

        # traduce artwork_type se presente nella mappa
        tipo_it = ARTWORK_TYPE_IT.get(artwork_type, smart_capitalize(artwork_type)) if artwork_type else ""

        # --- PULIZIA INIZIALE INSCRIPTION ---
        if inscription:
            # rimuove '/' e '|' multipli e codici Wikidata
            inscription = re.sub(r"\s*[|/]\s*", " ", inscription)
            inscription = re.sub(r"Q\d+", "", inscription)
            inscription = re.sub(r"\s{2,}", " ", inscription).strip()

        # --- PATCH SPECIFICA PER STATUE ---
        if tipo_it.lower() == "statua / monumento":
            tipo_it = tipo_it.replace("/", "").strip()  # rimuove '/'

            # se ci sono ancora '/' separatori nell'iscrizione, estrai prime due parole/parti
            if inscription:
                parts_inscription = inscription.split()
                if len(parts_inscription) > 0:
                    # trova indice ultima parola da tenere (qui "Orlandi")
                    try:
                        idx_stop = parts_inscription.index("Orlandi") + 1
                        inscription = " ".join(parts_inscription[:idx_stop])
                    except ValueError:
                        # se non trova "Orlandi", lascia solo le prime 5-6 parole
                        inscription = " ".join(parts_inscription[:6])

                # trasforma "In memoria ..." → "in memoria ..."
                if inscription.lower().startswith("in memoria"):
                    inscription = "in memoria" + inscription[10:]

        # --- PULIZIA FINALE INSCRIPTION ---
        if inscription and not inscription.lower().startswith("in memoria"):
            inscription = smart_capitalize(inscription)

        # costruisce nome finale: Tipo a Soggetto (senza prefisso generico)
        parts = []
        if tipo_it:
            parts.append(tipo_it)
        if inscription:
            parts.append(inscription)

        # se ci sono parti, compone "Tipo a Soggetto"
        if parts:
            name = " ".join(parts)
        else:
            # nessun dettaglio: mantieni il nome originale o tipo_it
            name = tipo_it if tipo_it else name


    # altre categorie generiche
    elif cat_base in CATEGORY_TO_NAME:
        base_name = CATEGORY_TO_NAME[cat_base]
        if len(original_words) == 1 and via_clean_short:
            name = f"{base_name} {via_clean_short}"
        else:
            name = smart_capitalize(base_name)


    # ----------------------------
    # GENERIC_WITH_ADDRESS
    # ----------------------------
    GENERIC_WITH_ADDRESS = {
        "bar","caffè","ristorante","parcheggio","supermercato",
        "mercato","farmacia","banca","belvedere","pub","hotel","parco","teatro"
    }

    base_name = name.lower()

    # Verifica se il nome è *solo* generico (una sola parola)
    first_word = base_name.split()[0]
    is_pure_generic = (first_word in GENERIC_WITH_ADDRESS) and (len(base_name.split()) == 1)

    if is_pure_generic:
        # aggiungi via SOLO in questo caso
        if via_clean_short and not any(x in base_name for x in ["via","piazza","viale","corso","largo"]):
            name = f"{name} {smart_capitalize(via_clean_short)}"

    # ----------------------------
    # Pulizia finale
    # ----------------------------
    name = smart_capitalize(name).strip()
    name = fix_initials_in_name(name)

    poi["nome_poi"] = name
    poi["categoria_persistente"] = categoria.strip()
    poi["address"] = address.strip()
    return poi
  
def clean_list(pois):
    """
    Pulisce una lista di POI applicando le regole di normalizzazione del nome e delle categorie.
    """
    try:
#        from tqdm import tqdm
#        iterator = lambda x: tqdm(x, desc="Pulizia POI")
        iterator = lambda x: x  # disabilita temporaneamente tqdm per debug

    except Exception:
        iterator = lambda x: x

    cleaned = []
    total = len(pois)
    renamed = 0
    skipped = 0

    print(f"Avvio pulizia nomi per {total} POI...")

    for poi in iterator(pois):
        try:
            # ----------------------------
            # 1️⃣ Calcolo rfi_count per la città
            # ----------------------------
            tag = (poi.get("tag_k3") or "").lower()
            tag_dict = {}
            for p in tag.split(";"):
                if "=" in p:
                    k, v = p.split("=", 1)
                    tag_dict[k.strip().lower()] = v.strip().lower()

            # Se l'operatore/network è RFI, conteggia quante RFI ci sono nella lista totale
            rfi_count = sum(
                1
                for x in pois
                if "tag_k3" in x
                and (
                    "rfi" in (x.get("tag_k3") or "").lower()
                )
            )
            poi["rfi_count"] = rfi_count

            # ----------------------------
            # 2️⃣ Salva nome precedente
            # ----------------------------
            old_name = (poi.get("nome_poi") or poi.get("nome", "")).strip()

            # ----------------------------
            # 3️⃣ Normalizzazione nome
            # ----------------------------
            poi = apply_name_cleaning(poi)
            new_name = (poi.get("nome_poi") or poi.get("nome", "")).strip()

            if new_name != old_name:
                renamed += 1
            else:
                skipped += 1

            for k, v in list(poi.items()):
                if v is None:
                    poi[k] = ""

            cleaned.append(poi)

        except Exception as e:
            print(f"Errore durante la pulizia di un POI (id={poi.get('poi_id','?')}): {e}")
            cleaned.append(poi)

    print(f"Pulizia completata")
    print(f"   ├─ POI totali: {total}")
    print(f"   ├─ Nomi modificati: {renamed}")
    print(f"   └─ Nomi invariati: {skipped}")

    return cleaned

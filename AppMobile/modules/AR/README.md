# AR Modules  
**Categoria dei moduli dedicati alla Realtà Aumentata**

---

## 1. Scopo della categoria

La cartella `modules/AR/` contiene tutti i moduli relativi alla **Realtà Aumentata**, inclusi:

- AR Foundation e provider (ARCore / ARKit)  
- geolocalizzazione e GPS  
- ancoraggi AR basati sulla posizione  
- gestione della camera AR  
- sistemi di tracking e sensori  
- estensioni future (occlusione, mesh, plane detection, ecc.)

Ogni modulo è un **Unity Package locale**, indipendente e integrabile nell’app finale tramite `manifest.json`.

Questa categoria è progettata per essere **scalabile**: puoi aggiungere nuovi moduli AR senza modificare la struttura esistente.

---

## 2. Architettura generale dei moduli AR

I moduli AR seguono una filosofia modulare:

- ogni funzionalità AR è isolata in un package  
- nessun modulo AR deve dipendere da moduli Avatar, AI o UI  
- i moduli AR possono dipendere da Unity AR Foundation e provider  
- i moduli AR devono essere testabili in scene dedicate  

Esempio di struttura concettuale:

```
ARCoreProvider
ARKitProvider
ARLocation
ARAnchors
ARCamera
```

---

## 3. Moduli attualmente presenti

Questa sezione elenca i moduli *attualmente* disponibili nella categoria AR.  
Può essere aggiornata liberamente quando ne aggiungerai di nuovi.

*“Nessun modulo presente”.*

---

## 4. Struttura consigliata per i moduli AR

Ogni modulo AR segue la struttura standard dei Unity Packages:

```
modules/AR/<NomeModulo>/
 ├── package.json
 ├── Runtime/
 ├── Editor/
 ├── Prefabs/        (opzionale)
 ├── Presets/        (opzionale)
 ├── Scenes/         (opzionale, per test AR)
 ├── Docs/           (opzionale)
 └── README.md
```

Questa struttura garantisce:

- chiarezza  
- isolamento  
- compatibilità con Unity Package Manager  
- facilità di testing  

---

## 5. Integrazione dei moduli AR nell’app finale

Per integrare un modulo AR nell’app Unity, aggiungi una dipendenza nel file:

```
app/Packages/manifest.json
```

Esempio:

```json
"com.project.ar.location": "file:../../modules/AR/ARLocation"
```

Unity importerà automaticamente il modulo tramite Package Manager.

---

## 6. Aggiungere nuovi moduli AR

Per creare un nuovo modulo nella categoria AR:

1. Crea una cartella in `modules/AR/<NomeModulo>/`
2. Aggiungi un `package.json` con nome univoco
3. Segui la struttura standard dei moduli
4. Documenta il modulo con un README dedicato
5. Aggiungilo al `manifest.json` dell’app finale

Per dettagli completi, consulta:

```
modules/README.md
```

---

## 7. Note per il team

- I moduli AR devono rimanere **indipendenti** dagli altri domini  
- Evitare dipendenze da moduli Avatar, AI o UI  
- Ogni modulo AR deve avere una scena di test dedicata  
- Documentare sempre API, componenti e requisiti  
- Evitare logica specifica dell’app finale dentro i moduli  

---

## 8. Obiettivi futuri (non vincolanti)

La categoria AR è progettata per supportare in futuro:

- occlusione ambientale  
- AR mesh reconstruction  
- plane detection avanzata  
- face tracking (se non gestito da Avatar)  
- body tracking  
- world mapping persistente  
- AR multiplayer (AR Shared Anchors)  

Queste estensioni non richiedono modifiche strutturali alla categoria.

---

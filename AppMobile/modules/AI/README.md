# AI Modules  
**Categoria dei moduli dedicati all’Intelligenza Artificiale**

---

## 1. Scopo della categoria

La cartella `modules/AI/` contiene tutti i moduli relativi ai sistemi di **Intelligenza Artificiale** dell’app, inclusi:

- gestione dei dialoghi  
- LLM client (locale o remoto)  
- pipeline RAG (Retrieval-Augmented Generation)  
- TTS (Text‑to‑Speech)  
- STT (Speech‑to‑Text)  
- orchestrazione delle risposte  
- sistemi di memoria e contesto  
- estensioni future (emotion analysis, intent detection, ecc.)

Ogni modulo è un **Unity Package locale**, indipendente e integrabile nell’app finale tramite `manifest.json`.

Questa categoria è progettata per essere **scalabile**: puoi aggiungere nuovi moduli AI senza modificare la struttura esistente.

---

## 2. Architettura generale dei moduli AI

I moduli AI seguono una filosofia modulare:

- ogni componente AI è isolato in un package  
- nessun modulo AI deve dipendere da moduli Avatar, AR o UI  
- i moduli AI possono dipendere da servizi esterni (API, backend)  
- i moduli AI devono essere testabili in isolamento  

Esempio concettuale:

```
LLMClient
RAGSystem
DialogueManager
TTS
STT
AIOrchestrator
```

---

## 3. Moduli attualmente presenti

Questa sezione elenca i moduli *attualmente* disponibili nella categoria AI.  
Può essere aggiornata liberamente quando ne aggiungerai di nuovi.

> Nessun modulo presente al momento.

---

## 4. Struttura consigliata per i moduli AI

Ogni modulo AI segue la struttura standard dei Unity Packages:

```
modules/AI/<NomeModulo>/
 ├── package.json
 ├── Runtime/
 ├── Editor/
 ├── Scripts/        (opzionale)
 ├── Resources/      (opzionale)
 ├── Docs/           (opzionale)
 └── README.md
```

Questa struttura garantisce:

- chiarezza  
- isolamento  
- compatibilità con Unity Package Manager  
- facilità di testing  

---

## 5. Integrazione dei moduli AI nell’app finale

Per integrare un modulo AI nell’app Unity, aggiungi una dipendenza nel file:

```
app/Packages/manifest.json
```

Esempio:

```json
"com.project.ai.dialogue": "file:../../modules/AI/DialogueManager"
```

Unity importerà automaticamente il modulo tramite Package Manager.

---

## 6. Aggiungere nuovi moduli AI

Per creare un nuovo modulo nella categoria AI:

1. Crea una cartella in `modules/AI/<NomeModulo>/`
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

- I moduli AI devono rimanere **indipendenti** dagli altri domini  
- Evitare dipendenze da moduli Avatar, AR o UI  
- Documentare sempre API, componenti e requisiti  
- Evitare logica specifica dell’app finale dentro i moduli  
- Se un modulo usa servizi esterni, isolare le API in interfacce  

---

## 8. Obiettivi futuri (non vincolanti)

La categoria AI è progettata per supportare in futuro:

- sentiment analysis  
- intent classification  
- memory graph  
- agenti autonomi  
- orchestrazione multi‑modello  
- generazione di animazioni basate su AI  
- personalizzazione del comportamento degli NPC  

Queste estensioni non richiedono modifiche strutturali alla categoria.

---

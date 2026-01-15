## AI Modules  
**Categoria dei moduli Unity dedicati alla comunicazione con il backend AI**

---

## 1. Scopo della categoria

La cartella `modules/AI/` contiene esclusivamente i moduli Unity che gestiscono la **comunicazione tra l’app mobile e il backend AI**.

Questi moduli includono:

- client per chiamate API verso il backend  
- gestione dei contratti JSON  
- gestione delle sessioni e dei turni lato app  
- STT cloud (fallback)  
- TTS cloud (streaming)  
- parsing delle risposte AI  
- gestione degli errori di rete  

---

### ❗ Importante  
Questa categoria **non contiene**:

- logica di avatar, audio locale, lipsync, UI, AR  
- orchestrazione del dialogo  
- modelli AI, RAG, agenti o pipeline server‑side (che vivono in repository backend separati)

Di seguito l’elenco dettagliato di ciò che *non* appartiene a `modules/AI/` e dove deve essere collocato.

---

## 1. **STT locale (on‑device)**
Logica legata al microfono, all’audio locale e all’avatar.

👉 **Sta in:**  
`modules/Avatar/`  
(es. `STTLocal`, `MicrophoneInput`, `AudioCapture`)

---

## 2. **Lipsync, analisi audio, animazioni facciali**
Componenti di presentazione e animazione dell’avatar.

👉 **Sta in:**  
`modules/Avatar/`  
(es. `LipsyncDriver`, `VisemeBlender`, `AvatarController`)

---

## 3. **Audio playback locale**  
Gestione di AudioSource, buffering e sincronizzazione.

👉 **Sta in:**  
`modules/Avatar/`

---

## 4. **Orchestrazione della pipeline conversazionale**  
La logica che collega STT → AI → TTS → Lipsync → Avatar.

👉 **Sta in:**  
`modules/Dialog/`  
(es. `DialogOrchestrator`, `ConversationState`, `PipelineController`)

---

## 5. **UI, pulsanti, indicatori di ascolto, waveform**  
Elementi di interfaccia utente.

👉 **Sta in:**  
`modules/UI/`

---

## 6. **Logica AR, tracking, ancoraggi**  
Funzionalità relative alla scena AR.

👉 **Sta in:**  
`modules/AR/`

---

## 7. **Modelli AI, RAG, agenti, orchestrazione server‑side**  
Questi componenti non appartengono all’app Unity.  
Vivono nel backend e non devono essere rappresentati come moduli Unity.

👉 **Sta in:**  
repository backend dedicati, ad esempio:  
- `backend-ai/`  
- `backend-rag/`  
- `backend-tts/`  
- `backend-stt/`  
- `backend-orchestrator/`

---

## 8. **Gestione della memoria conversazionale lato server**  
Parte del backend AI.

👉 **Sta in:**  
repository backend (es. `backend-ai-memory/`)

---

## 9. **Intent detection, sentiment analysis, agenti autonomi**  
Se implementati lato server, non devono apparire nei moduli Unity.

👉 **Sta in:**  
repository backend (es. `backend-ai-intent/`)

---

## 2. Architettura generale dei moduli AI

I moduli AI Unity seguono una filosofia di isolamento:

- ogni modulo è un Unity Package indipendente  
- nessun modulo AI dipende da Avatar, AR o UI  
- i moduli AI non contengono logica di presentazione  
- i moduli AI non contengono logica di orchestrazione del dialogo  
- i moduli AI sono semplici **client** che parlano con il backend  

Esempio concettuale:

```
AIBackendClient
TTSClient
STTCloudFallback
JsonContracts
```

---

## 3. Moduli attualmente presenti

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

---

## 5. Integrazione dei moduli AI nell’app finale

Per integrare un modulo AI nell’app Unity, aggiungi una dipendenza nel file:

```
app/Packages/manifest.json
```

Esempio:

```json
"com.project.ai.backend": "file:../../modules/AI/AIBackendClient"
```

---

## 6. Aggiungere nuovi moduli AI

Per creare un nuovo modulo nella categoria AI:

1. Crea una cartella in `modules/AI/<NomeModulo>/`
2. Aggiungi un `package.json` con nome univoco
3. Segui la struttura standard dei moduli
4. Documenta il modulo con un README dedicato
5. Aggiungilo al `manifest.json` dell’app finale

---

## 7. Note per il team

- I moduli AI devono rimanere **indipendenti** dagli altri domini Unity  
- Non devono contenere logica di dialogo o orchestrazione  
- Non devono contenere logica di avatar o audio  
- Devono essere semplici client API  
- Devono essere testabili in isolamento  
- Devono mantenere contratti JSON chiari e versionati  

---

## 8. Obiettivi futuri (non vincolanti)

La categoria AI potrà includere in futuro:

- client per nuovi servizi backend  
- client per modelli TTS/STT alternativi  
- client per servizi di analytics o intent detection lato server  

Tutto ciò rimane **client-side**, non AI lato backend.

---

# 🎯 In sintesi

Il README aggiornato chiarisce che:

- `modules/AI` contiene **solo moduli Unity**  
- non contiene logica AI vera e propria  
- non contiene orchestrazione del dialogo  
- non contiene modelli o pipeline server-side  
- è un insieme di **client API** che parlano con il backend  

Esattamente ciò che serve per mantenere la tua architettura pulita e scalabile.

---

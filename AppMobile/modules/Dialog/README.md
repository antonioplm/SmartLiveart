# 🗣️ **Dialog Modules**  
_Moduli Unity dedicati all’orchestrazione della pipeline conversazionale_

---

## 🎯 1. Scopo della categoria

La directory:

```
modules/Dialog/
```

contiene i moduli Unity responsabili della **gestione del dialogo** e dell’orchestrazione dell’intera pipeline conversazionale.  
Questi moduli non eseguono elaborazioni audio o AI, ma coordinano i flussi tra:

- **STT locale** (microfono + riconoscimento on‑device)  
- **STT cloud** (fallback)  
- **backend AI** (streaming JSON)  
- **TTS cloud** (streaming audio)  
- **audio playback locale**  
- **lipsync**  
- **avatar**  
- **UI**  

Il modulo Dialog agisce come **cervello dell’app**, mantenendo lo stato della conversazione e orchestrando i turni tra utente e avatar.

---

## 🧭 2. Architettura generale dei moduli Dialog

I moduli Dialog seguono una filosofia di orchestrazione rigorosa:

- **coordinano** i flussi tra Avatar, AI e UI  
- **non implementano logica di dominio** (AI, audio, animazioni, rigging)  
- **non dipendono da implementazioni concrete** dei moduli  
- **comunicano tramite interfacce, eventi e contratti dati**  
- **gestiscono lo stato della conversazione** e i turni  
- **centralizzano i fallback** (es. STT locale → cloud)  
- **mantengono la pipeline coerente** anche in caso di errori o ritardi  

### Esempio concettuale dei componenti

```
DialogOrchestrator      → Coordina l’intera pipeline
ConversationState       → Mantiene lo stato (Idle, Listening, Thinking, Speaking…)
PipelineController      → Gestisce i flussi STT → AI → TTS
TurnManager             → Gestisce i turni utente/avatar
EventBus (opzionale)    → Disaccoppia i moduli tramite eventi
```

### Principi chiave

- **Orchestrazione, non elaborazione**  
  Il modulo Dialog decide *quando* i moduli lavorano, non *come* lavorano.

- **Indipendenza dai moduli concreti**  
  Usa interfacce come `ISttProvider`, `IAiClient`, `ITtsStream`, `ILipSyncDriver`.

- **Gestione degli stati**  
  Evita race condition e comportamenti incoerenti.

- **Fallback automatici**  
  Es. STT locale → STT cloud → errore gestito.

- **Pipeline reattiva**  
  Supporto a streaming, partials, eventi.

---

## 📦 3. Moduli attualmente presenti

> Nessun modulo presente al momento.

Questa categoria è destinata a crescere con l’introduzione del modulo centrale:

### **DialogOrchestrator (in arrivo)**  
Il modulo principale che:

- coordina STT → AI → TTS → Lipsync  
- gestisce gli stati della conversazione  
- attiva fallback  
- comunica con UI e Avatar  
- mantiene la pipeline coerente e reattiva  

---

## 🧩 4. Ruolo nella pipeline conversazionale

I Dialog Modules rappresentano lo strato di **orchestrazione** della pipeline:

```
[Microfono] 
   ↓
STT locale → (fallback) → STT cloud 
   ↓
Backend AI (JSON streaming)
   ↓
TTS cloud (streaming audio)
   ↓
Audio Playback → Lipsync → Avatar
   ↓
UI feedback
```

Il modulo Dialog è l’unico responsabile di:

- decidere quando ascoltare  
- quando inviare all’AI  
- quando far parlare l’avatar  
- quando aggiornare la UI  
- quando gestire errori e fallback  

---

## 5. Struttura consigliata per i moduli Dialog

Ogni modulo Dialog segue la struttura standard dei Unity Packages:

```
modules/Dialog/<NomeModulo>/
 ├── package.json
 ├── Runtime/
 ├── Editor/
 ├── Scripts/        (opzionale)
 ├── Resources/      (opzionale)
 ├── Docs/           (opzionale)
 └── README.md
```

---

## 6. Integrazione dei moduli Dialog nell’app finale

Per integrare un modulo Dialog nell’app Unity, aggiungi una dipendenza nel file:

```
app/Packages/manifest.json
```

Esempio:

```json
"com.project.dialog.orchestrator": "file:../../modules/Dialog/DialogOrchestrator"
```

---

## 7. Aggiungere nuovi moduli Dialog

Per creare un nuovo modulo nella categoria Dialog:

1. Crea una cartella in `modules/Dialog/<NomeModulo>/`
2. Aggiungi un `package.json` con nome univoco
3. Segui la struttura standard dei moduli
4. Documenta il modulo con un README dedicato
5. Aggiungilo al `manifest.json` dell’app finale

---

## 8. Note per il team

- I moduli Dialog **non devono contenere logica di orchestrazione del dialogo** (sta in `modules/Dialog`)  
- I moduli Dialog **non devono contenere logica AI o chiamate al backend** (sta in `modules/AI`)  
- I moduli Dialog devono rimanere **indipendenti** dagli altri domini Unity  
- Non devono contenere logica AI, audio o animazioni  
- Devono coordinare i moduli tramite interfacce ed eventi  
- Devono essere testabili in isolamento  
- Devono mantenere la pipeline conversazionale chiara e modulare  

---

## 9. Obiettivi futuri (non vincolanti)

La categoria Dialog potrà includere in futuro:

- turn-taking avanzato  
- gestione delle interruzioni vocali (barge‑in)  
- gestione del contesto locale  
- orchestrazione multimodale (voce + gesture)  
- logging conversazionale locale  

---


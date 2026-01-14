# LipSync  
**Modulo per la generazione e l’applicazione di visemi basati su audio o testo**

---

## 1. Scopo del modulo

Il modulo LipSync fornisce un sistema modulare per generare e applicare **visemi** (blendshape legati alla fonetica) a un avatar compatibile con AvatarCore.

Gli obiettivi principali sono:

- supportare lipsync **audio‑driven** (FFT, microfono, file audio)  
- supportare lipsync **text‑driven** (TTS, parsing fonetico)  
- mantenere un’architettura **data‑driven** e indipendente dal modello 3D  
- garantire compatibilità con qualsiasi avatar conforme allo standard ARKit‑style  

Il modulo non richiede SDK esterni e non dipende da sistemi di face tracking.

---

## 2. Architettura del modulo

Il modulo è composto da tre livelli:

```
LipSync
 ├── Input Layer
 │     ├── AudioInput (microfono, clip)
 │     └── TextInput (stringhe, TTS)
 │
 ├── Processing Layer
 │     ├── FFTAnalyzer
 │     ├── PhonemeParser
 │     └── VisemeMapper
 │
 └── Output Layer
       └── ILipSyncTarget (interfaccia)
```

### Filosofia

- **Input agnostico**: audio o testo  
- **Output unificato**: visemi normalizzati (0–1)  
- **Avatar‑agnostic**: nessuna dipendenza da mesh specifiche  
- **Plug‑and‑play**: ogni componente può essere sostituito o esteso  

---

## 3. Componenti principali

### 3.1 ILipSyncTarget (interfaccia)

Definisce il contratto tra il sistema di lipsync e l’avatar.

**Metodi principali:**

- `SetViseme(string arkitName, float weight)`  
- `ResetVisemes()`  

Qualsiasi avatar compatibile deve implementare questa interfaccia.

Il modulo FacialExpressionPresets può essere usato come backend per applicare i visemi, ma non è obbligatorio.

---

### 3.2 LipSyncDriverFFT (audio‑driven)

Analizza un segnale audio tramite FFT e genera visemi in tempo reale.

**Funzionalità:**

- analisi spettro audio  
- smoothing temporale  
- mappatura bande → visemi  
- supporto microfono o AudioClip  

**Uso tipico:**

- avatar che parlano in tempo reale  
- streaming audio  
- input microfono  

---

### 3.3 LipSyncTextSimulator (text‑driven)

Genera visemi a partire da testo.

**Funzionalità:**

- parsing fonetico semplificato  
- generazione sequenza temporale di visemi  
- supporto per TTS esterni (opzionale)  
- playback controllato (velocità, pausa, stop)  

**Uso tipico:**

- NPC che parlano tramite dialoghi  
- cutscene  
- chatbot avatar  

---

### 3.4 VisemeMapper

Converte fonemi o bande audio in visemi ARKit‑style.

Esempi:

```
AA → jawOpen
F  → mouthFunnel
M  → mouthClose
S  → mouthPucker
```

La mappatura è completamente configurabile.

---

## 4. Scena di test

Il modulo include una scena di test (opzionale) che permette di:

- testare lipsync audio con microfono  
- testare lipsync da testo  
- visualizzare i visemi in tempo reale  
- verificare la corretta implementazione di ILipSyncTarget  

La scena non è necessaria per la build finale.

---

## 5. Compatibilità con AvatarCore

Il modulo richiede un avatar conforme a:

- naming ARKit‑style  
- struttura mesh definita in AvatarCore  
- implementazione di ILipSyncTarget  
- presenza dei blendshape necessari ai visemi  

Per dettagli tecnici, consultare:

```
modules/Avatar/AvatarCore/README.md
modules/Avatar/AvatarCore/Docs/Blendshapes.md
```

---

## 6. Pattern architetturali adottati

- **Data‑driven design**  
- **Interfacce come contratti (ILipSyncTarget)**  
- **Separazione netta tra input, processing e output**  
- **Modularità e sostituibilità dei componenti**  
- **Indipendenza dal modello 3D**  

---

## 7. Estensioni previste (non vincolanti)

Il modulo è progettato per supportare in futuro:

- lipsync basato su AI (modelli predittivi)  
- lipsync basato su face tracking  
- blending tra visemi e espressioni emotive  
- sincronizzazione in rete (multiplayer)  

Nessuna di queste estensioni richiede modifiche strutturali al modulo.

---

## 8. Note per il team

- Non inserire logica avatar‑specifica nel modulo  
- Mantenere ILipSyncTarget minimale e stabile  
- Validare sempre i visemi tramite la scena di test  
- Evitare dipendenze da SDK esterni  
- Mantenere la mappatura visemi configurabile  

---

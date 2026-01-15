# 🧍‍♂️ **Avatar Modules**  
_Moduli Unity dedicati agli Avatar 3D e all’audio locale_

---

## 🎯 1. Scopo della categoria

La directory:

```
modules/Avatar/
```

contiene tutti i moduli Unity responsabili della gestione degli **avatar 3D** e dell’**audio locale**.  
Questi moduli implementano la parte “visiva” e “acustica” della pipeline conversazionale, includendo:

- struttura e compatibilità dell’avatar  
- preset facciali data‑driven  
- lipsync audio‑driven e text‑driven  
- animazioni e rigging  
- cattura audio locale (STT on‑device)  
- riproduzione audio locale  

Ogni modulo è un **Unity Package locale**, indipendente e integrabile tramite `manifest.json`.  
La categoria è progettata per essere **scalabile e estendibile**, così da permettere l’aggiunta di nuovi moduli senza modificare quelli esistenti.

---

## 🧱 2. Architettura generale dei moduli Avatar

I moduli seguono una filosofia modulare e componibile:

```
AvatarCore
 ├── FacialExpressionPresets
 ├── LipSync
 ├── AudioCapture (STT locale)
 └── AudioPlayback
```

### Principi chiave

- **Indipendenza**  
  Ogni modulo è isolato, testabile e non dipende da altri moduli Avatar.

- **Contratti chiari**  
  I moduli comunicano tramite interfacce e strutture dati standardizzate.

- **Data‑driven**  
  Preset, visemi, configurazioni e mapping sono definiti tramite asset.

- **Avatar‑agnostic**  
  Nessun modulo è legato a un modello 3D specifico: qualsiasi avatar compatibile può essere integrato.

- **Responsabilità locale**  
  Tutto ciò che riguarda audio locale, lipsync e microfono vive in questa categoria, non nei moduli AI o Dialog.

---

## 📦 3. Moduli attualmente presenti

Questa sezione elenca i moduli disponibili oggi nella categoria Avatar.  
Può essere aggiornata liberamente quando ne aggiungerai di nuovi.

---

### ✔ **AvatarCore**

Modulo fondamentale che definisce:

- struttura dell’avatar  
- naming ARKit‑style dei blendshape  
- requisiti di compatibilità  
- documentazione tecnica per rigging e setup  

È il punto di riferimento per tutti gli altri moduli Avatar.

---

### ✔ **FacialExpressionPresets**

Sistema data‑driven per:

- definire preset facciali  
- applicare blendshape tramite controller  
- creare preset tramite editor tools dedicati  

Permette di gestire espressioni facciali in modo modulare e riutilizzabile.

---

### ✔ **LipSync**

Sistema modulare per:

- lipsync audio‑driven (FFT)  
- lipsync text‑driven (visemi)  
- generazione, smoothing e applicazione dei visemi  

Supporta pipeline future come:

- lipsync basato su TTS con visemi integrati  
- lipsync predittivo  
- lipsync streaming  

---

## 4. Struttura consigliata per i moduli Avatar

Ogni modulo segue la struttura standard dei Unity Packages:

```
modules/Avatar/<NomeModulo>/
 ├── package.json
 ├── Runtime/
 ├── Editor/
 ├── Prefabs/        (opzionale)
 ├── Presets/        (opzionale)
 ├── Docs/           (opzionale)
 └── README.md
```

Questa struttura garantisce:

- chiarezza  
- isolamento  
- compatibilità con Unity Package Manager  
- facilità di testing  

---

## 5. Integrazione dei moduli Avatar nell’app finale

Per integrare un modulo Avatar nell’app Unity, aggiungi una dipendenza nel file:

```
app/Packages/manifest.json
```

Esempio:

```json
"com.project.avatar.facialexpression": "file:../../modules/Avatar/FacialExpressionPresets"
```

Unity importerà automaticamente il modulo tramite Package Manager.

---

## 6. Aggiungere nuovi moduli Avatar

Per creare un nuovo modulo nella categoria Avatar:

1. Crea una cartella in `modules/Avatar/<NomeModulo>/`
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

- I moduli Avatar **non devono contenere logica di orchestrazione del dialogo** (sta in `modules/Dialog`)  
- I moduli Avatar **non devono contenere logica AI o chiamate al backend** (sta in `modules/AI`)  
- I moduli Avatar devono rimanere **indipendenti** tra loro  
- AvatarCore non deve dipendere da altri moduli  
- FacialExpressionPresets e LipSync devono dipendere solo da AvatarCore  
- Evitare dipendenze circolari  
- Documentare sempre API, componenti e requisiti  

---

## 8. Obiettivi futuri (non vincolanti)

La categoria Avatar è progettata per supportare in futuro:

- face tracking (MediaPipe, ARKit, OpenXR)  
- animazioni procedurali  
- avatar generati da AI  
- sistemi di espressioni avanzate  
- sincronizzazione in rete  

Queste estensioni non richiedono modifiche strutturali alla categoria.

---

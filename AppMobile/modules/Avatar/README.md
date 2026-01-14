# Avatar Modules  
**Categoria dei moduli dedicati agli Avatar 3D**

---

## 1. Scopo della categoria

La cartella `modules/Avatar/` contiene tutti i moduli relativi alla gestione degli **avatar 3D**, incluse:

- struttura e compatibilità dell’avatar  
- preset facciali data‑driven  
- lipsync audio/text‑driven  
- animazioni, rigging, estensioni future  

Ogni modulo è un **Unity Package locale**, indipendente e integrabile nell’app finale tramite `manifest.json`.

Questa categoria è progettata per essere **scalabile**: puoi aggiungere nuovi moduli senza modificare la struttura esistente.

---

## 2. Architettura generale dei moduli Avatar

I moduli della categoria Avatar seguono una filosofia modulare:

```
AvatarCore
 ├── FacialExpressionPresets
 └── LipSync
```

### Principi chiave

- **Indipendenza**: ogni modulo è isolato e testabile da solo  
- **Contratti chiari**: i moduli comunicano tramite interfacce e dati standardizzati  
- **Data‑driven**: preset, visemi e configurazioni sono definiti tramite asset  
- **Avatar‑agnostic**: nessun modulo dipende da un modello 3D specifico  

---

## 3. Moduli attualmente presenti

Questa sezione elenca i moduli *attualmente* disponibili nella categoria Avatar.  
Può essere aggiornata liberamente quando ne aggiungerai di nuovi.

### ✔ AvatarCore  
Modulo base che definisce:

- struttura dell’avatar  
- naming ARKit‑style  
- requisiti di compatibilità  
- documentazione tecnica sui blendshape  

### ✔ FacialExpressionPresets  
Sistema data‑driven per:

- definire preset facciali  
- applicare blendshape tramite controller  
- creare preset tramite editor tools  

### ✔ LipSync  
Sistema modulare per:

- lipsync audio‑driven (FFT)  
- lipsync text‑driven  
- generazione e applicazione dei visemi  

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

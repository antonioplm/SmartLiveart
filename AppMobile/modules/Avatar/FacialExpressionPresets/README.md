# FacialExpressionPresets  
**Modulo per la gestione dei preset facciali basati su blendshape**

---

## 1. Scopo del modulo

Il modulo FacialExpressionPresets fornisce un sistema **data‑driven** per definire, organizzare e applicare espressioni facciali tramite preset di blendshape.

Gli obiettivi principali sono:

- separare i **dati delle espressioni** dalla logica runtime  
- standardizzare la gestione dei blendshape tramite naming ARKit‑style  
- offrire strumenti di authoring e preview in Editor  
- garantire compatibilità con qualsiasi avatar conforme ad AvatarCore  

Il modulo è completamente indipendente dalla piattaforma e non richiede SDK esterni.

---

## 2. Componenti principali

### 2.1 ExpressionPresets (ScriptableObject)

Contiene la definizione statica delle espressioni facciali.

**Struttura dati:**

- `List<Expression>`
  - `name`
  - `List<BlendValue>`
    - `arkitName` (string)
    - `weight` (0–1)

**Responsabilità:**

- rappresentare preset emotivi o funzionali  
- fungere da unica fonte dati per il controller  
- supportare serializzazione in:
  - `.asset`
  - `.json` (solo scambio, non runtime)

---

### 2.2 ExpressionPresetController (MonoBehaviour)

Applica i preset facciali a una o più mesh con blendshape.

**Funzionalità principali:**

- mappatura `arkitName → blendshape index`  
- applicazione dei pesi (0–1 → 0–100)  
- supporto per:
  - mesh principale (`faceMesh`)
  - mesh aggiuntive (`extraMeshes`)
  - reset e override  
  - cross‑fade (se implementato)  
  - limitazioni dinamiche (es. jaw clamp)

Il controller è **runtime‑agnostic** e non dipende da editor tools.

---

### 2.3 ExpressionPresetEditorWindow (Editor‑only)

Strumento interno per la creazione e modifica dei preset.

**Funzionalità:**

- creazione preset da zero  
- generazione preset di default  
- editing dei valori tramite slider  
- selezione blendshape tramite dropdown  
- preview live in scena  
- esportazione in JSON o ScriptableObject  

Non viene incluso nella build.

---

### 2.4 ExpressionPresetControllerEditor (Custom Inspector)

Strumento rapido per testare i preset direttamente dall’Inspector.

**Funzionalità:**

- pulsanti per applicare le espressioni  
- test immediato senza scrivere codice  

---

## 3. Preview live

Quando un `ExpressionPresetController` è assegnato come **Preview Controller**, ogni modifica ai pesi:

- richiama `ApplyExpression()`  
- aggiorna immediatamente la mesh  
- forza il repaint della SceneView  

Questo permette:

- tuning artistico immediato  
- workflow rapido senza “apply/reset”  
- verifica visiva continua  

---

## 4. Piattaforme supportate

Il modulo è **platform‑agnostic**.

Funziona ovunque Unity supporti:

- `SkinnedMeshRenderer`  
- blendshape mesh  

| Platform | Support |
|----------|---------|
| Android  | OK      |
| iOS      | OK      |
| Desktop  | OK      |
| WebGL    | OK      |

---

## 5. Pattern architetturali adottati

- **Data‑driven design**  
- **Separation of concerns**  
- **Editor / Runtime split**  
- **Standard‑based naming (ARKit‑style)**  
- **Non vendor locked**  

---

## 6. Estensioni previste (non vincolanti)

Il modulo è progettato per integrarsi con sistemi futuri, senza richiedere modifiche strutturali:

- lipsync audio‑driven  
- face tracking (MediaPipe / ARKit / OpenXR)  
- AI‑driven facial animation  
- network sync delle espressioni  

---

## 7. Dipendenze

Il modulo richiede un avatar conforme a **AvatarCore**, in particolare:

- mesh con blendshape  
- naming ARKit‑style o mappabile  
- struttura mesh compatibile (`faceMesh` + `extraMeshes`)  

Per dettagli tecnici sull’avatar, consultare:

```
modules/Avatar/AvatarCore/README.md
modules/Avatar/AvatarCore/Docs/Blendshapes.md
```

---

## 8. Note per il team

- Non inserire logica runtime nei preset  
- Usare JSON solo come formato di scambio  
- Mantenere coerenza con lo standard ARKit per i nomi dei blendshape  
- Validare sempre i preset tramite preview live  

---
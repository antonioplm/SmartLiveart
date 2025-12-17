# Facial Expression Preset System

**Internal Technical Documentation**

---

## 1. Scopo del sistema

Questo sistema fornisce un **layer di astrazione per il controllo delle espressioni facciali** di avatar 3D in Unity tramite **preset di blendshape**.

L’obiettivo è:

* separare **dati di animazione facciale** dalla logica runtime
* standardizzare il naming dei blendshape
* consentire editing artistico + preview live
* mantenere il sistema **cross-platform** e **runtime-agnostic**

---

## 2. Chiarimento terminologico: “ARKit”

Nel codice e negli editor tool compare il termine **ARKit**.

### Importante:

> **ARKit NON indica una dipendenza dal framework Apple.**

Nel contesto di questo progetto:

* “ARKit” = **naming convention dei blendshape facciali**
* usata come **standard semantico**, non come tecnologia

Esempi:

```text
jawOpen
mouthSmileLeft
eyeBlinkRight
```

Questo standard è adottato da molte pipeline avatar moderne
(MetaHuman, MetaPerson, Ready Player Me, ecc.).

### Implicazioni:

* il sistema **non usa face tracking**
* il sistema **non richiede iOS**
* il sistema **funziona identico su Android, iOS, PC**

---

## 3. Componenti principali

### 3.1 ExpressionPresets (ScriptableObject)

**Ruolo**
Contiene la definizione statica delle espressioni facciali.

**Struttura**

* `List<Expression>`

  * `name`
  * `List<BlendValue>`

    * `arkitName` (string, naming standard)
    * `weight` (0–1 normalizzato)

**Responsabilità**

* fonte dati unica per:

  * espressioni emotive
  * visemi
* serializzazione:

  * `.asset`
  * `.json`

**Nota**
Non contiene logica runtime.

---

### 3.2 ExpressionPresetController (MonoBehaviour)

**Ruolo**
Applica i preset facciali a uno o più `SkinnedMeshRenderer`.

**Responsabilità**

* mappare `arkitName` → blendshape mesh
* applicare pesi (0–1 → 0–100)
* gestire reset / override
* supportare:

  * più mesh facciali
  * cross-fade tra espressioni (se previsto)
  * limitazioni dinamiche (es. jaw clamp)

**Ambito**

* runtime
* indipendente dalla piattaforma

---

### 3.3 ExpressionPresetEditorWindow (Editor-only)

**Ruolo**
Tool interno per authoring dei preset.

**Funzionalità**

* creazione preset da zero
* generazione preset di default
* editing:

  * nome espressione
  * blendshape tramite dropdown (lista ufficiale)
  * weight tramite slider
* preview live in scena
* esportazione:

  * JSON
  * ScriptableObject

**Nota**
Non viene incluso nel build.

---

### 3.4 ExpressionPresetControllerEditor (Custom Inspector)

**Ruolo**
Tool di test rapido in Editor.

**Funzionalità**

* pulsanti per applicare le espressioni
* testing immediato senza scrivere codice

---

## 4. Preview live: funzionamento

Quando viene assegnato un `ExpressionPresetController` come **Preview Controller**:

* ogni modifica a un `weight`
* triggera immediatamente:

  * `ApplyExpression()`
  * aggiornamento mesh
  * repaint della SceneView

Questo consente:

* tuning artistico fine
* verifica visiva immediata
* eliminazione di workflow “apply / reset”

---

## 5. Piattaforme target

Il sistema è **platform-agnostic**.

Supportato ovunque Unity supporti:

* `SkinnedMeshRenderer`
* blendshape mesh

| Platform | Support |
| -------- | ------- |
| Android  | ✔       |
| iOS      | ✔       |
| Desktop  | ✔       |
| WebGL    | ✔       |

---

## 6. Pattern architetturali adottati

* **Data-driven design**
* **Separation of concerns**
* **Editor / Runtime split**
* **Standard-based naming**
* **Non vendor locked**

---

## 7. Estensioni previste (non vincolanti)

Il sistema è progettato per essere esteso con:

* lipsync audio-driven
* face tracking (MediaPipe / ARKit / OpenXR)
* AI speech animation
* network sync delle espressioni

👉 Nessuna estensione richiede modifiche strutturali ai preset.

---

## 8. Avatar di riferimento utilizzato nei test

### Avatar di test

L’avatar di riferimento utilizzato durante lo sviluppo e i test di questo sistema è stato realizzato utilizzando **MetaPerson**.

MetaPerson consente la creazione di avatar umanoidi con:

* blendshape facciali completi
* naming coerente con lo **standard ARKit**
* struttura mesh modulare, adatta a sistemi data-driven

👉 Sito ufficiale MetaPerson:
[https://metaperson.avatarsdk.com/](https://metaperson.avatarsdk.com/)

---

## 9. Struttura dei blendshape nell’avatar

Nel modello MetaPerson utilizzato come riferimento, i **blendshape facciali** sono distribuiti su più `GameObject`.

I nodi principali sono:

* **AvatarHead**

  * mesh facciale principale
  * contiene la quasi totalità dei blendshape ARKit (bocca, occhi, sopracciglia, naso)

* **AvatarEyelashes**

  * mesh separata per le ciglia
  * include blendshape sincronizzati con blink, squint e wide eyes

* **AvatarTeethLower**

  * mesh dei denti inferiori
  * include blendshape associati all’apertura della mandibola (`jawOpen`) e alla fonetica

Questa struttura multi-mesh è il motivo per cui il sistema prevede:

* una mesh principale (`faceMesh`)
* una lista di mesh aggiuntive (`extraMeshes`)

Il controller applica automaticamente le espressioni a **tutte le mesh assegnate**, mantenendo la coerenza visiva.

---

## 10. Creazione di nuovi avatar compatibili

Per creare avatar compatibili con questo sistema è necessario che:

1. Le mesh utilizzino **blendshape facciali**
2. I blendshape seguano (o siano mappabili verso) il **naming standard ARKit**
3. Le mesh siano collegate al `ExpressionPresetController`:

   * mesh principale → `faceMesh`
   * mesh aggiuntive → `extraMeshes`

L’architettura **non è vincolata a MetaPerson**:
qualsiasi avatar che rispetti questi requisiti è supportato.

[Per approfondimenti sulla "Creazione di nuovi avatar compatibili" consultare il file **Blendshapes.md**](Blendshapes.md)

---

## 11. Linee guida per il team

Il termine “ARKit” nel progetto indica esclusivamente:

> **la convenzione di naming dei blendshape facciali**

e **non** l’uso dell’SDK Apple ARKit.

* Mantenere i nomi blendshape compatibili con lo standard
* Non inserire logica runtime nei ScriptableObject
* Usare JSON solo come formato di scambio, non runtime

Il riferimento a MetaPerson:
* è utilizzato **solo come avatar di test**
* **non introduce dipendenze runtime**
* **non limita l’utilizzo su Android o iOS**

---








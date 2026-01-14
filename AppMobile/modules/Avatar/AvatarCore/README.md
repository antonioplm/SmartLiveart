# AvatarCore  
**Modulo base per la gestione dell’avatar e della struttura facciale**

---

## 1. Scopo del modulo

AvatarCore fornisce le **fondamenta comuni** per tutti i sistemi che interagiscono con l’avatar:

- struttura delle mesh facciali  
- organizzazione dei blendshape  
- standard di naming (ARKit‑style)  
- requisiti per la compatibilità con i moduli  
- documentazione tecnica condivisa  

Questo modulo **non contiene logica di animazione**:  
la sua funzione è definire **come deve essere fatto un avatar** affinché gli altri moduli (FacialExpressionPresets, LipSync, ecc.) possano funzionare correttamente.

---

## 2. Architettura generale

AvatarCore è progettato per essere:

- **indipendente dai moduli** (nessuna dipendenza verso FacialExpressionPresets o LipSync)
- **riutilizzabile** in qualsiasi progetto Unity
- **estendibile** senza modifiche strutturali
- **data‑driven** e basato su standard riconosciuti

Gli altri moduli dipendono da AvatarCore, non viceversa.

```
AvatarCore
 ├── Definizione struttura avatar
 ├── Standard ARKit naming
 ├── Documentazione tecnica
 └── Requisiti compatibilità
      ↑
      │
      ├── FacialExpressionPresets
      └── LipSync
```

---

## 3. Avatar di riferimento utilizzato nei test

Durante lo sviluppo è stato utilizzato un avatar generato tramite **MetaPerson**, scelto per:

- disponibilità immediata  
- struttura mesh modulare  
- naming coerente con lo standard ARKit  
- buona compatibilità mobile  

MetaPerson è utilizzato **solo come avatar di test**.  
Non introduce dipendenze runtime e non è richiesto per la produzione.

Per dettagli tecnici sui modelli supportati, consultare:  
**Docs/Blendshapes.md**

---

## 4. Struttura delle mesh facciali

Gli avatar compatibili devono utilizzare una struttura multi‑mesh simile alla seguente:

### Mesh principali

- **AvatarHead**  
  Contiene la maggior parte dei blendshape (bocca, occhi, sopracciglia, naso)

- **AvatarEyelashes**  
  Mesh separata per ciglia, con blendshape sincronizzati con blink e squint

- **AvatarTeethLower**  
  Mesh dei denti inferiori, con blendshape legati a jawOpen e fonetica

### Motivazione

Molti avatar moderni distribuiscono i blendshape su più mesh.  
Per questo motivo i moduli che applicano espressioni (es. FacialExpressionPresets) devono poter:

- gestire una mesh principale (`faceMesh`)
- gestire mesh aggiuntive (`extraMeshes`)
- applicare i pesi in modo coerente su tutte le mesh

---

## 5. Standard di naming (ARKit)

Il progetto adotta lo **standard ARKit** come convenzione di naming dei blendshape.

Esempi:

```
jawOpen
mouthSmileLeft
eyeBlinkRight
browInnerUp
```

### Importante

> L’uso del termine “ARKit” indica **solo la convenzione di naming**,  
> non una dipendenza dall’SDK Apple.

Questo garantisce:

- compatibilità con pipeline moderne (MetaHuman, MetaPerson, RPM, ecc.)
- interoperabilità tra moduli
- chiarezza semantica

---

## 6. Requisiti per la compatibilità degli avatar

Un avatar è considerato compatibile se:

1. Le mesh utilizzano **blendshape facciali**  
2. I blendshape seguono (o possono essere mappati verso) lo **standard ARKit**  
3. La struttura mesh è collegata correttamente ai moduli:

   - mesh principale → `faceMesh`
   - mesh aggiuntive → `extraMeshes`

4. Le mesh sono importate in Unity come **SkinnedMeshRenderer**  
5. Il modello è in formato **FBX** o equivalente compatibile Unity  

Per approfondimenti:  
**Docs/Blendshapes.md**

---

## 7. Linee guida per il team

- Mantenere i nomi dei blendshape compatibili con lo standard ARKit  
- Evitare logica runtime nei dati (ScriptableObject, JSON)  
- Usare JSON solo come formato di scambio, non come formato runtime  
- Non introdurre dipendenze da SDK esterni nel modulo AvatarCore  
- Validare sempre la struttura mesh prima di integrare un nuovo avatar  

---

## 8. Documentazione aggiuntiva

Questo modulo include documentazione tecnica approfondita:

- **Docs/Blendshapes.md**  
  Guida completa ai modelli 3D, blendshape, compatibilità, licenze e raccomandazioni

---

## 9. Obiettivi futuri (non vincolanti)

AvatarCore è progettato per supportare in futuro:

- sistemi di face tracking  
- pipeline di lipsync avanzato  
- avatar generati proceduralmente  
- mapping automatico dei blendshape  
- validazione automatica della struttura mesh  

Nessuna di queste estensioni richiede modifiche strutturali al modulo.

---

## 10. Licenze e note legali

Gli avatar utilizzati nei test (MetaPerson, modelli Asset Store, ecc.) sono soggetti alle rispettive licenze.  
AvatarCore **non distribuisce** alcun modello 3D.

Il modulo è completamente agnostico rispetto alla provenienza dell’avatar.

---

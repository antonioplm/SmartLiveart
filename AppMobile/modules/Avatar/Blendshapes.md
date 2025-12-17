# **Report Tecnico – Modelli 3D con Blendshapes per Unity**

**Obiettivo:**
Selezionare e utilizzare modelli 3D facciali con blendshapes compatibili Unity per testare e sviluppare il sistema **Facial Expression Preset System**.

**Requisiti principali:**

* Supporto a blendshapes multipli per espressioni facciali e visemi.
* Compatibilità Unity (FBX, rigged mesh).
* Licenza adeguata per test e, eventualmente, uso in produzione.
* Prestazioni accettabili per mobile (Android/iOS) e desktop.

---

## **1. MetaPerson (AvatarSDK)**

**Sito:** [https://metaperson.avatarsdk.com/](https://metaperson.avatarsdk.com/)
**Tipo:** Avatar generato procedurale / low-mid poly

**Blendshapes principali:**

* Nodi: `AvatarHead`, `AvatarEyelashes`, `AvatarTeethLower`
* Set completo per bocca, occhi, sopracciglia, jaw
* ~40–50 blendshape utilizzabili in mobile

**Licenza:** Proprietaria SDK; gratuita per test, commerciale richiede licenza

**Pro:**

* Generazione veloce di avatar multipli
* Blendshape standard sufficienti per test su mobile
* Formato FBX e compatibilità Unity

**Contro:**

* Set di blendshape limitato rispetto a modelli ARKit standard
* Realismo medio
* Dipendenza dall’SDK MetaPerson

**Uso consigliato:**

* Test mobile di espressioni facciali
* Proof-of-concept e prototipi rapidi

---

## **2. Asset Store Realistic Head**

**Esempio:** Realistic Male/Female Head Animated with Facial Expressions
**Link:** [Unity Asset Store](https://assetstore.unity.com/packages/3d/characters/realistic-male-head-3d-model-animated-with-facial-expressions-264091)
**Prezzo:** ~€50

**Caratteristiche tecniche:**

* Modello 3D rigged con mesh e blendshapes configurati
* Set di espressioni facciali già pronto
* Compatibile Unity e mobile

**Licenza:** Standard Unity Asset Store EULA → uso commerciale consentito

**Pro:**

* Facile da importare in Unity
* Licenza chiara, costo contenuto
* Blendshape predefiniti sufficienti per test di sistema

**Contro:**

* Potrebbero non avere set completo di blendshape ARKit‑style
* Realismo variabile tra modelli

**Uso consigliato:**

* Test commerciali rapidi
* Demo del sistema di preset facciali
* Prototipi di applicazioni con espressioni facciali

---

## **3. Polywink – Blendshapes On Demand**

**Sito:** [Polywink](https://polywink.com/en/9-automatic-expressions-blendshapes-on-demand.html)

**Caratteristiche tecniche:**

* Genera blendshapes ARKit/FACS per qualsiasi modello 3D di head
* Importabile in Unity come mesh riggata
* Include fino a 157+ blendshapes dettagliati (visemi, micro-espressioni)

**Licenza e costi:**

* Uso commerciale consentito
* Prezzo: da ~499$ (non commerciale) fino a ~999$ per uso commerciale

**Pro:**

* Set completo di blendshape professionale
* Elevata qualità e compatibilità con sistemi di preset facciali

**Contro:**

* Costo elevato
* Non economico per test o prototipi rapidi

**Uso consigliato:**

* Produzione di modelli professionali per applicazioni commerciali
* Sistemi che richiedono set completo di visemi ed espressioni

---

## **4. Modelli Sketchfab gratuiti con blendshapes**

**Esempi:** Shannon, Samantha, Jess, Kelly
**Formato:** FBX con blendshapes (morph targets)

**Licenza:** Creative Commons (attribuzione richiesta, non sempre uso commerciale consentito)

**Pro:**

* Gratuiti e facilmente scaricabili
* Possono essere importati subito in Unity
* Utili per test rapido

**Contro:**

* Set di blendshape limitato, non sempre ARKit‑compatible
* Qualità non uniforme
* Alcune mesh non ottimizzate per mobile

**Uso consigliato:**

* Test rapidi di integrazione
* Debug e sviluppo del sistema senza costi

---

## **5. Humano3D – Rigged Humans ARKit Compatible**

**Sito:** [https://humano3d.com/](https://humano3d.com/product/rigged-rigged-plus-free-model/)
**Tipo:** Modelli realistici, rig completo con ARKit blendshapes (~52 blendshapes)
**Formato:** FBX, Unity‑ready

**Licenza:** Commerciale; alcuni modelli gratuiti per test

**Pro:**

* Blendshape ARKit standard → compatibilità completa con preset system
* Realismo medio-alto
* Ottimizzato per Unity

**Contro:**

* Modelli a pagamento se si richiede produzione
* Mesh più dettagliate → maggiore impatto su performance mobile

**Uso consigliato:**

* Test avanzati del Facial Expression Preset System
* Applicazioni mobile e desktop con espressioni realistiche

---

## **6. Louise – Eisko Digital Human (High-fidelity)**

**Sito:** [https://eisko.com/louise/](https://eisko.com/louise/)
**Tipo:** Modello high-end digital human
**Formato:** FBX, rig FACS avanzato

**Blendshapes principali:**

* ~236 blendshapes per dettagli facciali completi
* Include micro-espressioni, visemi, eye/mouth squint/puff

**Licenza:** Non commerciale gratuita; licenza commerciale disponibile su richiesta

**Pro:**

* Massima qualità di espressioni facciali
* Supporto per test realistici e referenze visive
* Compatibile con pipeline Unity/Unreal

**Contro:**

* Uso commerciale richiede licenza
* Molto pesante per mobile
* Troppo dettagliato per test di prestazioni leggere

**Uso consigliato:**

* Test di qualità e prototipi di alto realismo
* Studio referenziale per animazioni facciali

---

## **7. Considerazioni Tecniche per Unity**

| Aspetto                 | MetaPerson  | Asset Store Realistic Head | Polywink    | Sketchfab Free | Humano3D    | Louise (Eisko)    |
| ----------------------- | ----------- | -------------------------- | ----------- | -------------- | ----------- | ----------------- |
| Blendshapes disponibili | 40–50       | 30–50                      | 157+        | 20–30          | 52          | 236+              |
| Qualità mesh            | Media       | Media                      | Alta        | Media          | Media-Alta  | Alta              |
| Mobile friendly         | ✅           | ✅                          | ⚠️          | ✅              | ✅           | ⚠️                |
| Rig bones               | Limitato    | Completo                   | Completo    | Limitato       | Completo    | Completo FACS     |
| Uso commerciale         | SDK licenza | Asset Store EULA           | Commerciale | CC variabile   | Commerciale | Licenza richiesta |
| Integrazione Unity      | ✅           | ✅                          | ✅           | ✅              | ✅           | ✅                 |

---

## **8. Raccomandazioni per il team di sviluppo**

1. **MetaPerson** → test rapido e mobile proof-of-concept.
2. **Asset Store Realistic Head (~€50)** → test commerciali rapidi, facile da integrare.
3. **Polywink** → produzione professionale, alta qualità di blendshapes per uso commerciale.
4. **Humano3D ARKit** → test realistici di compatibilità ARKit preset.
5. **Sketchfab Free Models** → test rapidi, debug, sviluppo editor tools.
6. **Louise/Eisko** → referenze visive, validazione espressiva, non mobile-friendly.

**Suggerimento operativo:**

* Struttura nodi test: `AvatarHead`, `AvatarEyelashes`, `AvatarTeethLower`
* Usare **MetaPerson** e **Asset Store Realistic Head** come riferimento principale per test mobile e prototipi.
* Utilizzare altri modelli per test comparativi di qualità, blendshape mapping e produzione professionale.

---

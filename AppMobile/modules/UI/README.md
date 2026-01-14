# UI Modules  
**Categoria dei moduli dedicati all’interfaccia utente (UI/UX)**

---

## 1. Scopo della categoria

La cartella `modules/UI/` contiene tutti i moduli relativi alla **User Interface** dell’app, inclusi:

- componenti UI riutilizzabili  
- HUD, overlay, popup, menu  
- sistemi di navigazione e transizioni  
- layout responsive per mobile  
- elementi grafici e prefab UI  
- estensioni future (temi, skin, UI dinamica, ecc.)

Ogni modulo è un **Unity Package locale**, indipendente e integrabile nell’app finale tramite `manifest.json`.

Questa categoria è progettata per essere **scalabile**: puoi aggiungere nuovi moduli UI senza modificare la struttura esistente.

---

## 2. Architettura generale dei moduli UI

I moduli UI seguono una filosofia modulare:

- ogni componente UI è isolato in un package  
- nessun modulo UI deve dipendere da AR, Avatar o AI  
- i moduli UI possono dipendere da TextMeshPro o Unity UI Toolkit  
- i moduli UI devono essere testabili in scene dedicate  

Esempio concettuale:

```
UICommon
UINavigation
UIPopups
UIHUD
UITheme
```

---

## 3. Moduli attualmente presenti

Questa sezione elenca i moduli *attualmente* disponibili nella categoria UI.  
Può essere aggiornata liberamente quando ne aggiungerai di nuovi.

> Nessun modulo presente al momento.

---

## 4. Struttura consigliata per i moduli UI

Ogni modulo UI segue la struttura standard dei Unity Packages:

```
modules/UI/<NomeModulo>/
 ├── package.json
 ├── Runtime/
 ├── Editor/
 ├── Prefabs/        (opzionale)
 ├── Sprites/        (opzionale)
 ├── Fonts/          (opzionale)
 ├── Styles/         (opzionale, per UI Toolkit)
 ├── Docs/           (opzionale)
 └── README.md
```

Questa struttura garantisce:

- chiarezza  
- isolamento  
- compatibilità con Unity Package Manager  
- facilità di testing  

---

## 5. Integrazione dei moduli UI nell’app finale

Per integrare un modulo UI nell’app Unity, aggiungi una dipendenza nel file:

```
app/Packages/manifest.json
```

Esempio:

```json
"com.project.ui.navigation": "file:../../modules/UI/UINavigation"
```

Unity importerà automaticamente il modulo tramite Package Manager.

---

## 6. Aggiungere nuovi moduli UI

Per creare un nuovo modulo nella categoria UI:

1. Crea una cartella in `modules/UI/<NomeModulo>/`
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

- I moduli UI devono rimanere **indipendenti** dagli altri domini  
- Evitare dipendenze da AR, Avatar o AI  
- Ogni modulo UI deve avere una scena di test dedicata  
- Documentare sempre API, componenti e requisiti  
- Evitare logica specifica dell’app finale dentro i moduli  
- Mantenere gli asset UI (sprite, font, stili) dentro il modulo stesso  

---

## 8. Obiettivi futuri (non vincolanti)

La categoria UI è progettata per supportare in futuro:

- sistemi di temi dinamici  
- UI Toolkit avanzata  
- animazioni UI procedurali  
- UI adattiva basata sul contesto  
- componenti UI generati da AI  
- skin personalizzabili  

Queste estensioni non richiedono modifiche strutturali alla categoria.

---

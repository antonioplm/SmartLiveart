# 📱 AR + AI Mobile App

Benvenuto nel repository ufficiale dell'app mobile **Location-based AR** con **Avatar 3D intelligenti** sviluppata in **Unity**.

Questo progetto integra:
- Realtà Aumentata basata sulla posizione (GPS + AR Foundation)
- Avatar 3D animati con espressioni e lip-sync
- Dialoghi dinamici grazie a Intelligenza Artificiale (LLM, TTS/STT)
- Un'app finale modulare integrando 4 moduli principali (AR, Avatar, AI, UI)

---

# 🏗 Architettura del Repository

```
root/
├── docs/                      # Documentazione generale
│
├── modules/                   # Moduli indipendenti (Unity Packages)
│   ├── AR/                    # Realtà Aumentata
│   ├── Avatar/                # Avatar 3D, espressioni, lipsync
│   ├── AI/                    # Dialoghi, RAG, TTS/STT
│   └── UI/                    # UI/UX e componenti grafici
│
├── app/                       # L'app Unity finale che integra tutti i moduli
│   ├── Assets/
│   ├── ProjectSettings/
│   └── Packages/
│
├── tools/                     # Script utili, build, preprocessing
├── tests/                     # Test modulari per ciascun modulo
├── .gitignore
└── README.md
```

---

# 🌿 Workflow GitHub

## Branch principali:
- `main` → versione stabile
- `develop` → integrazione dei moduli

## Feature branch:
- `feature/AR-*`
- `feature/Avatar-*`
- `feature/AI-*`
- `feature/UI-*`

---

# 🔌 Integrazione dei moduli nell'app finale

Unity importa i moduli come **local packages**. Nel file `app/Packages/manifest.json`:

```json
"dependencies": {
  "com.project.ar": "file:../modules/AR",
  "com.project.avatar": "file:../modules/Avatar",
  "com.project.ai": "file:../modules/AI",
  "com.project.ui": "file:../modules/UI"
}
```

---

# 🧩 Moduli dettagliati

### AR
- AR Foundation, ARCore/ARKit  
- Geolocalizzazione, ancoraggi  

### Avatar
- Modelli 3D, animazioni, espressioni facciali, lip-sync  

### AI
- LLM Client, RAG, TTS/STT, gestione dialoghi  

### UI
- Menu, HUD, Canvas prefabs  

---

# 🏗 Build e contenuti inclusi nell’app finale

L’app Unity finale (`app/`) deve includere **solo**:

- scene di produzione  
- asset runtime  
- moduli importati tramite Package Manager  

I moduli presenti in `modules/` possono contenere:

- scene di test  
- asset di debug  
- strumenti editor-only  
- contenuti sperimentali  

> **Importante:**  
> Le scene e gli asset di test dei moduli **non devono essere referenziati** dall’app finale, altrimenti Unity li includerà nella build.

Unity include nella build solo le scene elencate in:

```
File → Build Settings → Scenes In Build
```

Assicurarsi che **solo le scene dell’app finale** siano presenti in questa lista.

---

# 🎬 Struttura delle scene Unity

Le scene sono organizzate in due livelli:

### 1. Scene dell’app finale  
Percorso:

```
app/Assets/Scenes/
```

Queste scene:

- rappresentano il flusso di gioco reale  
- vengono incluse nella build  
- non devono contenere asset di test dei moduli  
- non devono dipendere da scene dei moduli  

### 2. Scene dei moduli  
Ogni modulo può includere scene di test in:

```
modules/<Categoria>/<Modulo>/Scenes/
```

Queste scene:

- servono per testare il modulo in isolamento  
- **non vengono incluse nella build**  
- non devono essere referenziate da scene dell’app finale  
- possono contenere asset di debug o strumenti di sviluppo  

Questa separazione garantisce:

- build leggere  
- moduli indipendenti  
- test più rapidi  
- nessuna dipendenza indesiderata tra app e moduli  

---

# 🚀 Installazione

1. Clona il repository:
```
git clone https://github.com/<tuo-utente>/unity-ar-ai-app.git
```
2. Apri `app/` in Unity Hub  
3. Installa le dipendenze (AR Foundation, ARCore/ARKit, TextMeshPro)  
4. Avvia eventuali servizi backend se necessari  

---

# 🧪 Testing

- Test Unity:  
  ```
  Unity -runTests -projectPath app/
  ```
- Test moduli: separati per AR, Avatar, AI, UI  

---

# 🤝 Come contribuire

1. Crea un feature branch  
2. Sviluppa nella sottocartella del modulo  
3. Apri una Pull Request verso `develop`  
4. Testa l’integrazione nell’app finale  

---

## 📄 Licenza

Questo progetto è distribuito sotto **Apache License 2.0**, una licenza open‑source permissiva ampiamente utilizzata nei progetti di ricerca cofinanziati da enti pubblici (UE, MIUR, programmi regionali).  
La licenza consente:

- utilizzo libero del codice  
- modifica e ridistribuzione  
- integrazione in progetti accademici e industriali  
- protezione tramite clausole di patent grant  

L’obiettivo è favorire la **massima riusabilità** dei risultati della ricerca, garantendo al tempo stesso chiarezza sui diritti d’uso per tutti i partner coinvolti.

---

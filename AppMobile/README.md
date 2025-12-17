# AR + AI Mobile App

Repository ufficiale dell'app mobile **Location-based AR** con **Avatar 3D intelligenti** sviluppata in **Unity**.

Questo progetto integra:
- Realtà Aumentata basata sulla posizione (GPS + AR Foundation)
- Avatar 3D animati con espressioni e lip-sync
- Dialoghi dinamici grazie a Intelligenza Artificiale (LLM, TTS/STT)
- Un'app finale modulare integrando 4 moduli principali (AR, Avatar, AI, UI)

---

# Architettura del Repository

```
root/
├── docs/                      # Documentazione generale
│
├── modules/                   # Moduli indipendenti
│   ├── AR/                    # Modulo AR (Unity packages)
│   ├── Avatar/                # Gestione avatar 3D
│   ├── AI/                    # Dialoghi, RAG, backend, ecc.
│   └── UI/                    # UI/UX e menu di gioco
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


# Integrazione dei moduli nell'app finale

Unity importa i moduli come **local packages**. Nel file `app/Packages/manifest.json`:

```json
"dependencies": {
  "com.project.ar": "file:../modules/AR",
  "com.project.avatar": "file:../modules/Avatar",
  "com.project.ai": "file:../modules/AI",
  "com.project.ui": "file:../modules/UI"
}
```


# Moduli dettagliati

### AR
- AR Foundation, ARCore/ARKit
- Geolocalizzazione, ancoraggi

### Avatar
- Modelli 3D, animazioni, espressioni facciali, lip-sync

### AI
- LLM Client, RAG, TTS/STT, gestione dialoghi

### UI
- Menu, HUD, Canvas prefabs

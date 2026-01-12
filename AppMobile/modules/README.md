# 📦 Moduli Unity – Guida alla Creazione di un Nuovo Modulo

Questa cartella contiene tutti i **moduli indipendenti** dell’app mobile.  
Ogni modulo è un **Unity Package locale**, importato nell’app tramite `manifest.json`.

Questo documento spiega come creare correttamente un nuovo modulo seguendo la struttura del repository.

---

# 🧩 1. Struttura di un modulo

Ogni modulo deve essere organizzato come un **Unity Package**.  
La struttura minima consigliata è:

```
modules/
└── <NomeModulo>/
    ├── package.json
    ├── Runtime/
    ├── Editor/
    ├── Presets/        (opzionale)
    ├── Prefabs/        (opzionale)
    └── README.md
```

### Significato delle cartelle
- **Runtime/** → codice e asset inclusi nella build  
- **Editor/** → script usati solo nell’editor  
- **Presets/** → preset Unity (opzionali)  
- **Prefabs/** → prefab specifici del modulo (opzionali)  
- **README.md** → documentazione del modulo  

> La cartella **Tests/** è opzionale e va aggiunta solo se servono test EditMode/PlayMode.

---

# 📝 2. Creazione del file `package.json`

Ogni modulo deve contenere un `package.json` con nome univoco in formato reverse-domain.

Esempio reale basato sui moduli esistenti:

```json
{
  "name": "com.project.<nome-modulo>",
  "version": "1.0.0",
  "displayName": "<Nome Modulo>",
  "description": "Descrizione del modulo",
  "unity": "6000.3",
  "dependencies": {}
}
```

> Il campo `"unity"` deve riflettere la versione del progetto.

---

# 🔌 3. Aggiunta del modulo all’app Unity

Per rendere disponibile il modulo all’app finale, apri:

```
app/Packages/manifest.json
```

Aggiungi una dipendenza in questo formato:

```json
"com.project.<nome-modulo>": "file:../../modules/<PercorsoModulo>"
```

Esempio reale:

```json
"com.project.avatar.facialexpression": "file:../../modules/Avatar/FacialExpressionPresets"
```

Unity importerà automaticamente il package tramite Package Manager.

---

# 🔀 4. Workflow Git consigliato

1. Crea un branch dedicato:
   ```
   git checkout -b feature/<NomeModulo>-base
   ```
2. Crea la struttura del modulo in `modules/`
3. Aggiungi il modulo al `manifest.json` dell’app
4. Testa l’integrazione aprendo l’app Unity (`app/`)
5. Apri una Pull Request verso `develop`

---

# 🧪 5. (Opzionale) Aggiungere test al modulo

Se il modulo contiene logica complessa, puoi aggiungere:

```
modules/<NomeModulo>/Tests/
├── Editor/
└── Runtime/
```

E nel `package.json`:

```json
"tests": {
  "editMode": "Tests/Editor",
  "playMode": "Tests/Runtime"
}
```

---

# 📘 6. Documentazione del modulo

Ogni modulo deve includere un `README.md` con:

- Scopo del modulo  
- API o componenti principali  
- Dipendenze interne  
- Esempi di utilizzo  
- Note di integrazione con l’app  

---

# 🎉 Modulo creato!

Seguendo questi passaggi, il modulo sarà:

- isolato  
- riutilizzabile  
- integrabile come Unity Package  
- coerente con la struttura del repository  


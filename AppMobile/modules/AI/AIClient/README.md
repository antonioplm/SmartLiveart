# AI Client

Modulo responsabile della comunicazione con il backend AI.  
Gestisce richieste, risposte in streaming, parsing dei chunk JSON e la sessione conversazionale.

## 🎯 Scopo
- Inviare richieste al backend AI.
- Ricevere risposte in streaming (SSE/WebSocket).
- Estrarre testo, eventi e metadati dai chunk JSON.
- Gestire sessioni e turni conversazionali.
- Fornire un’interfaccia semplice al Dialog Orchestrator.

## 📦 Contenuto
- `AiClient.cs` – client principale.
- `AiStreamingParser.cs` – parser per chunk JSON.
- `AiSessionManager.cs` – gestione sessione.
- `JsonContracts.cs` – contratti dati condivisi.

## 🔌 Dipendenze
Nessuna dipendenza interna.

## 🧩 Integrazione
Il modulo Dialog utilizza `AiClient` per inviare testo e ricevere risposte AI.

## 🧪 Test
Da aggiungere se necessario.

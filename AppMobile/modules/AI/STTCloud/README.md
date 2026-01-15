# STT Cloud

Modulo per il riconoscimento vocale cloud.  
Gestisce l’invio dell’audio PCM/WAV al backend e riceve testo parziale e finale.

## 🎯 Scopo
- Inviare audio al backend STT.
- Ricevere testo parziale e finale.
- Supportare fallback rispetto allo STT locale.
- Fornire streaming di trascrizione al Dialog Orchestrator.

## 📦 Contenuto
- `SttCloudClient.cs`
- `SttStreamingParser.cs`
- `SttRequestBuilder.cs`

## 🔌 Dipendenze
Nessuna.

## 🧩 Integrazione
Il Dialog Orchestrator usa questo modulo quando lo STT locale non è disponibile.

## 🧪 Test
Da aggiungere.

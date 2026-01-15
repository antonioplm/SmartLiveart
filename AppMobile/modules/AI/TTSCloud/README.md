# TTS Cloud

Modulo per la generazione vocale cloud.  
Gestisce lo streaming audio e, se disponibile, lo streaming dei visemi.

## 🎯 Scopo
- Richiedere audio TTS al backend.
- Ricevere audio in streaming.
- Ricostruire AudioClip in tempo reale.
- Estrarre visemi se forniti dal backend.

## 📦 Contenuto
- `TtsCloudClient.cs`
- `TtsAudioStreamBuilder.cs`
- `TtsVisemeStreamParser.cs`

## 🔌 Dipendenze
Nessuna.

## 🧩 Integrazione
Il Dialog Orchestrator usa questo modulo per generare la risposta vocale dell’avatar.

## 🧪 Test
Da aggiungere.

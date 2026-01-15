# Dialog Orchestrator

Modulo centrale dell’app.  
Coordina l’intera pipeline conversazionale: STT → AI → TTS → Lipsync → Avatar.

## 🎯 Scopo
- Gestire gli stati della conversazione.
- Coordinare STT locale/cloud.
- Inviare testo all’AI.
- Gestire lo streaming della risposta AI.
- Attivare TTS cloud.
- Sincronizzare audio e lipsync.
- Aggiornare la UI.

## 📦 Contenuto
- `DialogOrchestrator.cs`
- `ConversationState.cs`
- `PipelineController.cs`
- `TurnManager.cs`
- `EventBus.cs`

## 🔌 Dipendenze
- Moduli AI
- Moduli Avatar
- Moduli UI

## 🧩 Integrazione
È il cuore dell’app: tutti i moduli passano da qui.

## 🧪 Test
Da aggiungere.

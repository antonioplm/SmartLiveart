# Avatar Audio Capture

Modulo responsabile della cattura audio locale dal microfono.  
Fornisce buffer PCM per STT locale o cloud.

## 🎯 Scopo
- Catturare audio dal microfono.
- Bufferizzare campioni PCM.
- Fornire audio grezzo ai moduli STT.
- Gestire permessi e device selection.

## 📦 Contenuto
- `IAudioCapture.cs`
- `MicrophoneCapture.cs`
- `AudioBuffer.cs`

## 🔌 Dipendenze
Nessuna.

## 🧩 Integrazione
Il Dialog Orchestrator usa questo modulo per avviare e fermare la cattura audio.

## 🧪 Test
Da aggiungere.

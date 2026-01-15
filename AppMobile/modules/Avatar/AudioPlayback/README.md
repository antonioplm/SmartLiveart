# Avatar Audio Playback

Modulo responsabile della riproduzione audio locale.  
Gestisce AudioClip, streaming TTS e sincronizzazione con il lipsync.

## 🎯 Scopo
- Riprodurre audio TTS.
- Gestire streaming audio chunked.
- Notificare inizio/fine riproduzione.
- Fornire audio al modulo LipSync.

## 📦 Contenuto
- `IAudioPlayback.cs`
- `AudioPlaybackController.cs`
- `AudioClipStreamPlayer.cs`

## 🔌 Dipendenze
Nessuna.

## 🧩 Integrazione
Il Dialog Orchestrator usa questo modulo per riprodurre la risposta vocale dell’avatar.

## 🧪 Test
Da aggiungere.

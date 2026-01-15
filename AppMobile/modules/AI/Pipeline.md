# 📘 **Documento Tecnico – Pipeline Audio Conversazionale Mobile (STT → AI → TTS → Lipsync → Avatar)**  
**Versione:** 1.0  
**Ambito:** App mobile Unity (Android + iOS) per dialogo vocale con avatar

---

# 1. Introduzione
L’obiettivo del sistema è permettere un dialogo naturale tra un utente e un avatar 3D, tramite:

- input vocale dell’utente  
- riconoscimento vocale (STT)  
- elaborazione AI su backend  
- generazione vocale (TTS)  
- riproduzione audio  
- lipsync in tempo reale sull’avatar  

La discussione ha analizzato:

- test del TTS  
- pipeline completa  
- architetture possibili  
- limiti e capacità dei device mobile  
- scelta ottimale per un pubblico eterogeneo (studenti, turisti)  
- STT locale vs cloud  
- TTS locale vs cloud  
- streaming vs pipeline sequenziale  

---

# 2. Test del TTS: obiettivo e pipeline
Il punto di partenza è stato il test della pipeline:

```
Testo → TTS → AudioClip → Lipsync → Avatar
```

Il test serve a verificare:

- che il TTS generi audio valido  
- che Unity carichi correttamente l’audio  
- che il lipsync riceva campioni reali  
- che l’avatar si muova in sync  

È stato definito uno script di test per:

- caricare un file WAV/MP3  
- riprodurlo tramite AudioSource  
- collegarlo al sistema di lipsync  

---

# 3. Pipeline completa di dialogo vocale
La pipeline conversazionale completa è:

```
Voce utente → STT → Testo → Backend AI → Testo → TTS → Audio → Lipsync → Avatar
```

Il backend AI risponde tramite **JSON**, e l’app deve:

1. estrarre il testo  
2. inviarlo al TTS  
3. riprodurre l’audio  
4. pilotare il lipsync  

---

# 4. Esistono pipeline più veloci?
Sì. La pipeline classica è funzionale ma non ottimale in termini di latenza.

Sono state analizzate 4 architetture più veloci:

### 4.1 Streaming completo
```
STT streaming → AI streaming → TTS streaming → lipsync
```
L’avatar inizia a parlare entro **200–400 ms**.

### 4.2 TTS predittivo
Il TTS inizia a generare audio prima che la frase sia completa.

### 4.3 TTS con visemi integrati
Il TTS genera direttamente:

- audio  
- visemi  
- durata fonemi  

Riduce la pipeline a:

```
Testo → TTS (audio + visemi) → Avatar
```

### 4.4 AI vocale end‑to‑end
Un unico modello trasforma voce in voce, senza testo intermedio.

---

# 5. JSON rimane compatibile con lo streaming
È stato chiarito che:

👉 **Lo streaming non elimina il JSON.**

Il backend può continuare a inviare:

- chunk JSON  
- eventi JSON (SSE)  
- pacchetti JSON con audio base64  
- token parziali  

Esempio:

```
{"partial_text": "Certo,"}
{"partial_text": "posso"}
{"partial_text": "aiutarti."}
{"done": true}
```

---

# 6. STT e TTS: lato app o lato backend?
Sono state analizzate le due possibilità:

## 6.1 STT/TTS lato app
Pro:
- latenza bassissima  
- offline  

Contro:
- modelli pesanti  
- consumo CPU  
- qualità inferiore  
- non uniforme su Android  

## 6.2 STT/TTS lato backend
Pro:
- qualità alta  
- modelli aggiornabili  
- nessun carico sul device  

Contro:
- latenza di rete  
- dipendenza dalla connessione  

## 6.3 Architettura ibrida (consigliata)
```
STT locale → AI cloud → TTS cloud → lipsync locale
```

È la soluzione più veloce e più stabile per mobile.

---

# 7. Considerazioni specifiche per app mobile (Android + iOS)
L’app è sviluppata in Unity per Android e iOS.

### 7.1 STT locale su iOS
- SFSpeechRecognizer  
- molto affidabile  
- offline per molte lingue  
- latenza bassa  

### 7.2 STT locale su Android
La situazione è più complessa:

- SpeechRecognizer esiste su quasi tutti i device  
- ma **non garantisce** STT offline  
- alcuni device non hanno modelli offline  
- alcuni device non hanno Google Services  
- alcuni device usano solo STT cloud  
- alcuni device non supportano STT affatto  

Conclusione:

👉 **STT locale Android non è affidabile al 100% su device eterogenei.**

---

# 8. Caso d’uso reale: studenti con smartphone personali
La sperimentazione iniziale coinvolge studenti liceali con smartphone personali.

Questo implica:

- device molto diversi  
- versioni Android diverse  
- alcuni con Google, altri senza  
- alcuni con STT offline, altri no  
- qualità microfoni variabile  

Per questo:

👉 **Non si può basare l’esperienza solo su STT locale Android.**

---

# 9. Architettura STT consigliata per studenti e turisti
La soluzione ottimale è una pipeline **ibrida con fallback automatico**.

## 9.1 Pipeline consigliata
```
STT locale (se disponibile)
↓ fallback automatico
STT cloud
↓
Backend AI (JSON)
↓
TTS cloud (streaming)
↓
AudioClip + Lipsync locale
↓
Avatar
```

## 9.2 Vantaggi
- compatibilità totale  
- latenza ottimizzata  
- qualità vocale uniforme  
- nessun blocco su device problematici  
- esperienza fluida anche con rete debole  

---

# 10. Scelta finale raccomandata
Per un’app mobile Unity destinata a:

- studenti  
- turisti  
- pubblico eterogeneo  

la pipeline migliore è:

### ✔ STT locale nativo (iOS + Android)  
### ✔ fallback automatico a STT cloud  
### ✔ AI cloud con JSON streaming  
### ✔ TTS cloud streaming  
### ✔ lipsync locale in Unity  

Questa architettura garantisce:

- latenza bassa  
- qualità alta  
- compatibilità totale  
- scalabilità  
- esperienza naturale  

---

# 11. Conclusione
La discussione ha portato a definire una pipeline conversazionale **robusta**, **scalabile** e **ottimizzata per mobile**, capace di funzionare su smartphone eterogenei e in contesti reali come scuole e turismo.

La soluzione finale è un’architettura **ibrida**, con:

- STT locale quando possibile  
- fallback cloud quando necessario  
- backend AI centralizzato  
- TTS streaming  
- lipsync locale  

Il tutto mantenendo **JSON come formato di scambio**, anche in modalità streaming.

---

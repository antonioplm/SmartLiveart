using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Threading.Tasks;

/// <summary>
/// 💬 Simula o riproduce parlato da testo.
/// Modalità:
/// 1️⃣ Simulazione fonetica senza audio
/// 2️⃣ TTS + visemi sincronizzati (OpenAI / ElevenLabs)
/// </summary>
public class LipSyncTextSimulator : MonoBehaviour
{
    public enum Mode { Simulazione, TTS }
    public enum TTSProvider { OpenAI, ElevenLabs }

    [Header("Configurazione")]
    public Mode modalita = Mode.Simulazione;
    public TTSProvider provider = TTSProvider.OpenAI;

    [TextArea(3, 5)]
    public string testo = "Ciao, sono Telesio e parlo grazie al tuo codice!";

    public AudioSource audioSource;
    public float velocitaParlato = 12f;
    public float moltiplicatoreDurataVocali = 1.3f;
    public float durataPausa = 0.25f;

    private Coroutine simulazioneCorrente;

    private ILipSyncTarget target;   // <-- riferimento generico al sistema facciale

    public static LipSyncTextSimulator Instance { get; private set; }

    private void Awake()
    {
        // Singleton setup
        if (Instance != null && Instance != this)
        {
            Destroy(this.gameObject);
            return;
        }

        Instance = this;
    }

    void Start()
    {
        // Trova automaticamente un componente che implementa ILipSyncTarget
        var all = FindObjectsByType<MonoBehaviour>(FindObjectsSortMode.None);

        foreach (var mb in all)
        {
            if (mb is ILipSyncTarget t)
            {
                target = t;
                break;
            }
        }

        if (target == null)
        {
            Debug.LogError("❌ Nessun ILipSyncTarget trovato nella scena!");
            return;
        }

        if (modalita == Mode.Simulazione)
            SimulaTesto(testo);
        else
            _ = RiproduciTTSESeguiVisemi(testo);
    }

    // -----------------------------
    // 🎭 SIMULAZIONE SOLO TESTO
    // -----------------------------
    public void SimulaTesto(string testo)
    {
        if (simulazioneCorrente != null)
            StopCoroutine(simulazioneCorrente);

        simulazioneCorrente = StartCoroutine(SimulazioneRoutine(testo));
    }

    private IEnumerator SimulazioneRoutine(string testo)
    {
        var fonemi = EstraiFonemi(testo);
        string ultimoViseme = "Neutral";

        foreach (var fonema in fonemi)
        {
            string viseme = MappaFonemaVisema(fonema);
            float durata = CalcolaDurataFonema(fonema);

            float durataTransizione = IsVocale(fonema) ? 0.08f : 0.04f;

            if (viseme != ultimoViseme)
            {
                target.SetViseme(viseme, durataTransizione);
                ultimoViseme = viseme;
            }

            yield return new WaitForSeconds(durata);
        }

        target.SetViseme("Neutral", 0.15f);
    }

    private float CalcolaDurataFonema(string fonema)
    {
        if (IsPausa(fonema)) return durataPausa;
        float baseDur = 1f / velocitaParlato;
        return IsVocale(fonema) ? baseDur * moltiplicatoreDurataVocali : baseDur;
    }

    // -----------------------------
    // 🧠 TTS CON SINCRONIZZAZIONE
    // -----------------------------
    public async Task RiproduciTTSESeguiVisemi(string testo)
    {
        if (audioSource == null)
        {
            Debug.LogError("❌ AudioSource mancante!");
            return;
        }

        Debug.Log($"🔊 Genero audio TTS con {provider}: {testo}");

        // 1️⃣ Genera audio
        AudioClip clip = await GeneraAudioDaTesto(testo);
        if (clip == null)
        {
            Debug.LogError("❌ Impossibile generare audio dal TTS.");
            return;
        }

        // 2️⃣ Avvia visemi simulati in parallelo
        StartCoroutine(SimulazioneRoutine(testo));

        // 3️⃣ Riproduci audio
        audioSource.clip = clip;
        audioSource.Play();
    }

    private async Task<AudioClip> GeneraAudioDaTesto(string testo)
    {
        // 🔸 Simulazione asincrona placeholder:
        await Task.Delay(500); // Simula tempo di rete
        Debug.Log($"✅ (Mock) Audio TTS generato per '{testo}'");
        return AudioClip.Create("FakeTTS", 44100, 1, 44100, false);
    }

    // -----------------------------
    // 🔠 MAPPATURA FONEMI → VISEMI
    // -----------------------------
    private List<string> EstraiFonemi(string testo)
    {
        List<string> fonemi = new();
        testo = testo.ToLower();

        foreach (char c in testo)
        {
            if ("aeiou".Contains(c)) fonemi.Add(c.ToString());
            else if ("m".Contains(c)) fonemi.Add("m");
            else if ("fpv".Contains(c)) fonemi.Add("f");
            else if ("tdnlr".Contains(c)) fonemi.Add("t");
            else if ("kgcq".Contains(c)) fonemi.Add("k");
            else if ("szx".Contains(c)) fonemi.Add("s");
            else if (".!?".Contains(c)) fonemi.Add("punto");
            else if (",;:".Contains(c)) fonemi.Add("virgola");
            else fonemi.Add("sil");
        }
        return fonemi;
    }

    private string MappaFonemaVisema(string fonema)
    {
        fonema = fonema.ToLower();

        switch (fonema)
        {
            case "a": return "Talk_A";
            case "e": return "Talk_E";
            case "i": return "Talk_I";
            case "o": return "Talk_O";
            case "u": return "Talk_U";

            case "m":
            case "p":
            case "b": return "Talk_P";

            case "f":
            case "v": return "Talk_F";

            case "t":
            case "d":
            case "n":
            case "l":
            case "r": return "Talk_T";

            case "k":
            case "g":
            case "c":
            case "q": return "Talk_K";

            case "s":
            case "z":
            case "x": return "Talk_S";

            case "sil":
            case "virgola":
            case "punto":
                return "Neutral";

            default: return "Neutral";
        }
    }

    private bool IsVocale(string f) => "aeiou".Contains(f);
    private bool IsPausa(string f) => f == "punto" || f == "virgola" || f == "sil";
}

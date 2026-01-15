using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Threading.Tasks;
using AvatarCore;

/// <summary>
/// 💬 Simula o riproduce parlato da testo.
/// Modalità:
/// 1️⃣ Simulazione fonetica senza audio
/// 2️⃣ TTS + visemi sincronizzati (OpenAI / ElevenLabs)
/// </summary>

// Se vuoi, posso prepararti anche:
// una versione con coarticolazione avanzata (basata su tabelle professionali)
// una versione sincronizzata con TTS reale (OpenAI / ElevenLabs)
// un inspector custom per controllare la simulazione in editor

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
    public float durataPausa = 0.30f;

    private Coroutine simulazioneCorrente;
    private ILipSyncTarget target;

    public static LipSyncTextSimulator Instance { get; private set; }

    private void Awake()
    {
        if (Instance != null && Instance != this)
        {
            Destroy(this.gameObject);
            return;
        }

        Instance = this;
    }

    void Start()
    {
        target = TrovaTarget();

        ILipSyncTarget TrovaTarget()
        {
            var all = FindObjectsByType<MonoBehaviour>(FindObjectsInactive.Exclude, FindObjectsSortMode.None);
            foreach (var mb in all)
                if (mb is ILipSyncTarget t)
                    return t;

            return null;
        }

        if (target == null)
        {
            Debug.LogError("❌ Nessun ILipSyncTarget trovato nella scena!");
            return;
        }
        else
            Debug.Log("Target trovato: " + target);

/*
        if (modalita == Mode.Simulazione)
            SimulaTesto(testo);
        else
            _ = RiproduciTTSESeguiVisemi(testo);
          */
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
            float transizione = CalcolaTransizione(fonema);

            if (viseme != ultimoViseme)
            {
                target.SetViseme(viseme, transizione);
                ultimoViseme = viseme;
            }

            yield return new WaitForSeconds(durata);
        }

        target.SetViseme("Neutral", 0.15f);
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

        AudioClip clip = await GeneraAudioDaTesto(testo);
        if (clip == null)
        {
            Debug.LogError("❌ Impossibile generare audio dal TTS.");
            return;
        }

        StartCoroutine(SimulazioneRoutine(testo));

        audioSource.clip = clip;
        audioSource.Play();
    }

    private async Task<AudioClip> GeneraAudioDaTesto(string testo)
    {
        await Task.Delay(500);
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

    private string MappaFonemaVisema(string f)
    {
        return f switch
        {
            "a" => "Talk_A",
            "e" => "Talk_E",
            "i" => "Talk_I",
            "o" => "Talk_O",
            "u" => "Talk_U",

            "m" or "p" or "b" => "Talk_P",
            "f" or "v" => "Talk_F",
            "t" or "d" or "n" or "l" or "r" => "Talk_T",
            "k" or "g" or "c" or "q" => "Talk_K",
            "s" or "z" or "x" => "Talk_S",

            "punto" or "virgola" or "sil" => "Neutral",
            _ => "Neutral"
        };
    }

    // -----------------------------
    // ⏱️ DURATE REALISTICHE
    // -----------------------------
    private float CalcolaDurataFonema(string f)
    {
        float baseDur = 1f / velocitaParlato;

        if (IsPausa(f)) return durataPausa;
        if (IsVocale(f)) return baseDur * 1.4f;
        if ("ptk".Contains(f)) return baseDur * 0.6f;
        if ("sz".Contains(f)) return baseDur * 0.8f;

        return baseDur;
    }

    // -----------------------------
    // 🔄 COARTICOLAZIONE
    // -----------------------------
    private float CalcolaTransizione(string f)
    {
        if (IsVocale(f)) return 0.10f;
        if ("ptk".Contains(f)) return 0.04f;
        if ("sz".Contains(f)) return 0.06f;
        return 0.08f;
    }

    private bool IsVocale(string f) => "aeiou".Contains(f);
    private bool IsPausa(string f) => f == "punto" || f == "virgola" || f == "sil";
}

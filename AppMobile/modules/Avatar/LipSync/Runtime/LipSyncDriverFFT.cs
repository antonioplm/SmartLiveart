using UnityEngine;
using System.Collections;
using AvatarCore;

[RequireComponent(typeof(AudioSource))]
public class LipSyncDriverFFT : MonoBehaviour
{
    [Header("References")]
    public AudioSource audioSource;
    
    [Header("LipSync Target")]
    public MonoBehaviour targetComponent;
    private ILipSyncTarget target;

    [Header("Microphone")]
    public string microphoneDevice = "";
    public int sampleRate = 48000; // il tuo device supporta 48000

    [Header("Sensitivity")]
    [Range(0f, 20f)] public float loudnessGain = 8f;
    [Range(0f, 1f)] public float smoothness = 0.1f;
    [Range(0f, 0.05f)] public float minAmplitude = 0.001f;

    [Header("Neutral viseme")]
    public string neutralViseme = "Neutral";

    private float[] samples = new float[1024];
    private float[] spectrum = new float[1024];

    private float loudness;
    private float smoothedLoudness;
    private float silenceTimer = 0f;
    private const float silenceThreshold = 0.25f;

    private string baseVisemeBeforeSpeech;
    private bool wasSpeaking = false;

    private string candidateViseme = "Neutral";
    private float visemeTimer = 0f;
    private const float visemeMinDuration = 0.05f;

    private float lowSmooth, midSmooth, highSmooth;

    // diagnostica
    private bool warnedZeroBuffer = false;
    private int zeroBufferFrames = 0;

    void Start()
    {
        if (audioSource == null)
            audioSource = GetComponent<AudioSource>();

        audioSource.bypassEffects = true;
        audioSource.bypassListenerEffects = true;
        audioSource.bypassReverbZones = true;
        audioSource.spatialBlend = 0f;
        audioSource.volume = 1f;
        audioSource.mute = false;
        audioSource.playOnAwake = false;

        // Auto-find ILipSyncTarget
        if (targetComponent != null)
            target = targetComponent as ILipSyncTarget;
        else
        {
            var all = FindObjectsByType<MonoBehaviour>(FindObjectsInactive.Exclude, FindObjectsSortMode.None);
            foreach (var mb in all)
                if (mb is ILipSyncTarget t)
                {
                    target = t;
                    break;
                }
        }

        if (target == null)
            Debug.LogWarning("⚠ Nessun ILipSyncTarget trovato dal driver FFT.");
        else
            Debug.Log("🎯 Target lipsync collegato: " + target);
    }

    // ============================
    // MICROPHONE CONTROL
    // ============================

    public void StartMicrophone()
    {
        StartCoroutine(InitMicrophone());
    }

    public void StopMicrophone()
    {
        if (audioSource != null)
            audioSource.Stop();

        Microphone.End(null);
        Debug.Log("🛑 Microfono fermato");
    }

    private IEnumerator InitMicrophone()
    {
        if (Microphone.devices.Length == 0)
        {
            Debug.LogWarning("⚠ Nessun microfono trovato.");
            yield break;
        }

        if (string.IsNullOrEmpty(microphoneDevice))
            microphoneDevice = Microphone.devices[0];

        int minFreq, maxFreq;
        Microphone.GetDeviceCaps(microphoneDevice, out minFreq, out maxFreq);
        Debug.Log($"🎤 Device: {microphoneDevice} | minFreq: {minFreq}, maxFreq: {maxFreq}");

        if (minFreq != 0 && maxFreq != 0)
            sampleRate = maxFreq;

        Debug.Log("🎤 Inizializzazione microfono a " + sampleRate + " Hz");

        audioSource.Stop();
        audioSource.clip = Microphone.Start(microphoneDevice, true, 1, sampleRate);

        while (Microphone.GetPosition(microphoneDevice) <= 0)
            yield return null;

        audioSource.loop = true;
        audioSource.Play();

        warnedZeroBuffer = false;
        zeroBufferFrames = 0;

        Debug.Log("🎤 Microfono avviato correttamente, AudioSource.isPlaying = " + audioSource.isPlaying);
    }

    // 🔥 Cattura il buffer del microfono
    private void OnAudioFilterRead(float[] data, int channels)
    {
        int length = Mathf.Min(data.Length, samples.Length);
        bool allZero = true;

        for (int i = 0; i < length; i++)
        {
            samples[i] = data[i];
            if (allZero && Mathf.Abs(data[i]) > 0.0000001f)
                allZero = false;
        }

        if (allZero)
        {
            zeroBufferFrames++;
            if (!warnedZeroBuffer && zeroBufferFrames > 30)
            {
                warnedZeroBuffer = true;
                Debug.LogWarning("⚠ Il buffer audio del microfono contiene solo zeri. " +
                                 "Controlla: volume OS, modalità esclusiva, miglioramenti audio, mixer, spatialBlend.");
            }
        }
        else
        {
            zeroBufferFrames = 0;
        }
    }

    // ============================
    // LIPSYNC LOGIC
    // ============================

    void Update()
    {
        if (audioSource == null || audioSource.clip == null || target == null)
            return;

        UpdateAudioData();
        float loudnessFactor = ComputeLoudnessFactor();

        if (HandleSilence(loudnessFactor))
            return;

        float low = SumBand(0, 50);
        float mid = SumBand(50, 200);
        float high = SumBand(200, 512);

        UpdateViseme(low, mid, high, loudnessFactor);
    }

    void UpdateAudioData()
    {
        audioSource.GetSpectrumData(spectrum, 0, FFTWindow.Hamming);

        float sum = 0f;
        for (int i = 0; i < samples.Length; i++)
            sum += samples[i] * samples[i];

        loudness = Mathf.Sqrt(sum / samples.Length) * loudnessGain;
        smoothedLoudness = Mathf.Lerp(smoothedLoudness, loudness, 1f - smoothness);

        // Debug veloce: commenta se ti dà fastidio
        // Debug.Log("🔊 Loudness raw: " + loudness + " | smooth: " + smoothedLoudness);
    }

    float ComputeLoudnessFactor()
    {
        float factor = Mathf.Log10(1f + smoothedLoudness * 100f);
        return Mathf.Clamp01(factor);
    }

    bool HandleSilence(float loudnessFactor)
    {
        if (smoothedLoudness < minAmplitude)
        {
            silenceTimer += Time.deltaTime;

            if (silenceTimer >= silenceThreshold && wasSpeaking)
            {
                target.SetViseme(neutralViseme, 0.12f);
                wasSpeaking = false;
            }
            return true;
        }

        if (!wasSpeaking)
        {
            baseVisemeBeforeSpeech = target.CurrentViseme;
            wasSpeaking = true;
        }

        silenceTimer = 0f;
        return false;
    }

    void UpdateViseme(float low, float mid, float high, float loudnessFactor)
    {
        string newViseme = DetectViseme(low, mid, high, smoothedLoudness);

        if (newViseme != candidateViseme)
        {
            candidateViseme = newViseme;
            visemeTimer = 0f;
            return;
        }

        visemeTimer += Time.deltaTime;

        if (visemeTimer >= visemeMinDuration && target.CurrentViseme != newViseme)
        {
            target.SetJaw(loudnessFactor);
            target.SetViseme(newViseme, 0.08f);
            // Debug.Log("👄 Viseme: " + newViseme + " | jaw: " + loudnessFactor);
        }
    }

    float SumBand(int start, int end)
    {
        float sum = 0f;
        end = Mathf.Min(end, spectrum.Length);
        for (int i = start; i < end; i++)
            sum += spectrum[i];
        return sum;
    }

    // 🎯 VERSIONE CALIBRATA DEL DETECT VISEME
    string DetectViseme(float low, float mid, float high, float loud)
    {
        lowSmooth = Mathf.Lerp(lowSmooth, low, 0.25f);
        midSmooth = Mathf.Lerp(midSmooth, mid, 0.25f);
        highSmooth = Mathf.Lerp(highSmooth, high, 0.25f);

        low = lowSmooth;
        mid = midSmooth;
        high = highSmooth;

        float total = low + mid + high + 0.0001f;
        low /= total;
        mid /= total;
        high /= total;

        if (loud < 0.005f) return "Neutral";
        if (low > mid && low > high) return "Talk_O";
        if (mid > low && mid > high) return "Talk_E";
        if (high > low && high > mid) return "Talk_I";

        return "Talk_A";
    }
}

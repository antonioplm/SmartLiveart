using UnityEngine;
using System.Collections;

[RequireComponent(typeof(AudioSource))]
public class LipSyncDriverFFT : MonoBehaviour
{
    [Header("References")]
    public AudioSource audioSource;
    public ILipSyncTarget target;

    [Header("Input")]
    public bool useMicrophone = false;
    public string microphoneDevice = "";
    public int sampleRate = 44100;

    [Header("Sensitivity")]
    [Range(0f, 5f)] public float loudnessGain = 2f;
    [Range(0f, 1f)] public float smoothness = 0.3f;
    [Range(0f, 1f)] public float minAmplitude = 0.01f;

    [Header("Neutral viseme")]
    public string neutralViseme = "Neutral";

    private float[] samples = new float[1024];
    private float[] spectrum = new float[1024];

    private float loudness;
    private float smoothedLoudness;
    private float silenceTimer = 0f;
    private const float silenceThreshold = 0.3f;

    private string baseVisemeBeforeSpeech;
    private bool wasSpeaking = false;

    private string candidateViseme = "Neutral";
    private float visemeTimer = 0f;
    private const float visemeMinDuration = 0.06f;

    private float lowSmooth, midSmooth, highSmooth;

    void Start()
    {
        if (audioSource == null)
            audioSource = GetComponent<AudioSource>();

        if (useMicrophone)
            StartCoroutine(InitMicrophone());
    }

    IEnumerator InitMicrophone()
    {
        if (Microphone.devices.Length == 0)
        {
            Debug.LogWarning("No microphone found.");
            yield break;
        }

        microphoneDevice = Microphone.devices[0];
        audioSource.loop = true;
        audioSource.clip = Microphone.Start(microphoneDevice, true, 1, sampleRate);

        while (Microphone.GetPosition(microphoneDevice) <= 0)
            yield return null;

        audioSource.Play();
    }

    void Update()
    {
        if (!IsAudioReady() || target == null)
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

    bool IsAudioReady()
    {
        return audioSource != null && (audioSource.clip != null || useMicrophone);
    }

    void UpdateAudioData()
    {
        audioSource.GetOutputData(samples, 0);
        audioSource.GetSpectrumData(spectrum, 0, FFTWindow.Hamming);

        float sum = 0f;
        for (int i = 0; i < samples.Length; i++)
            sum += samples[i] * samples[i];

        loudness = Mathf.Sqrt(sum / samples.Length) * loudnessGain;
        smoothedLoudness = Mathf.Lerp(smoothedLoudness, loudness, 1f - smoothness);
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
                string targetViseme = baseVisemeBeforeSpeech ?? neutralViseme;
                target.SetViseme(targetViseme, 0.15f);
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

        if (loud < 0.02f) return "Talk_M";
        if (low > 0.6f && mid < 0.3f) return "Talk_A";
        if (mid > 0.5f && low < 0.3f) return "Talk_E";
        if (high > 0.5f && mid > 0.3f) return "Talk_I";
        if (low > 0.5f && high < 0.3f) return "Talk_O";
        if (low > 0.4f && mid > 0.3f) return "Talk_U";
        if (high > 0.45f && loud > 0.03f) return "Talk_S";
        if (loud > 0.05f && mid > 0.3f && low > 0.3f) return "Talk_P";

        return "Talk_A";
    }

    public void StartMicrophone()
    {
        if (audioSource == null)
            audioSource = GetComponent<AudioSource>();

        // Ferma eventuale audio in corso
        audioSource.Stop();

        // Avvia il microfono
        audioSource.clip = Microphone.Start(null, true, 1, 44100);
        audioSource.loop = true;

        // Attendi che il microfono inizi a registrare
        while (Microphone.GetPosition(null) <= 0) { }

        audioSource.Play();

        Debug.Log("🎤 Microfono avviato");
    }

    public void StopMicrophone()
    {
        if (audioSource != null)
            audioSource.Stop();

        Microphone.End(null);

        Debug.Log("🛑 Microfono fermato");
    }
}

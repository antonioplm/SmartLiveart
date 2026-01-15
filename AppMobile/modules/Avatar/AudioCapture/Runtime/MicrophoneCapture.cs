using UnityEngine;

public class MicrophoneCapture : MonoBehaviour, IAudioCapture
{
    public bool IsRecording { get; private set; }

    private string deviceName;
    private AudioClip clip;
    private int sampleRate = 48000;
    private float[] buffer = new float[1024];

    public void StartCapture()
    {
        if (Microphone.devices.Length == 0)
        {
            Debug.LogWarning("Nessun microfono disponibile.");
            return;
        }

        deviceName ??= Microphone.devices[0];
        clip = Microphone.Start(deviceName, true, 1, sampleRate);
        IsRecording = true;
    }

    public void StopCapture()
    {
        if (!IsRecording) return;

        Microphone.End(deviceName);
        IsRecording = false;
    }

    public float[] GetLatestSamples()
    {
        if (!IsRecording || clip == null)
            return buffer;

        clip.GetData(buffer, Microphone.GetPosition(deviceName) - buffer.Length);
        return buffer;
    }

    public int GetSampleRate() => sampleRate;
}

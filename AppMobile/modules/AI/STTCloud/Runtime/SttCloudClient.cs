public class SttCloudClient : ISttProvider
{
    public event System.Action<string> OnPartialResult;
    public event System.Action<string> OnFinalResult;
    public event System.Action<string> OnError;

    public void SendAudio(float[] pcmData, int sampleRate)
    {
        // Stub: invio al backend
        OnPartialResult?.Invoke("…");
        OnFinalResult?.Invoke("Trascrizione finale (mock)");
    }
}

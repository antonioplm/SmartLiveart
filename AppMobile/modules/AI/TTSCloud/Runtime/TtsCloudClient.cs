public class TtsCloudClient : ITtsProvider
{
    public event System.Action<byte[]> OnAudioChunk;
    public event System.Action<string, float> OnViseme;
    public event System.Action OnCompleted;
    public event System.Action<string> OnError;

    public void RequestTts(string text)
    {
        // Stub: simulazione streaming
        OnAudioChunk?.Invoke(new byte[256]);
        OnViseme?.Invoke("Talk_A", 0.1f);
        OnCompleted?.Invoke();
    }
}

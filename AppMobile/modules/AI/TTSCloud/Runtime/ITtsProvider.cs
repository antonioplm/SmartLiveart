public interface ITtsProvider
{
    /// <summary>
    /// Richiede audio TTS per un testo.
    /// </summary>
    void RequestTts(string text);

    /// <summary>
    /// Evento per chunk audio (streaming).
    /// </summary>
    event System.Action<byte[]> OnAudioChunk;

    /// <summary>
    /// Evento per visemi (se disponibili).
    /// </summary>
    event System.Action<string, float> OnViseme;

    /// <summary>
    /// Evento per fine streaming.
    /// </summary>
    event System.Action OnCompleted;

    /// <summary>
    /// Evento per errori TTS.
    /// </summary>
    event System.Action<string> OnError;
}

public interface ISttProvider
{
    /// <summary>
    /// Invia audio PCM al backend STT.
    /// </summary>
    void SendAudio(float[] pcmData, int sampleRate);

    /// <summary>
    /// Evento per testo parziale.
    /// </summary>
    event System.Action<string> OnPartialResult;

    /// <summary>
    /// Evento per testo finale.
    /// </summary>
    event System.Action<string> OnFinalResult;

    /// <summary>
    /// Evento per errori STT.
    /// </summary>
    event System.Action<string> OnError;
}

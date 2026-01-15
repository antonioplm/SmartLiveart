public interface IAudioCapture
{
    bool IsRecording { get; }

    /// <summary>
    /// Avvia la cattura audio dal microfono.
    /// </summary>
    void StartCapture();

    /// <summary>
    /// Ferma la cattura audio.
    /// </summary>
    void StopCapture();

    /// <summary>
    /// Restituisce gli ultimi campioni PCM catturati.
    /// </summary>
    float[] GetLatestSamples();

    /// <summary>
    /// Restituisce il sample rate corrente.
    /// </summary>
    int GetSampleRate();
}

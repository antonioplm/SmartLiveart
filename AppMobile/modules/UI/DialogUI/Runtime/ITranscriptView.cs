public interface ITranscriptView
{
    /// <summary>
    /// Mostra testo parziale.
    /// </summary>
    void ShowPartial(string text);

    /// <summary>
    /// Mostra testo finale.
    /// </summary>
    void ShowFinal(string text);

    /// <summary>
    /// Pulisce la trascrizione.
    /// </summary>
    void Clear();
}

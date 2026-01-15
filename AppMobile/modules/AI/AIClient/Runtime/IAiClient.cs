public interface IAiClient
{
    /// <summary>
    /// Invia un messaggio testuale al backend AI.
    /// </summary>
    void SendMessage(string text);

    /// <summary>
    /// Evento per token/JSON parziali.
    /// </summary>
    event System.Action<string> OnPartialResponse;

    /// <summary>
    /// Evento per risposta finale.
    /// </summary>
    event System.Action<string> OnFinalResponse;

    /// <summary>
    /// Evento per errori AI.
    /// </summary>
    event System.Action<string> OnError;
}

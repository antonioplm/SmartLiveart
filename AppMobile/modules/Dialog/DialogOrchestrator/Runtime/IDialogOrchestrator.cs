public interface IDialogOrchestrator
{
    /// <summary>
    /// Avvia un turno di ascolto (STT).
    /// </summary>
    void StartListening();

    /// <summary>
    /// Ferma l'ascolto.
    /// </summary>
    void StopListening();

    /// <summary>
    /// Avvia la pipeline completa: STT → AI → TTS → Lipsync.
    /// </summary>
    void ProcessUserInput(string text);

    /// <summary>
    /// Evento per aggiornare la UI.
    /// </summary>
    event System.Action<string> OnStateChanged;
}

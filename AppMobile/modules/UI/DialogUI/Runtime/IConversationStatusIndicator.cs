public interface IConversationStatusIndicator
{
    /// <summary>
    /// Aggiorna lo stato della pipeline (Listening, Thinking, Speaking).
    /// </summary>
    void SetStatus(string status);
}

public class AiClient : IAiClient
{
    public event System.Action<string> OnPartialResponse;
    public event System.Action<string> OnFinalResponse;
    public event System.Action<string> OnError;

    public void SendMessage(string text)
    {
        // Stub: invio al backend
        OnPartialResponse?.Invoke("Risposta parziale (mock)");
        OnFinalResponse?.Invoke("Risposta finale (mock)");
    }
}

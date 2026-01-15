public class DialogOrchestrator : IDialogOrchestrator
{
    public event System.Action<string> OnStateChanged;

    private IAudioCapture audioCapture;
    private ISttProvider stt;
    private IAiClient ai;
    private ITtsProvider tts;
    private IAudioPlayback playback;

    public void StartListening()
    {
        OnStateChanged?.Invoke("Listening");
        audioCapture?.StartCapture();
    }

    public void StopListening()
    {
        audioCapture?.StopCapture();
        OnStateChanged?.Invoke("Processing");
    }

    public void ProcessUserInput(string text)
    {
        OnStateChanged?.Invoke("Thinking");
        ai.SendMessage(text);
    }
}

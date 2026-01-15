using UnityEngine;

public class TranscriptView : MonoBehaviour, ITranscriptView
{
    public void ShowPartial(string text)
    {
        Debug.Log("Partial: " + text);
    }

    public void ShowFinal(string text)
    {
        Debug.Log("Final: " + text);
    }

    public void Clear()
    {
        Debug.Log("Transcript cleared");
    }
}

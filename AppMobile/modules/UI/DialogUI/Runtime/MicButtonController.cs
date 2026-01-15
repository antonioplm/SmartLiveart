using UnityEngine;

public class MicButtonController : MonoBehaviour, IMicButton
{
    public event System.Action OnMicPressed;

    public void Press()
    {
        OnMicPressed?.Invoke();
    }

    public void SetListening(bool listening)
    {
        Debug.Log("MicButton: listening = " + listening);
    }
}

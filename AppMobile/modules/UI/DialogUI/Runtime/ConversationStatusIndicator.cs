using UnityEngine;

public class ConversationStatusIndicator : MonoBehaviour, IConversationStatusIndicator
{
    public void SetStatus(string status)
    {
        Debug.Log("Status: " + status);
    }
}

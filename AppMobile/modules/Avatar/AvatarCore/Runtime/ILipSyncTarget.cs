using UnityEngine;

public interface ILipSyncTarget
{
    string CurrentViseme { get; }
    void SetViseme(string viseme, float duration);
    void SetJaw(float openness);
}

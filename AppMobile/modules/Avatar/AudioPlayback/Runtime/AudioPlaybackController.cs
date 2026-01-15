using UnityEngine;

public class AudioPlaybackController : MonoBehaviour, IAudioPlayback
{
    public bool IsPlaying => audioSource != null && audioSource.isPlaying;

    public event System.Action OnPlaybackFinished;

    private AudioSource audioSource;

    void Awake()
    {
        audioSource = gameObject.AddComponent<AudioSource>();
        audioSource.playOnAwake = false;
    }

    public void Play(AudioClip clip)
    {
        if (clip == null) return;

        audioSource.clip = clip;
        audioSource.Play();

        StartCoroutine(WaitForEnd());
    }

    public void PlayStream(byte[] audioChunk)
    {
        // Stub: implementazione futura
        Debug.Log("PlayStream: chunk ricevuto (" + audioChunk.Length + " bytes)");
    }

    public void Stop()
    {
        audioSource.Stop();
    }

    private System.Collections.IEnumerator WaitForEnd()
    {
        while (audioSource.isPlaying)
            yield return null;

        OnPlaybackFinished?.Invoke();
    }
}

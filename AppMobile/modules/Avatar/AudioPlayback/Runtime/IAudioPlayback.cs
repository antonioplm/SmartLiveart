using UnityEngine;

public interface IAudioPlayback
{
    bool IsPlaying { get; }

    /// <summary>
    /// Riproduce un AudioClip completo.
    /// </summary>
    void Play(AudioClip clip);

    /// <summary>
    /// Riproduce audio in streaming (chunk → AudioClip).
    /// </summary>
    void PlayStream(byte[] audioChunk);

    /// <summary>
    /// Ferma la riproduzione.
    /// </summary>
    void Stop();

    /// <summary>
    /// Evento invocato quando la riproduzione termina.
    /// </summary>
    event System.Action OnPlaybackFinished;
}

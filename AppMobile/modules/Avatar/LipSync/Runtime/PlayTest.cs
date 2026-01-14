using UnityEngine;

public class PlayTest : MonoBehaviour
{
    public AudioSource audioSource;

    private void Update()
    {
        if (Input.GetKeyDown(KeyCode.A))
            audioSource.Play();

        if (Input.GetKeyDown(KeyCode.T))
            LipSyncTextSimulator.Instance.SimulaTesto(LipSyncTextSimulator.Instance.testo);
    }
}

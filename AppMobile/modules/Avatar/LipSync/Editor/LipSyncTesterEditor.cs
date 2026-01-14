using UnityEngine;
using UnityEditor;

[CustomEditor(typeof(LipSyncTextSimulator))]
public class LipSyncTesterEditor : Editor
{
    private LipSyncDriverFFT fft;

    private void OnEnable()
    {
        // Trova il driver FFT nella scena (se presente)
        fft = FindAnyObjectByType<LipSyncDriverFFT>();
    }

    public override void OnInspectorGUI()
    {
        DrawDefaultInspector();

        EditorGUILayout.Space();
        EditorGUILayout.LabelField("🎤 LipSync Tester", EditorStyles.boldLabel);

        LipSyncTextSimulator sim = (LipSyncTextSimulator)target;

        // --- Test Testo ---
        EditorGUILayout.Space();
        EditorGUILayout.LabelField("💬 Test da Testo", EditorStyles.boldLabel);

        if (GUILayout.Button("Simula Testo"))
            sim.SimulaTesto(sim.testo);

        if (GUILayout.Button("TTS + LipSync"))
            _ = sim.RiproduciTTSESeguiVisemi(sim.testo);

        // --- Test Microfono ---
        EditorGUILayout.Space();
        EditorGUILayout.LabelField("🎙 Test Microfono (FFT)", EditorStyles.boldLabel);

        if (fft == null)
        {
            EditorGUILayout.HelpBox("Nessun LipSyncDriverFFT trovato nella scena.", MessageType.Info);
        }
        else
        {
            if (GUILayout.Button("Avvia Microfono"))
                fft.StartMicrophone();

            if (GUILayout.Button("Ferma Microfono"))
                fft.StopMicrophone();
        }

        // --- Test Audio Clip ---
        EditorGUILayout.Space();
        EditorGUILayout.LabelField("🔊 Test Audio Clip", EditorStyles.boldLabel);

        if (sim.audioSource != null && sim.audioSource.clip != null)
        {
            if (GUILayout.Button("Riproduci Audio + LipSync"))
            {
                sim.audioSource.Play();
                sim.SimulaTesto(sim.testo); // o FFT se vuoi
            }
        }
        else
        {
            EditorGUILayout.HelpBox("Nessun AudioClip assegnato all'AudioSource.", MessageType.Info);
        }
    }
}

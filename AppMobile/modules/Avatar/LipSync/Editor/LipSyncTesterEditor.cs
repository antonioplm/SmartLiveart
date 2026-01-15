using UnityEngine;
using UnityEditor;

[CustomEditor(typeof(LipSyncTextSimulator))]
public class LipSyncTesterEditor : Editor
{
    private LipSyncDriverFFT fft;

    private void OnEnable()
    {
        fft = FindAnyObjectByType<LipSyncDriverFFT>();
    }

    public override void OnInspectorGUI()
    {
        DrawDefaultInspector();

        EditorGUILayout.Space();
        EditorGUILayout.LabelField("🎤 LipSync Tester", EditorStyles.boldLabel);

        LipSyncTextSimulator sim = (LipSyncTextSimulator)target;

        // ============================
        // TEST DA TESTO
        // ============================
        EditorGUILayout.Space();
        EditorGUILayout.BeginVertical("box");
        EditorGUILayout.LabelField("💬 Test da Testo", EditorStyles.boldLabel);

        if (GUILayout.Button("Simula Testo"))
            sim.SimulaTesto(sim.testo);

        if (GUILayout.Button("TTS + LipSync"))
            _ = sim.RiproduciTTSESeguiVisemi(sim.testo);

        EditorGUILayout.EndVertical();

        // ============================
        // MICROFONO (FFT)
        // ============================
        EditorGUILayout.Space();
        EditorGUILayout.BeginVertical("box");
        EditorGUILayout.LabelField("🎙 Test Microfono (FFT)", EditorStyles.boldLabel);

        if (fft == null)
        {
            EditorGUILayout.HelpBox("Nessun LipSyncDriverFFT trovato nella scena.", MessageType.Warning);
        }
        else
        {
            // --- Selettore Microfono ---
            string[] devices = Microphone.devices;

            if (devices.Length == 0)
            {
                EditorGUILayout.HelpBox("Nessun microfono rilevato.", MessageType.Warning);
            }
            else
            {
                int currentIndex = Mathf.Max(0, System.Array.IndexOf(devices, fft.microphoneDevice));
                int newIndex = EditorGUILayout.Popup("Device", currentIndex, devices);

                if (newIndex != currentIndex)
                {
                    Undo.RecordObject(fft, "Change Microphone Device");
                    fft.microphoneDevice = devices[newIndex];
                    EditorUtility.SetDirty(fft);
                }
            }

            EditorGUILayout.Space();

            // --- Pulsanti Microfono ---
            if (GUILayout.Button("Avvia Microfono"))
                fft.StartMicrophone();

            if (GUILayout.Button("Ferma Microfono"))
                fft.StopMicrophone();

            // --- Stato Microfono ---
            if (fft.audioSource != null && fft.audioSource.clip != null)
            {
                int pos = Microphone.GetPosition(fft.microphoneDevice);
                EditorGUILayout.LabelField("Posizione buffer:", pos.ToString());
            }
        }

        EditorGUILayout.EndVertical();

        // ============================
        // TEST AUDIO CLIP
        // ============================
        EditorGUILayout.Space();
        EditorGUILayout.BeginVertical("box");
        EditorGUILayout.LabelField("🔊 Test Audio Clip", EditorStyles.boldLabel);

        if (sim.audioSource != null && sim.audioSource.clip != null)
        {
            if (GUILayout.Button("Riproduci Audio + LipSync"))
            {
                sim.audioSource.Play();
                sim.SimulaTesto(sim.testo);
            }
        }
        else
        {
            EditorGUILayout.HelpBox("Nessun AudioClip assegnato all'AudioSource.", MessageType.Info);
        }

        EditorGUILayout.EndVertical();
    }
}

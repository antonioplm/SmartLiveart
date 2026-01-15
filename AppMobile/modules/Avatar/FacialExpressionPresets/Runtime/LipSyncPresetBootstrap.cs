using UnityEngine;
using FacialExpressionPresets;   // vede l'adapter
using LipSync;                   // vede il target

public class LipSyncPresetBootstrap : MonoBehaviour
{
    void Start()
    {
        // Trova l'adapter
        var adapter = GetComponent<VisemePresetAdapter>();
        if (adapter == null)
        {
            Debug.LogWarning("LipSyncPresetBootstrap: Nessun VisemePresetAdapter trovato.");
            return;
        }

        // Costruisce la tabella dei visemi dal preset
        var table = adapter.BuildVisemeTable();
        if (table == null || table.Count == 0)
        {
            Debug.LogWarning("LipSyncPresetBootstrap: Nessun visema trovato nel preset.");
            return;
        }

        // Trova il target lipsync
        var target = GetComponent<LipSyncBlendshapeTarget>();
        if (target == null)
        {
            Debug.LogWarning("LipSyncPresetBootstrap: Nessun LipSyncBlendshapeTarget trovato.");
            return;
        }

        // Inietta la tabella
        target.InjectVisemeTable(table);

        Debug.Log($"LipSyncPresetBootstrap: Iniettati {table.Count} visemi nel target lipsync.");
    }
}
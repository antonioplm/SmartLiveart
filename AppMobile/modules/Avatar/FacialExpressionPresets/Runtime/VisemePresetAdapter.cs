using UnityEngine;
using System.Collections.Generic;

namespace FacialExpressionPresets
{
    public class VisemePresetAdapter : MonoBehaviour
    {
        public ExpressionPresets presetSource;

        public Dictionary<string, List<(string arkit, float weight)>> BuildVisemeTable()
        {
            var table = new Dictionary<string, List<(string, float)>>();

            if (presetSource == null)
            {
                Debug.LogWarning("Nessun ExpressionPresets assegnato al VisemePresetAdapter.");
                return table;
            }

            foreach (var expr in presetSource.expressions)
            {
                if (!expr.name.StartsWith("Talk_"))
                    continue;

                var list = new List<(string, float)>();

                foreach (var blend in expr.blendValues)
                    list.Add((blend.arkitName, blend.weight));

                table[expr.name] = list;
            }

            Debug.Log($"Caricati {table.Count} visemi dal preset.");
            return table;
        }
    }
}
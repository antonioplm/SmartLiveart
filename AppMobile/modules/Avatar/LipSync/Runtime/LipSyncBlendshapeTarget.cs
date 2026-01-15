using UnityEngine;
using System.Collections.Generic;
using AvatarCore;

namespace LipSync
{
    public class LipSyncBlendshapeTarget : MonoBehaviour, ILipSyncTarget
    {
        [Header("Mesh Targets")]
        public SkinnedMeshRenderer faceMesh;
        public List<SkinnedMeshRenderer> extraMeshes;

        [Header("Jaw Settings")]
        [Range(0f, 1f)] public float jawOpenLimit = 0.6f;

        private Dictionary<string, int> faceBlendshapeIndex = new();
        private Dictionary<string, int>[] extraBlendshapeIndex;

        private Dictionary<string, List<(string arkit, float weight)>> visemeTable;
        private string currentViseme = "Neutral";

        void Start()
        {
            CacheBlendshapeIndices();
        }

        public void InjectVisemeTable(Dictionary<string, List<(string, float)>> table)
        {
            visemeTable = table;
        }

        private void CacheBlendshapeIndices()
        {
            if (faceMesh != null)
            {
                var mesh = faceMesh.sharedMesh;
                for (int i = 0; i < mesh.blendShapeCount; i++)
                {
                    string name = mesh.GetBlendShapeName(i).ToLower().Replace("_", "");
                    faceBlendshapeIndex[name] = i;
                }
            }

            if (extraMeshes != null)
            {
                extraBlendshapeIndex = new Dictionary<string, int>[extraMeshes.Count];

                for (int m = 0; m < extraMeshes.Count; m++)
                {
                    extraBlendshapeIndex[m] = new Dictionary<string, int>();
                    var mesh = extraMeshes[m].sharedMesh;

                    for (int i = 0; i < mesh.blendShapeCount; i++)
                    {
                        string name = mesh.GetBlendShapeName(i).ToLower().Replace("_", "");
                        extraBlendshapeIndex[m][name] = i;
                    }
                }
            }
        }

        // ---------------------------
        // ILipSyncTarget
        // ---------------------------

        public string CurrentViseme => currentViseme;

        public void SetJaw(float openness)
        {
            float jawValue = Mathf.Clamp01(openness) * jawOpenLimit * 100f;
            ApplyBlendshape("jawOpen", jawValue);
        }

        public void SetViseme(string viseme, float duration)
        {
            currentViseme = viseme;

            if (visemeTable == null || !visemeTable.ContainsKey(viseme))
                return;

            ResetAllVisemeBlendshapes();

            foreach (var (arkit, weight) in visemeTable[viseme])
                ApplyBlendshape(arkit, weight * 100f);
        }

        // ---------------------------
        // Helpers
        // ---------------------------

        private void ResetAllVisemeBlendshapes()
        {
            if (visemeTable == null)
                return;

            foreach (var entry in visemeTable)
                foreach (var (arkit, _) in entry.Value)
                    ApplyBlendshape(arkit, 0f);
        }

        private void ApplyBlendshape(string arkitName, float weight)
        {
            string key = arkitName.ToLower().Replace("_", "");

            if (faceMesh != null && faceBlendshapeIndex.TryGetValue(key, out int idx))
                faceMesh.SetBlendShapeWeight(idx, weight);

            if (extraMeshes != null)
            {
                for (int m = 0; m < extraMeshes.Count; m++)
                {
                    if (extraMeshes[m] == null) continue;

                    if (extraBlendshapeIndex[m].TryGetValue(key, out int eIdx))
                        extraMeshes[m].SetBlendShapeWeight(eIdx, weight);
                }
            }
        }
    }
}

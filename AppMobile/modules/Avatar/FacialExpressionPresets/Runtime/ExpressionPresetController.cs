using System.Collections.Generic;
using UnityEngine;

public class ExpressionPresetController : MonoBehaviour, ILipSyncTarget
{
    [Header("Avatar Settings")]
    public SkinnedMeshRenderer faceMesh;               // mesh principale (es. AvatarHead)
    public List<SkinnedMeshRenderer> extraMeshes;      // mesh aggiuntive (es. denti, lingua)
    public ExpressionPresets presets;            // riferimento al tuo asset JSON importato

    [Header("Dynamic modulation")]
    [Range(0f, 2f)] public float jawOpenScale = 1f; // fattore moltiplicativo dinamico

    [Range(0f, 1f)] 
    public float globalJawLimit = 0.6f; // % dell'apertura massima (MAX = 1.0)


    public string lastExpression = "Neutral";
    public int lastExpressionIndex = 0;

    public static ExpressionPresetController Instance { get; private set; }

    private void Awake()
    {
        // Singleton setup
        if (Instance != null && Instance != this)
        {
            Debug.LogWarning("Multiple ExpressionPresetControllers detected. Destroying duplicate.");
            Destroy(this.gameObject);
            return;
        }

        Instance = this;
    }

    private void OnDestroy()
    {
        if (Instance == this)
            Instance = null;
    }

    private bool initialized = false;

    private void Start()
    {
        if (!initialized)
        {
            ApplyExpression(lastExpression);
            initialized = true;
        }
    }

    bool Settings 
    {
        get
        {
            if (presets == null)
            {
                Debug.LogError("❌ ExpressionPresets asset not assigned.");
                return false;
            }
            if (faceMesh == null)
            {
                Debug.LogError("❌ SkinnedMeshRenderer not assigned.");
                return false;
            }
            return true;
        }
    }

    public void ApplyExpression(string expressionName)
    {
        if (!Settings)
            return;

        // 🔹 trova l'espressione nel file
        var index = presets.expressions.FindIndex(e => e.name == expressionName);
        if (index < 0)
        {
            Debug.LogWarning($"⚠️ Expression '{expressionName}' not found.");
            return;
        }

        var expr = presets.expressions[index];

        // 🔹 Reset di tutti i blendshape su tutte le mesh coinvolte
        ResetAllMeshes();

        // 🔹 Applica i blendshape per ciascun valore definito nell’espressione
        foreach (var blend in expr.blendValues)
        {
            ApplyBlendshapeToAll(blend.arkitName, blend.weight * 100f);
        }

        lastExpression = expressionName;
        lastExpressionIndex = index;

        Debug.Log($"✅ Applied expression: {expressionName}");
    }

    public void SetJawOpenScale(float value)
    {
        jawOpenScale = value;
    }

    public void LerpExpression(string expressionName, float duration)
    {
        StopAllCoroutines();
        StartCoroutine(CrossFadeRoutine(lastExpression, expressionName, duration));
    }

    public void LerpExpression(string fromExpression, string toExpression, float duration)
    {
        StopAllCoroutines();
        StartCoroutine(CrossFadeRoutine(fromExpression, toExpression, duration));
    }

    public void LerpExpression(int fromIndex, int toIndex, float duration)
    {
        StopAllCoroutines();
        StartCoroutine(CrossFadeRoutine(fromIndex, toIndex, duration));
    }

    public void LerpExpression(int toIndex, float duration)
    {
        StopAllCoroutines();
        StartCoroutine(CrossFadeRoutine(lastExpressionIndex, toIndex, duration));
    }

    // 🔹 Interpolazione completa sincronizzata su tutte le mesh
    private System.Collections.IEnumerator CrossFadeRoutine(ExpressionPresets.Expression fromExpr, ExpressionPresets.Expression toExpr, float duration)
    {
        if (!Settings)
            yield break;
        if (toExpr == null)
            yield break;

        var allMeshes = new List<SkinnedMeshRenderer>();
        if (faceMesh != null) allMeshes.Add(faceMesh);
        if (extraMeshes != null) allMeshes.AddRange(extraMeshes);

        // Stato iniziale di tutti i blendshape su tutte le mesh
        Dictionary<SkinnedMeshRenderer, float[]> startWeights = new();

        foreach (var smr in allMeshes)
        {
            var mesh = smr.sharedMesh;
            float[] weights = new float[mesh.blendShapeCount];
            for (int i = 0; i < mesh.blendShapeCount; i++)
                weights[i] = smr.GetBlendShapeWeight(i);
            startWeights[smr] = weights;
        }

        // Costruisci tabelle pesi da/verso
        var fromWeights = BuildWeightsMap(fromExpr, allMeshes);
        var toWeights = BuildWeightsMap(toExpr, allMeshes);

        // Interpolazione
        float t = 0f;
        while (t < 1f)
        {
            foreach (var smr in allMeshes)
            {
                var mesh = smr.sharedMesh;
                for (int i = 0; i < mesh.blendShapeCount; i++)
                {
                    string name = mesh.GetBlendShapeName(i).ToLower().Replace("_", "");
                    float fromVal = fromWeights.ContainsKey((smr, name)) ? fromWeights[(smr, name)] : 0f;
                    float toVal = toWeights.ContainsKey((smr, name)) ? toWeights[(smr, name)] : 0f;
                    float blended = Mathf.Lerp(fromVal, toVal, t);
                    // 🔹 Applica la limitazione jawOpen anche durante il lerp
                    if (name.Contains("jawopen"))
                        blended *= jawOpenScale * globalJawLimit;

                    smr.SetBlendShapeWeight(i, blended);
                }
            }

            t += Time.deltaTime / duration;
            yield return null;
        }

        // Imposta i valori finali
        foreach (var smr in allMeshes)
        {
            var mesh = smr.sharedMesh;
            for (int i = 0; i < mesh.blendShapeCount; i++)
            {
                string name = mesh.GetBlendShapeName(i).ToLower().Replace("_", "");
                float toVal = toWeights.ContainsKey((smr, name)) ? toWeights[(smr, name)] : 0f;
                float finalVal = toVal;
                if (name.Contains("jawopen"))
                {
                    finalVal *= jawOpenScale * globalJawLimit;
                }
                smr.SetBlendShapeWeight(i, finalVal);
            }
        }

        lastExpression = toExpr.name;
        lastExpressionIndex = presets.expressions.FindIndex(e => e == toExpr);

        Debug.Log($"✅ Crossfaded from '{fromExpr?.name ?? "Neutral"}' to '{toExpr.name}'");
    }

    private System.Collections.IEnumerator CrossFadeRoutine(string fromExpression, string toExpression, float duration)
    {
        if (!Settings)
            yield break;

        var fromExpr = presets.expressions.Find(e => e.name == fromExpression);
        var toExpr = presets.expressions.Find(e => e.name == toExpression);

        if (toExpr == null)
        {
            Debug.LogWarning($"⚠️ Target expression '{toExpression}' not found.");
            yield break;
        }

        yield return StartCoroutine(CrossFadeRoutine(fromExpr, toExpr, duration));
    }

    private System.Collections.IEnumerator CrossFadeRoutine(int fromIndex, int toIndex, float duration)
    {
        if (!Settings)
            yield break;

        fromIndex = Mathf.Clamp(fromIndex, 0, presets.expressions.Count - 1);
        toIndex = Mathf.Clamp(toIndex, 0, presets.expressions.Count - 1);

        yield return StartCoroutine(CrossFadeRoutine(presets.expressions[fromIndex], presets.expressions[toIndex], duration));
    }

    private Dictionary<(SkinnedMeshRenderer, string), float> BuildWeightsMap(ExpressionPresets.Expression expr, List<SkinnedMeshRenderer> meshes)
    {
        var map = new Dictionary<(SkinnedMeshRenderer, string), float>();
        if (expr == null) return map;

        foreach (var blend in expr.blendValues)
        {
            string targetName = blend.arkitName.ToLower().Replace("_", "");
            foreach (var smr in meshes)
            {
                var mesh = smr.sharedMesh;
                for (int i = 0; i < mesh.blendShapeCount; i++)
                {
                    string bsName = mesh.GetBlendShapeName(i).ToLower().Replace("_", "");
                    if (bsName == targetName)
                    {
                        map[(smr, bsName)] = blend.weight * 100f;
                        break;
                    }
                }
            }
        }

        return map;
    }


    private void ResetAllMeshes()
    {
        // resetta la mesh principale
        if (faceMesh != null)
        {
            for (int i = 0; i < faceMesh.sharedMesh.blendShapeCount; i++)
                faceMesh.SetBlendShapeWeight(i, 0f);
        }

        // resetta eventuali mesh extra (es. denti, lingua)
        if (extraMeshes != null)
        {
            foreach (var mesh in extraMeshes)
            {
                if (mesh == null) continue;
                for (int i = 0; i < mesh.sharedMesh.blendShapeCount; i++)
                    mesh.SetBlendShapeWeight(i, 0f);
            }
        }
    }

    private void ApplyBlendshapeToAll(string arkitName, float weight)
    {
        string targetName = arkitName.ToLower().Replace("_", "");

        void ApplyTo(SkinnedMeshRenderer smr)
        {
            if (smr == null) return;
            var mesh = smr.sharedMesh;
            for (int i = 0; i < mesh.blendShapeCount; i++)
            {
                string bsName = mesh.GetBlendShapeName(i).ToLower().Replace("_", "");
                if (bsName == targetName)
                {
                    float finalWeight = weight;

                    // 🔹 Se è il blendshape "jawOpen", modula dinamicamente in base all’audio
                    if (bsName.Contains("jawopen"))
                        finalWeight *= jawOpenScale * globalJawLimit;

                    smr.SetBlendShapeWeight(i, finalWeight);
                    return;
                }
            }
        }

        // Applica a tutte le mesh coinvolte
        ApplyTo(faceMesh);

        if (extraMeshes != null)
            foreach (var smr in extraMeshes)
                ApplyTo(smr);
    }

    // ---------------------------
    // ILipSyncTarget IMPLEMENTATION
    // ---------------------------

    public string CurrentViseme => lastExpression;

    public void SetJaw(float openness)
    {
        jawOpenScale = openness;
    }

    public void SetViseme(string viseme, float duration)
    {
        if (lastExpression == viseme)
            return;

        LerpExpression(lastExpression, viseme, duration);
    }
}

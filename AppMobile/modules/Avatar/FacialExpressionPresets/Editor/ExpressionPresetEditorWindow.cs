using UnityEngine;
using UnityEditor;
using System.Collections.Generic;
using System.IO;

public class ExpressionPresetEditorWindow : EditorWindow
{
    private ExpressionPresets workingAsset;
    private ExpressionPresetController previewController;
    private Vector2 scroll;

    // ===================== ARKit OFFICIAL BLENDSHAPES =====================
    static readonly string[] ARKitBlendShapes =
    {
        "jawOpen","jawForward","mouthClose","mouthFunnel","mouthPucker",
        "mouthSmileLeft","mouthSmileRight","mouthFrownLeft","mouthFrownRight",
        "mouthPressLeft","mouthPressRight","mouthStretchLeft","mouthStretchRight",
        "cheekPuff","cheekSquintLeft","cheekSquintRight","eyeBlinkLeft","eyeBlinkRight",
        "eyeSquintLeft","eyeSquintRight","eyeWideLeft","eyeWideRight",
        "browDownLeft","browDownRight","browInnerUp","browOuterUpLeft","browOuterUpRight",
        "noseSneerLeft","noseSneerRight"
    };

    // ===================== MENU =====================
    [MenuItem("ARKit/Expression Preset Editor")]
    public static void Open()
    {
        GetWindow<ExpressionPresetEditorWindow>("Expression Presets");
    }

    // ===================== GUI =====================
    private void OnGUI()
    {
        EditorGUILayout.Space();

        workingAsset = (ExpressionPresets)EditorGUILayout.ObjectField(
            "Working Asset",
            workingAsset,
            typeof(ExpressionPresets),
            false);

        previewController = (ExpressionPresetController)EditorGUILayout.ObjectField(
            "Preview Controller",
            previewController,
            typeof(ExpressionPresetController),
            true);

        EditorGUILayout.Space();

        if (workingAsset == null)
        {
            if (GUILayout.Button("➕ Create Empty Preset Asset"))
            {
                workingAsset = ScriptableObject.CreateInstance<ExpressionPresets>();
            }

            if (GUILayout.Button("🧱 Create Default Preset Asset"))
            {
                CreateDefaultAsset();
            }

            return;
        }

        scroll = EditorGUILayout.BeginScrollView(scroll);

        for (int i = 0; i < workingAsset.expressions.Count; i++)
        {
            DrawExpression(workingAsset.expressions[i], i);
        }

        EditorGUILayout.EndScrollView();

        EditorGUILayout.Space();

        if (GUILayout.Button("➕ Add Expression"))
        {
            workingAsset.expressions.Add(new ExpressionPresets.Expression
            {
                name = "NewExpression"
            });
        }

        EditorGUILayout.Space(10);

        EditorGUILayout.BeginHorizontal();

        if (GUILayout.Button("💾 Save JSON"))
            SaveJson();

        if (GUILayout.Button("📦 Create / Update Asset"))
            SaveAsset();

        EditorGUILayout.EndHorizontal();
    }

    // ===================== DRAW EXPRESSION =====================
    private void DrawExpression(ExpressionPresets.Expression expr, int index)
    {
        EditorGUILayout.BeginVertical("box");

        EditorGUILayout.BeginHorizontal();
        expr.name = EditorGUILayout.TextField("Name", expr.name);
        if (GUILayout.Button("✖", GUILayout.Width(30)))
        {
            workingAsset.expressions.RemoveAt(index);
            return;
        }
        EditorGUILayout.EndHorizontal();

        for (int i = 0; i < expr.blendValues.Count; i++)
        {
            EditorGUILayout.BeginHorizontal();

            int currentIndex = System.Array.IndexOf(ARKitBlendShapes, expr.blendValues[i].arkitName);
            if (currentIndex < 0) currentIndex = 0;

            int newIndex = EditorGUILayout.Popup(currentIndex, ARKitBlendShapes);
            expr.blendValues[i].arkitName = ARKitBlendShapes[newIndex];

            // Inizia il controllo delle modifiche
            EditorGUI.BeginChangeCheck();
            float newWeight = EditorGUILayout.Slider(expr.blendValues[i].weight, 0f, 1f);
            if (EditorGUI.EndChangeCheck())
            {
                expr.blendValues[i].weight = newWeight;

                // Aggiorna subito l'avatar in scena
                if (previewController != null)
                {
                    previewController.presets = workingAsset;
                    previewController.ApplyExpression(expr.name);
                    SceneView.RepaintAll();
                }
            }

            if (GUILayout.Button("-", GUILayout.Width(25)))
            {
                expr.blendValues.RemoveAt(i);
                break;
            }

            EditorGUILayout.EndHorizontal();
        }

        EditorGUILayout.BeginHorizontal();
        if (GUILayout.Button("➕ Add BlendShape"))
        {
            expr.blendValues.Add(new ExpressionPresets.BlendValue
            {
                arkitName = "jawOpen",
                weight = 0.5f
            });
        }
        EditorGUILayout.EndHorizontal();

        EditorGUILayout.EndVertical();
    }

    // ===================== CREATE DEFAULT ASSET =====================
    private void CreateDefaultAsset()
    {
        workingAsset = ScriptableObject.CreateInstance<ExpressionPresets>();
        workingAsset.expressions = new List<ExpressionPresets.Expression>();

        void Add(string name, params (string, float)[] values)
        {
            var e = new ExpressionPresets.Expression
            {
                name = name,
                blendValues = new List<ExpressionPresets.BlendValue>()
            };

            foreach (var (arkit, weight) in values)
            {
                e.blendValues.Add(new ExpressionPresets.BlendValue
                {
                    arkitName = arkit,
                    weight = weight
                });
            }

            workingAsset.expressions.Add(e);
        }

        // ===================== EXPRESSIONS =====================
        Add("Neutral");

        Add("Smile",
            ("mouthSmileLeft", 0.9f),
            ("mouthSmileRight", 0.9f),
            ("cheekSquintLeft", 0.4f),
            ("cheekSquintRight", 0.4f),
            ("eyeSquintLeft", 0.3f),
            ("eyeSquintRight", 0.3f)
        );

        Add("Sad",
            ("mouthFrownLeft", 0.8f),
            ("mouthFrownRight", 0.8f),
            ("browDownLeft", 0.7f),
            ("browDownRight", 0.7f),
            ("mouthShrugLower", 0.5f)
        );

        Add("Angry",
            ("browDownLeft", 0.9f),
            ("browDownRight", 0.9f),
            ("noseSneerLeft", 0.5f),
            ("noseSneerRight", 0.5f),
            ("mouthFrownLeft", 0.5f),
            ("mouthFrownRight", 0.5f)
        );

        Add("Surprised",
            ("jawOpen", 1.0f),
            ("mouthFunnel", 0.6f),
            ("eyeWideLeft", 0.8f),
            ("eyeWideRight", 0.8f),
            ("browInnerUp", 0.8f)
        );

        Add("Disgusted",
            ("noseSneerLeft", 0.9f),
            ("noseSneerRight", 0.9f),
            ("mouthFrownLeft", 0.6f),
            ("mouthFrownRight", 0.6f),
            ("browDownLeft", 0.7f),
            ("browDownRight", 0.7f)
        );

        Add("Cheeky",
            ("cheekPuff", 0.6f),
            ("mouthSmileLeft", 0.6f),
            ("mouthSmileRight", 0.6f),
            ("eyeSquintLeft", 0.3f),
            ("eyeSquintRight", 0.3f)
        );

        // ===================== VISEMES =====================
        Add("Talk_A",
            ("jawOpen", 0.35f),
            ("mouthFunnel", 0.2f),
            ("mouthStretchLeft", 0.15f),
            ("mouthStretchRight", 0.15f)
        );

        Add("Talk_E",
            ("jawOpen", 0.3f),
            ("mouthSmileLeft", 0.3f),
            ("mouthSmileRight", 0.3f),
            ("mouthFunnel", 0.2f)
        );

        Add("Talk_I",
            ("jawOpen", 0.25f),
            ("mouthSmileLeft", 0.45f),
            ("mouthSmileRight", 0.45f),
            ("cheekSquintLeft", 0.1f),
            ("cheekSquintRight", 0.1f)
        );

        Add("Talk_O",
            ("jawOpen", 0.3f),
            ("mouthFunnel", 0.5f),
            ("mouthPucker", 0.3f)
        );

        Add("Talk_U",
            ("jawOpen", 0.05f),
            ("mouthPucker", 0.75f),
            ("mouthFunnel", 0.36f)
        );

        Add("Talk_S",
            ("jawOpen", 0.2f),
            ("mouthFunnel", 0.25f),
            ("mouthPressLeft", 0.2f),
            ("mouthPressRight", 0.2f)
        );

        Add("Talk_M",
            ("mouthClose", 0.25f),
            ("jawOpen", 0.05f)
        );

        Add("Talk_P",
            ("mouthClose", 0.22f),
            ("mouthPressLeft", 0.2f),
            ("mouthPressRight", 0.2f),
            ("jawOpen", 0.05f),
            ("cheekSquintLeft", 0.1f),
            ("cheekSquintRight", 0.1f)
        );

        Add("Talk_F",
            ("jawOpen", 0.18f),
            ("mouthClose", 0.25f),
            ("mouthPressLeft", 0.35f),
            ("mouthPressRight", 0.35f),
            ("mouthFunnel", 0.2f),
            ("mouthPucker", 0.15f)
        );

        Add("Talk_T",
            ("jawOpen", 0.22f),
            ("mouthClose", 0.18f),
            ("mouthPressLeft", 0.25f),
            ("mouthPressRight", 0.25f),
            ("cheekSquintLeft", 0.05f),
            ("cheekSquintRight", 0.05f)
        );

        Add("Talk_K",
            ("jawOpen", 0.3f),
            ("mouthFunnel", 0.35f),
            ("mouthPucker", 0.2f),
            ("mouthClose", 0.1f),
            ("cheekSquintLeft", 0.05f),
            ("cheekSquintRight", 0.05f)
        );
    }

    // ===================== JSON =====================
    private void SaveJson()
    {
        string path = EditorUtility.SaveFilePanel(
            "Save Expression Presets JSON",
            Application.dataPath,
            "ExpressionPresets",
            "json");

        if (string.IsNullOrEmpty(path))
            return;

        var wrapper = new ExpressionPresetWrapper
        {
            expressions = workingAsset.expressions
        };

        string json = JsonUtility.ToJson(wrapper, true);
        File.WriteAllText(path, json);

        Debug.Log($"✅ JSON saved: {path}");
    }

    [System.Serializable]
    private class ExpressionPresetWrapper
    {
        public List<ExpressionPresets.Expression> expressions;
    }

    // ===================== ASSET =====================
    private void SaveAsset()
    {
        string path = EditorUtility.SaveFilePanelInProject(
            "Save Expression Presets Asset",
            "AvatarSDK_Expressions",
            "asset",
            "Select location");

        if (string.IsNullOrEmpty(path))
            return;

        var existing = AssetDatabase.LoadAssetAtPath<ExpressionPresets>(path);
        if (existing != null)
        {
            EditorUtility.CopySerialized(workingAsset, existing);
            EditorUtility.SetDirty(existing);
        }
        else
        {
            AssetDatabase.CreateAsset(workingAsset, path);
        }

        AssetDatabase.SaveAssets();
        AssetDatabase.Refresh();

        Debug.Log($"📦 Asset saved: {path}");
    }

}

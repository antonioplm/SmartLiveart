using UnityEditor;
using UnityEngine;
using System.IO;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

public class ModulesBrowser : EditorWindow
{
    private Vector2 scroll;
    private string search = "";
    private Dictionary<string, List<string>> modules = new();
    private Dictionary<string, bool> foldouts = new();

    [MenuItem("Window/Project Modules Browser")]
    public static void Open()
    {
        GetWindow<ModulesBrowser>("Modules Browser");
    }

    void OnEnable()
    {
        RefreshModules();
    }

    void RefreshModules()
    {
        modules.Clear();
        foldouts.Clear();

        string manifestPath = "Packages/manifest.json";
        if (!File.Exists(manifestPath))
        {
            Debug.LogError("manifest.json non trovato.");
            return;
        }

        string json = File.ReadAllText(manifestPath);

        // Trova tutte le dipendenze "file:..."
        var matches = Regex.Matches(json, "\"([^\"]+)\"\\s*:\\s*\"file:([^\"]+)\"");

        foreach (Match m in matches)
        {
            string relativePath = m.Groups[2].Value;

            // Risolve path relativi rispetto alla root del progetto
            string fullPath = Path.GetFullPath(Path.Combine(Application.dataPath, relativePath));

            if (!Directory.Exists(fullPath))
                continue;

            string category = DetectCategory(fullPath);

            if (!modules.ContainsKey(category))
                modules[category] = new List<string>();

            modules[category].Add(fullPath);
            foldouts[category] = false;
        }
    }

    string DetectCategory(string fullPath)
    {
        string parent = Path.GetFileName(Path.GetDirectoryName(fullPath));

        if (parent.Equals("AI")) return "AI";
        if (parent.Equals("Avatar")) return "Avatar";
        if (parent.Equals("Dialog")) return "Dialog";
        if (parent.Equals("UI")) return "UI";
        if (parent.Equals("AR")) return "AR";

        return "Other";
    }

    void OnGUI()
    {
        GUILayout.Label("Project Modules Browser", EditorStyles.boldLabel);

        search = EditorGUILayout.TextField("Search", search);

        if (GUILayout.Button("Refresh"))
            RefreshModules();

        scroll = GUILayout.BeginScrollView(scroll);

        foreach (var category in modules.Keys)
        {
            foldouts[category] = EditorGUILayout.Foldout(foldouts[category], category, true);

            if (foldouts[category])
            {
                foreach (var modulePath in modules[category])
                    DrawModule(modulePath);

                GUILayout.Space(10);
            }
        }

        GUILayout.EndScrollView();
    }

    void DrawModule(string modulePath)
    {
        GUILayout.BeginVertical("box");
        GUILayout.Label(Path.GetFileName(modulePath), EditorStyles.boldLabel);

        // Pulsanti utili
        GUILayout.BeginHorizontal();
        if (GUILayout.Button("Apri cartella"))
            EditorUtility.RevealInFinder(modulePath);

        string packageJson = Path.Combine(modulePath, "package.json");
        if (File.Exists(packageJson) && GUILayout.Button("package.json"))
            UnityEditorInternal.InternalEditorUtility.OpenFileAtLineExternal(packageJson, 1);

        string readme = Directory.GetFiles(modulePath, "README.md", SearchOption.AllDirectories).FirstOrDefault();
        if (readme != null && GUILayout.Button("README"))
            UnityEditorInternal.InternalEditorUtility.OpenFileAtLineExternal(readme, 1);

        GUILayout.EndHorizontal();

        DrawModuleScripts(modulePath);

        GUILayout.EndVertical();
    }

    void DrawModuleScripts(string modulePath)
    {
        var scripts = Directory.GetFiles(modulePath, "*.cs", SearchOption.AllDirectories)
                               .Where(f => f.ToLower().Contains(search.ToLower()));

        foreach (var script in scripts)
        {
            if (GUILayout.Button(Path.GetFileName(script)))
            {
                // Apre direttamente nell'IDE (funziona anche fuori da Assets/ e Packages/)
                UnityEditorInternal.InternalEditorUtility.OpenFileAtLineExternal(script, 1);
            }
        }
    }
}

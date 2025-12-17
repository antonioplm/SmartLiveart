using UnityEditor;
using UnityEngine;

[CustomEditor(typeof(ExpressionPresetController))]
public class ExpressionPresetControllerEditor : Editor
{
    public override void OnInspectorGUI()
    {
        DrawDefaultInspector();

        ExpressionPresetController ctrl = (ExpressionPresetController)target;

        if (ctrl.presets != null)
        {
            EditorGUILayout.Space();
            EditorGUILayout.LabelField("Apply Preset:", EditorStyles.boldLabel);

            foreach (var expr in ctrl.presets.expressions)
            {
                if (GUILayout.Button(expr.name))
                    ctrl.ApplyExpression(expr.name);
            }
        }
    }
}

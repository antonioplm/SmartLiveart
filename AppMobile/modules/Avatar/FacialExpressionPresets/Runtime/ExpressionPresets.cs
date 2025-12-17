using UnityEngine;
using System.Collections.Generic;

[CreateAssetMenu(fileName = "ExpressionPresets", menuName = "ARKit/Expression Presets", order = 2)]
public class ExpressionPresets : ScriptableObject
{
    [System.Serializable]
    public class Expression
    {
        public string name;
        public List<BlendValue> blendValues = new List<BlendValue>();
    }

    [System.Serializable]
    public class BlendValue
    {
        public string arkitName;
        [Range(0f, 1f)]
        public float weight;
    }

    public List<Expression> expressions = new List<Expression>();

    public Expression GetExpression(string name)
    {
        return expressions.Find(e => e.name == name);
    }
}

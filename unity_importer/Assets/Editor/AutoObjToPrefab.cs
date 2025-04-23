using UnityEditor;
using UnityEngine;
using System.IO;

public class AutoObjToPrefab : AssetPostprocessor
{
    static void OnPostprocessAllAssets(string[] importedAssets, string[] _, string[] __, string[] ___)
    {
        foreach (string assetPath in importedAssets)
        {
            if (assetPath.EndsWith(".obj") && assetPath.Contains("Resources/Models"))
            {
                Debug.Log("🛠 检测到新 .obj 模型: " + assetPath);

                GameObject obj = AssetDatabase.LoadAssetAtPath<GameObject>(assetPath);
                if (obj == null)
                {
                    Debug.LogWarning("❌ 无法加载 .obj 对象: " + assetPath);
                    continue;
                }

                string fileName = Path.GetFileNameWithoutExtension(assetPath);
                string prefabPath = $"Assets/Resources/Models/{fileName}.prefab";

                GameObject prefab = PrefabUtility.SaveAsPrefabAsset(obj, prefabPath);
                Debug.Log("✅ 已自动生成 prefab: " + prefabPath);

                // 自动加载进场景
                GameObject instance = PrefabUtility.InstantiatePrefab(prefab) as GameObject;
                instance.name = "ImportedModel";
                instance.transform.position = Vector3.zero;
                Debug.Log("🟢 模型已自动加载到场景: " + fileName);
            }
            if (assetPath.EndsWith(".ply") && assetPath.Contains("Resources/Models"))
            {
                string fileName = Path.GetFileNameWithoutExtension(assetPath);
                string prefabPath = $"Assets/Resources/Models/{fileName}.prefab";

                string content = File.ReadAllText(assetPath);
                GameObject go = PlyImporter.Import(content);
                go.name = "ImportedModel";

                GameObject prefab = PrefabUtility.SaveAsPrefabAsset(go, prefabPath);
                Debug.Log("✅ 已生成 prefab: " + prefabPath);

                GameObject instance = PrefabUtility.InstantiatePrefab(prefab) as GameObject;
                instance.name = "ImportedModel";
                instance.transform.position = Vector3.zero;
                Debug.Log("🟢 模型已自动加载到场景: " + fileName);
            }
        }
    }
}

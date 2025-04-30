
using UnityEngine;
using System.IO;

public class MeshAutoLoader : MonoBehaviour
{
    public string objPath = "Assets/NeRFPlugin/Outputs/output.obj";

    void Start()
    {
        if (File.Exists(objPath))
        {
            Mesh mesh = ObjImporter.ImportFile(objPath);
            if (mesh != null)
            {
                GameObject go = new GameObject("LoadedNeRFMesh");
                go.AddComponent<MeshFilter>().mesh = mesh;
                go.AddComponent<MeshRenderer>().material = new Material(Shader.Find("Standard"));
                Debug.Log("✅ NeRF 模型已加载！");
            }
        }
        else
        {
            Debug.LogWarning("❌ output.obj 未找到！");
        }
    }
}

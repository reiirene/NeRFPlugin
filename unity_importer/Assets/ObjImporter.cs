using UnityEngine;

public class ObjImporter : MonoBehaviour
{
    public string modelName = "cube"; // 不用加 .obj 后缀

    void Start()
    {
        GameObject prefab = Resources.Load<GameObject>("Models/" + modelName);
        if (prefab != null)
        {
            GameObject go = Instantiate(prefab, Vector3.zero, Quaternion.identity);
            go.name = "ImportedModel";
            Debug.Log("模型自动加载并实例化完成: " + modelName);
        }
        else
        {
            Debug.LogWarning("找不到 Resources/Models/" + modelName + "，请确认是否设置为可加载");
        }
    }
}
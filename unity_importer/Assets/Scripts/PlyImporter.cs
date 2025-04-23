using UnityEngine;
using System.Collections.Generic;
using System.IO;
using System.Globalization;
using System;

public static class PlyImporter
{
    public static GameObject Import(string plyText)
    {
        StringReader reader = new StringReader(plyText);
        string line;

        int vertexCount = 0;
        int faceCount = 0;
        List<Vector3> vertices = new List<Vector3>();
        List<int> triangles = new List<int>();

        // 解析 header
        while ((line = reader.ReadLine()) != null)
        {
            line = line.Trim();
            if (line.StartsWith("element vertex"))
                int.TryParse(line.Split(' ')[2], out vertexCount);
            else if (line.StartsWith("element face"))
                int.TryParse(line.Split(' ')[2], out faceCount);
            else if (line.StartsWith("end_header"))
                break;
        }

        // 解析顶点
        for (int i = 0; i < vertexCount; i++)
        {
            line = reader.ReadLine()?.Trim();
            if (string.IsNullOrWhiteSpace(line))
            {
                Debug.LogWarning($"[PlyImporter] 顶点第 {i} 行为空，跳过");
                continue;
            }

            string[] parts = line.Split(new[] { ' ', '\t' }, StringSplitOptions.RemoveEmptyEntries);
            if (parts.Length < 3)
            {
                Debug.LogWarning($"[PlyImporter] 顶点数据不足: {line}");
                continue;
            }

            try
            {
                float x = float.Parse(parts[0], CultureInfo.InvariantCulture);
                float y = float.Parse(parts[1], CultureInfo.InvariantCulture);
                float z = float.Parse(parts[2], CultureInfo.InvariantCulture);
                vertices.Add(new Vector3(x, y, z));
            }
            catch (Exception e)
            {
                Debug.LogError($"[PlyImporter] 顶点解析失败: 行 = '{line}' 错误 = {e.Message}");
            }
        }

        // 解析面（三角形）
        for (int i = 0; i < faceCount; i++)
        {
            line = reader.ReadLine()?.Trim();
            if (string.IsNullOrWhiteSpace(line)) continue;

            string[] parts = line.Split(new[] { ' ', '\t' }, StringSplitOptions.RemoveEmptyEntries);
            if (parts.Length < 4) continue;

            if (int.TryParse(parts[0], out int count) && count == 3)
            {
                if (int.TryParse(parts[1], out int a) &&
                    int.TryParse(parts[2], out int b) &&
                    int.TryParse(parts[3], out int c))
                {
                    triangles.Add(a);
                    triangles.Add(b);
                    triangles.Add(c);
                }
            }
        }

        // 检查有效性
        if (vertices.Count == 0 || triangles.Count == 0)
        {
            Debug.LogError("[PlyImporter] 导入失败：顶点或面数据为空");
            return null;
        }

        // 创建 Mesh 并返回
        Mesh mesh = new Mesh();
        mesh.SetVertices(vertices);
        mesh.SetTriangles(triangles, 0);
        mesh.RecalculateNormals();

        GameObject go = new GameObject("ImportedPLY");
        go.AddComponent<MeshFilter>().mesh = mesh;
        go.AddComponent<MeshRenderer>().material = new Material(Shader.Find("Standard"));

        return go;
    }
}

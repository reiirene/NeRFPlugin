
using System.Collections.Generic;
using UnityEngine;
using System.IO;

public static class ObjImporter
{
    public static Mesh ImportFile(string filePath)
    {
        if (!File.Exists(filePath)) return null;

        List<Vector3> vertices = new List<Vector3>();
        List<int> triangles = new List<int>();

        foreach (var line in File.ReadLines(filePath))
        {
            if (line.StartsWith("v "))
            {
                var parts = line.Split(' ');
                vertices.Add(new Vector3(
                    float.Parse(parts[1]),
                    float.Parse(parts[2]),
                    float.Parse(parts[3])
                ));
            }
            else if (line.StartsWith("f "))
            {
                var parts = line.Split(' ');
                triangles.Add(int.Parse(parts[1]) - 1);
                triangles.Add(int.Parse(parts[2]) - 1);
                triangles.Add(int.Parse(parts[3]) - 1);
            }
        }

        Mesh mesh = new Mesh();
        mesh.SetVertices(vertices);
        mesh.SetTriangles(triangles, 0);
        mesh.RecalculateNormals();
        return mesh;
    }
}

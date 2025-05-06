using System.IO;
using UnityEngine;

/// <summary>
/// Loads a raw volumetric float32 density grid exported from Instant-NGP
/// and converts it into a Texture3D for volume rendering in Unity.
/// </summary>
public class VolumeLoader : MonoBehaviour
{
    [Header("Volume File Settings")]
    public string volumePath = "Assets/NeRFPlugin/Outputs/density_grid.vol";
    public int resolution = 256;

    [Header("Texture3D Output")]
    public Texture3D volumeTexture;

    void Start()
    {
        volumeTexture = LoadVolume();
        if (volumeTexture != null)
        {
            Debug.Log($"[VolumeLoader] Loaded 3D volume texture ({resolution}³) from {volumePath}");
        }
        else
        {
            Debug.LogError("[VolumeLoader] Failed to load volume texture.");
        }
    }

    public Texture3D LoadVolume()
    {
        int voxelCount = resolution * resolution * resolution;

        if (!File.Exists(volumePath))
        {
            Debug.LogError($"[VolumeLoader] Volume file not found: {volumePath}");
            return null;
        }

        float[] floatData = new float[voxelCount];

        try
        {
            using (FileStream fs = new FileStream(volumePath, FileMode.Open, FileAccess.Read))
            using (BinaryReader reader = new BinaryReader(fs))
            {
                for (int i = 0; i < voxelCount; i++)
                {
                    floatData[i] = reader.ReadSingle(); // Read float32
                }
            }
        }
        catch (System.Exception e)
        {
            Debug.LogError($"[VolumeLoader] Failed to read volume file: {e.Message}");
            return null;
        }

        Color[] colors = new Color[voxelCount];
        for (int i = 0; i < voxelCount; i++)
        {
            float v = Mathf.Clamp01(floatData[i]); // Optional: normalize
            colors[i] = new Color(v, v, v, 1f);     // Greyscale encoding
        }

        Texture3D texture = new Texture3D(resolution, resolution, resolution, TextureFormat.RFloat, false);
        texture.wrapMode = TextureWrapMode.Clamp;
        texture.SetPixels(colors);
        texture.Apply();

        return texture;
    }
}

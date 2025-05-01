using UnityEditor;
using UnityEngine;
using System.IO;

[InitializeOnLoad]
public static class NerfPluginInstaller
{
    static NerfPluginInstaller()
    {
        string editorScriptPath = GetInstallerScriptPath();
        string pluginRoot = Path.GetFullPath(Path.Combine(editorScriptPath, "..", ".."));

        string unityDestRoot = Path.Combine(Application.dataPath, "NeRFPlugin", "Scripts");
        string topLevelDestRoot = Path.Combine(Directory.GetParent(Application.dataPath).FullName, "NeRFPlugin");

        // Skip copy if already in Assets/NeRFPlugin
        string expectedPluginPath = Path.Combine(Application.dataPath, "NeRFPlugin").Replace("\\", "/");
        if (pluginRoot.Replace("\\", "/") == expectedPluginPath)
        {
            Debug.Log("NerfPluginInstaller: Plugin is already installed in Assets/NeRFPlugin — skipping copy.");
            return;
        }

        // Copy ngp_runner.py to Unity scripts folder
        CopyAndLog("Scripts/ngp_runner.py", pluginRoot, unityDestRoot);

        // Copy Python modules to top-level NeRFPlugin folder
        CopyFolderIfExists("nerf_cli", pluginRoot, topLevelDestRoot);
        CopyFolderIfExists("pipeline", pluginRoot, topLevelDestRoot);
        CopyAndLog("setup.py", pluginRoot, topLevelDestRoot);

        AssetDatabase.Refresh();
    }

    private static void CopyAndLog(string relativePath, string srcRoot, string destRoot)
    {
        string source = Path.Combine(srcRoot, relativePath);
        string dest = Path.Combine(destRoot, Path.GetFileName(relativePath));

        if (File.Exists(source))
        {
            Directory.CreateDirectory(Path.GetDirectoryName(dest));
            File.Copy(source, dest, overwrite: true);
            Debug.Log($"{Path.GetFileName(source)} copied to {dest}");
        }
    }

    private static void CopyFolderIfExists(string folderName, string srcRoot, string destRoot)
    {
        string sourceFolder = Path.Combine(srcRoot, folderName);
        string destFolder = Path.Combine(destRoot, folderName);

        if (Directory.Exists(sourceFolder))
        {
            CopyDirectory(sourceFolder, destFolder);
            Debug.Log($"{folderName} copied to {destFolder}");
        }
    }

    private static void CopyDirectory(string sourceDir, string destDir)
    {
        Directory.CreateDirectory(destDir);
        foreach (string file in Directory.GetFiles(sourceDir))
        {
            string destFile = Path.Combine(destDir, Path.GetFileName(file));
            File.Copy(file, destFile, overwrite: true);
        }

        foreach (string folder in Directory.GetDirectories(sourceDir))
        {
            string destSubfolder = Path.Combine(destDir, Path.GetFileName(folder));
            CopyDirectory(folder, destSubfolder);
        }
    }

    private static string GetInstallerScriptPath()
    {
        string[] guids = AssetDatabase.FindAssets("NerfPluginInstaller");
        foreach (string guid in guids)
        {
            string path = AssetDatabase.GUIDToAssetPath(guid);
            if (Path.GetFileName(path) == "NerfPluginInstaller.cs")
                return Path.GetFullPath(Path.Combine(Application.dataPath, "..", path));
        }
        return "";
    }
}

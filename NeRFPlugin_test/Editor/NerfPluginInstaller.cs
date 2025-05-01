using UnityEditor;
using UnityEngine;
using System.IO;

[InitializeOnLoad]
public static class NerfPluginInstaller
{
    static NerfPluginInstaller()
    {
        // Get absolute path to the plugin package root
        string editorScriptPath = GetInstallerScriptPath();
        string packageRoot = Path.GetFullPath(Path.Combine(editorScriptPath, "..", ".."));

        string pluginDestRoot = Path.Combine(Application.dataPath, "NeRFPlugin");

        // Copy ngp_runner.py
        string sourceRunner = Path.Combine(packageRoot, "Scripts", "ngp_runner.py");
        string destRunnerDir = Path.Combine(pluginDestRoot, "Scripts");
        string destRunner = Path.Combine(destRunnerDir, "ngp_runner.py");

        if (!File.Exists(destRunner) && File.Exists(sourceRunner))
        {
            Directory.CreateDirectory(destRunnerDir);
            File.Copy(sourceRunner, destRunner);
            Debug.Log("ngp_runner.py copied to Assets/NeRFPlugin/Scripts/");
        }

        // Copy nerf_cli/
        string sourceNerfCli = Path.Combine(packageRoot, "nerf_cli");
        string destNerfCli = Path.Combine(pluginDestRoot, "nerf_cli");
        if (Directory.Exists(sourceNerfCli) && !Directory.Exists(destNerfCli))
        {
            CopyDirectory(sourceNerfCli, destNerfCli);
            Debug.Log("nerf_cli copied to Assets/NeRFPlugin/nerf_cli/");
        }

        // Copy pipeline/
        string sourcePipeline = Path.Combine(packageRoot, "pipeline");
        string destPipeline = Path.Combine(pluginDestRoot, "pipeline");
        if (Directory.Exists(sourcePipeline) && !Directory.Exists(destPipeline))
        {
            CopyDirectory(sourcePipeline, destPipeline);
            Debug.Log("pipeline copied to Assets/NeRFPlugin/pipeline/");
        }

        // Copy setup.py
        string sourceSetup = Path.Combine(packageRoot, "setup.py");
        string destSetup = Path.Combine(pluginDestRoot, "setup.py");
        if (File.Exists(sourceSetup) && !File.Exists(destSetup))
        {
            File.Copy(sourceSetup, destSetup);
            Debug.Log("setup.py copied to Assets/NeRFPlugin/setup.py");
        }

        AssetDatabase.Refresh();
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

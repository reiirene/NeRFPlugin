using UnityEngine;
using System.Diagnostics;
using System.IO;

public class TrainingOrchestrator : MonoBehaviour
{
    [Header("Automatically run the training script on start")]
    public bool autoRun = true;

    [Header("Path to the Python script (relative or absolute)")]
    public string pythonScript = "Assets/NeRFPlugin/Scripts/ngp_runner.py";

    [Header("Image input folder path (absolute)")]
    public string imageFolderPath = "/Users/yourname/Desktop/flowermug";

    [Header("Python executable name")]
    public string pythonCommand = "python3"; // Use "python" on Windows if needed

    void Start()
    {
        if (autoRun)
        {
            RunPipeline();
        }
        else
        {
            UnityEngine.Debug.Log("autoRun is disabled. TrainingOrchestrator will not run the Python script.");
        }
    }

    public void RunPipeline()
    {
        string scriptFullPath = Path.GetFullPath(pythonScript);
        string args = $"\"{scriptFullPath}\" \"{imageFolderPath}\"";

        ProcessStartInfo startInfo = new ProcessStartInfo
        {
            FileName = pythonCommand,
            Arguments = args,
            UseShellExecute = false,
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            CreateNoWindow = true,
            WorkingDirectory = Application.dataPath
        };

        Process process = new Process();
        process.StartInfo = startInfo;

        process.OutputDataReceived += (sender, e) => {
            if (!string.IsNullOrEmpty(e.Data))
                UnityEngine.Debug.Log($"[stdout] {e.Data}");
        };

        process.ErrorDataReceived += (sender, e) => {
            if (!string.IsNullOrEmpty(e.Data))
                UnityEngine.Debug.LogError($"[stderr] {e.Data}");
        };

        try
        {
            process.Start();
            process.BeginOutputReadLine();
            process.BeginErrorReadLine();
            UnityEngine.Debug.Log("NeRF pipeline script started.");
        }
        catch (System.Exception ex)
        {
            UnityEngine.Debug.LogError($"Failed to start process: {ex.Message}");
        }
    }
}

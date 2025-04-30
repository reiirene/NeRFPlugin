using UnityEngine;
using System.Diagnostics;
using System.IO;

public class TrainingOrchestrator : MonoBehaviour
{
    [Header("是否自动启动训练脚本")]
    public bool autoRun = true;  // ✅ Inspector 中的勾选项

    [Header("Python 脚本路径（相对路径 or 绝对路径）")]
    public string pythonScript = "Assets/NeRFPlugin/Scripts/ngp_runner.py";

    [Header("图片输入路径（绝对路径）")]
    public string imageFolderPath = "/Users/yourname/Desktop/flowermug";

    [Header("Python 可执行文件名")]
    public string pythonCommand = "python3"; // Windows 可改为 "python"

    void Start()
    {
        if (autoRun)
        {
            RunPipeline();
        }
        else
        {
            Debug.Log("🔕 autoRun 未勾选，TrainingOrchestrator 不执行 Python 脚本");
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
                UnityEngine.Debug.Log($"[py-out] {e.Data}");
        };

        process.ErrorDataReceived += (sender, e) => {
            if (!string.IsNullOrEmpty(e.Data))
                UnityEngine.Debug.LogError($"[py-err] {e.Data}");
        };

        try
        {
            process.Start();
            process.BeginOutputReadLine();
            process.BeginErrorReadLine();
            UnityEngine.Debug.Log("🚀 已启动 NeRF pipeline 脚本！");
        }
        catch (System.Exception ex)
        {
            UnityEngine.Debug.LogError($"❌ 启动失败：{ex.Message}");
        }
    }
}
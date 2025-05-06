using UnityEditor;
using UnityEngine;
using System.Diagnostics;
using System.IO;
using System.Text;

public class NeRFTerminalEditorWindow : EditorWindow
{
    private string inputArgs = "";
    private Vector2 scrollPos;
    private StringBuilder output = new StringBuilder();
    private string pythonPath;
    private Process currentProcess = null;
    private bool isRunning = false;

    [MenuItem("NeRF/Terminal")]
    public static void ShowWindow()
    {
        GetWindow<NeRFTerminalEditorWindow>("NeRF Terminal");
    }

    void OnEnable()
    {
        pythonPath = EditorPrefs.GetString("NeRF_PythonPath", "python");
    }

    void OnGUI()
    {
        EditorGUILayout.LabelField("Python CLI Terminal", EditorStyles.boldLabel);
        inputArgs = EditorGUILayout.TextField("Args:", inputArgs);

        if (GUILayout.Button("Run"))
        {
            RunCommand();
        }

        if (GUILayout.Button("Select Python Executable (venv or system)"))
        {
            string path = EditorUtility.OpenFilePanel("Select python.exe", "", "exe");
            if (!string.IsNullOrEmpty(path))
            {
                pythonPath = path;
                EditorPrefs.SetString("NeRF_PythonPath", pythonPath);
                AppendOutput($"[INFO] Python path set to: {pythonPath}");
            }
        }

        GUILayout.BeginHorizontal();

        if (GUILayout.Button("Stop"))
        {
            StopProcess();
        }

        if (GUILayout.Button("Clear Terminal"))
        {
            output.Clear();
            Repaint();
        }

        GUILayout.EndHorizontal();

        EditorGUILayout.Space();
        scrollPos = EditorGUILayout.BeginScrollView(scrollPos, GUILayout.Height(300));
        EditorGUILayout.TextArea(output.ToString(), GUILayout.ExpandHeight(true));
        EditorGUILayout.EndScrollView();

        if (GUILayout.Button("Load .ply"))
        {
            LoadPlyModel();
        }
        if (GUILayout.Button("Load .vol Volume"))
        {
            LoadVolumeModel();
        }

    }

    void RunCommand()
    {
        if (isRunning)
        {
            AppendOutput("[WARN] Process is already running.");
            return;
        }

        string scriptPath = Path.GetFullPath("Assets/NeRFPlugin/Scripts/ngp_runner.py");
        string args = $"\"{scriptPath}\" {inputArgs}";
        AppendOutput($"[INFO] Running: {pythonPath} {args}");

        ProcessStartInfo psi = new ProcessStartInfo
        {
            FileName = pythonPath,
            Arguments = args,
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            UseShellExecute = false,
            CreateNoWindow = true
        };

        try
        {
            currentProcess = new Process { StartInfo = psi };

            currentProcess.OutputDataReceived += (s, e) =>
            {
                if (!string.IsNullOrEmpty(e.Data))
                    AppendOutput($"[stdout] {e.Data}");
            };

            currentProcess.ErrorDataReceived += (s, e) =>
            {
                if (!string.IsNullOrEmpty(e.Data))
                    AppendOutput($"[stderr] {e.Data}");
            };

            currentProcess.EnableRaisingEvents = true;
            currentProcess.Exited += (s, e) =>
            {
                isRunning = false;
                AppendOutput("[INFO] Process finished.");
            };

            currentProcess.Start();
            currentProcess.BeginOutputReadLine();
            currentProcess.BeginErrorReadLine();

            isRunning = true;
            AppendOutput("[INFO] Process started...");
        }
        catch (System.Exception ex)
        {
            AppendOutput($"[ERROR] Failed to start process: {ex.Message}");
        }
    }

    void StopProcess()
    {
        if (currentProcess != null && !currentProcess.HasExited)
        {
            currentProcess.Kill();
            currentProcess.Dispose();
            currentProcess = null;
            isRunning = false;
            AppendOutput("[INFO] Process was stopped.");
        }
        else
        {
            AppendOutput("[WARN] No process is currently running.");
        }
    }

    void AppendOutput(string line)
    {
        output.AppendLine(line);
        Repaint();
    }

    private void LoadPlyModel()
    {
        string path = EditorUtility.OpenFilePanel("Select .Ply Model", "Assets/NeRFPlugin/Outputs", "ply");
        if (string.IsNullOrEmpty(path))
        {
            AppendOutput("[INFO] No file selected");
            return;
        }

        GameObject model = PlyImporter.Import(path);
        if (model != null)
        {
            model.name = Path.GetFileNameWithoutExtension(path);
            model.transform.position = Vector3.zero;
            Selection.activeGameObject = model;
            AppendOutput("$[INFO] Loaded model: {path}");
        }
        else
        {
            AppendOutput($"[ERROR] Failed to load .ply model: {path}");
        }
    }
    private void LoadVolumeModel()
    {
        string path = EditorUtility.OpenFilePanel("Select .vol Volume", "Assets/NeRFPlugin/Outputs", "vol");
        if (string.IsNullOrEmpty(path))
        {
            AppendOutput("[INFO] No volume file selected");
            return;
        }

        // Create a container GameObject and attach VolumeLoader
        GameObject container = new GameObject("LoadedVolume");
        VolumeLoader loader = container.AddComponent<VolumeLoader>();
        loader.volumePath = path;

        Texture3D volume = loader.LoadVolume();
        if (volume != null)
        {
            AppendOutput($"[INFO] Loaded volume from: {path}");
            // You can also assign this texture to a volume material if desired
        }
        else
        {
            AppendOutput($"[ERROR] Failed to load volume from: {path}");
        }
    }

}

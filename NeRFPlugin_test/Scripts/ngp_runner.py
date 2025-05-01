import sys
import os
import subprocess
import traceback
import shutil

print("[DEBUG] ngp_runner.py actually started")

try:
    if len(sys.argv) < 2:
        print("[ERROR] Not enough arguments. Usage: python ngp_runner.py /path/to/data")
        sys.exit(1)

    data_path = sys.argv[1]
    input_file_path = os.path.join("Assets", "NeRFPlugin", "Inputs", "deps_input.txt")
    log_path = os.path.join("Assets", "NeRFPlugin", "Outputs", "pipeline_log.txt")
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    os.makedirs(os.path.dirname(input_file_path), exist_ok=True)

    def log(msg):
        print(msg)
        with open(log_path, "a") as f:
            f.write(msg + "\n")

    log("[STEP 1] Parsed data path: " + data_path)

    def read_user_input():
        if os.path.exists(input_file_path):
            with open(input_file_path, "r") as f:
                return f.read().strip().lower()
        return ""

    # Try importing nerf_cli
    try:
        import nerf_cli
        log("[STEP 2] nerf_cli is importable")
    except ImportError:
        log("[STEP 2b] nerf_cli not found. Trying auto-install...")

        script_dir = os.path.dirname(os.path.abspath(__file__))
        plugin_root = os.path.abspath(os.path.join(script_dir, ".."))
        setup_path = os.path.join(plugin_root, "setup.py")

        if not os.path.exists(setup_path):
            log(f"[ERROR] setup.py not found in plugin root: {setup_path}")
            sys.exit(1)

        try:
            log(f"[STEP 2c] Running pip install -e {plugin_root}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", plugin_root])
            log("[STEP 2d] Restarting script after pip install...")
            subprocess.check_call([sys.executable, os.path.abspath(__file__)] + sys.argv[1:])
            sys.exit(0)
        except Exception as e:
            log(f"[ERROR] Failed to auto-install nerf_cli: {e}")
            traceback.print_exc()
            with open(log_path, "a") as f:
                traceback.print_exc(file=f)
            sys.exit(1)

    # Search for vcvars64.bat in common locations
    def find_vcvars():
        vs_paths = [
            os.environ.get("VSINSTALLDIR"),
            r"C:\Program Files\Microsoft Visual Studio\2022\Community",
            r"C:\Program Files\Microsoft Visual Studio\2022\Professional",
            r"C:\Program Files\Microsoft Visual Studio\2022\Enterprise",
            r"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community",
        ]
        for base in vs_paths:
            if base:
                vcvars = os.path.join(base, "VC", "Auxiliary", "Build", "vcvars64.bat")
                if os.path.exists(vcvars):
                    return vcvars
        return None

    vcvars_path = find_vcvars()

    if vcvars_path:
        bat_command = f'"{vcvars_path}" && "{sys.executable}" -m nerf_cli "{data_path}"'
        log(f"[INFO] Running with Visual Studio environment: {bat_command}")

        try:
            process = subprocess.Popen(f'cmd.exe /c "{bat_command}"',
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       shell=True,
                                       text=True)
        except Exception as e:
            log(f"[ERROR] Failed to launch process via vcvars64.bat: {e}")
            traceback.print_exc()
            sys.exit(1)
    else:
        log("[WARN] vcvars64.bat not found. Running without Visual Studio environment.")
        cmd = [sys.executable, "-m", "nerf_cli", data_path]
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        except Exception as e:
            log(f"[ERROR] Failed to launch subprocess: {e}")
            traceback.print_exc()
            with open(log_path, "a") as f:
                traceback.print_exc(file=f)
            sys.exit(1)

    for line in process.stdout:
        log(f"[stdout] {line.strip()}")
    for line in process.stderr:
        log(f"[stderr] {line.strip()}")

    process.wait()
    log("[STEP 4] Process finished.")

    os.makedirs("Assets/NeRFPlugin/Outputs", exist_ok=True)
    with open("Assets/NeRFPlugin/Outputs/output.obj", "w") as f:
        f.write("# Dummy .obj generated\n")

    log("[SUCCESS] output.obj generated.")

except Exception as e:
    def log(msg):
        print(msg)
        with open("Assets/NeRFPlugin/Outputs/pipeline_log.txt", "a") as f:
            f.write(msg + "\n")

    log(f"[ERROR] Exception occurred: {e}")
    traceback.print_exc()
    with open("Assets/NeRFPlugin/Outputs/pipeline_log.txt", "a") as f:
        traceback.print_exc(file=f)
    sys.exit(1)

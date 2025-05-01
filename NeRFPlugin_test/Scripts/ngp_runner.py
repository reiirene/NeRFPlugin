import sys
import os
import subprocess
import traceback
import shutil
import platform
import logging
from pathlib import Path

print("[DEBUG] ngp_runner.py actually started")

# Set up logging
log_path = os.path.join("Assets", "NeRFPlugin", "Outputs", "pipeline_log.txt")
os.makedirs(os.path.dirname(log_path), exist_ok=True)

logging.basicConfig(
    filename=log_path,
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s'
)

def log(msg):
    print(msg)
    logging.info(msg)

def log_exception(e):
    tb = traceback.format_exc()
    print(tb)
    with open(log_path, "a") as f:
        f.write(tb + "\n")

try:
    if len(sys.argv) < 2:
        log("[ERROR] Not enough arguments. Usage: python ngp_runner.py /path/to/data")
        sys.exit(1)

    data_path = sys.argv[1]
    log("[STEP 1] Parsed data path: " + data_path)
    log(f"[DEBUG] Python version: {platform.python_version()}")

    # Try importing nerf_cli
    try:
        import nerf_cli
        log("[STEP 2] nerf_cli is importable")
    except ImportError:
        log("[STEP 2b] nerf_cli not found. Trying auto-install...")
        script_dir = Path(__file__).resolve().parent
        plugin_root = Path(__file__).resolve().parents[3] / "NeRFPlugin"
        setup_path = plugin_root / "setup.py"

        if not setup_path.exists():
            log(f"[ERROR] setup.py not found in plugin root: {setup_path}")
            sys.exit(1)

        try:
            log(f"[STEP 2c] Running pip install -e {plugin_root}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", str(plugin_root)])
            log("[STEP 2d] Restarting script after pip install...")
            subprocess.check_call([sys.executable, __file__] + sys.argv[1:])
            sys.exit(0)
        except Exception as e:
            log(f"[ERROR] Failed to auto-install nerf_cli: {e}")
            log_exception(e)
            sys.exit(1)

    # Search for vcvars64.bat
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
    bat_script = os.path.join("Assets", "NeRFPlugin", "Outputs", "launch_pipeline.bat")
    os.makedirs(os.path.dirname(bat_script), exist_ok=True)

    if vcvars_path:
        with open(bat_script, "w") as f:
            f.write(f'@echo off\n')
            f.write(f'call "{vcvars_path}"\n')
            f.write(f'"{sys.executable}" -m nerf_cli "{data_path}"\n')
            f.write("pause\n")

        log(f"[INFO] Created batch file: {bat_script}")
        log("[INFO] Launching external terminal...")

        subprocess.Popen(
            ["cmd.exe", "/k", bat_script],
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        log("[INFO] External terminal launched. Exiting runner.")
        sys.exit(0)

    else:
        log("[WARN] vcvars64.bat not found. Running without Visual Studio environment.")
        cmd = [sys.executable, "-m", "nerf_cli", data_path]
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            for line in process.stdout:
                log(f"[stdout] {line.strip()}")
            for line in process.stderr:
                log(f"[stderr] {line.strip()}")
            process.wait()
        except Exception as e:
            log(f"[ERROR] Failed to launch subprocess: {e}")
            log_exception(e)
            sys.exit(1)

    log("[STEP 4] Process finished.")

    # Dummy output (only if not launched externally)
    output_path = os.path.join("Assets", "NeRFPlugin", "Outputs", "output.obj")
    with open(output_path, "w") as f:
        f.write("# Dummy .obj generated\n")

    log("[SUCCESS] output.obj generated.")

except Exception as e:
    log(f"[ERROR] Exception occurred: {e}")
    log_exception(e)
    sys.exit(1)

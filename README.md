# NeRFPlugin

NeRF Plug-in for Game Engine

- Shared Google Drive: https://drive.google.com/drive/folders/1LbkkiywWdCH_FyGzJAA2CTo7HfEqMkVs?usp=drive_link
- Initial Result(three model comparison): https://docs.google.com/spreadsheets/d/1pnHGtc6EfboHNJS1DQj4KptcSFemMGVWYgrk0GNdS9c/edit?gid=0#gid=0

## Requirements
### Python (Cross-platform)
Install Python >= 3.7

## Windows

> Manual installation is required for system-level tools.

### 1. Install System Dependencies

- [Visual Studio](https://visualstudio.microsoft.com/) with:
  - **Desktop Development with C++** workload
  - CMake integration
- [CUDA Toolkit](https://developer.nvidia.com/cuda-downloads) ≥ 11.4
  - Ensure your GPU is supported
  - Add CUDA paths to your system environment variables:
    - `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8\bin`
    - `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8\libnvvp`
- [COLMAP](https://colmap.github.io/install.html) (Required for 3D reconstruction):
  - Download the Windows binary from the official site
  - Add COLMAP to your system PATH:
    ```bash
    # Example (run in PowerShell as Admin):
    [Environment]::SetEnvironmentVariable(
        "Path",
        [Environment]::GetEnvironmentVariable("Path", [EnvironmentVariableTarget]::Machine) + ";C:\Program Files\COLMAP-3.8",
        [EnvironmentVariableTarget]::Machine
    )
    ```
  - Verify installation:
    ```bash
    colmap --version
    ```
### 2. Set up Python Environment

```bash
python -m venv venv_ngp
venv_ngp\Scripts\activate
pip install -r requirements/requirements_windows.txt
```

## Ubuntu/Linux
### 1. Install System Dependencies
Run the provided helper script (requires sudo):
```bash
bash install ubuntu_deps.sh
```
Or manually install:
```bash
sudo apt update
sudo apt install -y build-essential git cmake libglfw3-dev libglew-dev \
                    libomp-dev libopenexr-dev libxi-dev libxinerama-dev \
                    libxcursor-dev libpython3-dev python3-pip
```
Install COLMAP
```bash
# Install COLMAP
sudo apt install -y colmap
# Verify installation
colmap --version
```

### 2. Set up Python Environment
```bash
python3 -m venv venv_ngp
source venv_ngp/bin/activate
pip install -r requirements/requirements_ubuntu.txt
```

## MacOS
Due to CUDA's discontinued support of macOS, this plugin cannot be run on a macOS environment

## CLI Usage

To run the cli, use
```bash
python -m nerf_cli path\to\data
```

# Usage Guide: How to Use NeRFPlugin in Unity

## Import Plugin

1. Open Unity.
2. Navigate to `Window > Package Manager`.
3. Click `+ > Add package from disk...`.
4. Select `NeRFPlugin/package.json` to import the plugin.

## Scene Setup

1. Create an empty GameObject in your scene and rename it to `NeRFRunner`.
2. Attach the `TrainingOrchestrator.cs` script to the `NeRFRunner` GameObject.
3. Configure the following fields in the Inspector:
   - **Python script path**: `Scripts/ngp_runner.py`
   - **Image folder path**: Absolute path to your training image data
   - **AutoRun**: Tick the checkbox if you want training to automatically start when playing.

## Run the Plugin

1. Click the **Play** button in Unity.
2. `TrainingOrchestrator.cs` will launch the Python script.
3. `ngp_runner.py` internally executes the following command:python -m nerf_cli /your/image/path
4. `nerf_cli` runs the complete NeRF training pipeline.
5. Upon completion, the pipeline writes an `output.obj` file into:Assets/NeRFPlugin/Outputs/output.obj
6. `MeshAutoLoader.cs` automatically detects the generated `output.obj` file.
7. `ObjImporter.cs` parses the `.obj` file and constructs a Unity `Mesh`.
8. The 3D model is successfully loaded and displayed inside the Unity scene.



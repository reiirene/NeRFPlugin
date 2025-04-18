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
python -m nerf_cli
```

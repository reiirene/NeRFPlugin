# NeRFPlugin

NeRF Plug-in for Game Engine

- Shared Google Drive: https://drive.google.com/drive/folders/1LbkkiywWdCH_FyGzJAA2CTo7HfEqMkVs?usp=drive_link
- Initial Result(three model comparison): https://docs.google.com/spreadsheets/d/1pnHGtc6EfboHNJS1DQj4KptcSFemMGVWYgrk0GNdS9c/edit?gid=0#gid=0

## CLI Usage

To run the cli, use `python -m nerf_cli`

## Windows
### Set up Python Environment
```bash
python -m venv venv
venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```
### Prerequisites

Make sure you have installed:

1. **Install MSVC, CMAKE and Build Tools for Visual Studio**<br>
https://visualstudio.microsoft.com/ja/visual-cpp-build-tools/<br>
2. **CUDA Toolkit >= 11.4**<br>
https://docs.nvidia.com/cuda/cuda-installation-guide-microsoft-windows/index.html<br>
Check CUDA installation<br>
```bash
nvcc --version
```
3. **Ensure CUDA is in your PATH**
```bash
where nvcc
```
If you see something like:
```bash
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8\bin\nvcc.exe
```
Then it's already in your PATH


- **Python 3.7+**
- **COLMAP**
  - **macOS**: Please install COLMAP manually using Homebrew:
    ```bash
    brew install colmap
    ```
  - **Windows/Linux**: COLMAP will be downloaded automatically by `colmap2nerf.py` when needed.

## Ubuntu/Linux

## MacOS


Folder structure
```bash
    your_dataset/
    ├── images/
    │   ├── image_001.jpg
    │   ├── image_002.jpg
    │   └── ...
```
### Run the script
```bash
    python data_transform.py /absolute/path/to/your_dataset
```

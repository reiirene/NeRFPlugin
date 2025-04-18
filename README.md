# NeRFPlugin

NeRF Plug-in for Game Engine

- Shared Google Drive: https://drive.google.com/drive/folders/1LbkkiywWdCH_FyGzJAA2CTo7HfEqMkVs?usp=drive_link
- Initial Result(three model comparison): https://docs.google.com/spreadsheets/d/1pnHGtc6EfboHNJS1DQj4KptcSFemMGVWYgrk0GNdS9c/edit?gid=0#gid=0

## CLI Usage

To run the cli, use `python -m nerf_cli`

## Data Transform Usage(step 1)
### Prerequisites

Make sure you have installed:

- **Python 3.7+**
- **COLMAP**
  - **macOS**: Please install COLMAP manually using Homebrew:
    ```bash
    brew install colmap
    ```
  - **Windows/Linux**: COLMAP will be downloaded automatically by `colmap2nerf.py` when needed.

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

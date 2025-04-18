# DatasetPrep

## Prerequisites
- **Python 3.7+**
- **COLMAP**
  - **macOS**: Please install COLMAP manually using Homebrew:
    ```bash
    brew install colmap
    ```
  - **Windows/Linux**: COLMAP will be downloaded automatically by `colmap2nerf.py` when needed.

###Folder structure
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
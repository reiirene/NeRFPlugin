import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

from ..models import ColmapOutput, Image
from ..transformer import Transformer

REPO_URL = "https://github.com/NVlabs/instant-ngp.git"
REPO_DIR = "instant-ngp"

class ColmapTransformer(Transformer[Image, ColmapOutput]):
    def __init__(self, check_dependencies: bool = True):
        self.check_dependencies = check_dependencies
    
    def transform(self, input: Image) -> ColmapOutput:
        if self.check_dependencies:
            self._check_python()
            self._check_colmap_on_mac()
        
        image_dir = input.inner 
        print("Detected platform:", platform.system())
        
        image_dir = os.path.abspath(image_dir)
        parent_dir = str(Path(image_dir).parent)
        repo_path = self._clone_repo(parent_dir)
        
        transforms_path = self._run_colmap2nerf(repo_path, image_dir)
        
        return ColmapOutput(
            inner=input.inner + " colmap_transformed",
            transforms_path=transforms_path,
            colmap_path=os.path.join(image_dir, "colmap_text")
        )
    

    def _check_python(self):
        if sys.version_info < (3, 7):
            print("❌ Python 3.7 or higher is required.")
            sys.exit(1)
    
    def _check_colmap_on_mac(self):
        if platform.system().lower() == "darwin" and shutil.which("colmap") is None:
            print("❌ COLMAP not found on macOS.")
            print("💡 Please install COLMAP using Homebrew:")
            print("   brew install colmap")
            sys.exit(1)
    
    def _clone_repo(self, parent_dir: str) -> str:
        repo_path = os.path.join(parent_dir, REPO_DIR)
        if os.path.exists(repo_path):
            print(f"📂 '{REPO_DIR}' already exists. Skipping git clone.")
            return repo_path
            
        print("📥 Cloning instant-ngp repo ...")
        subprocess.run(["git", "clone", REPO_URL], cwd=parent_dir, check=True)
        return repo_path
    
    def _run_colmap2nerf(self, repo_path: str, project_root: str) -> str:
        script_path = os.path.join(repo_path, "scripts", "colmap2nerf.py")
        if not os.path.exists(script_path):
            print(f"❌ colmap2nerf.py not found in {script_path}")
            sys.exit(1)
        
        images_path = os.path.join(project_root, "images")
        if not os.path.isdir(images_path):
            print(f"❌ 'images' folder not found in {project_root}")
            sys.exit(1)
        
        num_images = len([f for f in os.listdir(images_path) 
                         if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
        print(f"Found {num_images} images in {images_path}")
        
        cmd = [
            sys.executable,
            script_path,
            "--images", images_path,
            "--colmap_matcher", "exhaustive",
            "--run_colmap",
            "--aabb_scale", "32",
            "--overwrite"
        ]
        
        print(f"Running colmap2nerf.py in {project_root} ...")
        result = subprocess.run(cmd, cwd=project_root, env=os.environ, 
                               capture_output=True, text=True)
        
        if result.returncode != 0:
            print("❌ colmap2nerf.py failed to execute")
            print("stderr:\n", result.stderr)
            print("stdout:\n", result.stdout)
            sys.exit(1)
        
        print("✅ colmap2nerf.py executed successfully")
        
        transforms_path = os.path.join(project_root, "transforms.json")
        if not os.path.exists(transforms_path):
            print(f"❌ transforms.json not found in {project_root}")
            sys.exit(1)
            
        return transforms_path

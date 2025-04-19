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
        
        image_dir = os.path.abspath(input.inner)
        print("Detected platform:", platform.system())
  
        parent_dir = str(Path(image_dir).parent)
        repo_path = self._clone_repo(parent_dir)
        
        transforms_path = self._run_colmap2nerf(repo_path, image_dir)
        
        return ColmapOutput(
            inner=input.inner + " colmap_transformed",
            transforms_path=transforms_path,
            colmap_path=os.path.join(image_dir, "colmap_text"),
            ngp_repo_path=repo_path
        )
    
    def _clone_repo(self, parent_dir: str) -> str:
        repo_path = os.path.join(parent_dir, REPO_DIR)
        if os.path.exists(repo_path):
            print(f"'{REPO_DIR}' already exists. Skipping git clone.")
            return repo_path
            
        print("Cloning instant-ngp repo ...")
        subprocess.run(["git", "clone", "--recursive", REPO_URL, repo_path], check=True)
        return repo_path
    
    def _run_colmap2nerf(self, repo_path: str, image_dir: str) -> str:
        script_path = os.path.join(repo_path, "scripts", "colmap2nerf.py")
        if not os.path.exists(script_path):
            raise FileNotFoundError(f"{script_path} not found!")
        
        transforms_output = os.path.join(image_dir, "transforms.json")

        subprocess.run([
            sys.executable, script_path,
            "--images", image_dir,
            "--output", image_dir,
            "--run_colmap"
        ], check=True)

        return transforms_output

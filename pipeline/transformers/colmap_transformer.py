import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

from ..models import ColmapOutput, Image
from ..transformer import Transformer

REPO_URL = "https://github.com/NVlabs/instant-ngp.git"

# Resolve Unity project structure
current_file = Path(__file__).resolve()

PROJECT_ROOT = Path(__file__).resolve()
while PROJECT_ROOT.name != "Assets":
    PROJECT_ROOT = PROJECT_ROOT.parent
PROJECT_ROOT = PROJECT_ROOT.parent  # Go from Assets -> Unity root

REPO_DIR = "instant-ngp"
REPO_PATH = PROJECT_ROOT / REPO_DIR

VALID_IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}

def is_image_file(filename):
    return Path(filename).suffix.lower() in VALID_IMAGE_EXTS

class ColmapTransformer(Transformer[Image, ColmapOutput]):
    
    def transform(self, input: Image) -> ColmapOutput:
        image_dir = os.path.abspath(input.inner)
        print("Detected platform:", platform.system())

        self._filter_image_directory(image_dir)
  
        repo_path = self._clone_repo()
        self._build_instant_ngp(repo_path)
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "colmap2nerf.py"))
        if not os.path.exists(script_path):
            raise FileNotFoundError(f"{script_path} not found!")

        transforms_path = self._run_colmap2nerf(script_path, image_dir)
        
        return ColmapOutput(
            inner=input.inner,
            transforms_path=transforms_path,
            colmap_path=os.path.join(image_dir, "colmap_text"),
            ngp_repo_path=str(repo_path)
        )
    
    def _clone_repo(self) -> str:
        repo_path = REPO_PATH
        if os.path.exists(repo_path):
            print(f"'{REPO_DIR}' already exists. Skipping git clone.")
            return repo_path
            
        print("Cloning instant-ngp repo ...")
        try:
            # Shallow clone main repo first
            subprocess.run([
                "git", "clone",
                "--recursive",
                "--depth", "1",
                REPO_URL,
                repo_path
            ], check=True)

            # Initialize only essential submodules
            os.chdir(repo_path)

            subprocess.run([
                "git", "submodule", "update", "--init", "--recursive"
            ], check=True)

            return repo_path
        except subprocess.CalledProcessError as e:
            print(f"Error cloning repository: {e}")
            # Clean up partial clone if failed
            if os.path.exists(repo_path):
                shutil.rmtree(repo_path)
            raise

    def _disable_submodules(self, repo_path: str):
        """Disable problematic submodules to avoid long path issues"""
        gitmodules_path = os.path.join(repo_path, ".gitmodules")
        if os.path.exists(gitmodules_path):
            with open(gitmodules_path, "a") as f:
                f.write("\n[submodule \"dependencies/cutlass\"]\n\tactive = false\n")
                f.write("\n[submodule \"dependencies/json\"]\n\tactive = false\n")
                f.write("\n[submodule \"dependencies/tinylogger\"]\n\tactive = false\n")


    def _build_instant_ngp(self, repo_path: Path):
        build_dir = repo_path / "build"
        if (build_dir / "ngp_cuda_test.exe").exists() or (build_dir / "ngp_cuda_test").exists():
            print("instant-ngp already built. Skipping build.")
            return

        print("Building instant-ngp...")

        os.makedirs(build_dir, exist_ok=True)
        original_cwd = os.getcwd()
        try:
            os.chdir(build_dir)
            subprocess.run(["cmake", "..", "-DCMAKE_BUILD_TYPE=RelWithDebInfo"], check=True)
            subprocess.run(["cmake", "--build", ".", "--config", "RelWithDebInfo"], check=True)
        finally:
            os.chdir(original_cwd)

    def _run_colmap2nerf(self, script_path: str, image_dir: str) -> str:

        transforms_output = os.path.join(image_dir, "transforms.json")

        cwd = image_dir

        # Check GPU availability
        gpu_available = self._check_gpu_available()

        try:
            # Run with automatic COLMAP
            cmd = [
                sys.executable, script_path,
                "--images", image_dir,
                "--run_colmap"
            ]
        
            if gpu_available:
                cmd.append("--use_gpu")
                print("GPU detected - using CUDA acceleration")
               
            else:
                cmd.extend(["--SiftExtraction.num_threads", "4"])
                print("No GPU detected - using CPU (slower)")
        
            subprocess.run(cmd, check=True, cwd=image_dir)
        
        except subprocess.CalledProcessError as e:
            print(f"Automatic COLMAP failed (exit code {e.returncode}), trying manual fallback...")
            raise RuntimeError("COLMAP execution failed.") from e
    
        return transforms_output

    def _check_gpu_available(self) -> bool:
        """Check if CUDA GPU is available"""
        try:
            result = subprocess.run(["nvidia-smi"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return result.returncode == 0
        except FileNotFoundError:
            return False
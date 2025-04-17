import os
import sys
import subprocess
import platform
import webbrowser
import shutil
from pathlib import Path

REPO_URL = "https://github.com/NVlabs/instant-ngp.git"
REPO_DIR = "instant-ngp"

def check_python():
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required.")
        webbrowser.open("https://www.python.org/downloads/")
        sys.exit(1)

def check_colmap_on_mac(): # Check if COLMAP is installed on macOS(instant-ngp cannot install colmap on mac automatically)
    if platform.system().lower() == "darwin" and shutil.which("colmap") is None:
        print("❌ COLMAP not found on macOS.")
        print("💡 Please install COLMAP using Homebrew:")
        print("   brew install colmap")
        sys.exit(1)

def clone_repo(parent_dir):
    repo_path = os.path.join(parent_dir, REPO_DIR)
    if os.path.exists(repo_path):
        print(f"📂 '{REPO_DIR}' already exists. Skipping git clone.")
        return repo_path
    print("📥 Cloning instant-ngp repo ...")
    subprocess.run(["git", "clone", REPO_URL], cwd=parent_dir, check=True)
    return repo_path

def run_colmap2nerf(repo_path, project_root):
    script_path = os.path.join(repo_path, "scripts", "colmap2nerf.py")
    if not os.path.exists(script_path):
        print(f"❌ colmap2nerf.py not found in {script_path}")
        sys.exit(1)

    images_path = os.path.join(project_root, "images")
    if not os.path.isdir(images_path):
        print(f"❌ 'images' folder not found in {project_root}")
        sys.exit(1)

    num_images = len([f for f in os.listdir(images_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
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
    result = subprocess.run(cmd, cwd=project_root, env=os.environ, text=True)

    if result.returncode != 0:
        print("❌ colmap2nerf.py failed to execute")
        print("stderr:\n", result.stderr)
        print("stdout:\n", result.stdout)
        sys.exit(1)

    print("✅ colmap2nerf.py executed successfully")
    print("stdout:\n", result.stdout)
    print("Done! Check transforms.json in", project_root)

def main(image_dir):
    check_python()
    check_colmap_on_mac()

    print("Detected platform:", platform.system())

    image_dir = os.path.abspath(image_dir)
    parent_dir = str(Path(image_dir).parent)
    repo_path = clone_repo(parent_dir)
    run_colmap2nerf(repo_path, image_dir)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python data_transform.py <path_to_image_folder>")
        sys.exit(1)
    main(sys.argv[1])
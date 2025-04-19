import os
import sys
import subprocess
import platform
import shutil

def install_ngp_python_deps():
    required_packages = [
        "commentjson", "imageio", "numpy", "opencv-python-headless",
        "pybind11", "pyquaternion", "scipy", "tqdm", "gdown"
    ]

    # Check if packages are already installed
    missing = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)

    if missing:
        print(f"Installing missing packages: {", ".join(missing)}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])
    else:
        print("All python packages already installed.")

def prompt_and_install_system_packages():
    # OS warning & setup
    current_os = platform.system().lower()

    if "linux" in current_os:
        print("instant-ngp requires system-level dependencies on Ubuntu.")
        print("This will run `sudo apt install ...` via install_ubuntu_deps.sh")

        '''
        proceed = input("Do you want to install them now? (y/n): ").lower()
        if proceed == "y":
            subprocess.run(["bash", "install_ubuntu_deps.sh"], check=True)
        else:
            print("Skipped Ubuntu system package installation.")
        '''

def check_all_dependencies():
    print("Checking system dependencies")
    prompt_and_install_system_packages()
    print("Checking python dependencies")
    install_ngp_python_deps

def prompt_for_dependency_check():
    response = input("Check dependencies (y/n)? ").strip().lower()
    if response == "y":
        check_all_dependencies()
        print("All dependencies installed")
        return True
    else:
        print("Skipping dependency check")
        return False

def check_system_requirements():
    current_os = platform.system().lower()

    if "windows" in current_os:
        print("Windows System Requirements:")

        cl_path = shutil.which("cl")
        if cl_path:
            print("Visual Studio Build Tools found.")
        else:
            print("Visual Studio with C++ workload not found. Please install:")
            print("- Visual Studio: https://visualstudio.microsoft.com/")
            print("  - With Desktop Development with C++ workload")
            print("- Make sure `cl.exe` is in your PATH.")
        
        cmake_path = shutil.which("cmake")
        if cmake_path:
            print("CMake found.")
        else:
            print("CMake not found. Please install CMake.")

        nvcc_path = shutil.which("nvcc")
        if nvcc_path:
            print("CUDA Toolkit found.")
        else:
            print("CUDA Toolkit not found. Please install from:")
            print("- https://developer.nvidia.com/cuda-downloads")
            print("Add CUDA paths to your environment variables:")
            print("  C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v11.8\\bin")
            print("  C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v11.8\\libnvvp")
    elif "linux" in current_os:
        print("📦 Linux System Requirements:")
        print("Run the following to install dependencies:")
        print("  bash install_ubuntu_deps.sh")
        print("Or manually install with:")
        print("  sudo apt update && sudo apt install -y build-essential git cmake libglfw3-dev libglew-dev \\")
        print("      libomp-dev libopenexr-dev libxi-dev libxinerama-dev libxcursor-dev libpython3-dev python3-pip")
    else:
        print(f"Unsupported platform: {current_os}")

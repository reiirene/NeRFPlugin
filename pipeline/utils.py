import os
import sys
import subprocess
import platform

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

        proceed = input("Do you want to install them now? (y/n): ").lower()
        if proceed == "y":
            subprocess.run(["bash", "install_ubuntu_deps.sh"], check=True)
        else:
            print("Skipped Ubuntu system package installation.")
    
    elif "windows" in current_os:
        print("Detected Windows platform.")
        print("Please ensure the following are manually installed:")
        print("   - Visual Studio with C++ & CMake support")
        print("   - CUDA Toolkit 11.4+ (matching your GPU)")
        print("   - Add CUDA to PATH (e.g., C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v11.8\\bin)")
    
    else:
        print(f"Unsupported platform: {current_os}. Please install system dependencies manually.")

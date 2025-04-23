# ✅ 自动执行 instant-ngp 的 mesh export 命令
# ✅ 把导出的 .obj 或 .ply 文件复制到 Unity 项目的 Assets/Resources/Models/
# ✅ 命令行调用即可集成到更大的 pipeline
# Usage: python export_and_move.py

import os
import shutil
import subprocess
import time

# === 你需要配置这些路径 ===
instant_ngp_path = "/path/to/instant-ngp"  # instant-ngp 根目录
ngp_data_path = "/path/to/output/base"     # 包含 trained .msgpack 的目录
unity_models_path = "/path/to/unity/Assets/Resources/Models"  # Unity 中的 Models 目录

# === 输出文件名（不含扩展名）===
output_name = "exported_model"

# === Step 1: 执行 mesh export 命令 ===
export_cmd = [
    os.path.join(instant_ngp_path, "build/testbed"),  # 可执行文件
    "--mode", "nerf",
    "--load_snapshot", os.path.join(ngp_data_path, "base.msgpack"),
    "--marching_cubes_res", "256",
    "--save_mesh", os.path.join(ngp_data_path, f"{output_name}.obj")
]

print("🚀 Running export command...")
subprocess.run(export_cmd, check=True)

# === Step 2: 拷贝导出文件到 Unity 项目 ===
obj_src = os.path.join(ngp_data_path, f"{output_name}.obj")
obj_dst = os.path.join(unity_models_path, f"{output_name}.obj")

print("📦 Copying exported model to Unity Resources...")
shutil.copy(obj_src, obj_dst)

# === (可选) 等待 Unity 自动导入 ===
print("✅ Done. Switch to Unity to see the model appear.")
time.sleep(2)

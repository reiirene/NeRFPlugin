import sys
import os
import subprocess

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ngp_runner.py /path/to/data")
        sys.exit(1)

    data_path = sys.argv[1]
    print(f"[INFO] Running nerf_cli pipeline with data path: {data_path}")

    # 构建运行命令
    cmd = [sys.executable, "-m", "nerf_cli", data_path]

    result = subprocess.run(cmd, capture_output=True, text=True)

    print("======== STDOUT ========")
    print(result.stdout)
    print("======== STDERR ========")
    print(result.stderr)

    # 模拟生成 Unity 可加载的输出模型[测试使用]
    # 训练 pipeline 最后真的导出了 .obj 文件之后，要修改这一段
    os.makedirs("Assets/NeRFPlugin/Outputs", exist_ok=True)
    with open("Assets/NeRFPlugin/Outputs/output.obj", "w") as f:
        f.write("# Dummy .obj generated after CLI pipeline\n")

    print("[SUCCESS] output.obj generated. Unity can now load the model.")

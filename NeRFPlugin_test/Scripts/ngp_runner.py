import sys
import time

if __name__ == "__main__":
    print("[INFO] Python script started.")
    
    if len(sys.argv) > 1:
        print(f"[INFO] Received image folder path: {sys.argv[1]}")
    else:
        print("[WARNING] No image folder path received.")
    
    for i in range(5):
        print(f"[TRAINING] Simulating training step {i+1}/5...")
        time.sleep(1)

    print("[INFO] Training simulation complete. Exporting output.obj...")
    with open("Assets/NeRFPlugin/Outputs/output.obj", "w") as f:
        f.write("# OBJ dummy file\n")
    print("[SUCCESS] output.obj has been successfully generated.")
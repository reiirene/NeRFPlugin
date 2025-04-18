import os
import subprocess
from binascii import b2a_uu
from ..models import ColmapOutput, NerfOutput
from ..transformer import Transformer

class NerfTransformer(Transformer[ColmapOutput, NerfOutput]):
    def __init__(self, scene_name = "flowers", n_steps = 30000):
        self.scene_name = scene_name
        self.n_steps = n_steps
        self.ngp_dir = os.path.abspath("instant-ngp")
        self.scene_dir = os.path.abspath(f"data/nerf/{scene_name}/{scene_name}")
        self.output_dir = os.path.abspath("saved")

    def clone_and_build_ngp(self):
        if not os.path.exists(self.ngp_dir):
            subprocess.run([
                "git", "clone", "--recursive", "https://github.com/NVlabs/instant-ngp.git", self.ngp_dir
            ], check=True)

        build_dir = os.path.join(self.ngp_dir, "build")
        if not os.path.exists(build_dir):
            os.makedirs(build_dir)
            subprocess.run([
                "cmake", ".", "-B", "build", "-DCMAKE_BUILD_TYPE=RelWithDebInfo"
            ], cwd=self.ngp_dir, check=True)
            subprocess.run([
                "cmake", "--build", "build", "--congif", "RelWithDebInfo", "-j"
            ], cwd=self.ngp_dir, check=True)

    def run_ngp_training(self):
        run_path = os.path.join(self.ngp_dir, "scripts", "run.py")
        if not os.path.exists(run_path):
            raise FileNotFoundError("Instant-ngp run.py script not found.")

        os.makedirs(self.output_dir, exist_ok=True)
        subprocess.run([
            "python", run_path,
            "--scene", self.scene_dir,
            "--n_steps", str(self.n_steps),
            "--save_snapshot", os.path.join(self.output_dir, f"{self.scene_name}.msgpack"),
            "--save_mesh", os.path.join(self.output_dir, f"{self.scene_name}.ply"),
            "--train"
        ], cwd=self.ngp_dir, check=True)

    def transform(self, input: ColmapOutput) -> NerfOutput:
        return NerfOutput(inner=input.inner + " nerf_transformed")

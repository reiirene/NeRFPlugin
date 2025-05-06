import os
import sys
import subprocess
from binascii import b2a_uu
from ..models import ColmapOutput, NerfOutput
from ..transformer import Transformer

class NerfTransformer(Transformer[ColmapOutput, NerfOutput]):
    def __init__(self, input_data: ColmapOutput, n_steps: int = 30000):
        self.input_data = input_data
        self.n_steps = n_steps

        # Extract info from input_data
        self.scene_dir = os.path.abspath(input_data.inner)
        self.scene_name = os.path.basename(self.scene_dir)
        if not input_data.ngp_repo_path:
            raise ValueError("ngp_repo_path is not set in ColmapOutput.")
        self.ngp_dir = os.path.abspath(input_data.ngp_repo_path)

        self.output_dir = os.path.abspath(os.path.join("Assets", "NeRFPlugin", "Outputs"))
        self.snapshot_path = os.path.join(self.output_dir, f"{self.scene_name}_snapshot.msgpack")
        self.mesh_path = os.path.join(self.output_dir, f"{self.scene_name}_mesh.ply")

    def transform(self) -> NerfOutput:
        
        self.run_ngp_training()
        
        return NerfOutput(
            inner=self.input_data.inner + " nerf_transformed",
            transforms_path=self.input_data.transforms_path,
            colmap_path=self.input_data.colmap_path,
            snapshot_path=self.snapshot_path,
            mesh_path=self.mesh_path,
        )
    
    def run_ngp_training(self):
        run_path = os.path.join(self.ngp_dir, "scripts", "run.py")
        if not os.path.exists(run_path):
            raise FileNotFoundError("Instant-ngp run.py script not found.")

        os.makedirs(self.output_dir, exist_ok=True)
        subprocess.run([
            sys.executable, run_path,
            "--scene", self.scene_dir,
            "--n_steps", str(self.n_steps),
            "--save_snapshot", self.snapshot_path,
            "--save_mesh", self.mesh_path,
            "--save_raw_volumes",
            "--save_mesh_format", "obj",
            "--train"
        ], cwd=self.ngp_dir, check=True)

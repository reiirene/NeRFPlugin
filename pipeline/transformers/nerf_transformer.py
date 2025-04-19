import os
import subprocess
from binascii import b2a_uu
from ..models import ColmapOutput, NerfOutput
from ..transformer import Transformer

class NerfTransformer(Transformer[ColmapOutput, NerfOutput]):
    def __init__(self, input_data: ColmapOutput, n_steps = 30000):
        self.input_data = input_data
        self.n_steps = n_steps

        # Extract info from input_data
        self.scene_dir = os.path.abspath(input_data.inner)
        self.scene_name = os.path.basename(self.scene_dir)
        self.ngp_dir = input_data.ngp_repo_path or os.path.abspath("instant-ngp")
        self.ngp_dir = os.path.abspath("instant-ngp")
        self.output_dir = os.path.abspath("saved")
        self.snapshot_path = os.path.join(self.output_dir, f"{self.scene_name}_snapshot.msgpack")
        self.mesh_path = os.path.join(self.output_dir, f"{self.scene_name}_mesh.ply")

    def run_ngp_training(self):
        run_path = os.path.join(self.ngp_dir, "scripts", "run.py")
        if not os.path.exists(run_path):
            raise FileNotFoundError("Instant-ngp run.py script not found.")

        os.makedirs(self.output_dir, exist_ok=True)
        subprocess.run([
            "python", run_path,
            "--scene", self.scene_dir,
            "--n_steps", str(self.n_steps),
            "--save_snapshot", self.snapshot_path,
            "--save_mesh", self.mesh_path,
            "--train"
        ], cwd=self.ngp_dir, check=True)

    def transform(self, input: ColmapOutput) -> NerfOutput:
        
        self.run_ngp_training()
        
        return NerfOutput(
            inner=input.inner + " nerf_transformed",
            transforms_path=input.transforms_path,
            colmap_path=input.colmap_path,
            snapshot_path=self.snapshot_path,
            mesh_path=self.mesh_path if os.path.exists(self.mesh_path) else None
        )
        #return NerfOutput(inner=input.inner + " nerf_transformed")

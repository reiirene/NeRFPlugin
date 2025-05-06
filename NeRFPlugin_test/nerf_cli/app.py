import typer
import os
from pipeline import run_pipeline
# from pipeline import nerf_pipeline

app = typer.Typer()


@app.command()
def run(input: str) -> None:
    # output = nerf_pipeline.execute(input)
    output = run_pipeline(input)

    print("Pipeline completed.")
    print("Output file at:", output.mesh_path)



if __name__ == "__main__":
    app()

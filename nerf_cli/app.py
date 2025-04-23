import typer
from pipeline import run_pipeline
# from pipeline import nerf_pipeline

app = typer.Typer()


@app.command()
def run(input: str) -> None:
    # output = nerf_pipeline.execute(input)
    output = run_pipeline(input)

    print("Pipeline completed. Output path:", output.inner)


if __name__ == "__main__":
    app()

import typer

from pipeline import nerf_pipeline

app = typer.Typer()


@app.command()
def run(input: str) -> None:
    output = nerf_pipeline.execute(input)
    print(output)


if __name__ == "__main__":
    app()

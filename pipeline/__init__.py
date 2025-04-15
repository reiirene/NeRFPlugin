from .pipeline import PipelineBuilder
from .transformers import (
    ColmapTransformer,
    Exporter,
    ImageReader,
    NerfTransformer,
)

nerf_pipeline = (
    PipelineBuilder()
    .add_step(ImageReader())
    .add_step(ColmapTransformer())
    .add_step(NerfTransformer())
    .add_step(Exporter())
)

from .pipeline import PipelineBuilder
from .utils import (
    install_ngp_python_deps,
    prompt_and_install_system_packages
)

install_ngp_python_deps()
prompt_and_install_system_packages

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
    .add_step(NerfTransformer(scene_name="flowers"))
    #.add_step(Exporter())
)

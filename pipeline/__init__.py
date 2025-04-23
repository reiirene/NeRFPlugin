import os
import sys

from pipeline.transformers import colmap_transformer, nerf_transformer
from .pipeline import PipelineBuilder
from .utils import (
    check_system_requirements,
    prompt_for_dependency_check
)

from .transformers import (
    ColmapTransformer,
    Exporter,
    ImageReader,
    NerfTransformer,
)

# 1. Print system prerequisites based on OS
check_system_requirements()
# 2. Prompt to install Python and system dependencies
if not prompt_for_dependency_check():
    print("Pipeline aborted due to missing dependencies.")
    sys.exit(1)

def run_pipeline(scene_path: str):
    # 1. Read image directory
    image_reader = ImageReader()
    image = image_reader.transform(scene_path)

    # 2. Run COLMAP processing
    colmap_transformer = ColmapTransformer()
    colmap_output = colmap_transformer.transform(image)

    # 3. Run NeRF training
    nerf_transformer = NerfTransformer(input_data=colmap_output)
    nerf_output = nerf_transformer.transform()

    return nerf_output

'''
nerf_pipeline = (
    PipelineBuilder()
    .add_step(ImageReader())
    .add_step(ColmapTransformer())
    .add_step(NerfTransformer())
    #.add_step(Exporter())
)
'''
import os
import sys
from .pipeline import PipelineBuilder
from .utils import (
    check_system_requirements,
    prompt_for_dependency_check
)

# 1. Print system prerequisites based on OS
check_system_requirements()

# 2. Prompt to install Python and system dependencies
if not prompt_for_dependency_check():
    print("Pipeline aborted due to missing dependencies.")
    sys.exit(1)

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

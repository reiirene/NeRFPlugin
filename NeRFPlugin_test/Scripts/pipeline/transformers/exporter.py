from ..models import NerfOutput, PipelineOutput
from ..transformer import Transformer


class Exporter(Transformer[NerfOutput, PipelineOutput]):
    def transform(self, input: NerfOutput) -> PipelineOutput:
        return PipelineOutput(inner=input.inner + " exported")

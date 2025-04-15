from ..models import ColmapOutput, NerfOutput
from ..transformer import Transformer


class NerfTransformer(Transformer[ColmapOutput, NerfOutput]):
    def transform(self, input: ColmapOutput) -> NerfOutput:
        return NerfOutput(inner=input.inner + " nerf_transformed")

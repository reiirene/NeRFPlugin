from ..models import ColmapOutput, Image
from ..transformer import Transformer


class ColmapTransformer(Transformer[Image, ColmapOutput]):
    def transform(self, input: Image) -> ColmapOutput:
        return ColmapOutput(inner=input.inner + " colmap_transformed")

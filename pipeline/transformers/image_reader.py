from ..models import Image
from ..transformer import Transformer


class ImageReader(Transformer[str, Image]):
    def transform(self, input: str) -> Image:
        return Image(inner=input + " read")

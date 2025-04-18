from typing import Any

from pydantic import BaseModel


class Image(BaseModel):
    inner: Any


class ColmapOutput(BaseModel):
    inner: Any


class NerfOutput(BaseModel):
    inner: Any


class PipelineOutput(BaseModel):
    inner: Any


from dataclasses import dataclass
from typing import Optional

@dataclass
class Image:
    inner: str

@dataclass
class ImageFolder:
    path: str
    num_images: int

@dataclass
class ColmapOutput:
    inner: str
    transforms_path: str
    colmap_path: Optional[str] = None

@dataclass
class NerfOutput:
    inner: str
    render_path: Optional[str] = None
    mesh_path: Optional[str] = None
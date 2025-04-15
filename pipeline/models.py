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

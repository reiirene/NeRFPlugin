from typing import Any
from pydantic import BaseModel
from dataclasses import dataclass
from typing import Optional


class Image(BaseModel):
    inner: str

class ColmapOutput(BaseModel):
    inner: str
    transforms_path: str
    colmap_path: Optional[str] = None
    ngp_repo_path: Optional[str] = None

class NerfOutput(BaseModel):
    inner: str
    transforms_path: str
    colmap_path: Optional[str] = None
    snapshot_path: Optional[str] = None 
    mesh_path: Optional[str] = None      

class PipelineOutput(BaseModel):
    inner: Any


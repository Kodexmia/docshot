
from pydantic import BaseModel
from datetime import datetime, timezone
import uuid
from typing import List, Dict, Optional

class ImageModel(BaseModel):
    path: str
    width: int
    height: int
    quality: Optional[int] = None  # Compatible with Python <3.10
    hires: bool = False

class Entry(BaseModel):
    id: str
    title: str
    timestamp: str
    tags: List = []  # avoid PEP585 syntax in older Pythons
    layout: str = "image-left"
    image: ImageModel
    notes: str
    context: Dict = {}

    @classmethod
    def new(cls, title: str, notes: str, layout: str, image: ImageModel):
        return cls(
            id=str(uuid.uuid4())[:8],
            title=title,
            timestamp=datetime.now(timezone.utc).isoformat(),
            layout=layout,
            image=image,
            notes=notes,
        )

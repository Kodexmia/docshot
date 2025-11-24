
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
    notes: str = ""  # Keep for backward compatibility, now optional
    
    # V3.5: NEW split note fields (with defaults for old entries)
    details: str = ""  # Quick summary (2-3 lines)
    location_type: str = "other"  # "web", "app", "desktop", "mobile", "other"
    location_url: str = ""  # URL or app path
    # notes field above for full detailed notes
    
    # V3.5.4: Entry ordering
    order: int = 0  # Display order (0 = use timestamp)
    
    context: Dict = {}

    @classmethod
    def new(cls, title: str, layout: str, image: ImageModel,
            details: str = "", location_type: str = "other", 
            location_url: str = "", notes: str = ""):
        """Create new entry with V3.5 structured fields (all optional for compatibility)"""
        return cls(
            id=str(uuid.uuid4())[:8],
            title=title,
            timestamp=datetime.now(timezone.utc).isoformat(),
            layout=layout,
            image=image,
            details=details,
            location_type=location_type,
            location_url=location_url,
            notes=notes,
        )

class SessionMetadata(BaseModel):
    """V3.5: Session-level metadata"""
    report_title: str = "Overlay Annotator Report"  # Editable report name
    description: str = ""  # Optional description
    created: str = ""
    last_modified: str = ""
    entry_count: int = 0
    
    @classmethod
    def new(cls, report_title: str = "Overlay Annotator Report"):
        now = datetime.now(timezone.utc).isoformat()
        return cls(
            report_title=report_title,
            created=now,
            last_modified=now,
            entry_count=0
        )

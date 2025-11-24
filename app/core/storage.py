
from pathlib import Path
import json
from datetime import datetime, timezone
from typing import List
from PIL import Image
from jinja2 import Environment, FileSystemLoader
from app.core.models import Entry

DEFAULT_REPORT_MD_J2 = '''# Overlay Annotator Session

{% for e in entries %}
## {{ e.title }}
Captured: {{ e.timestamp }}

| Screenshot | Notes |
|---|---|
| ![{{ e.title }}]({{ e.image.path }}) | {{ e.notes }} |

{% endfor %}
'''

class SessionStore:
    def __init__(self, session_root: Path):
        self.root = Path(session_root)
        self.images = self.root / "images"
        self.meta = self.root / "metadata"
        self.tpl_dir = self.root / "_templates"
        self.tpl_dir.mkdir(exist_ok=True)
        
        # Create default Markdown template
        default_md_tpl = self.tpl_dir / "report.md.j2"
        if not default_md_tpl.exists():
            default_md_tpl.write_text(DEFAULT_REPORT_MD_J2, encoding="utf-8")
        
        # Create default HTML template
        default_html_tpl = self.tpl_dir / "report.html.j2"
        if not default_html_tpl.exists():
            # Copy from package templates
            from pathlib import Path as P
            pkg_template = P(__file__).parent / "_templates" / "report.html.j2"
            if pkg_template.exists():
                default_html_tpl.write_text(pkg_template.read_text(encoding="utf-8"), encoding="utf-8")
            else:
                # Fallback: create minimal HTML template
                default_html_tpl.write_text(self._get_default_html_template(), encoding="utf-8")
        
        # V3.5: Initialize session metadata
        self.metadata = self.load_session_metadata()
    
    def load_session_metadata(self):
        """V3.5: Load session metadata"""
        from app.core.models import SessionMetadata
        metadata_file = self.meta / "session.json"
        if metadata_file.exists():
            try:
                data = json.loads(metadata_file.read_text(encoding="utf-8"))
                return SessionMetadata(**data)
            except:
                # Create default if loading fails
                return SessionMetadata.new()
        else:
            # Create default
            return SessionMetadata.new()
    
    def save_session_metadata(self, metadata=None):
        """V3.5: Save session metadata"""
        from app.core.models import SessionMetadata
        if metadata is None:
            metadata = self.metadata
        
        metadata.last_modified = datetime.now(timezone.utc).isoformat()
        self.meta.mkdir(exist_ok=True, parents=True)  # Ensure directory exists
        metadata_file = self.meta / "session.json"
        metadata_file.write_text(metadata.model_dump_json(indent=2), encoding="utf-8")
        self.metadata = metadata

    def save_image(self, pil: Image.Image) -> Path:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = self.images / f"entry_{ts}.jpg"
        self.images.mkdir(exist_ok=True, parents=True)
        pil.convert("RGB").save(path, "JPEG", quality=95, optimize=True, progressive=True)
        return path.relative_to(self.root)

    def save_entry(self, entry: Entry) -> None:
        self.meta.mkdir(exist_ok=True, parents=True)
        
        # V3.5.4: Auto-assign order if not set
        if entry.order == 0:
            entries = self.load_entries()
            max_order = max([e.order for e in entries], default=0)
            entry.order = max_order + 1
        
        path = self.meta / f"{entry.id}.json"
        try:
            data = entry.model_dump()
        except AttributeError:
            data = entry.dict()
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load_entries(self) -> List[Entry]:
        out: List[Entry] = []
        for p in sorted(self.meta.glob("*.json")):
            # Skip session.json (V3.5 metadata file)
            if p.name == "session.json":
                continue
            with open(p, "r", encoding="utf-8") as f:
                data = json.load(f)
                out.append(Entry(**data))
        
        # V3.5.4: Sort by order field (0 = use timestamp order)
        out.sort(key=lambda e: (e.order if e.order > 0 else 999999, e.timestamp))
        return out

    def export_markdown(self) -> Path:
        """Export session as Markdown (V3.5: with report_title)"""
        from datetime import datetime
        
        entries = self.load_entries()
        env = Environment(loader=FileSystemLoader(str(self.tpl_dir)), autoescape=False)
        tpl = env.get_template("report.md.j2")
        
        # Convert entries to dicts for template
        entries_dicts = [entry.model_dump() for entry in entries]
        
        md = tpl.render(
            entries=entries_dicts,
            report_title=self.metadata.report_title,
            export_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        out = self.root / "report.md"
        out.write_text(md, encoding="utf-8")
        return out
    def export_html(self) -> Path:
        """Export session as HTML with embedded base64 images (V3.5: with report_title)"""
        import base64
        from datetime import datetime
        
        entries = self.load_entries()
        
        # Convert entries to dicts and add base64 images
        entries_with_images = []
        for entry in entries:
            # Convert to dict
            entry_dict = entry.model_dump()
            
            # Add base64 image
            img_path = self.root / entry.image.path
            if img_path.exists():
                with open(img_path, 'rb') as f:
                    img_data = f.read()
                    entry_dict['image_base64'] = base64.b64encode(img_data).decode('utf-8')
            else:
                entry_dict['image_base64'] = None
            
            entries_with_images.append(entry_dict)
        
        env = Environment(loader=FileSystemLoader(str(self.tpl_dir)), autoescape=True)
        tpl = env.get_template("report.html.j2")
        html = tpl.render(
            entries=entries_with_images,
            session_name=self.root.name,
            report_title=self.metadata.report_title,
            export_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        out = self.root / "report.html"
        out.write_text(html, encoding="utf-8")
        return out
    
    def delete_entry(self, entry: Entry) -> None:
        """Delete an entry and its associated files (V3.5.4)
        
        Args:
            entry: Entry to delete
        """
        try:
            # Delete metadata file
            meta_file = self.meta / f"{entry.id}.json"
            if meta_file.exists():
                meta_file.unlink()
            
            # Delete image file
            image_path = self.root / entry.image.path
            if image_path.exists():
                image_path.unlink()
        except Exception as e:
            raise Exception(f"Failed to delete entry: {e}")
    
    def _get_default_html_template(self) -> str:
        """Fallback HTML template if package template not found"""
        return '''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>{{ session_name }}</title>
<style>body{font-family:sans-serif;padding:20px;background:#f5f5f5}
.entry{background:white;margin:20px 0;padding:20px;border-radius:8px}
img{max-width:100%;height:auto}</style></head><body>
<h1>{{ session_name }}</h1><p>Generated: {{ export_date }}</p>
{% for entry in entries %}
<div class="entry"><h2>{{ entry.title }}</h2>
<p>{{ entry.timestamp }}</p>
{% if entry.image_base64 %}<img src="data:image/jpeg;base64,{{ entry.image_base64 }}">{% endif %}
<p>{{ entry.notes }}</p></div>
{% endfor %}</body></html>'''

# Changelog

All notable changes to DocShot will be documented in this file.

## [3.5.3] - 2025-11-22

### Fixed
- Text annotation crash when clicking with text tool selected
- Image aspect ratio distortion in canvas display
- All BLUR tool references removed (tool was causing crashes)

### Improved
- Images now display with correct proportions and centering
- Text tool is now self-contained using QInputDialog
- Cleaner codebase with removed dead code

### Technical
- Added QInputDialog for text input instead of parent dependency
- Implemented aspect-ratio-preserving rectangle calculation
- Removed ImageFilter import and all blur-related code

## [3.5.2] - 2025-11-22

### Fixed
- Critical bug where `load_entries()` tried to load session.json as Entry object
- Application crash when saving entries
- Validation errors for Entry model

### Technical
- Added session.json exclusion in `load_entries()` method
- Ensured metadata directory creation before saving

## [3.5.1] - 2025-11-22

### Fixed
- Entry.new() backward compatibility with V3.4.x code
- Made new V3.5 structured fields optional with defaults

### Technical
- Changed Entry.new() signature to have default values
- Maintained 100% data compatibility with previous versions

## [3.5.0] - 2025-11-22

### Added
- Structured metadata fields (details, location_type, location_url)
- Real-time search across all entry fields
- Type filtering (Web, App, Mobile, Desktop, Other)
- Session statistics panel with entry counts
- Custom report naming
- Beautiful HTML export with gradient design
- Professional Markdown export templates
- Duration tracking
- Enhanced metadata system

### Changed
- Note fields split into structured sections
- Export templates completely redesigned
- Better organization and categorization

## [3.4.2] - Previous Version

### Core Features
- Screenshot capture with annotation
- Arrow, Box, Pen, and Blur tools
- Session management
- Markdown and HTML export
- Entry organization

---

## Version Naming

- **Major.Minor.Patch** (e.g., 3.5.3)
- **Major**: Breaking changes
- **Minor**: New features, backward compatible
- **Patch**: Bug fixes only

## Links

- [Repository](https://github.com/yourusername/docshot)
- [Issues](https://github.com/yourusername/docshot/issues)
- [Latest Release](https://github.com/yourusername/docshot/releases/latest)

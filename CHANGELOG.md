# Changelog

All notable changes to Subtitle Studio are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-02-10

### Added
- **Complete documentation suite**
  - `docs/user-guide.md` - Comprehensive user tutorial with examples
  - `CONTRIBUTING.md` - Developer guide with code standards and Blender 5.0 patterns
  - `docs/troubleshooting.md` - Common issues and detailed solutions
- **Documentation cross-linking** - All docs now include "Related" sections
- **UV-first dependency management** - Emphasized UV over pip throughout documentation
- **Blender 5.0 patterns documented**
  - Modal operators with threading
  - Sequence access patterns (`sequences` vs `sequences_all`)
  - Thread safety guidelines
- **Enhanced README.md**
  - Table of contents
  - Feature matrix
  - Quick reference tables
  - Badges and improved structure

### Changed
- Migrated to Blender Addon Framework for auto-loading and hot-reload
- Reorganized documentation structure (consolidated in `docs/`)
- Updated all documentation with "Last Updated: 2026-02-10" headers

### Removed
- **Deprecated `docs/changelog.md`** - Consolidated into root `CHANGELOG.md`
  - Duplicate changelog caused confusion
  - Root CHANGELOG.md is now the single source of truth

---

## [0.5.1] - 2026-02-08

### Added
- Documented UV-first dependency management and faster-whisper tuning references
- Added development workflow guidance for Blender iteration and UV commands

### Changed
- Reorganized the root `README.md` to reflect installation, UV dependency management, and documentation standards

### Fixed
- Clarified troubleshooting steps for add-on visibility and model downloads

### Removed
- Legacy Blender 3.x references were resolved in favor of Blender 4.5/5.0 guidance

---

## [0.1.0] - 2026-02-08

### Added
- Subtitle Studio branding and metadata updates
- Initial documentation updates (README and dev workflow)
- GPL-3.0-or-later license
- Attribution to the original Subtitle Editor project (https://github.com/tin2tin/Subtitle_Editor)
- Basic transcription with Faster Whisper integration
- Multi-format import/export (SRT, VTT, ASS, SSA)
- Speaker management with multi-channel support
- Style presets and batch styling
- Dependency management with UV and pip fallback
- Model download from Hugging Face
- GPU acceleration support (CUDA, ROCm, Metal)

### Changed
- Add-on display name updated to Subtitle Studio
- Module structure migrated to Blender Addon Framework

---

## Categories

Changes are categorized as:

- **Added** - New features
- **Changed** - Changes to existing functionality
- **Deprecated** - Soon-to-be removed features
- **Removed** - Removed features
- **Fixed** - Bug fixes
- **Security** - Security-related changes

---

## Related

- [README.md](README.md) - Project overview
- [ROADMAP.md](ROADMAP.md) - Future plans and milestones
- [docs/user-guide.md](docs/user-guide.md) - User documentation
- [CONTRIBUTING.md](CONTRIBUTING.md) - How to contribute

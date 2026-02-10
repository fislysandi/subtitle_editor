# Subtitle Studio

**Last Updated:** 2026-02-10

[![Blender](https://img.shields.io/badge/Blender-4.5%2B-orange)](https://www.blender.org/)
[![License](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)

AI-powered subtitle transcription and editing for Blender's Video Sequence Editor.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
- [Screenshots](#screenshots)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [Changelog](#changelog)
- [License](#license)

---

## Overview

**Subtitle Studio** brings AI transcription, subtitle editing, and multi-format export directly into Blender's Video Sequence Editor (VSE). Keep your entire workflow inside Blender while staying compliant with Blender 5.0+ UI paradigms.

### Why Subtitle Studio?

- **All-in-one workflow** - No need to switch between Blender and external tools
- **Offline AI transcription** - Run Whisper models locally without internet (after download)
- **Native Blender integration** - VSE-centric editing with frame-accurate controls
- **Multi-language support** - 99+ languages with auto-detection

---

## Features

| Feature | Description |
|---------|-------------|
| **AI Transcription** | Offline Faster Whisper inference with configurable models |
| **Multi-Language** | Auto-detect or force specific languages |
| **VSE Integration** | Frame-accurate editing inside Blender's sequencer |
| **Multi-Speaker** | Track multiple speakers on separate channels |
| **Import/Export** | SRT, VTT, ASS, SSA format support |
| **Style Presets** | Font, color, positioning controls |
| **Offline Ready** | Bundle dependencies for air-gapped installs |

### Supported Models

| Model | Size | Speed | Best For |
|-------|------|-------|----------|
| `tiny` | 39 MB | Very Fast | Testing |
| `base` | 74 MB | Fast | Quick drafts |
| `small` | 244 MB | Moderate | Balanced workflow |
| `medium` | 769 MB | Slow | High accuracy |
| `large-v3` | 1.5 GB | Very Slow | Best quality |

---

## Requirements

- **Blender** 4.5 LTS or 5.0+
- **Python** 3.11 (bundled with Blender)
- **Disk Space** ~500 MB for dependencies
- **GPU** (Optional) CUDA/ROCm/Metal for faster transcription

---

## Installation

### 1. Download

Download the latest release ZIP from the [releases page](../../releases).

### 2. Install in Blender

```
Edit → Preferences → Add-ons → Install...
Select subtitle_studio.zip
Enable ✅ Subtitle Studio
```

### 3. Install Dependencies

```
Click arrow to expand Subtitle Studio in add-ons list
Click Install Dependencies button
Wait for completion (2-5 minutes)
```

### 4. Install PyTorch (GPU Support)

```
In Subtitle Studio panel:
Select your GPU backend (CUDA/Metal/CPU)
Click Install PyTorch
```

**See [docs/dependencies.md](docs/dependencies.md)** for detailed dependency management and UV workflow.

---

## Quick Start

### Transcribe Audio to Subtitles

```
1. Open Video Sequence Editor
2. Add your audio/video strip
3. Select the strip
4. Open Sidebar (N key) → Subtitle Studio tab
5. Click Transcribe Audio
6. Edit subtitles in the list view
```

### Import Existing Subtitles

```
1. Click Import button in subtitle list
2. Select SRT/VTT/ASS file
3. Subtitles appear on designated channel
```

### Export Subtitles

```
1. Click Export button
2. Choose format (SRT/VTT/ASS)
3. Save file
```

**See [docs/user-guide.md](docs/user-guide.md)** for the complete tutorial.

---

## Documentation

| Document | Description |
|----------|-------------|
| [docs/user-guide.md](docs/user-guide.md) | Complete user tutorial with examples |
| [docs/whisper-config.md](docs/whisper-config.md) | Model selection & parameter reference |
| [docs/dependencies.md](docs/dependencies.md) | Dependency management & UV workflow |
| [docs/troubleshooting.md](docs/troubleshooting.md) | Common issues & solutions |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Developer guide & code standards |
| [docs/dev.md](docs/dev.md) | Development workflow & Blender iteration |

---

## Screenshots

*Screenshots will be added in a future update. See [ROADMAP.md](ROADMAP.md) Milestone 1.*

<!-- 
TODO: Add screenshots showing:
- Main panel in VSE sidebar
- Transcription in progress
- Subtitle list view
- Style editing section
-->

---

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Add-on not visible | Restart Blender after installation |
| Dependencies fail | Check internet; try UV fallback in preferences |
| Model download fails | Set Hugging Face token in preferences |
| No subtitles created | Select audio/video strip first |

**See [docs/troubleshooting.md](docs/troubleshooting.md)** for detailed solutions.

---

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:

- Development setup
- Code standards (Google-style docstrings, type hints)
- Blender 5.0 patterns (modal operators, thread safety)
- Testing guidelines
- Pull request process

### Quick Commands

```bash
# Run tests
uv run test subtitle_editor

# Build release
uv run release subtitle_editor

# Sync dependencies
uv sync
```

---

## Changelog

### [1.0.0] - 2026-02-10

#### Added
- Complete documentation suite (user guide, troubleshooting, contributing)
- Cross-linked all documentation
- UV-first dependency management
- Blender 5.0 modal operator patterns
- Thread-safe transcription with progress tracking

#### Changed
- Migrated to Blender Addon Framework
- Reorganized documentation structure

### [0.5.1] - 2026-02-08

#### Added
- UV-first dependency management
- Faster Whisper tuning references
- Development workflow documentation

**See [CHANGELOG.md](CHANGELOG.md)** for full history.

---

## License

GPL-3.0-or-later. See [LICENSE](LICENSE) for full terms.

---

## Acknowledgments

- Original concept by [tin2tin/Subtitle_Editor](https://github.com/tin2tin/Subtitle_Editor)
- Powered by [Faster Whisper](https://github.com/SYSTRAN/faster-whisper)
- Built with [Blender](https://www.blender.org/)

---

## Related

- [docs/user-guide.md](docs/user-guide.md) - Complete user tutorial
- [docs/whisper-config.md](docs/whisper-config.md) - Model configuration
- [CONTRIBUTING.md](CONTRIBUTING.md) - Developer guide
- [ROADMAP.md](ROADMAP.md) - Future plans & milestones

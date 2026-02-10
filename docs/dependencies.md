# Subtitle Studio - Dependency Management (UV First)

**Last Updated:** 2026-02-10

## Overview

Subtitle Studio no longer ships a bundled `libs/` folder. Dependencies are managed with UV and installed into Blender's Python at runtime, with pip fallback when UV is unavailable.

## Core Workflow

### 1. Verify Project Dependencies

Update the dependency list and version ranges in `pyproject.toml`, then refresh `uv.lock`:

```bash
uv lock --upgrade
uv sync
```

Commit `pyproject.toml` and `uv.lock` whenever dependency versions change.

### 2. Install Dependencies in Blender

Use the add-on Preferences panel:

- Click **Install Dependencies** to bootstrap UV (if needed) and install required packages.
- If UV cannot be bootstrapped, the installer falls back to pip.
- Progress is shown in Blender's status area and the system console.

### 3. Verify Runtime Installation

From the VSE panel, click **Check Dependencies** to confirm:

- `faster_whisper`
- `pysubs2`
- `onnxruntime`
- `torch` (optional, installed via the PyTorch button)

## Recommended Commands (Dev)

```bash
uv sync
uv run test subtitle_editor
uv run release subtitle_editor
```

## Version Pinning

Keep ranges compatible with Blender's embedded Python (3.11):

```toml
[project]
dependencies = [
    "faster-whisper>=1.0.3,<2.0.0",
    "pysubs2>=1.8.0,<2.0.0",
    "onnxruntime>=1.24.1,<2.0.0",
]
```

## Troubleshooting

- **UV not found**: Re-run **Install Dependencies** so the add-on can fall back to pip if UV cannot be bootstrapped.
- **Install fails**: Check the Blender system console for the exact command and error output.
- **No module found**: Run **Install Dependencies** again and re-check.

## Related

- [README.md](../README.md) - Installation and quick start
- [docs/dev.md](dev.md) - Developer workflow
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Detailed developer guide with code standards
- [docs/troubleshooting.md](troubleshooting.md) - Dependency-related troubleshooting
- [docs/whisper-config.md](whisper-config.md) - Model configuration reference

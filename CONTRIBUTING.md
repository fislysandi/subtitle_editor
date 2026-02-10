# Contributing to Subtitle Studio

**Last Updated:** 2026-02-10

Thank you for your interest in contributing to Subtitle Studio! This guide covers the development workflow, code standards, and how to submit contributions.

---

## Table of Contents

1. [Development Setup](#development-setup)
2. [Project Structure](#project-structure)
3. [Development Workflow](#development-workflow)
4. [Code Standards](#code-standards)
5. [Blender 5.0 Patterns](#blender-50-patterns)
6. [Testing](#testing)
7. [Submitting Changes](#submitting-changes)

---

## Development Setup

### Prerequisites

```bash
# Required
- Blender 4.5 LTS or 5.0+
- Python 3.11 (bundled with Blender)
- UV package manager (recommended)
- Git

# Optional but recommended
- GPU for testing transcription
- Visual Studio Code with Python extension
```

### Install UV

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Verify
uv --version
```

### Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd subtitle_editor

# Sync dependencies with UV
uv sync

# Verify installation
uv run test subtitle_editor
```

---

## Project Structure

```
subtitle_editor/
├── __init__.py              # Add-on entry point, registration
├── config.py                # Add-on identifier constants
├── constants.py             # Language codes, model configs
├── props.py                 # Property groups (bpy.props)
├── core/                    # Core business logic
│   ├── transcriber.py       # Faster Whisper wrapper
│   ├── subtitle_io.py       # SRT/VTT/ASS import/export
│   ├── dependency_manager.py
│   └── download_manager.py
├── operators/               # Blender operators
│   ├── ops_transcribe.py    # Modal transcription operators
│   ├── ops_import_export.py
│   ├── ops_strip_edit.py    # Strip manipulation
│   ├── ops_dependencies.py
│   └── ops_model_download.py
├── panels/                  # UI panels
│   ├── main_panel.py        # Main VSE panel
│   └── list_view.py         # Subtitle list UIList
├── utils/                   # Utility functions
│   ├── sequence_utils.py    # VSE sequence helpers
│   └── file_utils.py
├── tests/                   # Unit tests
│   └── test_basic.py
└── i18n/                    # Translations
    └── dictionary.py
```

---

## Development Workflow

### Live Development

For rapid iteration, install the add-on as a symbolic link:

```bash
# Find Blender's add-ons directory
# Linux: ~/.config/blender/4.5/scripts/addons/
# macOS: ~/Library/Application Support/Blender/4.5/scripts/addons/
# Windows: %APPDATA%\Blender Foundation\Blender\4.5\scripts\addons\

# Create symlink (Linux/macOS)
ln -s /path/to/subtitle_editor ~/.config/blender/4.5/scripts/addons/subtitle_editor

# Windows (run as Administrator)
mklink /J "%APPDATA%\Blender Foundation\Blender\4.5\scripts\addons\subtitle_editor" "C:\path\to\subtitle_editor"
```

### Reload Changes

After editing code:

1. In Blender's **Scripting** workspace
2. Click **Reload Scripts** button (or press `F8`)
3. Or use: `Text → Run Script` for quick tests

### Common Commands

```bash
# Run tests
uv run test subtitle_editor

# Build release ZIP
uv run release subtitle_editor

# List add-on dependencies
uv run addon-deps list subtitle_editor

# Sync dependencies
uv run addon-deps sync subtitle_editor
```

---

## Code Standards

### Google-Style Docstrings

```python
"""
Brief description of function/class.

Longer description if needed, explaining behavior,
side effects, and usage patterns.

Args:
    context: Blender context object
    scene: Target scene for operation
    segments: List of transcription segments
    config: Configuration dictionary with keys:
        - subtitle_channel: Target channel number
        - render_fps: Scene frame rate

Returns:
    The created text strip or None if creation failed.

Raises:
    ValueError: If segments is empty or config invalid.

Example:
    >>> strip = create_subtitle_strip(
    ...     scene, 
    ...     segments, 
    ...     {"subtitle_channel": 3, "render_fps": 24.0}
    ... )
    >>> strip.name
    'Subtitle_001'
"""
```

### Type Hints

Use Python type hints for all function signatures:

```python
from typing import Optional, List, Dict, Any
from bpy.types import Scene

def create_text_strip(
    scene: Scene,
    name: str,
    text: str,
    frame_start: int,
    frame_end: int,
    channel: int = 3
) -> Optional[Any]:
    """Create a text strip in the sequencer."""
    ...

def transcribe_audio(
    filepath: str,
    language: Optional[str] = None,
    config: Dict[str, Any] = {}
) -> List[TranscriptionSegment]:
    """Transcribe audio file to segments."""
    ...
```

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Classes | PascalCase | `SubtitleEditorProperties` |
| Functions | snake_case | `create_text_strip()` |
| Constants | UPPER_CASE | `DEFAULT_BEAM_SIZE` |
| Private | _leading_underscore | `_validate_filepath()` |
| Operators | SUBTITLE_OT_* | `SUBTITLE_OT_transcribe` |
| Panels | SEQUENCER_PT_* | `SEQUENCER_PT_panel` |

---

## Blender 5.0 Patterns

### Sequence Access Pattern

Blender 5.0 uses `sequences` instead of deprecated `sequences_all`:

```python
# ✅ Correct (Blender 5.0)
sequences = scene.sequence_editor.sequences

# ❌ Deprecated
sequences = scene.sequence_editor.sequences_all
```

Safe access with fallback:

```python
def _get_sequence_collection(scene):
    """Get sequences collection, handling API differences."""
    if not scene.sequence_editor:
        return None
    
    seq_editor = scene.sequence_editor
    for attr in ("sequences", "sequences_all", "strips"):
        sequences = getattr(seq_editor, attr, None)
        if sequences is not None:
            return sequences
    return None
```

### Modal Operators for Long-Running Tasks

Use modal operators with timers for background tasks:

```python
class SUBTITLE_OT_transcribe(Operator):
    """Transcribe audio with progress updates."""
    
    bl_idname = "subtitle.transcribe"
    bl_label = "Transcribe"
    bl_options = {"REGISTER", "UNDO"}
    
    _timer: Optional[bpy.types.Timer] = None
    _thread: Optional[threading.Thread] = None
    _queue: Optional[queue.Queue] = None
    
    def invoke(self, context, event):
        # Setup
        self._queue = queue.Queue()
        self._thread = threading.Thread(
            target=self._worker,
            args=(config, self._queue),
            daemon=True,
        )
        self._thread.start()
        
        # Add timer for UI updates
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.1, window=context.window)
        wm.modal_handler_add(self)
        
        return {"RUNNING_MODAL"}
    
    def modal(self, context, event):
        if event.type == "ESC":
            self._cancel(context)
            return {"CANCELLED"}
        
        if event.type == "TIMER":
            self._drain_queue(context)
            
            if self._finished:
                self._finalize(context)
                return {"FINISHED"}
            
            # Force UI redraw
            for area in context.screen.areas:
                area.tag_redraw()
        
        return {"PASS_THROUGH"}
    
    def _drain_queue(self, context):
        """Process messages from worker thread."""
        while True:
            try:
                msg = self._queue.get_nowait()
            except queue.Empty:
                break
            
            if msg.get("type") == "progress":
                props.progress = msg.get("progress", 0.0)
                props.progress_text = msg.get("text", "")
            elif msg.get("type") == "complete":
                self._segments = msg.get("segments", [])
                self._finished = True
```

### Thread Safety Rules

**NEVER** modify Blender data from background threads:

```python
# ✅ CORRECT: Use queue + timer
# Worker thread
out_queue.put({"type": "progress", "value": 0.5})

# Main thread (in modal/timer)
progress = queue.get()
props.value = progress  # Safe - running on main thread

# ❌ WRONG: Direct modification from thread
# Worker thread
def bad_worker():
    props.value = 0.5  # CRASH! Blender not thread-safe
```

### Property Groups

Define properties in `props.py`:

```python
class SubtitleEditorProperties(PropertyGroup):
    """Main properties for Subtitle Studio."""
    
    language: EnumProperty(
        name="Language",
        description="Language for transcription",
        items=LANGUAGE_ITEMS,
        default="auto",
    )
    
    is_transcribing: BoolProperty(
        name="Is Transcribing",
        default=False,
    )
    
    progress: FloatProperty(
        name="Progress",
        min=0.0,
        max=1.0,
        default=0.0,
        subtype="PERCENTAGE",
    )
```

Register in `__init__.py`:

```python
from .props import SubtitleEditorProperties

_addon_properties = {
    bpy.types.Scene: {
        "subtitle_editor": PointerProperty(type=SubtitleEditorProperties),
    }
}

def register():
    add_properties(_addon_properties)

def unregister():
    remove_properties(_addon_properties)
```

---

## Testing

### Running Tests

```bash
# Run all tests
uv run test subtitle_editor

# Run specific test file
python -m pytest tests/test_basic.py -v
```

### Writing Tests

```python
import unittest
from ..core.subtitle_io import SubtitleIO, SubtitleEntry

class TestSubtitleIO(unittest.TestCase):
    """Test subtitle import/export functionality."""
    
    def test_srt_parsing(self):
        """Test SRT file parsing."""
        entry = SubtitleEntry(
            index=1,
            start=0.0,
            end=5.0,
            text="Hello World"
        )
        
        self.assertEqual(entry.index, 1)
        self.assertEqual(entry.text, "Hello World")
        self.assertEqual(entry.duration, 5.0)
    
    def test_round_trip(self):
        """Test import → export preserves data."""
        entries = [
            SubtitleEntry(1, 0.0, 3.0, "First"),
            SubtitleEntry(2, 3.5, 6.0, "Second"),
        ]
        
        # Export to temp file
        temp_path = "/tmp/test.srt"
        SubtitleIO.save(temp_path, entries, ".srt")
        
        # Import and verify
        loaded = SubtitleIO.load(temp_path)
        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[0].text, "First")
```

### Manual Testing Checklist

- [ ] Install add-on in fresh Blender
- [ ] Install dependencies
- [ ] Download a model
- [ ] Transcribe a test audio file
- [ ] Edit subtitle text
- [ ] Nudge timing
- [ ] Import SRT file
- [ ] Export SRT file
- [ ] Verify round-trip accuracy

---

## Submitting Changes

### Before Submitting

1. Run all tests: `uv run test subtitle_editor`
2. Test in Blender manually
3. Update documentation if needed
4. Add entry to `CHANGELOG.md`

### Commit Message Format

```
type(scope): brief description

Longer description if needed. Explain what changed and why.

Fixes #123
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style (formatting)
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Build/process changes

Examples:
```
feat(transcription): add VAD filter support

Add voice activity detection to filter out non-speech
segments during transcription. Improves accuracy for
noisy audio.

Fixes #45
```

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Manual testing completed
- [ ] Tested in Blender 5.0

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
```

---

## Related Documentation

- [README.md](../README.md) - Project overview
- [docs/dev.md](dev.md) - Development workflow
- [docs/user-guide.md](user-guide.md) - User documentation
- [docs/whisper-config.md](whisper-config.md) - Model configuration
- [docs/troubleshooting.md](troubleshooting.md) - Common issues

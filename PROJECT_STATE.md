# Subtitle Editor - Project State

**Last Updated:** 2025-02-07  
**Addon Location:** `addons/subtitle_editor/`

## 📍 Current Status

**Status:** ✅ Migrated to Blender Addon Framework  
**Git Branch:** master  
**Framework Version:** Using auto-loading + UV dependency management

## 🎬 About This Addon

**Subtitle Editor** - AI-powered subtitle transcription and editing for Blender Video Sequence Editor (VSE)

**Forked from:** https://github.com/tin2tin/Subtitle_Editor  
**Original Author:** tin2tin

### Features
- 🤖 **AI Transcription** using Faster Whisper
- 📝 **Subtitle editing** with list-based UI
- 🌍 **Multi-language support**
- 📥 **Import/Export** (SRT, VTT, ASS formats)
- 🔥 **Hot-reload** during development

## ✅ Completed Migration Tasks

### Phase 1: UV Setup ✓
- [x] Initialized UV for dependency management
- [x] Added `pyproject.toml` with dependencies:
  - faster-whisper>=1.0.0
  - pysubs2>=1.8.0
  - onnxruntime>=1.24.1
- [x] Generated `uv.lock` file

### Phase 2: Framework Integration ✓
- [x] Created `config.py` with `__addon_name__ = "subtitle_editor"`
- [x] Created `i18n/` folder for translations
- [x] Created `panels/` folder for UI (framework convention)
- [x] Removed manual registration from all modules
- [x] Framework auto-load discovers all classes

### Phase 3: Code Updates ✓
- [x] Updated `__init__.py` to use framework's auto_load
- [x] Removed `core/dependencies.py` (replaced by UV)
- [x] Updated imports in operators
- [x] Fixed EnumProperty with LANGUAGE_ITEMS from constants
- [x] Removed duplicate UI files

### Phase 4: UI Alignment ✓
- [x] Panels match upstream layout style:
  - SEQUENCER_PT_panel (main panel with UIList)
  - SEQUENCER_PT_whisper_panel (transcription settings)
  - SEQUENCER_PT_edit_panel (subtitle editing)
- [x] UIList displays subtitle text
- [x] Category: "Subtitle Editor"

## 🚀 Available Commands

```bash
# Test with hot reload (auto-updates in Blender on save)
uv run test subtitle_editor

# Package for distribution
uv run release subtitle_editor

# Manage dependencies
uv run addon-deps list subtitle_editor
uv run addon-deps sync subtitle_editor
uv run addon-deps add subtitle_editor <package>
```

## 📁 File Structure

```
subtitle_editor/
├── __init__.py              # Framework auto-load integration
├── config.py                # Addon name config
├── constants.py             # Language & model constants
├── blender_manifest.toml    # Blender extension manifest
├── props.py                 # Property groups (SubtitleEditorProperties, TextStripItem)
├── pyproject.toml           # UV dependencies
├── uv.lock                  # Locked dependencies
├── .venv/                   # Isolated Python environment
│
├── core/                    # Core functionality
│   ├── __init__.py
│   ├── subtitle_io.py       # Import/export logic
│   └── transcriber.py       # Whisper transcription
│
├── operators/               # Blender operators (auto-registered)
│   ├── __init__.py
│   ├── ops_import_export.py # Import/export operators
│   ├── ops_strip_edit.py    # List edit operators
│   └── ops_transcribe.py    # Transcription operator
│
├── panels/                  # UI panels (framework convention)
│   ├── __init__.py
│   ├── main_panel.py        # Main panels
│   └── list_view.py         # UIList
│
├── ui/                      # Legacy folder (kept empty)
│   └── __init__.py
│
├── utils/                   # Utilities
│   ├── __init__.py
│   ├── file_utils.py        # File operations
│   └── sequence_utils.py    # VSE operations
│
├── i18n/                    # Translations
│   ├── __init__.py
│   └── dictionary.py
│
└── tests/                   # Test suite
    ├── __init__.py
    └── test_basic.py
```

## 🔧 Key Classes & Operators

### Property Groups
- `SubtitleEditorProperties` - Main addon properties (model, device, language, etc.)
- `TextStripItem` - Individual subtitle item in the list

### Operators
- `subtitle.transcribe` - Transcribe audio to subtitles
- `subtitle.import_subtitles` - Import subtitle files
- `subtitle.export_subtitles` - Export subtitle files
- `subtitle.refresh_list` - Refresh subtitle list
- `subtitle.select_strip` - Select strip from list
- `subtitle.update_text` - Update subtitle text

### Panels
- `SEQUENCER_PT_panel` - Main panel with UIList
- `SEQUENCER_PT_whisper_panel` - Transcription settings
- `SEQUENCER_PT_edit_panel` - Subtitle editing

### UIList
- `SEQUENCER_UL_List` - Displays text strips

## 📝 Properties Available

**Scene Properties:**
- `scene.subtitle_editor` (SubtitleEditorProperties)
- `scene.text_strip_items` (Collection of TextStripItem)
- `scene.text_strip_items_index` (Int)

**SubtitleEditorProperties:**
- `language` - Transcription language
- `model` - Whisper model (tiny, base, small, medium, large-v3)
- `device` - Compute device (auto, cpu, cuda)
- `translate` - Translate to English
- `word_timestamps` - Word-level timestamps
- `vad_filter` - Voice activity detection
- `show_advanced` - Show advanced options
- `is_transcribing` - Transcription in progress
- `progress` - Progress (0-1)
- `progress_text` - Status text
- `current_text` - Currently editing text

## 🐛 Known Issues / TODO

- [ ] Add progress callback during transcription
- [ ] Implement batch styling (copy style to selected)
- [ ] Add line break insertion
- [ ] Test all import/export formats
- [ ] Add file browser panels for import/export
- [ ] Optimize transcription performance

## 🔄 To Resume Work

**In a new chat, say:**
> "Load from PROJECT_STATE.md in subtitle_editor addon and continue"

Or navigate to addon and:
```bash
cd addons/subtitle_editor
cat PROJECT_STATE.md
```

## 📝 Recent Changes

1. **UI Update** - Matched upstream tin2tin layout style
2. **Framework Migration** - Migrated to auto-load system
3. **UV Integration** - Dependency management via UV
4. **Bug Fixes** - Fixed EnumProperty, removed duplicates

## 💡 For AI Assistant

**When working on this addon:**

1. **Check current state** - Read this file first
2. **Understand structure** - Files are in `panels/`, `operators/`, `core/`, etc.
3. **Framework rules** - Uses auto_load, no manual registration needed
4. **Test frequently** - Use `uv run test subtitle_editor` for hot-reload

**What can be modified:**
- ✅ Operators in `operators/`
- ✅ UI in `panels/`
- ✅ Core logic in `core/`
- ✅ Properties in `props.py`
- ✅ Constants in `constants.py`

**What needs care:**
- ⚠️ `__init__.py` - Framework integration point
- ⚠️ `config.py` - Addon identifier
- ⚠️ `blender_manifest.toml` - Blender metadata

## 📊 Quick Stats

- **Total Files:** 28
- **Operators:** 6
- **Panels:** 3
- **Property Groups:** 2
- **Dependencies:** 3 (faster-whisper, pysubs2, onnxruntime)
- **Lines of Code:** ~2000+

## 🔗 Important Links

- **Upstream Repo:** https://github.com/tin2tin/Subtitle_Editor
- **Faster Whisper:** https://github.com/SYSTRAN/faster-whisper
- **Framework Docs:** See main repo README.md

---

**Current context loaded:** ✅ Subtitle Editor with Framework Integration

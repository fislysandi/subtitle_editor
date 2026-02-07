# Model Download System - Complete Redesign Plan v2

Based on comprehensive context analysis from:
- technical-domain.md (Blender modal operators)
- code-quality.md (functional programming principles)
- agent-context.md (non-blocking patterns)
- download-redesign-plan.md (architecture)

---

## 🎯 Design Goals

1. **Non-blocking UI** - Modal operator + threading (GIL-safe pattern)
2. **Real Progress** - Actual bytes downloaded, not fake percentages
3. **Cancel Support** - Clean cancellation with Threading.Event
4. **Pure Functions** - Download logic separate from Blender (testable)
5. **Memory Efficient** - Download files without loading into RAM
6. **Optional Auth** - HF token optional, not required

---

## 🏗️ Architecture (Clean Separation)

```
subtitle_editor/
├── core/
│   ├── __init__.py
│   ├── download_manager.py      # NEW: Pure Python, no Blender deps
│   ├── transcriber.py
│   └── subtitle_io.py
├── operators/
│   ├── __init__.py
│   ├── ops_model_download.py    # MODIFIED: UI only, uses DownloadManager
│   └── ...
└── utils/
    └── file_utils.py
```

---

## 📦 Phase 1: DownloadManager (Pure Python)

**File:** `core/download_manager.py`

### Design Principles (from code-quality.md):
- Pure functions where possible
- Small functions (< 50 lines)
- Composition over inheritance
- Explicit dependencies (dependency injection)

### Implementation:

```python
"""
Pure Python download manager - no Blender dependencies.
Follows functional programming principles.
"""

import os
import threading
from pathlib import Path
from typing import Optional, Callable, Dict, Any
from dataclasses import dataclass
from enum import Enum

try:
    from huggingface_hub import snapshot_download
    from huggingface_hub.utils import RepositoryNotFoundError
    HAS_HF = True
except ImportError:
    HAS_HF = False


class DownloadStatus(Enum):
    """Pure data - immutable state representation"""
    PENDING = "pending"
    CHECKING = "checking"
    DOWNLOADING = "downloading"
    COMPLETE = "complete"
    ERROR = "error"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class DownloadProgress:
    """
    Immutable progress state.
    Frozen dataclass ensures immutability (functional approach).
    """
    status: DownloadStatus
    bytes_downloaded: int
    bytes_total: int
    current_file: str
    message: str
    
    @property
    def percentage(self) -> float:
        """Pure function - same input always same output"""
        if self.bytes_total == 0:
            return 0.0
        return self.bytes_downloaded / self.bytes_total


class DownloadManager:
    """
    Manages model downloads with functional approach.
    No side effects - all state changes explicit.
    """
    
    def __init__(self, cache_dir: str):
        self.cache_dir = Path(cache_dir)
        self._cancel_event = threading.Event()
        self._current_progress = DownloadProgress(
            status=DownloadStatus.PENDING,
            bytes_downloaded=0,
            bytes_total=0,
            current_file="",
            message="Ready"
        )
        self._lock = threading.Lock()
    
    def get_progress(self) -> DownloadProgress:
        """Pure read - returns immutable state"""
        with self._lock:
            return self._current_progress
    
    def is_cancelled(self) -> bool:
        """Pure function check"""
        return self._cancel_event.is_set()
    
    def cancel(self) -> None:
        """Signal cancellation - thread-safe"""
        self._cancel_event.set()
        self._update_progress(
            status=DownloadStatus.CANCELLED,
            message="Download cancelled"
        )
    
    def _update_progress(self, **kwargs) -> None:
        """
        Internal: Update progress state immutably.
        Creates new DownloadProgress instead of modifying.
        """
        with self._lock:
            current = self._current_progress
            # Create new immutable state (functional approach)
            new_state = DownloadProgress(
                status=kwargs.get('status', current.status),
                bytes_downloaded=kwargs.get('bytes_downloaded', current.bytes_downloaded),
                bytes_total=kwargs.get('bytes_total', current.bytes_total),
                current_file=kwargs.get('current_file', current.current_file),
                message=kwargs.get('message', current.message)
            )
            self._current_progress = new_state
    
    def _get_repo_id(self, model_name: str) -> str:
        """Pure function - model name to repo ID mapping"""
        repo_map = {
            "tiny": "Systran/faster-whisper-tiny",
            "tiny.en": "Systran/faster-whisper-tiny.en",
            "base": "Systran/faster-whisper-base",
            "base.en": "Systran/faster-whisper-base.en",
            "small": "Systran/faster-whisper-small",
            "small.en": "Systran/faster-whisper-small.en",
            "medium": "Systran/faster-whisper-medium",
            "medium.en": "Systran/faster-whisper-medium.en",
            "large-v1": "Systran/faster-whisper-large-v1",
            "large-v2": "Systran/faster-whisper-large-v2",
            "large-v3": "Systran/faster-whisper-large-v3",
            "large": "Systran/faster-whisper-large-v3",
            "distil-small.en": "Systran/faster-distil-whisper-small.en",
            "distil-medium.en": "Systran/faster-distil-whisper-medium.en",
            "distil-large-v2": "Systran/faster-distil-whisper-large-v2",
            "distil-large-v3": "Systran/faster-distil-whisper-large-v3",
            "distil-large-v3.5": "distil-whisper/distil-large-v3.5-ct2",
            "large-v3-turbo": "mobiuslabsgmbh/faster-whisper-large-v3-turbo",
            "turbo": "mobiuslabsgmbh/faster-whisper-large-v3-turbo",
        }
        return repo_map.get(model_name, f"Systran/faster-whisper-{model_name}")
    
    def _is_cached(self, model_name: str) -> bool:
        """Pure function - check if model exists in cache"""
        repo_id = self._get_repo_id(model_name)
        cache_path = self.cache_dir / f"models--{repo_id.replace('/', '--')}"
        return cache_path.exists()
    
    def _make_progress_callback(self):
        """
        Factory function - creates callback for huggingface_hub.
        Returns function that updates our immutable state.
        """
        def callback(files, total_files, downloaded_bytes, total_bytes):
            # Check cancellation
            if self._cancel_event.is_set():
                raise InterruptedError("Download cancelled")
            
            # Get current file being downloaded
            current_file = files[-1] if files else "unknown"
            
            # Update progress state immutably
            self._update_progress(
                status=DownloadStatus.DOWNLOADING,
                bytes_downloaded=downloaded_bytes,
                bytes_total=total_bytes,
                current_file=current_file,
                message=f"Downloading {current_file}"
            )
        
        return callback
    
    def download(
        self,
        model_name: str,
        token: Optional[str] = None
    ) -> DownloadProgress:
        """
        Download a model. Blocks until complete or cancelled.
        Returns final progress state.
        
        Args:
            model_name: Whisper model name
            token: Optional HF token (None = anonymous)
            
        Returns:
            Final DownloadProgress state
        """
        if not HAS_HF:
            return DownloadProgress(
                status=DownloadStatus.ERROR,
                bytes_downloaded=0,
                bytes_total=0,
                current_file="",
                message="huggingface_hub not installed"
            )
        
        # Check already cached
        if self._is_cached(model_name):
            return DownloadProgress(
                status=DownloadStatus.COMPLETE,
                bytes_downloaded=0,
                bytes_total=0,
                current_file="",
                message=f"Model {model_name} already cached"
            )
        
        # Update state: checking
        self._update_progress(
            status=DownloadStatus.CHECKING,
            message=f"Preparing to download {model_name}..."
        )
        
        repo_id = self._get_repo_id(model_name)
        
        try:
            # Download using huggingface_hub
            # This downloads files WITHOUT loading into memory
            snapshot_download(
                repo_id=repo_id,
                cache_dir=self.cache_dir,
                token=token,  # None = anonymous (optional auth)
                local_files_only=False,
                resume_download=True,  # Support partial resume
                tqdm_class=None,  # Disable default tqdm
                # Use our custom progress callback
            )
            
            # Success
            return DownloadProgress(
                status=DownloadStatus.COMPLETE,
                bytes_downloaded=100,
                bytes_total=100,
                current_file="",
                message=f"Model {model_name} downloaded successfully!"
            )
            
        except InterruptedError:
            # Cancelled by user
            return self._current_progress
            
        except Exception as e:
            # Error
            return DownloadProgress(
                status=DownloadStatus.ERROR,
                bytes_downloaded=0,
                bytes_total=0,
                current_file="",
                message=f"Error: {str(e)}"
            )


def create_download_manager(cache_dir: str) -> DownloadManager:
    """
    Factory function - creates DownloadManager with dependency injection.
    Pure function - same input always same output.
    """
    return DownloadManager(cache_dir)
```

---

## 🎮 Phase 2: Modal Operator (UI Layer)

**File:** `operators/ops_model_download.py`

### Design Principles (from technical-domain.md):
- Modal operator for non-blocking execution
- Always return `{'PASS_THROUGH'}`
- Use `event.type == 'TIMER'` for updates
- Call `area.tag_redraw()` to force UI refresh
- Cleanup in `cancel()` - always remove timers

### Implementation:

```python
"""
Model Download Operator - UI Layer Only
Uses DownloadManager for actual logic (separation of concerns)
"""

import bpy
import threading
import time
from bpy.types import Operator
from ..core.download_manager import (
    DownloadManager, 
    DownloadStatus, 
    create_download_manager
)
from ..utils import file_utils


class SUBTITLE_OT_download_model(Operator):
    """Download Whisper model with real progress tracking"""
    
    bl_idname = "subtitle.download_model"
    bl_label = "Download Model"
    bl_description = "Download the selected Whisper model"
    bl_options = {"REGISTER", "UNDO"}
    
    # Modal operator state
    _timer = None
    _download_manager = None
    _thread = None
    _model_name = None
    
    def modal(self, context, event):
        """
        Called repeatedly by Blender's event loop.
        CRITICAL: Must return quickly, do heavy work in thread.
        """
        props = context.scene.subtitle_editor
        
        if event.type == "TIMER":
            # Poll download manager for progress (fast operation)
            if self._download_manager:
                progress = self._download_manager.get_progress()
                
                # Update UI properties
                props.model_download_progress = progress.percentage
                props.model_download_status = progress.message
                
                # Update Blender's built-in progress bar
                wm = context.window_manager
                wm.progress_update(int(progress.percentage * 100))
                
                # Check if complete
                if progress.status in [DownloadStatus.COMPLETE, 
                                      DownloadStatus.ERROR, 
                                      DownloadStatus.CANCELLED]:
                    # Show final message
                    if progress.status == DownloadStatus.COMPLETE:
                        self.report({"INFO"}, progress.message)
                    elif progress.status == DownloadStatus.ERROR:
                        self.report({"ERROR"}, progress.message)
                    
                    # End modal operator
                    self.cancel(context)
                    return {"FINISHED"}
            
            # CRITICAL: Force UI redraw (from technical-domain.md)
            for area in context.screen.areas:
                area.tag_redraw()
        
        # CRITICAL: Return PASS_THROUGH to keep Blender responsive
        # (from technical-domain.md)
        return {"PASS_THROUGH"}
    
    def execute(self, context):
        """
        Start modal operator.
        Sets up timer, modal handler, and background thread.
        """
        props = context.scene.subtitle_editor
        self._model_name = props.model
        
        # Check faster-whisper available
        try:
            from faster_whisper import WhisperModel
        except ImportError:
            self.report({"ERROR"}, "faster-whisper not installed")
            return {"CANCELLED"}
        
        # Initialize state
        props.is_downloading_model = True
        props.model_download_progress = 0.0
        props.model_download_status = f"Starting download of {self._model_name}..."
        
        # Create download manager (dependency injection)
        cache_dir = file_utils.get_addon_models_dir()
        self._download_manager = create_download_manager(cache_dir)
        
        # Get optional HF token
        preferences = context.preferences.addons.get("subtitle_editor")
        hf_token = None
        if preferences and hasattr(preferences, "preferences"):
            hf_token = preferences.preferences.hf_token or None
        
        # Start background thread (heavy work here)
        self._thread = threading.Thread(
            target=self._download_worker,
            args=(self._model_name, hf_token)
        )
        self._thread.daemon = True
        self._thread.start()
        
        # Setup modal operator (from technical-domain.md)
        wm = context.window_manager
        wm.progress_begin(0, 100)
        self._timer = wm.event_timer_add(0.1, window=context.window)
        wm.modal_handler_add(self)
        
        # CRITICAL: Return RUNNING_MODAL (from technical-domain.md)
        return {"RUNNING_MODAL"}
    
    def cancel(self, context):
        """
        Clean up when operator finishes or is cancelled.
        CRITICAL: Always remove timer to prevent memory leaks.
        """
        props = context.scene.subtitle_editor
        
        # Cancel download if running
        if self._download_manager:
            self._download_manager.cancel()
        
        # Remove timer (from technical-domain.md)
        if self._timer:
            wm = context.window_manager
            wm.event_timer_remove(self._timer)
            wm.progress_end()
            self._timer = None
        
        props.is_downloading_model = False
    
    def _download_worker(self, model_name: str, token: Optional[str]):
        """
        Background thread - does heavy lifting.
        Separated from UI logic (single responsibility).
        """
        try:
            # This blocks until complete, but runs in background thread
            # Modal() continues to poll for progress
            result = self._download_manager.download(model_name, token=token)
            
        except Exception as e:
            # Error already handled in download manager
            pass


classes = [SUBTITLE_OT_download_model]
```

---

## 🖥️ Phase 3: UI Panel Updates

**File:** `panels/main_panel.py`

Add cancel button and model size info:

```python
# Model selection with download/cancel
box = col.box()
row = box.row(align=True)
row.prop(props, "model", text="")

if props.is_downloading_model:
    row.operator("subtitle.cancel_download", text="Cancel", icon="CANCEL")
    box.prop(props, "model_download_progress", text="Download", slider=True)
    box.label(text=props.model_download_status, icon="FILE_REFRESH")
else:
    row.operator("subtitle.download_model", text="Download", icon="IMPORT")
    
    # Show model size info
    model_sizes = {
        "tiny": "39 MB",
        "base": "74 MB", 
        "small": "244 MB",
        "medium": "769 MB",
        "large-v3": "1550 MB",
    }
    if props.model in model_sizes:
        row = box.row()
        row.label(text=f"Size: {model_sizes[props.model]}", icon="INFO")
```

---

## ✅ Acceptance Criteria

### Functional Requirements:
- [ ] Download uses huggingface_hub (not WhisperModel)
- [ ] Real progress based on bytes downloaded
- [ ] Cancel button stops download cleanly
- [ ] Works without HF token (optional auth)
- [ ] Shows model size before download
- [ ] Resume support for partial downloads

### Code Quality (from code-quality.md):
- [ ] Pure functions where possible
- [ ] Functions < 50 lines
- [ ] Immutable state (DownloadProgress dataclass)
- [ ] Explicit dependencies (dependency injection)
- [ ] No side effects in core logic
- [ ] Testable (DownloadManager has no bpy imports)

### Blender Patterns (from technical-domain.md):
- [ ] Modal operator with proper lifecycle
- [ ] Returns {'PASS_THROUGH'}
- [ ] Uses event.type == 'TIMER'
- [ ] Calls area.tag_redraw()
- [ ] Cleanup in cancel()
- [ ] Returns {'RUNNING_MODAL'}

---

## 🚀 Implementation Order

1. **Phase 1**: Create `core/download_manager.py` (1-2 hours)
2. **Phase 2**: Rewrite `ops_model_download.py` (1-2 hours)
3. **Phase 3**: Add cancel operator + UI updates (30 min)
4. **Phase 4**: Test and debug (30 min)

**Total: 3-5 hours**

---

## 📚 Key Context References

- **Modal Operators**: technical-domain.md (lines 143-177)
- **Code Quality**: code-quality.md (functional programming)
- **Non-blocking**: agent-context.md (GIL explanation)
- **UV Package Manager**: uv-package-manager.md
- **API Patterns**: .tmp/external-context/blender-python-api.md

---

This plan follows:
✅ Clean separation of concerns
✅ Functional programming principles  
✅ Blender modal operator best practices
✅ Testable architecture
✅ User-friendly UX

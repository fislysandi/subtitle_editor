"""
Model Download Operator - UI Layer Only

Uses DownloadManager from core module for actual download logic.
Implements proper Modal Operator pattern for non-blocking UI.
"""

import bpy
import threading
from typing import Optional
from bpy.types import Operator
from ..core.download_manager import (
    DownloadManager,
    DownloadStatus,
    create_download_manager,
)
from ..utils import file_utils


class SUBTITLE_OT_download_model(Operator):
    """Download Whisper model with real progress tracking"""

    bl_idname = "subtitle.download_model"
    bl_label = "Download Model"
    bl_description = "Download the selected Whisper model"
    bl_options = {"REGISTER", "UNDO"}

    # Modal operator state (class variables to persist across modal calls)
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
                if progress.status in [
                    DownloadStatus.COMPLETE,
                    DownloadStatus.ERROR,
                    DownloadStatus.CANCELLED,
                ]:
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

        # Get optional HF token from addon preferences
        preferences = context.preferences.addons.get("subtitle_editor")
        hf_token = None
        if preferences and hasattr(preferences, "preferences"):
            hf_token = preferences.preferences.hf_token or None

        # Start background thread (heavy work here)
        self._thread = threading.Thread(
            target=self._download_worker, args=(self._model_name, hf_token)
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
            self._download_manager.download(model_name, token=token)
        except Exception:
            # Error already handled in download manager
            pass


classes = [SUBTITLE_OT_download_model]

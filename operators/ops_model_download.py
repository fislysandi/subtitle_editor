"""
Model Download Operator

Handles downloading Whisper models on demand
"""

import bpy
import threading
from bpy.types import Operator
from ..utils import file_utils


class SUBTITLE_OT_download_model(Operator):
    """Download the selected Whisper model"""

    bl_idname = "subtitle.download_model"
    bl_label = "Download Model"
    bl_description = (
        "Download the selected Whisper model (large models may take several minutes)"
    )
    bl_options = {"REGISTER"}

    def execute(self, context):
        props = context.scene.subtitle_editor
        model_name = props.model

        # Check if faster-whisper is installed
        try:
            from faster_whisper import download_model
        except ImportError:
            self.report(
                {"ERROR"}, "faster-whisper not installed. Install dependencies first."
            )
            return {"CANCELLED"}

        # Start download in background thread
        props.is_downloading_model = True
        props.model_download_status = f"Starting download of {model_name}..."
        props.model_download_progress = 0.0

        thread = threading.Thread(
            target=self._download_thread, args=(context, model_name)
        )
        thread.daemon = True
        thread.start()

        return {"FINISHED"}

    def _download_thread(self, context, model_name):
        """Download model in background thread"""
        props = context.scene.subtitle_editor

        try:
            from faster_whisper import download_model

            cache_dir = file_utils.get_addon_models_dir()

            # Update status
            def update_status(text, progress=0.0):
                def update():
                    props.model_download_status = text
                    props.model_download_progress = progress
                    return None

                bpy.app.timers.register(update, first_interval=0.0)

            update_status(
                f"Downloading {model_name} model... This may take several minutes.", 0.1
            )

            # Download the model
            # faster-whisper will download to cache_dir
            import os
            import time

            # Check if model already exists
            model_path = os.path.join(
                cache_dir, f"models--Systran--faster-whisper-{model_name}"
            )
            if os.path.exists(model_path):
                update_status(f"Model {model_name} already downloaded!", 1.0)
                props.is_downloading_model = False
                return

            # Download model (this will block until complete)
            update_status(f"Downloading {model_name}... (0%)", 0.2)

            # Note: faster-whisper download_model doesn't provide progress callbacks
            # We'll download it by attempting to load it, which triggers download
            from faster_whisper import WhisperModel

            # This will download if not present
            model = WhisperModel(
                model_name, device="cpu", compute_type="int8", download_root=cache_dir
            )

            update_status(f"Model {model_name} downloaded successfully!", 1.0)

            # Report success
            def report_success():
                self.report({"INFO"}, f"Model {model_name} downloaded successfully!")
                return None

            bpy.app.timers.register(report_success, first_interval=0.5)

        except Exception as e:

            def report_error():
                props.model_download_status = f"Error: {str(e)}"
                self.report({"ERROR"}, f"Failed to download model: {str(e)}")
                return None

            bpy.app.timers.register(report_error, first_interval=0.0)
        finally:

            def finish():
                props.is_downloading_model = False
                return None

            bpy.app.timers.register(finish, first_interval=1.0)


classes = [
    SUBTITLE_OT_download_model,
]

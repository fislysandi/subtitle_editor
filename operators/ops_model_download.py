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

        print(f"[Subtitle Editor] Starting model download for: {model_name}")

        # Check if faster-whisper is installed
        try:
            from faster_whisper import WhisperModel

            print("[Subtitle Editor] faster-whisper imported successfully")
        except ImportError as e:
            error_msg = f"faster-whisper not installed: {e}"
            print(f"[Subtitle Editor] ERROR: {error_msg}")
            self.report({"ERROR"}, error_msg)
            return {"CANCELLED"}

        # Start download in background thread
        props.is_downloading_model = True
        props.model_download_status = f"Preparing to download {model_name}..."
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
            from faster_whisper import WhisperModel
            import os

            cache_dir = file_utils.get_addon_models_dir()
            print(f"[Subtitle Editor] Download thread started for {model_name}")
            print(f"[Subtitle Editor] Cache directory: {cache_dir}")

            # Update status
            def update_status(text, progress=0.0):
                def update():
                    props.model_download_status = text
                    props.model_download_progress = progress
                    return None

                bpy.app.timers.register(update, first_interval=0.0)

            update_status(f"Checking if {model_name} exists...", 0.1)

            # Check if model already exists
            model_path = os.path.join(
                cache_dir, f"models--Systran--faster-whisper-{model_name}"
            )
            if os.path.exists(model_path):
                print(
                    f"[Subtitle Editor] Model {model_name} already exists at {model_path}"
                )
                update_status(f"Model {model_name} already downloaded!", 1.0)

                def report_already():
                    self.report({"INFO"}, f"Model {model_name} already downloaded!")
                    return None

                bpy.app.timers.register(report_already, first_interval=0.5)

                def finish_already():
                    props.is_downloading_model = False
                    return None

                bpy.app.timers.register(finish_already, first_interval=1.5)
                return

            # Download model
            update_status(
                f"Downloading {model_name}... This may take several minutes", 0.2
            )
            print(
                f"[Subtitle Editor] Starting WhisperModel instantiation for {model_name}"
            )

            # This will download if not present
            # Use local_files_only=False to force download
            model = WhisperModel(
                model_name,
                device="cpu",
                compute_type="int8",
                download_root=cache_dir,
                local_files_only=False,
            )

            print(f"[Subtitle Editor] Model {model_name} loaded successfully")
            update_status(f"Model {model_name} downloaded successfully!", 1.0)

            # Report success
            def report_success():
                self.report({"INFO"}, f"Model {model_name} downloaded successfully!")
                return None

            bpy.app.timers.register(report_success, first_interval=0.5)

        except Exception as e:
            error_msg = str(e)
            print(f"[Subtitle Editor] ERROR downloading model: {error_msg}")
            import traceback

            traceback.print_exc()

            def report_error():
                props.model_download_status = f"Error: {error_msg}"
                self.report({"ERROR"}, f"Failed to download model: {error_msg}")
                return None

            bpy.app.timers.register(report_error, first_interval=0.0)

        finally:

            def finish():
                props.is_downloading_model = False
                return None

            bpy.app.timers.register(finish, first_interval=2.0)


classes = [
    SUBTITLE_OT_download_model,
]

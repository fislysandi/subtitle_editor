"""
Model Download Cancel Operator

Simple operator to cancel an in-progress model download.
The actual cancellation is handled by the modal operator polling
is_downloading_model and calling download_manager.cancel().
"""

import bpy
from bpy.types import Operator


class SUBTITLE_OT_cancel_download(Operator):
    """Cancel the current model download"""

    bl_idname = "subtitle.cancel_download"
    bl_label = "Cancel Download"
    bl_description = "Cancel the current model download"
    bl_options = {"REGISTER"}

    def execute(self, context):
        """
        Set is_downloading_model to False to signal cancellation.
        The modal operator will see this and call download_manager.cancel().
        """
        props = context.scene.subtitle_editor
        props.is_downloading_model = False
        props.model_download_status = "Cancelling..."
        self.report({"INFO"}, "Download cancelled")
        return {"FINISHED"}


classes = [
    SUBTITLE_OT_cancel_download,
]

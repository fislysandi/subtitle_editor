"""
UI Panels for Subtitle Editor
Based on upstream: https://github.com/tin2tin/Subtitle_Editor
"""

import bpy
from bpy.types import Panel


class SEQUENCER_PT_panel(Panel):
    """Main Subtitle Editor Panel"""

    bl_idname = "SEQUENCER_PT_panel"
    bl_label = "Subtitle Editor"
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Subtitle Editor"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        col = row.column()
        col.template_list(
            "SEQUENCER_UL_List",
            "",
            context.scene,
            "text_strip_items",
            context.scene,
            "text_strip_items_index",
            rows=14,
        )

        row = row.column(align=True)
        row.operator("text.refresh_list", text="", icon="FILE_REFRESH")

        row.separator()

        row.operator("sequencer.import_subtitles", text="", icon="IMPORT")
        row.operator("sequencer.export_list_subtitles", text="", icon="EXPORT")

        row.separator()

        row.operator("text.add_strip", text="", icon="ADD", emboss=True)
        row.operator("text.delete_item", text="", icon="REMOVE", emboss=True)
        row.operator("text.delete_strip", text="", icon="SCULPTMODE_HLT", emboss=True)

        row.separator()

        row.operator("text.select_previous", text="", icon="TRIA_UP")
        row.operator("text.select_next", text="", icon="TRIA_DOWN")

        row.separator()

        row.operator("text.insert_newline", text="", icon="EVENT_RETURN")


class SEQUENCER_PT_whisper_panel(Panel):
    """Transcription & Translation Panel"""

    bl_label = "Transcription & Translation"
    bl_idname = "SEQUENCER_PT_whisper"
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Subtitle Editor"

    @classmethod
    def poll(cls, context):
        return context.scene is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.whisper_props

        # Setup Section
        box = layout.box()
        row = box.row(align=True)
        status_icon = (
            "CHECKMARK"
            if hasattr(bpy.types.Scene, "dependencies_installed")
            and bpy.types.Scene.dependencies_installed
            else "ERROR"
        )
        row.label(text="Dependencies:", icon=status_icon)
        row.operator("sequencer.whisper_setup", icon="SCRIPTPLUGINS")

        # Configuration Section
        col = layout.column()
        box = col.box()
        box.prop(props, "model_size", text="Model")
        row = box.row(align=True)
        row.prop(props, "device", text="Device")
        row.prop(props, "compute_type", text="Compute")
        box.prop(props, "language", text="Language")
        row = box.row(align=True)
        row.prop(props, "beam_size", text="Beam Size")
        row.prop(props, "use_vad", text="VAD Filter")

        # Subtitle Output Settings
        box = col.box()
        row = box.row(align=True)
        row.prop(props, "output_channel", text="Channel")
        row.prop(props, "font_size", text="Font Size")
        row = box.row(align=True)
        row.prop(props, "text_align_y", text="")
        row.prop(props, "wrap_width", text="Wrap Width")

        # Actions Section
        box = col.box()
        action_col = box.column(align=True)

        op_transcribe = action_col.operator(
            "sequencer.whisper_transcribe", text="Transcribe to Text Strips", icon="REC"
        )
        op_transcribe.task = "transcribe"

        op_translate = action_col.operator(
            "sequencer.whisper_transcribe",
            text="Translate to Text Strips (EN)",
            icon="WORDWRAP_ON",
        )
        op_translate.task = "translate"

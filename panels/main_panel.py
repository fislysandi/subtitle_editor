"""
UI Panels for Subtitle Editor
Simplified version matching upstream layout but using existing operators
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
        scene = context.scene

        row = layout.row()
        col = row.column()
        col.template_list(
            "SEQUENCER_UL_List",
            "",
            context.scene,
            "text_strip_items",
            context.scene,
            "text_strip_items_index",
            rows=10,
        )

        # Button column
        row = row.column(align=True)

        # Refresh
        row.operator("subtitle.refresh_list", text="", icon="FILE_REFRESH")
        row.separator()

        # Import/Export
        row.operator("subtitle.import_subtitles", text="", icon="IMPORT")
        row.operator("subtitle.export_subtitles", text="", icon="EXPORT")
        row.separator()

        # Navigation
        row.operator("subtitle.select_strip", text="", icon="TRIA_UP")
        row.separator()

        # Update
        row.operator("subtitle.update_text", text="", icon="CHECKMARK")


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
        props = scene.subtitle_editor

        # Configuration Section
        col = layout.column()
        box = col.box()
        box.prop(props, "model")
        row = box.row(align=True)
        row.prop(props, "device")
        row.prop(props, "language")
        row = box.row(align=True)
        row.prop(props, "show_advanced", text="Advanced", toggle=True)

        if props.show_advanced:
            box.prop(props, "translate")
            box.prop(props, "word_timestamps")
            box.prop(props, "vad_filter")

        # Actions Section
        box = col.box()
        action_col = box.column(align=True)

        # Transcribe button
        row = action_col.row()
        row.scale_y = 1.5
        row.operator(
            "subtitle.transcribe", text="Transcribe to Text Strips", icon="REC"
        )


class SEQUENCER_PT_edit_panel(Panel):
    """Edit Subtitles Panel"""

    bl_label = "Edit Subtitles"
    bl_idname = "SEQUENCER_PT_edit_panel"
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Subtitle Editor"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Edit selected
        if scene.text_strip_items_index >= 0 and scene.text_strip_items:
            item = scene.text_strip_items[scene.text_strip_items_index]
            box = layout.box()
            box.label(text=f"Editing: {item.name}")
            box.prop(scene.subtitle_editor, "current_text")
        else:
            layout.label(text="Select a subtitle from the list above")

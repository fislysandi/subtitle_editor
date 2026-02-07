"""
UI List for Text Strips
Based on upstream: https://github.com/tin2tin/Subtitle_Editor
"""

import bpy
from bpy.types import UIList


class SEQUENCER_UL_List(UIList):
    """UI List showing text strips"""

    bl_idname = "SEQUENCER_UL_List"

    def draw_item(
        self, context, layout, data, item, icon, active_data, active_propname
    ):
        layout.prop(item, "text", text="", emboss=False)

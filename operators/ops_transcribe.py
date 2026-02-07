"""
Transcription Operators
"""

import bpy
import threading
import os
from bpy.types import Operator
from bpy.props import StringProperty, BoolProperty, EnumProperty

from ..core import transcriber
from ..utils import sequence_utils, file_utils


class SUBTITLE_OT_transcribe(Operator):
    """Transcribe selected audio/video strip to subtitles"""

    bl_idname = "subtitle.transcribe"
    bl_label = "Transcribe"
    bl_description = "Transcribe selected strip to subtitles using AI"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        props = scene.subtitle_editor

        # Get selected strip
        strip = sequence_utils.get_selected_strip(context)
        if not strip:
            self.report({"ERROR"}, "Please select an audio or video strip")
            return {"CANCELLED"}

        # Start transcription in background thread
        props.is_transcribing = True
        props.progress = 0.0
        props.progress_text = "Starting transcription..."

        thread = threading.Thread(
            target=self._transcribe_thread, args=(context, strip, props)
        )
        thread.daemon = True
        thread.start()

        return {"FINISHED"}

    def _transcribe_thread(self, context, strip, props):
        """Run transcription in background thread"""
        # Thread-safe storage for progress data
        progress_data = {"progress": 0.0, "text": "Starting..."}

        def update_props_on_main_thread(progress, text):
            """Schedule property updates on the main thread using bpy.app.timers"""
            progress_data["progress"] = progress
            progress_data["text"] = text

            def apply_updates():
                props.progress = progress_data["progress"]
                props.progress_text = progress_data["text"]
                return None  # Don't repeat

            bpy.app.timers.register(apply_updates, first_interval=0.0)

        try:
            # Extract audio from strip
            filepath = sequence_utils.get_strip_filepath(strip)
            if not filepath:
                update_props_on_main_thread(0.0, "Error: Cannot get strip file path")
                bpy.app.timers.register(
                    lambda: setattr(props, "is_transcribing", False) or None,
                    first_interval=0.0,
                )
                return

            # Initialize transcriber
            tm = transcriber.TranscriptionManager(
                model_name=props.model, device=props.device
            )

            cache_dir = file_utils.get_addon_models_dir()
            if not tm.load_model(cache_dir):
                update_props_on_main_thread(0.0, "Error: Failed to load AI model")
                bpy.app.timers.register(
                    lambda: setattr(props, "is_transcribing", False) or None,
                    first_interval=0.0,
                )
                return

            # Set up progress callback - uses thread-safe updates
            def progress_callback(progress, text):
                update_props_on_main_thread(progress, text)

            tm.set_progress_callback(progress_callback)

            # Extract audio if needed
            audio_path = filepath
            if not filepath.lower().endswith((".wav", ".mp3", ".flac", ".m4a")):
                update_props_on_main_thread(0.0, "Extracting audio...")
                audio_path = file_utils.get_temp_filepath("audio_extract.wav")
                audio_path = tm.extract_audio(filepath, audio_path)

            # Transcribe
            segments = list(
                tm.transcribe(
                    audio_path,
                    language=props.language if props.language != "auto" else None,
                    translate=props.translate,
                    word_timestamps=props.word_timestamps,
                    vad_filter=props.vad_filter,
                )
            )

            # Create text strips in main thread
            bpy.app.timers.register(
                lambda: self._create_strips(context, segments), first_interval=0.0
            )

            # Clean up temp file
            if audio_path != filepath and os.path.exists(audio_path):
                os.remove(audio_path)

            update_props_on_main_thread(1.0, f"Created {len(segments)} subtitle strips")

        except Exception as e:
            update_props_on_main_thread(0.0, f"Error: {str(e)}")
        finally:
            # Schedule cleanup on main thread
            def cleanup_props():
                props.is_transcribing = False
                props.progress = 0.0
                return None

            bpy.app.timers.register(cleanup_props, first_interval=0.0)

    def _create_strips(self, context, segments):
        """Create text strips from transcription (called in main thread)"""
        scene = context.scene

        # Determine channel
        channel = 3
        if scene.sequence_editor:
            # Find empty channel
            for seq in scene.sequence_editor.sequences:
                if seq.channel >= channel:
                    channel = seq.channel + 1
            channel = min(channel, 128)

        # Create strips
        for i, seg in enumerate(segments):
            frame_start = int(seg.start * scene.render.fps)
            frame_end = int(seg.end * scene.render.fps)

            strip = sequence_utils.create_text_strip(
                scene,
                name=f"Subtitle_{i + 1:03d}",
                text=seg.text,
                frame_start=frame_start,
                frame_end=frame_end,
                channel=channel,
            )

            if strip:
                # Add to UI list
                item = scene.text_strip_items.add()
                item.name = strip.name
                item.text = seg.text
                item.frame_start = frame_start
                item.frame_end = frame_end
                item.channel = channel

        # Refresh UI
        sequence_utils.refresh_list(context)
        return None  # Don't repeat


class SUBTITLE_OT_translate(Operator):
    """Translate selected audio/video strip to English subtitles"""

    bl_idname = "subtitle.translate"
    bl_label = "Translate"
    bl_description = "Translate non-English audio to English subtitles"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        props = scene.subtitle_editor

        # Get selected strip
        strip = sequence_utils.get_selected_strip(context)
        if not strip:
            self.report({"ERROR"}, "Please select an audio or video strip")
            return {"CANCELLED"}

        # Start translation in background thread
        props.is_transcribing = True
        props.progress = 0.0
        props.progress_text = "Starting translation to English..."

        thread = threading.Thread(
            target=self._translate_thread, args=(context, strip, props)
        )
        thread.daemon = True
        thread.start()

        return {"FINISHED"}

    def _translate_thread(self, context, strip, props):
        """Run translation in background thread"""
        # Thread-safe storage for progress data
        progress_data = {"progress": 0.0, "text": "Starting..."}

        def update_props_on_main_thread(progress, text):
            """Schedule property updates on the main thread using bpy.app.timers"""
            progress_data["progress"] = progress
            progress_data["text"] = text

            def apply_updates():
                props.progress = progress_data["progress"]
                props.progress_text = progress_data["text"]
                return None  # Don't repeat

            bpy.app.timers.register(apply_updates, first_interval=0.0)

        try:
            # Extract audio from strip
            filepath = sequence_utils.get_strip_filepath(strip)
            if not filepath:
                update_props_on_main_thread(0.0, "Error: Cannot get strip file path")
                bpy.app.timers.register(
                    lambda: setattr(props, "is_transcribing", False) or None,
                    first_interval=0.0,
                )
                return

            # Initialize transcriber
            tm = transcriber.TranscriptionManager(
                model_name=props.model, device=props.device
            )

            cache_dir = file_utils.get_addon_models_dir()
            if not tm.load_model(cache_dir):
                update_props_on_main_thread(0.0, "Error: Failed to load AI model")
                bpy.app.timers.register(
                    lambda: setattr(props, "is_transcribing", False) or None,
                    first_interval=0.0,
                )
                return

            # Set up progress callback - uses thread-safe updates
            def progress_callback(progress, text):
                update_props_on_main_thread(progress, text)

            tm.set_progress_callback(progress_callback)

            # Extract audio if needed
            audio_path = filepath
            if not filepath.lower().endswith((".wav", ".mp3", ".flac", ".m4a")):
                update_props_on_main_thread(0.0, "Extracting audio...")
                audio_path = file_utils.get_temp_filepath("audio_extract.wav")
                audio_path = tm.extract_audio(filepath, audio_path)

            # Translate (always translate to English)
            segments = list(
                tm.transcribe(
                    audio_path,
                    language=props.language if props.language != "auto" else None,
                    translate=True,  # Force translate
                    word_timestamps=props.word_timestamps,
                    vad_filter=props.vad_filter,
                )
            )

            # Create text strips in main thread
            bpy.app.timers.register(
                lambda: self._create_strips(context, segments), first_interval=0.0
            )

            # Clean up temp file
            if audio_path != filepath and os.path.exists(audio_path):
                os.remove(audio_path)

            update_props_on_main_thread(
                1.0, f"Created {len(segments)} translated subtitle strips"
            )

        except Exception as e:
            update_props_on_main_thread(0.0, f"Error: {str(e)}")
        finally:
            # Schedule cleanup on main thread
            def cleanup_props():
                props.is_transcribing = False
                props.progress = 0.0
                return None

            bpy.app.timers.register(cleanup_props, first_interval=0.0)

    def _create_strips(self, context, segments):
        """Create text strips from translation (called in main thread)"""
        scene = context.scene
        props = scene.subtitle_editor

        # Determine channel
        channel = props.subtitle_channel
        if scene.sequence_editor:
            # Find empty channel
            for seq in scene.sequence_editor.sequences:
                if seq.channel >= channel:
                    channel = seq.channel + 1
            channel = min(channel, 128)

        # Create strips
        for i, seg in enumerate(segments):
            frame_start = int(seg.start * scene.render.fps)
            frame_end = int(seg.end * scene.render.fps)

            strip = sequence_utils.create_text_strip(
                scene,
                name=f"Subtitle_{i + 1:03d}_EN",
                text=seg.text,
                frame_start=frame_start,
                frame_end=frame_end,
                channel=channel,
            )

            if strip:
                # Add to UI list
                item = scene.text_strip_items.add()
                item.name = strip.name
                item.text = seg.text
                item.frame_start = frame_start
                item.frame_end = frame_end
                item.channel = channel

        # Refresh UI
        sequence_utils.refresh_list(context)
        return None  # Don't repeat

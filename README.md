# Subtitle Studio

Subtitle Studio is a Blender VSE add-on for creating, editing, timing, and exporting subtitles with a future path toward TTS voicing.

## Overview

Subtitle Studio integrates directly with Blender's Video Sequence Editor so you can transcribe audio, edit subtitle text, and export standard subtitle formats without leaving Blender.

## Requirements

- Blender 5.0+ (or 4.5 LTS)
- Python 3.11 (bundled with Blender)
- ~500MB disk space for AI models

## Installation

1. Download the release zip.
2. In Blender: Edit → Preferences → Add-ons → Install.
3. Enable "Subtitle Studio" in the Add-ons list.
4. Use the add-on Preferences panel to download dependencies (or use bundled libs for offline installs).

## Quick Start

1. Open the Video Sequence Editor.
2. Add a video or audio strip.
3. Open the Subtitle Studio panel and run Transcribe.
4. Edit subtitle cues in the list view.
5. Export when finished.

## Usage

- Activate the add-on in Blender Preferences → Add-ons.
- In the VSE sidebar, open the Subtitle Studio panel.
- Transcribe or import subtitles, then adjust timing and text.
- Export to SRT/VTT/ASS/SSA when ready.

## Features

- **AI-Powered Transcription**: Faster Whisper for offline speech-to-text.
- **Multi-Language Support**: 99+ languages supported.
- **Visual Subtitle Editing**: Edit subtitles directly in Blender VSE.
- **Import/Export**: SRT, VTT, ASS, SSA formats.
- **Offline Capable**: Bundled dependencies for air-gapped workflows.
- **Blender 5.0+ Compatible**: Works with latest Blender versions.

## Troubleshooting

- Add-on not visible: Ensure the zip is installed and enabled, then restart Blender.
- Model download fails: Check your download directory permissions and retry in Preferences.
- No subtitles created: Confirm the strip is selected and the timeline is active.

## Attribution

Inspired by the original Subtitle Editor add-on: https://github.com/tin2tin/Subtitle_Editor

## License

GPL-3.0-or-later. See LICENSE.

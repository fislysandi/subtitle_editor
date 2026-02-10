# Subtitle Studio - Troubleshooting

**Last Updated:** 2026-02-10

Common issues and solutions for Subtitle Studio.

---

## Table of Contents

1. [Installation Issues](#installation-issues)
2. [Dependency Issues](#dependency-issues)
3. [Transcription Issues](#transcription-issues)
4. [UI/Display Issues](#uidisplay-issues)
5. [Import/Export Issues](#importexport-issues)
6. [Performance Issues](#performance-issues)

---

## Installation Issues

### Add-on Not Visible After Installation

**Symptoms:** Subtitle Studio doesn't appear in the add-ons list.

**Solutions:**

1. **Verify ZIP structure**
   ```
   subtitle_studio.zip
   └── subtitle_editor/
       ├── __init__.py
       └── ...
   ```
   The folder containing `__init__.py` should be directly inside the ZIP.

2. **Check Blender version**
   - Requires Blender 4.5 LTS or 5.0+
   - Check: `Help → About Blender`

3. **Restart Blender**
   - Close Blender completely
   - Reopen and check add-ons list

4. **Check console for errors**
   ```
   Window → Toggle System Console (Windows)
   # or launch Blender from terminal (Linux/macOS)
   ```

### ZIP Installation Fails

**Symptoms:** Error message when clicking "Install..."

**Solutions:**

```bash
# Manual installation workaround
# 1. Extract ZIP to a folder
# 2. Copy the 'subtitle_editor' folder to:

# Linux
~/.config/blender/4.5/scripts/addons/

# macOS
~/Library/Application Support/Blender/4.5/scripts/addons/

# Windows
%APPDATA%\Blender Foundation\Blender\4.5\scripts\addons\
```

---

## Dependency Issues

### Dependencies Not Installing

**Symptoms:** "Install Dependencies" button fails or hangs.

**Solutions:**

1. **Check internet connection**
   - Dependencies download from PyPI
   - Models download from Hugging Face

2. **Try UV fallback**
   - In Add-on Preferences, uncheck "Use UV for Downloads"
   - Click Install Dependencies again (uses pip)

3. **Manual installation**
   ```bash
   # Find Blender's Python
   blender --version  # Get version
   
   # Navigate to Blender's Python directory
   # Linux example:
   cd /usr/share/blender/4.5/python/bin
   
   # Install dependencies
   ./python -m pip install faster-whisper pysubs2 onnxruntime
   ```

4. **Check permissions**
   - Blender needs write access to its Python directory
   - Try running Blender as administrator (Windows)
   - Check folder permissions (Linux/macOS)

### PyTorch Installation Fails

**Symptoms:** PyTorch install fails or wrong CUDA version installed.

**Solutions:**

1. **Check GPU compatibility**
   ```
   NVIDIA GTX/RTX: Use CUDA 11.8, 12.1, or 12.4
   AMD GPU (Linux): Use ROCm 5.7
   Apple Silicon: Use Metal
   CPU only: Use CPU option
   ```

2. **Verify CUDA version**
   ```bash
   # Windows/Linux
   nvidia-smi
   
   # Look for "CUDA Version: X.X"
   # Match PyTorch CUDA version to your driver
   ```

3. **Common CUDA mismatches**
   | GPU | Recommended CUDA |
   |-----|-----------------|
   | GTX 10 series | CUDA 11.8 |
   | RTX 20/30 series | CUDA 12.1 |
   | RTX 40 series | CUDA 12.1 or 12.4 |

4. **Reinstall with correct version**
   - In panel, select correct CUDA version from dropdown
   - Click "Install PyTorch"
   - Wait for completion

### Model Download Fails

**Symptoms:** Model download hangs or errors.

**Solutions:**

1. **Check disk space**
   - Large models need up to 1.5 GB
   - Ensure free space available

2. **Set Hugging Face token**
   - Get token: https://huggingface.co/settings/tokens
   - Add to Add-on Preferences
   - Retry download

3. **Manual download**
   ```bash
   # Download from Hugging Face manually
   # Place in Blender's models folder:
   
   # Linux
   ~/.config/blender/4.5/scripts/addons/subtitle_editor/models/
   
   # Or set custom path in preferences
   ```

4. **Check firewall/antivirus**
   - Whitelist Blender for internet access
   - Temporarily disable VPN if using one

---

## Transcription Issues

### No Subtitles Created

**Symptoms:** Transcription runs but no strips appear.

**Solutions:**

1. **Verify strip selection**
   - Must select audio or video strip before transcribing
   - Strip must have audio track

2. **Check file path**
   - Strip must reference a file on disk
   - Generated strips (not from files) won't work

3. **Check sequence editor**
   - Ensure sequence editor exists
   - Try: `Add → Sequence Editor`

4. **Check console for errors**
   ```python
   # Open Python Console in Blender
   # Check if transcription module loaded
   import faster_whisper
   print("Faster Whisper loaded successfully")
   ```

### Transcription Is Very Slow

**Symptoms:** Takes hours for short audio.

**Solutions:**

| Issue | Solution |
|-------|----------|
| Running on CPU | Install GPU-accelerated PyTorch |
| Using large model | Try `base` or `small` model |
| High beam size | Reduce beam size to 1-3 |
| Long audio | Split into shorter segments |
| Memory full | Close other applications |

### Poor Transcription Quality

**Symptoms:** Many errors, missed words.

**Solutions:**

1. **Use larger model**
   - Upgrade from `base` → `small` → `medium`

2. **Increase beam size**
   - Default: 5
   - Try: 7-10 for better accuracy (slower)

3. **Check language setting**
   - Use specific language instead of "auto"
   - Verify language code is correct

4. **Adjust VAD for noisy audio**
   ```
   VAD Threshold: 0.3 (lower = more sensitive)
   Min Speech Duration: 100ms
   ```

5. **Pre-process audio**
   - Remove background noise if possible
   - Ensure good audio levels

### Out of Memory Error

**Symptoms:** Blender crashes or freezes during transcription.

**Solutions:**

```python
# Reduce memory usage:
1. Use smaller model (tiny/base)
2. Use int8 compute type
3. Reduce batch size (if exposed)
4. Close other Blender projects
5. Split audio into chunks
```

**Compute Type Settings:**
- `int8` - Lowest memory, fastest
- `float16` - Balanced (recommended with GPU)
- `float32` - Best quality, most memory

---

## UI/Display Issues

### Panel Not Showing

**Symptoms:** Sidebar panel is empty or missing.

**Solutions:**

1. **Check workspace**
   - Must be in **Video Sequence Editor**
   - Press `N` to show sidebar

2. **Verify add-on enabled**
   ```
   Edit → Preferences → Add-ons
   Search: "Subtitle Studio"
   Ensure checkbox is checked ✅
   ```

3. **Reload scripts**
   ```
   Scripting workspace → Reload Scripts (or F8)
   ```

4. **Check for errors**
   - Open System Console
   - Look for Python errors
   - Report errors on GitHub

### Subtitle List Empty

**Symptoms:** List shows no subtitles even though they exist.

**Solutions:**

1. **Check channel settings**
   - Subtitles must be on the designated channel
   - Default: Channel 2
   - Check panel for channel number

2. **Refresh the list**
   - Click the **Refresh** button (circular arrows icon)

3. **Check strip type**
   - Only TEXT strips appear in list
   - Other types won't show

### Styling Not Applied

**Symptoms:** Style changes don't affect strips.

**Solutions:**

1. **Select strips first**
   - Changes only apply to selected strips
   - Select in sequencer or list

2. **Apply explicitly**
   - Use **Copy Active Style to Selected** button

3. **Check strip properties**
   ```python
   # Some properties may not exist in older Blender versions
   # Verify in Python Console:
   strip = bpy.context.scene.sequence_editor.active_strip
   print(dir(strip))  # See available properties
   ```

---

## Import/Export Issues

### Import Fails

**Symptoms:** Error when importing subtitle file.

**Solutions:**

1. **Check file format**
   - Supported: SRT, VTT, ASS, SSA
   - Verify file extension matches content

2. **Check encoding**
   - Files should be UTF-8 encoded
   - Re-save with UTF-8 if needed

3. **Validate file format**
   ```
   SRT format:
   1
   00:00:01,000 --> 00:00:04,000
   Hello World
   
   2
   00:00:05,000 --> 00:00:08,000
   Second subtitle
   ```

### Export Timing Wrong

**Symptoms:** Exported subtitles have incorrect timing.

**Solutions:**

1. **Check frame rate**
   - Subtitle times are calculated from scene FPS
   - Ensure `Scene Properties → Frame Rate` is correct

2. **Frame rate mismatch**
   ```python
   # If video is 30fps but scene is 24fps:
   # Subtitles will be out of sync
   
   # Match scene FPS to video FPS before export
   ```

3. **Round-trip test**
   - Import → Export → Compare files
   - Should be identical (within rounding)

---

## Performance Issues

### Blender Freezes During Transcription

**Solutions:**

1. **Normal behavior**
   - Modal operators should keep UI responsive
   - But some lag is expected

2. **Reduce model size**
   - Use `base` instead of `large`

3. **Close other applications**
   - Free up RAM and CPU

4. **Check for errors**
   - Open System Console before transcribing
   - Watch for error messages

### Slow UI Response

**Solutions:**

```python
# If panel lags:
1. Reduce subtitle count in scene
2. Disable real-time preview
3. Restart Blender
4. Check for memory leaks (watch memory usage)
```

---

## Getting More Help

If issues persist:

1. **Check documentation**
   - [User Guide](user-guide.md)
   - [README.md](../README.md)
   - [Whisper Config](whisper-config.md)

2. **Enable debug logging**
   ```python
   # In Blender Python Console
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

3. **Gather information**
   - Blender version
   - Add-on version
   - Operating system
   - GPU model
   - Error messages (copy from console)

4. **Report issues**
   - GitHub Issues page
   - Include steps to reproduce
   - Attach .blend file (if possible)
   - Include console output

---

## Related Documentation

- [README.md](../README.md) - Project overview
- [docs/user-guide.md](user-guide.md) - Complete user tutorial
- [docs/whisper-config.md](whisper-config.md) - Model configuration
- [docs/dependencies.md](dependencies.md) - Dependency management
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Developer guide

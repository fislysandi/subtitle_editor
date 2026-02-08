# Subtitle Studio - Development Workflow

## Overview

This document describes how to develop, test, and package Subtitle Studio locally.

## Requirements

- Blender 5.0+ (or 4.5 LTS)
- Python 3.11 (bundled with Blender)
- UV package manager

## Local Workflow

1. Clone the repository.
2. Open Blender and install the add-on zip for a baseline test, or use the folder directly in your Blender scripts/addons path for iterative development.
3. Enable Subtitle Studio in Blender Preferences.

## Run and Test

Use UV to run local commands:

```bash
uv run test subtitle_editor
```

## Package Release

```bash
uv run release subtitle_editor
```

## Blender Iteration Tips

- Use Blender's scripting console to reload the add-on after changes.
- Restart Blender if UI panels do not update after a code change.

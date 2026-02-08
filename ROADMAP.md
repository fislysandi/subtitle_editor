# Subtitle Studio — Roadmap

> Subtitle Studio is a Blender VSE add-on for creating, editing, timing, and exporting subtitles — with a future path to generating voiced tracks via TTS.

## Project Goals
- **P0:** Reliable subtitle creation + editing in VSE (timing is correct; strips are placed correctly; exports are correct).
- **P1:** Smooth UX (non-blocking downloads, clear status/progress, preferences, guardrails).
- **P2:** Extensibility toward **TTS voicing** (generate voice audio that aligns with subtitles).

---

## Milestone 0 — Rename + Polish Baseline (Brand/Repo Hygiene)
**Outcome:** Project is consistently named “Subtitle Studio” everywhere, and the repo looks intentional.

- [ ] Rename addon display name to **Subtitle Studio**
- [ ] Add me as the author "Fislysandi"
- [ ] Credit the original repo for the idea "https://github.com/tin2tin/Subtitle_Editor"
- [ ] Update `bl_info` (name, description, versioning, links)
- [ ] Update README: install steps, quickstart, troubleshooting
- [ ] Ensure module/package naming is consistent (keep Python package name stable if needed; rename only UI-facing strings first)
- [ ] Add `ROADMAP.md` + `CHANGELOG.md` + `LICENSE` verification
- [ ] Add screenshots/gifs for the README (optional but recommended)
- [ ] Add `docs/dev.md`: dev workflow (how to run, how to test in Blender)

**Acceptance criteria**
- Blender Add-ons list shows “Subtitle Studio”
- README reflects the correct name and how to install/run

---

## Milestone 1 — Core Subtitle Strip Engine (VSE Correctness)
**Outcome:** Subtitles place correctly in time and track/channel, every time.

- [ ] Implement/verify timestamp→frame conversion:
  - uses `fps / fps_base`
  - respects `scene.frame_start`
- [ ] Implement robust VSE TEXT strip creation:
  - `sequence_editor.sequences.new_effect(type="TEXT")`
  - correct `frame_start/frame_end`
  - correct `channel` selection
- [ ] Channel strategy:
  - user-select channel OR auto-find free channel
  - never overwrite existing strips unexpectedly
- [ ] Idempotent operations:
  - “Create subtitles” doesn’t duplicate unless requested
  - support “Replace existing subtitle strips” option
- [ ] Support basic styling parameters (font size, wrap, position, color) if not present

**Acceptance criteria**
- Given a sample transcript with timestamps, strips land correctly (time + channel) and play back aligned.

---

## Milestone 2 — Import/Export Reliability
**Outcome:** Subtitle Studio is dependable for real workflows.

- [ ] Import SRT reliably (encoding, multi-line cues, edge cases)
- [ ] Export SRT reliably (rounding rules, ordering, overlaps)
- [ ] (Optional) Export VTT
- [ ] Normalize time rounding behavior (document it)
- [ ] Add “Validate timeline” tool:
  - detect overlaps
  - detect out-of-range cues
  - detect missing end times

**Acceptance criteria**
- Round-trip: Import SRT → export SRT preserves timing and text (within rounding rules).

---

## Milestone 3 — Non-Blocking Downloads + Status Bar Progress (UX)
**Outcome:** Downloads never freeze Blender; progress appears like render/bake.

- [ ] Download manager (pure python) supports progress callback:
  - `downloaded_bytes`, `total_bytes`, `state`
- [ ] Blender modal operator wrapper:
  - timer-based polling
  - `wm.progress_begin/update/end` (status bar)
  - error + cancel handling
- [ ] Preferences panel:
  - download directory
  - “Download model/deps” button
  - show installed/version info
- [ ] Logging + user-facing messages:
  - non-spammy reports
  - actionable errors

**Acceptance criteria**
- Downloading a large file shows smooth status-bar progress and UI remains responsive.

---

## Milestone 4 — UI/Workflow Polish
**Outcome:** Feels like a real Blender tool.

- [ ] Panel layout cleanup (VSE sidebar / add-on prefs)
- [ ] Clear “happy path” workflow:
  - Load media
  - Import/generate subtitles
  - Adjust
  - Export
- [ ] Undo/redo correctness (operators structured properly)
- [ ] Better selection and editing tools:
  - edit subtitle text in UI list
  - jump timeline to cue
  - adjust in/out with buttons
- [ ] Presets for styling (subtitle theme presets)

**Acceptance criteria**
- A new user can install and create subtitles in <5 minutes with minimal confusion.

---

## Milestone 5 — Architecture for TTS Voicing (Design + Foundations)
**Outcome:** Subtitle Studio is ready to add TTS without rewriting everything.

- [ ] Define a **“Cue model”** that is independent of VSE strips:
  - `text`, `start_s`, `end_s`, `speaker?`, `style?`, `voice?`
- [ ] Define an **audio generation pipeline interface**:
  - input: list of cues
  - output: audio files + placement metadata
- [ ] Add per-cue metadata fields needed for TTS later:
  - voice id, speed, pitch, volume, emotion (future-safe fields)
- [ ] Storage strategy:
  - where metadata lives (scene custom props vs JSON sidecar)
- [ ] Decide on initial TTS engine target(s) (defer implementation)

**Acceptance criteria**
- You can attach “voice settings” to cues without breaking subtitle workflows.

---

## Milestone 6 — TTS Voicing MVP (Future)
**Outcome:** Generate voice audio aligned to subtitles.

- [ ] Choose initial TTS backend (local or API)
- [ ] Generate per-cue audio clips
- [ ] Place audio strips into VSE aligned with subtitle start times
- [ ] Handle gaps, overlaps, fades
- [ ] Export combined audio track (optional)

**Acceptance criteria**
- One-click: cues → audio strips placed correctly on a chosen channel.

---

## Backlog / Nice-to-Haves
- [ ] Speaker diarization + per-speaker voices
- [ ] Translate subtitles (multi-language tracks)
- [ ] Karaoke/highlight word timing (advanced)
- [ ] Batch processing for multiple clips
- [ ] Packaging automation + releases

---

## Immediate Next Tasks (Pick 3)
- [ ] (P0) Lock down frame math + channel placement (Milestone 1)
- [ ] (P1) Non-blocking download operator + status-bar progress (Milestone 3)
- [ ] (P1) Rename + README polish to Subtitle Studio (Milestone 0)


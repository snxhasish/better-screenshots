# Better Screenshots - Project Specification

## Overview

A CLI-driven screenshot tool for Linux with background customization. Configurable via TOML/JSON/YAML files with hot-reload support. Optional cloud hosting for uploading screenshots and generating shareable links.

**Philosophy**: Leverage existing tools (grim, slurp, scrot) for capture, focus on unique value (background customization, config-driven workflow).

---

## Core Features

### 1. Capture Modes
- **Full screen** - Capture all monitors or single monitor (via grim)
- **Window** - Select and capture a specific window (via grim)
- **Region** - Interactive region selection (via slurp)
- **Delayed** - 3s, 5s, 10s countdown options

### 2. Background Customization (Key Differentiator)
- **Solid color** backgrounds
- **Gradient** backgrounds (with direction control)
- **Custom image** backgrounds
- **Frame/Border** styles (solid, rounded)
- **Shadow** depth and blur
- **Padding** around screenshot
- **Preset templates** (Instagram, Twitter, blog-ready sizes)

### 3. Output Options
- **Formats**: PNG, JPEG, WebP
- **Copy to clipboard**
- **Auto-save** with custom naming pattern

### 4. Cloud Hosting (Phase 5)
- Upload screenshots to cloud
- Generate short shareable links
- Link history management
- Auto-upload option

---

## CLI Usage

```bash
# Capture with default settings from config
better-screenshots

# Override config options
better-screenshots --mode region --format png

# Full screen capture
better-screenshots --mode fullscreen

# Window capture
better-screenshots --mode window

# Delayed capture
better-screenshots --delay 5

# Use a preset
better-screenshots --preset "Instagram Post"

# Upload to cloud
better-screenshots --upload

# Copy to clipboard only (don't save)
better-screenshots --clipboard-only
```

### Keybind Integration

Configure in your window manager (i3, Sway, etc.):

```bash
# Sway
bindsym $mod+Print exec better-screenshots --mode region
bindsym Print exec better-screenshots --mode fullscreen
```

---

## Config File Support

**Priority**: TOML > JSON > YAML  
**Location**: `~/.config/better-screenshots/`  
**Hot Reload**: Yes - config changes apply on next run

### Config Files Checked (in order)
1. `config.toml`
2. `config.json`
3. `config.yaml`

### TOML Config Structure

```toml
# ============================================
# CAPTURE SETTINGS
# ============================================
[capture]
default_format = "png"
save_directory = "~/Pictures/Screenshots"
naming_pattern = "screenshot_%Y%m%d_%H%M%S"
default_mode = "region"  # fullscreen, window, region
delay_seconds = 0

# ============================================
# BACKGROUND SETTINGS
# ============================================
[background]
default_type = "solid"  # solid, gradient, image
default_color = "#1a1a2e"
padding = 32
shadow_enabled = true
shadow_blur = 20
shadow_offset_x = 0
shadow_offset_y = 10
shadow_color = "#000000"
frame_enabled = false
frame_width = 0
frame_color = "#ffffff"
frame_radius = 0

[background.gradient]
enabled = false
start_color = "#1a1a2e"
end_color = "#16213e"
direction = "vertical"  # vertical, horizontal, diagonal

[background.image]
enabled = false
path = "~/Pictures/bg.png"
fit = "cover"  # cover, contain, stretch
opacity = 1.0

# ============================================
# OUTPUT SETTINGS
# ============================================
[output]
jpeg_quality = 90
png_compression = 6
copy_to_clipboard = true
show_save_dialog = false

# ============================================
# CLOUD HOSTING
# ============================================
[cloud]
enabled = false
provider = "self_hosted"  # self_hosted, imgur, cloudinary, s3

[cloud.self_hosted]
api_url = "https://your-server.com/api"
api_key = ""

[cloud.third_party]
service = "imgur"
api_key = ""

[cloud.advanced]
auto_upload = false
copy_link_to_clipboard = true
delete_after_days = 30  # 0 = never

# ============================================
# PRESETS
# ============================================
[[presets]]
name = "Instagram Post"
width = 1080
height = 1080
background_type = "solid"
background_color = "#1a1a2e"
padding = 40

[[presets]]
name = "Twitter Image"
width = 1200
height = 675
background_type = "gradient"
gradient_start = "#1a1a2e"
gradient_end = "#16213e"
padding = 32
```

---

## Technical Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.10+ |
| CLI Framework | click |
| Capture | Native `grim` (Wayland) / `scrot` (X11) |
| Region select | `slurp` |
| Image processing | Pillow (PIL) |
| Config parsing | `toml`, `yaml` |
| HTTP client | `requests` |

---

## Architecture

```
better_screenshots/
├── better_screenshots/
│   ├── __init__.py
│   ├── __main__.py           # CLI entry point
│   ├── cli/
│   │   ├── __init__.py
│   │   └── commands.py      # click command definitions
│   ├── capture/
│   │   ├── __init__.py
│   │   ├── grim.py           # grim integration
│   │   ├── scrot.py          # scrot integration
│   │   └── slurp.py          # slurp integration
│   ├── config/
│   │   ├── __init__.py
│   │   ├── manager.py         # Load/save config
│   │   ├── parser.py         # TOML/JSON/YAML parsing
│   │   └── models.py         # Config data classes
│   ├── processor/
│   │   ├── __init__.py
│   │   ├── image_processor.py # Background/shadow/padding
│   │   └── background.py      # Render backgrounds
│   ├── output/
│   │   ├── __init__.py
│   │   ├── saver.py          # Save to file
│   │   └── clipboard.py      # Copy to clipboard
│   └── cloud/
│       ├── __init__.py
│       ├── uploader.py       # Upload service
│       └── providers/
│           ├── __init__.py
│           ├── self_hosted.py
│           └── imgur.py
├── pyproject.toml
├── setup.py
└── requirements.txt
```

---

## Workflow

```
User runs: better-screenshots [options]

1. Load config (~/.config/better-screenshots/config.toml)
2. Merge with CLI arguments (CLI takes precedence)
3. Determine capture mode (from args or config)
4. Execute capture:
   - Wayland: grim [-s] [-o]
   - X11: scrot
5. Load captured image
6. Apply background customization:
   - Create canvas with background
   - Add padding
   - Render screenshot with shadow
7. Handle output:
   - Save to file (PNG/JPEG/WebP)
   - Copy to clipboard (if enabled)
   - Upload to cloud (if auto_upload enabled)
8. Copy shareable link to clipboard (if cloud enabled)
```

---

## Implementation Phases

### Phase 1: Core Capture + Config
- CLI argument parsing with click
- grim/scrot integration
- slurp region selection
- Config file loading (TOML/JSON/YAML)
- Basic save/export

### Phase 2: Background Customization
- Solid color backgrounds
- Gradient backgrounds
- Shadow and frame effects
- Padding control
- Image compositing

### Phase 3: Presets & Export
- Preset templates (Instagram, Twitter sizes)
- Multiple format export (PNG, JPEG, WebP)
- Copy to clipboard

### Phase 4: Cloud Hosting
- Account settings (via config file)
- Upload service (self-hosted + third-party)
- Short link generation
- Link history (stored locally)
- Auto-upload option

---

## Cloud Hosting Details

### Self-Hosted Backend (Optional)

**API Endpoints**:
```
POST /api/upload     - Upload image, returns short code
GET  /s/{code}       - Redirect to actual image
GET  /api/links      - List user's links (with API key)
DELETE /api/links/{code} - Delete a link
```

**Recommended Stack**:
- API: Dart (Shelf) / Go / Node.js
- Database: PostgreSQL or SQLite
- Short codes: Nanoid/UUID
- Storage: Local filesystem or S3-compatible

### Supported Third-Party Services
- Imgur
- Cloudinary
- AWS S3

---

## Key Differentiators

| Tool | Background Features | Config File | CLI-driven | Hot Reload |
|------|---------------------|-------------|------------|------------|
| Flameshot | None | No | Partial | No |
| Grim+swappy | Basic | No | Yes | No |
| Shutter | Limited | No | No | No |
| **Better Screenshots** | Full | TOML/JSON/YAML | Yes | Yes |

---

## Dependencies

### System Dependencies
```bash
# Wayland
grim          # Screenshot capture
slurp         # Region selection

# X11 (fallback)
scrot         # Screenshot capture

# Optional
wl-copy       # Clipboard (Wayland)
xclip         # Clipboard (X11)
xdotool       # Window selection (X11)
```

### Python Dependencies (requirements.txt)
```
click>=8.0.0
Pillow>=10.0.0
toml>=0.10.2
PyYAML>=6.0
requests>=2.28.0
```

---

## Build & Run Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run in development
python -m better_screenshots

# Install as CLI tool
pip install -e .

# Build distribution
python -m build

# Run
better-screenshots --help
```

---

## Future Considerations

- Plugin system for custom backgrounds
- Batch processing
- TUI (terminal UI) for settings
- Mobile companion app
- Team/workspace features for cloud

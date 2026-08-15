# Godot 4 Setup Guide for 2D Game Development

## Your Specs Check
- **CPU**: AMD Athlon 200GE (2 cores, 4 threads @ 3.2GHz) — fine for Godot 4 2D
- **RAM**: 8GB DDR4 — enough, but close any browsers when running Godot
- **GPU**: Radeon Vega 3 (1GB VRAM) — fine for 2D, disable 3D features
- **Storage**: 30GB free on C: — plenty for Godot + assets

---

## 1. Download & Install Godot 4

### Step 1: Download
1. Go to https://godotengine.org/download/windows/
2. Download the **Standard version** (64-bit, ~60MB .zip)
   - NOT the .NET version (that's for C#, you want GDScript)
3. Extract the zip to `C:\Godot\` or `D:\Godot\` (keep it simple)

### Step 2: Create Shortcut
Right-click `Godot_v4.x_stable_win64.exe` → Send to → Desktop (create shortcut)

### Step 3: First Launch
1. Double-click the shortcut
2. Click **New Project** → Name it `MyFirstGame` → Browse to `D:\GodotProjects\`
3. Under **Renderer**, select **Mobile** (NOT Forward+ — Mobile is better for 2D + your GPU)
4. Click **Create & Edit**

---

## 2. Optimize Godot for Your PC

### Project Settings (Project → Project Settings → General)
```
Display > Window > Width: 1920
Display > Window > Height: 1080  
Display > Window > Mode: Windowed (not fullscreen — you'll crash less)
Rendering > Quality > 2D > HDR 2D: Disabled
Rendering > Textures > Default Filters: Nearest (for pixel art sharpness)
```

### Editor Settings (Editor → Editor Settings)
```
General > Main > Max FPS: 60
General > Interface > Editor > Display Scale: Auto (match your screen)
General > Text Editor > Completion > Enable Auto Completion: On
General > Run > Auto Save Before Running: On
Network > Debug > Debug Port: 6007 (default is fine)
```

### Performance Tweak
- **Close Chrome/Edge** while using Godot — browsers eat 2-4GB RAM
- Set Windows power plan to **High Performance** (Control Panel → Power Options)

---

## 3. Install Essential Plugins (Asset Library)

Open Godot → Click **AssetLib** tab (top of editor) → Search and install:

| Plugin | What It Does | How to Install |
|--------|-------------|----------------|
| **Pixelorama Importer** | Import .pxl sprite files | AssetLib → search → Install |
| **2D Fake Retro Blur** | CRT/scanline shaders | AssetLib → search → Install |
| **Dialogic 2** | Dialogue system for RPGs | AssetLib → search → Install |
| **Godot Tilemap Manager** | Better tilemap editing | AssetLib → search → Install |

---

## 4. Import Free Sprite Packs

### Method A: Drag & Drop
1. Download a free sprite pack (e.g., from Kenney.nl or OpenGameArt)
2. Unzip it into your project folder: `D:\GodotProjects\MyFirstGame\assets\`
3. Back in Godot, you'll see the files appear in the **FileSystem** panel

### Method B: System File Manager
1. Open your project folder in Windows Explorer
2. Create folders: `assets/sprites/`, `assets/tilesets/`, `assets/sfx/`, `assets/music/`
3. Copy assets into those folders
4. In Godot, right-click the FileSystem panel → **Rescan**

### Import Settings (For Pixel Art Sprites)
When you click a sprite file in Godot's FileSystem:
1. Click the file → **Import** tab (bottom of FileSystem panel)
2. Set:
   - **Filter**: Nearest (keeps pixel art sharp instead of blurry)
   - **Repeat**: Enabled (for tileable textures)
   - **Compress/Mode**: Lossless (for pixel art)
3. Click **Reimport**

---

## 5. Create Your First 2D Scene (Test Page)

```
FileSystem panel → Right-click → New Folder → "scenes"
Right-click "scenes" → New → Scene → "Main.tscn"
```

### Node Structure (for a platformer)
```
Main (Node2D)
├── World (TileMapLayer)
│   └── TileSet (from your tileset sprite)
├── Player (CharacterBody2D)
│   └── Sprite2D (assign your player sprite)
│   └── CollisionShape2D (RectangleShape2D)
│   └── Camera2D (enable "Current")
├── Enemies (Node2D) — placeholder group
└── UI (CanvasLayer)
    └── Label (Score)
    └── TextureProgressBar (Health)
```

### Player Script (to test movement)
1. Select **Player** node → **Attach Script** → `player.gd`
2. Paste this:

```gdscript
extends CharacterBody2D

@export var speed = 200
@export var jump_velocity = -400
var gravity = 980

func _physics_process(delta):
    # Gravity
    if not is_on_floor():
        velocity.y += gravity * delta
    # Jump
    if Input.is_action_just_pressed("ui_accept") and is_on_floor():
        velocity.y = jump_velocity
    # Horizontal movement
    var direction = Input.get_axis("ui_left", "ui_right")
    velocity.x = direction * speed
    move_and_slide()
```

3. Press **F5** to run — you'll see your player moving with arrow keys

---

## 6. Configure Input Map

Project → Project Settings → Input Map

Add these (for WASD + Arrow keys):
| Action | Key 1 | Key 2 |
|--------|-------|-------|
| `move_left` | A | Left Arrow |
| `move_right` | D | Right Arrow |
| `move_up` | W | Up Arrow |
| `move_down` | S | Down Arrow |
| `jump` | Space | — |
| `interact` | E | — |
| `pause` | Escape | — |

---

## 7. Export Settings (Build Your Game)

Project → Export → Add... → Select platform:

### For Windows (.exe)
```
Binary Format: .exe (64-bit)
Include Pck: On (bundles assets in one file)
Embeds PCK: On (single-file export)
```
Click **Export Project** → Save as `MyGame.exe`

### For Web (HTML5 — play in browser)
```
Variant: Regular (not Threads — better compatibility)
Canvas Resize Policy: Project
```
Click **Export Project** → Save as `index.html`
Upload to **Itch.io** or **GitHub Pages** (free hosting)

---

## 8. Folder Structure Convention

```
MyFirstGame/
├── assets/
│   ├── sprites/        # .png sprite sheets, character sprites
│   ├── tilesets/       # .png tilemaps
│   ├── backgrounds/    # .png parallax backgrounds
│   ├── sfx/            # .wav/.ogg sound effects
│   └── music/          # .ogg background music
├── scenes/             # .tscn scene files
├── scripts/            # .gd script files
├── autoload/           # singleton scripts (inventory, save, etc.)
├── fonts/              # .ttf/.otf font files
├── ui/                 # theme files (.theme, .res)
└── exports/            # built .exe / web builds
```

---

## 9. Recommended 2D Settings Summary

| Setting | Value | Why |
|---------|-------|-----|
| Renderer | Mobile | Better performance on integrated GPUs |
| Window Mode | Windowed | Avoids crashes on low-end GPUs |
| Texture Filter | Nearest | Sharp pixel art (not blurry) |
| FPS Limit | 60 | Prevents GPU overheating |
| HDR 2D | Off | Saves VRAM |
| MSAA | Disabled | Saves GPU performance |
| VSync | On | Prevents screen tearing |
| Max FPS (editor) | 60 | Saves CPU when alt-tabbed |

---

## 10. Testing Your Setup

Do this checklist to verify everything works:
1. [ ] Godot opens without errors
2. [ ] Can create a new 2D scene
3. [ ] Can attach a script and run (F5)
4. [ ] Arrow keys move the player
5. [ ] Can import a .png sprite (no blur)
6. [ ] Can export to .exe (find it in exports folder)
7. [ ] .exe runs on its own outside Godot
8. [ ] Can export to HTML (open in Chrome)

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Godot crashes on launch | Use **Mobile** renderer, not Forward+ |
| Sprites look blurry | Set **Filter → Nearest** in Import tab |
| Game runs laggy | Set Display → Window → VSync → On; close Chrome |
| Godot won't open | Install VC++ redistributable: https://aka.ms/vs/17/release/vc_redist.x64.exe |
| Can't find AssetLib | Make sure you're online; use Godot 4.x (not 3.x) |
| Script won't attach | Make sure you selected a node first |
| Export fails | Project → Install Android SDK (for mobile) or just use Windows/Web |
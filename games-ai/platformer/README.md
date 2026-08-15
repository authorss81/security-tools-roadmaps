# Build a 2D Platformer (Mario/Celeste-Style) with ONLY Free Tools & Free AI

> Production-ready guide for indie devs, game jams, and hobbyists. Zero budget, maximum quality.
> Last updated: July 2026

---

## 1. Game Concept

**Genre:** Precision 2D platformer with light combat/collectathon (Celeste meets Mario). Side-scrolling, pixel art, 60 FPS target.

**What makes it production-quality:**
- **Juice:** Screen shake on landing/hit, particle trails, camera easing, squash-and-stretch on jump
- **Camera feel:** Smooth-follow with dead-zone box, look-ahead, clamp to level bounds
- **Controls:** Coyote time (~0.1s grace after ledge), jump buffering (~0.1s early input), variable jump height (release early = short hop)
- **Polish:** Animated UI, parallax backgrounds, fade transitions between levels, sound FX on every interaction
- **Save/load:** Level progress + collectibles via JSON
- **Performance:** Tilemap batching, sprite atlas, texture filter nearest, limit physics to 60 FPS

---

## 2. Complete Free Toolchain

### Engine: Godot 4.7+

| Feature | Godot 4.7 |
|---------|-----------|
| License | MIT - completely free, no royalties, no revenue share |
| Export | Windows, Linux, macOS, Web (HTML5), Android, iOS |
| 2D tools | TileMapLayer, CharacterBody2D, Camera2D smoothing, AnimationPlayer, Parallax2D |
| Scripting | GDScript (Python-like) or C# |
| Download | https://godotengine.org/download |
| Docs | https://docs.godotengine.org/en/stable/ |

**Why Godot over Unity/Unreal:** Free with no strings attached. Built-in 2D physics that Just Works. Tiny export size (~20 MB web build). No licensing fees ever.

### AI Code Assistants — Free Tier Comparison

| Tool | Free Tier Limits | Best For | URL |
|------|-----------------|----------|-----|
| **Claude (Anthropic)** | 5+ messages per 8h on Free; access to Claude 4 Sonnet. No project limit. | Best code generation quality. Use for full scripts | https://claude.ai |
| **ChatGPT** | GPT-4o mini: unlimited; GPT-4o: limited messages per 3h (~50). | Solid all-around. Good for debugging | https://chatgpt.com |
| **GitHub Copilot** | Free for verified students/OSS maintainers; otherwise 30-day trial | IDE autocomplete in VSCode | https://github.com/features/copilot |
| **Cursor** | Free tier: 2000 completions/month, 50 premium model requests/month | IDE with built-in AI for Godot | https://cursor.sh |
| **Bolt.new** | Free: 5 projects, 100 messages/month, web-only export | Rapid prototyping (not ideal for Godot) | https://bolt.new |
| **Replit** | Free tier: limited compute (0.5 vCPU, 1 GB RAM), 1 workspace | Online coding environment | https://replit.com |
| **Codeium/Windsurf** | Free: unlimited completions, 300 premium requests/month | VSCode extension, good GDScript autocomplete | https://codeium.com |

**Recommended stack:** Claude (free) for writing full GDScript files + Cursor (free tier) for in-editor help.

### AI Art Generation

| Tool | Free Tier | Best For | URL |
|------|-----------|----------|-----|
| **SEELE AI Sprite Generator** | Unlimited generations (logged in), no login for basic, PNG+JSON output | Sprite sheets, animated characters | https://www.seeles.ai/features/tools/sprite |
| **Leonardo AI** | 150 tokens/day free (~25-30 generations) | High-quality character art, backgrounds | https://leonardo.ai |
| **Stable Diffusion WebUI** | 100% free (local, requires GPU) | Full control, custom models | https://github.com/AUTOMATIC1111/stable-diffusion-webui |
| **CivitAI** | Free downloads of community models | Pixel art SD models, LoRAs | https://civitai.com |
| **SpriteCook** | Free credits monthly, no credit card | Game-ready sprites with engine export | https://www.spritecook.ai |
| **MyAIArt.io** | Free, no watermark | Pixel art sprites 16x16 to 128x128 | https://www.myaiart.io/features/ai-sprite-generator |

### AI Music & Sound Effects

| Tool | Free Tier | Best For | URL |
|------|-----------|----------|-----|
| **Treblo** | Unlimited free songs, Melodia v3 | Background music (actually free) | https://treblo.com |
| **ElevenLabs Music** | Generate free via web app | Vocals, instrumental tracks | https://elevenlabs.io/music |
| **MusicGen (Meta)** | Free open-source, run locally or via HF | Generative music loops | https://huggingface.co/spaces/facebook/MusicGen |
| **sfxr / jsfxr** | Free web tool, no login | 8-bit sound effects (jump, coin, hit) | https://sfxr.me |
| **OpenGameArt** | Free download (CC0/CC-BY) | Pre-made SFX and music tracks | https://opengameart.org |
| **Free Music Archive** | Free download | Royalty-free music by genre | https://freemusicarchive.org |

### Other Free Tools

| Tool | Purpose | URL |
|------|---------|-----|
| **Aseprite** (build yourself free) | Pixel art editor, sprite animation | https://github.com/aseprite/aseprite (build from source) |
| **Libresprite** | Free Aseprite fork | https://libresprite.github.io |
| **Krita** | Free painting/digital art | https://krita.org |
| **GIMP** | Free image editor, sprite sheet slicing | https://gimp.org |
| **Tiled** | Free tile map editor (alternative to Godot's) | https://thorbjorn.itch.io/tiled |
| **Audacity** | Free audio editor, SFX polishing | https://audacityteam.org |
| **OBS Studio** | Free recording/promo video | https://obsproject.com |
| **PixelComposer** | Free node-based pixel art tool | https://pixelcomposer.itch.io/pixel-composer |

---

## 3. Free Sprite Packs Table (10+ Direct Links)

| # | URL | Included | License | Notes |
|---|-----|----------|---------|-------|
| 1 | https://kenney.nl/assets/pixel-platformer | 200 sprites: tiles, characters, enemies, HUD, items (18x18) | CC0 | Best starter pack. Full platformer kit |
| 2 | https://kenney.nl/assets/pixel-platformer-blocks | 80 block tiles (platforms, bricks, slopes) | CC0 | Extension for the above |
| 3 | https://kenney.nl/assets/platformer-pack-remastered | HD platformer tiles, 2 characters, enemies, 64+ tiles | CC0 | Higher resolution remaster |
| 4 | https://ansimuz.itch.io/sunny-land-pixel-game-art | Player (6 anims), 3 enemies, parallax BG, items, FX, music | CC0 | Godot project included. Premium quality |
| 5 | https://opengameart.org/content/sunny-land-2d-pixel-art-pack | Same as above (mirror) + PSD files | CC0 | Direct OGA download |
| 6 | https://opengameart.org/content/kings-and-pigs | King Human (10 anims), Pigs (24 anims), 108-piece tileset | CC-BY 4.0 | Full combat platformer set. Aseprite src |
| 7 | https://opengameart.org/content/pixel-art-platformer-complete-pack | Tiles, characters, items, backgrounds | CC-BY 3.0 | Retro 8-bit style |
| 8 | https://pixel-frog.itch.io/pixel-adventure-2 | Player, enemies, tiles, items, FX, 3 environments | CC-BY 4.0 | Very popular. Colorful Mario-like |
| 9 | https://grafxkid.itch.io/mini-platformer-pack | Mini sprites, tiles, enemies, items (16x16) | CC0 | Tiny pixel perfect set |
| 10 | https://opengameart.org/content/platformer-art-pixel-redux | Full platformer tileset with grass, caves, snow | CC0 | Good for multi-biome levels |
| 11 | https://0x72.itch.io/16x16-industrial-tileset | Industrial/steampunk tiles, 100+ tiles | CC0 | Unique theme |
| 12 | https://elthen.itch.io/2d-pixel-art-platformer-pack | 380+ assets: 4 characters, tiles, items, enemies | CC0 | Massive pack, very polished |
| 13 | https://opengameart.org/content/generic-platformer-tileset-16x16-background | Generic tiles + backgrounds, 16x16 | CC0 | Good fallback tiles |
| 14 | https://opengameart.org/content/arcade-platformer-assets | Arcade beat-em-up style characters and tiles | CC0 | Brawler/platformer hybrid |
| 15 | https://opengameart.org/content/open-pixel-platformer-tiles-sprites | Jungle-themed platformer tiles + sprites | CC0 | Jungle/nature theme |

---

## 4. Step-by-Step Dev Path (5 Phases)

### Phase 1: Project Setup & Player Controller (Day 1)

**AI Prompt to Claude/ChatGPT:**
```
You are a Godot 4.7 expert. Write a complete GDScript script for a 2D platformer
player controller using CharacterBody2D. It must include:
- Speed = 200, jump_velocity = -350, gravity = 980
- Variable jump height (release early = fall fast)
- Coyote time (0.1s grace after leaving ledge)
- Jump buffering (0.1s input stored before landing)
- AnimatedSprite2D switching: idle, run, jump, fall
- Flip sprite based on direction
- Input map actions: "move_left" (A/Left), "move_right" (D/Right), "jump" (Space/W/Up)
- Use move_and_slide()
- All variables exported so they can be tweaked in inspector
- Type hints on everything
```

**Manual Steps:**
1. Download Godot 4.7 from godotengine.org
2. Create new project: `platformer_game/`
3. Create `scenes/Player.tscn` — root `CharacterBody2D`, children: `CollisionShape2D` (capsule), `AnimatedSprite2D`, `Camera2D`
4. Create `scripts/player.gd` with the AI-generated code
5. Import a sprite sheet (e.g. from Kenney Pixel Platformer), set up `SpriteFrames` in `AnimatedSprite2D` with animations: idle, run, jump, fall
6. Go to Project Settings > Input Map, add: `move_left` (A/Left), `move_right` (D/Right), `jump` (Space/W/Up)
7. Create a test level: `scenes/Level1.tscn` with `TileMapLayer` + a simple ground platform
8. Instance Player in Level1, hit F5 to test

**Player Controller Code (player.gd):**
```gdscript
extends CharacterBody2D

@export var speed: float = 200.0
@export var jump_velocity: float = -350.0
@export var gravity: float = 980.0

@export var coyote_time: float = 0.1
@export var jump_buffer_time: float = 0.1

var coyote_timer: float = 0.0
var jump_buffer_timer: float = 0.0
var was_on_floor: bool = false

@onready var anim: AnimatedSprite2D = $AnimatedSprite2D

func _physics_process(delta: float) -> void:
    handle_coyote_and_buffer(delta)
    apply_gravity(delta)
    handle_jump()
    handle_horizontal_movement()
    move_and_slide()
    handle_animation()
    handle_facing_direction()

func handle_coyote_and_buffer(delta: float) -> void:
    if is_on_floor():
        coyote_timer = coyote_time
    else:
        coyote_timer -= delta

    if Input.is_action_just_pressed("jump"):
        jump_buffer_timer = jump_buffer_time
    else:
        jump_buffer_timer -= delta

func apply_gravity(delta: float) -> void:
    if not is_on_floor():
        velocity.y += gravity * delta

func handle_jump() -> void:
    if jump_buffer_timer > 0.0 and coyote_timer > 0.0:
        velocity.y = jump_velocity
        jump_buffer_timer = 0.0
        coyote_timer = 0.0

    if Input.is_action_just_released("jump") and velocity.y < 0.0:
        velocity.y = velocity.y * 0.5

func handle_horizontal_movement() -> void:
    var direction: float = Input.get_axis("move_left", "move_right")
    velocity.x = direction * speed

func handle_animation() -> void:
    if not is_on_floor():
        if velocity.y < 0:
            anim.play("jump")
        else:
            anim.play("fall")
    elif velocity.x != 0:
        anim.play("run")
    else:
        anim.play("idle")

func handle_facing_direction() -> void:
    if velocity.x > 0:
        anim.flip_h = false
    elif velocity.x < 0:
        anim.flip_h = true
```

### Phase 2: Level Design & Camera (Day 2)

**AI Prompt:**
```
Write a Godot 4.7 GDScript for Camera2D attached to a player that provides:
- Position smoothing enabled (speed 5.0)
- Look-ahead: shift camera slightly in movement direction
- Dead zone box region (left=-50, top=-30, right=50, bottom=30)
- Limit the camera to level boundaries using limits
- Parallax support hint for background layers
```

**Camera Code (camera.gd):**
```gdscript
extends Camera2D

@export var look_ahead_distance: float = 50.0
@export var smoothing_speed: float = 5.0

@onready var player: CharacterBody2D = get_parent()

func _ready() -> void:
    position_smoothing_enabled = true
    position_smoothing_speed = smoothing_speed

func _process(_delta: float) -> void:
    var direction: float = Input.get_axis("move_left", "move_right")
    var target_offset: Vector2 = Vector2(direction * look_ahead_distance, 0)
    offset = offset.lerp(target_offset, 0.1)
```

**Manual Steps:**

1. **TileMapLayer:** Create ground, walls, platforms using the TileSet from your sprite pack
2. **Parallax Background:** Add `Parallax2D` node with 3 layers (far/sky, mid/mountains, near/trees). Use sprite pack backgrounds
3. **Level Transition:** Add `Area2D` at level exit, connect `body_entered` signal to `get_tree().change_scene_to_file("res://scenes/Level2.tscn")`
4. **One-way platforms:** In TileSet, mark specific tiles as "One Way" in physics layer settings
5. **Camera limits:** Set `camera.limit_*` values to match level size

### Phase 3: Enemies, Coins & Collectibles (Day 2-3)

**AI Prompt for enemy AI:**
```
Write a Godot 4.7 GDScript for a patrol enemy (CharacterBody2D) that:
- Moves left and right at speed 60
- Uses a RayCast2D pointed downward-left to detect floor edges
- Turns around when it reaches a ledge or hits a wall (RayCast2D or wall collision)
- Hurts player on contact (Area2D child for hitbox)
- Can be stomped (player lands on top = enemy dies, player bounces)
- Add an AnimatedSprite2D with idle and walk animations
- Export all relevant variables
```

**Enemy Code (enemy.gd):**
```gdscript
extends CharacterBody2D

@export var speed: float = 60.0
@export var gravity: float = 980.0

@onready var floor_check: RayCast2D = $FloorCheck
@onready var anim: AnimatedSprite2D = $AnimatedSprite2D
@onready var hitbox: Area2D = $Hitbox

var direction: int = -1

func _physics_process(delta: float) -> void:
    if not is_on_floor():
        velocity.y += gravity * delta

    if is_on_wall() or (floor_check and not floor_check.is_colliding()):
        direction *= -1
        anim.flip_h = direction > 0

    velocity.x = direction * speed
    move_and_slide()
    anim.play("walk")

func die() -> void:
    queue_free()
```

**Coin/Collectible Code (coin.gd):**
```gdscript
extends Area2D

signal coin_collected

func _ready() -> void:
    body_entered.connect(_on_body_entered)

func _on_body_entered(body: Node) -> void:
    if body is CharacterBody2D and body.has_method("collect_coin"):
        body.collect_coin()
        coin_collected.emit()
        queue_free()
```

**Manual Steps:**
1. Create `Enemy.tscn`: `CharacterBody2D` + `CollisionShape2D` + `AnimatedSprite2D` + `RayCast2D` (named `FloorCheck`, pointed down-left at 45 degrees) + `Area2D` (named `Hitbox`, slightly smaller than body)
2. Create `Coin.tscn`: `Area2D` + `CollisionShape2D` + `AnimatedSprite2D` (spinning animation)
3. Place enemies and coins in level using scene instances or the new Scene Paint Mode (press B in 2D editor)
4. Connect Hitbox's `body_entered` to check for player stomp (player velocity.y > 0 and player.global_position.y < enemy.global_position.y)

### Phase 4: UI, Health, Score & Game State (Day 3-4)

**AI Prompt:**
```
Write a Godot 4.7 autoload GameManager script that manages:
- Player lives (3), score, coins collected
- Methods: add_score(amount), take_damage(), heal(amount), add_coin(), reset_level()
- Save/load progress to user://save.json using FileAccess and JSON
- Signal on score_change, lives_change, game_over
- Persistent between scene changes (autoload)
Also write the HUD script (Control node) that:
- Shows hearts for lives, score text, coin count
- Updates via signals from GameManager
- Has a game over screen overlay with restart button
```

**Game Manager (game_manager.gd) — create as Autoload:**
```gdscript
extends Node

signal score_updated(new_score: int)
signal lives_updated(new_lives: int)
signal coins_updated(new_coins: int)
signal game_over

var score: int = 0
var lives: int = 3
var coins: int = 0
var current_level: String = "res://scenes/Level1.tscn"

func add_score(amount: int) -> void:
    score += amount
    score_updated.emit(score)

func add_coin() -> void:
    coins += 1
    score += 100
    coins_updated.emit(coins)
    score_updated.emit(score)

func take_damage() -> void:
    lives -= 1
    lives_updated.emit(lives)
    if lives <= 0:
        game_over.emit()
    else:
        reset_level()

func reset_level() -> void:
    get_tree().reload_current_scene()

func restart_game() -> void:
    score = 0
    lives = 3
    coins = 0
    score_updated.emit(score)
    lives_updated.emit(lives)
    coins_updated.emit(coins)
    get_tree().change_scene_to_file(current_level)

func save_progress() -> void:
    var data: Dictionary = {
        "score": score,
        "coins": coins,
        "current_level": current_level
    }
    var file: FileAccess = FileAccess.open("user://save.json", FileAccess.WRITE)
    file.store_string(JSON.stringify(data))

func load_progress() -> void:
    if not FileAccess.file_exists("user://save.json"):
        return
    var file: FileAccess = FileAccess.open("user://save.json", FileAccess.READ)
    var data: Dictionary = JSON.parse_string(file.get_as_text())
    score = data.get("score", 0)
    coins = data.get("coins", 0)
    current_level = data.get("current_level", "res://scenes/Level1.tscn")
```

**HUD Code (hud.gd):**
```gdscript
extends CanvasLayer

@onready var score_label: Label = $ScoreLabel
@onready var lives_container: HBoxContainer = $LivesContainer
@onready var coin_label: Label = $CoinLabel
@onready var game_over_screen: Control = $GameOverScreen

func _ready() -> void:
    var gm: Node = get_node("/root/GameManager")
    gm.score_updated.connect(_on_score_updated)
    gm.lives_updated.connect(_on_lives_updated)
    gm.coins_updated.connect(_on_coins_updated)
    gm.game_over.connect(_on_game_over)

func _on_score_updated(new_score: int) -> void:
    score_label.text = "SCORE: %d" % new_score

func _on_lives_updated(new_lives: int) -> void:
    for i in range(lives_container.get_child_count()):
        lives_container.get_child(i).visible = i < new_lives

func _on_coins_updated(new_coins: int) -> void:
    coin_label.text = "x %d" % new_coins

func _on_game_over() -> void:
    game_over_screen.visible = true
    get_tree().paused = true

func _on_restart_pressed() -> void:
    get_tree().paused = false
    get_node("/root/GameManager").restart_game()
```

**Manual Steps:**
1. Create `scripts/game_manager.gd`, go to Project > Project Settings > Autoload, add GameManager
2. Create `scenes/hud.tscn`: `CanvasLayer` > children: `ScoreLabel`, `LivesContainer` (HBoxContainer with heart sprites), `CoinLabel`, `GameOverScreen` (with restart button)
3. Add script to HUD, connect all signals
4. Instance HUD in main scene (or add it to autoload too)

### Phase 5: Audio, Juice & Polish (Day 4-5)

**AI Prompt:**
```
Write a Godot 4.7 AudioManager autoload script that:
- Has methods: play_sfx(path: String), play_music(path: String), stop_music()
- Uses AudioStreamPlayer2D for SFX and AudioStreamPlayer for music
- Fade in/out for music changes
- Volume sliders stored in config file
```

**Manual Steps:**
1. Use **sfxr** (https://sfxr.me) to generate: jump.wav, coin.wav, stomp.wav, hurt.wav, death.wav
2. Use **Treblo** (https://treblo.com) to generate background music: prompt = "upbeat 8-bit platformer adventure loop cheerful"
3. Create `ScreenShake` autoload:

```gdscript
extends Node

@onready var camera: Camera2D

func shake(intensity: float = 5.0, duration: float = 0.2) -> void:
    var tween: Tween = create_tween()
    tween.tween_method(_apply_shake, intensity, 0.0, duration)

func _apply_shake(value: float) -> void:
    if camera and camera is Camera2D:
        camera.offset = Vector2(randf_range(-value, value), randf_range(-value, value))
```

4. Add particle effects: `GPUParticles2D` for coin sparkle, landing dust, enemy death smoke
5. Add `ColorRect` fade transitions between levels:

```gdscript
# In main.gd or GameManager
func fade_to_level(level_path: String) -> void:
    var fade: ColorRect = $FadeOverlay
    var tween: Tween = create_tween()
    tween.tween_property(fade, "color:a", 1.0, 0.5)
    await tween.finished
    get_tree().change_scene_to_file(level_path)
    await get_tree().process_frame
    tween = create_tween()
    tween.tween_property(fade, "color:a", 0.0, 0.5)
```

---

## 5. AI Workflow — Exact Prompts

### Prompt Template: player.gd
```
Write a production-quality Godot 4.7 GDScript for a CharacterBody2D platformer player.
Requirements:
- Speed 250, jump_velocity -400, gravity 1200
- Coyote time 0.12s, jump buffer 0.1s
- Variable jump height (release early = cut velocity by 60%)
- AnimatedSprite2D with animations: idle, run, jump, fall
- Flip sprite horizontally
- Dash mechanic: double-tap shift, 500 speed for 0.2s, cooldown 0.5s
- Wall slide when touching wall in air, wall jump (jump away from wall)
- Input: arrow keys / WASD + Space

Write the COMPLETE script with type hints and exported variables.
Assume standard Godot 4.7 node setup.
```

### Prompt Template: enemy.gd
```
Write a Godot 4.7 GDScript for a patrolling enemy platformer character.
Must have:
- CharacterBody2D with gravity
- Moves at speed 50, turns at walls and ledges
- Two RayCast2Ds: one forward, one downward
- AnimatedSprite2D with walk animation
- Area2D child for hitbox detection
- Method die() called on stomp
- On stomp: play animation, disable collision, queue_free after 0.5s
- On touch: call GameManager.take_damage() (use get_node("/root/GameManager"))

Full script with type hints.
```

### Prompt Template: level.gd
```
Write a Godot 4.7 GDScript for a level scene root Node2D.
Features:
- On _ready: instantiate Player from packed scene at spawn point marker
- Connect coin Area2Ds to GameManager.add_coin()
- Connect level exit Area2D to change scene
- Spawn enemies from predefined Marker2D positions
- ParallaxBackground layers for depth
- Pause handling (ESC key)

Assume player.tscn, coin.tscn, enemy.tscn exist.
```

### Prompt Template: camera.gd
```
Write a Godot 4.7 Camera2D script for 2D platformer.
Features:
- Smooth follow with position_smoothing_speed = 5.0
- Look-ahead based on player direction (50px)
- Vertical dead zone (-60, 60) so camera doesn't bob on small bumps
- Limits set via exported vars: limit_left, limit_right, limit_top, limit_bottom
- Screen shake method: shake(intensity, duration) using Tween on offset
- Zoom in/out with mouse wheel for debug
```

### How to Iterate with AI
1. **Generate first draft** with the prompt above
2. **Test in Godot** — note errors and unexpected behavior
3. **Copy-paste error messages** to the AI: "Got error: Invalid call. Nonexistent function in base 'Nil'. Line 42. What's wrong?"
4. **Ask for modifications**: "Add double jump. Also make the jump feel floaty, reduce gravity to 800 and jump to -300."
5. **Refactor prompts**: "Split the player script into a state machine pattern with idle, run, jump, wall_slide states."
6. **Final polish**: "Add screen shake on landing. Detect landing when velocity.y changes from positive to 0 and was not on floor last frame."

---

## 6. Asset Pipeline — Mixing Free Sprites + AI Art

### Strategy: Use a consistent base from Kenney/OGA, supplement with AI

1. **Download Kenney Pixel Platformer** (CC0, 200 sprites) as your base art
2. **Use SEELE AI** for custom characters not in the pack:
   - Prompt: "pixel art ninja character side view idle running jumping 16-bit 32x32 transparent"
   - Download PNG + JSON sprite sheet
   - Import into Godot: drag PNG into FileSystem, set Texture Filter to Nearest
   - Use `AnimatedSprite2D` with `SpriteFrames` created from individual frames
3. **For backgrounds:** Use the parallax layers from the pack OR generate with Leonardo AI:
   - Prompt: "2D pixel art parallax background sunset mountains clouds side-scrolling platformer game art layers separated"
   - Slice into 3 layers in GIMP using layer masks
4. **Match pixel art styles:** Keep resolution consistent. If base pack is 16x16, generate AI sprites at 32x32 and scale down with nearest-neighbor in GIMP

### Generating Character Sheets with Leonardo AI
1. Go to https://leonardo.ai (150 tokens/day free)
2. Use preset: "Pixel Art"
3. Prompt structure: "sprite sheet [character description], [animation frames], [style], game asset, pixel art, [size], transparent background"
4. Example: "sprite sheet robot character, multiple frames idle walk jump attack, 16-bit pixel art, 32x32 each frame, transparent, game asset"
5. Download result, slice into individual frames in GIMP (guides > slice using grid)
6. Create SpriteFrames in Godot, drag each frame to the correct animation

### No Manual Pixel Editing Required
- AI generates full sprite sheets; just import, slice, and assign
- Adjust contrast/saturation in Godot's Import dock if styles don't match
- Use `modulate` property in Godot to recolor characters to match palette
- For tilesets: AI can generate a tile sheet, import as TileSet atlas, auto-slice in Godot

---

## 7. Free Tier Limitations & Workarounds

| Tool | Free Limit | Workaround |
|------|-----------|------------|
| **Claude** (Anthropic) | ~5 messages per 8 hours on Free tier | Use ChatGPT as backup; alternate between them. Write longer prompts (maximize output per message). Save code locally so you don't need to regenerate. |
| **ChatGPT** | GPT-4o mini: unlimited but weaker; GPT-4o: ~50/3h | Use GPT-4o for complex scripts, GPT-4o mini for boilerplate. Regenerate one function at a time. |
| **Cursor** | 2000 completions/month, 50 premium requests | Use free Codeium/Windsurf as alternative. Save completions for complex logic. |
| **Leonardo AI** | 150 tokens/day (~25-30 gens) | Generate in batches. Download all variations. Use SEELE AI (unlimited) for most sprites, save Leonardo for hero characters. |
| **SEELE AI** | Unlimited for logged in users | No workaround needed — this is truly free. Use as primary AI art tool. |
| **Treblo** | Unlimited free songs | No workaround needed. Just use it. |
| **Bolt.new** | Free: 5 projects, 100 messages, web only | Don't use Bolt for Godot projects — it's web-app focused. Use Claude/ChatGPT instead. |
| **Replit** | Free: 0.5 vCPU, 1 GB RAM, 1 workspace | Don't use Replit for Godot. Godot runs natively. Use Replit only for backend/leaderboard. |
| **GitHub Pages** | Free: 1 GB, 100 GB bandwidth/month, 500 MB files | Compress web export (gzip). Godot web export is ~15-25 MB. You can host multiple games. |
| **Itch.io** | Free uploads, unlimited bandwidth | No limits. Upload as many games as you want. |
| **Godot** | 100% free, no limits | No workaround needed. This is the whole point. |

---

## 8. Publishing — Free Deployment

### Option A: Itch.io (Recommended for games)

1. Sign up at https://itch.io (free)
2. Create a new project:
   - Click "Upload new project"
   - Set kind to "Game"
   - Choose visibility (draft or public)
3. Export from Godot:
   - Project > Export > Add... > Web (HTML5)
   - Enable "Include GDScript source" only if you want open source
   - Export Project > save as `platformer-web/index.html`
4. Upload to Itch.io:
   - Zip the `platformer-web` folder
   - Upload the zip
   - Set "This file will be played in the browser" under Embed Options
   - Viewport: 1280x720 (match your game resolution)
5. For Windows/macOS/Linux builds:
   - Export from Godot, zip the executable + `.pck` file
   - Upload as separate download

### Option B: GitHub Pages (Web export)

1. Create a repo on GitHub
2. Export Godot as Web (HTML5) into `docs/` folder (GitHub Pages default)
3. Push to GitHub
4. Go to repo Settings > Pages > Source: "Deploy from branch" > branch: main, folder: /docs
5. Your game is live at `https://yourusername.github.io/repo-name`
6. Pro tip: Use a `.nojekyll` file in the docs folder to prevent Jekyll processing

### Option C: Game Jolt

1. Sign up at https://gamejolt.com
2. Similar process to Itch.io
3. Good for game jam entries

### Godot Export Settings for Web
```
Publish as:
  Name: PlatformerGame
  Target: Web
  Vsync: On
  Include GDScript: Off (for production)
  Compress: Gzip
  HTML5:
    Export Mode: Full
    Custom HTML Shell: (optional, use Godot's default)
    Head: <meta name="viewport" content="width=device-width, initial-scale=1">
```

---

## 9. Production Readiness Checklist

### Camera & Effects
- [ ] Camera2D position smoothing enabled (speed 5-8)
- [ ] Camera dead zone to prevent micro-jitter
- [ ] Look-ahead in movement direction (50-100px)
- [ ] Camera limits set to level bounds
- [ ] Screen shake on: landing, damage, enemy death
- [ ] Parallax scrolling background (3+ layers)
- [ ] Particles: coin collect sparkle, landing dust, death explosion
- [ ] Squash-and-stretch on jump (scale tween)

### Sound Design
- [ ] Jump SFX (short, punchy)
- [ ] Landing SFX
- [ ] Coin/item collect SFX
- [ ] Damage SFX
- [ ] Enemy stomp SFX
- [ ] Death SFX
- [ ] Background music (loops smoothly)
- [ ] Volume controls in settings menu
- [ ] Music fade in/out on level start/end

### UI Polish
- [ ] Score display (top left, animated counter)
- [ ] Lives display (hearts, animated on loss)
- [ ] Coin counter with icon
- [ ] Game over screen with fade overlay
- [ ] Pause menu (ESC key, resume + quit buttons)
- [ ] Main menu with title animation
- [ ] Level select screen (optional)
- [ ] Settings: volume sliders, fullscreen toggle
- [ ] All UI uses same font style (Kenney Fonts)

### Save / Load
- [ ] Save progress after completing level
- [ ] Save file stores: current_level, score, coins, unlocked_levels
- [ ] Load on game start
- [ ] JSON format for readability
- [ ] Fallback defaults if save file corrupted

### Mobile Support
- [ ] Virtual joystick (on-screen touch controls)
- [ ] Touch jump button (right side)
- [ ] Responsive UI scaling
- [ ] Test on 16:9 and 18:9 aspect ratios
- [ ] Disable V-sync on mobile, fixed 60 FPS
- [ ] Touch input works alongside keyboard

### Controller Support
- [ ] Map: D-pad/left stick = move, A/B = jump, Start = pause
- [ ] Use Godot's built-in Input Map for joypad actions
- [ ] Auto-detect controller on connection
- [ ] UI navigable with controller

### Loading & Transitions
- [ ] Fade-to-black between levels (0.5s)
- [ ] Loading screen with progress bar (for larger levels)
- [ ] Preload heavy assets in main menu
- [ ] Resource.interactive_load for streaming

### Error Handling
- [ ] Graceful fallback if save file corrupt
- [ ] Error logging to file (user://error.log)
- [ ] Try/catch around file operations
- [ ] Default settings if config file missing
- [ ] Catch missing node references with is_instance_valid()

### Performance Optimization
- [ ] Texture filter: Nearest (no blurry pixels)
- [ ] Sprite atlas (pack sprites into single texture)
- [ ] Limit physics to 60 FPS (Engine.physics_jitter_fix = 0)
- [ ] Use TileMapLayer (not individual sprites) for level geometry
- [ ] Disable processing for off-screen enemies (VisibilityNotifier2D)
- [ ] Pool common objects (coins, particles) instead of instantiating/freeing
- [ ] Use AnimationPlayer instead of per-frame _process tweens where possible
- [ ] Set max FPS in Project Settings > Physics > Common

### Accessibility
- [ ] Color-blind friendly palette (avoid red/green only)
- [ ] Option to disable screen shake
- [ ] Subtitles for any dialogue
- [ ] Configurable controls

---

## 10. How to Improve (Post-Base Game)

### Advanced Enemy AI
- Use **finite state machine** pattern: idle, patrol, chase, attack, retreat
- AI prompt: "Godot 4.7 enemy state machine with states: idle (wait 2s), patrol (walk left/right, 60 speed), chase (follow player within 300px at 120 speed), attack (melee range 30px). Use RayCast2D for line-of-sight."
- Add flying enemies with sinusoidal movement
- Add bosses with phases (health threshold triggers new attack pattern)

### Boss Fights
- Boss: 3-phase fight with attack patterns
- Phase 1: walk + occasional projectile
- Phase 2: faster, adds jump slam (shockwave AOE)
- Phase 3: enraged, faster projectiles, charge attack
- Use `AnimationPlayer` for boss attack telegraphs
- Code structure: `BossStateMachine.gd` with `@export var phases: Array[Dictionary]`

### Procedural Levels
- Use Godot's `FastNoiseLite` for terrain height generation
- Place platforms, enemies, and coins using rules (minimum spacing, difficulty curve)
- Seed-based generation so levels are repeatable
- Simple approach: pre-made room chunks, connect them randomly

```gdscript
# procedural_chunk_manager.gd
@export var chunk_scenes: Array[PackedScene]
func generate_level(length: int) -> void:
    for i in range(length):
        var chunk: Node2D = chunk_scenes.pick_random().instantiate()
        chunk.position = Vector2(i * 640, 0)
        add_child(chunk)
```

### Achievements
- Store in `user://achievements.json`
- Track: levels beaten, total deaths, total coins, speedrun times
- Toast notification system: `$AchievementToast.show("Speed Demon!", "Beat Level 1 in under 60s")`

### Online Leaderboards
- Use **LootLocker** (free tier: 1000 players/month, no credit card) at https://lootlocker.com
- Or **PlayFab** (free tier: 100k MAU)
- Or build your own with **Supabase** free tier (500 MB DB, 50k rows)
- Godot HTTPRequest node to POST/GET scores as JSON

```gdscript
# leaderboard.gd
func submit_score(player_name: String, score: int) -> void:
    var http: HTTPRequest = HTTPRequest.new()
    add_child(http)
    http.request_completed.connect(_on_submit_done)
    var body: String = JSON.stringify({"name": player_name, "score": score})
    http.request("https://your-leaderboard.com/api/scores", ["Content-Type: application/json"], HTTPClient.METHOD_POST, body)
```

### Cutscenes
- Use Godot's `AnimationPlayer` on a `CanvasLayer` with `ColorRect` bars for cinematic letterbox
- Dialogue system: `RichTextLabel` with typewriter effect (Tween per character)
- Skip cutscene on any key press
- Store dialogue in `Resource` files (`.tres`):

```gdscript
class_name DialogueLine extends Resource
@export var speaker: String
@export var text: String
@export var portrait: Texture2D
```

### Level Editor
- Build in-game: toggle edit mode (F2 key)
- Click to place tiles, enemies, coins from a palette
- Save as `.tscn` or custom `.json` format
- Allow players to share levels via base64-encoded string
- Simple approach: use Godot's `TileMapLayer` editor at runtime

```gdscript
# level_editor.gd
func _input(event: InputEvent) -> void:
    if not editing: return
    if event is InputEventMouseButton and event.pressed:
        var tile_pos: Vector2i = tile_map.local_to_map(tile_map.get_local_mouse_position())
        tile_map.set_cell(tile_pos, 0, selected_tile_atlas_coords)
```

### More Polish Ideas
- **Water/liquid physics:** Area2D with different gravity (velocity.y *= 0.5), splash particles
- **Moving platforms:** Use `AnimatableBody2D` with Tween; player becomes child when standing on it
- **Checkpoints:** `Area2D` that saves position, player respawns there on death
- **Dash/double jump:** Add to player state machine
- **Wall jump:** Detect wall contact, allow jump away from wall with reduced gravity
- **Grappling hook:** Use `PinJoint2D` and `Line2D` for visual rope
- **Time trial mode:** Countdown timer, best time saved
- **Secret areas:** Hidden rooms accessible through breakable walls or alternate paths
- **Power-ups:** Temporary speed boost, invincibility star, double jump feather
- **NPCs:** Simple dialogue interactions using the dialogue system
- **Weather effects:** GPUParticles2D for rain/snow (use `FastNoiseLite` for wind variation)

---

## Appendix: Quick Start

```bash
# 1. Download Godot 4.7
https://godotengine.org/download

# 2. Clone or set up your project
mkdir platformer-game && cd platformer-game

# 3. Download Kenney Platformer Assets
# Download from https://kenney.nl/assets/pixel-platformer
# Extract into assets/sprites/

# 4. Create project.godot and start building
# Open Godot, create project, follow Phase 1 above

# 5. Generate music
# https://treblo.com - "upbeat 8-bit platformer adventure loop"

# 6. Generate SFX
# https://sfxr.me - jump, coin, stomp, hurt

# 7. Generate custom sprites
# https://www.seeles.ai - "pixel art hero with cape, idle run jump"

# 8. Publish to Itch.io
# Export as Web (HTML5), zip, upload to https://itch.io
```

---

## Appendix: File Structure

```
platformer-game/
  project.godot
  icon.png
  assets/
    sprites/
      kenney_pixel-platformer/
        tiles.png
        characters.png
        enemies.png
        items.png
      ai_generated/
        player_sheet.png
        player_sheet.json
    sounds/
      jump.wav
      coin.wav
      stomp.wav
      hurt.wav
      music.ogg
  scenes/
    Main.tscn
    Player.tscn
    Enemy.tscn
    Coin.tscn
    Level1.tscn
    Level2.tscn
    HUD.tscn
    MainMenu.tscn
    GameOver.tscn
  scripts/
    player.gd
    enemy.gd
    coin.gd
    camera.gd
    game_manager.gd
    hud.gd
    audio_manager.gd
    level.gd
  autoload/
    GameManager.gd
    AudioManager.gd
  ui/
    main_menu.gd
    settings_menu.gd
  levels/
    Level1.tscn
    Level2.tscn
  exports/
    web/
      index.html
      platformer_game.pck
      platformer_game.wasm
```

---

> **Total cost to build and ship this game: $0.**
> Godot, all sprite packs listed, all AI tools in free tiers, Itch.io hosting.
> You own everything you make. No royalties. No licensing fees. Ship it.

# Space Shooter - Build a Galaga/Geometry Wars Style 2D Arcade Shooter with FREE Tools & AI

## 1. Game Concept

Wave-based arcade space shooter inspired by Galaga, Geometry Wars, and classic SHMUPs.

**Core Loop:** Survive progressively harder enemy waves, collect power-ups, defeat bosses, and chase high scores.

**Features:**
- Player ship with smooth 360-degree movement (Geometry Wars style) or 2D horizontal/vertical (Galaga style)
- 10+ enemy types with unique movement patterns (sine wave, chase, straight-line, teleport, swarm)
- 5 boss fights at milestone waves
- 6 power-ups: Spread Shot, Laser, Homing Missiles, Shield, Speed Boost, Bomb (screen clear)
- Score attack with local high score persistence
- Particle-based explosions, screen shake, and visual feedback
- Main menu, game over screen, and wave progression
- Controller + keyboard support
- Mobile touch controls (optional)
- Sound effects + chiptune background music

## 2. Free Toolchain (Exact Limits — 2026)

| Tool | Free Tier Limits | Use in This Project |
|------|------------------|-------------------|
| **Godot 4.4+** | Unrestricted — open source, no limits | Game engine — main development |
| **Claude (opencode)** | Variable — depends on provider | AI-assisted coding, architecture, debugging |
| **ChatGPT Free** | GPT-4o mini — limited messages/day | Code snippets, asset prompts, debugging |
| **Bolt.new** | 1M tokens/month, 300K/day, 10MB uploads | Rapid prototyping UI, web builds |
| **Replit Starter** | 1,200 dev mins/month, 1 published app, 100 AI completions | Browser-based editing, quick tests |
| **GitHub Free** | Unlimited public repos, 2000 Actions mins/month | Version control, CI/CD, GitHub Pages |
| **Itch.io** | Free game hosting — no limits on uploads | Game distribution |
| **Supabase Free** | 500MB DB, 50K MAU, 5GB egress, 2 projects | Online leaderboard (if desired) |
| **bfxr.net** | Free, unlimited | Sound effects generation |
| **MusicGPT Free** | Limited monthly credits | Chiptune BGM generation |
| **Audacity** | Free, open source | Audio editing/trimming |

## 3. Sprite Pack Direct Links (Free / CC0)

### Ship & Enemy Sprites
1. **Kenney Space Shooter Remastered** — https://kenney.nl/assets/space-shooter-remastered (CC0, 295+ sprites)
2. **Kenney Space Shooter Extension** — https://kenney.nl/assets/space-shooter-extension (CC0, 270+ sprites)
3. **Kenney Pixel Shmup** — https://kenney-assets.itch.io/pixel-shmup (CC0, 128+ sprites)
4. **OpenGameArt 16x16 Ship Collection** — https://opengameart.org/content/1616-ship-collection (CC0, 100 ships)
5. **OpenGameArt 2D Spaceships** — https://opengameart.org/content/2d-spaceships (CC0)
6. **CraftPix Free Spaceship Pixel Art** — https://craftpix.net/freebies/free-spaceship-pixel-art-sprite-sheets/ (Free)
7. **Helianthus Games Space Shooter Kit** — https://helianthus-games.itch.io/pixel-art-space-shooter-kit (Free)

### Explosions & Effects
8. **BDragon1727 Free Effect Explosion 32x32** — https://bdragon1727.itch.io/free-effect-bullet-impact-explosion-32x32 (Free)
9. **Kenney Particle Pack** — https://kenney.nl/assets/particle-pack (CC0)

### Backgrounds & UI
10. **Kenney Space Shooter Redux (Backgrounds)** — https://kenney.nl/assets/space-shooter-redux (CC0)
11. **Foozle Void Environment Pack** — https://foozlecc.itch.io/void-environment-pack (Free CC0-like)

### Sounds & Music
12. **bfxr.net** — Generate SFX in browser (Free)
13. **Shononoki Bullet Hell Music Pack** — https://shononoki.itch.io/bullet-hell-music-pack (Free)
14. **FreeMusic AI 8-Bit Generator** — https://www.freemusic.ai/8-bit-music-generator (Free credits)

## 4. Five-Phase Step-by-Step with GDScript

### Phase 1: Player Ship Movement + Shooting

**Project Setup:**
- Download Godot 4.4+ from https://godotengine.org
- Create new project, import Kenney sprites into `assets/sprites/`
- Set viewport to 640x960 (portrait) or 1280x720 (landscape)

**player.gd** — Full script for the player ship:

```gdscript
extends Area2D

class_name Player

signal player_died

@export var speed: float = 400.0
@export var bullet_scene: PackedResource
@export var fire_rate: float = 0.15
@export var max_lives: int = 3

var can_fire: bool = true
var is_invulnerable: bool = false
var lives: int = max_lives
var current_weapon: String = "single"
var velocity: Vector2 = Vector2.ZERO

@onready var sprite: Sprite2D = $Sprite2D
@onready var muzzle: Marker2D = $Muzzle
@onready var fire_timer: Timer = $FireTimer
@onready var invuln_timer: Timer = $InvulnTimer
@onready var animation_player: AnimationPlayer = $AnimationPlayer

func _ready() -> void:
	fire_timer.wait_time = fire_rate
	Global.player = self

func _process(delta: float) -> void:
	var input_dir: Vector2 = Input.get_vector("move_left", "move_right", "move_up", "move_down")
	velocity = input_dir * speed
	position += velocity * delta
	position = position.clamp(Vector2.ZERO, get_viewport_rect().size)

	if Input.is_action_pressed("fire") and can_fire:
		_shoot()
		can_fire = false
		fire_timer.start()

	if Input.is_action_just_pressed("bomb") and Global.bombs > 0:
		_detonate_bomb()

func _shoot() -> void:
	if not bullet_scene:
		return
	var bullet: Bullet = bullet_scene.instantiate()
	bullet.global_position = muzzle.global_position
	bullet.direction = Vector2.UP
	get_parent().add_child(bullet)

	match current_weapon:
		"spread":
			for angle in [-15, 0, 15]:
				var b: Bullet = bullet_scene.instantiate()
				b.global_position = muzzle.global_position
				b.direction = Vector2.UP.rotated(deg_to_rad(angle))
				get_parent().add_child(b)
		"laser":
			var b: Bullet = bullet_scene.instantiate()
			b.global_position = muzzle.global_position
			b.direction = Vector2.UP
			b.is_laser = true
			b.speed = 1200.0
			get_parent().add_child(b)

func _on_fire_timer_timeout() -> void:
	can_fire = true

func _on_invuln_timer_timeout() -> void:
	is_invulnerable = false
	sprite.modulate = Color.WHITE

func take_damage() -> void:
	if is_invulnerable:
		return
	lives -= 1
	Global.update_hud.emit()
	if lives <= 0:
		player_died.emit()
		return
	is_invulnerable = true
	invuln_timer.start()
	animation_player.play("flash")

func _detonate_bomb() -> void:
	Global.bombs -= 1
	Global.update_hud.emit()
	for enemy in get_tree().get_nodes_in_group("enemies"):
		enemy.take_damage(999)
	for bullet in get_tree().get_nodes_in_group("enemy_bullets"):
		bullet.queue_free()
```

**Input Map Setup:**
- `move_left` → A / Left Arrow
- `move_right` → D / Right Arrow
- `move_up` → W / Up Arrow
- `move_down` → S / Down Arrow
- `fire` → Space / Z / Gamepad Right Trigger
- `bomb` → X / Gamepad Left Shoulder

**Player Scene Structure (`player.tscn`):**
```
CharacterBody2D (or Area2D)
├── Sprite2D (ship texture)
├── CollisionShape2D (ship hitbox)
├── Muzzle (Marker2D — bullet spawn point)
├── FireTimer (wait_time: 0.15, one_shot: true)
├── InvulnTimer (wait_time: 2.0, one_shot: true)
└── AnimationPlayer (flash animation)
```

### Phase 2: Enemy Waves + Patterns

**enemy.gd** — Base enemy with pattern system:

```gdscript
extends Area2D

class_name Enemy

signal died(points: int)

enum Pattern { STRAIGHT, SINE, CHASE, TELEPORT, SWARM }

@export var hp: int = 1
@export var speed: float = 150.0
@export var score_value: int = 100
@export var pattern: Pattern = Pattern.STRAIGHT
@export var bullet_scene: PackedScene
@export var fire_rate: float = 2.0
@export var sine_amplitude: float = 50.0
@export var sine_frequency: float = 2.0

var elapsed_time: float = 0.0
var start_position: Vector2
var can_fire: bool = true

@onready var sprite: Sprite2D = $Sprite2D
@onready var fire_timer: Timer = $FireTimer
@onready var explosion_scene: PackedScene = preload("res://scenes/explosion.tscn")

func _ready() -> void:
	start_position = position
	add_to_group("enemies")
	fire_timer.wait_time = fire_rate
	fire_timer.start()

func _process(delta: float) -> void:
	elapsed_time += delta
	match pattern:
		Pattern.STRAIGHT:
			position += Vector2.DOWN * speed * delta
		Pattern.SINE:
			position += Vector2.DOWN * speed * delta
			position.x = start_position.x + sin(elapsed_time * sine_frequency) * sine_amplitude
		Pattern.CHASE:
			if Global.player:
				var dir: Vector2 = (Global.player.position - position).normalized()
				position += dir * speed * delta
		Pattern.TELEPORT:
			if elapsed_time > 2.0:
				var vp_size: Vector2 = get_viewport_rect().size
				position = Vector2(randf_range(50, vp_size.x - 50), randf_range(-100, -50))
				elapsed_time = 0.0
		Pattern.SWARM:
			var swarm_offset: Vector2 = Vector2(sin(elapsed_time * 3.0 + start_position.x * 0.1),
				cos(elapsed_time * 2.0 + start_position.y * 0.1)) * 40.0
			position += (Vector2.DOWN * speed * 0.5 + swarm_offset) * delta

	if position.y > get_viewport_rect().size.y + 100:
		queue_free()

func _on_fire_timer_timeout() -> void:
	if not bullet_scene or not Global.player:
		return
	var bullet: Bullet = bullet_scene.instantiate()
	bullet.global_position = $Muzzle.global_position
	bullet.direction = (Global.player.position - position).normalized()
	bullet.is_enemy_bullet = true
	get_parent().add_child(bullet)

func take_damage(amount: int) -> void:
	hp -= amount
	if hp <= 0:
		_die()

func _die() -> void:
	died.emit(score_value)
	Global.score += score_value
	Global.update_hud.emit()
	if explosion_scene:
		var explosion: Node2D = explosion_scene.instantiate()
		explosion.global_position = global_position
		get_parent().add_child(explosion)
	_on_died()

func _on_died() -> void:
	queue_free()
```

**wave_manager.gd** — Wave progression controller:

```gdscript
extends Node

class_name WaveManager

signal wave_started(wave_number: int)
signal wave_completed(wave_number: int)
signal all_waves_completed

@export var enemy_scenes: Dictionary = {
	"basic": preload("res://scenes/enemies/basic_enemy.tscn"),
	"sine": preload("res://scenes/enemies/sine_enemy.tscn"),
	"chaser": preload("res://scenes/enemies/chaser_enemy.tscn"),
	"tank": preload("res://scenes/enemies/tank_enemy.tscn"),
}
@export var boss_scene: PackedScene

var current_wave: int = 0
var enemies_spawned: int = 0
var enemies_alive: int = 0
var wave_in_progress: bool = false
var spawn_points: Array[Vector2] = []

@onready var spawn_timer: Timer = $SpawnTimer

func _ready() -> void:
	_calculate_spawn_points()

func start_game() -> void:
	current_wave = 0
	Global.score = 0
	Global.lives = 3
	Global.bombs = 2
	start_next_wave()

func start_next_wave() -> void:
	current_wave += 1
	wave_in_progress = true
	enemies_spawned = 0
	wave_started.emit(current_wave)

	var wave_config: Dictionary = _get_wave_config(current_wave)
	spawn_timer.wait_time = wave_config.get("spawn_interval", 1.0)
	spawn_timer.start()

func _get_wave_config(wave: int) -> Dictionary:
	if wave % 5 == 0:  # Boss wave every 5
		return {"type": "boss", "spawn_interval": 0.0}
	var config: Dictionary = {
		"spawn_interval": max(0.3, 1.5 - wave * 0.05),
		"enemy_count": 5 + wave * 2,
		"types": ["basic"]
	}
	if wave >= 3:
		config.types.append("sine")
	if wave >= 5:
		config.types.append("chaser")
	if wave >= 7:
		config.types.append("tank")
	return config

func _on_spawn_timer_timeout() -> void:
	var config: Dictionary = _get_wave_config(current_wave)
	if config.get("type") == "boss":
		_spawn_boss()
		return
	if enemies_spawned >= config.get("enemy_count", 10):
		spawn_timer.stop()
		return
	var enemy_type: String = config.types[randi() % config.types.size()]
	var enemy: Enemy = enemy_scenes[enemy_type].instantiate()
	enemy.global_position = spawn_points[randi() % spawn_points.size()]
	enemy.died.connect(_on_enemy_died)
	add_child(enemy)
	enemies_spawned += 1
	enemies_alive += 1

func _spawn_boss() -> void:
	if not boss_scene:
		return
	var boss: Node2D = boss_scene.instantiate()
	boss.global_position = Vector2(get_viewport_rect().size.x / 2, -100)
	boss.tree_exited.connect(_on_boss_died)
	add_child(boss)

func _on_enemy_died(points: int) -> void:
	enemies_alive -= 1
	_check_wave_complete()

func _on_boss_died() -> void:
	_check_wave_complete()

func _check_wave_complete() -> void:
	if enemies_alive <= 0 and not spawn_timer.is_stopped() == false:
		wave_completed.emit(current_wave)
		wave_in_progress = false
		if current_wave >= 20:
			all_waves_completed.emit()
		else:
			await get_tree().create_timer(2.0).timeout
			start_next_wave()

func _calculate_spawn_points() -> void:
	var vp_size: Vector2 = get_viewport_rect().size
	for i in range(5):
		spawn_points.append(Vector2(vp_size.x * (i + 1) / 6, -50))
```

### Phase 3: Collision + Explosions + Screen Shake

**bullet.gd** — Universal bullet script:

```gdscript
extends Area2D

class_name Bullet

@export var speed: float = 600.0
@export var damage: int = 1
@export var is_laser: bool = false
@export var is_enemy_bullet: bool = false

var direction: Vector2 = Vector2.UP

func _ready() -> void:
	add_to_group("enemy_bullets" if is_enemy_bullet else "player_bullets")
	body_entered.connect(_on_body_entered)

func _process(delta: float) -> void:
	position += direction * speed * delta
	var vp_size: Vector2 = get_viewport_rect().size
	if position.y < -50 or position.y > vp_size.y + 50 or \
	   position.x < -50 or position.x > vp_size.x + 50:
		queue_free()

func _on_body_entered(body: Node) -> void:
	if is_enemy_bullet and body is Player:
		body.take_damage()
		queue_free()
	elif not is_enemy_bullet and body is Enemy:
		body.take_damage(damage)
		queue_free()
```

**explosion.gd** — Particle-based explosion:

```gdscript
extends Node2D

@export var particle_count: int = 20
@export var explosion_radius: float = 40.0
@export var lifetime: float = 0.6

func _ready() -> void:
	var gp: GPUParticles2D = $GPUParticles2D
	gp.amount = particle_count
	gp.lifetime = lifetime
	gp.explosiveness = 1.0
	gp.one_shot = true
	gp.emitting = true
	_screen_shake()
	await get_tree().create_timer(lifetime).timeout
	queue_free()

func _screen_shake() -> void:
	if not get_tree():
		return
	var camera: Camera2D = get_viewport().get_camera_2d()
	if camera and camera.has_method("shake"):
		camera.shake(0.3, 10.0)
```

**Camera with Screen Shake:**

```gdscript
extends Camera2D

class_name GameCamera

var shake_intensity: float = 0.0
var shake_duration: float = 0.0
var shake_remaining: float = 0.0

func shake(duration: float, intensity: float) -> void:
	shake_duration = duration
	shake_intensity = intensity
	shake_remaining = duration

func _process(delta: float) -> void:
	if shake_remaining > 0:
		shake_remaining -= delta
		offset = Vector2(
			randf_range(-shake_intensity, shake_intensity),
			randf_range(-shake_intensity, shake_intensity)
		)
	else:
		offset = Vector2.ZERO
```

### Phase 4: Power-ups + Scoring + Lives

**powerup.gd** — Collectible power-up system:

```gdscript
extends Area2D

class_name PowerUp

enum Type { SPREAD, LASER, HOMING, SHIELD, SPEED, BOMB }

@export var power_type: Type = Type.SPREAD

var fall_speed: float = 80.0

@onready var sprite: Sprite2D = $Sprite2D

func _ready() -> void:
	add_to_group("powerups")
	body_entered.connect(_on_collected)

	var colors: Dictionary = {
		Type.SPREAD: Color.YELLOW,
		Type.LASER: Color.RED,
		Type.HOMING: Color.CYAN,
		Type.SHIELD: Color.BLUE,
		Type.SPEED: Color.GREEN,
		Type.BOMB: Color.ORANGE,
	}
	sprite.modulate = colors.get(power_type, Color.WHITE)

func _process(delta: float) -> void:
	position += Vector2.DOWN * fall_speed * delta
	if position.y > get_viewport_rect().size.y + 50:
		queue_free()

func _on_collected(body: Node) -> void:
	if body is Player:
		match power_type:
			Type.SPREAD:
				body.current_weapon = "spread"
			Type.LASER:
				body.current_weapon = "laser"
			Type.HOMING:
				body.current_weapon = "homing"
			Type.SHIELD:
				body.is_invulnerable = true
				body.invuln_timer.start(5.0)
			Type.SPEED:
				body.speed = 600.0
				await get_tree().create_timer(5.0).timeout
				body.speed = 400.0
			Type.BOMB:
				Global.bombs += 1
		Global.update_hud.emit()
		queue_free()
```

**global.gd** — Autoload singleton for shared state:

```gdscript
extends Node

class_name Global

static var player: Player
static var score: int = 0
static var high_score: int = 0
static var lives: int = 3
static var bombs: int = 2
static var current_wave: int = 0

signal update_hud
signal game_over

const SAVE_PATH: String = "user://save.dat"
const HIGH_SCORE_KEY: String = "high_score"

func _ready() -> void:
	load_high_score()

func load_high_score() -> void:
	var config: ConfigFile = ConfigFile.new()
	var err: int = config.load(SAVE_PATH)
	if err == OK:
		high_score = config.get_value("game", HIGH_SCORE_KEY, 0)

func save_high_score() -> void:
	var config: ConfigFile = ConfigFile.new()
	config.set_value("game", HIGH_SCORE_KEY, high_score)
	config.save(SAVE_PATH)

func reset_game() -> void:
	score = 0
	lives = 3
	bombs = 2
	current_wave = 0
	update_hud.emit()
```

### Phase 5: HUD, Main Menu, Game Over, Sound + Music

**hud.gd** — Heads-up display:

```gdscript
extends CanvasLayer

@onready var score_label: Label = $ScoreLabel
@onready var lives_label: Label = $LivesLabel
@onready var wave_label: Label = $WaveLabel
@onready var bombs_label: Label = $BombsLabel

func _ready() -> void:
	Global.update_hud.connect(_on_update_hud)

func _on_update_hud() -> void:
	score_label.text = "SCORE: " + str(Global.score)
	lives_label.text = "LIVES: " + str(Global.lives)
	wave_label.text = "WAVE: " + str(Global.current_wave)
	bombs_label.text = "BOMBS: " + str(Global.bombs)
```

**main_menu.gd:**

```gdscript
extends Control

@onready var high_score_label: Label = $HighScoreLabel
@onready var start_button: Button = $StartButton

func _ready() -> void:
	high_score_label.text = "HIGH SCORE: " + str(Global.high_score)
	start_button.pressed.connect(_on_start_pressed)

func _on_start_pressed() -> void:
	get_tree().change_scene_to_file("res://scenes/game.tscn")
```

**game_over.gd:**

```gdscript
extends Control

@onready var final_score_label: Label = $FinalScoreLabel
@onready var high_score_label: Label = $HighScoreLabel
@onready var restart_button: Button = $RestartButton

func _ready() -> void:
	if Global.score > Global.high_score:
		Global.high_score = Global.score
		Global.save_high_score()
	final_score_label.text = "SCORE: " + str(Global.score)
	high_score_label.text = "HIGH SCORE: " + str(Global.high_score)
	restart_button.pressed.connect(_on_restart)
	$MenuButton.pressed.connect(_on_menu)

func _on_restart() -> void:
	Global.reset_game()
	get_tree().change_scene_to_file("res://scenes/game.tscn")

func _on_menu() -> void:
	Global.reset_game()
	get_tree().change_scene_to_file("res://scenes/main_menu.tscn")
```

**Audio Integration:**

```gdscript
# In main.gd or autoload
extends Node

@onready var music_player: AudioStreamPlayer = $MusicPlayer
@onready var sfx_player: AudioStreamPlayer = $SFXPlayer

func play_music(stream: AudioStream) -> void:
	music_player.stream = stream
	music_player.play()

func play_sfx(stream: AudioStream) -> void:
	sfx_player.stream = stream
	sfx_player.play()

func set_music_volume(db: float) -> void:
	music_player.volume_db = db

func set_sfx_volume(db: float) -> void:
	sfx_player.volume_db = db
```

**Audio Bus Layout:**
```
Master
├── Music (bus_index 1)
└── SFX (bus_index 2)
```

## 5. AI Prompts for Each Script

### player.gd prompt:
```
Write a Godot 4 GDScript for a Player class extending Area2D.
Requirements:
- 8-directional movement using Input.get_vector with configurable speed
- Mouse/gamepad aim support
- Weapon system: single, spread (3 angles), laser (piercing)
- Fire rate control via Timer (0.15s default)
- Invulnerability frames (2s) with sprite flash animation
- Lives system with signal emission on death
- Bomb mechanic that damages all enemies in group "enemies" and removes enemy bullets
- Clamp position to viewport bounds
- Exported vars for speed, fire_rate, max_lives
- Use @onready for node references
- Connect signals in _ready()
```

### enemy.gd prompt:
```
Write a Godot 4 GDScript for an Enemy class extending Area2D with class_name Enemy.
Requirements:
- HP, speed, score_value as exported vars
- Pattern enum: STRAIGHT, SINE, CHASE, TELEPORT, SWARM
- SINE: moves down + sinusoidal x oscillation (amplitude/frequency exported)
- CHASE: follows player position
- TELEPORT: randomly repositions every 2s
- SWARM: group movement with perlin-like offset
- Auto-fire at player with configurable fire_rate
- Emit died(points) signal on death
- Instantiate explosion scene at position on death
- Add to "enemies" group on ready
```

### wave_manager.gd prompt:
```
Write a Godot 4 GDScript for WaveManager extending Node.
Requirements:
- Wave progression: wave 1-3 basic, 4-6 add sine, 7-9 add chasers, 10+ add tanks
- Boss wave every 5 waves (instantiate boss_scene)
- Spawn interval decreases per wave (1.5s -> 0.3s minimum)
- Enemy count: 5 + wave * 2
- Track enemies_spawned and enemies_alive
- Emit wave_started(wave_number), wave_completed(wave_number), all_waves_completed
- 2s delay between waves
- Calculate 5 spawn points across top of screen
```

### bullet.gd prompt:
```
Write a Godot 4 GDScript for Bullet extending Area2D.
Requirements:
- Speed and damage exported vars
- is_enemy_bullet bool for team affiliation
- direction: Vector2 set on spawn
- Auto-queue_free when off-screen (50px margin)
- Connect body_entered: if enemy bullet hits Player -> call take_damage; if player bullet hits Enemy -> call take_damage(damage)
- Group assignment: "enemy_bullets" or "player_bullets"
```

### powerup.gd prompt:
```
Write a Godot 4 GDScript for PowerUp extending Area2D.
Requirements:
- Type enum: SPREAD, LASER, HOMING, SHIELD, SPEED, BOMB
- Fall downward at 80px/s
- Color-coded sprite modulate per type
- On body_entered with Player:
  - SPREAD/LASER/HOMING: set player.current_weapon
  - SHIELD: 5s invulnerability
  - SPEED: 5x speed boost for 5s
  - BOMB: increment Global.bombs
- Emit Global.update_hud on collect
- Auto-queue_free when off-screen
```

### hud.gd prompt:
```
Write a Godot 4 GDScript for HUD extending CanvasLayer.
Requirements:
- Labels for Score, Lives, Wave, Bombs (use $NodePath references)
- Connect to Global.update_hud signal in _ready()
- Format text as "SCORE: 0", "LIVES: 3", "WAVE: 1", "BOMBS: 2"
- Anchor top-left for score/lives, top-right for wave/bombs
```

## 6. Asset Pipeline — Mixing Free Sprites + AI Art

### Manual Sprite Workflow:
1. Download Kenney Space Shooter Remastered (295+ CC0 sprites)
2. Extract PNGs into `assets/sprites/`
3. Create `assets/sprites/player/`, `assets/sprites/enemies/`, `assets/sprites/effects/`, `assets/sprites/ui/`
4. Drag sprites into Godot; adjust pixels-per-meter and scale
5. Use AnimationPlayer for animated sprites (or AnimatedSprite2D)

### AI Art Generation Prompts:
Use ChatGPT Free, Claude, or Bing Image Creator:

**Player Ship Prompt:**
```
"Pixel art top-down spaceship, blue and white color scheme, 64x64 pixels, sleek fighter design, 4 directional frames, transparent background, game sprite sheet"
```

**Enemy Ship Prompt:**
```
"Pixel art enemy spaceship sprite, red and dark gray, 48x48 pixels, menacing alien design, top-down view, transparent background, retro arcade style"
```

**Explosion Spritesheet Prompt:**
```
"Pixel art explosion animation spritesheet, 8 frames, orange and yellow, 64x64 each frame, transparent background, cartoon fire style"
```

**Background Prompt:**
```
"Starfield space background, 640x960 pixels, dark blue with stars and nebula clouds, seamless tile, parallax ready, game background"
```

### AI Music Generation:
1. Go to https://www.freemusic.ai/8-bit-music-generator
2. Prompt: "Upbeat chiptune arcade music, 8-bit style, 120 BPM, loopable, space shooter theme, energetic"
3. Generate multiple: menu theme, gameplay loop, boss theme, game over
4. Trim in Audacity, export as OGG (Godot's preferred format)

### AI Sound Effects:
1. Go to https://bfxr.net
2. Generate: laser shoot, explosion, power-up collect, enemy hit, player hit, bomb detonate
3. Export as WAV, convert to OGG in Audacity

## 7. Free Tier Limitations Table with Workarounds

| Service | Limitation | Workaround |
|---------|-----------|------------|
| **Godot** | None — fully free | N/A |
| **GitHub** | 2000 Actions min/month free | Use for CI only; build locally |
| **Itch.io** | 1GB file size limit per upload | Keep builds lean; use external hosting for downloads |
| **Bolt.new** | 1M tokens/month, 10MB uploads | Write core logic in Godot; use Bolt only for UI prototypes |
| **Replit** | 1,200 dev mins/month, 1 published app | Use for quick Godot GDScript tests in web; main dev in Godot locally |
| **Supabase** | 500MB DB, auto-pause after 7 days idle | Use ping service (cron-job.org free) to keep alive |
| **ChatGPT Free** | Limited GPT-4o mini messages | Use Claude via opencode for sustained sessions |
| **MusicGPT Free** | Limited credits/month | Generate all tracks at once; reuse loops |
| **bfxr.net** | Unlimited | Use for all SFX |
| **CraftPix Free** | Requires login, limited downloads | Download once; redistribute in your project files |
| **Kenney Assets** | CC0 — unlimited | Best source, no workarounds needed |

## 8. Publishing

### Itch.io Publishing (Free):
1. Create account at https://itch.io
2. Click "Upload new project"
3. Set kind to "Game"
4. Set pricing to "Free" (or "Pay what you want")
5. In Godot: Project → Export → Add platform (Windows, Linux, Web)
6. Export to `builds/` folder
7. Create ZIP of export folder
8. Upload to Itch.io:
   - Add screenshots and GIFs
   - Set tags: "space-shooter", "arcade", "2d", "godot"
   - Write short description
   - Set controls in instructions
9. For HTML5/Web: Export as HTML5, upload the folder

### GitHub Pages (HTML5 Build + Dev Site):
1. Push project to GitHub
2. Create branch `gh-pages` or use GitHub Actions
3. Add workflow `.github/workflows/export.yml`:

```yaml
name: Export Godot to GitHub Pages
on:
  push:
    branches: [main]
jobs:
  export:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Export
        uses: firebelley/godot-export-action@v6
        with:
          godot_version: 4.4
          export_preset: "HTML5"
      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./build/web
```

4. Enable GitHub Pages in repo Settings → Pages (source: gh-pages branch)

## 9. Production Checklist

### Core Gameplay
- [ ] Player movement smooth with no jitter (use delta)
- [ ] Shooting with auto-fire or hold-to-fire
- [ ] Enemy wave system with increasing difficulty
- [ ] Collision detection works for player/enemy/bullets
- [ ] Power-ups drop from enemies (20% chance) and apply correctly
- [ ] Bomb mechanic clears screen
- [ ] Score increments on enemy kill
- [ ] Lives decrement on hit; invulnerability frames work
- [ ] Game over triggers when lives = 0 and all animations finish

### Visual Polish
- [ ] Particle systems for explosions (GPUParticles2D)
- [ ] Screen shake on heavy damage events
- [ ] Ship thruster particle trail effect
- [ ] Starfield parallax background (2-3 layers at different scroll speeds)
- [ ] Glow effect on bullets (WorldEnvironment + Glow)
- [ ] Enemy death animation before removal
- [ ] Power-up color coding and glow
- [ ] Wave transition announcement with tween animation
- [ ] Boss entrance animation

### Audio
- [ ] SFX for: shoot, hit, explosion, power-up, bomb, menu click, game over
- [ ] Background music for: menu, gameplay, boss, game over
- [ ] Volume sliders in options menu (Master, Music, SFX)
- [ ] Audio bus layout with correct routing

### Controls
- [ ] Keyboard: WASD + Space/Z + X
- [ ] Controller: Left stick + A/B + RT/LB (map in Input Map)
- [ ] Remappable controls (settings menu)
- [ ] Mobile touch controls (virtual joystick + fire/bomb buttons)

### Persistence
- [ ] High score saved via ConfigFile to user://
- [ ] Sound/music volume persisted
- [ ] Save data loads on startup

### UI/UX
- [ ] Main menu with Start, High Score, Credits buttons
- [ ] HUD shows score, lives, wave, bombs
- [ ] Game over screen with final score, high score, restart/menu buttons
- [ ] Pause menu (ESC key) with Resume/Quit
- [ ] Options menu (volume sliders)
- [ ] Credits screen

## 10. How to Improve

### Boss Fights
- Create boss enemy with 50+ HP, phase transitions at 50% and 25% HP
- Attack patterns: aimed shots, spread bursts, summoned minions, laser sweep
- Giant sprites from Kenney extension packs or scale up existing enemies

```gdscript
extends Enemy

class_name Boss

var phase: int = 1

func _process(delta: float) -> void:
	super(delta)
	if hp < max_hp * 0.5 and phase == 1:
		phase = 2
		_change_pattern()
	if hp < max_hp * 0.25 and phase == 2:
		phase = 3
		_change_pattern()

func _change_pattern() -> void:
	fire_rate *= 0.7
	speed *= 1.2
	sprite.modulate = Color.RED
```

### Upgrade Shop
- Between waves or on game over, spend score on permanent upgrades
- Options: +1 life, +fire rate, +damage, +bomb count, shield start
- Store state in Global singleton with save/load

### Endless Mode
- After wave 20, continue infinitely with no boss waves
- Difficulty continues scaling: spawn rate increases, enemy HP scales
- Track "endless wave" separately in HUD

### Online Leaderboards (Supabase Free)

```gdscript
# Leaderboard.gd
extends Node

const SUPABASE_URL: String = "https://your-project.supabase.co"
const SUPABASE_KEY: String = "your-anon-key"

func submit_score(player_name: String, score: int) -> void:
	var http: HTTPRequest = HTTPRequest.new()
	add_child(http)
	var body: Dictionary = {
		"name": player_name,
		"score": score,
		"wave": Global.current_wave
	}
	var json_body: String = JSON.stringify(body)
	var headers: PackedStringArray = [
		"Content-Type: application/json",
		"apikey: " + SUPABASE_KEY
	]
	http.request_completed.connect(_on_submit_done)
	http.request(SUPABASE_URL + "/rest/v1/leaderboard",
		headers, HTTPClient.METHOD_POST, json_body)

func fetch_top_scores(callback: Callable) -> void:
	var http: HTTPRequest = HTTPRequest.new()
	add_child(http)
	http.request_completed.connect(func(_r, _c, _h, body):
		var data: Array = JSON.parse_string(body.get_string_from_utf8())
		callback.call(data)
	)
	http.request(SUPABASE_URL + "/rest/v1/leaderboard?order=score.desc&limit=10")
```

- Supabase table: `leaderboard` with columns `id`, `name`, `score`, `wave`, `created_at`
- Enable RLS with anon insert/select policies

### Co-op Mode
- Second player with P2 controls (Arrow keys + / or gamepad)
- Shared screen; enemies scale HP by 1.5x
- Player 2 spawns at different position

### Level Editor
- Export enemy wave configurations to JSON files
- Simple in-game editor: place enemies, set patterns, save as custom wave
- Load custom wave files from `user://custom_waves/`

### Weapon Variety
- **Laser:** Piercing beam, 1.5s cooldown, high damage
- **Spread:** 3-way shot, medium damage, great for groups
- **Homing:** Targets nearest enemy, lower damage but auto-aim
- **Missile:** Explodes on contact (area damage)
- **Railgun:** High damage, slow fire rate, penetrates all enemies

```gdscript
# Add to player.gd _shoot()
match current_weapon:
	"homing":
		var targets: Array = get_tree().get_nodes_in_group("enemies")
		if targets.size() > 0:
			var nearest: Enemy = targets[0]
			for e in targets:
				if global_position.distance_squared_to(e.global_position) < \
				   global_position.distance_squared_to(nearest.global_position):
					nearest = e
			var b: Bullet = bullet_scene.instantiate()
			b.global_position = muzzle.global_position
			b.is_homing = true
			b.target = nearest
			get_parent().add_child(b)
```

### Visual Polish Ideas
- **Trails:** Line2D or GPUParticles2D behind player and fast bullets
- **Glow:** WorldEnvironment with glow enabled; glow layer on bullet material
- **Parallax:** 3 background layers at 0.2x, 0.5x, 0.8x scroll speed
- **Hit Flash:** White modulate flash on enemies for 0.1s on hit
- **Score Popup:** Floating +100 text that fades up
- **Ship Engine Flame:** Animated sprite or particles behind ship
- **Warp-in Effect:** Enemies scale from 0 to 1 with alpha fade on spawn
- **Boss Health Bar:** ColorRect at top of screen during boss waves
- **Wave Banner:** "WAVE 5" animated text with scale/alpha tween

### GDScript Organization Tips
- Use `class_name` for commonly referenced classes
- Use Autoload (Global) for shared state — avoid pass-through chains
- Use groups ("enemies", "player_bullets", "enemy_bullets") for batch operations
- Use Signals instead of direct coupling between systems
- Prefer `@export` for tunable values — adjust in Inspector without re-coding
- Use `@onready` for all node references (fails fast on null)

---

**License:** MIT — Free to use, modify, and distribute. Asset licenses vary (see individual packs — most are CC0).

**Built with Godot 4.4+ | GDScript | Free AI Tools | CC0 Assets**

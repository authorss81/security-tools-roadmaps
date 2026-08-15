# 2D Roguelike Dungeon Crawler — Production Guide

> **Style:** Binding of Isaac / Enter the Gungeon  
> **Engine:** Godot 4.4+ (free, MIT license)  
> **Language:** GDScript  
> **Budget:** $0 (all tools + assets free)  
> **Target:** Itch.io + GitHub Pages (HTML5)

---

## Table of Contents

1. [Game Concept](#1-game-concept)
2. [Free Toolchain & AI Limits](#2-free-toolchain--ai-limits)
3. [12+ Free Sprite Pack Links](#3-12-free-sprite-pack-direct-links)
4. [5-Phase Step-by-Step Build (with GDScript)](#4-5-phase-step-by-step-build-with-gdscript)
5. [AI Prompts for Every Script](#5-ai-prompts-for-every-script)
6. [Asset Pipeline: Free Sprites + AI Art](#6-asset-pipeline-free-sprites--ai-art)
7. [Free Tier Limitations Table](#7-free-tier-limitations-table)
8. [Publishing on Itch.io + GitHub Pages](#8-publishing-on-itchio--github-pages)
9. [Production Checklist](#9-production-checklist)
10. [How to Improve](#10-how-to-improve)

---

## 1. Game Concept

**Premise:** A top-down 2D roguelike where the player descends through procedurally generated dungeon floors, defeats enemies, collects items, fights bosses, and dies permanently.

### Core Systems

| System | Description |
|--------|-------------|
| Procedural Rooms | BSP algorithm splits dungeon into rooms + corridors. Each room has a type: combat, treasure, boss, shop, secret. |
| Real-time Combat | WASD movement, mouse aim + click to shoot, Space to dodge roll (i-frames). |
| Enemy AI | Chase, strafe-shoot, patrol, spawn-minion patterns with finite-state machines. |
| Items & Pickups | Passive stat upgrades, active items (Q to use), health, keys, coins. |
| Room Clearing | Doors lock when entering a room, unlock when all enemies dead. |
| Permadeath & Runs | Death = run over. Meta-progression unlocks persist across runs (characters, starting items). |
| Boss Rooms | Every 3 floors, a boss room. Bosses have multi-phase attack patterns. |
| Floor Themes | Dungeon (stone), Catacombs (bone/blue), Library (purple/book), Hell (red/fire). |

### Controls

| Key | Action |
|-----|--------|
| WASD | Move |
| Mouse | Aim |
| Left Click | Shoot |
| Space | Dodge Roll |
| Q | Use active item |
| E | Interact (shop, chest) |
| Tab | Open inventory |
| M | Minimap toggle |
| Esc | Pause / Settings |

---

## 2. Free Toolchain & AI Limits

### Primary Tools

| Tool | Use | Cost | Free Tier |
|------|-----|------|-----------|
| **Godot 4.4+** | Game engine | $0 (MIT) | Full engine, unlimited |
| **GDScript** | Scripting | $0 | Built into Godot |
| **Aseprite** | Sprite editing | Free | Can use free trial or [aseprite-free](https://github.com/aseprite-community/aseprite) community build |
| **Krita** | Texture/pixel art | $0 | Full-featured, no limits |
| **GIMP** | Image editing | $0 | Full-featured |
| **Audacity** | Sound effects | $0 | Full-featured |
| **BFXR** | SFX generation | $0 | Free web/app |
| **ChipTone** | Chiptune SFX | $0 | Free web |
| **Tiled** | Tile map editor | $0 | Full-featured |
| **Inkscape** | Vector/splash art | $0 | Full-featured |

### Free AI Coding Tools (Exact Limits as of July 2026)

| AI Tool | Free Limit | Best For | Workaround |
|---------|-----------|----------|------------|
| **Claude (claude.ai)** | ~20-30 messages/day (Sonnet 4.6), resets midnight UTC. No code API on free tier. | GDScript generation, architecture planning | Split work across multiple sessions. Use prompt templates below to minimize iterations. |
| **Cursor (Hobby tier)** | 2,000 completions/month + 50 slow premium requests + 200 Tab completions. | Writing GDScript in-editor with AI autocomplete | Reserve premium requests for complex logic. Use completions for boilerplate. |
| **Bolt.new (Free)** | 1M tokens/month, 300K daily cap, 10MB uploads. | Rapid prototyping of smaller Godot scripts | Export scripts as files and paste into Godot. Use concise prompts. |
| **GitHub Copilot (Free)** | 50 requests/month, 2,000 completions. | GDScript snippets | Use only for short completions. |
| **Gemini (Google AI Studio)** | 60 requests/minute (Flash 2.0), free for non-commercial. | Generating tilemaps, asset descriptions | Rate limit is generous — use for bulk content generation. |
| **ChatGPT (Free)** | ~40 messages/3 hours (GPT-4o mini). GPT-5 limited. | Prompt engineering, system design | Use for architecture discussions, not code generation (hallucinates GDScript). |
| **OpenAI API (Free credits)** | $5 credit on signup (expires 3 months). | Batch code generation | Use credits efficiently — one large prompt vs many small ones. |
| **Workik AI (Free)** | Free Godot code generator (web). | GDScript generation | Good for single-file generation, limited context. |
| **Sorceress WizardGenie** | 100 free credits on signup. | Godot-specific code generation | Best Godot-specialized AI — knows TileMapLayer, signals, `_input`. |
| **Ziva (Godot AI)** | Free tier available (limited). | In-editor Godot AI assistant | Installs as plugin inside Godot editor. |

### Free AI Art Tools (Exact Limits)

| AI Tool | Free Limit | Best For |
|---------|-----------|----------|
| **Sorceress Quick Sprites** | 100 starter credits (9 credits/gen) | Pixel art sprite sheets |
| **Stable Diffusion (local)** | Unlimited (runs on your GPU) | Any art, requires setup |
| **Playground AI** | 500 images/month | Prompts → sprites |
| **Leonardo AI** | 150 tokens/day | RPG character sprites |
| **Craiyon** | Unlimited (watermarked) | Concept art |

### Free Audio Tools

| Tool | Type | Cost |
|------|------|------|
| **BFXR** | SFX generator | Free |
| **ChipTone** | Chiptune SFX | Free |
| **MusicGen (Meta)** | AI music generation | Free (local or Colab) |
| **Jukebox (OpenAI)** | AI music | Free (local) |
| **Freesound.org** | CC0 SFX library | Free |
| **Pixabay Music** | Royalty-free tracks | Free |

---

## 3. 12+ Free Sprite Pack Direct Links

All packs below are **CC0, MIT, or free-to-use** for commercial projects.

### Dungeon Tilesets

| # | Pack | Format | License | Link |
|---|------|--------|---------|------|
| 1 | **16x16 DungeonTileset II** (0x72) | 16x16 PNG | CC0 | https://0x72.itch.io/dungeontileset-ii |
| 2 | **Kenney Roguelike/RPG Pack** | 16x16 PNG | CC0 | https://kenney.nl/assets/roguelike-rpg-pack |
| 3 | **Kenney Micro Roguelike** (320+ sprites) | 8x8 PNG | CC0 | https://kenney-assets.itch.io/micro-roguelike |
| 4 | **Kenney Tiny Dungeon** (130+ sprites) | 16x16 PNG | CC0 | https://kenney-assets.itch.io/tiny-dungeon |
| 5 | **OpenGameArt Dungeon Tileset** (Calciumtrice) | 16x16 PNG | CC-BY 3.0 | https://opengameart.org/content/dungeon-tileset-1 |
| 6 | **OpenGameArt Dungeon Tileset** (Buch) | 16x16 PNG | CC0 | https://opengameart.org/content/dungeon-tileset |
| 7 | **Pixel Crawler Free Pack** (Anokolisa, 500+ sprites) | 16x16 PNG | Free | https://anokolisa.itch.io/free-pixel-art-asset-pack-topdown-tileset-rpg-16x16-sprites |

### Characters & Enemies

| # | Pack | Format | License | Link |
|---|------|--------|---------|------|
| 8 | **32rogues** (Seth, fantasy tiles + chars) | 32x32 PNG | Free | https://sethbb.itch.io/32rogues |
| 9 | **Roguelike 300+ Asset Pack** (ibirothe, animated) | 16x16 1-bit | Free | https://ibirothe.itch.io/roguelike1bit16x16assetpack |
| 10 | **Monochrome RPG** (Kenney, 130+ sprites) | 16x16 PNG | CC0 | https://kenney-assets.itch.io/monochrome-rpg |

### Items, UI, & Effects

| # | Pack | Format | License | Link |
|---|------|--------|---------|------|
| 11 | **1-Bit Pack** (Kenney, 1,000+ tiles) | 16x16 PNG | CC0 | https://kenney-assets.itch.io/1-bit-pack |
| 12 | **Board Game Icons** (Kenney, 250+ icons) | PNG | CC0 | https://kenney-assets.itch.io/board-game-icons |
| 13 | **Input Prompts Pixel 16x** (Kenney) | 16x16 PNG | CC0 | https://kenney-assets.itch.io/input-prompts-pixel-16 |
| 14 | **Urizen 1Bit Tileset** (5,500+ tiles) | 12x12 | CC0 | https://vurmux.itch.io/urizen-onebit-tileset |
| 15 | **Minifantasy Forgotten Plains** (380 tiles) | 8x8 | CC0 | https://krishna-palacio.itch.io/minifantasy-forgotten-plains |

### Bosses & Monsters

| # | Pack | Format | License | Link |
|---|------|--------|---------|------|
| 16 | **Monster Builder Pack** (Kenney, 170+ sprites) | PNG | CC0 | https://kenney-assets.itch.io/monster-builder-pack |
| 17 | **Kings and Pigs** (Pixel Frog) | PNG | CC0 | https://pixelfrog-assets.itch.io/kings-and-pigs |

---

## 4. 5-Phase Step-by-Step Build (with GDScript)

### Phase 1: Procedural Room Generation (BSP Algorithm)

> **Algorithm:** Binary Space Partitioning splits a rectangle into sub-rectangles, then carves rooms and connects them with corridors.

**File:** `scripts/room_generator.gd`

```gdscript
extends Node

class_name RoomGenerator

const TILE_FLOOR := Vector2i(1, 0)
const TILE_WALL := Vector2i(0, 0)
const TILE_DOOR := Vector2i(2, 0)

var rng := RandomNumberGenerator.new()
var seed_value: int = 0

var _tilemap: TileMapLayer
var _room_tiles: Dictionary = {}
var _rooms: Array[Rect2i] = []
var _corridors: Array[Rect2i] = []

func generate(tilemap: TileMapLayer, map_size: Vector2i, _seed: int = -1) -> void:
	if _seed >= 0:
		seed_value = _seed
		rng.seed = _seed
	else:
		seed_value = randi()
		rng.seed = seed_value

	_tilemap = tilemap
	_rooms.clear()
	_corridors.clear()
	_room_tiles.clear()

	tilemap.clear()

	_fill_area(Rect2i(Vector2i.ZERO, map_size), TILE_WALL)
	_split(Rect2i(Vector2i.ZERO, map_size), 6)
	_carve_rooms()
	_carve_corridors()

func _fill_area(area: Rect2i, tile: Vector2i) -> void:
	for x in range(area.position.x, area.end.x):
		for y in range(area.position.y, area.end.y):
			_tilemap.set_cell(Vector2i(x, y), 0, tile)

func _split(rect: Rect2i, depth: int) -> void:
	if depth <= 0:
		_rooms.append(rect)
		return

	var split_h: bool = rect.size.x < rect.size.y if rng.randi_range(0, 1) == 0 else rect.size.y < rect.size.x
	var max_size: int = (rect.size.y if split_h else rect.size.x) * 0.7
	var min_size: int = (rect.size.y if split_h else rect.size.x) * 0.3
	if max_size <= min_size:
		_rooms.append(rect)
		return

	var split_pos: int = rng.randi_range(min_size, max_size)

	if split_h:
		var top := Rect2i(rect.position, Vector2i(rect.size.x, split_pos))
		var bottom := Rect2i(Vector2i(rect.position.x, rect.position.y + split_pos),
			Vector2i(rect.size.x, rect.size.y - split_pos))
		_split(top, depth - 1)
		_split(bottom, depth - 1)
	else:
		var left := Rect2i(rect.position, Vector2i(split_pos, rect.size.y))
		var right := Rect2i(Vector2i(rect.position.x + split_pos, rect.position.y),
			Vector2i(rect.size.x - split_pos, rect.size.y))
		_split(left, depth - 1)
		_split(right, depth - 1)

func _carve_rooms() -> void:
	var final_rooms: Array[Rect2i] = []
	for rect in _rooms:
		var padding := Vector2i(1, 1)
		var room_rect := Rect2i(
			rect.position + padding,
			rect.size - padding * 2
		)
		if room_rect.size.x >= 4 and room_rect.size.y >= 4:
			room_rect.size.x = rng.randi_range(4, room_rect.size.x)
			room_rect.size.y = rng.randi_range(4, room_rect.size.y)
			_fill_area(room_rect, TILE_FLOOR)
			final_rooms.append(room_rect)

	_rooms = final_rooms

func _carve_corridors() -> void:
	for i in range(_rooms.size() - 1):
		var a: Vector2i = _rooms[i].get_center()
		var b: Vector2i = _rooms[i + 1].get_center()

		var h_corridor := Rect2i(
			Vector2i(min(a.x, b.x), a.y),
			Vector2i(abs(a.x - b.x) + 1, 1)
		)
		var v_corridor := Rect2i(
			Vector2i(b.x, min(a.y, b.y)),
			Vector2i(1, abs(a.y - b.y) + 1)
		)

		if rng.randi_range(0, 1) == 0:
			_carve_line(h_corridor)
			_carve_line(v_corridor)
		else:
			_carve_line(v_corridor)
			_carve_line(h_corridor)

func _carve_line(area: Rect2i) -> void:
	for x in range(area.position.x, area.end.x):
		for y in range(area.position.y, area.end.y):
			if _tilemap.get_cell_atlas_coords(Vector2i(x, y)) == TILE_WALL:
				_tilemap.set_cell(Vector2i(x, y), 0, TILE_FLOOR)

func get_spawn_positions() -> Array[Vector2i]:
	var positions: Array[Vector2i] = []
	for room in _rooms:
		positions.append(room.get_center())
	return positions

func get_room_centers() -> Array[Vector2i]:
	var centers: Array[Vector2i] = []
	for room in _rooms:
		centers.append(room.get_center())
	return centers
```

**AI Prompt Template — Phase 1:**

```
You are an expert Godot 4 GDScript developer. Generate a room_generator.gd script that uses Binary Space Partitioning (BSP) to procedurally generate dungeon rooms and corridors on a TileMapLayer node. Requirements:
- Use class_name RoomGenerator
- Accept a seed for deterministic generation
- Split a rectangle recursively with BSP
- Carve rooms with padding from walls
- Connect rooms with L-shaped corridors
- Return arrays of room centers for spawning
- Use TileMapLayer.set_cell() for Godot 4.4 compatibility
- Include a RandomNumberGenerator for all random choices
Write the complete GDScript code with no placeholder functions.
```

---

### Phase 2: Player Movement + Shooting + Dodge Roll

**File:** `scripts/player.gd`

```gdscript
extends CharacterBody2D

class_name Player

@export var speed: float = 250.0
@export var dodge_speed: float = 500.0
@export var dodge_duration: float = 0.35
@export var dodge_cooldown: float = 1.0
@export var max_health: int = 6
@export var bullet_scene: PackedScene

var health: int = max_health
var current_direction: Vector2 = Vector2.DOWN
var is_dodging: bool = false
var can_dodge: bool = true
var invincible: bool = false
var invincibility_time: float = 0.5

var _stats: Dictionary = {
	"damage": 1.0,
	"fire_rate": 0.3,
	"bullet_speed": 500.0,
	"range": 600.0,
	"move_speed_mult": 1.0
}

@onready var sprite: Sprite2D = $Sprite2D
@onready var dodge_timer: Timer = $DodgeTimer
@onready var dodge_cooldown_timer: Timer = $DodgeCooldownTimer
@onready var shoot_timer: Timer = $ShootTimer
@onready var invincibility_timer: Timer = $InvincibilityTimer
@onready var gun_point: Marker2D = $GunPoint
@onready var animation_player: AnimationPlayer = $AnimationPlayer

func _ready() -> void:
	dodge_timer.one_shot = true
	dodge_cooldown_timer.one_shot = true
	shoot_timer.one_shot = true
	health = max_health

func _physics_process(_delta: float) -> void:
	if is_dodging:
		return

	var input_dir := Vector2(
		Input.get_axis("move_left", "move_right"),
		Input.get_axis("move_up", "move_down")
	).normalized()

	if input_dir.length() > 0:
		current_direction = input_dir

	velocity = input_dir * speed * _stats.move_speed_mult
	move_and_slide()

func _input(event: InputEvent) -> void:
	if event.is_action_pressed("dodge") and can_dodge and not is_dodging:
		_start_dodge()

	if event.is_action_pressed("shoot"):
		_try_shoot()

	if event.is_action_pressed("use_item"):
		_use_active_item()

func _process(_delta: float) -> void:
	if not is_dodging:
		var mouse_pos: Vector2 = get_global_mouse_position()
		var look_dir: Vector2 = (mouse_pos - global_position).normalized()
		sprite.rotation = look_dir.angle()
		gun_point.rotation = look_dir.angle()

func _start_dodge() -> void:
	is_dodging = true
	can_dodge = false
	invincible = true

	var dodge_dir: Vector2 = current_direction if current_direction.length() > 0 else Vector2.RIGHT
	velocity = dodge_dir * dodge_speed
	move_and_slide()

	dodge_timer.start(dodge_duration)
	dodge_cooldown_timer.start(dodge_cooldown)
	invincibility_timer.start(invincibility_time)

	if animation_player.has_animation("dodge"):
		animation_player.play("dodge")

func _on_dodge_timer_timeout() -> void:
	is_dodging = false
	velocity = Vector2.ZERO

func _on_dodge_cooldown_timeout() -> void:
	can_dodge = true

func _on_invincibility_timeout() -> void:
	invincible = false

func _try_shoot() -> void:
	if shoot_timer.is_stopped():
		if bullet_scene:
			var bullet: Bullet = bullet_scene.instantiate()
			var mouse_pos: Vector2 = get_global_mouse_position()
			var dir: Vector2 = (mouse_pos - gun_point.global_position).normalized()
			bullet.setup(
				gun_point.global_position,
				dir,
				_stats.damage,
				_stats.bullet_speed,
				_stats.range
			)
			get_tree().current_scene.add_child(bullet)
			shoot_timer.start(_stats.fire_rate)

func _use_active_item() -> void:
	print("Active item used")

func take_damage(amount: int, knockback_dir: Vector2 = Vector2.ZERO) -> void:
	if invincible:
		return

	health -= amount
	invincible = true
	invincibility_timer.start(invincibility_time)

	if knockback_dir.length() > 0:
		velocity = knockback_dir * 300.0

	modulate = Color(1, 0.3, 0.3, 0.7)
	await get_tree().create_timer(0.1).timeout
	modulate = Color.WHITE

	if health <= 0:
		_die()

func _die() -> void:
	queue_free()
	GameManager.on_player_died()

func heal(amount: int) -> void:
	health = min(health + amount, max_health)

func upgrade_stat(stat: String, value: float) -> void:
	if _stats.has(stat):
		_stats[stat] += value
```

**AI Prompt Template — Phase 2:**

```
Generate a player.gd script for a Godot 4 top-down roguelike with real-time combat. The player is a CharacterBody2D with:
- WASD movement with speed variable
- Dodge roll on Space with i-frames, duration, and cooldown timers
- Mouse aim (sprite rotates toward mouse), left-click shoot from a GunPoint Marker2D
- Bullet scene instantiation with damage, speed, range from exported bullet scene
- Stats dictionary (damage, fire_rate, bullet_speed, range, move_speed_mult) with upgrade method
- Health system with invincibility frames, take_damage(), heal()
- Knockback on hit
- Dodge timer, shoot timer, invincibility timer as @onready vars
Use class_name Player and proper Node references.
```

---

### Phase 3: Enemy AI (Chase, Shoot, Patrol, Spawn)

**File:** `scripts/enemy.gd`

```gdscript
extends CharacterBody2D

class_name Enemy

enum State { IDLE, PATROL, CHASE, ATTACK, HURT, DEATH }

@export var max_health: int = 3
@export var speed: float = 80.0
@export var chase_range: float = 200.0
@export var attack_range: float = 40.0
@export var damage: int = 1
@export var score_value: int = 10
@export var bullet_scene: PackedScene
@export var spawn_scene: PackedScene
@export var drops: Array[PackedScene]

var health: int = max_health
var state: State = State.IDLE
var player_ref: Player = null
var patrol_points: Array[Vector2] = []
var current_patrol_index: int = 0
var nav_target: Vector2 = Vector2.ZERO

var _attack_cooldown: float = 1.5
var _can_attack: bool = true
var _aggro_time: float = 0.0

@onready var sprite: Sprite2D = $Sprite2D
@onready var state_timer: Timer = $StateTimer
@onready var attack_timer: Timer = $AttackTimer
@onready var navigation_agent: NavigationAgent2D = $NavigationAgent2D
@onready var hitbox: Area2D = $Hitbox
@onready var spawn_point: Marker2D = $SpawnPoint

func _ready() -> void:
	health = max_health
	player_ref = get_tree().get_first_node_in_group("player")
	_set_state(State.IDLE)

func _physics_process(delta: float) -> void:
	match state:
		State.IDLE:
			_idle(delta)
		State.PATROL:
			_patrol(delta)
		State.CHASE:
			_chase(delta)
		State.ATTACK:
			_attack(delta)
		State.HURT:
			_hurt(delta)
		State.DEATH:
			_death(delta)

func _set_state(new_state: State) -> void:
	state = new_state
	match state:
		State.IDLE:
			state_timer.start(2.0)
		State.PATROL:
			if patrol_points.size() > 0:
				current_patrol_index = 0
				nav_target = patrol_points[0]
		State.CHASE:
			navigation_agent.target_position = player_ref.global_position if player_ref else global_position

func _idle(_delta: float) -> void:
	if _can_see_player():
		_set_state(State.CHASE)

func _patrol(_delta: float) -> void:
	if patrol_points.size() == 0:
		_set_state(State.IDLE)
		return

	if global_position.distance_to(nav_target) < 10.0:
		current_patrol_index = (current_patrol_index + 1) % patrol_points.size()
		nav_target = patrol_points[current_patrol_index]

	_move_toward(nav_target, speed * 0.5)

	if _can_see_player():
		_set_state(State.CHASE)

func _chase(_delta: float) -> void:
	if not player_ref:
		_set_state(State.IDLE)
		return

	var dist: float = global_position.distance_to(player_ref.global_position)

	if dist > chase_range * 1.5:
		_set_state(State.PATROL)
		return

	if dist <= attack_range:
		_set_state(State.ATTACK)
		return

	navigation_agent.target_position = player_ref.global_position

	if navigation_agent.is_navigation_finished():
		return

	var next_pos: Vector2 = navigation_agent.get_next_path_position()
	if next_pos != Vector2.ZERO:
		_move_toward(next_pos, speed)

func _attack(_delta: float) -> void:
	if not player_ref:
		_set_state(State.IDLE)
		return

	var dist: float = global_position.distance_to(player_ref.global_position)
	if dist > attack_range * 1.2:
		_set_state(State.CHASE)
		return

	_look_at(player_ref.global_position)

	if _can_attack:
		_can_attack = false
		attack_timer.start(_attack_cooldown)
		_execute_attack()

func _execute_attack() -> void:
	if bullet_scene:
		var bullet: Bullet = bullet_scene.instantiate()
		var dir: Vector2 = (player_ref.global_position - spawn_point.global_position).normalized()
		bullet.setup(spawn_point.global_position, dir, damage, 300.0, 400.0, true)
		get_tree().current_scene.add_child(bullet)

func _spawn_minions() -> void:
	if spawn_scene:
		for i in range(2):
			var minion: Enemy = spawn_scene.instantiate()
			var offset := Vector2(randf_range(-30, 30), randf_range(-30, 30))
			minion.global_position = global_position + offset
			get_tree().current_scene.add_child(minion)

func _hurt(delta: float) -> void:
	state_timer.start(0.3)

func _death(_delta: void) -> void:
	_drop_loot()
	queue_free()
	RoomManager.on_enemy_killed(self)

func _drop_loot() -> void:
	if drops.size() > 0 and randi() % 4 == 0:
		var item: Item = drops[randi() % drops.size()].instantiate()
		item.global_position = global_position
		get_tree().current_scene.add_child(item)

func take_damage(amount: int, _knockback_dir: Vector2 = Vector2.ZERO) -> void:
	health -= amount
	sprite.modulate = Color(1, 0.3, 0.3)
	await get_tree().create_timer(0.1).timeout
	sprite.modulate = Color.WHITE

	if health <= 0:
		_set_state(State.DEATH)
	else:
		_set_state(State.HURT)

func _can_see_player() -> bool:
	if not player_ref:
		return false
	var dist: float = global_position.distance_to(player_ref.global_position)
	return dist <= chase_range

func _move_toward(target: Vector2, move_speed: float) -> void:
	var dir: Vector2 = (target - global_position).normalized()
	velocity = dir * move_speed
	_look_at(target)
	move_and_slide()

func _look_at(target: Vector2) -> void:
	sprite.rotation = (target - global_position).angle()

func _on_attack_timer_timeout() -> void:
	_can_attack = true

func _on_state_timer_timeout() -> void:
	if state == State.IDLE:
		_set_state(State.PATROL)
	elif state == State.HURT:
		_set_state(State.CHASE)

func _on_hitbox_area_entered(area: Area2D) -> void:
	if area is Bullet and not area.is_enemy_bullet:
		take_damage(area.damage, area.direction * 50.0)
```

**AI Prompt Template — Phase 3:**

```
Generate an enemy.gd for a Godot 4 top-down roguelike. CharacterBody2D with finite state machine: IDLE, PATROL, CHASE, ATTACK, HURT, DEATH. Requirements:
- Patrol between assigned Vector2 points
- Chase player using NavigationAgent2D within chase_range
- Attack with bullet spawning from Marker2D when within attack_range
- Optional spawn_minions() for summoner enemy type
- take_damage() with flash effect, knockback param
- Drop loot from array of PackedScene items on death
- Uses class_name Enemy
- attack_timer and state_timer for cooldowns
- Look at target via sprite.rotation
Write complete GDScript with no placeholders.
```

---

### Phase 4: Item/Pickup System + Room Clearing + Doors

**File:** `scripts/item.gd`

```gdscript
extends Area2D

class_name Item

enum ItemType { HEALTH, KEY, COIN, DAMAGE_UP, SPEED_UP, FIRE_RATE_UP, ACTIVE_ITEM, WEAPON }

@export var item_type: ItemType = ItemType.HEALTH
@export var item_name: String = "Item"
@export var item_description: String = ""
@export var value: float = 1.0
@export var texture: Texture2D
@export var is_active_item: bool = false
@export var active_cooldown: float = 5.0

var used: bool = false

@onready var sprite: Sprite2D = $Sprite2D
@onready var pickup_sound: AudioStreamPlayer2D = $PickupSound
@onready var bob_tween: Tween

func _ready() -> void:
	body_entered.connect(_on_body_entered)
	if texture:
		sprite.texture = texture
	_start_bob_animation()

func _start_bob_animation() -> void:
	bob_tween = create_tween().set_loops()
	bob_tween.tween_property(sprite, "position:y", -4.0, 0.5).set_ease(Tween.EASE_IN_OUT)
	bob_tween.tween_property(sprite, "position:y", 0.0, 0.5).set_ease(Tween.EASE_IN_OUT)

func _on_body_entered(body: Node2D) -> void:
	if used:
		return
	if body is Player:
		used = true
		_apply_effect(body as Player)
		if pickup_sound:
			pickup_sound.play()
		sprite.visible = false
		set_deferred("monitoring", false)
		set_deferred("monitorable", false)
		await pickup_sound.finished if pickup_sound else get_tree().create_timer(0.1).timeout
		queue_free()

func _apply_effect(player: Player) -> void:
	match item_type:
		ItemType.HEALTH:
			player.heal(int(value))
		ItemType.COIN:
			GameManager.add_coins(int(value))
		ItemType.KEY:
			GameManager.add_keys(int(value))
		ItemType.DAMAGE_UP:
			player.upgrade_stat("damage", value)
		ItemType.SPEED_UP:
			player.upgrade_stat("move_speed_mult", value * 0.1)
		ItemType.FIRE_RATE_UP:
			player.upgrade_stat("fire_rate", -value * 0.05)
		ItemType.ACTIVE_ITEM:
			GameManager.set_active_item(self)
		ItemType.WEAPON:
			player._stats.damage = value

func get_item_data() -> Dictionary:
	return {
		"name": item_name,
		"description": item_description,
		"type": item_type,
		"value": value,
		"is_active": is_active_item,
		"cooldown": active_cooldown
	}
```

**File:** `scripts/room_manager.gd`

```gdscript
extends Node

class_name RoomManager

signal room_cleared(room_index: int)
signal all_rooms_cleared()

enum RoomType { COMBAT, TREASURE, BOSS, SHOP, START }

var current_room_index: int = -1
var rooms: Array[RoomData] = []
var enemies_in_room: int = 0
var room_cleared_states: Array[bool] = []

func _ready() -> void:
	_enemy_died.connect(_on_enemy_killed)

func register_rooms(room_data: Array[RoomData]) -> void:
	rooms = room_data
	room_cleared_states.resize(rooms.size())
	room_cleared_states.fill(false)

func enter_room(index: int) -> void:
	if index < 0 or index >= rooms.size():
		return

	current_room_index = index

	if rooms[index].room_type == RoomType.COMBAT and not room_cleared_states[index]:
		_lock_doors(index)
		_spawn_room_enemies(index)
	elif rooms[index].room_type == RoomType.BOSS:
		_lock_doors(index)
		_spawn_boss(index)

func _lock_doors(index: int) -> void:
	var room = rooms[index]
	for door_pos in room.door_positions:
		_tilemap.set_cell(door_pos, 0, TILE_WALL)

func _spawn_room_enemies(index: int) -> void:
	var room = rooms[index]
	enemies_in_room = 0
	for spawn_data in room.enemy_spawns:
		var enemy: Enemy = spawn_data.scene.instantiate()
		enemy.global_position = spawn_data.position
		enemy.died.connect(_on_enemy_killed)
		get_tree().current_scene.add_child(enemy)
		enemies_in_room += 1

func _spawn_boss(index: int) -> void:
	var boss: Enemy = rooms[index].boss_scene.instantiate()
	boss.global_position = rooms[index].boss_spawn_position
	boss.died.connect(_on_enemy_killed)
	get_tree().current_scene.add_child(boss)
	enemies_in_room = 1

func _on_enemy_killed(_enemy: Enemy) -> void:
	if current_room_index < 0:
		return
	enemies_in_room -= 1
	if enemies_in_room <= 0:
		_on_room_cleared()

func _on_room_cleared() -> void:
	if current_room_index >= 0:
		room_cleared_states[current_room_index] = true
		_unlock_doors(current_room_index)
		_spawn_rewards(current_room_index)
		room_cleared.emit(current_room_index)

func _unlock_doors(index: int) -> void:
	var room = rooms[index]
	for door_pos in room.door_positions:
		_tilemap.set_cell(door_pos, 0, TILE_DOOR)

func _spawn_rewards(index: int) -> void:
	var room = rooms[index]
	if room.reward_scene:
		var reward: Item = room.reward_scene.instantiate()
		reward.global_position = room.reward_position
		get_tree().current_scene.add_child(reward)

func is_current_room_cleared() -> bool:
	if current_room_index < 0:
		return true
	return room_cleared_states[current_room_index]
```

**AI Prompt Template — Phase 4:**

```
Generate an item.gd script for a Godot 4 roguelike. Area2D pickup with:
- Enum ItemType: HEALTH, KEY, COIN, DAMAGE_UP, SPEED_UP, FIRE_RATE_UP, ACTIVE_ITEM, WEAPON
- Floating bob animation using Tween
- On body_entered with Player: apply effect (heal, stat upgrade, coin/key add)
- One-time pickup, destroy after use
- signal emission on pickup
- Item data dictionary for UI
Also generate a room_manager.gd that tracks rooms, locks/unlocks doors via TileMapLayer cell changes, spawns enemies on room entry, detects room clear via all enemies dead signal, and spawns rewards. Use class_name for both.
```

---

### Phase 5: Permadeath, Runs, Meta-Progression, Boss Rooms

**File:** `scripts/game_manager.gd`

```gdscript
extends Node

class_name GameManager

signal game_started()
signal game_over(win: bool)
signal floor_changed(floor: int)
signal coins_changed(amount: int)
signal keys_changed(amount: int)

const SAVE_PATH: String = "user://savegame.dat"
const MAX_FLOORS: int = 12

var current_floor: int = 1
var run_seed: int = 0
var coins: int = 0
var keys: int = 0
var kills: int = 0
var time_elapsed: float = 0.0
var active_item: Item = null
var active_item_cooldown: float = 0.0

# Meta-progression (persists across runs)
var meta_unlocks: Dictionary = {
	"characters_unlocked": ["knight"],
	"starting_items": [],
	"max_health_bonus": 0,
	"damage_bonus": 0.0,
	"speed_bonus": 0.0,
	"total_runs": 0,
	"total_wins": 0,
	"unlocked_floors": 1
}

func _ready() -> void:
	_load_meta_progression()

func start_new_run() -> void:
	run_seed = randi()
	current_floor = 1
	coins = 0
	keys = 0
	kills = 0
	time_elapsed = 0.0
	active_item = null
	game_started.emit()
	_generate_floor()

func _generate_floor() -> void:
	var floor_type: String = _get_floor_type(current_floor)
	var is_boss_floor: bool = current_floor % 3 == 0

	var generator: RoomGenerator = RoomGenerator.new()
	generator.generate(tilemap, Vector2i(50, 50), run_seed + current_floor)

	var room_data: Array[RoomData] = _assign_room_types(generator.get_room_centers(), is_boss_floor)
	RoomManager.register_rooms(room_data)

	_spawn_player(generator.get_spawn_positions()[0])
	RoomManager.enter_room(0)

	floor_changed.emit(current_floor)

func _get_floor_type(floor: int) -> String:
	match floor:
		1, 2: return "dungeon"
		3: return "boss_dungeon"
		4, 5: return "catacombs"
		6: return "boss_catacombs"
		7, 8: return "library"
		9: return "boss_library"
		10, 11: return "hell"
		12: return "final_boss"
	return "dungeon"

func _assign_room_types(centers: Array[Vector2i], has_boss: bool) -> Array[RoomData]:
	if centers.size() < 3:
		return []

	var data: Array[RoomData] = []

	var start_room := RoomData.new()
	start_room.room_type = RoomManager.RoomType.START
	start_room.center = centers[0]
	data.append(start_room)

	var rng := RandomNumberGenerator.new()
	rng.seed = run_seed + current_floor

	var end_index: int = centers.size() - 1
	if has_boss:
		var boss_data := RoomData.new()
		boss_data.room_type = RoomManager.RoomType.BOSS
		boss_data.center = centers[end_index]
		boss_data.boss_scene = _get_boss_for_floor(current_floor)
		data.append(boss_data)
		end_index -= 1

	for i in range(1, end_index + 1):
		var rd := RoomData.new()
		var roll: int = rng.randi_range(0, 100)
		if roll < 15:
			rd.room_type = RoomManager.RoomType.TREASURE
		elif roll < 20:
			rd.room_type = RoomManager.RoomType.SHOP
		else:
			rd.room_type = RoomManager.RoomType.COMBAT
		rd.center = centers[i]
		rd.enemy_spawns = _generate_enemy_layout(centers[i], rng)
		data.append(rd)

	return data

func _generate_enemy_layout(center: Vector2i, rng: RandomNumberGenerator) -> Array:
	var spawns: Array = []
	var enemy_count: int = rng.randi_range(2, 5 + current_floor)
	var enemy_types: Array[PackedScene] = _get_floor_enemies(current_floor)

	for i in range(enemy_count):
		var offset := Vector2(
			rng.randf_range(-80, 80) + center.x * 16,
			rng.randf_range(-80, 80) + center.y * 16
		)
		spawns.append({
			"position": offset,
			"scene": enemy_types[rng.randi_range(0, enemy_types.size() - 1)]
		})
	return spawns

func _get_boss_for_floor(floor: int) -> PackedScene:
	match floor:
		3: return preload("res://enemies/boss_dungeon.tscn")
		6: return preload("res://enemies/boss_catacombs.tscn")
		9: return preload("res://enemies/boss_library.tscn")
		12: return preload("res://enemies/boss_final.tscn")
	return preload("res://enemies/boss_dungeon.tscn")

func _get_floor_enemies(floor: int) -> Array[PackedScene]:
	match floor:
		1, 2: return [preload("res://enemies/rat.tscn"), preload("res://enemies/slime.tscn")]
		4, 5: return [preload("res://enemies/skeleton.tscn"), preload("res://enemies/wraith.tscn")]
		7, 8: return [preload("res://enemies/mage.tscn"), preload("res://enemies/book.tscn")]
		10, 11: return [preload("res://enemies/demon.tscn"), preload("res://enemies/fire_imp.tscn")]
	return [preload("res://enemies/slime.tscn")]

func _spawn_player(spawn_pos: Vector2i) -> void:
	var player_scene: PackedScene = preload("res://player/player.tscn")
	var player: Player = player_scene.instantiate()
	player.global_position = Vector2(spawn_pos.x * 16, spawn_pos.y * 16)
	player.max_health += meta_unlocks.max_health_bonus
	player.health = player.max_health
	player._stats.damage += meta_unlocks.damage_bonus
	player._stats.move_speed_mult += meta_unlocks.speed_bonus
	get_tree().current_scene.add_child(player)

func on_player_died() -> void:
	meta_unlocks.total_runs += 1
	_save_meta_progression()
	game_over.emit(false)

func on_boss_defeated() -> void:
	if current_floor >= MAX_FLOORS:
		meta_unlocks.total_runs += 1
		meta_unlocks.total_wins += 1
		game_over.emit(true)
	else:
		current_floor += 1
		if current_floor > meta_unlocks.unlocked_floors:
			meta_unlocks.unlocked_floors = current_floor
		_generate_floor()

func add_coins(amount: int) -> void:
	coins += amount
	coins_changed.emit(coins)

func add_keys(amount: int) -> void:
	keys += amount
	keys_changed.emit(keys)

func set_active_item(item: Item) -> void:
	active_item = item

func _save_meta_progression() -> void:
	var file := FileAccess.open(SAVE_PATH, FileAccess.WRITE)
	if file:
		file.store_var(meta_unlocks)
		file.close()

func _load_meta_progression() -> void:
	if FileAccess.file_exists(SAVE_PATH):
		var file := FileAccess.open(SAVE_PATH, FileAccess.READ)
		if file:
			var data = file.get_var()
			if data is Dictionary:
				for key in data:
					if meta_unlocks.has(key):
						meta_unlocks[key] = data[key]
			file.close()
```

**File:** `scripts/hud.gd`

```gdscript
extends CanvasLayer

class_name HUD

@export var health_icon_scene: PackedScene
@export var max_health_display: int = 12

@onready var health_container: HBoxContainer = $HealthContainer
@onready var coin_label: Label = $CoinLabel
@onready var key_label: Label = $KeyLabel
@onready var floor_label: Label = $FloorLabel
@onready var minimap: Minimap = $Minimap
@onready var active_item_icon: TextureRect = $ActiveItemIcon
@onready var active_item_cooldown: TextureProgressBar = $ActiveItemCooldown
@onready var damage_indicator: ColorRect = $DamageIndicator
@onready var boss_health_bar: TextureProgressBar = $BossHealthBar

var _health_icons: Array[TextureRect] = []

func _ready() -> void:
	GameManager.coins_changed.connect(_on_coins_changed)
	GameManager.keys_changed.connect(_on_keys_changed)
	GameManager.floor_changed.connect(_on_floor_changed)
	GameManager.game_over.connect(_on_game_over)

	for player in get_tree().get_nodes_in_group("player"):
		_setup_health(player)

func _setup_health(player: Player) -> void:
	for child in health_container.get_children():
		child.queue_free()
	_health_icons.clear()
	for i in range(player.max_health):
		var icon: TextureRect = health_icon_scene.instantiate()
		health_container.add_child(icon)
		_health_icons.append(icon)
	_update_health(player.health)

func _process(_delta: float) -> void:
	var player := get_tree().get_first_node_in_group("player") as Player
	if player:
		_update_health(player.health)

func _update_health(current: int) -> void:
	for i in _health_icons.size():
		_health_icons[i].modulate = Color.WHITE if i < current else Color(0.3, 0.3, 0.3, 0.5)

func _on_coins_changed(amount: int) -> void:
	coin_label.text = str(amount)

func _on_keys_changed(amount: int) -> void:
	key_label.text = str(amount)

func _on_floor_changed(floor: int) -> void:
	floor_label.text = "Floor %d" % floor

func _on_game_over(_win: bool) -> void:
	show_death_screen()

func show_boss_health_bar(max_hp: int) -> void:
	boss_health_bar.max_value = max_hp
	boss_health_bar.value = max_hp
	boss_health_bar.visible = true

func update_boss_health(current: int) -> void:
	boss_health_bar.value = current

func hide_boss_health_bar() -> void:
	boss_health_bar.visible = false

func show_death_screen() -> void:
	$DeathScreen.visible = true
	$DeathScreen/StatsLabel.text = "Kills: %d\nFloor: %d\nTime: %s" % [
		GameManager.kills,
		GameManager.current_floor,
		_format_time(GameManager.time_elapsed)
	]

func _format_time(seconds: float) -> String:
	var m: int = int(seconds) / 60
	var s: int = int(seconds) % 60
	return "%02d:%02d" % [m, s]
```

**AI Prompt Template — Phase 5:**

```
Generate a game_manager.gd autoload singleton for a Godot 4 roguelike. Requirements:
- Manages runs (seed, floor progression, coins, keys, time)
- Meta-progression saved to user://savegame.dat via FileAccess.store_var/get_var
- Array of characters_unlocked, starting_items, stat bonuses
- Floor generation: 12 floors, boss every 3rd floor, 4 themes (dungeon, catacombs, library, hell)
- Coordinates RoomGenerator + RoomManager for level creation
- Tracks run stats, saves on death
- Signals: game_started, game_over, floor_changed, coins_changed, keys_changed
- on_player_died(), on_boss_defeated(), add_coins(), add_keys()
Write full GDScript with class_name GameManager.

Also generate hud.gd CanvasLayer that connects to GameManager signals and displays health icons, coins, keys, floor number, boss health bar, and death screen with stats.
```

---

## 5. AI Prompts for Every Script

### room_generator.gd
```
"Generate a BSP dungeon generator for Godot 4.4 using TileMapLayer. Create class_name RoomGenerator. Use recursive splitting, room carving with padding, L-shaped corridor connections. Accept seed param. Return room center array for spawning. Use RandomNumberGenerator."
```

### player.gd
```
"Generate Player class (CharacterBody2D) for top-down roguelike with: WASD movement, mouse aim/rotation, dodge roll (Space) with i-frames, left-click shooting with bullet scene instantiation, stats dictionary (damage, fire_rate, bullet_speed, range, speed_mult), health with invincibility frames, upgrade_stat() method. Godot 4.4 GDScript."
```

### enemy.gd
```
"Generate Enemy class (CharacterBody2D) with finite state machine: IDLE/PATROL/CHASE/ATTACK/HURT/DEATH. NavigationAgent2D for pathfinding. Bullet attack for ranged enemies. Spawn minions for summoners. Drop loot on death. Take damage with knockback. Connect to RoomManager signals. Godot 4 GDScript with class_name."
```

### item.gd
```
"Generate Item class (Area2D) for roguelike pickups: enum ItemType (HEALTH, KEY, COIN, DAMAGE_UP, SPEED_UP, FIRE_RATE_UP, ACTIVE_ITEM, WEAPON), bob animation via Tween, body_entered detection for Player, effect application, Coin/Key tracking via GameManager singleton. Godot 4 GDScript."
```

### room_manager.gd
```
"Generate RoomManager for Godot 4 roguelike. Tracks rooms (COMBAT/TREASURE/BOSS/SHOP/START). Locks/unlocks doors via TileMapLayer. Spawns enemies on room entry. Detects all-clear via enemy died signal. Spawns rewards. Signals: room_cleared, all_rooms_cleared. Godot 4 GDScript."
```

### game_manager.gd
```
"Generate GameManager autoload singleton for roguelike: run management (seed, floor, coins, keys, time), meta-progression saving/loading with FileAccess, floor generation (12 floors, 4 themes, boss every 3rd floor), coordinates RoomGenerator + RoomManager, signals game_started/game_over/floor_changed/coins_changed/keys_changed. Godot 4 GDScript."
```

### hud.gd
```
"Generate HUD (CanvasLayer) for roguelike: health bar with heart icons, coin/key count labels, floor number, minimap reference, active item icon + cooldown, boss health bar (show/hide/update), death screen with stats (kills, floor, time). Connect to GameManager signals. Godot 4 GDScript."
```

### bullet.gd
```
"Generate Bullet class (Area2D) for roguelike projectiles. Properties: speed, damage, range, direction, is_enemy_bullet flag. Move in _process, queue_free on max distance or body/area collision. Setup method for initialization. Godot 4 GDScript."
```

### boss_template.gd
```
"Generate boss.gd extending Enemy with multi-phase behavior. Phase 1: charge + melee. Phase 2: bullet spread pattern (3-way shot). Phase 3: spawn minions + enrage. Health gates transition between phases. Show boss health bar via HUD. Drop special item on death. Godot 4 GDScript."
```

### minimap.gd
```
"Generate Minimap (Control node) for roguelike: draws explored rooms on small grid, shows player position as dot, darkens unexplored rooms, updates on room change, toggle with M key. Use _draw() for rendering. Godot 4 GDScript."
```

---

## 6. Asset Pipeline: Free Sprites + AI Art

### Pipeline Workflow

```
1. COLLECT PHASE
   └─ Download Kenney Roguelike/RPG Pack (base tileset)
   └─ Download 16x16 DungeonTileset II (alternative theme)
   └─ Download Pixel Crawler Free Pack (characters + enemies)
   └─ Extract to res://assets/sprites/

2. TILESET SETUP (Godot Editor)
   └─ Create TileSet resource
   └─ Import sprite sheets, slice to 16x16 grid
   └─ Define terrains (wall, floor, door, pit)
   └─ Set collision layers per tile
   └─ Add navigation polygons for pathfinding

3. CHARACTER SPRITES
   └─ Use Kenney characters or Pixel Crawler heroes
   └─ Slice sprite sheets into individual animations
   └─ Create AnimatedSprite2D per animation (idle, walk, attack, dodge, hurt, death)
   └─ Set animation speed to match gameplay (4-8 frames each)

4. AI-GENERATED ASSETS (Optional Enhancement)
   └─ Use Sorceress Quick Sprites for unique hero/monster sprites
   └─ Use Leonardo AI to generate custom item icons
   └─ Post-process in Aseprite/Krita to fit 16x16 grid
   └─ Quantize palette to match Kenney style (reduce colors)

5. SOUND EFFECTS
   └─ BFXR: shoot, hit, pickup, dodge, door, coin, death sounds
   └─ ChipTone: ambient loop, boss warning, floor transition
   └─ Export as .ogg (compressed) for Godot

6. UI ASSETS
   └─ Kenney Board Game Icons for item sprites
   └─ Kenney Input Prompts for control hints
   └─ Custom health hearts from Kenney 1-Bit Pack
   └─ Font: Kenney Pixel Font (res://assets/fonts/)

7. THEME VARIATIONS
   └─ Create 4 TileSet variants (stone, bone, blue, red)
   └─ Recolor sprites using modulate for floor themes
   └─ Swap enemy sprites per theme via @export
```

### Directory Structure

```
res://
├── assets/
│   ├── sprites/
│   │   ├── tilesets/        (kenney_roguelike_rpg, dungeon_tileset_ii, pixel_crawler)
│   │   ├── characters/      (hero_sheet.png, npc_sheet.png)
│   │   ├── enemies/         (slime, skeleton, mage, demon, bosses)
│   │   ├── items/           (hearts, keys, coins, weapons, actives)
│   │   ├── effects/         (bullet, explosion, hit_spark, dodge_trail)
│   │   └── ui/              (hearts, icons, buttons, panels, font)
│   ├── audio/
│   │   ├── sfx/             (shoot, hit, pickup, dodge, door, death)
│   │   └── music/           (dungeon_loop, boss_theme, menu_theme)
│   └── fonts/               (kenney_pixel_font.ttf)
├── scenes/
│   ├── player/
│   │   ├── player.tscn
│   │   └── bullet.tscn
│   ├── enemies/
│   │   ├── slime.tscn, skeleton.tscn, mage.tscn, demon.tscn
│   │   └── bosses/
│   ├── rooms/
│   │   ├── room_template.tscn
│   │   └── door.tscn
│   ├── items/
│   │   ├── health.tscn, coin.tscn, key.tscn
│   │   └── stat_upgrade.tscn, active_item.tscn
│   └── ui/
│       ├── hud.tscn
│       ├── main_menu.tscn
│       ├── pause_menu.tscn
│       └── death_screen.tscn
├── scripts/
│   ├── room_generator.gd
│   ├── player.gd
│   ├── enemy.gd
│   ├── item.gd
│   ├── bullet.gd
│   ├── room_manager.gd
│   ├── game_manager.gd
│   ├── hud.gd
│   └── minimap.gd
└── project.godot
```

---

## 7. Free Tier Limitations Table

| Tool | Free Limit | Pain Point | Workaround |
|------|-----------|------------|------------|
| **Godot 4** | Unlimited | Web export requires Emscripten setup | Use official export templates from godotengine.org |
| **Claude Web** | ~20-30 msgs/day, resets midnight UTC | Long coding sessions cut off | Break work into daily sessions. Use prompt templates above to minimize iterations. Write complete scripts in one prompt. |
| **Cursor Hobby** | 2K completions + 50 premium req/month | Premium requests exhaust fast | Use premium only for complex multi-file logic. Use completions for trivial GDScript. Re-register if needed (see warnings). |
| **Bolt.new Free** | 1M tokens/month, 300K daily cap | Large file context burns tokens | Export each script as standalone file. Don't upload entire project. Use precise prompts. |
| **GitHub Copilot Free** | 50 req/month, 2K completions | Minimal for full game dev | Only use for autocomplete. Write architecture yourself. |
| **Gemini API Free** | 60 RPM (Flash), 50/day (Pro) | Pro model severely limited | Use Flash 2.0 for most work. Reserve Pro for complex generation. |
| **Sorceress Credits** | 100 free on signup, 9 credits/gen | ~11 generations free | Use strategically for unique hero/boss art. Use Kenney packs for base assets. |
| **Playground AI** | 500 images/month | Resolution limits | Generate 512x512, downscale to 16x16. Use img2img for sprite consistency. |
| **OpenAI API Credits** | $5 one-time, expires 3 months | Timer expiration | Create account when ready to build. Use credits in one focused burst. |
| **BFXR / ChipTone** | Unlimited | Limited sound variety | Layer multiple BFXR sounds. Use pitch modulation for variation. |
| **Itch.io Hosting** | Unlimited bandwidth (free) | 1 GB file storage for free accounts | Export Godot HTML5 build (~30-60MB WASM). Compress with gzip. |
| **GitHub Pages** | 1 GB repo, 100 GB bandwidth | No server-side logic | Perfect for HTML5 Godot exports. Use .nojekyll file. |

### Token/Request Budget Strategy (Free AI)

```
Budget type         ───  Total free/month  ───  Per-day
Claude msgs         ───  ~780 (26*30)       ───  ~26/day
Cursor completions  ───  2,000              ───  ~66/day
Cursor premium      ───  50                 ───  Use sparingly
Bolt tokens         ───  1,000,000          ───  ~33K/day

Estimated GDScript lines per budget:
Claude: 6 scripts/month (80-120 lines each) = 500+ lines
Cursor: Complete GDScript files via completions = 800+ lines
Bolt: Full project scaffolding = 2000+ lines (if optimized)

Strategy: Use Claude for complex architecture → paste into Godot.
Use Cursor for iteration/fixes within Godot editor.
Use Bolt for rapid scaffolding/prototyping.
```

---

## 8. Publishing on Itch.io + GitHub Pages

### Itch.io (Primary)

```
1. Build → Export → HTML5
   - Enable "Export with Debug" unchecked
   - Enable "Variant" for different themes
   - Set compression: GZip

2. Create itch.io page
   - Set genre: "Roguelike, Action, Dungeon Crawler"
   - Price: Free or "Name Your Own Price"
   - Tags: roguelike, godot, dungeon-crawler, pixel-art
   - Upload: .zip containing index.html + .pck + .wasm

3. Embed options:
   - Full screen button: true
   - Mobile-friendly: true (if supporting gamepad)
   - Dimensions: 960x540 (scales up)
```

### GitHub Pages (Secondary/Dev Build)

```
1. Create repo: yourname/roguelike-dungeon-crawler
2. Export HTML5 build to docs/ folder
3. Add .nojekyll file (prevents Jekyll processing)
4. Settings → Pages → Deploy from docs/
5. URL: https://yourname.github.io/roguelike-dungeon-crawler/

Advantages: Automatic on push, no storage cap for 1GB,
  ideal for sharing WIP builds with testers.
```

### Itch.io Page Description Template

```
# DUNGEON DESCENT

A top-down roguelike dungeon crawler in the style of 
Binding of Isaac meets Enter the Gungeon.

## Features
✅ Procedural rooms (BSP generation)  
✅ 4 floor themes (Dungeon, Catacombs, Library, Hell)  
✅ 12 enemy types + 4 multi-phase bosses  
✅ 30+ items (passives, actives, weapons)  
✅ Permadeath with meta-progression unlocks  
✅ Dodge roll with i-frames  
✅ Gamepad support  
✅ 4 unlockable characters  

## Controls
WASD - Move  
Mouse - Aim  
Left Click - Shoot  
Space - Dodge Roll  
Q - Active Item  
M - Minimap  
Esc - Pause  

## Credits
Engine: Godot 4  
Sprites: Kenney (CC0), 0x72 (CC0), Anokolisa  
SFX: BFXR, ChipTone  
Music: MusicGen (Meta)  
Font: Kenney Pixel  
```

---

## 9. Production Checklist

### Core Mechanics
- [ ] Player movement (WASD + joystick)
- [ ] Mouse aiming with sprite rotation
- [ ] Shooting with bullet scene pooling
- [ ] Dodge roll with invincibility frames
- [ ] Dodge cooldown and stamina bar
- [ ] Health system (hearts/containers)
- [ ] Damage with knockback
- [ ] Death animation and game over screen
- [ ] Room clearing (enemies → doors unlock)
- [ ] Item pickup with floating animation
- [ ] Active item system (Q to use, cooldown)
- [ ] Coin/key currency system

### Procedural Generation Fairness
- [ ] Player always spawns near entrance
- [ ] Boss room always at end of path
- [ ] Minimum distance between start and boss
- [ ] Treasure rooms always reachable
- [ ] No softlocks (flood fill check all rooms reachable)
- [ ] Enemy count scales with floor number
- [ ] Health pickups in first 2 rooms always
- [ ] Shop appears after floor 2 minimum
- [ ] Guaranteed weapon/upgrade on floor 1

### Enemy Balancing
- [ ] Damage scales with floor (multiplier)
- [ ] Enemy HP scales (1.2x per floor)
- [ ] Speed caps (enemies don't outspeed dodge)
- [ ] Attack patterns have telegraphs
- [ ] Bullet hell patterns have gaps
- [ ] Minion spawns limited per room
- [ ] Boss phases scale with player damage
- [ ] No enemies that stunlock

### Item Synergies
- [ ] Damage items stack multiplicatively
- [ ] Fire rate has diminishing returns (cap at 10x base)
- [ ] Speed items have hard cap (max 2x base)
- [ ] Defense items reduce damage by percentage
- [ ] Active item cooldown reduction effects
- [ ] On-hit effects (poison, burn, slow)
- [ ] Luck stat affects drop rates
- [ ] Item pool dilution (no repeats until pool exhausted)

### UI & Experience
- [ ] Minimap with room exploration tracking
- [ ] Pause menu with settings (volume, controls)
- [ ] Settings persist to config file
- [ ] Full gamepad support (buttons, aiming stick)
- [ ] Control remapping screen
- [ ] HUD: health, coins, keys, floor
- [ ] Boss health bar
- [ ] Floating damage numbers
- [ ] Screen shake on hit
- [ ] Pickup notification popups
- [ ] Death screen with run stats
- [ ] Main menu with character select
- [ ] Run history (best run stats)

### Performance
- [ ] Bullet pooling (pre-instantiate 50+ bullets)
- [ ] Enemy pooling (reuse enemies per room)
- [ ] TileMapLayer optimization (no re-gen mid-room)
- [ ] Particle cleanup (queue free after duration)
- [ ] Animation reuse (don't create new tweens per frame)
- [ ] Navigation baking (pre-bake nav mesh per floor)
- [ ] LOD for distant enemies (disable AI > 500px)
- [ ] Web export under 50MB total
- [ ] 60 FPS on Steam Deck / mid-range hardware
- [ ] 30+ enemies + bullets maintain 60 FPS

### Polish
- [ ] Room transition animation (fade)
- [ ] Door open/close animation
- [ ] Enemy death particles
- [ ] Ambient lighting (occlusion shader)
- [ ] Floor theme music tracks
- [ ] Boss intro animation
- [ ] Victory fanfare on clear
- [ ] Sound effects for all interactions
- [ ] Hit flash (white tint on damage)
- [ ] Dodge trail effect
- [ ] Muzzle flash on shoot
- [ ] Item glow/pulse on floor

---

## 10. How to Improve

### Secret Rooms
Add a `RoomGenerator` pass that places 1x1 secret rooms adjacent to existing rooms. Use a special wall tile that can be blown up with a bomb item. Contents: high-value items, extra coins, character unlocks.

**Implementation:** After corridor carving, scan for wall tiles adjacent to 3+ floor tiles. Place a SecretRoom type. Use `Input.is_action_just_pressed("bomb")` on a wall tile check.

### Devil Deals
After boss rooms (floors 3, 6, 9), spawn a "devil door" that opens a special room. Player trades max HP for powerful items. Track `max_health` before/after trade.

**Balance:** Offer 3 deals: small (1 heart for damage up), medium (2 hearts for weapon), large (3 hearts for game-breaking item).

### Boss Rush Mode
After beating the game once, unlock Boss Rush from main menu. Spawn all bosses sequentially with reduced loot and no exploration between fights. Timer tracks completion.

**Implementation:** New scene `boss_rush.tscn` — array of `[boss_scene, Vector2 spawn_pos]`. Advance on each boss death. Track time via `Time.get_ticks_msec()`.

### Daily Runs
Same seed for all players on a given day. Leaderboard on Itch.io (via iframe or external service). Use `Date` to derive seed: `hash("%d-%d-%d" % [year, month, day])`.

**Constraints:** No meta-progression in daily runs. Fixed character. Score = coins + kills * 10 + (time_bonus).

### Character Unlocks
Unlock characters by completing challenges:
- Knight: Default
- Mage: Beat floor 3
- Rogue: Collect 100 coins total across runs
- Tank: Take 500 damage total across runs
- Angel: Beat a boss without taking damage
- Demon: Complete a devil deal

Each character has different base stats and starting item.

### Weapon Variety
Create weapon types via Resource:
- **Pistol** (base, balanced)
- **Shotgun** (spread 5, short range)
- **Machine Gun** (fast fire, low damage, spread)
- **Sniper** (slow, high damage, pierce enemies)
- **Rocket Launcher** (slow, AoE, self-damage risk)
- **Beam** (continuous, ramping damage)
- **Boomerang** (returns, pierce, slow)
- **Bouncing Shot** (ricochets off walls)

**File:** `scripts/weapon_data.gd` — use `extends Resource` with `@export var` fields.

### Floor Generation (Multiple Themes)
Already covered in Phase 5 `_get_floor_type()`. Extend to 8+ themes:
- Dungeon (stone, brown)
- Catacombs (bone, blue-gray)
- Library (purple, blue)
- Hell (red, dark)
- Factory (metal, orange)
- Garden (green, pink) — hedge walls
- Ice Cave (white, cyan) — slippery floors
- Void (black, purple) — random gravity

Each theme has its own `TileSet`, enemy list, ambient track, and boss.

### NPCs in Hub Area
Create a "Camp" scene between runs. NPCs provide:
- **Merchant:** Spend coins on starting items
- **Blacksmith:** Upgrade stats for floor 1
- **Lore Keeper:** Unlock character backstory pages
- **Challenge Board:** Pick from 3 bonus challenges (+difficulty, +reward)
- **Well:** Donate coins for blessing (random positive effect next run)

**Implementation:** New `camp.tscn` scene. NPCs are `Area2D` with `interact` prompt. Use `GameManager.meta_unlocks` for persistent camp upgrades.

### Save/Quit Mid-Run
Serialize run state:

```gdscript
func save_run() -> void:
	var data := {
		"seed": run_seed,
		"floor": current_floor,
		"coins": coins,
		"keys": keys,
		"time": time_elapsed,
		"player_health": player_ref.health,
		"player_max_health": player_ref.max_health,
		"player_stats": player_ref._stats.duplicate(),
		"cleared_rooms": RoomManager.room_cleared_states.duplicate(),
		"items": _serialize_items()
	}
	var file := FileAccess.open("user://run_save.dat", FileAccess.WRITE)
	file.store_var(data)
	file.close()

func load_run() -> void:
	var file := FileAccess.open("user://run_save.dat", FileAccess.READ)
	var data = file.get_var()
	file.close()

	run_seed = data.seed
	current_floor = data.floor
	# ... restore state, regenerate floor but restore cleared rooms
	# Delete save after loading (permadeath enforced)
	DirAccess.remove_absolute("user://run_save.dat")
```

The save file is deleted on load to enforce permadeath. Offer "Continue Run" option on main menu if save exists.

---

## Appendix: Quick Start Commands

```bash
# Create Godot project from command line
mkdir DungeonDescent && cd DungeonDescent
# Open Godot editor and create new project

# Godot 4 download
# https://godotengine.org/download/windows/

# Export HTML5 build via CLI (after setting up export presets)
godot --headless --export-release "Web" docs/index.html

# Push to GitHub Pages
git init
git add .
git commit -m "Initial build"
git remote add origin https://github.com/you/dungeon-descent.git
git push -u origin main

# Itch.io upload via butler CLI
butler push docs/ you/dungeon-descent:html5
```

---

*"The only way to make a roguelike is to start one. The procedural generation will never be perfect. The synergies will never be balanced. Ship it, iterate, and let players discover the chaos."*

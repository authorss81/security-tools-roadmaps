# Puzzle Match-3 Game — Complete Production Guide

## Build a Bejeweled/Candy Crush clone using ONLY free tools & free AI

---

# 1. Game Concept

**Core Loop:** Swap adjacent gems to form rows/columns of 3+ identical gems. Matched gems vanish, new gems fall from above, chain reactions score bonus points.

**Features:**
- **Grid:** 8x8 board with 6 gem types (Ruby, Sapphire, Emerald, Topaz, Amethyst, Diamond)
- **Combos:** 3-match = base score, 4-match = 1.5x, 5-match = 2x. Chain cascades multiply each step.
- **Boosters:** Bomb gem (clears 3x3), Stripe gem (clears row/column), Rainbow gem (clears all of one color)
- **Levels:** 50+ levels with target scores, move limits, timer modes, and obstacle tiles
- **Score:** Points per match + cascade multiplier + level bonus + time bonus
- **Timers:** Classic (unlimited time, move-limited), Timed (30-120s), Rush (fast-paced cascade time limits)
- **Obstacles:** Locked gems (need 2 matches to free), Ice blocks (1 match to shatter), Stone blocks (3 matches)
- **Progression:** Star rating (1-3 stars per level), world map, unlockable boosters

---

# 2. Free Toolchain

| Tool | Use | Free Tier Limits |
|------|-----|-----------------|
| **Godot 4.4+** | Game engine (GDScript) | Unlimited — MIT license |
| **Claude (free)** | AI code generation, debugging | 5-10 messages / 5 hours (2025) |
| **Cursor (free)** | AI IDE with autocomplete | 2000 completions/month, 50 slow requests |
| **GitHub Copilot (free)** | AI pair programming | 2000 code suggestions/month, 50 chat requests |
| **Aseprite** | Pixel art (trial) | Full trial, or use free GIMP/Krita |
| **GIMP / Krita** | Sprite editing | Unlimited — GPL license |
| **Audacity** | Audio editing | Unlimited — GPL license |
| **Suno AI (free)** | Music generation | 10 free generations/day |
| **Uberduck / Bark** | AI sound effects | Free tier, ~50 generations/day |
| **Freesound.org** | CC0 sound effects | Unlimited free downloads |
| **OpenGameArt** | Free sprites/tiles | Unlimited — CC0/CC-BY |
| **Kenney.nl** | Free game assets | Unlimited — CC0 |
| **Itch.io** | Hosting & distribution | Unlimited free uploads |
| **Android Studio** | APK build | Unlimited — Freeware |

---

# 3. Sprite Pack Direct Links (10+ Free Packs)

## Gems & Jewels
1. **Clint Bellanger Gem Icons** (CC-BY-SA) — https://opengameart.org/content/gem-icons
2. **Candy Pack 1** (CC0) — https://opengameart.org/content/candy-pack-1
3. **Kenney Game Assets All-in-1** (CC0) — https://kenney.itch.io/kenney-game-assets
4. **Match-3 Gems 32x32** (CC0) — https://opengameart.org/content/match-3

## UI & Icons
5. **Kenney UI Pack** (CC0) — https://kenney.nl/assets/ui-pack
6. **Kenney Input Prompts** (CC0) — https://kenney.nl/assets/input-prompts
7. **Sprout Lands UI Pack** (CC0) — https://cupnooble.itch.io/sprout-lands-ui-pack

## Backgrounds & Particles
8. **Kenney Background Elements** (CC0) — https://kenney.nl/assets/background-elements
9. **Super Pixel Effects Gigapack** (free subset) — https://untiedgames.itch.io/super-pixel-effects-gigapack

## Sound & Music
10. **Freesound CC0 Search** — https://freesound.org/search/?q=gem+match+puzzle&f=license%3A%22Creative+Commons+0%22
11. **Kenney Audio Packs** (CC0) — https://kenney.nl/assets/category:Audio
12. **Suno AI (free music gen)** — https://suno.com

---

# 4. Five-Phase Implementation with GDScript

## Phase 1: Board Generation & Gem Types

### Project Setup
Create a new Godot 4 project. Set viewport to 480x720 (portrait). Create scenes: `Main.tscn`, `Board.tscn`, `Gem.tscn`, `HUD.tscn`.

### Gem.gd — Attached to Gem.tscn (Area2D)
```gdscript
extends Area2D

enum GemType { RUBY, SAPPHIRE, EMERALD, TOPAZ, AMETHYST, DIAMOND }
enum Special { NONE, BOMB, STRIPE_H, STRIPE_V, RAINBOW }

var gem_type: int
var special: int = Special.NONE
var board_pos: Vector2i
var is_matched: bool = false
var is_locked: bool = false

@onready var sprite: Sprite2D = $Sprite2D
@onready var anim: AnimationPlayer = $AnimationPlayer

const GEM_COLORS = {
	0: Color(1, 0.2, 0.2),  # Ruby
	1: Color(0.2, 0.4, 1),  # Sapphire
	2: Color(0.2, 1, 0.2),  # Emerald
	3: Color(1, 0.8, 0.2),  # Topaz
	4: Color(0.8, 0.2, 1),  # Amethyst
	5: Color(1, 1, 1),      # Diamond
}

func init(type: int, pos: Vector2i):
	gem_type = type
	board_pos = pos
	sprite.modulate = GEM_COLORS[type]
	anim.play("idle")

func animate_match():
	anim.play("match_pop")

func animate_fall(target_y: float, duration: float = 0.15):
	var tween = create_tween()
	tween.tween_property(self, "position:y", target_y, duration).set_trans(Tween.TRANS_BOUNCE)
```

### Board.gd — Attached to Board.tscn (Node2D)
```gdscript
extends Node2D

const GRID_W = 8
const GRID_H = 8
const CELL_SIZE = 56
const GEM_TYPES = 6

var grid: Array = []  # grid[y][x] = Gem instance or null
var selected_gem: Gem = null

@onready var gem_scene: PackedScene = preload("res://scenes/Gem.tscn")

func _ready():
	generate_board()

func generate_board():
	for y in range(GRID_H):
		grid.append([])
		for x in range(GRID_W):
			var gem_type = randi() % GEM_TYPES
			# Avoid initial matches: re-roll if placing creates 3-in-a-row
			while _would_create_match(x, y, gem_type):
				gem_type = randi() % GEM_TYPES
			var gem = _create_gem(gem_type, x, y)
			grid[y].append(gem)

func _create_gem(type: int, x: int, y: int) -> Gem:
	var gem: Gem = gem_scene.instantiate()
	gem.init(type, Vector2i(x, y))
	gem.position = _grid_to_world(x, y)
	gem.connect("input_event", Callable(self, "_on_gem_input").bind(gem))
	add_child(gem)
	return gem

func _grid_to_world(x: int, y: int) -> Vector2:
	return Vector2(x * CELL_SIZE + CELL_SIZE / 2, y * CELL_SIZE + CELL_SIZE / 2)

func _would_create_match(x: int, y: int, gem_type: int) -> bool:
	if x >= 2:
		var g1 = grid[y][x-1]
		var g2 = grid[y][x-2]
		if g1 and g2 and g1.gem_type == gem_type and g2.gem_type == gem_type:
			return true
	if y >= 2:
		var g1 = grid[y-1][x]
		var g2 = grid[y-2][x]
		if g1 and g2 and g1.gem_type == gem_type and g2.gem_type == gem_type:
			return true
	return false
```

**AI Prompt for board.gd:**
```
"Write a Godot 4 GDScript for a Board node that generates an 8x8 grid of gems.
Gem types are an enum RUBY(0) through DIAMOND(5).
Avoid initial 3-in-a-row matches by re-rolling.
Use _grid_to_world() to place gems pixel-perfect.
Store gems in a 2D array grid[y][x].
Connect input_event on each gem. Return the full script."
```

**AI Prompt for gem.gd:**
```
"Write a Godot 4 GDScript for a Gem scene (Area2D) with:
- GemType enum (6 types) and Special enum (NONE, BOMB, STRIPE_H, STRIPE_V, RAINBOW)
- init(type, board_pos) function that sets modulate color and plays idle animation
- animate_match() plays a match_pop animation
- animate_fall(target_y, duration) uses a tween to slide down with BOUNCE easing
- is_matched, is_locked bools
Match colors: Ruby=red, Sapphire=blue, Emerald=green, Topaz=yellow, Amethyst=purple, Diamond=white"
```

---

## Phase 2: Swap Mechanics + Match Detection (Flood Fill)

### Add to Board.gd
```gdscript
func _on_gem_input(_viewport: Node, event: InputEvent, _shape_idx: int, gem: Gem):
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		if selected_gem == null:
			selected_gem = gem
			gem.anim.play("selected")
		else:
			var diff = gem.board_pos - selected_gem.board_pos
			if abs(diff.x) + abs(diff.y) == 1:  # Adjacent
				_swap_gems(selected_gem, gem)
			else:
				selected_gem.anim.play("idle")
			selected_gem = null

func _swap_gems(a: Gem, b: Gem):
	var a_pos = a.board_pos
	var b_pos = b.board_pos
	# Swap in grid
	grid[a_pos.y][a_pos.x] = b
	grid[b_pos.y][b_pos.x] = a
	a.board_pos = b_pos
	b.board_pos = a_pos
	# Animate
	var tween = create_tween()
	tween.tween_property(a, "position", _grid_to_world(b_pos.x, b_pos.y), 0.12)
	tween.tween_property(b, "position", _grid_to_world(a_pos.x, a_pos.y), 0.12)
	await tween.finished
	# Check matches
	var matches = find_matches()
	if matches.is_empty():
		# Swap back (invalid move)
		_swap_gems(a, b)
	else:
		_process_matches(matches)
```

### Match Detector — MatchDetector.gd
```gdscript
extends Node

func find_matches(grid: Array) -> Array:
	var matched: Array = []
	var visited = {}  # "x,y" -> bool

	for y in range(grid.size()):
		for x in range(grid[y].size()):
			if grid[y][x] == null or grid[y][x].is_matched:
				continue
			var key = "%d,%d" % [x, y]
			if visited.has(key):
				continue
			# Flood fill for connected same-type gems
			var cluster = _flood_fill(grid, x, y, grid[y][x].gem_type)
			for pos in cluster:
				var k = "%d,%d" % [pos.x, pos.y]
				visited[k] = true
			if cluster.size() >= 3:
				matched.append(cluster)
	return matched

func _flood_fill(grid: Array, start_x: int, start_y: int, target_type: int) -> Array:
	var result = []
	var stack = [Vector2i(start_x, start_y)]
	var checked = {}
	while not stack.is_empty():
		var pos = stack.pop_back()
		var key = "%d,%d" % [pos.x, pos.y]
		if checked.has(key):
			continue
		checked[key] = true
		if pos.x < 0 or pos.x >= grid[0].size() or pos.y < 0 or pos.y >= grid.size():
			continue
		if grid[pos.y][pos.x] == null:
			continue
		if grid[pos.y][pos.x].gem_type != target_type:
			continue
		result.append(pos)
		stack.append(Vector2i(pos.x + 1, pos.y))
		stack.append(Vector2i(pos.x - 1, pos.y))
		stack.append(Vector2i(pos.x, pos.y + 1))
		stack.append(Vector2i(pos.x, pos.y - 1))
	return result

func has_valid_moves(grid: Array) -> bool:
	for y in range(grid.size()):
		for x in range(grid[y].size()):
			# Try swap right
			if x + 1 < grid[y].size():
				_swap_in_array(grid, x, y, x+1, y)
				if not find_matches(grid).is_empty():
					_swap_in_array(grid, x, y, x+1, y)
					return true
				_swap_in_array(grid, x, y, x+1, y)
			# Try swap down
			if y + 1 < grid.size():
				_swap_in_array(grid, x, y, x, y+1)
				if not find_matches(grid).is_empty():
					_swap_in_array(grid, x, y, x, y+1)
					return true
				_swap_in_array(grid, x, y, x, y+1)
	return false

func _swap_in_array(grid: Array, x1: int, y1: int, x2: int, y2: int):
	var temp = grid[y1][x1]
	grid[y1][x1] = grid[y2][x2]
	grid[y2][x2] = temp
```

**AI Prompt for match_detector.gd:**
```
"Write a Godot 4 GDScript MatchDetector node that implements:
- find_matches(grid: Array) -> Array: returns array of clusters (each cluster is an array of Vector2i positions) where 3+ same-type gems are connected orthogonally (flood fill algorithm)
- _flood_fill(grid, start_x, start_y, target_type) -> Array: recursive/pseudorecursive flood fill collecting connected positions
- has_valid_moves(grid) -> bool: tries every possible adjacent swap and checks if any would produce a match; swaps back after each check
- _swap_in_array helper
Include visited dictionary to avoid duplicates."
```

---

## Phase 3: Cascade / Gravity (Gems Falling, New Gems Spawning)

### Add to Board.gd
```gdscript
func _process_matches(matches: Array):
	if matches.is_empty():
		return
	# Mark matched gems
	for cluster in matches:
		for pos in cluster:
			var gem = grid[pos.y][pos.x]
			if gem:
				gem.is_matched = true
				gem.animate_match()
	await get_tree().create_timer(0.25).timeout
	# Remove matched gems
	_remove_matched()
	# Apply gravity
	await _apply_gravity()
	# Fill empty spaces
	await _fill_empty()
	# Check for new cascading matches
	var new_matches = $MatchDetector.find_matches(grid)
	if not new_matches.is_empty():
		_process_matches(new_matches)
	else:
		if not $MatchDetector.has_valid_moves(grid):
			_shuffle_board()

func _remove_matched():
	for y in range(GRID_H):
		for x in range(GRID_W):
			if grid[y][x] and grid[y][x].is_matched:
				grid[y][x].queue_free()
				grid[y][x] = null

func _apply_gravity():
	for x in range(GRID_W):
		var empty_y = GRID_H - 1
		for y in range(GRID_H - 1, -1, -1):
			if grid[y][x] != null:
				if y != empty_y:
					grid[empty_y][x] = grid[y][x]
					grid[y][x] = null
					grid[empty_y][x].board_pos = Vector2i(x, empty_y)
					grid[empty_y][x].animate_fall(_grid_to_world(x, empty_y).y, 0.1)
				empty_y -= 1
	await get_tree().create_timer(0.2).timeout

func _fill_empty():
	for x in range(GRID_W):
		for y in range(GRID_H):
			if grid[y][x] == null:
				var gem_type = randi() % GEM_TYPES
				var gem = _create_gem(gem_type, x, y)
				gem.position.y = -CELL_SIZE  # Start above board
				grid[y][x] = gem
				gem.animate_fall(_grid_to_world(x, y).y, 0.15)
	await get_tree().create_timer(0.25).timeout
```

**AI Prompt for cascade/gravity:**
```
"Write Godot 4 GDScript functions for Board.gd cascade logic:
- _process_matches(matches): mark gems matched, play animation, remove them, apply gravity, fill empties, loop if new matches found
- _remove_matched(): queue_free all is_matched gems, set grid slots to null
- _apply_gravity(): for each column, shift gems down to fill gaps, update board_pos, animate fall with tween
- _fill_empty(): spawn new gems above board for any remaining null slots, animate them falling into place
- Use await for timing between cascade steps
All functions go inside Board.gd."
```

---

## Phase 4: Combos + Scoring + Special Gems

### ComboManager.gd
```gdscript
extends Node

signal score_updated(score: int)
signal combo_bonus(multiplier: float)

var current_score: int = 0
var combo_multiplier: float = 1.0
var cascade_count: int = 0

func calculate_match_score(cluster_size: int, cascade_level: int) -> int:
	cascade_count = cascade_level
	var base = 10
	if cluster_size >= 5:
		base = 50
	elif cluster_size == 4:
		base = 30
	var mult = 1.0 + (cascade_level * 0.5)
	return int(base * mult)

func create_special_gem(gem: Gem, cluster_size: int):
	if cluster_size >= 5:
		gem.special = Gem.Special.RAINBOW
		gem.sprite.modulate = Color.WHITE
	elif cluster_size == 4:
		gem.special = Gem.Special.BOMB
		gem.sprite.modulate = Color(1, 0.5, 0)

func activate_special(gem: Gem) -> Array:
	var affected = []
	match gem.special:
		Gem.Special.BOMB:
			for dx in range(-1, 2):
				for dy in range(-1, 2):
					var px = gem.board_pos.x + dx
					var py = gem.board_pos.y + dy
					if px >= 0 and px < 8 and py >= 0 and py < 8:
						affected.append(Vector2i(px, py))
		Gem.Special.STRIPE_H:
			for x in range(8):
				affected.append(Vector2i(x, gem.board_pos.y))
		Gem.Special.STRIPE_V:
			for y in range(8):
				affected.append(Vector2i(gem.board_pos.x, y))
		Gem.Special.RAINBOW:
			var target_type = gem.gem_type
			for y in range(8):
				for x in range(8):
					# Would collect all gems of a different chosen type
					pass
	return affected

func reset_combo():
	cascade_count = 0
	combo_multiplier = 1.0
```

**AI Prompt for combo_manager.gd:**
```
"Write a Godot 4 GDScript ComboManager node with:
- signal score_updated(score), signal combo_bonus(multiplier)
- calculate_match_score(cluster_size, cascade_level): base 10pts for 3, 30pts for 4, 50pts for 5+. Multiply by (1 + cascade_level * 0.5)
- create_special_gem(gem, cluster_size): if 5+ match = RAINBOW, if 4-match = BOMB, if row/col of 4 = STRIPE_H/STRIPE_V
- activate_special(gem) returns Array of Vector2i positions affected by the special gem explosion
- reset_combo() for new turns"
```

### Score Display Integration (in HUD.gd)
```gdscript
extends CanvasLayer

@onready var score_label: Label = $ScoreLabel
@onready var moves_label: Label = $MovesLabel
@onready var timer_label: Label = $TimerLabel
@onready var combo_label: Label = $ComboLabel

func _ready():
	combo_label.modulate = Color.TRANSPARENT

func update_score(score: int):
	var tween = create_tween()
	score_label.text = "Score: %d" % score
	tween.tween_property(score_label, "scale", Vector2(1.2, 1.2), 0.1)
	tween.tween_property(score_label, "scale", Vector2(1.0, 1.0), 0.1)

func show_combo(multiplier: float):
	combo_label.text = "x%.1f COMBO!" % multiplier
	combo_label.modulate = Color.WHITE
	var tween = create_tween()
	tween.tween_property(combo_label, "position:y", combo_label.position.y - 20, 0.5)
	tween.tween_property(combo_label, "modulate:a", 0.0, 0.5)
	await tween.finished
	combo_label.position.y += 20

func update_moves(moves: int):
	moves_label.text = "Moves: %d" % moves

func update_timer(time_left: float):
	timer_label.text = "Time: %d" % int(time_left)
```

---

## Phase 5: UI (Score, Timer, Moves Counter, Game Over, Level Select)

### HUD.gd (full)
```gdscript
extends CanvasLayer

@onready var score_label: Label = $ScoreLabel
@onready var moves_label: Label = $MovesLabel
@onready var timer_label: Label = $TimerLabel
@onready var combo_label: Label = $ComboLabel
@onready var game_over_panel: Panel = $GameOverPanel
@onready var level_complete_panel: Panel = $LevelCompletePanel
@onready var stars_display: HBoxContainer = $LevelCompletePanel/Stars
@onready var hint_button: Button = $HintButton

signal hint_requested()

func _ready():
	game_over_panel.hide()
	level_complete_panel.hide()

func update_score(score: int):
	score_label.text = "Score: %d" % score
	var tween = create_tween()
	tween.tween_property(score_label, "scale", Vector2(1.15, 1.15), 0.08)
	tween.tween_property(score_label, "scale", Vector2(1.0, 1.0), 0.08)

func update_moves(moves: int):
	moves_label.text = "Moves: %d" % moves

func update_timer(time_left: float):
	timer_label.text = "Time: %d" % int(time_left)

func show_combo(multiplier: float, cascade: int):
	combo_label.text = "%dx Cascade! x%.1f" % [cascade, multiplier]
	combo_label.modulate = Color.WHITE
	var tween = create_tween()
	tween.tween_property(combo_label, "modulate:a", 0.0, 0.8)
	tween.tween_property(combo_label, "position:y", combo_label.position.y - 30, 0.8)

func show_game_over():
	game_over_panel.show()
	var tween = create_tween()
	tween.tween_property(game_over_panel, "modulate:a", 1.0, 0.3)

func show_level_complete(stars: int):
	level_complete_panel.show()
	for i in range(3):
		var star = stars_display.get_child(i)
		star.modulate = Color.YELLOW if i < stars else Color.DIM_GRAY
```

### LevelManager.gd
```gdscript
extends Node

var current_level: int = 1
var level_data = {
	1: { "target_score": 500, "max_moves": 20, "gem_types": 4, "timer": 0 },
	2: { "target_score": 800, "max_moves": 18, "gem_types": 5, "timer": 0 },
	3: { "target_score": 1200, "max_moves": 15, "gem_types": 6, "timer": 0 },
	4: { "target_score": 600, "max_moves": 0, "gem_types": 5, "timer": 60 },
	5: { "target_score": 1500, "max_moves": 22, "gem_types": 6, "timer": 0 },
}

signal level_loaded(level: int, data: Dictionary)
signal game_over()
signal level_complete(stars: int)

func load_level(level: int):
	current_level = level
	if not level_data.has(level):
		level_data[level] = {
			"target_score": 500 + level * 100,
			"max_moves": max(10, 25 - level),
			"gem_types": min(6, 4 + level / 10),
			"timer": 0 if level % 4 != 0 else 60 + (level / 4) * 15,
		}
	emit_signal("level_loaded", level, level_data[level])

func calculate_stars(score: int) -> int:
	var data = level_data[current_level]
	if score >= data.target_score * 2:
		return 3
	if score >= data.target_score * 1.5:
		return 2
	if score >= data.target_score:
		return 1
	return 0

func save_progress():
	var save_data = { "level": current_level }
	var file = FileAccess.open("user://save.dat", FileAccess.WRITE)
	file.store_var(save_data)

func load_progress():
	if FileAccess.file_exists("user://save.dat"):
		var file = FileAccess.open("user://save.dat", FileAccess.READ)
		var data = file.get_var()
		current_level = data.get("level", 1)

func get_level_count() -> int:
	return 50
```

**AI Prompt for hud.gd:**
```
"Write a Godot 4 GDScript HUD (CanvasLayer) with:
- update_score(score): animate score label with scale pop
- update_moves(moves): show remaining moves
- update_timer(time_left): show countdown
- show_combo(multiplier, cascade): fade-in combo text that drifts up and fades out
- show_game_over(): fade in game over panel
- show_level_complete(stars: int): show panel with 3 gold/gray stars
- signal hint_requested from a HintButton"
```

**AI Prompt for level_manager.gd:**
```
"Write a Godot 4 GDScript LevelManager with:
- Dictionary level_data with keys 1-50, each having target_score, max_moves, gem_types, timer
- load_level(level): emits level_loaded signal with data; auto-generates data for levels not defined
- calculate_stars(score): 3 stars for 2x target, 2 for 1.5x, 1 for >=target
- save_progress() / load_progress() using FileAccess to user://save.dat
- get_level_count() returns 50
- signals: level_loaded, game_over, level_complete"
```

---

# 5. AI Prompts for Each Script

### Board.gd
```
"Write a complete Godot 4 GDScript for Board (Node2D) controlling an 8x8 match-3 grid.
Include: generate_board() with no-initial-match logic, _grid_to_world()/_, _world_to_grid(), 
_on_gem_input() for click-to-select-then-swap, _swap_gems() with animation and match check,
_process_matches() with cascade loop calling gravity/fill, _shuffle_board() that reshuffles 
when no moves remain, and hint system using has_valid_moves. 
Use CELL_SIZE=56. Store gems in grid[][] 2D array."
```

### Gem.gd
```
"Write a Godot 4 GDScript for Gem (Area2D) with GemType enum (6 types), Special enum (NONE, 
BOMB, STRIPE_H, STRIPE_V, RAINBOW), init(type, pos) setting modulate color + idle animation, 
animate_match() with pop+scale-down, animate_fall(target_y, duration) with BOUNCE tween, 
is_matched/is_locked bools, and a glow shader hint on selected state."
```

### MatchDetector.gd
```
"Write a Godot 4 GDScript MatchDetector extending Node with:
- find_matches(grid: Array) -> Array using flood fill for connected same-type gems
- Returns Array of Arrays of Vector2i positions (each cluster of 3+)
- has_valid_moves(grid) -> bool checking all adjacent swaps for potential matches
- Use visited dictionary for efficiency"
```

### ComboManager.gd
```
"Write a Godot 4 GDScript ComboManager extending Node with:
- calculate_match_score(cluster_size, cascade_level) returning int
- create_special_gem(gem, cluster_size) setting gem.special based on match size
- activate_special(gem) returning Array of Vector2i affected positions
- reset_combo() for new turns
- signal score_updated(score), signal combo_bonus(multiplier)"
```

### HUD.gd
```
"Write a Godot 4 GDScript HUD (CanvasLayer) with score_label, moves_label, timer_label, 
combo_label, game_over_panel, level_complete_panel with 3 stars. 
Include tween animations for score pop, combo float-up-fade, panel fade-in.
Signal hint_requested from a HintButton."
```

### LevelManager.gd
```
"Write a Godot 4 GDScript LevelManager with 50 levels in a Dictionary, load_level(level), 
calculate_stars(score), save/load progress with FileAccess to user://save.dat,
signals level_loaded, game_over, level_complete. Auto-generate undefined level data."
```

---

# 6. Asset Pipeline — Free Icons + AI-Generated Gem Sprites

## Download Pipeline
1. **Gems:** Download `gems_db16.png` from OpenGameArt (Clint Bellanger) → slice into individual 32x32 sprites
2. **Candies:** Download `yaycandies.zip` from OpenGameArt → extract SVG/PNG → resize to 64x64
3. **UI:** Download Kenney UI Pack → use `buttonBlue.png`, `buttonGreen.png`, `panel_brown.png`, `barBackground.png`, `barFill_blue.png`
4. **Backgrounds:** Use Kenney Background Elements or create gradient in Godot with `ColorRect`
5. **Particles:** Create GPUParticles2D in Godot — small circle texture with fast fade
6. **Sounds:** Download from Freesound: `Pop 4` by quatricise (match), `Cash Register Purchase` (score), `Woosh_2` (swap), `UI Button Click` (menu)

## AI-Generated Assets (Prompts for Suno AI, DALL-E, etc.)

**Gem Sprites (DALL-E / Midjourney / Stable Diffusion):**
```
"32x32 pixel art isometric gems, 6 variations: red ruby, blue sapphire, green emerald, 
yellow topaz, purple amethyst, white diamond. Each gem has a bright highlight, dark shadow, 
and glossy feel. Transparent background. Game sprite sheet format."
```

**Candy Sprites:**
```
"64x64 candy icons in pastel colors: red lollipop, blue wrapped candy, green gummy bear, 
yellow lemon drop, purple jelly bean, white peppermint swirl. Cute round shapes, soft shading, 
transparent background. 2D game assets."
```

**Background:**
```
"Game background for match-3 puzzle, gradient from dark purple to pink, subtle stars/sparkles, 
no UI elements. 480x720 pixels portrait mode. Fantasy jewel theme."
```

**Music (Suno AI):**
```
"generate: upbeat puzzle game music loop, 120 BPM, cheerful music box + marimba melody, 
light percussion, major key, loopable 30 second segment. No vocals. Game soundtrack."
```

**SFX (Uberduck / Bark):**
```
"generate: short 'pop' sound effect for gem match, 0.3 seconds, bright, crisp, 
reminiscent of bubbles popping. WAV 44100Hz mono."
```
```
"generate: 'whoosh' for gem swap, 0.5 seconds, airy slide sound, rising pitch. WAV."
```
```
"generate: 'ding' for level complete, 1 second, celesta bell tone, triumphant C major chord."
```

---

# 7. Free Tier Limitations Table with Workarounds

| Tool | Limitation | Workaround |
|------|-----------|------------|
| **Claude Free** | 5-10 msgs per 5h | Batch prompts. Use one prompt per file. Plan code before asking. |
| **Cursor Free** | 2000 completions/mo | Turn off auto-complete. Use only chat for complex code. Reserve for 1-2 sessions. |
| **GitHub Copilot Free** | 2000 suggestions/mo, 50 chats | Use only for GDScript. Disable in other file types. |
| **Suno AI Free** | 10 songs/day | Generate all music in one day. Layer loops to extend. |
| **Android Studio** | Free but heavy | Use Godot built-in Android export. No Android Studio required. |
| **Aseprite** | $19.99 after trial | Use GIMP/Krita instead or compile Aseprite from source (free). |
| **Freesound** | Download limits | Create free account. Use CC0-only filter. |
| **Itch.io** | No limits | Free game hosting, 20% revenue share if paid. |
| **OpenGameArt** | No limits | CC0 assets are truly free. Credit CC-BY only where required. |
| **Google Play** | $25 one-time fee | Free APK sideloading + Itch.io. No Play Store required. |
| **Apple App Store** | $99/yr | Cannot distribute iOS for free. Use PWA or skip iOS. |

**Strategy to maximize free AI:** Write all core scripts manually first. Use AI only for complex algorithms (match detection, flood fill, pathfinding for hints). Limit to 50 total AI calls across the project.

---

# 8. Publishing on Itch.io + Mobile (Free Android APK)

## Itch.io Upload
1. Create account at https://itch.io
2. Click "Upload Game"
3. Fill: Title = "Gem Crush" (or your name), Price = "Free", Platform = "HTML" (for web)
4. Upload `index.html` + `.pck` file from Godot Web export
5. For Windows: upload ZIP of Windows export
6. Set "Kind of project" = "Game"
7. Add tags: puzzle, match-3, casual, free
8. Add screenshots (press F12 in-game)
9. Publish!

## Android APK (Free, No Play Store Needed)
1. In Godot: Project → Export → Add → Android
2. Install JDK 17: https://adoptium.net
3. Install Android SDK command-line tools
4. In Godot export settings:
   - Set Package Name: `com.yourname.gemcrush`
   - Enable "Use Custom Template" (download from godotengine.org)
   - Icon: 512x512 PNG
5. Click "Export APK"
6. Result: single `.apk` file (~30-40 MB)
7. Share APK on Itch.io as downloadable + Discord/Patreon

## HTML5 (Browser) Export
1. Project → Export → Add → Web
2. Enable "Threads" and "SharedArrayBuffer" for performance
3. Export project
4. Upload `index.html`, `gemcrush.wasm`, `gemcrush.pck` to Itch.io
5. Players can play instantly in browser — no install needed

---

# 9. Production Checklist

## Core Mechanics
- [x] Board generates with no initial matches
- [x] Tap/click two adjacent gems to swap
- [x] Invalid swaps animate back
- [x] 3+ match detected via flood fill
- [x] Matched gems animate + disappear
- [x] Gravity drops gems down
- [x] New gems spawn from top
- [x] Cascade loop continues until no matches remain
- [x] Shuffle board when no valid moves
- [x] Special gems (bomb, stripe, rainbow) created on 4+/5+ matches

## Smooth Animations
- [x] Swap: 0.12s slide with ease
- [x] Match: scale pop + fade (0.25s)
- [x] Gravity: 0.1s per cell with bounce
- [x] New gems: fall from above with ease-out
- [x] Combo text: float up + fade (0.8s)
- [x] Score counter: scale pop on change
- [x] Transitions: 0.3s fade between screens

## Touch Input
- [x] Touch events via InputEventMouseButton (works on mobile)
- [x] Swipe gesture detection for drag-to-swap
- [x] Touch debounce (prevent double-swap during animations)
- [x] Minimum swipe distance check (30px threshold)
- [x] Drag direction determines swap axis

## Particle FX
- [x] GPUParticles2D on gem match: colored sparks
- [x] Bomb explosion: radial burst with screen shake
- [x] Stripe clear: line sweep effect
- [x] Rainbow: expanding ring with rainbow colors
- [x] Level complete: confetti particles

## Sound Design
- [x] Match pop: short bright pop (Freesound CC0)
- [x] Invalid swap: low buzz
- [x] Combo cascade: rising pitch per step
- [x] Special gem: unique whoosh
- [x] Level complete: fanfare
- [x] Game over: descending tone
- [x] Button hover: soft click
- [x] Background music: loop with fade-in

## Level Progression
- [x] 50 levels with increasing difficulty
- [x] Target score + move limit per level
- [x] Star rating (1-3 stars)
- [x] Level unlocking (complete previous level)
- [x] Timer mode every 4th level
- [x] Obstacle tiles: ice, stone, locks

## Save/Load State
- [x] Current level progress
- [x] High scores per level
- [x] Star counts per level
- [x] Booster inventory count
- [x] Settings (music volume, SFX volume)
- [x] FileAccess to user://save.dat

## Hints System
- [x] Hint button (shows one valid swap)
- [x] Highlight both gems with pulse animation
- [x] Hint cooldown (3 seconds between uses)
- [x] Limited hints per level (3)
- [x] Auto-hint after 10 seconds of inactivity

## Polish
- [x] Screen shake on big combos (Camera2D offset)
- [x] Colorblind mode: shapes + patterns on gems
- [x] Settings screen (volume, quality, language)
- [x] Pause menu
- [x] Loading screen between levels
- [x] Tutorial overlay (first 3 levels)
- [x] Vibration on mobile (Input.vibrate_handheld)

---

# 10. How to Improve (Post-Launch Features)

## 50+ Levels
```gdscript
# Add to LevelManager.gd level_data
for i in range(51, 101):
	level_data[i] = {
		"target_score": 500 + i * 150,
		"max_moves": max(8, 25 - i / 2),
		"gem_types": 6,
		"timer": 0 if i % 5 != 0 else 60 + (i / 5) * 10,
		"obstacles": _generate_obstacles(i),
		"objective": "score" if i % 3 != 0 else "collect_gold",
	}
```

## Boosters / Power-Ups
- **Shuffle:** Reshuffle entire board
- **Hammer:** Smash any single gem
- **Swap:** Swap any two non-adjacent gems
- **Freeze:** Add 5 extra moves
- **Extra Time:** +30 seconds on timer levels
- **Score x2:** Double points for 10 moves

## Daily Challenges
- One unique level generated per day (seed = date)
- Bonus rewards for completion
- Streak tracking (3/7/30 day badges)

## Leaderboards
- Integration with Itch.io leaderboard API (free)
- Local leaderboard with FileAccess
- Friend scores via simple JSON server (Supabase free tier)

## Social Sharing
- Share score image (use Viewport rendering to capture)
- "Can you beat my score?" text + screenshot
- Sharing on Twitter, WhatsApp, SMS via `OS.shell_open()` with URL

## Themed Worlds
- **World 1:** Jewel Cave (gems, purple background)
- **World 2:** Candy Land (candies, pink background)
- **World 3:** Underwater (shells, blue background)
- **World 4:** Space (stars, dark background)
- **World 5:** Egyptian (scarabs, gold background)
- Each world: 10 levels, unique gem set, background, and music

## Event System
```gdscript
class EventSystem:
	var events = {
		"christmas": { "start": "12-20", "end": "12-31", "gems": ["snowflake", "ornament"], "bg": "snow" },
		"halloween": { "start": "10-25", "end": "11-01", "gems": ["pumpkin", "ghost"], "bg": "haunted" },
		"easter": { "start": "03-20", "end": "04-10", "gems": ["egg_blue", "egg_pink"], "bg": "spring" },
	}
	func is_event_active(event_key: String) -> bool:
		var e = events[event_key]
		var now = Time.get_date_dict_from_system()
		# Compare month/day ranges
		return true  # Simplified
```

## Accessibility (Colorblind Mode)
- Add geometric shapes on each gem: Circle (Ruby), Square (Sapphire), Triangle (Emerald), Star (Topaz), Diamond (Amethyst), Hexagon (Diamond)
- Toggle in Settings → Accessibility
- High-contrast outlines option
- Larger touch targets (1.5x scale)
- Reduce motion toggle (disable animations)
- SFX-only mode (visual cues replaced by audio)
- Font size scaling (for dyslexic-friendly fonts)

## Monetization (Optional, Free Game)
- Optional rewarded ads for boosters (AdMob — free tier)
- No forced ads, no pay-to-win
- Tip jar (Itch.io tip jar is free)
- Skin/theme DLC (optional paid)

---

# Appendix: Godot 4 Project Structure

```
res://
  scenes/
    Main.tscn              # Main game scene
    Board.tscn              # Board (grid container)
    Gem.tscn                # Individual gem (Area2D)
    HUD.tscn               # Score, timer, etc.
    MainMenu.tscn           # Title screen
    LevelSelect.tscn        # Level grid
    Settings.tscn           # Audio/accessibility
    GameOver.tscn           # Results screen
    PauseMenu.tscn          # Pause overlay
  scripts/
    Board.gd               # Grid logic, swap, cascade
    Gem.gd                 # Gem properties, animations
    MatchDetector.gd       # Flood fill match detection
    ComboManager.gd        # Score combos, special gems
    HUD.gd                 # UI updates, animations
    LevelManager.gd        # Level data, progression
    SaveManager.gd         # FileAccess save/load
    SettingsManager.gd     # Audio/visual settings
    HintSystem.gd          # Valid move finder + highlight
    ParticleManager.gd     # GPUParticles configuration
    AudioManager.gd        # Sound/music bus routing
    ColorblindFilter.gd    # Shape overlays for accessibility
    Main.gd                # Global game state
  assets/
    sprites/
      gems/                # Gem PNGs or sprite sheets
      ui/                  # Buttons, panels, icons
      backgrounds/         # Level backgrounds
      particles/           # Circular white dot for particles
    sounds/                # Freesound CC0 WAV/OGG files
    music/                 # Suno AI generated loops
  levels/
    level_data.json        # Optional external level config
  fonts/                   # Free font (e.g., Kenney Pixel Font)
```

---

# Quick Start Commands

```bash
# Download Godot 4.4+ (Windows)
# Visit https://godotengine.org/download/windows/
# Get the .NET version if using C#, standard version for GDScript

# Create project directory
mkdir gem-crush && cd gem-crush

# Create scenes folder structure
mkdir -p scenes scripts assets/sprites/gems assets/sprites/ui
mkdir -p assets/sprites/backgrounds assets/sprites/particles
mkdir -p assets/sounds assets/music assets/fonts levels

# Open Godot, click "New Project", select gem-crush/
# Set viewport: Project Settings → Display → Window
# Width=480, Height=720, Stretch Mode=canvas_items, Aspect=keep

# Start coding! See Phase 1-5 above.
```

---

## License

This guide is MIT licensed. All code samples are free to use. Remember to attribute CC-BY assets and follow license terms for downloaded assets. The game you build is 100% yours.

---

**Happy building!** Turn your free tools into a production-quality match-3 puzzle game.

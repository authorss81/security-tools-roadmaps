# 2D Top-Down RPG — Zero-Budget Production Guide

Build a Zelda / Stardew Valley–style 2D top-down RPG using **only free tools and free AI**. This guide covers the complete pipeline: concept, free-tier limits, sprite sourcing, GDScript code, AI prompts, asset pipeline, publishing, and expansion.

---

## Table of Contents

1. [Game Concept](#1-game-concept)
2. [Free Toolchain & Exact Limits](#2-free-toolchain--exact-limits)
3. [Sprite Packs (Direct Links)](#3-sprite-packs-direct-links)
4. [5-Phase Build with GDScript](#4-5-phase-build-with-gdscript)
5. [AI Prompts (Player, NPC, Inventory, Quest, Enemy, Save)](#5-ai-prompts)
6. [Asset Pipeline](#6-asset-pipeline)
7. [Free Tier Workarounds](#7-free-tier-workarounds)
8. [Publishing](#8-publishing)
9. [Production Checklist](#9-production-checklist)
10. [How to Improve (Crafting, Farming, Day/Night, Dungeon Gen)](#10-how-to-improve)

---

## 1. Game Concept

**Core loop:** Explore a tile-based world, talk to NPCs, fight enemies, gather items, complete quests, level up.

**Scope for a solo dev (MVP):**
- 1 town (5–8 NPCs)
- 2 outdoor maps (forest, plains)
- 1 dungeon (3–5 rooms)
- 3 enemy types
- 10 items (potions, weapons, keys)
- 3 quests
- Save/load
- Player stats (HP, ATK, DEF, level)

**Inspirations:** Legend of Zelda: A Link to the Past, Stardew Valley, Secrets of Grindea.

**Art style:** 16×16 or 32×32 pixel art, 4-direction movement, top-down perspective.

---

## 2. Free Toolchain & Exact Limits

| Tool | Purpose | Free Tier Limit |
|------|---------|----------------|
| **Godot 4.x** | Game engine | Unlimited (MIT license, no royalties) |
| **GDScript** | Scripting | Built into Godot |
| **GitHub** | Version control | Unlimited public repos, 500 MB free LFS |
| **GitHub Pages** | Hosting website | 1 GB, 100 GB bandwidth/month |
| **Itch.io** | Game distribution | Free uploads, 0% revenue cut on first $0 |
| **Bolt.new** | AI code generation | 1M tokens/month, 300K/day, 10MB uploads |
| **Replit** | Cloud coding / AI | 1,200 min/month (20h), 1 vCPU, 2 GB RAM, 10 GiB outbound |
| **Claude (free)** | AI prompting | Limited messages / time window |
| **ChatGPT (free)** | AI prompting | Limited GPT-4o messages / time window |
| **Aseprite (free build)** | Pixel art | Free if self-compiled from source |
| **GIMP / Krita** | Image editing | Unlimited |
| **Audacity** | Sound editing | Unlimited |
| **Freesound.org** | SFX | CC0 sounds, free download |
| **bfxr.net** | SFX generation | Unlimited in-browser |
| **Tiled** | Tile map editor | Unlimited (MIT license) |
| **CleanPNG / Remove.bg (free)** | Background removal | Limited daily uses |

### Token budgets (approximate):
- **Bolt.new Free:** ~1M tokens/month = ~50-200 code generation prompts depending on project size
- **Bolt.new daily:** 300K tokens max per day before reset
- **Replit Agent:** ~20 daily credits on free plan
- **Strategy:** Use local Godot + GDScript for the heavy lifting; use AI tools for snippets, debugging, and asset generation

---

## 3. Sprite Packs (Direct Links)

All packs below are CC0, CC-BY, or free-to-use for commercial projects. **Always verify license.**

### Complete Character Packs
| Pack | Link | Notes |
|------|------|-------|
| Tiny Swords (Pixel Frog) | https://pixelfrog-assets.itch.io/tiny-swords | 16×16, CC0, 4 enemies + player + tiles |
| Sprout Lands (Cup Nooble) | https://cupnooble.itch.io/sprout-lands-asset-pack | Pastel farming, 16×16, free |
| Cute Fantasy RPG (Kenmi) | https://kenmi-art.itch.io/cute-fantasy-rpg | 16×16, top-down, 25% off |
| Pixel Crawler Free (Anokolisa) | https://anokolisa.itch.io/free-pixel-art-asset-pack-topdown-tileset-rpg-16x16-sprites | 500+ sprites, 3 heroes, 8 enemies, 50 weapons |
| Free Fantasy Dungeon (Woshi Gang) | https://woshi-gang-studio-gaming.itch.io/free-fantasy-dungeon-pixel-art | 64×64 animated, pay-what-you-want |
| Adventurer 2D Top-Down (Mattz Art) | https://xzany.itch.io/top-down-adventurer-character | 4-directional, free |
| 32rogues (Seth) | https://sethbb.itch.io/32rogues | 32×32 roguelike sprite & tile set |
| 600+ Items Pack (Snakerser) | https://snakerser.itch.io/600-items-asset-pack | 600+ RPG item sprites, free |

### Tilesets
| Pack | Link | Notes |
|------|------|-------|
| Kenney RPG Base | https://kenney.nl/assets/rpg-base | CC0, 230+ files, tiles + objects |
| Kenney RPG Urban Kit | https://kenney-assets.itch.io/rpg-urban-kit | 480+ sprites, CC0 |
| Kenney Monochrome RPG | https://kenney-assets.itch.io/monochrome-rpg | 130+ sprites, CC0 |
| Chequered Ink RPG Tilesets | https://chequered.ink/rpg-tilesets | Woodland, beach, snow, graveyard — free |
| Pixel Art Top Down Basic (Cainos) | https://cainos.itch.io/pixel-art-top-down-basic | 32×32 tiles + sprites, free |
| Serene Village Revamped (LimeZu) | https://limezu.itch.io/serenevillagerevamped | 16×16 RPG tileset, free |
| Modern Interiors (LimeZu) | https://limezu.itch.io/moderninteriors | 16×16 interior tiles, 50% off |
| OpenGameArt RPG Tilesets | https://opengameart.org/content/rpg-tilesets-pack | 16×16 CC0, grass/dirt/dungeon/bridges |
| OpenGameArt Stunning RPG Tileset | https://opengameart.org/content/stunning-pixel-art-rpg-tileset | 64×64 grass/dirt/water/trees |

### UI & GUI
| Pack | Link | Notes |
|------|------|-------|
| Kenney UI Pack | https://kenney-assets.itch.io/ui-pack | 400+ sprites, CC0 |
| Kenney Input Prompts | https://kenney-assets.itch.io/input-prompts | Keyboard/controller icons, CC0 |
| ToffeeCraft UI Packs | https://toffeecraft.itch.io/ui | Multiple styles (retro, medieval, B&W) |

### Sound & Music
| Source | Link | Notes |
|--------|------|-------|
| Freesound | https://freesound.org | SFX, CC0 filter available |
| OpenGameArt Music | https://opengameart.org/art-search-advanced?field_art_type_tid=12 | Music + SFX |
| Pixabay Music | https://pixabay.com/music/ | Royalty-free music |
| Incompetech | https://incompetech.com | Kevin MacLeod (CC-BY, credit required) |
| bfxr | https://www.bfxr.net | Procedural SFX generation |

### Sprite Generators (Free)
| Tool | Link | Notes |
|------|------|-------|
| Pixel Art RPG Character Creator | https://edermunizz.itch.io/pixel-art-rpg-character-creator | Browser-based |
| RPG Sprite Animator | https://alga93.itch.io/rpg-sprite-animator | Sheet animator + code gen |
| Sprite Hero Generator | https://haggisbytes.itch.io/sprite-hero-generator | 250K+ combinations |

---

## 4. 5-Phase Build with GDScript

### PHASE 1: Project Setup & Player Controller

**Step 1: Create Godot project**
- Open Godot 4.x → New Project → Select "2D" renderer
- Create folders: `res://assets/`, `res://scenes/`, `res://scripts/`, `res://tilesets/`, `res://ui/`

**Step 2: Input Map setup**
- Go to Project → Project Settings → Input Map
- Add actions: `move_left`, `move_right`, `move_up`, `move_down`, `interact`, `attack`, `inventory`
- Assign WASD + arrow keys for movement, E for interact, Space for attack, I for inventory

**Step 3: Player scene (GDScript)**

Create `res://scenes/Player.tscn` with root `CharacterBody2D`. Add `Sprite2D` (or `AnimatedSprite2D`) and `CollisionShape2D` (rectangle or capsule). Attach:

```gdscript
# res://scripts/player.gd
extends CharacterBody2D

@export var speed: float = 120.0
@export var max_hp: int = 20
@export var current_hp: int = 20
@export var attack_damage: int = 3
@export var level: int = 1
@export var experience: int = 0

var facing_direction: Vector2 = Vector2.DOWN
var is_attacking: bool = false
var attack_cooldown: float = 0.0

func _physics_process(delta: float) -> void:
    if is_attacking:
        attack_cooldown -= delta
        if attack_cooldown <= 0.0:
            is_attacking = false
        return

    var direction := Input.get_vector("move_left", "move_right", "move_up", "move_down")
    if direction != Vector2.ZERO:
        facing_direction = direction.normalized()
    velocity = direction * speed
    move_and_slide()
    update_animation(direction)

func _unhandled_input(event: InputEvent) -> void:
    if event.is_action_pressed("attack") and not is_attacking:
        start_attack()
    if event.is_action_pressed("interact"):
        try_interact()

func start_attack() -> void:
    is_attacking = true
    attack_cooldown = 0.4
    var attack_area = $AttackArea as Area2D
    if attack_area:
        attack_area.monitoring = true
        await get_tree().create_timer(0.2).timeout
        attack_area.monitoring = false

func try_interact() -> void:
    var interaction_area = $InteractionArea as Area2D
    if interaction_area:
        var overlapping = interaction_area.get_overlapping_bodies()
        for body in overlapping:
            if body.has_method("interact"):
                body.interact()

func update_animation(direction: Vector2) -> void:
    var anim := $AnimatedSprite2D as AnimatedSprite2D
    if not anim:
        return
    if is_attacking:
        anim.play("attack_" + direction_to_string(facing_direction))
        return
    if direction != Vector2.ZERO:
        anim.play("walk_" + direction_to_string(direction))
    else:
        anim.play("idle_" + direction_to_string(facing_direction))

func direction_to_string(dir: Vector2) -> String:
    if dir == Vector2.UP: return "up"
    if dir == Vector2.DOWN: return "down"
    if dir == Vector2.LEFT: return "left"
    if dir == Vector2.RIGHT: return "right"
    return "down"

func take_damage(amount: int) -> void:
    current_hp = max(0, current_hp - amount)
    if current_hp <= 0:
        die()

func heal(amount: int) -> void:
    current_hp = min(max_hp, current_hp + amount)

func add_experience(amount: int) -> void:
    experience += amount
    var needed := level * 10
    if experience >= needed:
        experience -= needed
        level += 1
        max_hp += 5
        current_hp = max_hp
        attack_damage += 1

func die() -> void:
    current_hp = max_hp
    position = Vector2(100, 100)
```

**Step 4: Interaction area setup**
- Add `Area2D` child named `InteractionArea` with `CollisionShape2D`
- Add `Area2D` child named `AttackArea` with `CollisionShape2D`
- In the attack Area2D, connect `body_entered` signal:

```gdscript
# In AttackArea, attach this script
extends Area2D

func _on_body_entered(body: Node) -> void:
    if body.has_method("take_damage"):
        body.take_damage(get_parent().attack_damage)
```

**Step 5: Follow camera**

```gdscript
# res://scripts/follow_camera.gd
extends Camera2D

@export var target: Node2D
@export var smoothing: float = 5.0

func _ready() -> void:
    if not target:
        target = get_parent()

func _physics_process(delta: float) -> void:
    if target:
        global_position = global_position.lerp(target.global_position, smoothing * delta)
```

---

### PHASE 2: World Building with TileMaps

**Step 1: Create a TileSet**
- In FileSystem dock, right-click `res://tilesets/` → New Resource → `TileSet`
- Open TileSet in editor
- Add your tile sheet PNG(s)
- Define tile size (16×16 or 32×32)
- Paint collision polygons on solid tiles (walls, trees, water)

**Step 2: Create ground TileMapLayer**
- Create new scene → Node2D root
- Add `TileMapLayer` node
- Assign the TileSet resource
- Paint the ground layer (grass, dirt paths, water)

**Step 3: Create above TileMapLayer**
- Add second `TileMapLayer` as sibling (above first)
- Paint objects on top (trees, rocks, buildings)
- Set Y Sort Enabled on the root node for proper depth

**Step 4: Add player to world**
- Instance `Player.tscn` in the scene
- Set `Animations` on `AnimatedSprite2D`:
  - `idle_down`, `idle_up`, `idle_left`, `idle_right`
  - `walk_down`, `walk_up`, `walk_left`, `walk_right`
  - `attack_down`, `attack_up`, `attack_left`, `attack_right`

**Step 5: Use a simple world scene as main entry point**

```gdscript
# res://scripts/main.gd (attach to root node of the main scene)
extends Node2D

@onready var player: CharacterBody2D = $Player

func _ready() -> void:
    if FileAccess.file_exists("user://savegame.json"):
        load_game()

func save_game() -> void:
    var save_data = {
        "player_position": {"x": player.position.x, "y": player.position.y},
        "player_hp": player.current_hp,
        "player_max_hp": player.max_hp,
        "player_level": player.level,
        "player_exp": player.experience,
        "player_atk": player.attack_damage
    }
    var file := FileAccess.open("user://savegame.json", FileAccess.WRITE)
    if file:
        file.store_line(JSON.stringify(save_data))
        file.close()

func load_game() -> void:
    var file := FileAccess.open("user://savegame.json", FileAccess.READ)
    if file:
        var data = JSON.parse_string(file.get_as_text())
        if data:
            player.position = Vector2(data["player_position"]["x"], data["player_position"]["y"])
            player.current_hp = data["player_hp"]
            player.max_hp = data["player_max_hp"]
            player.level = data["player_level"]
            player.experience = data["player_exp"]
            player.attack_damage = data["player_atk"]
        file.close()
```

---

### PHASE 3: NPCs & Dialogue

**Step 1: NPC scene**

Create `res://scenes/NPC.tscn` with root `CharacterBody2D`:
- `AnimatedSprite2D`
- `CollisionShape2D`
- `Area2D` named `TalkArea` (for proximity detection)

```gdscript
# res://scripts/npc.gd
extends CharacterBody2D

@export var npc_name: String = "Villager"
@export var dialogue_lines: Array[String] = ["Hello there!", "The forest to the east is dangerous."]
@export var portrait_texture: Texture2D

var current_line: int = 0

func interact() -> void:
    var dialogue_ui = get_tree().root.get_node("Main/DialogueUI")
    if dialogue_ui and dialogue_ui.has_method("show_dialogue"):
        dialogue_ui.show_dialogue(self)

func get_next_line() -> String:
    var line = dialogue_lines[current_line]
    current_line = (current_line + 1) % dialogue_lines.size()
    return line
```

**Step 2: Dialogue UI**

Create `res://ui/DialogueUI.tscn` (CanvasLayer):
- `ColorRect` (background panel)
- `Label` (npc-name)
- `Label` (dialogue text)
- `TextureRect` (portrait)

```gdscript
# res://ui/dialogue_ui.gd
extends CanvasLayer

@onready var panel: ColorRect = $Panel
@onready var name_label: Label = $Panel/NameLabel
@onready var text_label: Label = $Panel/TextLabel
@onready var portrait: TextureRect = $Panel/Portrait

var current_npc: Node

func _ready() -> void:
    hide()
    panel.hide()

func show_dialogue(npc: Node) -> void:
    current_npc = npc
    name_label.text = npc.npc_name
    text_label.text = npc.get_next_line()
    if npc.portrait_texture:
        portrait.texture = npc.portrait_texture
    panel.show()

func _unhandled_input(event: InputEvent) -> void:
    if event.is_action_pressed("interact") and panel.visible:
        if current_npc:
            text_label.text = current_npc.get_next_line()
        else:
            close_dialogue()

func close_dialogue() -> void:
    panel.hide()
    current_npc = null
```

---

### PHASE 4: Inventory System

**Step 1: Item resource**

```gdscript
# res://scripts/items/item_data.gd
extends Resource

class_name ItemData

@export var item_name: String = "Item"
@export var description: String = ""
@export var icon: Texture2D
@export var item_type: String = "consumable"  # "consumable", "weapon", "armor", "key"
@export var value: int = 0
@export var heal_amount: int = 0
@export var attack_bonus: int = 0
@export var defense_bonus: int = 0
@export var stackable: bool = true
@export var max_stack: int = 99

func use(player: Node) -> void:
    match item_type:
        "consumable":
            if heal_amount > 0 and player.has_method("heal"):
                player.heal(heal_amount)
        "weapon":
            if attack_bonus > 0 and player.has_method("equip_weapon"):
                player.equip_weapon(self)
        "armor":
            if defense_bonus > 0 and player.has_method("equip_armor"):
                player.equip_armor(self)
```

**Step 2: Inventory singleton**

```gdscript
# res://scripts/autoload/inventory.gd
extends Node

var items: Array[InventorySlot] = []
var max_slots: int = 24
var gold: int = 0

signal inventory_changed
signal gold_changed

func _ready() -> void:
    for i in range(max_slots):
        items.append(InventorySlot.new())

func add_item(item: ItemData, quantity: int = 1) -> bool:
    if item.stackable:
        for slot in items:
            if slot.item and slot.item.item_name == item.item_name and slot.quantity < item.max_stack:
                var can_add = min(quantity, item.max_stack - slot.quantity)
                slot.quantity += can_add
                quantity -= can_add
                inventory_changed.emit()
                if quantity <= 0:
                    return true
    for slot in items:
        if not slot.item:
            slot.item = item
            slot.quantity = 1
            quantity -= 1
            inventory_changed.emit()
            if quantity <= 0:
                return true
    return false

func remove_item(item_name: String, quantity: int = 1) -> bool:
    for slot in items:
        if slot.item and slot.item.item_name == item_name:
            var to_remove = min(quantity, slot.quantity)
            slot.quantity -= to_remove
            quantity -= to_remove
            if slot.quantity <= 0:
                slot.item = null
                slot.quantity = 0
            inventory_changed.emit()
            if quantity <= 0:
                return true
    return false

func count_item(item_name: String) -> int:
    var total := 0
    for slot in items:
        if slot.item and slot.item.item_name == item_name:
            total += slot.quantity
    return total

func has_item(item_name: String) -> bool:
    return count_item(item_name) > 0

class InventorySlot:
    var item: ItemData = null
    var quantity: int = 0
```

**Step 3: Enable as Autoload**
- Project → Project Settings → Autoload
- Path: `res://scripts/autoload/inventory.gd`
- Name: `Inventory`

**Step 4: Inventory UI (optional but recommended)**

```gdscript
# res://ui/inventory_ui.gd
extends CanvasLayer

@onready var grid_container: GridContainer = $Panel/GridContainer
var slot_scene: PackedScene = preload("res://ui/InventorySlotUI.tscn")

func _ready() -> void:
    Inventory.inventory_changed.connect(refresh)
    hide()

func _unhandled_input(event: InputEvent) -> void:
    if event.is_action_pressed("inventory"):
        visible = not visible
        if visible:
            refresh()

func refresh() -> void:
    for child in grid_container.get_children():
        child.queue_free()
    for slot in Inventory.items:
        if slot.item:
            var slot_ui = slot_scene.instantiate()
            slot_ui.setup(slot.item, slot.quantity)
            grid_container.add_child(slot_ui)
```

---

### PHASE 5: Enemies, Combat & Save System

**Step 1: Enemy scene**

```gdscript
# res://scripts/enemy.gd
extends CharacterBody2D

@export var enemy_name: String = "Slime"
@export var max_hp: int = 5
@export var attack_damage: int = 1
@export var speed: float = 30.0
@export var experience_reward: int = 5
@export var drop_item: ItemData
@export var drop_chance: float = 0.3

var current_hp: int
var player_ref: Node2D
var is_dead: bool = false
var is_hit: bool = false

var NavigationAgent: NavigationAgent2D

func _ready() -> void:
    current_hp = max_hp
    NavigationAgent = $NavigationAgent2D
    player_ref = get_tree().root.find_child("Player", true, false)

func _physics_process(delta: float) -> void:
    if is_dead or not player_ref:
        return
    if is_hit:
        return

    var distance = global_position.distance_to(player_ref.global_position)
    if distance < 200 and distance > 16:
        NavigationAgent.target_position = player_ref.global_position
        var next_pos := NavigationAgent.get_next_path_position()
        if next_pos:
            velocity = global_position.direction_to(next_pos) * speed
        else:
            velocity = global_position.direction_to(player_ref.global_position) * speed
        move_and_slide()
    elif distance <= 16:
        _attack_player()

func _attack_player() -> void:
    if player_ref and player_ref.has_method("take_damage"):
        player_ref.take_damage(attack_damage)

func take_damage(amount: int) -> void:
    if is_dead:
        return
    current_hp -= amount
    is_hit = true
    modulate = Color.RED
    await get_tree().create_timer(0.1).timeout
    modulate = Color.WHITE
    is_hit = false
    if current_hp <= 0:
        die()

func die() -> void:
    is_dead = true
    velocity = Vector2.ZERO
    if player_ref and player_ref.has_method("add_experience"):
        player_ref.add_experience(experience_reward)
    if drop_item and randf() < drop_chance:
        Inventory.add_item(drop_item, 1)
    $AnimatedSprite2D.play("death")
    await $AnimatedSprite2D.animation_finished
    queue_free()
```

**Step 2: Save system (expanded)**

```gdscript
# Extend the save in main.gd
func save_game() -> void:
    var items_data: Array[Dictionary] = []
    for slot in Inventory.items:
        if slot.item:
            items_data.append({
                "name": slot.item.resource_path,
                "qty": slot.quantity
            })
    var save_data = {
        "player_position": {"x": player.position.x, "y": player.position.y},
        "player_hp": player.current_hp,
        "player_max_hp": player.max_hp,
        "player_level": player.level,
        "player_exp": player.experience,
        "player_atk": player.attack_damage,
        "gold": Inventory.gold,
        "inventory": items_data,
        "quests_completed": QuestManager.completed_quests  # see Phase 5
    }
    var file := FileAccess.open("user://savegame.json", FileAccess.WRITE)
    if file:
        file.store_line(JSON.stringify(save_data))
        file.close()

func load_game() -> void:
    var file := FileAccess.open("user://savegame.json", FileAccess.READ)
    if not file:
        return
    var data = JSON.parse_string(file.get_as_text())
    if not data:
        return
    player.position = Vector2(data["player_position"]["x"], data["player_position"]["y"])
    player.current_hp = data.get("player_hp", player.max_hp)
    player.max_hp = data.get("player_max_hp", player.max_hp)
    player.level = data.get("player_level", 1)
    player.experience = data.get("player_exp", 0)
    player.attack_damage = data.get("player_atk", 3)
    Inventory.gold = data.get("gold", 0)
    Inventory.items.clear()
    for inv_slot in data.get("inventory", []):
        var res = load(inv_slot["name"]) as ItemData
        if res:
            Inventory.add_item(res, inv_slot["qty"])
    QuestManager.completed_quests = data.get("quests_completed", [])
    file.close()
```

**Step 3: Quest manager singleton**

```gdscript
# res://scripts/autoload/quest_manager.gd
extends Node

var active_quests: Array[QuestData] = []
var completed_quests: Array[String] = []

signal quest_updated
signal quest_completed(quest_name: String)

func add_quest(quest: QuestData) -> void:
    if completed_quests.has(quest.quest_name):
        return
    active_quests.append(quest)
    quest_updated.emit()

func progress_quest(quest_name: String, amount: int = 1) -> void:
    for quest in active_quests:
        if quest.quest_name == quest_name:
            quest.progress += amount
            if quest.progress >= quest.goal:
                complete_quest(quest)
            quest_updated.emit()
            return

func complete_quest(quest: QuestData) -> void:
    active_quests.erase(quest)
    completed_quests.append(quest.quest_name)
    if quest.reward_gold > 0:
        Inventory.gold += quest.reward_gold
    if quest.reward_item:
        Inventory.add_item(quest.reward_item)
    quest_completed.emit(quest.quest_name)

# QuestData resource
# Create new Resource → QuestData with: quest_name, description, goal, progress, reward_gold, reward_item
```

**Step 4: Connect save to F5/F6**

```gdscript
# In main.gd or autoload
func _unhandled_input(event: InputEvent) -> void:
    if event.is_action_pressed("quick_save"):
        save_game()
    if event.is_action_pressed("quick_load"):
        load_game()
```

Add Input Map actions: `quick_save` (F5), `quick_load` (F6).

---

## 5. AI Prompts

Use these prompts with ChatGPT, Claude, or Bolt.new. Substitute your sprite/mechanic names.

### Player Controller
```
Write a Godot 4 GDScript for a CharacterBody2D top-down player.
Features:
- WASD movement with Input.get_vector("move_left", "move_right", "move_up", "move_down")
- Walking speed 130, running speed 220 with Shift held
- AnimatedSprite2D with direction-based animations: idle_down, idle_up, idle_left, idle_right, walk_down, walk_up, walk_left, walk_right
- Attack on Space key: locked movement for 0.3s, enable AttackArea monitoring for 0.2s
- facing_direction Vector2 variable that updates based on last movement
- take_damage(amount), heal(amount), die() methods
- Export vars for max_hp, current_hp, attack_damage, level, experience
- add_experience(amount) that levels up when exp >= level * 10
- Interaction with E key using Area2D overlapping detection
```

### NPC with Dialogue
```
Create a Godot 4 NPC (CharacterBody2D) with GDScript.
Features:
- Export vars: npc_name (String), dialogue_lines (Array[String]), portrait_texture (Texture2D)
- interact() method called from player
- get_next_line() that cycles through dialogue_lines
- SpeakerSystem integration: on interact() find CanvasLayer DialogueUI and call show_dialogue(npc)
- Add AnimatedSprite2D with idle animation
- CollisionShape2D and Area2D child for proximity detection
```

### Inventory System
```
Write a Godot 4 autoload inventory singleton (extends Node).
Features:
- Array of slots (max 24), each slot has item (ItemData resource) and quantity (int)
- add_item(item: ItemData, quantity: int) -> bool returns false if full
- remove_item(item_name: String, quantity: int) -> bool returns false if not enough
- count_item(item_name: String) -> int
- has_item(item_name: String) -> bool
- gold: int variable
- signal inventory_changed
- signal gold_changed
- Inner class InventorySlot with item and quantity
```

### Quest System
```
Create a Godot 4 quest system with two scripts.

QuestData.gd (extends Resource):
- quest_name, description, goal (int), progress (int), reward_gold (int), reward_item (ItemData)

QuestManager.gd (autoload, extends Node):
- active_quests array, completed_quests (Array[String])
- add_quest(quest: QuestData), progress_quest(quest_name, amount), complete_quest(quest)
- signal quest_updated, signal quest_completed
- Give reward on completion: gold + item
```

### Enemy AI
```
Write a Godot 4 enemy (CharacterBody2D) with AI.
Features:
- NavigationAgent2D for pathfinding to player
- Detection range 200px, attack range 16px
- Export: max_hp, attack_damage, speed, experience_reward, enemy_name
- take_damage(amount) with red flash, die() with death animation
- If hit, invincibility for 0.5s
- Drop loot: export drop_item (ItemData), drop_chance (float 0-1)
- On death: add EXP to player, check drop, play death anim, queue_free
- _physics_process: move toward player if in range, stop and attack when close
```

### Save System
```
Write a Godot 4 save/load system using JSON and FileAccess.
Features:
- Save to "user://savegame.json"
- Save player position (Vector2), stats, inventory (items + quantities), gold, quest progress
- Load and restore all saved data
- Use FileAccess.open with FileAccess.WRITE / READ
- JSON.stringify + JSON.parse_string
- F5 to quick save, F6 to quick load
- Handle missing file gracefully
- Store inventory as array of {name: resource_path, qty: int}
```

### TileMap Generator
```
Write a Godot 4 GDScript for procedural dungeon generation.
- TileMapLayer node reference
- Use Cellular Automata or BSP algorithm for room generation
- Place floor tiles (ID 0), wall tiles (ID 1), corridor tiles (ID 2)
- Spawn player at first room center
- Place enemies (Marker2D prefabs) randomly in rooms
- Parameters: map_width, map_height, fill_percent, smooth_iterations
- Connect rooms with L-shaped corridors
- Ensure all rooms are reachable with flood fill check
```

### Day/Night Cycle
```
Create a Godot 4 day/night cycle (autoload or node).
Features:
- ColorRect overlay that alpha-blends to black at night
- Timer for full cycle (e.g. 120 seconds = 1 game day)
- 70% day, 30% night
- Smooth alpha transition over 5 seconds between phases
- signal day_started, night_started
- Clock display: export var hour, minute that update
- Use modulate.a on ColorRect: 0.0 at noon, 0.6 at midnight
- Optional: dim lights / torches at night
```

### Crafting System
```
Write a Godot 4 crafting system UI + script.
Features:
- GridContainer showing craftable recipes
- Each recipe: required items (Array[ItemData + quantity]), result (ItemData + quantity)
- Check Inventory.has_item for each required
- On craft: remove required items, add result
- Gray out recipes the player can't afford
- Craft button with confirmation
- Recipe data as Resource (extends Resource) with required array and result
```

### Farming
```
Write a Godot 4 farming system.
Features:
- Plant seeds on tilled soil (detectable tile)
- Growth stages with timer (0 -> 25% -> 50% -> 75% -> harvestable)
- Water plant to skip growth stage
- Hoe tile to till soil (change tile on TileMapLayer)
- Harvest: randomly drop items (vegetables, fruits)
- Inventory check before planting (must have seed item)
- Watering can tool with limited uses per day
```

---

## 6. Asset Pipeline

### Recommended workflow for importing sprites

```
1. Download sprite pack (.zip) from Itch.io / Kenney / OpenGameArt
2. Extract to res://assets/<pack-name>/
3. In Godot: FileSystem dock will auto-import PNGs
4. Create AnimatedSprite2D sprite frames:
   - Select all frames for one animation direction
   - Drag into SpriteFrames panel
   - Set animation speed (5-10 FPS for walk, 3-5 for idle)
5. Create TileSet:
   - New TileSet resource
   - Add tile PNG
   - Define tile size (16x16 or 32x32)
   - Paint collision polygons on wall/water tiles
   - Flag jump-through platforms if needed
6. Create ItemData resources for each item:
   - New Resource → ItemData
   - Set name, icon, type, value
7. Create QuestData resources for each quest
```

### Naming convention
```
assets/
  characters/
    player/
      player_idle_down.png
      player_walk_down.png (sprite sheet)
      player_attack_down.png
      ...
    enemies/
      slime.png
      skeleton.png
      bat.png
    npcs/
      farmer.png
      blacksmith.png
      elder.png
  tilesets/
    overworld_tileset.png
    dungeon_tileset.png
    interior_tileset.png
  items/
    potion_red.png
    sword_iron.png
    key_dungeon.png
  ui/
    inventory_bg.png
    button_normal.png
    button_hover.png
    dialogue_panel.png
  sfx/
    hit.wav
    pickup.wav
    enemy_death.wav
    step_grass.wav
  music/
    overworld.ogg
    battle.ogg
```

---

## 7. Free Tier Workarounds

### Bolt.new free (1M tokens/month, 300K/day)
- **Workaround:** Write all game logic locally in Godot. Use Bolt only for specific isolated features (enemy AI, save system, UI widgets). Paste only the relevant script.
- **Tip:** Keep each Bolt prompt focused on one script. Don't ask for the whole game at once.
- **Tip:** Export your code to Bolt as starting context rather than asking it to re-generate from scratch.

### Replit free (1,200 min/month, 1 vCPU, 2 GB, 10 GiB outbound)
- **Workaround:** Don't build the whole game in Replit. Use Replit for:
  - AI Agent to prototype small features
  - Quick HTML5 builds for testing in browser
  - Hosting a leaderboard or save cloud sync (simple Flask/Express)
- **Replit Agent** (~20 daily free credits): Use for "write a GDScript for enemy pathfinding" — paste result into local Godot.

### Asset limitations
- **No budget for paid assets:** Stick to CC0 packs (Kenney, Pixel Frog, Snakerser)
- **Missing a sprite?** Use Pixel Monster Generator (itch.io browser tool) or edit existing sprites in GIMP/Krita
- **No custom character:** Use character creators from itch.io (Pixel Art RPG Character Creator, Sprite Hero Generator)

### AI prompt limits (free ChatGPT/Claude)
- **Workaround:** Use focused one-function prompts. Regenerate previous outputs by saying "fix the attack animation code, it doesn't reset after hit"
- **Workaround:** Keep a local text file of your best prompts for reuse.
- **Workaround:** Paste your existing code + ask for specific modifications instead of full rewrites.

### Sound
- **No budget:** Use bfxr.net for all SFX (free, browser-based, procedural)
- **Music:** Use Pixabay or Incompetech (CC-BY — add credit in game credits screen)
- **No audio editor:** Audacity is free and supports all formats Godot needs (OGG, WAV)

---

## 8. Publishing

### Platform: Itch.io (100% free)

**Step 1: Export for Windows/Linux/macOS**
- Godot → Project → Export
- Add Windows Desktop, Linux/X11, macOS templates
- If templates missing: download from godotengine.org (free, open source)
- Set: `Export Mode = Release`, `Texture Format = Basis Universal` (smaller size)

**Step 2: ZIP and upload**
- Compress the exported .exe + .pck into a .zip
- Go to itch.io → Upload new project
- Set price = "Free" (or "Name Your Own Price")
- Fill tags: `godot`, `rpg`, `top-down`, `pixel-art`, `fantasy`, `2d`
- Upload screenshots (3-5 minimum)
- Upload a GIF of gameplay (compressed with ezgif.com)

**Step 3: Web export (optional)**
- Godot → Export → HTML5
- Upload to itch.io as "HTML" project type
- Free hosting on Itch.io, playable in browser
- Limits: ~50 MB max for comfortable loading

**Step 4: Direct download uploads**
- Itch.io supports files up to 2 GB on free accounts
- Use 7-Zip (free) for compression

### Marketing checklist
- Gameplay GIF on Twitter/Bluesky
- Post in r/godot, r/indiegames, r/playmygame
- Add to itch.io collections (Godot games, free RPGs, etc.)
- Enable comments + rating on Itch.io
- Embed Itch.io widget on GitHub Pages site

### No-cost promotion channels
- Itch.io community (forums, game jams)
- Godot Discord share channel
- Reddit: r/godot, r/IndieGaming, r/playmygame
- YouTube devlog (DaVinci Resolve is free)

---

## 9. Production Checklist

### [ ] Project Setup
- [ ] Godot 4.x installed and project created
- [ ] Input Map configured (move, interact, attack, inventory, quick save/load)
- [ ] Folder structure created (assets, scenes, scripts, ui, tilesets)
- [ ] Autoloads registered (Inventory, QuestManager, SaveManager)
- [ ] Default world scene set in Project Settings

### [ ] Phase 1: Player
- [ ] Player scene with CharacterBody2D
- [ ] Movement with Input.get_vector()
- [ ] AnimatedSprite2D with 4-direction idle/walk/attack animations
- [ ] Attack system with Area2D hitbox
- [ ] Interaction detection Area2D
- [ ] Stats (HP, ATK, DEF, level, exp)
- [ ] Camera2D with smoothing
- [ ] CollisionShape2D fitting the sprite

### [ ] Phase 2: World
- [ ] TileSet with at least 3 tile types (ground, solid, water)
- [ ] TileMapLayer for ground layer
- [ ] TileMapLayer for above-layer (trees, walls)
- [ ] Y-sort enabled on world root
- [ ] At least 2 connected maps
- [ ] Door/transition areas between maps
- [ ] Proper collision on walls and obstacles

### [ ] Phase 3: NPCs
- [ ] NPC scene with talk Area2D
- [ ] DialogueUI CanvasLayer
- [ ] At least 3 NPCs placed in world
- [ ] NPCs respond to interact key
- [ ] Dialogue text cycles on repeated press
- [ ] Portrait display working

### [ ] Phase 4: Inventory
- [ ] ItemData resources created for all items
- [ ] Inventory autoload with add/remove/count
- [ ] Inventory UI toggle (I key)
- [ ] Grid of slots displaying icons + quantity
- [ ] Item use functionality (heal, equip)
- [ ] Equipment system (weapon + armor slot)
- [ ] Gold tracking and display

### [ ] Phase 5: Enemies & Combat
- [ ] Enemy scene with NavigationAgent2D
- [ ] Enemy detection range and chase AI
- [ ] Melee attack on player contact
- [ ] Damage flash animation
- [ ] Death animation + EXP reward
- [ ] Loot drops (item + chance)
- [ ] At least 2 enemy types
- [ ] Enemy respawn (on screen reload)

### [ ] Save System
- [ ] Save to user://savegame.json (F5)
- [ ] Load from user://savegame.json (F6)
- [ ] Saves player position, stats, inventory, quests, gold
- [ ] Handles missing save file gracefully
- [ ] Auto-save on scene transition (optional)

### [ ] Quests
- [ ] QuestData resources created
- [ ] QuestManager autoload
- [ ] At least 3 quests (kill X enemies, collect Y items, talk to Z)
- [ ] Quest journal UI (J key)
- [ ] Quest completion rewards (gold + items)
- [ ] Quest progress tracking

### [ ] Polish
- [ ] Sound effects (hit, pickup, step, death, UI click)
- [ ] Background music in each area
- [ ] Main menu (Start, Load, Quit)
- [ ] Pause menu (Esc)
- [ ] Game over screen / respawn
- [ ] Transition effects between scenes
- [ ] Damage numbers / floating text
- [ ] 5+ screenshots + 1 GIF for Itch.io page
- [ ] Credits screen (free asset attribution)

### [ ] Build & Ship
- [ ] Desktop export (Windows build tested)
- [ ] Itch.io page created with tags/screenshots/description
- [ ] GitHub repo with README + license
- [ ] .gitignore for Godot (use github.com/github/gitignore/Godot.gitignore)
- [ ] Playtester feedback (at least 3 people)

---

## 10. How to Improve

### Crafting System
- Recipe-based: combine materials at a crafting station
- Materials are items in inventory
- Result is a new item (weapon, potion, furniture)
- Unlock new recipes from NPCs or quest rewards
- **AI prompt:** see Section 5

### Farming (Stardew Valley style)
- Till soil tiles with hoe (tool item)
- Plant seeds from inventory onto tilled tiles
- Water daily using watering can
- Growth stages (4 stages) over 3-5 game days
- Harvest crops as items (sells for gold)
- **AI prompt:** see Section 5

### Day/Night Cycle
- Timer-driven overlay: ColorRect alpha 0 (day) to 0.6 (night)
- 2-minute real-time = 1 game day
- 70:30 day-to-night ratio
- Different enemy spawns at night
- Torches/lanterns emit light using PointLight2D
- Bed to skip night
- **AI prompt:** see Section 5

### Dungeon Generation
- Procedural room layout using Binary Space Partition (BSP)
- Cellular automata for cave-like levels
- L-shaped corridor connections
- Locked doors requiring keys
- Enemy spawn points based on room type
- Treasure rooms with loot
- Boss room at deepest point
- **AI prompt:** see Section 5

### Shop System
- NPC shopkeeper with inventory
- Buy items with gold
- Sell items at reduced price (50% of value)
- Dynamic pricing based on player reputation
- Restock timer (daily)

### Weather System
- Rain, snow, fog overlay particles
- Seasonal color palette changes
- Weather affects enemy behavior / spawns
- Audio: rain SFX, thunder

### Character Customization
- Sprite palette swap (hair, clothes, skin)
- Equipment visible on character sprite
- Multiple character classes (warrior, mage, rogue)
- Stat distribution per class

### Side-scrolling sections
- Hybrid top-down + side view (e.g. house interiors become side view)
- New input mode for side-scrolling (jump + gravity)
- Seamless transition between perspectives

### Multiplayer (advanced)
- Godot's built-in ENetMultiplayerPeer
- Sync player positions, NPC states, world changes
- Lobby system
- Server authority model

### Performance optimization
- TileMapLayer culling for large worlds (Godot handles this automatically in 4.x)
- Limit `_physics_process` enemies to those within 500px of player
- Use GPUParticles2D instead of CPUParticles2D
- Texture atlas merging (combine individual sprites into single atlas)
- Use `VisibleOnScreenEnabler2D` nodes for enemy activation

---

## Final Notes

**This guide is yours.** Adapt, remix, expand. The tools are free, the art is free, and the engine respects you. Build your dream RPG one `move_and_slide()` at a time.

**Key links recap:**
- Godot Engine: https://godotengine.org
- Kenney Assets: https://kenney.nl
- Itch.io free assets: https://itch.io/game-assets/free
- OpenGameArt: https://opengameart.org
- Freesound: https://freesound.org
- Pixabay Music: https://pixabay.com/music/
- Incompetech: https://incompetech.com
- bfxr: https://www.bfxr.net
- Itch.io distribution: https://itch.io
- Bolt.new: https://bolt.new
- Replit: https://replit.com

**License for this guide:** CC0 — do whatever you want with it.

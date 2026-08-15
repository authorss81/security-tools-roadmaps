# Replit (2026) — Complete Free Tier Analysis

## Starter (Free) Plan — What You Get

### AI Agent Credits
- **Daily Agent credits** — limited daily amount, resets every day, capped at a monthly max
- **Lite build only** — fast, lightweight models for small edits/bug fixes. **No Full build** (needs Core at $20/mo)
- Effort-based pricing: simple requests cost less, complex builds cost more
- Agent chat is billed per interaction (even text-only responses cost credits)

### Cloud Credits (Monthly)
- Monthly credits for: databases (production), object storage, publishing (autoscale/static)
- Resets each month. Running out = services may stop until next cycle or you buy packs

### Published Apps
- **1 free published app** — auto-taken down after **30 days**
- **"Made with Replit" badge** is mandatory (cannot remove without Core at $20/mo)
- Badge includes your referral link — get referral credits when people sign up through it

### Storage
- **2 GB per workspace** (hard limit)

### Compute
- **CPU/RAM** determined by plan (Starter gets lowest tier)
- **20 concurrent Replit Apps** max (hard limit)
- Network bandwidth: soft limit, plan-determined

### What's BLOCKED on Free (Must upgrade to Core $20/mo)
| Feature | Free (Starter) | Core ($20/mo) |
|---------|---------------|---------------|
| Full build (autonomous agent) | ❌ | ✅ |
| Convert Design Canvas to artifact | ❌ | ✅ |
| All artifact types (slides, video, etc.) | ❌ | ✅ |
| Plan Mode (plan before building) | ❌ | ✅ |
| Third-party connectors (Stripe, Google, etc.) | ❌ | ✅ |
| Replit AI Integrations | ❌ | ✅ |
| Remove "Made with Replit" badge | ❌ | ✅ |
| Additional published apps | 1 (30-day) | Unlimited |
| Active background tasks | — | 1 |
| Collaboration seats | — | 5 |
| Turbo mode (2.5x faster) | ❌ | ❌ (Pro only) |

## What Replit is BEST At

1. **Rapid prototyping from a single prompt** — Describe an app in plain English, Agent builds it end-to-end. Best for: landing pages, CRUD apps, dashboards, mobile apps, booking systems, slide decks, videos.

2. **Full-stack web apps** — Built-in PostgreSQL database, auth, and hosting. Deploy with one click. No DevOps.

3. **Web-based development** — Zero setup. No local installs. Works on any computer with a browser. Great for: beginners, teams who want instant collaboration, rapid iteration.

4. **Importing existing projects** — From GitHub, Figma, Vercel, Bolt, Lovable, or ZIP. Continue building with Agent.

5. **Mobile apps** — Build mobile apps without Xcode or Android Studio (though not as deep as native tools).

## What Replit is TERRIBLE At (for games)

1. **Godot/Unity/Unreal engine games** — Replit is for **web apps**, not game engines. You cannot run Godot, Unity, or Unreal on Replit.
2. **Desktop games** — Can't export .exe/.app files for Steam distribution.
3. **Low-level/graphics-heavy games** — No WebGL/WebGPU support for complex 2D rendering. No shader support.
4. **Real-time multiplayer** — Possible but latency is poor. Not built for game server hosting.
5. **Large sprite/asset storage** — 2GB limit per workspace. Large game assets will fill it fast.
6. **Offline/local development** — Everything is online. No internet = no work.
7. **Long development sessions** — Free tier has compute limits. Idle sessions time out.

## Where Replit CAN Work for Games (limited scope)

- **HTML5/Canvas/Phaser.js games** — 2D browser games rendered in Canvas/WebGL. Works if you keep scope small.
- **Puzzle games, card games, simple platformers** — Anything that runs in a browser with JavaScript/TypeScript.
- **Game prototypes/demos** — Quick proof-of-concept before moving to Godot.
- **Web-based game websites** — Scoreboards, level editors, community portals for your Godot game.

## Recommended Free Tier Game Development Stack

### For actual 2D games (NOT text): Use **Godot 4** locally
- Godot is 100% free (MIT license), no royalties, no revenue share
- Export to Windows, Mac, Linux, Web, Android, iOS
- Download at https://godotengine.org/download

### AI Tools to pair with Godot:
| Tool | Free Limit | How to Use |
|------|-----------|------------|
| **Claude (claude.ai)** | ~5-20 msgs/day free | Generate GDScript files, player controllers, enemy AI |
| **Cursor** | 2000 completions/mo, 50 premium requests | AI-powered IDE for writing Godot code |
| **ChatGPT** | GPT-4o mini unlimited, GPT-4o limited | Debugging, code generation, asset prompt ideas |
| **Leonardo AI** | 150 tokens/day | Generate sprite sheets, character art, backgrounds |
| **Seele AI** | Unlimited free | Generate pixel art sprites |
| **Stable Diffusion (local)** | Completely free via Fooocus/ComfyUI | Unlimited AI art generation (needs GPU) |
| **MusicGen / Stable Audio** | Free tiers | Generate background music, SFX |
| **jsfxr / sfxr** | Free | Generate retro sound effects |
| **Trello / Notion** | Free | Track game dev tasks |

### Replit's Role in Game Dev (free)
- **Skip it for actual game development** — wrong tool for the job
- **Use it for**: Game website/landing page, leaderboard backend, community forums, asset management dashboard

## Bottom Line

**Replit free tier is excellent for:**
- Web app prototypes, landing pages, SaaS MVPs, dashboards, mobile apps
- Learning to code, quick experiments, hackathons
- Full-stack apps with database + auth + hosting

**Replit free tier is NOT suitable for:**
- Godot/Unity game development
- Desktop or console games
- Graphics-heavy or real-time games
- Large projects (2GB storage limit, no background tasks, 30-day app expiry)

**For game development, use: Godot (engine) + Claude/Cursor (AI code) + Leonardo/Seele (AI art) + sfxr (sounds) — all free, all local/offline.**
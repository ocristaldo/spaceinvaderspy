# Space Invaders Py – Release Notes (Draft)

## v1.0.0 – HUD & Palette Refresh (Target: December 2025)

### ✨ Highlights
- **Cabinet HUD** – Replaced text HUD with sprite-authentic digits, the `HI-SCORE` marquee, and a dedicated bottom band for credits + cannon icons.
- **Lives Panel** – Spare cannons now render in the bottom-left corner and update automatically when extra lives are awarded.
- **Credit Divider** – Horizontal line separates gameplay from the credit/lives panel, matching the reference cabinet screenshots.
- **Sprite Tint System** – `src/ui/color_scheme.py` centralizes palette tweaks; toggling "Sprite tint" in Options recolors aliens, bunkers, player, UFO, bombs, and FX without touching the background.
- **Explosions Everywhere** – Both explosion frames run whenever aliens, UFOs, or the player are destroyed; UFO bomb drops got their own sprite.
- **Sprite Utilization** – `text_hi_score`, `text_credit`, digit sprites, and all validated atlas entries (except the intentionally unused `bomb_3`) now appear in-game.
- **Documentation Refresh** – Cleaned up old guides, updated the configuration reference, roadmap, and per-sprite usage table, and introduced this release notes draft.
- **Credit & Audio Flow** – Insert coins with `C`, spends a credit when starting, and manage independent Sound FX / Music toggles (both off by default).

### 🧩 Compatibility & Settings
- All toggles persist in `settings.json`: `audio_enabled`, `intro_demo_enabled`, `debug_sprite_borders`, and the new `tint_enabled`.  
- Colors and tints live in `src/ui/color_scheme.py`; edit the palette and flip the sprite-tint option to preview changes instantly.

### 📋 Remaining Launch Tasks
- Credit/coin insertion flow that gates gameplay.  
- Attract-mode polish so the demo reuses the new HUD.  
- Alternating 2-player scaffold.  
- Cross-platform smoke tests + README screenshots.

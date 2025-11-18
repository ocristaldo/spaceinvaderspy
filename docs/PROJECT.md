# 🚀 Space Invaders Py – Launch Prep Hub

**Last Updated:** November 28, 2025  
**Version Target:** 1.0.0 (First public release)  
**Status:** 🔄 Final polish & release readiness in progress

---

## 🎯 Current Focus – "Cabinet HUD & Polish" Sprint

We just landed the biggest visual refresh since the project started:

- ✅ Cabinet-style HUD with sprite digits, `HI-SCORE` marquee, and a credit/lives bar separated by a divider line.
- ✅ Lives are now represented by cannon sprites (auto-updated when extra lives are awarded).
- ✅ UFOs have their own bomb sprite; aliens only use the classic projectile.
- ✅ Sprite tinting pipeline with per-object colors (`src/ui/color_scheme.py`) and a toggle surfaced in Options.
- ✅ Explosion FX wired to the new `explosion`/`explosion_alt` sprites so kills feel alive.

The remaining work for 1.0.0 is tracked below.

---

## 📌 Release Checklist

| Area | Owner | Status | Notes |
|------|-------|--------|-------|
| Credits / coin flow scaffold | gameplay | ✅ Done | `C` inserts a credit, Start consumes it, HUD shows remaining credits. |
| Attract-loop polish | gameplay | ⏳ Pending | Reuse the refreshed HUD during demos + cycle through score table/credit prompts. |
| 2-player alternating shell | systems | ⏳ Pending | Store per-player score/lives, swap turns on death. |
| Extra assets hook-up | art/code | ✅ Done | `text_hi_score`, `text_credit`, digits, and dual explosion frames are now in use. |
| Tint toggle persistence | settings | ✅ Done | Stored in `settings.json` (`tint_enabled`). |
| Release notes & documentation | docs | 🔄 Drafting now | See `docs/RELEASE_NOTES.md`. |
| Packaging & test sweep | build | ⏳ Pending | Smoke-test on Windows/macOS/Linux, update README instructions. |

---

## 🧭 What's Next (By Priority)

1. **Attract Mode Touch-ups**  
   - Swap the font-driven score advance table with sprite digits for consistency.  
   - Add "PRESS START" pulses reusing the HUD color palette.  
   - Ensure idle return logic uses the refreshed layout.

2. **Alternating Two-Player Stub**  
   - Maintain two score slots and switch `current_player` when a life is lost.  
   - Share the alien wave but keep per-player lives/score.

3. **Test & Release Infrastructure**  
   - Update `docs/STATUS.md` with the final test plan (smoke checklist + automated suite).  
   - Capture reference screenshots for README/release notes.  
   - Prepare tagged release + binary instructions.

---

## 🛠️ Working Agreements

- **Code style** – Keep modules small, favor helper classes over monolith functions, and add logging where state changes.  
- **Sprites first** – When adding new art, update the atlas (`assets/images/SpaceInvaders.arcade.json`), the mapping in `src/utils/sprite_sheet.py`, and the documentation table.  
- **Configuration clarity** – Any new toggle lives either in `settings.json` (persisted) or `src/ui/color_scheme.py` (palette). Update `docs/CONFIGURATION.md` when knobs change.

---

## 🤝 Contributing

1. **Play:** `python -m src.main`
2. **Tweak settings:** edit `settings.json` (or use Options → sprite tint/audio/demo).
3. **Change colors:** edit `src/ui/color_scheme.py` and use the tint toggle to preview.
4. **Run tests:** `python3 -m pytest tests/unit/test_layout_visuals.py`
5. **Document:** Touch the relevant section in `docs/` so others know what changed.

---

## 📄 Reference Docs

- [`docs/STATUS.md`](STATUS.md) – quick health snapshot & blocking tasks.  
- [`docs/ROADMAP.md`](ROADMAP.md) – high-level milestones through GA.  
- [`docs/RELEASE_NOTES.md`](RELEASE_NOTES.md) – draft release notes for v1.0.0.  
- [`docs/SPRITES.md`](SPRITES.md) – authoritative sprite usage + validation list.  
- [`docs/CONFIGURATION.md`](CONFIGURATION.md) – where to change fonts, colors, toggles.

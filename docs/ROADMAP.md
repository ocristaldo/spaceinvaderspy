# 🗺️ Roadmap – Path to v1.0.0

> **Reference docs:** [PROJECT.md](PROJECT.md) (management hub), [STATUS.md](STATUS.md) (live progress), [RELEASE_NOTES.md](RELEASE_NOTES.md) (public summary)

---

## 🎬 Phase NOW – Launch Prep (Dec 2025)
**Goal:** Ship a faithful, single-player cabinet experience with the refreshed HUD/tint system.

| Epic | Tasks | Exit Criteria |
|------|-------|---------------|
| ✅ Credit / Start Flow | Complete | MENU shows `CREDIT 00`, `C` inserts coins, Start consumes one per game. |
| Attract Loop Upgrade | - Reuse HUD overlays in demos<br>- Cycle score table, instructions, and staged gameplay clips<br>- Respect tint toggle & divider line | Idle mode mirrors cabinet presentation; any key exits to MENU. |
| Alternating 2P Scaffold | - Maintain per-player score/lives<br>- Swap control after death<br>- Display both scores at top HUD | Two players can alternate turns using the same wave; HUD reflects current player. |
| Release Packaging | - Smoke-test on Win/macOS/Linux<br>- Capture screenshots/gifs<br>- Finalize README & RELEASE_NOTES | Releasable build + documentation bundle posted on GitHub. |

---

## 🔭 Phase NEXT – Post-Launch Enhancements
1. **Authentic attract scripting** – Insert coin prompt animations, cycling score advance table, and demo AI refinements.  
2. **Gameplay modifiers** – Accessibility toggles (multi-shot, slow mode, endless mode).  
3. **2P competitive mode** – Track alternating runs in the high score table.  
4. **Online release package** – Itch.io page or similar distribution with binaries + instructions.  
5. **Stretch Goals** – Challenge stages, tractor beam enemy variants, deluxe sprite packs.

---

## ✅ Recently Delivered
- Cabinet-aligned HUD with sprite digits, credit/lives panel, and divider line.  
- Optional sprite tinting plus palette configuration (`src/ui/color_scheme.py`).  
- Explosion FX and bomb variants wired to the atlas.  
- Credit/coin flow implemented (`C` inserts, Start consumes, HUD counter updates live).  
- `docs/SPRITES.md` annotated with usage + validation state for every sprite.

---

## 🧾 Tracking & Issues
- **GitHub Issues:** use labels `launch-blocker`, `enhancement`, `docs`.  
- **Kanban:** simple columns on the project board (Backlog → In Progress → Review → Done).  
- **Owner cadence:** at least one touch per day on blockers; daily stand-up note in project discussions when travelling/offline.

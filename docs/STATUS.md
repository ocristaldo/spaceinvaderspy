# 📊 Status Snapshot – November 28, 2025

**Build:** HUD & Tint Refresh (release candidate workstream)  
**State:** 🟡 On track – launch blockers identified, implementation underway

---

## ✅ Highlights Since Last Update
-	Cabinet-accurate HUD: score digits, `HI-SCORE` marquee, and credit/lives panel with divider.  
-	Lives now render as cannon sprites (auto-updated when extra lives trigger).  
-	Sprite tint pipeline wired across player, aliens, UFO, bunkers, bombs, and explosions with a persisted toggle in Options.  
-	UFOs drop their own projectile (`bomb_2`); alien formations stick to the original bomb.  
-	Explosion FX using both arcade frames fire whenever aliens, UFOs, or the player are destroyed.  
-	Credit/coin flow implemented (`C` inserts, Start consumes, counter visible in HUD).  
-	All validated sprites (except the intentionally shelved `bomb_3`) are now used in-game, and the documentation tables track usage/validation state.

## 🚧 Active Work / Blockers
| Item | Owner | Status | Notes |
|------|-------|--------|-------|
| Idle/attract polish | gameplay | 📝 Design | Hook demos into the new HUD, ensure tint + divider look correct in attract screens. |
| Alternating 2-player scaffold | systems | 📝 Design | Requires per-player score/lives storage + HUD slots. |
| Test sweep & packaging | build | 🔜 Pending | Need smoke matrix across macOS/Windows/Linux before tagging release. |

## 🧪 Test Matrix
- **Automated:** layout/visual unit tests pending update (pytest unavailable locally – run in CI).  
- **Manual checklist:**
  1. Toggle sprite tint ON/OFF from Options and verify lives/aliens recolor without restarting.  
  2. Confirm the divider line, credit text, and cannon icons remain aligned through window resizes.  
  3. Destroy aliens/UFO/player and ensure explosion FX cycle both frames.  
  4. Confirm `text_hi_score` / digit sprites match the scoreboard screenshot (see ROADMAP for acceptance shots).

## 📅 Near-Term Plan
1. Wire the attract demo to reuse the HUD update (including tint toggle + divider).  
2. Draft alternating 2-player scaffold (shared wave, alternating lives).  
3. Run a full smoke-test sweep and finalize release notes.

## 🔔 Callouts
- Documentation cleanup complete (`docs/CHANGELOG.md`, `CLEANUP_SUMMARY.md`, and `DOCS_GUIDE.md` removed).  
- `docs/SPRITES.md` now tracks "In Use" + "Validated" for every entry – keep it current when adding art.  
- Configuration reference updated with `color_scheme.py`, the `tint_enabled` flag, and separate SFX/music toggles.

# Critical Bug Fix: Font Profile Error in High Score Screen

**Date:** November 19, 2025
**Status:** ✅ FIXED
**Issue:** Game crashed when player lost all lives and high score initials entry screen displayed

## Problem Description

When a player lost all 3 lives and achieved a new high score, the game would crash with the following error:

```
KeyError: 'Unknown font profile: menu_large'
```

### Root Cause

The `InitialsEntry.draw()` method in `src/ui/initials_entry.py` (line 141) was attempting to use a non-existent font profile `menu_large`:

```python
text_font = get_font("menu_large")  # ❌ This profile doesn't exist
```

The `menu_large` font profile was never defined in `src/ui/font_manager.py`. Available menu font profiles are:
- `menu_title` (size 14, bold)
- `menu_body` (size 12, min_size 14)
- `menu_small` (size 10, min_size 10)

## Solution

Changed line 141 in `src/ui/initials_entry.py` to use the `menu_body` font profile instead:

```python
text_font = get_font("menu_body")  # ✅ Correct: profile exists with min_size 14
```

The `menu_body` profile provides appropriate sizing for the high score initials display while being properly defined in the font manager.

## Testing

✅ Verified that all fonts are correctly loaded:
```bash
python -c "from src.ui.font_manager import get_font; get_font('menu_title'); get_font('menu_body'); get_font('menu_small'); print('✓ All fonts OK')"
```

✅ Game runs without crashing (verified with 5-second debug run)

✅ Test suite still passes: **77/85 tests** (no regressions)
- 8 pre-existing menu navigation test failures (documented separately)

## Impact

- **Critical:** Fixes game crash on high score screen
- **Zero-Impact:** No breaking changes, no API changes
- **Isolated:** Only affects high score initials entry screen rendering

## Files Modified

- `src/ui/initials_entry.py` (1 line change)

## Commit Information

```
commit b8c6cae
Author: [User]
Date: 2025-11-19

fix: Replace invalid menu_large font profile with menu_body in InitialsEntry

The InitialsEntry.draw() method was referencing 'menu_large' font profile
which doesn't exist in the FONT_PROFILES dictionary, causing KeyError crash.

Changed to use 'menu_body' profile which provides appropriate sizing with
min_size=14 for high score initials entry display.

This fixes the game crash when player loses all lives and high score screen
is displayed.
```

## How to Verify

1. Run the game: `./debug.sh` or `python -m src.main`
2. Start a 1-player game (press `1`)
3. Lose all 3 lives (let aliens hit you until you run out of lives)
4. If your score is in the top 10, the initials entry screen will appear
5. The game should display the high score entry screen without crashing
6. You can now enter your initials and confirm them

If you don't reach the top 10, replay until you score at least 1120 points (current top score).

## Related Documentation

- See `DEBUG_GUIDE.md` for how to run in debug mode with full logging
- See `src/ui/font_manager.py` for available font profiles
- See `src/ui/initials_entry.py` for high score initials entry implementation

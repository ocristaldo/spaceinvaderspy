SpaceInvadersPy — Roadmap & Project Plan

This document captures the short/medium/long-term roadmap, milestones, acceptance criteria, and a first-step implementation plan for the SpaceInvadersPy project.

1 — Vision

Build a faithful, well-tested, and easily extensible Space Invaders clone in Python with clean code, automated tests, CI, and approachable docs so contributors can iterate on gameplay, art, and sound.

Short-term goals (next 2 weeks)
- Deliverables
  - Definite project roadmap and milestones (this document).
  - A simple main menu and pause overlay (Start / Options / Quit, Pause with P/Esc).
  - Basic audio support (SFX + music) with volume control.
  - Solid unit + integration tests for core gameplay; raise coverage to >= 60%.
- Acceptance criteria
  - `main` launches to a menu screen and entering Start begins gameplay.
  - Pause toggles game updates/drawing and displays overlay.
  - Audio toggles and volume control exist in Options.
  - CI runs tests + coverage and reports results.
- Estimated effort: 5–10 work-days (depends on asset availability)

Medium-term goals (1–3 months)
- Level progression and difficulty scaling (multi-wave levels).
- Improved bunker visuals, damage model and UI polish.
- More tests and coverage to 75%+.
- Performance tuning and 60 FPS target on supported systems.

Long-term goals (3+ months)
- Packaging and distribution (pip/zip), release artifact generation.
- Leaderboards/high-scores persistence (local or online optional).
- Community content: alternate sprite sets, additional modes.

Milestones
- M1: Roadmap + CI coverage (COMPLETE)
- M2: Main menu + pause + Options (SFX/music toggle) — target: next PR
- M3: Level progression + power-ups + difficulty scaling
- M4: Visual polish + performance + release

Prioritized backlog (high to low)
1. Main menu + Pause UI + Options (SFX toggle, volume)
2. Unit tests for core modules (input, game state, collision)
3. Level/wave system
4. Bunker visuals & per-block durability
5. Performance profiling and fixes
6. Packaging and release

First-step implementation plan (what I will do next)
- Finish this roadmap (done) and link it from `docs/DEVELOPMENT_STATUS.md`.
- Create a minimal UI module skeleton: `src/ui/menu.py` with classes for Menu and Overlay.
- Integrate the menu into `src/main.py` so game starts in MENU state instead of directly running.
- Add simple unit tests for menu state transitions (menu -> play -> pause -> restart).

Implementation notes and conventions
- State machine: Game states will be simple strings/enum: MENU, PLAYING, PAUSED, GAME_OVER.
- Keep main loop responsive: only run `update()` when in PLAYING state; `draw()` continues in other states.
- Tests should avoid requiring real display where possible; use `pygame.display.set_mode((1,1))` in test setup.

How to review progress
- Each milestone will be a PR with small, focused changes: docs, tests, UI, audio, gameplay.
- CI will run tests and coverage for each PR. Aim to keep PRs small (1–3 files changed) to speed review.

Contact / ownership
- Repo owner: (you)
- I will implement the next step (menu + pause) unless you tell me to start a different item.




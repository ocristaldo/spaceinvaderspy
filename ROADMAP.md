# 🗺️ Space Invaders Py - Vision & Roadmap

> **For detailed project status, phases, and action items, see [PROJECT.md](PROJECT.md) and [STATUS.md](STATUS.md)**

---

## 🎯 Product Vision

Build a faithful Space Invaders clone in Python that naturally evolves toward Galaga-style mechanics. The game should:

1. **Be playable today** - Core Space Invaders loop works now
2. **Add depth gradually** - Expand with Galaga features over time
3. **Stay maintainable** - Clean code, good tests, clear docs
4. **Welcome contributors** - Easy to understand and extend

---

## 📈 High-Level Phases

### Phase 1: Foundation ✅ Complete
- Core Space Invaders gameplay
- Collision detection
- Scoring and lives
- Sprite system
- CI/CD pipeline

### Phase 2: Quick Wins ✅ Complete
- Audio system (muted by default)
- High score persistence
- Extra lives milestones
- Unit tests

### Phase 3: Foundation Systems 📅 Next
- Game state machine
- Menu UI
- Pause system
- Level progression

### Phase 4: Galaga Expansion 📅 Planned
- Enemy formations (40-enemy layout)
- Challenge stages (bonus waves)
- Tractor beam capture
- Dual fighter power-up

### Phase 5: Polish & Release 📅 Final
- Performance tuning
- Comprehensive tests
- 2-player mode
- Packaging for distribution

---

## 🎮 Feature Roadmap

### Today (Phase 2)
- ✅ Classic Space Invaders gameplay
- ✅ Audio (muted by default, toggle with 'A')
- ✅ High scores saved to disk
- ✅ Extra lives at 20k + 70k points

### Soon (Phase 3)
- 📅 Game menu and attract mode
- 📅 Pause/resume functionality
- 📅 Multi-wave level progression
- 📅 Difficulty scaling

### Later (Phase 4)
- 📅 Galaga-style enemy formations
- 📅 Challenge stages with bonuses
- 📅 Boss enemies with tractor beam
- 📅 Dual ship power-up
- 📅 Enemy morphing mechanics

### Eventually (Phase 5)
- 📅 2-player alternating mode
- 📅 Leaderboard system
- 📅 Performance optimization
- 📅 Release packaging

---

## 📋 Design Principles

1. **Start Simple** - Get Space Invaders working first
2. **Expand Gradually** - Add Galaga features phase by phase
3. **Test Everything** - Aim for 70%+ code coverage
4. **Document Clearly** - Make architecture easy to follow
5. **Welcome Help** - Contribute-friendly setup and docs

---

## 🚀 How to Get Started

### To Play
```bash
python -m src.main
```

### To Contribute
1. Read [PROJECT.md](PROJECT.md) for full context
2. Check [STATUS.md](STATUS.md) for current work
3. Pick an item from Phase 3 (next phase)
4. Create a feature branch and submit a PR

### To Understand the Code
1. Read `docs/GAMEPLAY_OVERVIEW.md` - how current systems work
2. Read `docs/detailed_gameplay.md` - what Galaga features we're adding
3. Explore `src/main.py` - main game loop
4. Check tests for expected behavior

---

## 🎯 Success Criteria

Each phase is complete when:
- All features working as designed
- Tests passing (70%+ coverage by Phase 5)
- Documentation up to date
- No known bugs or performance issues

---

## 📞 Questions?

- **What should I work on?** → Check [STATUS.md](STATUS.md)
- **How does X work?** → See [PROJECT.md](PROJECT.md)
- **What's the plan?** → You're reading it
- **How do I contribute?** → [PROJECT.md Contributing section](PROJECT.md#-how-to-contribute)

---

**For detailed project management, see [PROJECT.md](PROJECT.md)**




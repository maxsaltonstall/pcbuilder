# Quick Start Guide

## Installation Issue?

Your system's security scanner is blocking npm install. Try:

```bash
# Option 1: Override environment variable
SCFW_ALLOW=true npm install

# Option 2: Use yarn
yarn install

# Option 3: Use pnpm
pnpm install
```

See `SETUP.md` for detailed troubleshooting.

## Running the App

```bash
npm run dev
```

This starts:
- Vite dev server on http://localhost:5173
- Electron desktop window

## Project Tour

### 📁 Key Directories

```
src/
├── types/           ← Start here: understand data structures
├── steps/           ← Wizard UI screens
├── context/         ← State management
└── services/        ← TODO: Core business logic goes here

data/
├── classes.json           ← 5 base classes
├── prestige-classes.json  ← 2 prestige classes
├── feats.json             ← 20 feats
└── skills.json            ← 15 skills
```

### 🎯 What to Build Next

Create these files in `src/services/`:

**1. prerequisiteValidator.ts** (easiest)
- Input: `Requirement`, `CharacterContext`
- Output: `{ valid: boolean, errors: string[] }`
- Logic: Check if requirement is met at given level

**2. skillCalculator.ts** (medium)
- Input: `LevelProgression[]`, `AbilityScores`
- Output: Total skill points available
- Logic: (base + INT) × 4 at lvl 1, (base + INT) after

**3. optimizationEngine.ts** (hardest)
- Input: Target classes, feats, skills
- Output: Ordered `LevelProgression[]`
- Logic: Greedy algorithm (see plan)

### 🔍 Type Cheat Sheet

```typescript
// Main state
CharacterState {
  totalLevel: number
  abilityScores: AbilityScores
  targetClasses: ClassSelection[]
  desiredFeats: string[]
  keySkills: string[]
  optimizedProgression: LevelProgression[]
}

// Per-level breakdown
LevelProgression {
  levelNumber: number
  class: CharacterClass
  skillPoints: number
  baseAttackBonus: number
  saves: { fortitude, reflex, will }
}

// Validation
Requirement {
  type: 'feat' | 'skill' | 'baseAttackBonus' | ...
  description: string
  validate: (context) => boolean
}
```

### 🧪 Testing Current Build

1. Start app: `npm run dev`
2. Enter level 10, concept "Archer"
3. Set ability scores
4. Select Fighter 6, Wizard 4
5. Pick archery feats
6. See wizard flow (optimization placeholder)

### 📖 Data Examples

**Adding a new class:**
```json
{
  "id": "barbarian",
  "name": "Barbarian",
  "hitDie": 12,
  "skillPointsPerLevel": 4,
  "classSkills": ["climb", "intimidate", "jump", "listen", ...],
  "baseAttackBonus": "good",
  "saves": {
    "fortitude": "good",
    "reflex": "poor",
    "will": "poor"
  }
}
```

**Adding a new feat:**
```json
{
  "id": "feat-name",
  "name": "Feat Name",
  "prerequisites": [
    {
      "type": "ability",
      "description": "Str 13",
      "ability": "str",
      "minimumScore": 13
    }
  ],
  "benefits": "What it does...",
  "type": ["General", "Fighter Bonus"]
}
```

### 🐛 Common Issues

**"Cannot find module '@/types'"**
→ Install: `npm install -D @types/node`

**Vite not starting**
→ Check port 5173 is free: `lsof -i :5173`

**Electron window blank**
→ Check dev console (auto-opens), look for errors

**TypeScript errors**
→ Run: `npm run type-check` for details

### 🎨 UI Customization

Colors defined in `src/main.tsx`:
```typescript
const theme = createTheme({
  palette: {
    primary: { main: '#8B0000' },    // Dark red
    secondary: { main: '#DAA520' },  // Gold
  }
})
```

### 📚 Documentation

- `README.md` - Project overview
- `SETUP.md` - Installation help
- `IMPLEMENTATION_SUMMARY.md` - What's built
- **This file** - Quick reference

### 🚀 Development Workflow

1. **Read types** (`src/types/`) to understand data
2. **Implement service** in `src/services/`
3. **Wire to UI** in wizard steps
4. **Test** with example characters
5. **Iterate**

### 💡 Tips

- Components are thin, services are thick
- Types are strict, use them
- Data is minimal, expand later
- Services are pure functions (testable)
- State lives in Context, not components

### 🎯 Success Criteria

When Phase 2 is done, you should be able to:
- ✅ Enter "level 10 Fighter/Wizard"
- ✅ Select "Power Attack, Cleave"
- ✅ Click "Optimize"
- ✅ See valid level-by-level progression
- ✅ All prerequisites validated
- ✅ Skill points calculated correctly

---

**Current Status**: UI works, logic needed 🛠️

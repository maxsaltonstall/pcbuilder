# Build Validation System

This directory contains benchmark builds from the D&D 3.5 optimization community used to validate the optimizer's output.

## Quick Start

### Run Validation Tests

```bash
# Run all validation tests
npm run test:validation

# Run in watch mode (re-run on changes)
npm run test:validation:watch

# Run full CI suite (type-check + lint + validation)
npm run ci
```

### Available Benchmark Builds

1. **arcane-archer-example.json** - Gish optimization (Wizard/Fighter/AA)
   - Tests: BAB/caster level balance, prestige class entry timing
   - Tier: 2

2. **codzilla-cleric.json** - Divine Metamagic optimization
   - Tests: Full caster progression, feat chain ordering
   - Tier: 1

3. **ubercharger.json** - Melee charger (Barbarian/Fighter)
   - Tests: Full BAB, HP maximization, Power Attack chain
   - Tier: 2

4. **skill-monkey-supreme.json** - Skill optimization (Factotum/Rogue)
   - Tests: Skill point maximization, level 1 Rogue start
   - Tier: 2

5. **batman-wizard.json** - Pure arcane caster
   - Tests: 9th level spells, full wizard progression
   - Tier: 1

6. **wildshape-druid.json** - Natural Spell druid
   - Tests: Natural Spell timing, full caster progression
   - Tier: 1

7. **crusader-tob.json** - Tome of Battle martial
   - Tests: Full BAB, feat selection
   - Tier: 3

8. **twf-ranger.json** - Two-Weapon Fighting ranger
   - Tests: TWF chain completion, feat progression
   - Tier: 3

## How It Works

### 1. Benchmark Build Format

Each JSON file contains:

```json
{
  "buildName": "Arcane Archer",
  "source": "GitP Character Optimization Handbook",
  "level": 20,
  "focus": "ranged",
  "abilityScores": { ... },
  "targetClasses": [ ... ],
  "expectedStats": { ... },
  "validationCriteria": {
    "mustHave": {
      "baseAttackBonus": { "min": 15, "ideal": 17 },
      "casterLevel": { "min": 16, "ideal": 18 }
    },
    "shouldHave": {
      "feats": ["Point Blank Shot", "Precise Shot"],
      "spellLevel": 8
    }
  }
}
```

### 2. Validation Tests

Tests in `src/tests/buildValidation.test.ts`:

- **Skill Point Efficiency** - Within 10% of expected
- **BAB/Caster Level** - Within ±1 of expected
- **Feat Coverage** - All critical feats present
- **Prestige Class Timing** - Entry level ±1 from optimal
- **HP Maximization** - Within range for focus

### 3. Success Criteria

A build **passes** if:
- ✅ Skill points ≥ minimum (usually 90% of ideal)
- ✅ BAB/caster level within ±1 of expected
- ✅ Critical feats included
- ✅ Prestige classes entered on time

## Adding New Benchmark Builds

### Step 1: Find a Build

**Best Sources:**
- [GitP Character Optimization Forum](https://forums.giantitp.com/)
- GitP Handbook threads (Wizard, Cleric, Gish, etc.)
- BrilliantGameologists Archive (via Wayback Machine)
- Dragon Magazine #310-359

**Quality Indicators:**
- High engagement (100+ replies)
- Detailed mechanics discussion
- Sourcebook citations
- Trade-off analysis

### Step 2: Create JSON File

```bash
# Create new build file
touch test-builds/my-new-build.json
```

Use existing builds as templates. Include:
- Build name and source URL
- Level and focus
- Ability scores
- Target classes with level distribution
- Expected stats (HP, BAB, caster level, skill points)
- Expected feats
- Validation criteria (min/ideal/max thresholds)

### Step 3: Add Test Cases

Edit `src/tests/buildValidation.test.ts`:

```typescript
describe('My New Build - Description', () => {
  test('critical feature X works', () => {
    const build = loadTestBuild('my-new-build');
    // ... test logic
  });
});
```

### Step 4: Verify

```bash
npm run test:validation
```

## Continuous Integration

### GitHub Actions

Every push to `main` or PR triggers:

1. **Type checking** - Ensure TypeScript compiles
2. **Validation tests** - Run all benchmark builds
3. **Coverage report** - Track code coverage
4. **PR comments** - Post results to pull request

### Local Pre-Commit

Add to `.git/hooks/pre-commit`:

```bash
#!/bin/sh
npm run ci
```

## Interpreting Results

### Test Output

```
 ✓ Arcane Archer - achieves expected caster level and BAB
 ✓ CoDzilla Cleric - maintains full caster progression
 ✗ Ubercharger - includes Power Attack chain feats
 ✓ Skill Monkey - maximizes total skill points
```

### Failure Analysis

When a test fails:

1. **Check the diff** - What's different?
   ```typescript
   Expected: 450 skill points
   Received: 425 skill points
   ```

2. **Identify root cause**:
   - Class ordering wrong? (Rogue should be first)
   - Feat chain broken? (Missing prerequisite)
   - Prestige class timing off? (Entered too late)

3. **Fix the algorithm** - Usually in:
   - `optimizationEngine.ts` - Class ordering
   - `skillCalculator.ts` - Skill point math
   - `featRecommendations.ts` - Feat selection
   - `prerequisiteValidator.ts` - Prerequisite checking

4. **Re-run tests** - Ensure fix doesn't break other builds

### Performance Tracking

Track optimizer quality over time:

```bash
# Current benchmark
npm run test:validation | tee validation-$(date +%Y%m%d).log

# Compare to baseline
diff validation-baseline.log validation-$(date +%Y%m%d).log
```

## Benchmark Roadmap

### Current Coverage (8 builds)
- ✅ Arcane caster (Wizard)
- ✅ Divine caster (Cleric, Druid)
- ✅ Gish (Arcane Archer)
- ✅ Melee (Ubercharger, TWF Ranger, Crusader)
- ✅ Skills (Factotum/Rogue)

### Gaps to Fill
- ⬜ Psionics (Psion, Wilder, Psychic Warrior)
- ⬜ Monk optimization
- ⬜ Necromancer (Dread Necromancer)
- ⬜ Artificer (item creation focus)
- ⬜ Beguiler/Mindbender (skill+spells)
- ⬜ Epic level builds (21-30)

### Community Contributions

Submit new builds via PR:

1. Fork the repo
2. Add benchmark build JSON to `test-builds/`
3. Add test case to `src/tests/buildValidation.test.ts`
4. Document source and rationale in PR description
5. CI will auto-validate

## Troubleshooting

### "Cannot find module @data/classes.json"

Make sure alias is configured in `vitest.config.ts`:

```typescript
resolve: {
  alias: {
    '@data': path.resolve(__dirname, './data'),
  },
}
```

### Tests hang or timeout

Increase timeout in test file:

```typescript
test('slow optimization test', async () => {
  // ...
}, 30000); // 30 second timeout
```

### Validation always fails

Check that test build expectations match reality:
- Are expected stats achievable?
- Are prerequisites actually met?
- Is the build theoretically possible?

## Resources

- [GitP Character Optimization Forum](https://forums.giantitp.com/forumdisplay.php?46-Gaming)
- [D&D 3.5 SRD](https://www.d20srd.org/)
- [Build Optimization Theory](../TESTING.md)
- [Where to Find Builds](../scripts/BUILD_SOURCES.md)

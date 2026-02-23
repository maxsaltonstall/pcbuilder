# Build Validation Strategy

## Sources for "Definitive" Optimized Builds

### Primary Sources (High Quality)

1. **Giant in the Playground (GitP) Forums**
   - URL: https://forums.giantitp.com/forumdisplay.php?46-Gaming
   - The "Handbook" threads compile best-in-class builds
   - Search for: "[Build] [optimization]" or "[Guide]"
   - Notable: "CO Handbooks" sticky thread

2. **BrilliantGameologists Archive** (if accessible)
   - Was the premier optimization forum
   - Many archived threads on Wayback Machine
   - Hosted famous builds like "Mailman" and optimization tiers

3. **Min/Max Boards**
   - Focus on mechanical optimization
   - Many prestige class chains documented
   - Good for feat progression validation

### Secondary Sources

4. **Character Optimization Wiki**
   - Community-maintained optimization guides
   - Tier rankings for classes
   - Feat chains and synergies documented

5. **D&D Wiki Character Optimization**
   - Variable quality but some excellent builds
   - Good for edge cases and unusual combinations

6. **Dragon Magazine Archives**
   - Official WotC optimized builds
   - "Class Acts" series
   - "Nodwick's Guide" optimization articles

### Benchmark Builds to Test Against

#### Tier 1 Optimized Builds

1. **"Batman Wizard" (Diviner/Incantatrix)**
   - Level 20 build
   - Focus: Spell versatility, divine oracle cheese
   - Key metrics: Spell slots, save DCs, utility coverage
   - Should achieve: 9th level spells by L17, metamagic cheese

2. **"CoDzilla" (Cleric Optimization)**
   - Level 15 Cleric with Divine Metamagic
   - Focus: Persistent spell abuse, summoning
   - Key metrics: Effective caster level, buff duration
   - Should achieve: All-day Divine Power + Righteous Might

3. **"Arcane Archer God" (Wizard/Fighter/AA)**
   - Wizard 5 / Fighter 2 / Arcane Archer 10 / Arcane Archer 3
   - Focus: Ranged attack optimization
   - Key metrics: BAB progression, caster level preservation
   - Should achieve: Full BAB, 7th level spells

#### Tier 2-3 Optimized Builds

4. **"Ubercharger" (Lion Totem Barbarian/Fighter)**
   - Focus: Pounce + shock trooper + leap attack
   - Key metrics: Damage per round, mobility
   - Should achieve: 10+ attacks on charge by L12

5. **"Melee Sorcerer" (Draconic Sorcerer/Eldritch Knight)**
   - Sorcerer 5 / Fighter 2 / Eldritch Knight 10
   - Focus: Gish optimization (melee + casting)
   - Key metrics: BAB vs caster level trade-off
   - Should achieve: 6th level spells, full BAB equivalent

6. **"Skill Monkey Supreme" (Factotum/Rogue)**
   - Focus: Maximum skill points and versatility
   - Key metrics: Total skill points, number of maxed skills
   - Should achieve: 15+ skills at max ranks by L15

## Testing Methodology

### Phase 1: Data Collection

```bash
# Create test suite directory
mkdir -p /Users/max.saltonstall/pcbuilder/test-builds/

# For each benchmark build:
# 1. Extract character sheet data
# 2. Convert to JSON test case
# 3. Document expected outputs
```

### Phase 2: Test Case Format

```typescript
// test-builds/batman-wizard.json
{
  "buildName": "Batman Wizard (Diviner 5/Incantatrix 10/Archmage 5)",
  "source": "GitP Forums - CO Handbook",
  "url": "https://forums.giantitp.com/...",
  "level": 20,
  "focus": "spells",
  "concept": "Ultimate prepared arcane caster",

  "expectedProgression": [
    { "level": 1, "class": "Wizard", "feats": ["scribe-scroll"] },
    { "level": 2, "class": "Wizard" },
    // ... full progression
  ],

  "expectedStats": {
    "totalSkillPoints": 160,  // (2+INT) * 20
    "keySkills": ["Spellcraft", "Knowledge (arcana)", "Concentration"],
    "maxRanksSkills": ["Spellcraft"],
    "casterLevel": 20,
    "spellsPerDay": {
      "9": 4  // Should have 9th level spells
    }
  },

  "expectedFeats": [
    "Spell Focus (Evocation)",
    "Greater Spell Focus (Evocation)",
    "Metamagic School Focus",
    // ... etc
  ],

  "criticalFeatures": [
    "Must enter Incantatrix by level 6",
    "Must have access to 9th level spells by 17",
    "Divination specialization for forewarned"
  ]
}
```

### Phase 3: Automated Testing

```typescript
// test/optimizationValidation.test.ts

describe('Build Optimization Validation', () => {

  test('Batman Wizard achieves expected caster level', () => {
    const testBuild = loadTestBuild('batman-wizard.json');
    const result = optimizeClassProgression(
      testBuild.level,
      testBuild.targetClasses,
      testBuild.expectedFeats,
      testBuild.keySkills
    );

    const finalCasterLevel = calculateCasterLevel(result);
    expect(finalCasterLevel).toBeGreaterThanOrEqual(testBuild.expectedStats.casterLevel);
  });

  test('Arcane Archer achieves prestige class on time', () => {
    const testBuild = loadTestBuild('arcane-archer-god.json');
    const result = optimizeClassProgression(/*...*/);

    // Should enter AA by level 8 (Wizard 5, Fighter 2, AA 1)
    const aaEntryLevel = result.findIndex(l => l.class.name === 'Arcane Archer');
    expect(aaEntryLevel).toBeLessThanOrEqual(7); // 0-indexed
  });

  test('Skill Monkey maximizes skill points', () => {
    const testBuild = loadTestBuild('skill-monkey.json');
    const result = optimizeClassProgression(/*...*/);

    const totalPoints = calculateTotalSkillPoints(result, testBuild.abilityScores);
    // Factotum + high INT should get 400+ skill points by level 15
    expect(totalPoints).toBeGreaterThanOrEqual(400);
  });
});
```

### Phase 4: Metrics for Comparison

For each test build, measure:

1. **Skill Point Optimization**
   - Total skill points: our build vs reference build
   - Number of maxed-out skills
   - Skill point efficiency (points per level)

2. **Feat Efficiency**
   - Are all feat prerequisites met?
   - Feat synergies detected
   - Feat chain completion

3. **Prestige Class Timing**
   - Entry level vs optimal entry level
   - Caster level preservation
   - BAB progression

4. **Combat Stats at Key Levels**
   - Compare at levels 5, 10, 15, 20
   - HP, AC, attack bonuses, saves
   - Spell slots and caster level

5. **Build Coherence**
   - Does progression make tactical sense?
   - Are there "dead levels" (levels that don't advance goals)?
   - Is the build achievable (prerequisites met)?

## Scoring System

```typescript
interface BuildScore {
  skillPointEfficiency: number;    // 0-100
  featSynergy: number;             // 0-100
  prestigeClassTiming: number;     // 0-100
  combatEffectiveness: number;     // 0-100
  buildCoherence: number;          // 0-100

  overallScore: number;            // weighted average

  comparisonToReference: {
    skillPoints: number;           // % difference
    feats: string[];              // missing or extra feats
    classProgression: string[];   // differences in order
  };
}
```

## Validation Workflow

1. **Collect 10-15 benchmark builds** across different tiers and focuses
2. **Convert to test cases** with expected outputs
3. **Run optimizer** on each test case
4. **Compare outputs** using scoring system
5. **Identify failures** and edge cases
6. **Iterate on algorithm** to improve scores
7. **Regression testing** - ensure fixes don't break other builds

## Success Criteria

A "good" optimizer should:
- ✅ Match or exceed reference build skill points (within 5%)
- ✅ Include all critical feats for the build's focus
- ✅ Enter prestige classes at optimal level (±1 level)
- ✅ Achieve 90%+ of reference build's combat effectiveness
- ✅ Pass prerequisite validation for all choices
- ✅ Maintain feat chain coherence (no broken chains)

## Red Flags to Watch For

- ❌ Skill points significantly lower than reference (>10% gap)
- ❌ Prestige class entry delayed by 2+ levels
- ❌ Missing critical feats for the build archetype
- ❌ Feat chains started but not completed
- ❌ Prerequisites not met for recommended feats
- ❌ Caster level loss exceeding -2 from optimal

## Future Enhancements

1. **Community Build Scraper**
   - Automatically parse builds from GitP forums
   - Build test database of 100+ optimized characters
   - Continuous validation against community standards

2. **Build Simulator**
   - Simulate combat encounters at key levels
   - Measure actual performance (damage, survivability, utility)
   - Compare optimizer output vs reference builds in practice

3. **User-Submitted Builds**
   - Allow users to submit their optimized builds
   - Crowdsource test cases
   - Build leaderboard for different archetypes

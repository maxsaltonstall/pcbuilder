# Phase 2 Implementation Plan - Core Logic

**Status**: Ready to implement
**Date**: 2026-02-22
**Estimated Time**: 8-12 hours

---

## 🎯 Goals

Implement the three core services that power the character optimization:

1. **Prerequisite Validator** - Validate feat and prestige class requirements
2. **Skill Calculator** - Calculate total skill points available
3. **Optimization Engine** - Generate optimal class progression

---

## 📋 Task Breakdown

### Task 1: Prerequisite Validator (2 hours)
**File**: `src/services/prerequisiteValidator.ts`

**Requirements:**
- Validate ability score requirements (e.g., Str 13)
- Validate skill rank requirements (e.g., 8 ranks in Disable Device)
- Validate feat prerequisites (e.g., must have Power Attack)
- Validate base attack bonus requirements (e.g., BAB +6)
- Validate caster level requirements (e.g., cast 3rd level spells)
- Validate class level requirements (e.g., Fighter 4)

**Functions to implement:**
```typescript
validatePrerequisites(
  requirement: Requirement,
  context: RequirementContext,
  atLevel: number
): ValidationResult

validateAllPrerequisites(
  requirements: Requirement[],
  context: RequirementContext,
  atLevel: number
): ValidationResult

canTakeFeat(
  featId: string,
  character: CharacterState,
  atLevel: number
): ValidationResult

canEnterPrestigeClass(
  classId: string,
  character: CharacterState,
  atLevel: number
): ValidationResult
```

**Test Cases:**
- Power Attack requires Str 13 ✓
- Cleave requires Str 13 + Power Attack ✓
- Arcane Archer requires BAB+6, Point Blank, Precise, Weapon Focus, 1st level spells ✓
- Eldritch Knight requires 3rd level arcane spells ✓

---

### Task 2: Skill Calculator (2 hours)
**File**: `src/services/skillCalculator.ts`

**Requirements:**
- Calculate skill points at 1st level: (base + INT mod) × 4
- Calculate skill points at levels 2+: (base + INT mod)
- Track ability score increases at 4, 8, 12, 16, 20
- Handle negative INT modifiers (minimum 1 point)
- Track class skills vs cross-class skills
- Calculate max ranks per skill

**Functions to implement:**
```typescript
calculateSkillPointsForLevel(
  level: number,
  classData: CharacterClass,
  intelligenceModifier: number
): number

calculateTotalSkillPoints(
  progression: LevelProgression[],
  abilityScores: AbilityScores
): number

getMaxRanks(
  skillId: string,
  characterLevel: number,
  isClassSkill: boolean
): number

canAssignSkillRanks(
  skillId: string,
  ranks: number,
  characterLevel: number,
  isClassSkill: boolean
): boolean
```

**Key Rules:**
- 1st level: multiply by 4
- Minimum 1 skill point per level even with negative INT
- Class skill max ranks = level + 3
- Cross-class max ranks = (level + 3) / 2
- First rank in class skill = +3 bonus

**Test Cases:**
- Wizard 1 (INT 18) = (2 + 4) × 4 = 24 points ✓
- Rogue 1 (INT 14) = (8 + 2) × 4 = 40 points ✓
- Fighter 2 (INT 10) = 2 + 0 = 2 points ✓
- Rogue 1 → Fighter 1 vs Fighter 1 → Rogue 1 difference ✓

---

### Task 3: Optimization Engine (4-6 hours)
**File**: `src/services/optimizationEngine.ts`

**Requirements:**
- Order class levels to maximize skill points
- Ensure prestige class prerequisites met before entry
- Ensure feat prerequisites met before selection
- Assign feats at correct levels (1, 3, 6, 9, 12, 15, 18)
- Handle fighter bonus feats (1, 2, 4, 6, 8, ...)
- Track ability score increases
- Generate complete level-by-level progression

**Algorithm (Greedy Approach):**
```
1. Build feat dependency graph
   - Map each desired feat to its prerequisites
   - Determine earliest level each feat can be taken

2. Calculate prestige class entry points
   - For each prestige class target:
     - Check skill rank requirements
     - Check feat requirements
     - Check BAB requirements
     - Determine minimum entry level

3. Order base class levels for skill optimization
   - Sort classes by skill points per level (descending)
   - Front-load high-skill classes
   - Consider INT bonuses from ability increases

4. Insert prestige class levels
   - Place at earliest legal entry point
   - Respect level count targets

5. Assign feats
   - Place prerequisite feats before dependent feats
   - Use fighter bonus feats when available
   - Optimize for user's desired feat list

6. Generate progression
   - For each level 1-20:
     - Assign class
     - Calculate skill points
     - Calculate BAB
     - Calculate saves
     - Assign feats (if applicable)
     - Track ability increases
```

**Functions to implement:**
```typescript
optimizeClassProgression(
  totalLevel: number,
  targetClasses: ClassSelection[],
  desiredFeats: string[],
  keySkills: string[],
  abilityScores: AbilityScores
): LevelProgression[]

buildFeatDependencyGraph(
  desiredFeats: string[]
): Map<string, string[]>

calculatePrestigeEntryLevel(
  prestigeClass: PrestigeClass,
  baseClasses: ClassSelection[],
  desiredFeats: string[]
): number

orderClassesForSkillOptimization(
  classes: ClassSelection[],
  abilityScores: AbilityScores
): ClassSelection[]

assignFeatsToLevels(
  progression: LevelProgression[],
  desiredFeats: string[],
  featGraph: Map<string, string[]>
): LevelProgression[]
```

**Test Cases:**
- Level 10: Fighter 10 (simple single class) ✓
- Level 10: Rogue 5 / Fighter 5 (optimize order) ✓
- Level 15: Fighter 6 / Wizard 3 / Eldritch Knight 6 (prestige entry) ✓
- Level 15: Ranger 6 / Arcane Archer 9 (feat chain + entry) ✓

---

### Task 4: Wire to UI (1 hour)
**File**: `src/steps/OptimizationResults.tsx`

**Requirements:**
- Call optimization engine with character state
- Display loading state while computing
- Show level-by-level progression table
- Display warnings/errors if prerequisites not met
- Allow user to accept or modify progression
- Save to character state on accept

**UI Components:**
```typescript
- ProgressionTable
  - Shows levels 1-20
  - Class at each level
  - Feats gained
  - Skill points available
  - BAB/Saves progression

- ValidationMessages
  - Errors (red): Missing prerequisites
  - Warnings (yellow): Suboptimal choices
  - Info (blue): Suggestions

- ActionButtons
  - Accept Progression
  - Modify Goals (go back)
  - Regenerate (recompute)
```

---

## 🧪 Testing Strategy

### Unit Tests
Create `src/services/__tests__/`:
- `prerequisiteValidator.test.ts`
- `skillCalculator.test.ts`
- `optimizationEngine.test.ts`

### Integration Tests
Test complete flows:
1. Simple single-class character
2. Multiclass character (2 classes)
3. Prestige class entry (3+ classes)
4. Complex feat chains
5. Edge cases (low INT, high level)

### Manual Testing
Real D&D builds to validate:
1. **Arcane Archer** (Ranger/Wizard/AA)
2. **Arcane Trickster** (Rogue/Wizard/AT)
3. **Mystic Theurge** (Cleric/Wizard/MT)
4. **Power Attack Fighter** (feat chain)
5. **Skill Monkey Rogue** (maximize skills)

---

## 📊 Success Criteria

### Minimum Viable Product (MVP)
- [ ] Validates feat prerequisites correctly
- [ ] Validates prestige class requirements correctly
- [ ] Calculates skill points correctly
- [ ] Generates valid class progression
- [ ] Shows progression in UI
- [ ] Handles at least 3 common builds correctly

### Full Success
- [ ] Optimizes skill point allocation
- [ ] Places prestige classes at optimal entry level
- [ ] Assigns feats in correct order
- [ ] Handles all 11 base classes
- [ ] Handles 2 prestige classes
- [ ] UI shows clear progression and validation

---

## 🚀 Implementation Order

**Day 1 (4-6 hours):**
1. ✅ Prerequisite Validator (2 hours)
   - Start with simple ability/skill checks
   - Add feat dependency validation
   - Test with existing feats

2. ✅ Skill Calculator (2 hours)
   - Implement core calculation
   - Add max ranks validation
   - Test with different INT scores

**Day 2 (4-6 hours):**
3. ✅ Optimization Engine - Part 1 (3 hours)
   - Implement greedy class ordering
   - Add prestige entry calculation
   - Test with simple builds

4. ✅ Optimization Engine - Part 2 (2 hours)
   - Add feat assignment
   - Complete progression generation
   - Test with complex builds

5. ✅ UI Integration (1 hour)
   - Wire services to OptimizationResults
   - Display progression table
   - Add validation messages

**Day 3 (2-4 hours):**
6. Testing & Refinement
   - Test real D&D builds
   - Fix edge cases
   - Polish UI

---

## 🎓 Key Algorithms

### Skill Point Optimization
```
Problem: Order N classes to maximize total skill points

Insight: High-skill classes early = more total points
         (because of ×4 multiplier at 1st level)

Solution: Sort classes by (skillPoints + INTmod) descending
          Take highest skill-point class first
```

### Prestige Entry Timing
```
Problem: When can character first enter prestige class?

Constraints:
- BAB requirement (need X base class levels)
- Skill requirements (need Y ranks)
- Feat requirements (need Z feats)

Solution: Max of all constraint minimums
          Entry level = max(BAB level, skill level, feat level)
```

### Feat Dependency Resolution
```
Problem: Order feats to satisfy prerequisites

Example: Whirlwind Attack → Spring Attack → Mobility → Dodge

Solution: Topological sort of dependency graph
          Assign feats in sorted order at available levels
```

---

## 💡 Optimization Opportunities (Future)

### Phase 2 (Current)
- Greedy algorithm
- Simple ordering heuristics
- Linear time complexity

### Phase 3 (Future Enhancements)
- Dynamic programming for optimal solution
- Consider multiple feat paths
- Optimize for combat effectiveness (not just skills)
- A* search for complex builds
- User preferences weighting

### Phase 4 (Advanced)
- Machine learning to suggest builds
- Community builds database
- Build comparison tools
- Min-max optimization modes

---

## 📝 Notes

### Design Decisions
- **Start simple**: Greedy algorithm first, optimize later
- **Type safety**: Leverage TypeScript for correctness
- **Pure functions**: Services are stateless for testability
- **Incremental**: Each service works independently

### Edge Cases to Handle
- Negative INT modifier (minimum 1 skill point)
- Prestige class unattainable (missing prerequisites)
- Desired feats impossible (not enough feat slots)
- Class level distribution exceeds total level
- Circular feat dependencies (shouldn't happen in D&D)

### Performance Considerations
- Max 20 levels = limited search space
- Pre-compute feat graphs
- Cache skill calculations
- Memoize prestige entry levels

---

## ✅ Definition of Done

For each service:
- [ ] Implementation complete
- [ ] Type-safe (no `any` types)
- [ ] Basic tests passing
- [ ] Integrated with UI
- [ ] Documented with JSDoc comments
- [ ] Handles edge cases
- [ ] Works with real D&D builds

For Phase 2 overall:
- [ ] All three services implemented
- [ ] UI shows optimization results
- [ ] Can create at least 3 complete builds
- [ ] Validation catches common errors
- [ ] Ready for Phase 3 (character generation)

---

**Let's build this! 🎲⚔️🔮**

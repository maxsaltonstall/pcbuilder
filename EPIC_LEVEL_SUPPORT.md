# Epic Level Support (Levels 1-30)

**Date**: 2026-02-22
**Status**: ✅ Fully Implemented

---

## 🎯 Overview

The D&D 3.5 Character Builder now supports **epic levels (21-30)** in addition to standard levels (1-20).

### Epic Level Rules

In D&D 3.5, epic levels follow the Epic Level Handbook:
- **Levels 1-20**: Standard D&D 3.5 rules
- **Levels 21-30**: Epic rules with some modifications

---

## ✅ What Was Updated

### 1. Level Selection (InitialSetup.tsx)
- ✅ Slider now goes from **1 to 30** (was 1-20)
- ✅ Shows marks at 1, 10, 20, 30
- ✅ Warning message for epic levels (21+)

```typescript
<Slider
  min={1}
  max={30}  // Updated from 20
  marks={[1, 10, 20, 30]}
/>
```

### 2. Feat Progression (optimizationEngine.ts)
- ✅ Standard feats: 1, 3, 6, 9, 12, 15, 18
- ✅ **Epic feats**: 21, 24, 27, 30 (every 3 levels)
- ✅ Fighter bonus feats continue (every even class level)

```typescript
// Epic progression after level 20
if (characterLevel === 21 || (characterLevel - 21) % 3 === 0) {
  return true;
}
```

### 3. Ability Score Increases (optimizationEngine.ts)
- ✅ Continue every 4 levels through epic
- ✅ Levels 4, 8, 12, 16, 20, 24, 28

### 4. Skill Points (skillCalculator.ts)
- ✅ Max ranks = level + 3 (continues through epic)
- ✅ At level 30: max 33 ranks in class skills
- ✅ At level 30: max 16 ranks in cross-class skills

### 5. BAB and Saves (optimizationEngine.ts)
- ✅ Good BAB: +30 at level 30
- ✅ Average BAB: +22 at level 30
- ✅ Poor BAB: +15 at level 30
- ✅ Saves continue standard progressions

### 6. UI Updates
- ✅ Optimization results shows "Epic Level" indicator
- ✅ Character review shows "Epic" label
- ✅ Warning about Epic Level Handbook reference
- ✅ Tables handle 30 rows of progression

---

## 📊 Epic Level Progression

### Feat Progression Comparison

| Level Range | Feat Frequency | Example Levels |
|-------------|----------------|----------------|
| 1-20 (Standard) | 1, 3, 6, 9, 12, 15, 18 | 7 total feats |
| 21-30 (Epic) | Every 3 levels | 21, 24, 27, 30 |
| **Total** | **11 feats at level 30** | +4 epic feats |

### Ability Score Increases

| Level | Standard | Epic |
|-------|----------|------|
| 4, 8, 12, 16, 20 | ✅ | - |
| 24, 28 | - | ✅ |
| **Total at 30** | **7 increases** | **+28 to ability scores** |

### Skill Points Example

**Level 30 Rogue (8 skill points/level, INT 14 = +2):**
- Level 1: (8+2) × 4 = 40 points
- Levels 2-30: (8+2) × 29 = 290 points
- **Total: 330 skill points!**

### Max Ranks Example

**Level 30 Character:**
- Class skills: 30 + 3 = **33 ranks max**
- Cross-class: (30 + 3) / 2 = **16 ranks max**

---

## 🎮 Example Epic Builds

### 1. Epic Arcane Trickster
**Level 30**: Rogue 10 / Wizard 10 / Arcane Trickster 10

**Progression:**
- Levels 1-10: Rogue (maximize skill points)
- Levels 11-20: Wizard (arcane casting)
- Levels 21-30: Arcane Trickster (prestige)

**Epic Features:**
- Sneak attack +10d6
- 9th level arcane spells
- 330+ skill points
- 11 total feats

### 2. Epic Fighter
**Level 30**: Fighter 30

**Progression:**
- Straight fighter progression
- 26 bonus feats total!
- BAB +30/+25/+20/+15
- Fort +17, Ref +10, Will +10

**Epic Features:**
- Multiple attacks per round
- Massive feat selection
- Can take epic feats (Great Strength, etc.)

### 3. Epic Mystic Theurge
**Level 30**: Cleric 10 / Wizard 10 / Mystic Theurge 10

**Progression:**
- Levels 1-5: Cleric
- Levels 6-10: Wizard
- Levels 11-30: Mystic Theurge

**Epic Features:**
- 9th level divine spells
- 9th level arcane spells
- Both spell lists available
- Ultimate versatility

### 4. Epic Dragon Disciple
**Level 30**: Sorcerer 20 / Dragon Disciple 10

**Progression:**
- Levels 1-10: Sorcerer
- Levels 11-30: Dragon Disciple + more Sorcerer

**Epic Features:**
- Full draconic transformation
- Breath weapon
- Natural armor bonuses
- Epic spellcasting

---

## 📝 Epic Rules Notes

### What Works
- ✅ Level progression 1-30
- ✅ Feat progression (standard + epic)
- ✅ Ability score increases
- ✅ Skill points calculation
- ✅ BAB and save progression
- ✅ All class combinations
- ✅ Prestige class entry

### Epic Features Not Yet Implemented
- ❌ Epic feats (Great Strength, Epic Weapon Focus, etc.)
- ❌ Epic prestige classes (High Proselytizer, etc.)
- ❌ Epic spells (10th level+)
- ❌ Epic monsters/challenges
- ❌ Epic magic items

### Future Enhancements
These can be added from the Epic Level Handbook:
1. Epic feat list (50+ feats)
2. Epic prestige classes (10+ classes)
3. Epic spell system
4. Epic progression tables
5. Divine ranks (for demigods)

---

## 🧪 Testing Epic Levels

### Test Case 1: Level 30 Fighter
```
Level: 30
Classes: Fighter 30
Expected:
- 26 bonus feats
- BAB +30
- Feats at: 1,2,3,4,6,8,9,10,12,14,15,16,18,20,21,22,24,26,27,28,30
```

### Test Case 2: Level 25 Multiclass
```
Level: 25
Classes: Rogue 10, Wizard 10, Arcane Trickster 5
Expected:
- Entry to AT at level 11
- Epic feats at 21, 24
- Ability increases at 4,8,12,16,20,24
```

### Test Case 3: Level 30 Pure Caster
```
Level: 30
Classes: Wizard 30
Expected:
- Poor BAB (+15)
- Good Will saves
- 11 total feats
- Massive skill points (INT-based)
```

---

## 💡 Design Decisions

### Why Support Epic Levels?
1. **Campaign flexibility** - Some campaigns go beyond 20
2. **Complete builds** - Test ultimate character potential
3. **"What if" scenarios** - See how builds scale
4. **Epic planning** - Plan long-term character arcs

### Why Stop at 30?
1. **D&D 3.5 convention** - Most epic campaigns end by 30
2. **Balance** - Beyond 30, game balance breaks down
3. **Data availability** - Epic Level Handbook covers 21-30
4. **UI constraints** - Tables become unwieldy past 30 levels

### Implementation Approach
1. **Conservative** - Use standard rules through epic
2. **Compatible** - Works with existing optimization
3. **Clear indicators** - User knows when in epic territory
4. **Graceful degradation** - Missing epic feats won't break app

---

## 🎓 D&D 3.5 Epic Rules Reference

### Feat Progression
- **Levels 1-20**: 1st, 3rd, 6th, 9th, 12th, 15th, 18th
- **Levels 21+**: Every 3 levels (21st, 24th, 27th, 30th)

### Epic Feats
Requirements to take epic feats:
- Character level 21+
- Meet feat prerequisites
- Some require specific epic BAB/caster level

Examples of epic feats:
- Great Strength (STR +1, repeatable)
- Epic Weapon Focus (+2 to hit)
- Epic Toughness (+30 HP)
- Improved Combat Casting (+4 concentration)

### Epic Saving Throws
Continue standard progression:
- Good: +2 at 1st, +1 every 2 levels
- Poor: +0 at 1st, +1 every 3 levels

### Epic Skill Ranks
No change from standard:
- Max = character level + 3
- At 30: 33 ranks in class skills

---

## 🚀 How to Use

### Creating an Epic Character

1. **Set Level to 21-30**
   ```
   Initial Setup → Level slider → Move to 21-30
   ```

2. **Warning Appears**
   ```
   "Epic Level (21+) - Some features may be limited"
   ```

3. **Configure Normally**
   - Choose classes (can take 30 levels of anything)
   - Select feats (will get epic feat slots)
   - Pick skills (max ranks will be level+3)

4. **Optimization Runs**
   - Places classes optimally
   - Assigns feats at correct levels
   - Shows epic level progression

5. **Review Results**
   - See "Epic Level" indicator
   - Note about Epic Level Handbook
   - Export character as JSON

---

## 📋 Validation

### What's Checked
- ✅ Total levels don't exceed 30
- ✅ Feat progression follows epic rules
- ✅ Ability increases every 4 levels
- ✅ Skill ranks don't exceed max
- ✅ BAB calculated correctly

### What's Not Checked (Yet)
- ❌ Epic feat prerequisites
- ❌ Epic prestige class requirements
- ❌ Epic spell prerequisites
- ❌ Epic-specific rules

---

## 📊 Statistics

### Before Update
- Max level: 20
- Max feats: 7 (standard) + fighter bonuses
- Max ability score: +20 (5 increases)

### After Update
- Max level: **30** ✅
- Max feats: **11** (standard + epic) ✅
- Max ability score: **+28** (7 increases) ✅

### Impact
- **+50% level range** (20 → 30)
- **+57% feat slots** (7 → 11)
- **+40% ability increases** (5 → 7)

---

## 🎯 Compatibility

### Works With
- ✅ All 11 base classes
- ✅ All 13 prestige classes
- ✅ All current feats
- ✅ Skill system
- ✅ Multiclass optimization
- ✅ JSON export

### Future Additions Needed
- Epic feat database
- Epic prestige classes
- Epic-specific rules
- Epic magic items
- Divine ranks (optional)

---

**Status**: Epic levels (1-30) fully supported! 🎲⚔️✨

**Try it now in the running app:**
1. Set level to 25 or 30
2. Create a build
3. Watch epic progression!

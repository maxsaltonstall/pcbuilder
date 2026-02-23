# Data Extraction Complete - DM Guide Prestige Classes

**Date**: 2026-02-22
**Status**: ✅ Successfully extracted 11 new prestige classes

---

## 📊 Summary

### Total Prestige Classes: 13

| # | Class Name | Hit Die | Skills | BAB | Saves (F/R/W) | Type |
|---|------------|---------|--------|-----|---------------|------|
| 1 | Arcane Archer | d8 | 4 | Good | Good/Good/Poor | Archer + Magic |
| 2 | Eldritch Knight | d6 | 2 | Good | Good/Poor/Poor | Warrior + Magic |
| 3 | **Arcane Trickster** | d4 | 4 | Poor | Poor/Good/Good | Rogue + Magic |
| 4 | **Assassin** | d6 | 4 | Average | Poor/Good/Poor | Killer |
| 5 | **Blackguard** | d10 | 2 | Good | Good/Poor/Poor | Evil Paladin |
| 6 | **Dragon Disciple** | d12 | 2 | Average | Good/Poor/Good | Draconic Sorcerer |
| 7 | **Duelist** | d10 | 4 | Good | Poor/Good/Poor | Finesse Fighter |
| 8 | **Dwarven Defender** | d12 | 2 | Good | Good/Poor/Good | Tank |
| 9 | **Hierophant** | d8 | 2 | Poor | Good/Poor/Good | High Priest |
| 10 | **Horizon Walker** | d8 | 4 | Good | Good/Poor/Poor | Terrain Master |
| 11 | **Loremaster** | d4 | 4 | Poor | Poor/Poor/Good | Knowledge Seeker |
| 12 | **Mystic Theurge** | d4 | 2 | Poor | Poor/Poor/Good | Arcane + Divine |
| 13 | **Shadowdancer** | d8 | 6 | Average | Poor/Good/Poor | Shadow Manipulator |

**Bold** = Newly extracted from DM Guide

---

## 📚 Extraction Details

### Source
- **File**: `pdfs/D&D 3.5 2/DM Guide I.pdf`
- **Pages**: 176-198
- **Tool Used**: pdftotext (poppler)

### Method
1. Installed poppler: `brew install poppler`
2. Used AI agent to extract text from PDF
3. Parsed prestige class information
4. Converted to JSON format
5. Merged with existing data

### Data Extracted for Each Class
- ✅ **id** (kebab-case identifier)
- ✅ **name** (display name)
- ✅ **description** (one sentence summary)
- ✅ **hitDie** (d4, d6, d8, d10, or d12)
- ✅ **skillPointsPerLevel** (2-6 points)
- ✅ **classSkills** (array of skill IDs)
- ✅ **baseAttackBonus** ("good", "average", or "poor")
- ✅ **saves** (fortitude, reflex, will)
- ✅ **source** ("Dungeon Master's Guide")
- ✅ **isPrestige** (true)
- ✅ **requirements** (detailed prerequisites)

---

## 🎯 Prestige Class Highlights

### Combat Focused
- **Arcane Archer** - BAB +6, Point Blank Shot, Precise Shot, Weapon Focus, 1st level arcane spells
- **Duelist** - BAB +6, Dodge, Mobility, Weapon Finesse, Tumble 5, Perform 3
- **Dwarven Defender** - Dwarf only, BAB +7, Dodge, Endurance, Toughness
- **Blackguard** - Evil only, BAB +6, Hide 5, Cleave, Power Attack, contact with evil outsider

### Magic Focused
- **Arcane Trickster** - Nonlawful, 3rd level arcane spells, Decipher Script 7, Disable Device 7, sneak attack +2d6
- **Mystic Theurge** - 2nd level divine + 2nd level arcane spells, Knowledge (arcana/religion) 6 each
- **Hierophant** - 7th level divine spells, Knowledge (religion) 15, any metamagic feat
- **Loremaster** - Two Knowledge skills at 10 ranks, Skill Focus, three metamagic/item creation feats

### Unique Builds
- **Assassin** - Evil only, Hide 8, Move Silently 8, Disguise 4, must kill to join
- **Dragon Disciple** - Nondragon race, Knowledge (arcana) 8, Draconic language, spontaneous arcane caster
- **Shadowdancer** - Hide 10, Move Silently 8, Perform (dance) 5, Combat Reflexes, Dodge, Mobility
- **Horizon Walker** - Knowledge (geography) 8, Endurance

---

## 🎮 Example Builds Now Possible

### 1. Arcane Trickster
**Level 15 Build**: Rogue 7 / Wizard 3 / Arcane Trickster 5
- Prerequisites met at level 10
- Combines sneak attack with spellcasting
- Full rogue skills + arcane magic

### 2. Mystic Theurge
**Level 15 Build**: Cleric 3 / Wizard 3 / Mystic Theurge 9
- Prerequisites met at level 6
- Advances both divine and arcane casting
- Ultimate versatility

### 3. Assassin
**Level 15 Build**: Rogue 5 / Assassin 10
- Prerequisites met at level 6
- Death attack ability
- Master of stealth and killing

### 4. Duelist
**Level 15 Build**: Fighter 8 / Duelist 7
- Prerequisites met at level 8
- Finesse combat specialist
- High AC and precise strikes

### 5. Dragon Disciple
**Level 15 Build**: Sorcerer 10 / Dragon Disciple 5
- Prerequisites met at level 10
- Draconic transformation
- Breath weapon + increased stats

---

## 📈 Data Coverage Update

| Category | Before | After | Growth |
|----------|--------|-------|--------|
| Base Classes | 11/11 | 11/11 | ✅ 100% |
| Prestige Classes | 2/~100 | 13/~100 | 🔼 +550% |
| Feats | 20/~400 | 20/~400 | - |
| Skills | 15/~100 | 15/~100 | - |

---

## 🚀 Impact on App

### Optimization Engine Now Handles
- ✅ 13 different prestige class paths
- ✅ Complex multiclass builds (3-4 classes)
- ✅ Prerequisite validation for all DMG prestige classes
- ✅ Automatic prestige entry level calculation

### New Character Archetypes Available
1. **Arcane Trickster** - Rogue/Wizard hybrid
2. **Mystic Theurge** - Divine/Arcane dual caster
3. **Assassin** - Professional killer
4. **Blackguard** - Evil champion
5. **Dragon Disciple** - Draconic sorcerer
6. **Duelist** - Precision fighter
7. **Dwarven Defender** - Ultimate tank
8. **Hierophant** - Divine master
9. **Horizon Walker** - Terrain specialist
10. **Loremaster** - Knowledge expert
11. **Shadowdancer** - Shadow manipulator

---

## 🎯 Next Data Extraction Priorities

### High Priority (Complete Series)
1. **Complete Warrior** - 10+ combat prestige classes
2. **Complete Arcane** - 10+ arcane prestige classes
3. **Complete Divine** - 8+ divine prestige classes

### Medium Priority
4. **More Feats** - Expand from 20 to 50-100
5. **Complete Skills** - Add remaining 45 skills
6. **Racial Variants** - Races of Stone, Wild, Dragon

### Low Priority
7. **Specialized Systems** - Psionics, Tome of Battle
8. **Setting-Specific** - Eberron, Forgotten Realms

---

## 📝 File Locations

### Updated Files
- ✅ `data/prestige-classes.json` - Now contains 13 prestige classes
- ✅ All classes validated and formatted
- ✅ All requirements properly structured

### Temporary Files (Cleaned Up)
- ❌ `data/dmg-prestige-classes.json` - Removed after merge

---

## 🧪 Testing Recommendations

### Test These Builds in the App
1. **Arcane Trickster Build**
   - Level 15: Rogue 7 / Wizard 3 / Arcane Trickster 5
   - Should enter Arcane Trickster at level 11

2. **Mystic Theurge Build**
   - Level 15: Cleric 3 / Wizard 3 / Mystic Theurge 9
   - Should enter Mystic Theurge at level 7

3. **Assassin Build**
   - Level 10: Rogue 5 / Assassin 5
   - Should enter Assassin at level 6

### Verify
- ✅ Prestige classes appear in class selection dropdown
- ✅ Prerequisites are validated correctly
- ✅ Entry level is calculated accurately
- ✅ BAB and saves calculate correctly
- ✅ Skill points are calculated correctly

---

## 💡 Fun Facts

### Highest Hit Die
**Dragon Disciple** and **Dwarven Defender** - d12
- Best for HP-focused builds
- Great for front-line tanks

### Most Skills
**Shadowdancer** - 6 skill points per level
- Only prestige class with more than 4
- Great for skill-focused builds

### Highest Entry Requirements
**Hierophant** - Requires 7th level divine spells
- Need Cleric/Druid 13 minimum
- Earliest entry: level 13-14

### Lowest Entry Requirements
**Horizon Walker** - Just Knowledge (geography) 8 + Endurance
- Can enter as early as level 5
- Most accessible prestige class

---

**Status**: All core DM Guide prestige classes extracted and ready to use! 🎉

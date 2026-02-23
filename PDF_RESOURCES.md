# PDF Resources Integration

## 📚 Available Resources

Your `./pdfs/` directory contains a comprehensive D&D 3.5 library:

### Core Rulebooks (3 books)
- ✅ **Player's Handbook** (20MB) - Base classes, feats, skills
- ✅ **Dungeon Master's Guide I** (13MB) - Prestige classes, magic items
- ✅ **Dungeon Master's Guide II** (26MB) - Additional content

### Complete Series (7 books, 184MB total)
- Complete Warrior (17MB)
- Complete Arcane (7.8MB)
- Complete Divine (7.8MB)
- Complete Adventurer (16MB)
- Complete Scoundrel (20MB)
- Complete Mage (47MB)
- Complete Psionic (36MB)

### Supplemental Books (40+ books, ~1.1GB)
See `scripts/pdf-sources.md` for complete list.

## ✅ Data Already Extracted

### Classes: 11/11 Base Classes Complete
All Player's Handbook base classes have been extracted:
1. Barbarian - d12, 4 skill points
2. Bard - d6, 6 skill points
3. Cleric - d8, 2 skill points
4. Druid - d8, 4 skill points
5. Fighter - d10, 2 skill points
6. Monk - d8, 4 skill points
7. Paladin - d10, 2 skill points
8. Ranger - d8, 6 skill points
9. Rogue - d6, 8 skill points
10. Sorcerer - d4, 2 skill points
11. Wizard - d4, 2 skill points

## 📊 Data Extraction Status

| Category | Current | Available | Priority |
|----------|---------|-----------|----------|
| Base Classes | 11/11 | ✅ Complete | - |
| Prestige Classes | 2/~100 | 12 core, 50+ extended | High |
| Feats | 20/~400 | 100 core, 300+ extended | Medium |
| Skills | 15/~100 | 60 core, 100 extended | Medium |

## 🎯 Extraction Priorities

### High Priority (Next Steps)
1. **Core Prestige Classes** (DM Guide I)
   - Arcane Trickster, Assassin, Mystic Theurge
   - These are most commonly used
   - ~2 hours to extract

2. **Combat Feat Chains** (Player's Handbook)
   - Great Cleave, Whirlwind Attack
   - Spring Attack, Shot on the Run
   - ~30 minutes to extract

### Medium Priority
3. **Complete Skills List** (Player's Handbook)
   - Add remaining 45 skills
   - ~30 minutes to extract

4. **Metamagic Feats** (Player's Handbook)
   - Quicken, Still, Silent Spell
   - Essential for casters
   - ~15 minutes to extract

### Low Priority
5. **Complete Series Prestige Classes**
   - 30+ additional options
   - Extract as needed

6. **Specialized Systems**
   - Psionics (Complete Psionic)
   - Tome of Battle maneuvers
   - Extract if users request

## 🛠️ How to Extract Data

### Option 1: AI-Assisted (Recommended)

Install PDF tools first:
```bash
brew install poppler
```

Then use Claude Code to read specific pages:
```
Read pages 100-110 from "pdfs/D&D 3.5 2/DM Guide I.pdf"
and extract the Arcane Trickster prestige class data
```

### Option 2: Manual Extraction

1. Open PDF in Preview/Adobe
2. Navigate to desired class/feat/skill
3. Use JSON template from `scripts/extract-classes.md`
4. Add to appropriate data file
5. Validate JSON syntax

### Option 3: Script-Based (Future)

Create parsers in `scripts/`:
```bash
node scripts/extract-prestige-classes.js "DM Guide I" 100 110
```

## 📁 Where to Add Extracted Data

| Data Type | File Location | Format |
|-----------|---------------|--------|
| Base Classes | `data/classes.json` | JSON array |
| Prestige Classes | `data/prestige-classes.json` | JSON array with requirements |
| Feats | `data/feats.json` | JSON array with prerequisites |
| Skills | `data/skills.json` | JSON array |

## 🔍 Quick Reference: Book Locations

### Classes & Prestige Classes
- **Player's Handbook**: Pages 24-56 (base classes)
- **DM Guide I**: Pages 176-198 (core prestige classes)
- **Complete Warrior**: Pages 10-59 (combat prestige classes)
- **Complete Arcane**: Pages 6-52 (arcane prestige classes)
- **Complete Divine**: Pages 6-50 (divine prestige classes)

### Feats
- **Player's Handbook**: Pages 90-104 (core feats)
- **Complete Warrior**: Pages 104-113 (combat feats)
- **Complete Arcane**: Pages 74-84 (metamagic feats)
- **Complete Divine**: Pages 84-92 (divine feats)

### Skills
- **Player's Handbook**: Pages 66-84 (all standard skills)

## 💡 Pro Tips

1. **Start with Popular Builds**
   - Extract classes/feats for common builds first
   - Example: Arcane Trickster needs Rogue + Wizard + Arcane Trickster prestige

2. **Follow Prerequisites**
   - When extracting a prestige class, also extract required feats
   - Example: Arcane Archer needs Point Blank Shot, Precise Shot, Weapon Focus

3. **Batch Similar Items**
   - Extract all metamagic feats at once
   - Extract all Knowledge skills at once
   - Faster than one-by-one

4. **Validate as You Go**
   - Test in app after each batch
   - Fix any ID mismatches immediately

5. **Use Templates**
   - See `scripts/extract-classes.md` for templates
   - Copy-paste structure, fill in values

## 🎮 Example: Building an Arcane Trickster

**Required Data (check what we have):**
- ✅ Rogue class (base class)
- ✅ Wizard class (base class)
- ❌ Arcane Trickster (prestige class) - NEED TO EXTRACT
- ✅ Various rogue skills (class skills)
- ✅ Disable Device skill (for prerequisites)
- ✅ Concentration skill (for spellcasting)

**Extraction Steps:**
1. Open DM Guide I, page 176
2. Find Arcane Trickster entry
3. Copy to prestige class template
4. Add requirements: skill ranks, spellcasting ability
5. Save to `data/prestige-classes.json`
6. Test in app!

## 📈 Long-Term Vision

### MVP (Current Goal)
- ✅ 11 base classes
- [ ] 12 core prestige classes
- [ ] 50 essential feats
- [ ] 30 core skills

### Extended (Future)
- All Player's Handbook content
- All DM Guide content
- Popular Complete Series options
- 100+ prestige classes total

### Ultimate (Dream)
- All D&D 3.5 content digitized
- PDF parser automates extraction
- User-submitted custom content
- Community-maintained database

## 🚀 Getting Started

1. **Install PDF tools**: `brew install poppler`
2. **Read extraction guide**: `scripts/DATA_EXTRACTION_PLAN.md`
3. **Start with high priority**: Arcane Trickster, Assassin, Mystic Theurge
4. **Test in app** after each extraction
5. **Commit changes** to track progress

---

**Status**: 11 classes ready, 100+ more to extract 📚

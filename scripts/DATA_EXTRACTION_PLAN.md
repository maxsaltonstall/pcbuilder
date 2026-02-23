# D&D 3.5 Data Extraction Plan

## ✅ Current Status

### Classes: 11/11 Base Classes Complete
- Fighter, Wizard, Rogue, Cleric, Ranger
- Barbarian, Bard, Druid, Monk, Paladin, Sorcerer

### Prestige Classes: 2/~50
- Arcane Archer
- Eldritch Knight

### Feats: 20/~100+
- Power Attack tree, Weapon Focus, Archery feats, Metamagic, Save boosters

### Skills: 15/~60
- Core skills for stealth, perception, magic, social, utility

## 📋 Next Extraction Priorities

### Phase 1: Core Prestige Classes (DM Guide I)
**Location:** DM Guide I, Chapter 2 (Prestige Classes)

**Priority List:**
1. Arcane Trickster
2. Assassin
3. Blackguard
4. Dragon Disciple
5. Duelist
6. Dwarven Defender
7. Eldritch Knight (✅ done)
8. Hierophant
9. Horizon Walker
10. Loremaster
11. Mystic Theurge
12. Shadowdancer

**Template for prestige classes:**
```json
{
  "id": "class-name",
  "name": "Class Name",
  "description": "Brief description",
  "hitDie": 0,
  "skillPointsPerLevel": 0,
  "classSkills": ["skill-ids"],
  "baseAttackBonus": "good|average|poor",
  "saves": {
    "fortitude": "good|poor",
    "reflex": "good|poor",
    "will": "good|poor"
  },
  "source": "Dungeon Master's Guide",
  "isPrestige": true,
  "requirements": [
    {
      "type": "skill",
      "description": "8 ranks in Skillname",
      "skillId": "skill-id",
      "minimumRanks": 8
    },
    {
      "type": "feat",
      "description": "Feat Name",
      "featId": "feat-id"
    },
    {
      "type": "baseAttackBonus",
      "description": "Base attack bonus +5",
      "minimumBonus": 5
    }
  ]
}
```

### Phase 2: Expand Feats (Player's Handbook)
**Location:** Player's Handbook, Chapter 5 (Feats)

**Priority Categories:**
1. **Combat Feats** (for fighters)
   - Great Cleave
   - Whirlwind Attack
   - Spring Attack
   - Shot on the Run
   - Manyshot

2. **Spell Feats** (for casters)
   - Spell Penetration
   - Greater Spell Penetration
   - Spell Focus (schools)
   - Quicken Spell
   - Still Spell
   - Silent Spell

3. **Skill Feats**
   - Skill Focus
   - Investigator
   - Negotiator
   - Alertness

### Phase 3: Complete Skills List (Player's Handbook)
**Location:** Player's Handbook, Chapter 4 (Skills)

**Missing Skills:**
- Appraise
- Balance
- Climb
- Craft
- Decipher Script
- Disguise
- Escape Artist
- Forgery
- Gather Information
- Handle Animal
- Heal
- Jump
- Knowledge (all types)
- Perform
- Profession
- Ride
- Sense Motive
- Sleight of Hand
- Speak Language
- Survival
- Swim
- Use Magic Device
- Use Rope

### Phase 4: Complete Series Books

**Complete Warrior** prestige classes:
- Cavalier
- Exotic Weapon Master
- Frenzied Berserker
- Kensai
- Master Thrower
- Order of the Bow Initiate
- Purple Dragon Knight
- Reaping Mauler
- Tactical Soldier
- War Chanter

**Complete Arcane** prestige classes:
- Abjurant Champion
- Battle Sorcerer
- Elemental Savant
- Green Star Adept
- Jade Phoenix Mage
- Master Specialist
- Shadowcraft Mage
- Spellsword
- Sublime Chord
- Ultimate Magus
- Warmage

**Complete Divine** prestige classes:
- Contemplative
- Divine Oracle
- Radiant Servant of Pelor
- Sacred Exorcist
- Shining Blade of Heironeous
- Temple Raider of Olidammara
- Warpriest

## 🛠️ Extraction Tools

### Manual Method (Current)
1. Open PDF in viewer
2. Navigate to class/feat/skill section
3. Copy data into JSON template
4. Validate JSON syntax
5. Add to appropriate data file

### Semi-Automated Method (Future)
```bash
# Install PDF text extraction
brew install poppler

# Extract text from specific pages
pdftotext -f 100 -l 110 "pdfs/D&D 3.5 2/DM Guide I.pdf" output.txt

# Parse with script
node scripts/parse-prestige-classes.js output.txt >> data/prestige-classes.json
```

### AI-Assisted Method (Recommended)
1. Install poppler: `brew install poppler`
2. Use Claude Code with Read tool to view PDF pages
3. Ask Claude to extract data in JSON format
4. Review and commit

## 📊 Data Completeness Goals

### MVP (Minimum Viable Product)
- ✅ 11 base classes
- [ ] 12 core prestige classes (DM Guide)
- [ ] 50 essential feats
- [ ] 30 core skills

### Full Core (Player's Handbook + DMG)
- ✅ 11 base classes
- [ ] 12-15 prestige classes
- [ ] 100+ feats
- [ ] 60+ skills

### Extended (Complete Series)
- ✅ 11 base classes
- [ ] 50+ prestige classes
- [ ] 200+ feats
- [ ] 80+ skills

### Comprehensive (All Books)
- ✅ 11 base classes
- [ ] 100+ prestige classes
- [ ] 400+ feats
- [ ] 100+ skills
- [ ] Variant rules
- [ ] Custom options

## 🎯 Immediate Next Steps

1. **Extract Core Prestige Classes** (1-2 hours)
   - Focus on most popular: Arcane Trickster, Assassin, Mystic Theurge
   - Add to `data/prestige-classes.json`

2. **Expand Feat List** (30 min)
   - Add combat feat chains (Great Cleave, Whirlwind Attack)
   - Add metamagic feats (Quicken, Still, Silent)
   - Add to `data/feats.json`

3. **Complete Skills** (15 min)
   - Add remaining ~45 skills
   - Update `data/skills.json`

4. **Test with Real Builds** (ongoing)
   - Try creating popular builds
   - Identify missing data
   - Extract as needed

## 📝 Quality Checklist

When adding new data, verify:
- [ ] JSON syntax is valid
- [ ] All IDs are lowercase-kebab-case
- [ ] All referenced IDs exist (skills, feats, classes)
- [ ] Prerequisites are complete and accurate
- [ ] Source book is cited
- [ ] Hit die matches official source
- [ ] Skill points per level matches official source
- [ ] BAB/Saves progressions are correct

## 🔄 Continuous Improvement

As you use the app:
1. Note which classes/feats/skills are missing
2. Look up in PDFs
3. Add to data files
4. Commit changes
5. App automatically picks up new data

## 📚 Reference Quick Links

**Player's Handbook Sections:**
- Classes: Pages 24-56
- Skills: Pages 66-84
- Feats: Pages 90-104

**DM Guide I Sections:**
- Prestige Classes: Pages 176-198
- Magic Items: Pages 214-284

**Complete Warrior:**
- Prestige Classes: Pages 10-59
- Feats: Pages 104-113

**Complete Arcane:**
- Prestige Classes: Pages 6-52
- Feats: Pages 74-84
- Spells: Pages 98-173

# Class Data Extraction Guide

## How to Extract Class Data

### Quick Reference Table Location

**Player's Handbook:**
- Base Classes: Pages 24-25 (Table 3-1 through 3-11)
- Class descriptions: Pages 24-56

### Data Template

Use this template for each class:

```json
{
  "id": "class-name-lowercase",
  "name": "Class Name",
  "description": "One sentence description",
  "hitDie": 0,
  "skillPointsPerLevel": 0,
  "classSkills": ["skill-id-1", "skill-id-2"],
  "baseAttackBonus": "good|average|poor",
  "saves": {
    "fortitude": "good|poor",
    "reflex": "good|poor",
    "will": "good|poor"
  },
  "source": "Player's Handbook"
}
```

### Conversion Guide

**Base Attack Bonus:**
- "Good" = +1 per level (Fighter, Ranger, Paladin, Barbarian)
- "Average" = +3/4 per level (Cleric, Druid, Monk, Rogue, Bard)
- "Poor" = +1/2 per level (Wizard, Sorcerer)

**Saves:**
- "Good" = +2 base at 1st level, +1 per 2 levels
- "Poor" = +0 base at 1st level, +1 per 3 levels

## Missing Base Classes (Priority Order)

### 1. Barbarian (PHB p.24)
```json
{
  "id": "barbarian",
  "name": "Barbarian",
  "description": "A fierce warrior of primitive background who can enter a battle rage.",
  "hitDie": 12,
  "skillPointsPerLevel": 4,
  "classSkills": [
    "climb", "craft", "handle-animal", "intimidate", "jump",
    "listen", "ride", "survival", "swim"
  ],
  "baseAttackBonus": "good",
  "saves": {
    "fortitude": "good",
    "reflex": "poor",
    "will": "poor"
  },
  "source": "Player's Handbook"
}
```

### 2. Bard (PHB p.28)
```json
{
  "id": "bard",
  "name": "Bard",
  "description": "A performer whose music works magic, and a jack-of-all-trades.",
  "hitDie": 6,
  "skillPointsPerLevel": 6,
  "classSkills": [
    "appraise", "balance", "bluff", "climb", "concentration", "craft",
    "decipher-script", "diplomacy", "disguise", "escape-artist", "gather-information",
    "hide", "jump", "knowledge-all", "listen", "move-silently", "perform",
    "profession", "sense-motive", "sleight-of-hand", "speak-language", "spellcraft",
    "swim", "tumble", "use-magic-device"
  ],
  "baseAttackBonus": "average",
  "saves": {
    "fortitude": "poor",
    "reflex": "good",
    "will": "good"
  },
  "source": "Player's Handbook"
}
```

### 3. Druid (PHB p.33)
```json
{
  "id": "druid",
  "name": "Druid",
  "description": "A divine spellcaster who draws power from nature and can wild shape.",
  "hitDie": 8,
  "skillPointsPerLevel": 4,
  "classSkills": [
    "concentration", "craft", "diplomacy", "handle-animal", "heal",
    "knowledge-nature", "listen", "profession", "ride", "spellcraft",
    "spot", "survival", "swim"
  ],
  "baseAttackBonus": "average",
  "saves": {
    "fortitude": "good",
    "reflex": "poor",
    "will": "good"
  },
  "source": "Player's Handbook"
}
```

### 4. Monk (PHB p.39)
```json
{
  "id": "monk",
  "name": "Monk",
  "description": "A martial artist whose unarmed strikes are as powerful as weapons.",
  "hitDie": 8,
  "skillPointsPerLevel": 4,
  "classSkills": [
    "balance", "climb", "concentration", "craft", "diplomacy",
    "escape-artist", "hide", "jump", "knowledge-arcana", "knowledge-religion",
    "listen", "move-silently", "perform", "profession", "sense-motive",
    "spot", "swim", "tumble"
  ],
  "baseAttackBonus": "average",
  "saves": {
    "fortitude": "good",
    "reflex": "good",
    "will": "good"
  },
  "source": "Player's Handbook"
}
```

### 5. Paladin (PHB p.42)
```json
{
  "id": "paladin",
  "name": "Paladin",
  "description": "A champion of justice and destroyer of evil, protected and strengthened by divine power.",
  "hitDie": 10,
  "skillPointsPerLevel": 2,
  "classSkills": [
    "concentration", "craft", "diplomacy", "handle-animal", "heal",
    "knowledge-nobility", "knowledge-religion", "profession", "ride",
    "sense-motive"
  ],
  "baseAttackBonus": "good",
  "saves": {
    "fortitude": "good",
    "reflex": "poor",
    "will": "poor"
  },
  "source": "Player's Handbook"
}
```

### 6. Sorcerer (PHB p.50)
```json
{
  "id": "sorcerer",
  "name": "Sorcerer",
  "description": "A spellcaster who draws on inherent magic from a gift or bloodline.",
  "hitDie": 4,
  "skillPointsPerLevel": 2,
  "classSkills": [
    "bluff", "concentration", "craft", "knowledge-arcana", "profession",
    "spellcraft"
  ],
  "baseAttackBonus": "poor",
  "saves": {
    "fortitude": "poor",
    "reflex": "poor",
    "will": "good"
  },
  "source": "Player's Handbook"
}
```

## How to Add These

1. Open `data/classes.json`
2. Add a comma after the last Ranger entry
3. Copy the new class JSON from above
4. Save the file
5. Restart the app to see the new classes

## Validation

After adding, verify:
- ✅ JSON is valid (no syntax errors)
- ✅ All skill IDs match entries in `data/skills.json`
- ✅ Hit die is correct (d4, d6, d8, d10, or d12)
- ✅ Skill points per level is correct
- ✅ BAB progression matches class type

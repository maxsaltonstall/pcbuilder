#!/bin/bash

# Add missing base classes to classes.json
# This script will append the 6 missing classes from Player's Handbook

echo "Adding missing base classes to data/classes.json..."

# Backup the original file
cp data/classes.json data/classes.json.backup

# Read the current file, remove the closing bracket, add new classes, add closing bracket
cat > data/classes-temp.json << 'EOF'
[
  {
    "id": "fighter",
    "name": "Fighter",
    "description": "A master of combat, skilled with a variety of weapons and armor.",
    "hitDie": 10,
    "skillPointsPerLevel": 2,
    "classSkills": ["climb", "craft", "handle-animal", "intimidate", "jump", "ride", "swim"],
    "baseAttackBonus": "good",
    "saves": {
      "fortitude": "good",
      "reflex": "poor",
      "will": "poor"
    },
    "source": "Player's Handbook"
  },
  {
    "id": "wizard",
    "name": "Wizard",
    "description": "A powerful arcane spellcaster who studies magical arts.",
    "hitDie": 4,
    "skillPointsPerLevel": 2,
    "classSkills": ["concentration", "craft", "decipher-script", "knowledge-arcana", "knowledge-all", "profession", "spellcraft"],
    "baseAttackBonus": "poor",
    "saves": {
      "fortitude": "poor",
      "reflex": "poor",
      "will": "good"
    },
    "source": "Player's Handbook"
  },
  {
    "id": "rogue",
    "name": "Rogue",
    "description": "A skilled thief and scout, master of stealth and deception.",
    "hitDie": 6,
    "skillPointsPerLevel": 8,
    "classSkills": ["appraise", "balance", "bluff", "climb", "craft", "decipher-script", "diplomacy", "disable-device", "disguise", "escape-artist", "forgery", "gather-information", "hide", "intimidate", "jump", "listen", "move-silently", "open-lock", "perform", "profession", "search", "sense-motive", "sleight-of-hand", "spot", "swim", "tumble", "use-magic-device", "use-rope"],
    "baseAttackBonus": "average",
    "saves": {
      "fortitude": "poor",
      "reflex": "good",
      "will": "poor"
    },
    "source": "Player's Handbook"
  },
  {
    "id": "cleric",
    "name": "Cleric",
    "description": "A divine spellcaster who channels the power of a deity.",
    "hitDie": 8,
    "skillPointsPerLevel": 2,
    "classSkills": ["concentration", "craft", "diplomacy", "heal", "knowledge-arcana", "knowledge-history", "knowledge-religion", "knowledge-planes", "profession", "spellcraft"],
    "baseAttackBonus": "average",
    "saves": {
      "fortitude": "good",
      "reflex": "poor",
      "will": "good"
    },
    "source": "Player's Handbook"
  },
  {
    "id": "ranger",
    "name": "Ranger",
    "description": "A skilled woodsman and tracker who defends the wilderness.",
    "hitDie": 8,
    "skillPointsPerLevel": 6,
    "classSkills": ["climb", "concentration", "craft", "handle-animal", "heal", "hide", "jump", "knowledge-dungeoneering", "knowledge-geography", "knowledge-nature", "listen", "move-silently", "profession", "ride", "search", "spot", "survival", "swim", "use-rope"],
    "baseAttackBonus": "good",
    "saves": {
      "fortitude": "good",
      "reflex": "good",
      "will": "poor"
    },
    "source": "Player's Handbook"
  },
  {
    "id": "barbarian",
    "name": "Barbarian",
    "description": "A fierce warrior of primitive background who can enter a battle rage.",
    "hitDie": 12,
    "skillPointsPerLevel": 4,
    "classSkills": ["climb", "craft", "handle-animal", "intimidate", "jump", "listen", "ride", "survival", "swim"],
    "baseAttackBonus": "good",
    "saves": {
      "fortitude": "good",
      "reflex": "poor",
      "will": "poor"
    },
    "source": "Player's Handbook"
  },
  {
    "id": "bard",
    "name": "Bard",
    "description": "A performer whose music works magic, and a jack-of-all-trades.",
    "hitDie": 6,
    "skillPointsPerLevel": 6,
    "classSkills": ["appraise", "balance", "bluff", "climb", "concentration", "craft", "decipher-script", "diplomacy", "disguise", "escape-artist", "gather-information", "hide", "jump", "knowledge-all", "listen", "move-silently", "perform", "profession", "sense-motive", "sleight-of-hand", "speak-language", "spellcraft", "swim", "tumble", "use-magic-device"],
    "baseAttackBonus": "average",
    "saves": {
      "fortitude": "poor",
      "reflex": "good",
      "will": "good"
    },
    "source": "Player's Handbook"
  },
  {
    "id": "druid",
    "name": "Druid",
    "description": "A divine spellcaster who draws power from nature and can wild shape.",
    "hitDie": 8,
    "skillPointsPerLevel": 4,
    "classSkills": ["concentration", "craft", "diplomacy", "handle-animal", "heal", "knowledge-nature", "listen", "profession", "ride", "spellcraft", "spot", "survival", "swim"],
    "baseAttackBonus": "average",
    "saves": {
      "fortitude": "good",
      "reflex": "poor",
      "will": "good"
    },
    "source": "Player's Handbook"
  },
  {
    "id": "monk",
    "name": "Monk",
    "description": "A martial artist whose unarmed strikes are as powerful as weapons.",
    "hitDie": 8,
    "skillPointsPerLevel": 4,
    "classSkills": ["balance", "climb", "concentration", "craft", "diplomacy", "escape-artist", "hide", "jump", "knowledge-arcana", "knowledge-religion", "listen", "move-silently", "perform", "profession", "sense-motive", "spot", "swim", "tumble"],
    "baseAttackBonus": "average",
    "saves": {
      "fortitude": "good",
      "reflex": "good",
      "will": "good"
    },
    "source": "Player's Handbook"
  },
  {
    "id": "paladin",
    "name": "Paladin",
    "description": "A champion of justice and destroyer of evil, protected and strengthened by divine power.",
    "hitDie": 10,
    "skillPointsPerLevel": 2,
    "classSkills": ["concentration", "craft", "diplomacy", "handle-animal", "heal", "knowledge-nobility", "knowledge-religion", "profession", "ride", "sense-motive"],
    "baseAttackBonus": "good",
    "saves": {
      "fortitude": "good",
      "reflex": "poor",
      "will": "poor"
    },
    "source": "Player's Handbook"
  },
  {
    "id": "sorcerer",
    "name": "Sorcerer",
    "description": "A spellcaster who draws on inherent magic from a gift or bloodline.",
    "hitDie": 4,
    "skillPointsPerLevel": 2,
    "classSkills": ["bluff", "concentration", "craft", "knowledge-arcana", "profession", "spellcraft"],
    "baseAttackBonus": "poor",
    "saves": {
      "fortitude": "poor",
      "reflex": "poor",
      "will": "good"
    },
    "source": "Player's Handbook"
  }
]
EOF

mv data/classes-temp.json data/classes.json

echo "✅ Done! All 11 base classes now in data/classes.json"
echo "Backup saved to data/classes.json.backup"

# Complete Skills List - D&D 3.5

**Date**: 2026-02-22
**Status**: ✅ All 45 skills extracted from Player's Handbook

---

## Overview

The `data/skills.json` file now contains all 45 D&D 3.5 skills from the Player's Handbook (pages 66-88) with complete attributes.

---

## Skills by Ability Score

### Strength (3 skills)
- Climb
- Jump
- Swim

### Dexterity (9 skills)
- Balance
- Escape Artist
- Hide
- Move Silently
- Open Lock
- Ride
- Sleight of Hand
- Tumble
- Use Rope

### Constitution (1 skill)
- Concentration

### Intelligence (17 skills)
- Appraise
- Craft
- Decipher Script (trained only)
- Disable Device (trained only)
- Forgery
- Knowledge (Arcana) (trained only)
- Knowledge (Architecture and Engineering) (trained only)
- Knowledge (Dungeoneering) (trained only)
- Knowledge (Geography) (trained only)
- Knowledge (History) (trained only)
- Knowledge (Local) (trained only)
- Knowledge (Nature) (trained only)
- Knowledge (Nobility and Royalty) (trained only)
- Knowledge (Religion) (trained only)
- Knowledge (The Planes) (trained only)
- Search
- Spellcraft (trained only)

### Wisdom (6 skills)
- Heal
- Listen
- Profession (trained only)
- Sense Motive
- Spot
- Survival

### Charisma (8 skills)
- Bluff
- Diplomacy
- Disguise
- Gather Information
- Handle Animal (trained only)
- Intimidate
- Perform
- Use Magic Device (trained only)

### None (1 skill)
- Speak Language (trained only)

---

## Special Properties

### Trained Only (20 skills)
These skills cannot be used untrained:
- Decipher Script
- Disable Device
- Handle Animal
- Knowledge (all 10 types)
- Open Lock
- Profession
- Sleight of Hand
- Speak Language
- Spellcraft
- Tumble
- Use Magic Device

### Armor Check Penalty (9 skills)
These skills are affected by armor check penalty:
- Balance
- Climb
- Escape Artist
- Hide
- Jump
- Move Silently
- Sleight of Hand
- Swim
- Tumble

---

## Data Structure

Each skill in `data/skills.json` has:

```json
{
  "id": "skill-id",
  "name": "Skill Name",
  "description": "What this skill is used for",
  "keyAbility": "str|dex|con|int|wis|cha|none",
  "trainedOnly": true|false,
  "armorCheckPenalty": true|false,
  "source": "Player's Handbook"
}
```

---

## Usage in App

Skills are now available in:
1. **Goal Setting step** - Select key skills for optimization
2. **Optimization engine** - Maximizes ranks in selected skills
3. **Skill calculator** - Calculates max ranks (level + 3 for class skills)
4. **Character sheet** - Display skill ranks and modifiers

---

## Statistics

- **Total skills**: 45
- **Trained only**: 20 (44%)
- **Armor check penalty**: 9 (20%)
- **Most common ability**: Intelligence (17 skills)
- **Least common ability**: Constitution (1 skill)

---

**Status**: Complete! All D&D 3.5 core skills are now in the app. 🎲

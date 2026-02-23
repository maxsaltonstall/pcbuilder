# Available D&D 3.5 PDF Sources

## Core Books
- ✅ **Player's Handbook** (20MB) - Base classes, feats, skills
- ✅ **DM Guide I** (13MB) - Prestige classes, magic items
- ✅ **DM Guide II** (26MB) - Additional prestige classes
- Rules Compendium (10MB) - Consolidated rules

## Complete Series (Character Options)
- ✅ **Complete Warrior** (17MB) - Fighter, Barbarian, Ranger, etc.
- ✅ **Complete Arcane** (7.8MB) - Wizard, Sorcerer, Bard arcane options
- ✅ **Complete Divine** (7.8MB) - Cleric, Druid, Paladin divine options
- ✅ **Complete Adventurer** (16MB) - Rogue, Scout, Ranger options
- ✅ **Complete Scoundrel** (20MB) - Rogue and skill-focused options
- ✅ **Complete Mage** (47MB) - Advanced arcane options
- ✅ **Complete Psionic** (36MB) - Psionics system

## Specialized Books
- Expanded Psionics (60MB)
- Tome of Battle: Book of Nine Swords (33MB)
- Tome of Magic (54MB)
- Magic Item Compendium (58MB)
- Spell Compendium (7.2MB)
- Unearthed Arcana (6.9MB)

## Races
- Races of Destiny (13MB)
- Races of Stone (7.9MB)
- Races of the Dragon (17MB)
- Races of the Wild (12MB)
- Savage Species (4.5MB)

## Setting-Specific
- Book of Exalted Deeds (5.1MB)
- Book of Vile Darkness (11MB)
- Draconomicon (7.2MB)
- Dragon Magic (50MB)
- Fiend Folio (5.1MB)
- Libris Mortis (111MB)
- Magic of Incarnum (69MB)

## Environment Books
- Frostburn (7.1MB)
- Sandstorm (23MB)
- Stormwrack (21MB)

## Priority for Data Extraction

### Phase 1 (Core) - Extract First
1. **Player's Handbook** - All base classes, core feats, all skills
2. **DM Guide I** - Core prestige classes (Arcane Archer, Arcane Trickster, etc.)

### Phase 2 (Expanded Options)
3. **Complete Warrior** - Fighter variants, prestige classes
4. **Complete Arcane** - Wizard/Sorcerer options
5. **Complete Divine** - Cleric/Druid options

### Phase 3 (Advanced)
6. Other Complete series books
7. Specialized systems (Psionics, Tome of Battle)

## Extraction Strategy

For each book, we need to extract:

### Classes
- Name, description
- Hit die, skill points per level
- Class skills list
- Base attack bonus progression
- Save progressions (Fort/Ref/Will)

### Prestige Classes
- All of the above, plus:
- Requirements (skills, feats, BAB, special)
- Entry level (when can first enter)

### Feats
- Name, description
- Prerequisites (ability scores, feats, BAB, skills)
- Benefits
- Type (General, Fighter Bonus, Metamagic, etc.)

### Skills
- Name, description
- Key ability
- Trained only flag
- Armor check penalty flag

## Current Data Coverage

From manual entry, we have:
- 5/11 base classes (missing: Barbarian, Bard, Druid, Monk, Paladin, Sorcerer)
- 2/~50 prestige classes
- 20/~100+ feats
- 15/~60 skills

## Next Steps

1. Extract remaining base classes from Player's Handbook
2. Extract core prestige classes from DM Guide
3. Expand feat list (Power Attack tree, metamagic, etc.)
4. Complete skill list
5. Add Complete series options

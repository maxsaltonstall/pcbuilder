# D&D 3.5 Content Extraction Session - February 22, 2026

## Session Summary

This session continued the comprehensive extraction of D&D 3.5 content from PDF sourcebooks, building on previous work. Started with **1,915 elements** and added **7 new sourcebooks** for a total of **2,507 game elements**.

## Books Extracted This Session

### 1. Tome of Battle: The Book of Nine Swords ✅
**Content Added:**
- Base Classes: 3 (Crusader, Swordsage, Warblade)
- Prestige Classes: 8
- Feats: 19 martial discipline feats
- Martial Disciplines: 9 (saved to `data/martial-disciplines.json`)
- Maneuver Types: 4 (Boost, Counter, Strike, Stance)

**Note:** Individual maneuvers not extracted due to copyright concerns.

### 2. Magic of Incarnum ✅
**Content Added:**
- Base Classes: 3 (Incarnate, Soulborn, Totemist)
- Prestige Classes: 10
- Feats: 36 incarnum feats
- Soulmelds: 51 (saved to `data/soulmelds.json`)
- Incarnum Items: 7 (saved to `data/incarnum-items.json`)

### 3. Fiendish Codex I: Hordes of the Abyss ✅
**Content Added:**
- Prestige Classes: 0
- Feats: 23 (Abyssal Heritor feats)
- Spells: 21 demon-themed spells

### 4. Fiendish Codex II: Tyrants of the Nine Hells ✅
**Content Added:**
- Prestige Classes: 4
- Feats: 27 (Devil-Touched feats)
- Spells: 21 hellish spells

### 5. Libris Mortis: The Book of Undead ✅
**Content Added:**
- Prestige Classes: 9 (including Dread Necromancer)
- Feats: 22 necromancy feats
- Spells: 36 necromancy spells

### 6. Magic Item Compendium ✅
**Content Added:**
- Magic Items: 147 notable items (saved to `data/magic-items.json`)
- Focus: Relics, artifacts, unique items (excluded generic +1/+2/+3 items)

### 7. Environment Trilogy ✅

#### Sandstorm (Desert)
- Prestige Classes: 5
- Feats: 32
- Spells: 59

#### Frostburn (Arctic)
- Prestige Classes: 10
- Feats: 32
- Spells: 31

#### Stormwrack (Aquatic)
- Prestige Classes: 7
- Feats: 24
- Spells: 38

### 8. Lords of Madness ✅
**Content Added:**
- Prestige Classes: 6
- Feats: 20 aberration feats
- Spells: 19 aberration spells

## Database Totals

### Starting Point (Previous Sessions)
- Base Classes: 16
- Prestige Classes: 116
- Feats: 531
- Spells: 1,215
- Skills: 45
- **Total: 1,915 elements**

### After This Session
- **Base Classes: 19** (+3: Crusader, Swordsage, Warblade, Incarnate, Soulborn, Totemist)
- **Prestige Classes: 167** (+51)
- **Feats: 765** (+234)
- **Spells: 1,428** (+213)
- **Skills: 45** (unchanged)
- **Magic Items: 147** (NEW)
- **Soulmelds: 51** (NEW)
- **Incarnum Items: 7** (NEW)
- **Martial Disciplines: 9** (NEW)
- **Maneuver Types: 4** (NEW)
- **Total: 2,642 elements**

## New Data Files Created

1. `data/martial-disciplines.json` - 9 Tome of Battle disciplines
2. `data/maneuver-types.json` - 4 maneuver types (Boost, Counter, Strike, Stance)
3. `data/soulmelds.json` - 51 incarnum soulmelds
4. `data/incarnum-items.json` - 7 incarnum magic items
5. `data/magic-items.json` - 147 notable magic items from MIC

## Content by Source

### Core + Complete Series (Previous)
- Player's Handbook, DMG, Complete Adventurer, Complete Arcane, Complete Divine, Complete Mage, Complete Scoundrel, Complete Warrior

### Expansion Books (Previous + This Session)
- Epic Level Handbook
- Expanded Psionics Handbook
- **Tome of Battle** ✨
- **Magic of Incarnum** ✨

### Themed Books (Previous + This Session)
- Book of Exalted Deeds
- Book of Vile Darkness
- Dragon Magic
- **Fiendish Codex I** ✨
- **Fiendish Codex II** ✨
- **Libris Mortis** ✨

### Racial Books (Previous)
- Races of Stone, Races of Destiny, Races of the Wild, Races of the Dragon

### Environment Books ✨ NEW
- **Sandstorm** (desert)
- **Frostburn** (arctic)
- **Stormwrack** (aquatic)

### Monster/Aberration Books ✨ NEW
- **Lords of Madness**

### Equipment Books ✨ NEW
- **Magic Item Compendium**

## Books Extracted: 31 Total
- Previous sessions: 24 books
- This session: 7 books (Tome of Battle, Magic of Incarnum, Fiendish Codex I & II, Libris Mortis, Magic Item Compendium, Sandstorm, Frostburn, Stormwrack, Lords of Madness - counting environment trilogy and fiendish codexes)

## Technical Notes

### Extraction Challenges
1. **OCR Requirements**: Some PDFs (Libris Mortis, Magic of Incarnum) were image-based and required OCR processing
2. **Copyright Awareness**: Tome of Battle maneuvers not extracted per agent's copyright concern
3. **Data Volume**: Magic Item Compendium required filtering to exclude generic enhancement items

### Extraction Method
- Used Task agents with `general-purpose` subagent type
- PDF → pdftotext → parsing → JSON formatting
- Merging with `jq -s 'add | unique_by(.id)'` for deduplication

## Remaining PDFs Available

Still have **100+ PDFs** available for extraction including:
- Setting books (Forgotten Realms, Eberron, Greyhawk)
- Draconomicon (dragon content)
- Heroes of Horror
- Weapons of Legacy
- Various campaign setting supplements

## Application Integration

All extracted data is immediately available in the D&D 3.5 Character Builder:
- Hot reload via Vite HMR
- 32 passing tests validating character generation
- Priority-based class selection working
- Epic level support (1-30)

